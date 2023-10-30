from pymongo import MongoClient
import os

# Create the database and database connection
client = MongoClient(
    host=os.getenv("MONGO_HOSTNAME"),
    port=int(os.getenv("MONGO_PORT")),
    username=os.getenv("MONGO_USERNAME"),
    password=os.getenv("MONGO_PASSWORD"),
    authSource="admin"
)
db = client[os.getenv("MONGO_DATABASE")]
