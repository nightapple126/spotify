# Kevin's result

## Overview
This command line (console) application is one for BuildBook Coding Exercise.

## Install
 * Download and install Python3(if you have not it) - [Here](https://www.python.org/downloads/)
 * Unlike other python projects, this project never used any third-party dependency modules.

 In your terminal:
```
$ git clone https://github.com/nightapple126/spotify.git
$ cd spotify
$ python main.py .\input\spotify.json .\input\changes.json .\output\output.json
```

## Usage
`$ python main.py <input-file> <changes-file> <output-file>`

For example, in this program:
`$ python python main.py .\input\spotify.json .\input\changes.json .\output\output.json`

## Validation of output
This program process the validation of the <changes-file> internally, so the validation of output is guaranteed.

## Large scale
This program reads the files at once and load all data into the PC's memory(RAM).
It is okay regarding not so large files, but when using very large input file and changes file, the architecture will cause the problem definitely.
At that case, I think that some progressive method that uses proper sized buffer should be used.

## Structure of <changes-file>
{
  "playlist": {
    "update": [
      {
        "id": "",
        "song_ids": []
      }
    ],
    "create": [
      {
        "owner_id": "",
        "song_ids": []
      }
    ],
    "delete": [
      {
        "id": ""
      }
    ]
  }
}

## Spent of time
2.5 hours to completed the program and 0.5 hours to make the readme.

