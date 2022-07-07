from json import loads

from time import sleep
from json import dumps
from websocket import WebSocket
from concurrent.futures import ThreadPoolExecutor
import easygui, os
tokenlist = open(easygui.fileopenbox(), 'r').read().splitlines()
channel = int(input("Channel ID: "))
server = int(input("Server ID: "))
deaf = input("Defean: (y/n) ")
if deaf == "y":
  deaf = True
  if deaf == "n":
    deaf = False
mute = input("Mute: (y/n) ")
if mute == "y":
  mute = True
  if mute == "n":
    mute = False
stream = input("Stream: (y/n) ")
if stream == "y":
  stream = True
  if stream == "n":
    stream = False
video = input("Video: (y/n) ")
if video == "y":
  video = True
  if video == "n":
    video = False

executor = ThreadPoolExecutor(max_workers=int(1000))
def run(token):
  while True:
    ws = WebSocket()
    ws.connect("wss://gateway.discord.gg/?v=8&encoding=json")
    hello = loads(ws.recv())
    heartbeat_interval = hello['d']['heartbeat_interval']
    ws.send(dumps({"op": 2,"d": {"token": token,"properties": {"$os": "windows","$browser": "Discord","$device": "desktop"}}}))
    ws.send(dumps({"op": 4,"d": {"guild_id": server,"channel_id": channel,"self_mute": mute,"self_deaf": deaf, "self_stream?": stream, "self_video": video}}))
    ws.send(dumps({"op": 18,"d": {"type": "guild","guild_id": server,"channel_id": channel,"preferred_region": "singapore"}}))
    ws.send(dumps({"op": 1,"d": None}))
    ws.close()
    sleep(0.1)
    
os.system(f"title Total Tokens: {len(tokenlist)}")
i = 0
for token in tokenlist:
  executor.submit(run, token)
  i+=1
  print("[+] Joined voice channel")
  sleep(0.01)
yay = input("Enter to exit.")
