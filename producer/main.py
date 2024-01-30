import time
import random
import os

import redis


r = redis.Redis(host="redis", port=6379)

while True:
    with r.pubsub() as pubsub:
        r.publish("messages", f"producer({os.uname().nodename}) @ {int(time.time())}")

        time.sleep(random.randint(1, 5))
