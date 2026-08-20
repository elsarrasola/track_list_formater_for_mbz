import sys, os, pydub, re

########################## Function section ##########################
def show_help():
    """
    Show the help message in the standard output
    """
    help_msg = """Welcome to the Track List Formater for MusicBrainz !
    This is how to use the program:

    tlfm --path /path/to/album/folder --artist "Artiste name"
    
    Here are the tags :
    -h,  --help       : show this message.
    -p,  --path       : Path to the album folder you want to scan.
    -a,  --artist     : Name of the artist.
    -ap, --artist-pos : Position of the artist name in the file name.
    -sp, --song-pos   : Position of the song name in the file name.
    -e,  --extension  : Extention of the files.
    -o,  --output     : Output file for your tracklist.

    Enjoy !"""
    print(help_msg)
    exit()

def get_music_len(music_file):
    audio = pydub.AudioSegment.from_file(music_file)
    duration_sec = len(audio) // 1000
    duration_min = duration_sec // 60
    remaining_seconds = duration_sec % 60

    final_duration = f"{duration_min}:{remaining_seconds:{0}{2}}"
    return final_duration

def extract_infos_from_filename(filename, artist_pos, song_pos = 0, extension = "mp3"):
    raw_infos = filename.split(" - ")
    artist_pos = int(artist_pos)
    song_pos = int(song_pos)
    first_element_to_clean = raw_infos[0]
    track_num_regex = re.search("^[0-9]{0,}", first_element_to_clean)
    track_num = first_element_to_clean[track_num_regex.start():track_num_regex.end()].strip('._ ')
    first_element_cleaned = re.sub("^[0-9]{0,}", '', first_element_to_clean)

    if artist_pos > -1:
        if artist_pos == 0:
            artist = first_element_cleaned
            song = raw_infos[song_pos]
        else:
            artist = raw_infos[artist_pos]
            song = first_element_cleaned
    else:
        artist = ""
        song = first_element_cleaned
    clean_ext = extension.strip('.')
    ext_index = song.find(f".{clean_ext}")
    song_name = song[0:ext_index].strip('._ -')

    return track_num, artist, song_name
######################################################################

data_needed = {
    "path": "",
    "artist": "",
    "artist_pos": -1,
    "song_pos": -1,
    "extension": "mp3",
    "tracks": [],
    "outputfile": "./MusicBrainz_tracklist.txt"
}
if len(sys.argv) > 2:
    for argument in sys.argv:
        if argument in ('-p', '--path'):
            path = sys.argv[sys.argv.index(argument)+1]
            if path != '':
                data_needed["path"] = path
            else:
                print("There is no path")
                show_help()
        if argument in ('-a', '--artist'):
            artist = sys.argv[sys.argv.index(argument)+1]
            if artist != '':
                data_needed["artist"] = artist
            else:
                print("Artist is needed")
                show_help()
        if argument in ('-ap', '--artist-pos'):
            ap = sys.argv[sys.argv.index(argument)+1]
            if ap != '':
                data_needed["artist_pos"] = ap
            else:
                print("The artist index is needed")
                show_help()
        if argument in ('-sp', '--song-pos'):
            sp = sys.argv[sys.argv.index(argument)+1]
            if sp != '':
                data_needed["song_pos"] = sp
            else:
                print("The song index is needed")
                show_help()
        if argument in ('-e', '--extension'):
            ext = sys.argv[sys.argv.index(argument)+1]
            if ext != '':
                data_needed["extension"] = ext
            else:
                print("The extension is needed")
                show_help()
        if argument in ('-o', '--output'):
            output = sys.argv[sys.argv.index(argument)+1]
            if output != '':
                data_needed["outputfile"] = output
            else:
                print("The output file is needed")
                show_help()
                
else:
    show_help()

if data_needed["path"] == "":
    print("There is no path :(\n")
    show_help()

scanned_dir = os.scandir(data_needed["path"])
print("Formating datas")
for entry in scanned_dir:
    if entry.is_file():
        if data_needed["song_pos"] == -1 and data_needed["artist_pos"] == -1:
            data_needed["song_pos"] = 0
        fn_track_number, fn_artist, fn_song = extract_infos_from_filename(entry.name, data_needed["artist_pos"], data_needed["song_pos"], data_needed["extension"])
        
        if data_needed["artist"] != "" :
            artist_segment = f"- {data_needed['artist']} "
        else:
            if fn_artist != "":
                artist_segment = f"- {fn_artist} "
            else:
                print("You may need an artist for MusicBrainz :^)")
                show_help() 

        track_num = f"{fn_track_number:{0}{2}}."
        new_track = f"{track_num} {fn_song} {artist_segment}({get_music_len(entry.path)})"
        data_needed["tracks"].append(new_track)

sorted_tracklist = sorted(data_needed["tracks"])
with open(data_needed["outputfile"], 'w') as tracklist_file:
    for t in sorted_tracklist:
        tracklist_file.write(t)
        tracklist_file.write("\n")
print(f"Your tracklist is save in {data_needed['outputfile']}")