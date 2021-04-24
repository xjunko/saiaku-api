import time

from objects import glob

class Score:
  def __init__(self, data: dict):
    self.data = data
    self.created_at = time.time()

  def __repr__(self):
    return f'<Score by {self.player_id} | on {self.data.get("beatmap_id")}>'

  @classmethod
  async def get_scores(cls, map_id: int, name: str='', mode: int = 0, mods: int = -1, limit: int = 50):
    async with glob.api.http.get(glob.api.base_url + '/get_scores', params={'k': glob.api.token, 'b': map_id, 'u': name, 'm': mode, 'mods': mods, 'limit': limit}) as res:
      if not res or res.status != 200:
        return None

      return [Score(d) for d in await res.json()]

  @property
  async def beatmap(self):
    return await glob.api.beatmap.from_beatmap_id(self.data['beatmap_id'])

  @property
  def id(self):
    return int(self.data['score_id'])

  @property
  def pp(self):
    return float(self.data['pp'])

  @property
  def score(self):
    return int(self.data['score'])

  @property
  def maxcombo(self):
    return int(self.data['maxcombo'])

  @property
  def hitcount(self):
    return {
      hit_type: int(self.data['count' + hit_type]) for hit_type in ['300', '100', '50', 'geki', 'katu', 'miss']
    }

  @property
  def perfect(self):
    return self.data['perfect'] == 1

  @property
  def replay_available(self):
    return self.data['replay_available'] == 1

  @property
  def mods(self):
    return int(self.data['enabled_mods'])

  @property
  def player_id(self):
    return int(self.data['user_id'])

  @property
  async def player(self):
    if not self.player_id in glob.cache['players']:
      glob.cache['players'] = await glob.api.get_user(self.player_id)

    return glob.cache['players'][self.player_id]
