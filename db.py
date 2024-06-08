import pymongo
from pymongo import MongoClient
import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['1.1.1.1']
from config import *



class db:
    client = MongoClient(MONGO)
    database = client["clouebot"]
    storage = database["storage"]

