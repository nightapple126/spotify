import copy
import json
import uuid

### Constant
KEY_UPDATE = 'update'
KEY_CREATE = 'create'
KEY_DELETE = 'delete'

KEY_PLAYLIST = 'playlist'
KEY_PLAYLISTS = 'playlists'
KEY_ID = 'id'
KEY_OWNER_ID = 'owner_id'
KEY_SONG_IDS = 'song_ids'
KEY_SONGS = 'songs'

ITEM_TYPE_UPDATE = 1
ITEM_TYPE_CREATE = 2
ITEM_TYPE_DELETE = 3
### Constant end


class Playlist:
  def __init__(self):
    self.__json_spotify = None
    self.__json_output = None
    self.__json_changes = None
  

  def read_spotify_json(self, filepath):
    with open(filepath) as raw_spotify:
      self.__json_spotify = json.load(raw_spotify)
      self.__json_output = copy.deepcopy(self.__json_spotify)
    return self.__json_spotify is not None


  def read_changes_json(self, filepath):
    with open(filepath) as raw_changes:
      self.__json_changes = json.load(raw_changes)
    return self.__json_changes is not None


  def write_output_json(self, filepath):
    str_output = json.dumps(self.__json_output, indent = 2)
    with open(filepath, "w") as outfile:
      outfile.write(str_output)
  

  def process(self):
    if KEY_PLAYLIST not in self.__json_changes.keys():
      return False

    change_playlist = self.__json_changes[KEY_PLAYLIST]
    keys = change_playlist.keys()
    if KEY_UPDATE in keys:
      self.__update_playlist(self.__json_output, change_playlist[KEY_UPDATE])
    if KEY_CREATE in keys:
      self.__create_playlist(self.__json_output, change_playlist[KEY_CREATE])
    if KEY_DELETE in keys:
      self.__delete_playlist(self.__json_output, change_playlist[KEY_DELETE])

    return True


  def __find_playlist_by_id(self, playlists, id):
    idx = 0
    for playlist in playlists:
      if playlist[KEY_ID] == id:
        return idx
      idx += 1
    return -1


  def __find_playlist_by_owner_id(self, playlists, owner_id):
    idx = 0
    for playlist in playlists:
      if playlist[KEY_OWNER_ID] == owner_id:
        return idx
      idx += 1
    return -1


  def __validate_item(self, item_type, json_output, item):
    keys = item.keys()

    if item_type == ITEM_TYPE_UPDATE:
      return KEY_ID in keys and KEY_SONG_IDS in keys and len(item[KEY_SONG_IDS]) != 0
    elif item_type == ITEM_TYPE_CREATE:
      return KEY_OWNER_ID in keys and KEY_SONG_IDS in keys and len(item[KEY_SONG_IDS]) != 0
    elif item_type == ITEM_TYPE_DELETE:
      return KEY_ID in keys
    return False


  def __append_song_ids(self, _song_ids, song_ids, songs):
    for song_id in song_ids:
      if song_id in _song_ids:
        continue
      self.__append_song_id(_song_ids, song_id, songs)


  def __append_song_id(self, song_ids, song_id, songs):
    for song in songs:
      if KEY_ID in song.keys() and song[KEY_ID] == song_id:
        song_ids.append(song_id)
        return


  def __update_playlist_item(self, json_output, id, song_ids):
    playlists = json_output[KEY_PLAYLISTS]
    idx = self.__find_playlist_by_id(playlists, id)
    if idx == -1:
      return
    _song_ids = playlists[idx][KEY_SONG_IDS]
    self.__append_song_ids(_song_ids, song_ids, json_output[KEY_SONGS])


  def __update_playlist(self, json_output, json_changes_update):
    for update_item in json_changes_update:
      if not self.__validate_item(ITEM_TYPE_UPDATE, json_output, update_item):
        continue
      self.__update_playlist_item(json_output, update_item[KEY_ID], update_item[KEY_SONG_IDS])
      

  def __create_playlist_item(self, json_output, owner_id, song_ids):
    playlists = json_output[KEY_PLAYLISTS]
    idx = self.__find_playlist_by_owner_id(playlists, owner_id)
    if idx == -1:
      # add new playlist
      id = str(uuid.uuid1())
      _song_ids = []
      self.__append_song_ids(_song_ids, song_ids, json_output[KEY_SONGS])
      if len(_song_ids) > 0:
        new_playlist = { KEY_ID: id, KEY_OWNER_ID: owner_id, KEY_SONG_IDS: _song_ids }
        playlists.append(new_playlist)
    else:
      # update the playlist
      self.__update_playlist_item(json_output, playlists[idx][KEY_ID], song_ids)


  def __create_playlist(self, json_output, json_changes_create):
    for create_item in json_changes_create:
      if not self.__validate_item(ITEM_TYPE_CREATE, json_output, create_item):
        continue
      self.__create_playlist_item(json_output, create_item[KEY_OWNER_ID], create_item[KEY_SONG_IDS])


  def __delete_playlist_item(self, json_output, id):
    playlists = json_output[KEY_PLAYLISTS]
    idx = self.__find_playlist_by_id(playlists, id)
    if idx == -1:
      return
    playlists.pop(idx)


  def __delete_playlist(self, json_output, json_changes_delete):
    for delete_item in json_changes_delete:
      if not self.__validate_item(ITEM_TYPE_DELETE, json_output, delete_item):
        continue
      self.__delete_playlist_item(json_output, delete_item[KEY_ID])
