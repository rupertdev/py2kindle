## py2kindle

py2kindle is a python script that sends .mobi files to your kindle device using Amazon's send2kindle service.

#### Setup

1. Make sure you're running Python 2.7.x
2. Git clone this repo
3. run ./py2kindle --config to set up your Kindle's email and SMTP Server settings.
    - Make sure that the email address you send from is allowed in your Kindle's email settings. 

#### Usage

usage: py2kindle.py [-h] [--file [FILE]] [--config]

optional arguments:
  -h, --help     show this help message and exit
  --file [FILE]  The file that you wish to send to your kindle.
  --config       Run py2kindle email configuration.
