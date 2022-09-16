import json
import requests
import threading
import os


class SnapChatDL:
    def __init__(self, json_path, return_path=os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))):
        self.store_path = os.path.join(return_path, "memories_dl")

        self.length = 0
        self.queue = []
        self.verbose_msg = []
        self.threads = []
        self.json_path = json_path
        self.lock_q = threading.Lock()

    def dl_thread(self, thread_num, batch):
        snap_queue = []

        self.lock_q.acquire()
        q_length = len(self.queue)
        self.lock_q.release()

        while q_length != 0:
            self.lock_q.acquire()
            for i in range(batch):
                try:
                    snap_queue.append(self.queue.pop())
                except:
                    pass
            self.lock_q.release()

            for snap in snap_queue:
                url = snap["Download Link"]
                media_type = snap['Media Type']
                date = snap['Date']

                try:
                    req = requests.post(url, allow_redirects=True)
                    response = req.text
                    file = requests.get(response)

                    day = date.split(" ")[0]
                    snap_time = date.split(" ")[1].replace(':', '-')
                    filename = f'{self.store_path}/{day}_{snap_time}.mp4' if media_type == 'Video' else f'{self.store_path}/{day}_{snap_time}.jpg'

                    with open(filename, 'wb') as f:
                        f.write(file.content)

                    print("Download Success: Snap @ " + date)
                except:
                    print("Download Failed: Snap @ " + date)

            self.lock_q.acquire()
            q_length = len(self.queue)
            self.lock_q.release()

    def run(self, thread_count=10, batch=10):
        try:
            with open(self.json_path) as file:
                mem = json.load(file)
                self.queue = mem["Saved Media"]
                print("Total: " + str(len(self.queue)))
        except:
            print("trouble opening/ finding file " + str(self.json_path))
            return

        if not os.path.exists(self.store_path):
            os.mkdir(self.store_path)

        for i in range(thread_count):
            thread = threading.Thread(target=self.dl_thread, args=(i, batch))
            thread.start()
            self.threads.append(thread)

        for thread in self.threads:
            thread.join()

        print("Finished")