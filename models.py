from sqlalchemy import Integer, Column, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.event import listen
from sqlalchemy.ext.declarative import declarative_base

from lab7.app import db

#declears a pokemon model
class Pokemon(db.Model):
    __tablename__='pokemon'
    id = Column(Integer, primary_key=True, autoincrement="auto")
    name=Column(String(100))
    hp=Column(String(4))
    type_1=Column(String(20))
    type_2=Column(String(20))
    attack=Column(Integer)
    defense=Column(Integer)
    special_attack=Column(Integer)
    special_defense=Column(Integer)
    total=Column(Integer)
    speed=Column(Integer)
    date_created=Column(DateTime(), server_default=func.now())



    #takes json data and puts it into the object attributes
    def fromJSON(self, json_rec):
        if 'name' in json_rec:
            self.name = json_rec['name']
        else:
            raise Exception('The name field is required')

        self.hp = json_rec['hp'] if 'hp' in json_rec else ''
        self.type_1 = json_rec['type_1'] if 'type_1' in json_rec else ''
        self.type_2 = json_rec['type_2'] if 'type_2' in json_rec else ''
        self.attack = json_rec['attack'] if 'attack' in json_rec else 0
        self.defense = json_rec['defense'] if 'defense' in json_rec else 0
        self.special_attack = json_rec['sp_atk'] if 'sp_atk' in json_rec else 0
        self.special_defense= json_rec['sp_def'] if 'sp_def' in json_rec else 0
        self.total = json_rec['total'] if 'total' in json_rec else 0
        self.speed = json_rec['speed'] if 'speed' in json_rec else 0


    #pushes pokemon to a dictionary of all pokemon objects 
    def toDict(self):
        return {
            'id': self.id,
            'name': self.name,
            'hp':self.hp,
            'type_1':self.type_1,
            'type_2':self.type_2,
            'attack':self.attack,
            'defense':self.defense,
            'special_attack':self.special_attack,
            'special_defense':self.special_defense,
            'total':self.total,
            'speed':self.speed,
            'date_created': str(self.date_created) # TODO Convert to controlled date format
        }

#
def load_pkfile_into_table(target, connection, **kw):
    import json

    with open('pokedata.json') as fp:
        full_data = fp.read()
        fp.close()
        json_data = json.loads(full_data)
    print("Found {0} records".format(len(json_data)))
    for rec in json_data:
        rec_details = rec['fields']
        p = Pokemon()
        p.fromJSON(rec_details)
        db.session.add(p)
    db.session.commit()


listen(Pokemon.__table__, 'after_create', load_pkfile_into_table)