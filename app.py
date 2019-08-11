import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc, asc

db = "hawaii.sqlite"

engine = create_engine(f"sqlite:///{db}", echo=False)
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

from flask import Flask, jsonify

app = Flask(__name__)
@app.route("/")
def home():
    print('Server received request for "Home" page...')
    return (
        f"Welcome to The climate app!<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# Precipitations
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    q = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    dic = {}
    for row in q:
        dic[row._asdict()['date']] = row._asdict()['prcp']
    return jsonify(dic)

# Stations

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    q = session.query(Station.station, Station.name).all()
    session.close()
    a = []
    for row in q:
        a.append(row._asdict())
    return jsonify(a)

# Tobs
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    last_date = session.query(Measurement.date).order_by(desc(Measurement.date)).first()[0]
    one_year = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)
    q = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date.between(one_year, last_date)).order_by(desc(Measurement.date)).all()
    session.close()
    a = []
    for row in q:
        a.append(row._asdict())
    return jsonify(a)



@app.route("/api/v1.0/<start>")
def date_start(start):
    session = Session(engine)
    q = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()
    a = {}
    a['Min Temperature'] = q[0][0]
    a['Max Temperature'] = q[0][1]
    a['Avg Temperature'] = q[0][2]
    return jsonify(a)

@app.route("/api/v1.0/<start>/<end>")
def date_start_end(start, end):
    session = Session(engine)
    q = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date.between(start, end)).all()
    session.close()
    a = {}
    a['Min Temperature'] = q[0][0]
    a['Max Temperature'] = q[0][1]
    a['Avg Temperature'] = q[0][2]
    return jsonify(a)
if __name__ == "__main__":
    app.run(debug=True)
