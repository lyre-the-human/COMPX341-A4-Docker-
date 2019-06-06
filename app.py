import time
import traceback
import redis
from flask import Flask
import math

app = Flask(__name__)
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
@app.route('/isPrime/<number>')
def isPrime(number):
    try:
        num = int(number)
        if(num < 2):
            return(str(num)+" is not prime.")

        for i in range(2,math.floor(num/2)): #check for factors
            if (num % i) == 0:
                return(str(num)+" is not prime.")
        #check if number was stored in redis previousl
        if cache.get(str(num)) == None:
            cache.set(str(num), str(num))
            print(str(num) + "WAS STORED BY REDIS")
        return(str(num)+" is prime.")
    except Exception as e:
        print(e)
        traceback.print_stack(e)
        return('Please provide an integer')

       
    
@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
