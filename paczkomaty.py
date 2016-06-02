#!/usr/bin/python

import json
import subprocess
import requests
import time
import random
import sys
import smtplib
import config


STATUS_URL = 'https://tracking.inpost.pl/api/v1/history/package[0]=%s?_=%s'


def send_email(message, subject):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(config.username, config.password)
    message_body = 'Subject: %s\n\n%s' % (subject, message)
    server.sendmail(config.fromaddr, config.toaddrs, message_body)
    server.quit()


def get_status(pkg_id):
    random_three_digits = "%03d" % random.randint(0, 999)
    epoch_now = '%d%s' % (time.time(), random_three_digits)
    url = STATUS_URL % (pkg_id, epoch_now)
    # url = url.replace('[', '\\[').replace(']', '\\]')
    # s = subprocess.check_output(['curl', url, '-s',
    #                              '-H', 'Origin: https://twoj.inpost.pl'])
    s = requests.get(url, headers={'Origin': 'https://twoj.inpost.pl'}).text
    j = json.loads(s)
    last_history_key = [j['history'].keys()[-1]]
    return j['history'][last_history_key]['pl']

if __name__ == '__main__':
    package_no = sys.argv[1]
    old_status = None
    while True:
        status = get_status(package_no)
        if status != old_status:
            send_email(status, 'New paczkomaty status for %s' % package_no)
            old_status = status
        time.sleep(5.0)
