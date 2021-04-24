# TERRIBLE NOT GOOD AT ALL asynchronous OSU!V1 API!!!!!!

# How to fucking use
* u dont

# How to use (for real)
* rename the folder to osu_api or something, im too lazy to setup the setup.py thing
* import API
* give it osu!token like
```py
from osu_api import API

api = API(token='sus')

# Player
player = await api.player.from_name('FireRedz') # you can also call top_play, recent_play from the player class
print(f'{player.name} has {player.pp}pp!') 

# Beatmap
bmap = await api.beatmap.from_beatmap_id(2776718)
scores = await bmap.get_scores(mods=64)
print(f'DT scores on {bmap.title} [{bmap.version}]: {scores}')

# Score
scores = await api.score.get_scores(...) # is the same as bmap.get_scores but you need to give it the map id

```