# surveymonkey-takeout
Export all your surveys using API.

## Purpose
Now you can easily backup all your surveys with single tool! Not meant for taking your data to another solution (that would be against their TOS..).

## Usage

Visit `https://api.surveymonkey.net/v3/docs` and create an app. This will provide you access token.

Edit the `main.py`, insert token and run it.


## Limits

Survey Monkey enforces limits on API (120req/minute, 500req/day), this app sleeps for 24h when the number of requests exceed 500. Thas should be enough for exporting ~230 surveys.
