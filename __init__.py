import asyncio
import aiohttp

from objects import Player, Score, Beatmap
from objects import glob

class API:
  base_url: str = 'https://osu.ppy.sh/api'

  def __init__(self, token: str):
    self.token = token
    self.http = aiohttp.ClientSession()

    glob.api = self

  @property
  def player(self):
    return Player

  @property
  def score(self):
    return Score

  @property
  def beatmap(self):
    return Beatmap


async def main():
  api = API(token='')
  player = await api.player.from_name('fireredz')
  top_play = await player.top_play(mode=0)
  score = top_play[0]
  beatmap = await score.beatmap
  leaderboard = await beatmap.get_scores()

  # Test 1
  print(f'{player.name} #1st TopPlay is on {beatmap.title} [{beatmap.version}] with {score.pp}pp')

  # Test 2
  lb_first = leaderboard[0]
  print(f'#1st score on that map is {lb_first}')

  # Test 3
  recent = await player.recent_play(mode=0)
  print(f'Recent play for {player.name}, {recent}')

  await api.http.close()


if __name__ == '__main__':
  asyncio.run(main())

