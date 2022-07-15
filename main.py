import sys
from playlist import Playlist


def exit_with_usage():
    exit("usage: python main.py <input-file> <changes-file> <output-file>")


if __name__ == '__main__':
  if len(sys.argv) != 4:
    exit_with_usage()

  input_filepath = sys.argv[1].strip()
  changes_filepath = sys.argv[2].strip()
  output_filepath = sys.argv[3].strip()

  playlist = Playlist()

  if not playlist.read_spotify_json(input_filepath):
    exit("The spotify file doesn't exist or an error occurred while reading it.")
  
  if not playlist.read_changes_json(changes_filepath):
    playlist.write_output_json(output_filepath)
    exit("The change file doesn't exist or an error occurred while reading it.")

  if not playlist.process():
    playlist.write_output_json(output_filepath)
    exit("The change file seems to be invalid")

  playlist.write_output_json(output_filepath)

  print("Completed successfully.")
