# Create-Calendar-Events
My job did not have an effective way to automatically add calendar events for the retail shifts I was working, so I wrote this small python script. I have plans to write it again as a Javascript applet, but have not taken on that task yet.

Most of this information for actually create the calendar events for your google calendar can be found on https://developers.google.com/calendar/create-events

Interesting solutions that I accomplished in this script: converting a time like "8A" or "5.30P" to a format that Python's datetime module can interpret, through the use of a dictionary; randomizing calendar event names; and parsing a string deliminated by doublew whitespaces

Feel free to use parts of this script for your own purposes, I have removed anything related to my job specifically.
