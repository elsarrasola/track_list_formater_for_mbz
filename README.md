# Tracklist formater for MusicBrainz

This little CLI programme, will scan your album folder and format a tracklist file ready to be send to MusicBrainz.

## REQUIREMENTS

- [Python3](https://www.python.org/downloads/)
- `pydub==0.25.1`
- `audioop-lts==0.2.2`

## INSTALL

### 1. Clone the repo or download the zip

```bash
git clone https://github.com/elsarrasola/track_list_formater_for_mbz.git

# Or

unzip ~/Downloads/track_list_formater_for_mbz.zip
```

### 2. Go in the src folder

Do I realy need to show you how to do this ?

### 3. Install the required packages (if you don't already did it)

```bash
pip install -e .
```

Here you go !

## USE IT

### Flags

```
-h,  --help       : show this message.
-p,  --path       : Path to the album folder you want to scan.
-a,  --artist     : Name of the artist.
-ap, --artist-pos : Position of the artist name in the file name.
-sp, --song-pos   : Position of the song name in the file name.
-e,  --extension  : Extention of the files.
-o,  --output     : Output file for your tracklist.
```

### Exemple

For a forlder called `Human_After_All` with the artist `Daft Punk` :

#### 1. Files name are in this format : `song.mp3`

```
format-mbz.py -p ./Human_After_All -a 'Daft Punk' -e mp3 -o ./dp_haa_tracklist.txt
```

#### 2. Files names are in this format : `Daft Punk - song.mp3`

```
format-mbz.py -p ./Human_After_All -ap 0 -sp 1 -e mp3 -o ./dp_haa_tracklist.txt
```
