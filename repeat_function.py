from __future__ import print_function
from threading import Timer
from functools import partial
import time
import intrinio_sdk
from intrinio_sdk.rest import ApiException
from pprint import pprint
import sys,os
import curses

#setting up de of time which triggers the trade
class Interval(object):

    def __init__(self, interval, function, args=[], kwargs={}):
        """
        Runs the function at a specified interval with given arguments.
        """
        self.interval = interval
        self.function = partial(function, *args, **kwargs)
        self.running  = False 
        self._timer   = None 

    def __call__(self):
        """
        Handler function for calling the partial and continuting. 
        """
        self.running = False  # mark not running
        self.start()          # reset the timer for the next go 
        self.function()       # call the partial function 

    def start(self):
        """
        Starts the interval and lets it run. 
        """
        if self.running:
            # Don't start if we're running! 
            return 
            
        # Create the timer object, start and set state. 
        self._timer = Timer(self.interval, self)
        self._timer.start() 
        self.running = True

    def stop(self):
        """
        Cancel the interval (no more function calls).
        """
        if self._timer:
            self._timer.cancel() 
        self.running = False 
        self._timer  = None

#def gets stock by name using intrinio api
def Getstock(name):
    intrinio_sdk.ApiClient().configuration.api_key['api_key'] = '[your-intrino-api-key]'

    security_api = intrinio_sdk.SecurityApi()

    identifier = name # str | A Security identifier (Ticker, FIGI, ISIN, CUSIP, Intrinio ID)
    #returns info on stock in json format
    try:
        api_response = security_api.get_security_realtime_price(identifier)
        high = api_response.high_price
        low = api_response.low_price
        opn = api_response.open_price
        exc = api_response.exchange_volume
        stock = [high, low, opn, exc]
        return (stock)

    except ApiException as e:
        zip = ("Exception when calling SecurityApi->get_security_realtime_price: %s\n" % e)

#within this statement all action on the interval occour

if __name__ == "__main__":
    import time 
    import random

    def clock(start):
        """
        Prints out the elapsed time when called from start.
        """
	#stock call, must not make more than 10,000 calls per day
        myh = Getstock('NKE')
        keystr = "Nike: {}, {}, {}, {}".format(myh[0], myh[1], myh[2], myh[3])
        print(keystr)


    # Create an interval
    interval = Interval(9.0, clock, args=[time.time(),])
    print ("Starting Interval, press CTRL+C to stop.")
    interval.start() 

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            print ("Shutting down interval ...")
            interval.stop()
            break
