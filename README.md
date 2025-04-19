# NoteSharer
This is a simple project to automate the monitoring and pushing of notes. I originally wrote this for my Obsidian notes folder that I like to share across devices. This could be used for any folder though where you want all files and subdirectories to be staged, committed, and pushed automatically after a period of time when changes are no longer detected.

## Getting started
I would recommend forking this repository or duplicating it to begin a new repo for your own notes. This way you will aready be set up with a repo where your notes may live.
### Setup
- In a terminal, enter the directory in which you've locally cloned your repo.
- I recommend using a virtual environment to keep things clean:
    ```
    python3 -m venv .venv
    source .venv/bin/activate
    ```
- Install the required dependencies
    ```
    pip install -r requirements.txt
    ```
- You may run the script either in the foreground or background. For testing your own changes, foreground makes sense. For actual usage, I would recommend running in the background.
### Background process
#### Start
`bash start_auto_commit.sh`
#### End
```
ps aux | grep auto_commit.py
kill <process num>
```
### Foreground Process
#### Start
```
python3 auto_commit.py
```
#### End
`Ctl-C` will keyboard interrupt and end the script.
## Watch
If you want to watch the logs, run 
```
tail -f logs/auto_commit.log
```

## Customization
Feel free to change this however you please. Things you may want to customize:
- Commit Timeout
    - Default: 10 minutes (600s)
    - This is the amount of time from the last change detected before the script will auto commit and push.
- Path:
    - Default: Current working directory
    - You may wish to hard code this value so it will run on the same directory regardless of where you start it from.
- Credentials:
    - Default: Local config and SSH key
    - You may wish to configure differently using a token, hard-coded sign in (maybe refrain from this one...), or some other funky config. This was the most straightforward and simple solution to me though.
    - Note, this will push to whatever branch you have checked out.
- Logging:
    - Default: 1 file, rotating at size of 1MB
    - This was mainly for debugging purposes, you may change the number of rollover files, size of rollover, or do away with this entirely. Just be careful not to make a never ending, size increasing log file that isn't all that useful or important.
- Literally anything else:
    - Default: This project, as you cloned it
    - Do whatcha want with it!