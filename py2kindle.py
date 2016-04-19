#! /usr/bin/python

import argparse
import ConfigParser
import os
import smtplib
import sys
import mimetypes

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename

convert_flag = False;
cp = ConfigParser.SafeConfigParser()
cp.read('config.txt')

def send_mobi_mail(file_name):
    email = cp.get('config', 'email')
    user = cp.get('config', 'user')
    if not email:
        print 'You have not configured a kindle email address, run py2kindle --config to add one.'
        exit()

    mobi_file = open(file_name, 'rb')
    file_name = os.path.basename(file_name)
    msg = MIMEMultipart()
    msg['Subject'] = file_name
    msg['From'] = user
    msg['To'] = email
    mobi = MIMEApplication(
        mobi_file.read(),
        Content_Dispostition='attachment; filename=""%s"' % file_name.split('.')[0],
        Name=file_name)
    mobi_file.close()
    msg.attach(mobi)

    s = smtplib.SMTP(cp.get('config', 'server'))
    s.starttls()
    s.login(cp.get('config', 'user'), cp.get('config', 'pass'))

    try:
        s.sendmail(cp.get('config', 'user'), email, msg.as_string())
    except smtplib.SMTPRecipientsRefused as e:
        print "Email was refused, check your send to kindle email address."
        exit()
    except smtplib.SMTPSenderRefused as e:
        print e
        exit()
    except Exception as e:
        print e
        exit()

    s.quit()
    print(file_name + " sent to " + email + "!")

def config_emails():
    print "Leave blank for unchanged."
    print "Enter your Kindle's email address:"
    kindle_email = raw_input()
    if kindle_email is not '':
        cp.set('config', 'email', kindle_email)

    print "Enter your SMTP Server Address:"
    smtp_server = raw_input()
    if smtp_server is not '':
        cp.set('config', 'server', smtp_server)

    print "Enter your SMTP Username (email):"
    user = raw_input()
    if user is not '':
        cp.set('config', 'user', user)

    print "Enter your SMTP Password:"
    password = raw_input()
    if password is not '':
        cp.set('config', 'pass', password)

    with open('config.txt', 'wb') as cp_file:
        cp.write(cp_file)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file",
                        nargs='?',
                        required=False,
                        help="The file that you wish to send to your kindle.")
    parser.add_argument("--config",
                        action='store_const',
                        const=True,
                        default=False,
                        help="Run py2kindle email configuration.")
    parser.add_argument("--convert",
                        action='store_const',
                        const=True,
                        default=False,
                        help='Use calibre\'s ebook-convert to convert ebook to mobi and upload.')
    args = parser.parse_args()

    if args.config:
        config_emails()
    elif '.mobi' in args.file or '.pdf' in args.file:
        if (os.path.getsize(args.file)/1000 < 10000):
            send_mobi_mail(args.file)
        else:
            print("File entered was greater than 10 MegaBytes, Amazon's Limit.")
    elif not convert_flag:
        print "File entered was not a .mobi or .pdf file."
        return
    else:
        print "Converting " + args.file + "...."

if __name__ == '__main__':
    main()
