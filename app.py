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

#----------------------------------------------------------------------------

@app.route('/isPrime/<number>')
def isPrime(number):
    try:
        num = int(number)

        #if number is 0, 1 or negative
        if(num < 2):
            return(str(num)+" is not prime.")

        #if number already exists in the list
        listLength = cache.llen('listPrimes')
        if listLength != 0:
            for x in range (0,listLength):
                element = cache.lindex('listPrimes', x)
                element = str(element, 'utf-8')
                if element == str(num):
                    return(str(num)+" is prime.")
        #else
        for i in range(2,math.floor(num/2)): #check for factors
            if (num % i) == 0:
                return(str(num)+" is not prime.")
        #store to redis if prime
        cache.rpush('listPrimes', str(num)) 
        return(str(num)+" is prime.")
    except Exception as e:
        print(e)
        traceback.print_stack(e)
        return('Please provide an integer')

#----------------------------------------------------------------------------

@app.route('/primesStored/')
def primesStored():
    #TODO get redis list and store each element into test list
    listLength = cache.llen('listPrimes')
    if listLength == 0:
        return("No primes stored yet")
    testList = []
    for x in range (0,listLength):
        element = cache.lindex('listPrimes', x)
        element = str(element, 'utf-8')
        testList.append(element)

    string = ', '.join(str(e) for e in testList)
    return(string) 
#----------------------------------------------------------------------------    
@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
