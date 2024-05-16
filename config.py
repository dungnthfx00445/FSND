import os
from dotenv import load_dotenv

load_dotenv()

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
ALGORITHMS = os.environ.get("ALGORITHMS")
API_AUDIENCE = os.environ.get("API_AUDIENCE")

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres_deployment_example_52kc_user:ECXWusLkThp8NNAtsYEhbhKyVbYR2HR3@dpg-cp2ruhq1hbls7383mdp0-a.oregon-postgres.render.com/postgres_deployment_example_52kc'
SQLALCHEMY_TRACK_MODIFICATIONS = False