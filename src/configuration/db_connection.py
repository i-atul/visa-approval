import os
import sys
import pymongo
import certifi
from src.exception import MyException
from src.logger import logging
from src.constants import DATABASE_NAME, MONGODB_URL_KEY

# certificate to avoid timeout errors when connecting to MongoDB
ca = certifi.where()

class MongoDBClient:
    client = None  

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        try:
            # Check if a MongoDB client connection has already been established; if not, create a new one
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)  
                if mongo_db_url is None:
                    raise Exception(f"Environment variable '{MONGODB_URL_KEY}' is not set.")
                
                # Establish a new MongoDB client connection
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
                
            # Use the shared MongoClient for this instance
            self.client = MongoDBClient.client
            self.database = self.client[database_name]  
            self.database_name = database_name
            logging.info("MongoDB connection successful.")
            
        except Exception as e:
            raise MyException(e, sys)