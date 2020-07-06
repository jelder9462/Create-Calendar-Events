#!/usr/bin/env python

from __future__ import print_function
import datetime
import pickle
import os.path
import random
import dateutil
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

#first section here comes from the python quickstart guide: https://developers.google.com/calendar/quickstart/python

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

#request the copied data from .info (this is what we call our back end site at my work.)
#format expected: Saturday - Friday copied as a single row
# ex: 10.30A-6.30P	11.30A-5.30P	 	 	 	10.30A-6.30P	OFF
#This line is to be interpreted as Saturday 10:30-6:30, Sunday 11:30-5:30, and Thursday 10:30-6:30
sloppyPaste = input('Put in the sloppy pasted data from .info\n')

weekStart = input("please input the first day of the work week in the format: mm/dd/yy\n")         #prompt the user for the start of the workweek to calculate the dates
weekStart = datetime.datetime.strptime(weekStart, '%m/%d/%y')   #convert the input date to UTC for the google 

#define our working variables

tempString = ''
spaceCount = 0
shiftList = []    #create the list to be worked with


for name in sloppyPaste:
    if name.isspace():    #spaces are found between the shifts on .info
        if spaceCount >= 1:    #two spaces indicate a day off
            tempString = 'No Shift'
            spaceCount = 0     #reset the counter to prepare for a second day off
        else:
            spaceCount += 1    #first space should be tallied
            shiftList.append(tempString)      #add our shift string to the list
            tempString = ''             #reset the working var
        
    else:
        tempString = tempString + name         #add another char to the current shift
        spaceCount = 0

shiftList.append(tempString)      #add the last shift to the list

timeTable = {                       #dictionary to convert .info format to UTC
    "8A" : "8:00:00",
    "8.30A" : "8:30:00",
    "9A" : "9:00:00",
    "9.30A" : "9:30:00",
    "10A" : "10:00:00",
    "10.30A" : "10:30:00",
    "11A" : "11:00:00",
    "11.30A" : "11:30:00",
    "12P" : "12:00:00",
    "12.30P" : "12:30:00",
    "1P" : "13:00:00",
    "1.30P" : "13:30:00",
    "2P" : "14:00:00",
    "2.30P" : "14:30:00",
    "3P" : "15:00:00",
    "3.30P" : "15:30:00",
    "4P" : "16:00:00",
    "4.30P" : "16:30:00",
    "5P" : "17:00:00",
    "5.30P" : "17:30:00",
    "6P" : "18:00:00",
    "6.30P" : "18:30:00",
    "7P" : "19:00:00",
    "7.30P" : "19:30:00",
    "8P" : "20:00:00",
    "8.30P" : "20:30:00",
    "9P" : "21:00:00",
    "9.30P" : "21:30:00",
    "10P" : "22:00:00",
    "10.30P" : "22:30:00",
    "11P" : "23:00:00",
    "11.30P" : "23:30:00"
}

starts = []                                                             #create lists for the start and end times of shifts
ends = []
tempTime = ''                                                           #working variable

for shift in shiftList:                                                  #handle the non-work days
    if shift == 'No Shift' or shift == 'OFF':
        starts.append('No Shift')
        ends.append("No Shift")
    else:
        for char in shift:                                           #separate the start from the end using the '-' delimeter
            if char != "-":
                tempTime += char
            else:
                starts.append(tempTime)                        #add the start time to the starting list
                tempTime = ''
        ends.append(tempTime)                                    #add the end time to the ending list
        tempTime = ''

fullTimeStarts = []                                                 #lists for UTC times
fullTimeEnds = []

for time in starts:
    if time != 'No Shift':                                          #if the list entry is not a 'No Shift' or 'OFF'
        fullTime = timeTable[time]                                  #convert times to UTC
        fullTimeStarts.append(fullTime)                         #add to the list of UTC times
        fullTime = ''
    else:
        fullTimeStarts.append('No Shift')                            #add the days off to the list
        fullTime = ''

for time in ends:                                                       #same as above but for the ends
    if time != 'No Shift':
        fullTime = timeTable[time]
        fullTimeEnds.append(fullTime)
        fullTime = ''
    else:
        fullTimeEnds.append('No Shift')
        fullTime = ''

dateList = []                                                               #create list of dates

for x in range (0,7):                                                       #fill list of dates with 7 correct dates
    workingDay = weekStart + datetime.timedelta(days = x)
    workingDay.astimezone(tz=None)         #assign timezone for the dates
    dateList.append(workingDay.date())
       

#list of silly names to name my shifts
shiftNames = ['Research The Outdoors',
              'Face North',
              'Unite the Blue',
              'There is no Back Room',
              'Santa\'s Elves got Nothing on Arc Build Quality',
              'Shred the Gnar Sales',
              'Sweep... a lot',
              'Count Money a Couple Times',
              'Find That One Thing That I Misplaced Last Time I Misplaced Something',
              'Put on the Music That Makes the Customers Buy Stuff',
              'Sell a Shirt, Probably',
              'Is it Wing Day Yet?',
              'It\'s Probably Nice Out',
              'Help the Customers Spend Their Unneeded Money',
              'Make the Bike Stop Going CLACK-KICKETY-CLACK-KA-CHUNK',
              'Sit in Boredom Because the Customers Didn\'t Show Up',
              'Drink 3 much Coffee, Then Sell 3 Fast 5 Custies',
              'Pet as Many Dogs as Possible',
              'No Price Tag?? Must Be Free',
              'Resist the Urge to Buy Anything',
              'Ring \'em up, Ring \'em down',
              'Scanner Goes BEEEEEEP',
              'Hope the Fire Alarm Doesn\'t Go Off!',
              'Stare a Baby in the Face, Then Sell Things to the Baby\'s parents',
              'Try Not to Knock Over a Snowboard While Scooting by WAAAAAAY too Fast',
              'Review the Plethora of Items Received by Generous Reps',
              'Work Off of Monster & Wasabi Peas',
              'Please Dont Throw Poop Out Your Window',
              'Fjall the Raven',
              'Be Like Houdini. Expensive.',
              'I Don\'t NEED More Shoes',
              'Wonder if \"Where the Wild Things Are\" is Supposed to be About Conrad Anker',
              'Stream Meru for Allllllllllllll the Custies',
              'Long After the Adorable Photos of Dogs on the Dog Wall',
              'Try Not to Ship My Pants',
              'Impress a Customer By Not Only Remembering Their Name, But Also Exactly What They Bought Last Time They Were in']


#creation of events
for day in range(0,7):
    try:
        #this came from Google's calendar event creation page: https://developers.google.com/calendar/create-events
        event = {
        'summary': random.choice(shiftNames),
        'location': 'THE PLACE I WORK',
        'description': 'Oh, you know.',
        'start': {
            'dateTime': str(dateList[day]) + 'T'+ str(fullTimeStarts[day]) + '-05:00',
            },
        'end': {
            'dateTime': str(dateList[day]) + 'T' + str(fullTimeEnds[day]) + '-05:00',
            },
        }
        print("Calendar event created for ", dateList[day], fullTimeStarts[day], " - ", fullTimeEnds[day])
        
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:creds = pickle.load(token)

        service = build('calendar', 'v3', credentials=creds)

        event = service.events().insert(calendarId='your calender ID goes here', body=event).execute()
        print ('Event created on ' + dateList[day] + '%s' % (event.get('htmlLink')))
    except:
        continue

if __name__ == '__main__':
    main()
