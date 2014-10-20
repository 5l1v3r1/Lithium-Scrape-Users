#!/usr/bin/python
# LAST UPDATE 20/10/14
#
# LITHIUM-SCRAPE-USERS.PY
# This script cycles through each member that exists on a lithium based site, grabs the user and outputs the username to file.
#
# For test purposes only i have put litiums actual site, please change accoringly
#
# ADD ME ON TWITTER @NOOBIEDOG
#
# NO LONGER MAINTAINED - Quick, Easy and Dirty!
#
# A Few Sites that use Lithium
#
# http://www.barclaycardtravel.com/t5/user/viewprofilepage/user-id
# http://www.community.skype.com/t5/user/v1/viewprofilepage/user-id
# https://forums.autodesk.com/t5/user/v2/viewprofilepage/user-id
#
# Google Dork: inurl:"/t5/user/viewprofilepage/user-id/" or a varient of that 
#

from urllib import urlopen

from BeautifulSoup import BeautifulSoup

import Queue
import threading
import urllib2
import time
import re

queue = Queue.Queue()

class ThreadUrl(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def run(self):
		while True:
			usernumber = self.queue.get()
			# Copy all of the content from the provided web page
			url = "http://community.lithium.com/t5/user/viewprofilepage/user-id" # CHANGE ME - Replace with actual site
			webpage = urlopen(url + '/' + str(usernumber)).read()

			# Grab everything that lies between the title tags using a REGEX
			patFinderTitle = re.compile('')

			# Store all of the titles and links found in 2 lists
			findPatTitle = re.findall(patFinderTitle,webpage)

			soup2 = BeautifulSoup(webpage)

			titleSoup = soup2.title.string
			if titleSoup == " Person does not exist - Lithium Community": # CHANGE ME - Replace this with the person not found title
				continue
			else:
				usernames = titleSoup.replace(" About ","",1).replace(" - Lithium Community","",1) # CHANGE ME - Replace this with a sucessful attempt title.
				Output_file.write(usernames + '\n')
				print usernames
			self.queue.task_done()


def main():
    ThreadNumber = 10
    #spawn a pool of threads, and pass them queue instance 
    for i in range(ThreadNumber):
        t = ThreadUrl(queue)
        t.setDaemon(True)
        t.start()

    #populate queue with data
    for x in range(0, 10000): # 0 to 10000 users if they exist
	    queue.put(x)

    #wait on the queue until everything has been processed
    queue.join()

Output_file = open("usernames.txt", "w")
main()
Output_file.close()



