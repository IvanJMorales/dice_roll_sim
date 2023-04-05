import sqlite3

import click
from flask import current_app, g # current_app points to the Flask application handling request

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect( # Establish connection to the file pointed at by the DATABASE config key
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row #Tells the connection to return row that behave like dicts. This allows accessing the columns by name

    return g.db

# Check if a connection was created by checking if g.db was set.
# If connection exists, close it
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f: # Open file realtive to the flask package
        db.executescript(f.read().decode('utf8'))

@click.command('init-db') # Defines command line command called init-db that calls the init_db function
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db) # Tells flask to call that function when cleaning up after returning the response
    app.cli.add_command(init_db_command) # Adds a new command that can be called with the flask command