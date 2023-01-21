## Python 3 script to get useful information from Resonate Playlists
## I use this to talk about the radio show I produce
# import urllib library
from urllib.request import urlopen
import urllib.error

# import json
import json
# store the URL in url as 
# parameter for urlopen
# This is a Resonate tracklist id. Find it via https://api.resonate.coop/v3/trackgroups/?order=newest&type=playlist
# url = "https://api.resonate.coop/v2/trackgroups/9d9f7bcb-6082-470a-b66c-ec7e15a13305" #2022-05-24
url = "https://api.resonate.coop/v3/trackgroups/cd98c627-7390-49f8-8de6-6ed88ac70b3d"

  
# store the response of URL
response = urlopen(url)
  
# storing the JSON response 
# from url in data
data_json = json.loads(response.read())
 
titles = []
artists= []
creator_ids = []
 
items = data_json['data']['items']
for item in items:
	title = item['track']['title']
	artist = item['track']['artist']
	creator_id = item['track']['creator_id']
	titles.append(title)
	artists.append(artist)
	creator_ids.append(creator_id)

# Comma seperated list of track,artist - easy to copy into a spreadsheet
tracks = dict(zip(titles, artists))
for key,value in tracks.items():
	print("{},{}".format(key,value))
	
# 3 lists - just tracks, just artists, written list of artists comma seperated for text posts	
print(*titles, sep = "\n")
print(*artists, sep = "\n")
print(*artists, sep = ", ")
print(*artists, sep = " · ")

# We need to fetch info about each artists to get more information - We assume creator id = artist id
artists2 = dict(zip(artists, creator_ids))
twitter = []
instagram = []
youtube = []
facebook = []
bandcamp= []

# Simple list of links to artist pages
for key,value in artists2.items():
	print("https://api.resonate.coop/v3/artists/{}".format(value))
	
	
for key,value in artists2.items():
	url = "https://api.resonate.coop/v3/artists/{}".format(value)
	# Markdown of Artist with a link - useful for the webiste and Resonate community posts
	print("[{}](https://stream.resonate.coop/artist/{})".format(key,value), end = ', ')

	# store the response of URL
	try:
    		response = urlopen(url)
	except urllib.error.HTTPError as err:
    		continue
  	
	
	  
	# storing the JSON response 
	# from url in data
	data_json = json.loads(response.read())
	
	links = data_json['data']['links']
	for link in links:
		if "twitter" in link['href']:
			twitter.append(link['href'])
		elif "instagram" in link['href']:
			instagram.append(link['href'])
		elif "youtube" in link['href']:
			youtube.append(link['href'])
		elif "facebook" in link['href']:
			facebook.append(link['href'])
		elif "bandcamp" in link['href']:
			bandcamp.append(link['href'])
	
# We can click on all the links to follow people
print(*twitter, sep = "\n")
print(*instagram, sep = "\n")
print(*youtube, sep = "\n")
print(*facebook, sep = "\n")
print(*bandcamp, sep = "\n")

# This gives us a nice list we can copy directly into posts on these services
print("instagram")
for item in instagram: 
	item = item.replace("https://", "")
	item = item.replace("www.", "")
	item = item.replace("instagram.com/", "@")
	print(item)
	
print("twitter")
for item in twitter: 
	item = item.replace("https://", "")
	item = item.replace("www.", "")
	item = item.replace("twitter.com/", "@")
	print(item)

print("facebook")
for item in facebook: 
	item = item.replace("https://", "")
	item = item.replace("www.", "")
	item = item.replace("facebook.com/", "@")
	print(item)

# print the json response
#print(data_json)
