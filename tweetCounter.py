import requests
import csv
import json
from calendar import monthrange

class tweetCounter:
    # To set your enviornment variables in your terminal run the following line:
    # export 'BEARER_TOKEN'='<your_bearer_token>'
    
    def auth(self):
        return "AAAAAAAAAAAAAAAAAAAAAP5KNAEAAAAAycIuL%2BYXlU9sdi7Z267bDQp%2FfE0%3DAkIyNchX9UmeGO10oUkryZa75J7FP4o5jEyM3m4uMbvwe69sXw"
    
    
    def createDate(self):
        global Dates
        with open("Data//Time.txt","r") as file:
            asString = file.read()
        months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
        yearInt = int(asString[asString.index(" ")+1:len(asString)])
        monthString = months.index(asString[0:asString.index(" ")])+1
        monthRange = monthrange(yearInt,int(monthString))
        dayString = str(monthRange[1])
        if int(monthString) < 10: monthString = "0" + str(monthString)
        if monthRange[1] < 10: dayString = "0" + str(monthRange[1])
        start = str(yearInt)+"-"+monthString+"-01T00:00:00Z"
        end = str(yearInt)+"-"+monthString+"-"+dayString+"T23:59:59Z"
        Dates = [start,end]
    
    
    def create_url(self,id):
        return "https://api.twitter.com/2/users/{}/tweets".format(id)
    
    
    def get_params(self):
        # Tweet fields are adjustable.
        # Options include:
        # attachments, author_id, context_annotations,
        # conversation_id, created_at, entities, geo, id,
        # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
        # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
        # source, text, and withheld
        return {"tweet.fields": "created_at","end_time":Dates[1],"start_time":Dates[0],"max_results":"100"}
    
    
    def create_headers(self,bearer_token):
        return {"Authorization": "Bearer {}".format(bearer_token)}
    
    
    def connect_to_endpoint(self,url, headers, params):
        response = requests.request("GET", url, headers=headers, params=params)
        if response.status_code != 200:
            print(response.status_code)
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return response.json()
    
    
    def getID(self):
        file = open(fileName,"r")
        reader = csv.reader(file)
        index = 0
        for line in reader:
            if index == 0:
                index += 1
                continue
            ID.append(line)
    
    
    def writeData(self,data):
        outfile = open(writeFileName,'w')
        outfile.write(data)
    
    
    def writeTotal(self):
        totalTweets = 0
        read_file = ""
        read_data = []
        for id in ID:
            read_file = "Data//User_Data//"
            read_file += id[0]+".json"
            read_file = open(read_file,'r')
            for line in read_file:
                if "result_count" in line:
                    read_data.append(line)
        write_file = "Data//User_Data//Admin.json"
        write_file = open(write_file,'w')
        for index, line in enumerate(read_data):
            line = line[line.index(":")+2:len(line)]
            totalTweets += int(line)
            write_file.write(ID[index][0]+":"+ line)
        print(totalTweets)
    
    
    def main(self):
        global fileName
        global writeFileName
        global ID
        global Data
        global totalTweets
        fileName = "Data//Handles_ID.csv"
        ID = []
        Data = []
        self.createDate()
        self.getID()
        bearer_token = self.auth()
        for id in ID:
            writeFileName = "Data//User_Data//"
            writeFileName += id[0]+".json"
            url = self.create_url(id[1])
            headers = self.create_headers(bearer_token)
            params = self.get_params()
            json_response = self.connect_to_endpoint(url, headers, params)
            Data.append(json_response)
            self.writeData(json.dumps(json_response,indent=4,sort_keys=True))
        self.writeTotal()
