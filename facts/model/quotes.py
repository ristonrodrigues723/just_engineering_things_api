import datetime as dt

from marshmallow import Schema,fields

class Quotes(object):
    def __init__(self, varient, content, type):
        self.varient=varient
        self.content=content
        self.created_at=dt.datetme.now()
        self.type=type

    def __repr__(self):
        return '<Quotes(name={self.description!r})> '.format(self=self)

class QuoteSchema(Schema):
    varient =fields.Str()
    content =fields.Str()
    created_at = fields.Date()
    type = fields.Str()

class JokeSchema(Schema):
    varient = fields.Str()
    content =fields.Str()
    created_at =fields.Date()

class FactSchema(Schema):
    varient = fields.Str()
    content = fields.Str()
    created_at =fields.Date()

    
