"""Create database models to represent tables."""
from events_app import db
from sqlalchemy.orm import backref
import enum

class Event_Type(enum.Enum):
    PARTY = "Party"
    STUDY = "Study Session"
    NETWORKING = "Networking"
    GROUP_CRYING_SESSION = "Group Crying Session"

# TODO: Create a model called `Guest` with the following fields:
# - id: primary key
# - name: String column
# - email: String column
# - phone: String column
# - events_attending: relationship to "Event" table with a secondary table

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    events_attending = db.relationship('Event', secondary='event_guests', back_populates='guests')
    
    def __str__(self):
        return f'<ID: {self.id}>, <Name: {self.name}>, <Email: {self.email}>, <Phone: {self.phone}>'

# TODO: Create a model called `Event` with the following fields:
# - id: primary key
# - title: String column
# - description: String column
# - date_and_time: DateTime column
# - guests: relationship to "Guest" table with a secondary table

# STRETCH CHALLENGE: Add a field `event_type` as an Enum column that denotes the
# type of event (Party, Study, Networking, etc)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date_and_time = db.Column(db.DateTime, nullable=False)
    event_type = db.Column(db.Enum(Event_Type), default=Event_Type.NETWORKING, nullable=False)
    guests = db.relationship ('Guest', secondary='event_guests', back_populates='events_attending')

    def __str__(self):
        return f'<ID: {self.id}>, <Title: {self.title}>, <Description: {self.description}>, <Date and time: {self.date_and_time}>, <Event Type: {self.event_type}>'

# TODO: Create a table `guest_event_table` with the following columns:
# - event_id: Integer column (foreign key)
# - guest_id: Integer column (foreign key)

guest_event_table = db.Table('event_guests',
    db.Column('guest_id', db.Integer, db.ForeignKey('guest.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)