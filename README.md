# Multi-Threaded-Snapchat-Downloader
Simple multi-threaded snapchat memories downloader.  Requires 'memories_history.json' provided by snapchat upon data request.

## Usage
place 'memories_history.json' from the snapchat json data zip into same directory as main.py

Run
```
python3 main.py
```
Using ```SnapChatDL```
```
from snapchatdl.dl import*
...
snap = SnapChatDL(input_path, return_path)
snap.run(instance_n_threads, batch_per_thread)
```



