howdoi_web
==========

Added REST api to [howdoi](https://github.com/gleitz/howdoi) python module.

Using Stackoverflow API instead of Fetching page and parsing HTML.

Usage:

1. Update Stackoverflow API key S_KEY in howdoi.py
2. Start Server with app.py

REST call example: [here](http://howdoi1.herokuapp.com/howdoi?q=concat%20string%20java)

Sample Response:

    {
      "status": "success", 
    }


