import time

import redis
from flask import Flask
import math

app = Flask(app.py)
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def isPrime(number):
    for i in range(2,math.floor(number/2)): #check for factors
        if (number % i) == 0:
            print(num, " is not prime.")
            return;
    print(num, " is prime.")
    
@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
