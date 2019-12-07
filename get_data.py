from decouple import config
import pymongo
from bson.json_util import dumps


def get_subreddit_info(array):
    """
    Function written by Matthew/Johana that gets
    subreddit information based on ID numbers
    """
    code = config('mongo_code')
    client = pymongo.MongoClient(code)
    db = client.sfw_db
    data = [dumps(db.sfw_db.find({'sub_id': int(num)})[0]) for num in array]
    return(data)
