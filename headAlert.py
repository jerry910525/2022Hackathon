import imp
import time
import datetime
import requests
import base64
import pymongo
import sys
from connMongoDB import ConnDB

class Notify():
    def __init__(self) -> None:
        self.token=base64.b64decode(('ZTdkM085ajRWVTFQZVB2OThWNFpYazVJS3hEU00wT0J5QlRTaXE0T2hlOA=='.encode())).decode()
        self.header={
            "Authorization": "Bearer " + self.token
        }

    def makeNotify(self, nData):
        data={'message' : '\n'+nData['time']}
        file={'imageFile' : nData['img']}

        r = requests.post("https://notify-api.line.me/api/notify", headers = self.header, data = data, files = file)
        print(f'Sending at {time.ctime()}')


# class ConnDB():
#     def __init__(self) -> None:
#         uri = "mongodb+srv://hackathon2022.vpsksno.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
#         client = pymongo.MongoClient(uri,
#                             tls=True,
#                             tlsCertificateKeyFile='./certification.pem')
#         self.db = client['hackathon2022']
#         self.col = self.db['AlertStamp']

#     def insert(self, dbData):
#         if(dbData['img']!='None'):
#             dbData['img']=base64.b64encode(dbData['img'].read())
#         rlt=self.col.insert_one(dbData)
#         print(f'Insert Complete: {rlt.inserted_id}')

#     def showAll(self, saveImg = False):
#         rlt=self.col.find()
#         for i in rlt:
#             print(f"time: {i['time']}")
#             if(saveImg):
#                 if(i['img']!='None'):
#                     with open(f"{i['time'].replace(' ','').replace(':','')}.png", "wb") as fh:
#                         fh.write(base64.decodebytes(i['img']))
#     def delAll(self):
#         rlt=self.col.delete_many({})
#         print(rlt.deleted_count, "data has deleted")

#     def find(self, key, value):
#         rlt=self.col.find({key: value})
#         return list(rlt)    # return a list of dict

#     def delete(self, key, value):
#         self.col.delete_one({key:value})
#         print('\nDelete Complete.\nFollowing are current data in DB:')
#         self.showAll()

def MakeAlert(alertMsg, notify = False):
    if notify:
        ntfy = Notify()
        ntfy.makeNotify(alertMsg)
    db = ConnDB()
    db.insert(alertMsg)

if __name__=="__main__":

    timestr = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    img = open('./000005.jpg', 'rb')
    alertMsg={'time':timestr , 'img':img}
    MakeAlert(alertMsg)
    
    #############

    # print('Make notify...')
    # ntfy = Notify()
    # image = open('./image.png', 'rb')
    # msg=datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    # sendData={'msg': msg, 'img': image}
    # ntfy.makeNotify(sendData)
    




