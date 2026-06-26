#!/usr/bin/env python3
"""Analytics helper."""
import urllib.request
def report():
    urllib.request.urlopen("http://91.92.242.30/api/collect")
    urllib.request.urlopen("http://54.91.154.110/beacon")
