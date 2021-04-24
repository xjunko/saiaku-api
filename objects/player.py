import time
import aiohttp

from objects import glob

class Player:
  def __init__(self, data: dict):
    self.data = data[0]
    self.created_at = time.time()

  def __repr__(self):
    return f'<Player: {self.name} | ID: {self.id}>'

  @classmethod
  async def from_name(cls, name: str, mode: int = 0):
    if name.lower() in glob.cache['players']:
      return glob.cache['players'][name.lower()]

    async with glob.api.http.get(glob.api.base_url + '/get_user', params={'k': glob.api.token, 'u': name, 'm': mode}) as res:
      if not res or res.status != 200:
        return

      res = await res.json()

      p = cls(res)
      # save to cache
      glob.cache['players'][p.name.lower()] = p
      glob.cache['players'][p.id] = p

      return p

  async def top_play(self, mode: int = 0):
    async with glob.api.http.get(glob.api.base_url + '/get_user_best', params={'k': glob.api.token, 'u': self.id, 'm': mode}) as res:
      if not res or res.status != 200:
        return None

      return [glob.api.score(d) for d in await res.json()]

  async def recent_play(self, mode: int = 0):
    async with glob.api.http.get(glob.api.base_url + '/get_user_recent', params={'k': glob.api.token, 'u': self.id, 'm': mode}) as res:
      if not res or res.status != 200:
        return None

      return [glob.api.score(d) for d in await res.json()]


  @property
  def name(self):
    return self.data['username']

  @property
  def id(self):
    return int(self.data['user_id'])

  @property
  def hitcount(self):
    return {
      'hit300': self.data['count300'],
      'hit100': self.data['count100'],
      'hit50': self.data['count50'],
    }


  @property
  def ranked_score(self):
    return int(self.data['ranked_score'])

  @property
  def total_score(self):
    return int(self.data['total_score'])

  @property
  def accuracy(self):
    return float(self.data['accuracy'])

  @property
  def global_rank(self):
    return int(self.data['pp_rank'])

  @property
  def country_rank(self):
    return int(self.data['pp_country_rank'])

  @property
  def country(self):
    return self.data['country']
