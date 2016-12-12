# Copyright (C) 2016 Simon Shields
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import os
import subprocess
import sys

import praw
if 'IS_TRAVIS' not in os.environ:
    try:
        with open('/home/simon/.redditrc') as f:
            CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD = f.readline().strip().split('|')
    except Exception:
        print('Please put CLIENT_ID|CLIENT_SECRET|REDDIT_USERNAME|REDDIT_PASSWORD in ~/.redditrc')
else:
    print('Travis detected, using environment variables...')
    CLIENT_ID = os.environ['CLIENTID']
    CLIENT_SECRET = os.environ['SECRET']
    USERNAME = os.environ['USERNAME']
    PASSWORD = os.environ['PASSWORD']

reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
        password=PASSWORD, username=USERNAME,
        user_agent='CSS Uploader on Python %d.%d'%(sys.version_info.major, sys.version_info.minor))

sub = 'laoscss'

if len(sys.argv) > 1 and '-' not in sys.argv[-1]:
    sub = sys.argv[-1]

skipres = False
if '--nores' in sys.argv or '-n' in sys.argv:
    skipres = True

if not skipres:
    css = reddit.subreddit(sub).stylesheet
    print('Uploading resources...')
    for f in os.listdir('res'):
        print('Uploading %s...'%f, end=' ')
        css.upload('.'.join(f.split('.')[:-1]), os.path.join('res', f))
        print('Uploaded!')
else:
    print('Skipping resource upload.')
try:
    rev = subprocess.check_output('git rev-parse HEAD', shell=True).strip()
    dirty = subprocess.check_output('git diff HEAD', shell=True).strip() != ''
except subprocess.CalledProcessError:
    rev = 'unknown'
    dirty = False

ver = rev + ('-dirty' if dirty else '')
print('Uploading CSS version %s'%ver)
with open('theme.css') as f:
    c = f.read()
    css.update(c, reason='update CSS to ' + ver)


