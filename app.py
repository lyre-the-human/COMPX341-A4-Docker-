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

	#if num == 2147483647:
          #  cache.rpush('listPrimes', str(num)) 
          #  return(str(num)+" is prime.")

        #else
        if num % 2 != 0 and num % 3 != 0 and num % 5 != 0 and num % 7 != 0 and num > 7 :
            for i in range(7,math.floor(num/4)): #check for factors but only those which are odd
                oddNum = i*2+1
                if (num % oddNum) == 0:
                    return(str(num)+" is not prime.")
        #store to redis if prime
            cache.rpush('listPrimes', str(num)) 
            return(str(num)+" is prime.")

        else:
            if num== 2 or num == 3 or num == 5 or num == 7:
                cache.rpush('listPrimes', str(num)) 
                return(str(num)+" is prime.")
            return(str(num)+" is not prime.")

    except Exception as e:
        #print(e)
        #traceback.print_stack(e)
        return("Please provide an integer")

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
