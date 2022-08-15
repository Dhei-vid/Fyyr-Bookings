#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from concurrent.futures.process import _python_exit
import json
from lib2to3.pgen2.pgen import generate_grammar
from venv import create
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import collections
import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
import sys




#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


collections.Callable = collections.abc.Callable

# TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/fyyr'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    # genres = db.Column(db.String(120))
    genres = db.Column(ARRAY(db.String(120)))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(500))
    looking_for_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship("Show", backref="venues", lazy=False, cascade="all, delete-orphan")

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    # genres = db.Column(db.String(120))
    genres = db.Column(ARRAY(db.String(120)))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(500))
    looking_for_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship("Show", backref="artists", lazy=False, cascade="all, delete-orphan")

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    def __repr__(self):
      return f'<Artist {self.id} {self.name} {self.city}>'

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__ = "Show"
  id = db.Column(db.Integer, primary_key=True)
  artistID = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  venueID = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  startTime = db.Column(DateTime, default=datetime.datetime.utcnow)
  

def __repr__(self):
    return f'<Show {self.id}, artist {self.artistID}, venue {self.venueID}>'

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  # date = dateutil.parser.parse(value)
  if isinstance(value, str):
        date = dateutil.parser.parse(value)
  else:
      date = value

  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.  
  
  #Return o implement show and number of shows
  
  venuesAll = Venue.query.distinct(Venue.city, Venue.state).all()
  
  data = []
  for venues in venuesAll:
      city_state = {
        "city" : venues.city,
        "state" : venues.state,
        "venues": []
      }
      venue = Venue.query.filter_by(city=venues.city, state=venues.state).all()
      # upcoming_shows = Show.query.filter(Show.venue_id == venue.id).filter(Show.start_time > datetime.now()).count()

      for venue_data in venue:
         city_state["venues"].append({
            "id": venue_data.id,
            "name": venue_data.name,
            # "num_upcoming_shows": upcoming_shows
          })
      data.append(city_state)


  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  data = Venue.query.get(venue_id)

  # if data["genres"] is not None:
  setattr(data, "genres", data.genres.split(","))

  
  

  past_shows = list(filter(lambda show: show.startTime < datetime.datetime.now(), data.shows))
  upcoming_shows = list(filter(lambda show: show.startTime > datetime.datetime.now(), data.shows))

  # Getting the past shows
  past_show = []
  for show in past_shows:
      past = {
        "artist_id": show.artists.id,
        "artist_name": show.artists.name,
        "artist_image_link": show.artists.image_link,
        "start_time": show.startTime
      }

      past_show.append(past)

      setattr(data, "past_shows", past_show)
  setattr(data, "past_shows_count", len(past_show))

  # Getting the upcoming shows
  upcoming_show = []
  for show in upcoming_shows:
    upcoming = {
      "artist_id": show.artists.id,
      "artist_name": show.artists.name,
      "artist_image_link": show.artists.image_link,
      "start_time": show.startTime
    }

    upcoming_show.append(upcoming)

    setattr(data, "upcoming_shows", past_show)
  setattr(data, "upcoming_shows_count", len(past_show))

  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST', 'GET'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  
  try:
    # if request.method == 'POST' and request.validate():
    venue = Venue (
      name = request.form.get('name'), 
      city = request.form.get('city'), 
      state = request.form.get("state"), 
      address = request.form.get('address'), 
      phone = request.form.get('phone'), 
      genres = "".join(request.form.get('genres')),
      image_link = request.form.get('image_link'), 
      facebook_link = request.form.get('facebook_link'), 
      website_link = request.form.get('website_link'), 
      looking_for_talent = request.form.get('looking_for_talent'), 
      seeking_description = request.form.get('seeking_description')
    )
    db.session.add(venue)
    db.session.commit() 
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  finally: 
    db.session.close()

  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('home'))

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  # return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  artist = Artist.query.distinct(Artist.id, Artist.name).all()
  data = []
  for artists in artist:
    data.append({
      "id": artists.id,
      "name": artists.name,
    })

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  search_term = request.form.get('search_term')
  artist = Artist.query.filter(Artist.name.ilike('%{}%'.format(search_term))).all()
        
    
  response={
    "count": len(artist),
    "data": []
  }

  response.data.append({
    "id": artists.id,
    "name": artists.name,
    "num_upcoming_shows": artists.upcoming_shows_count
  })
  
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id

  data = Artist.query.get(artist_id)
  setattr(data, "genres", data.genres.split(","))

  past_shows = list(filter(lambda show: show.startTime < datetime.datetime.now(), data.shows))
  upcoming_shows = list(filter(lambda show: show.startTime > datetime.datetime.now(), data.shows))

  past_show = []
  for show in past_shows:
      past = {
        "venue_name": show.venues.name,
        "venue_id": show.venues.id,
        "venue_image_link": show.venues.image_link,
        "start_time": show.startTime
      }

      past_show.append(past)

      setattr(data, "past_shows", past_show)
  setattr(data, "past_shows_count", len(past_show))

  upcoming_show = []
  for show in upcoming_shows:
    upcoming = {
      "venue_id": show.Venue.id,
      "venue_name": show.Venue.name,
      "venue_image_link": show.Venue.image_link,
      "start_time": show.startTime
    }

    upcoming_show.append(upcoming)

    setattr(data, "upcoming_shows", past_show)
  setattr(data, "upcoming_shows_count", len(past_show))

  
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist_list = Artist.query.get(artist_id)
  
  # TODO: populate form with fields from artist with ID <artist_id>
  artist={
    "id": artist_list.id,
    "name": artist_list.name,
    "genres": artist_list.genres.split(','),
    "city": artist_list.city,
    "state": artist_list.state,
    "phone": artist_list.phone,
    "website": artist_list.website_link,
    "facebook_link": artist_list.facebook_link,
    "seeking_venue": artist_list.looking_for_venue,
    "seeking_description": artist_list.seeking_description,
    "image_link": artist_list.image_link
  }
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  artist = Artist.query.get(artist_id)
  form = ArtistForm(request.form)

  if form.validate():
    try:
      artist.name = form.name.data,
      artist.genres = ",".join(form.genres.data),
      artist.city = form.city.data,
      artist.state = form.state.data
      artist.phone = form.phone.data
      artist.website = form.website_link.data
      artist.facebook_link = form.facebook_link.data
      artist.seeking_venue = form.seeking_venue.data
      edit_venue.image_link = form.image_link.data

      db.session.add(artist)
      db.session.commit()
      flash('Successfully updated artist')
    except Exception:
      print(sys.exc_info())
      db.session.rollback()
      flash('Could not update artist')
    finally:
      db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  #  Check for the form in the main project
  form = VenueForm(request.form)
  venue = Venue.query.get(venue_id)

  # TODO: populate form with values from venue with ID <venue_id>
  venue={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.looking_for_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link
  }
  
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  edit_venue = Venue.query.get(venue_id)
  form = Venue(request.form)

  if form.validate():
    try:
      edit_venue.name = form.name.data
      edit_venue.genres = form.genres.data
      edit_venue.address = form.address.data
      edit_venue.city = form.city.data
      edit_venue.state = form.state.data
      edit_venue.phone = form.phone.data
      edit_venue.website = form.website_link.data
      edit_venue.facebook_link = form.facebook_link.data
      edit_venue.looking_for_talent = form.looking_for_talent.data
      edit_venue.image_link = form.image_link.data

      db.session.add(edit_venue)
      db.commit()
      flash('Successfully updated venue')
    except:
      db.session.rollback()
      flash('Could not update venue')
    finally:
      db.session.close()
 
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()

  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  try:
    artist = Artist(
      name = request.form.get('name'),
      city = request.form.get('city'),
      state = request.form.get('state'),
      phone = request.form.get('phone'),
      genres = request.form.get('genres'),
      image_link = request.form.get('image_link'),
      facebook_link = request.form.get('facebook_link'),
      website_link = request.form.get('website_link'),
      looking_for_venue = request.form.get('looking_for_venue'),
      seeking_description = request.form.get('seeking_description'),
   )

    db.session.add(artist)
    db.session.commit()
     # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist ' + Artist.name + ' could not be listed.')
    db.session.rollback()
  finally:
    db.session.close()
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.

  show_items = Show.query.all()

  data = []
  for show in show_items:
    artist = Artist.query.get(show.artistID) 
    venue = Venue.query.get(show.venueID) 

    show_object = {
      "venue_id": show.venueID,
      "venue_name": venue.name,
      "artist_id": show.artistID,
      "artist_name": artist.name,
      "artist_image_link" : artist.image_link,
      "start_time": show.startTime,
    }
  
    data.append(show_object)

  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  
  try:
    new_show = Show (
      artistID = request.form.get("artist_id"),
      venueID = request.form.get("venue_id"),
      startTime = request.form.get('start_time')
    )
    # Show.insert(new_show)
    db.session.add(new_show)
    db.session.commit()
     # on successful db insert, flash success
    flash('Show was successfully listed!')
  except Exception as e:
    db.session.rollback()
    print(sys.exc_info())
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()
    
    
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
