# meet-me-in-the-middle

<p align="left">
  <img width=40% src="https://raw.githubusercontent.com/andrew-curthoys//meet-me-in-the-middle/master/docs/meet_me_logo.png">
</p>

![PyPI - License](https://img.shields.io/pypi/l/meetme)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/meetme)
![PyPI](https://img.shields.io/pypi/v/meetme?color=blue)
[![Build Status](https://travis-ci.com/andrew-curthoys/meetme.svg?branch=master)](https://travis-ci.com/andrew-curthoys/meetme)

# Overview
Meet Me in the Middle is a flight search engine for meeting up with friends, family, and loved ones who live in a different city. The user will input two origin cities and MMitM will output a table with flight prices for common destinations 

# Usage
Create a 'flight_frame' object and give it a name. User will need to input their API key & API secret to authenticate to run requests.
```python
import meet_me
ff = meet_me.FlightFrame(api_key, api_secret)
```

To return a dataframe with destinations and combined prices call the 'lets_go' method. Minimum inputs are two origin cities, a departure date, and trip duration.

```python
ff.lets_meet('LAX','JFK', '2020-01-01', 7)
```