from flask import Blueprint, render_template

import requests
import json

general = Blueprint('general', __name__)


@general.route("/")
def splash(name=None):
    return render_template('splash.html')


@general.route("/about")
def about():
    logins = {'cindyqtruong': 0, 'BrandonHarrisonCode': 1, 'hrfofut': 2, 'straitlaced': 3, 'fantomats15': 4}
    iss_count = []
    iss_total = 0
    for i in range(0, 5):
        iss_count.append(0)
    req = requests.get('https://api.github.com/repos/hrfofut/idb/stats/contributors')
    req_list = req.json()
    d = {'total': 0}
    for x in req_list:
        d[x['author']['login']] = x['total']
        d['total'] += x['total']
    req_issue = requests.get('https://api.github.com/repos/hrfofut/idb/issues?state=all&page=1&per_page=500')
    for x in (req_issue.json()):
        iss_total += 1
        iss_count[logins[x['user']['login']]] += 1
    iss_count.append(iss_total)
    return render_template('about.html', commits=d, issues=iss_count)

# Error handling


@general.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@general.errorhandler(500)
def internal_error(e):
    return render_template('errors/500.html'), 500
