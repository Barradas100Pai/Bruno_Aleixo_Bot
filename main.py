import praw
import os
from psaw import PushshiftAPI
from replit import db
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
#from datetime import datetime
import time

#IMPORT REDDIT VALS
client_id = os.environ['client_id']
client_secret = os.environ['client_secret']
username = os.environ['username']
password = os.environ['password']

#IMPORT SPOTIFY VALS
spotify_client_id = os.environ['spotify_client_id']
spotify_client_secret = os.environ['spotify_client_secret']

#CONEXÃO BASE AO REDDIT
reddit = praw.Reddit(
	client_id = client_id,
	client_secret = client_secret,
	username = username,
	password = password,
	user_agent = "<BrunoAleixoBot 1.0>"
)

#CONEXÃO BASE AO SPOTIFY
client_credentials_manager = SpotifyClientCredentials(
    client_id=spotify_client_id,
    client_secret=spotify_client_secret
)

sp = spotipy.Spotify(
    client_credentials_manager=client_credentials_manager
)

#SUBREDIT ONDE FAZER O POST
subreddit = reddit.subreddit('BrunoAleixo')

#PODCAST ID's
aleixofm_id = '0bUbdKMxCffxh43lwbAkoi' 
aleixopedia_id = '0HRvyjL0cqgIhezozspzm4'
aleixoamigo_id = '1U1ZfNhVr2ZwFLHUWCkFqk'

#LAST EPISODE HOLDER
aleixopedia = sp.show_episodes(aleixopedia_id, limit = 1, offset = 0, market = 'PT')
aleixofm = sp.show_episodes(aleixofm_id, limit = 1, offset = 0, market = 'PT')
aleixoamigo = sp.show_episodes(aleixoamigo_id, limit = 1, offset = 0, market = 'PT')

#FUNÇÃO QUE REALIZA O POST
def makeRedditPost(podName, dict):
		episode_id = dict['items'][0]['id']
		episode_name = sp.episode(episode_id, market='PT')['name']
	
		title = "Novo episódio de " + podName + " - " + episode_name
		
		body = dict['items'][0]['description'] + "\n\n" +"Podem agora ouvir este excelente episódio em: " + dict['items'][0]['external_urls']['spotify']
		#image_url = dict['items'][0]['images'][0]['url']
		subreddit.submit(title, selftext=body)

#TESTE
#makeRedditPost("Aleixo Amigo", aleixoamigo)

while True:
	time.sleep(60)
	#GET PODCAST ALEIXOPEDIA
	now_aleixopedia = sp.show_episodes(aleixopedia_id, limit = 1, offset = 0, market = 'PT')
	if now_aleixopedia != aleixopedia:
		aleixopedia = now_aleixopedia
		makeRedditPost("Aleixopédia", aleixopedia)
	#GET PODCAST ALEIXO FM
	now_aleixofm = sp.show_episodes(aleixofm_id, limit = 1, offset = 0, market= 'PT')
	if now_aleixofm != aleixofm:
		aleixofm = now_aleixofm
		makeRedditPost("Aleixo FM", aleixofm)
	#GET PODCAST ALEIXO AMIGO
	now_aleixoamigo = sp.show_episodes(aleixoamigo_id, limit = 1, offset = 0, market = 'PT')
	if now_aleixoamigo != aleixoamigo:
		aleixoamigo = now_aleixoamigo
		makeRedditPost("Aleixo Amigo", aleixoamigo)
	
