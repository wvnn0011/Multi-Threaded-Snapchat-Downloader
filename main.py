from snapchatdl.dl import *
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

if __name__ == "__main__":
    snap = SnapChatDL('memories_history.json', __location__)
    snap.run()

