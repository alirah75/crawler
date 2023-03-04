import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["divar_db"]
mycol = mydb["car"]
# mycol.insert_one({'ali':'hey'})


def insert(mydict):
    print('\033[94m inserting in Database...')
    mycol.insert_one(mydict)

