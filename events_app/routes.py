"""Import packages and modules."""
import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from events_app.models import Event, Guest, Event_Type

# Import app and db from events_app package so that we can run app
from events_app import app, db

main = Blueprint('main', __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def index():
    """Show upcoming events to users!"""
    events = Event.query.all()
    # TODO: Get all events and send to the template
    context = {
        'events': events
    }
    return render_template('index.html', **context)

@main.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new event."""
    event_enums = list(Event_Type)
    print("event enums")
    print(event_enums)
    event_types = []
    for enum in event_enums:
        event_types.append(enum.name)
    print(event_types)

    context = {
        'event_types': event_types
    }

    if request.method == 'POST':
        new_event_title = request.form.get('title')
        new_event_description = request.form.get('description')
        date = request.form.get('date')
        time = request.form.get('time')
        new_event_type = request.form.get('event_type')
        print("new event type")
        print(new_event_type)

        try:
            new_date_and_time = datetime.strptime(
                f'{date} {time}',
                '%Y-%m-%d %H:%M')
        except ValueError:
            return render_template('create.html', **context,
                error='Incorrect datetime format! Please try again.')

        # TODO: Create a new event with the given title, description, & 
        # datetime, then add and commit to the database

        new_event = Event(title=new_event_title, description=new_event_description, date_and_time=new_date_and_time, event_type=new_event_type)
        db.session.add(new_event)
        db.session.commit()

        flash('Event created.')
        return redirect(url_for('main.index'))
    else:
        return render_template('create.html', **context)

@main.route('/event/<event_id>', methods=['GET'])
def event_detail(event_id):
    """Show a single event."""
    event = Event.query.filter_by(id=event_id).one()

    context = {
        'event': event
    }
    # TODO: Get the event with the given id and send to the template
    
    return render_template('event_detail.html', **context)

@main.route('/event/<event_id>', methods=['POST'])
def rsvp(event_id):
    """RSVP to an event."""
    # TODO: Get the event with the given id from the database
    is_returning_guest = request.form.get('returning')
    guest_name = request.form.get('guest_name')
    current_event = Event.query.filter_by(id=event_id).one()

    context = {
        'event': current_event
    }

    if is_returning_guest:
        # TODO: Look up the guest by name. If the guest doesn't exist in the 
        # database, render the event_detail.html template, and pass in an error
        # message as `error`.

        # TODO: If the guest does exist, add the event to their 
        # events_attending, then commit to the database.
        new_guest = Guest.query.filter_by(name=guest_name).first()
        if new_guest:
            current_event.guests.append(new_guest)
            db.session.commit()
        else:
            return render_template('event_detail.html', **context, error='error')
    else:
        guest_email = request.form.get('email')
        guest_phone = request.form.get('phone')

        # TODO: Create a new guest with the given name, email, and phone, and 
        # add the event to their events_attending, then commit to the database.

        new_guest = Guest(name=guest_name, email=guest_email, phone=guest_phone)
        db.session.add(new_guest)
        current_event.guests.append(new_guest)
        db.session.commit()

    flash('You have successfully RSVP\'d! See you there!')
    return redirect(url_for('main.event_detail', event_id=event_id))

@main.route('/guest/<guest_id>')
def guest_detail(guest_id):
    # TODO: Get the guest with the given id and send to the template
    guest = Guest.query.filter_by(id=guest_id).one()
    context = {
        'guest': guest
    }
    return render_template('guest_detail.html', **context)
