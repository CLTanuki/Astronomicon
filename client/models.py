__author__ = 'cltanuki'
from pony.orm import *
from datetime import date

db = Database('sqlite', 'sat.sqlite', create_db=True)


class Satellite(db.Entity):
    title = Required(str)
    sync = Required(date)
    active = Required(bool, default=False)
