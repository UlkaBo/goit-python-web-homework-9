from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
_CONN = 'postgresql://...:...@localhost:5432/postgres'

engine = create_engine(_CONN)

insp = inspect(engine)
db_list = insp.get_schema_names()

databases = engine.execute('SELECT datname FROM pg_database;').scalars().fetchall()

if 'addressbook' not in databases:
    with engine.connect() as connection:
        connection.execute('commit')
        connection.execute('CREATE database addressbook')


_CONN = 'postgresql://postgres:6894@localhost:5432/addressbook'
engine = create_engine(_CONN, echo = True)
print(1)
#databases = engine.execute('SELECT datname FROM pg_database;').scalars().fetchall()
#print(databases)

#print(engine.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';").scalars().fetchall())


metadata = Base.metadata
DBSession = sessionmaker(bind=engine)
session = DBSession()
