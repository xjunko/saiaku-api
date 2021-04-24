import time
from enum import IntEnum

from objects import glob

class ApprovedState(IntEnum):
  graveyard = -2
  WIP = -1
  pending = 0
  ranked = 1
  approved = 2
  qualified = 3
  loved = 4


class Beatmap:
  def __init__(self, data: dict):
    self.data = data[0]
    self.created_at = time.time()

  def __repr__(self):
    return f'<Beatmap: {self.id}>'

  @classmethod
  async def from_mapset_id(cls, id: int):
    if (b := cls.from_cache(id)):
      return b

    if not (data := await cls.get_beatmap(s=id)):
      return None

    b = cls(data)
    b.save_to_cache()

    return b

  @classmethod
  async def from_beatmap_id(cls, id: int):
    if (b := cls.from_cache(id)):
      return b

    if not (data := await cls.get_beatmap(b=id)):
      return None

    b = cls(data)
    b.save_to_cache()

    return b

  @staticmethod
  async def get_beatmap(**kwargs: dict):
    async with glob.api.http.get(glob.api.base_url + '/get_beatmaps', params={'k': glob.api.token, **kwargs}) as res:
      if not res or res.status != 200:
        return None

      return await res.json()

  @staticmethod
  def from_cache(id: int):
    if int(id) in glob.cache['beatmaps']:
      return glob.cache['beatmaps'][int(id)]

  def save_to_cache(self):
    if not self.from_cache(self.id):
      glob.cache['beatmaps'][self.id] = self
      glob.cache['beatmaps'][self.set_id] = self


  async def get_scores(self, **kwargs):
    return await glob.api.score.get_scores(map_id=self.id, **kwargs)

  @property
  def id(self):
    return int(self.data['beatmap_id'])

  @property
  def set_id(self):
    return int(self.data['beatmapset_id'])

  @property
  def md5(self):
    return self.data['file_md5']

  @property
  def approved(self):
    return ApprovedState(int(self.data['approved']))

  @property
  def artist(self):
    return self.data['artist']

  @property
  def artist_unicode(self):
    return self.data['artist_unicode']

  @property
  def title(self):
    return self.data['title']

  @property
  def title_unicode(self):
    return self.data['title_unicode']

  @property
  def version(self):
    return self.data['version']

  @property
  async def creator(self):
    return await glob.api.get_user(self.data['creator'])

  @property
  def total_length(self):
    return int(self.data['total_length'])

  @property
  def hit_length(self):
    return int(self.data['hit_length'])

  @property
  def frozen(self):
    return [ApprovedState.ranked, ApprovedState.loved, ApprovedState.graveyard] in self.approved
