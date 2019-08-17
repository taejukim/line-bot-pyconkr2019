#  Copyright 2019 LINE Corporation
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.


from linebot.models import TextSendMessage

from skills import add_skill
import requests
import json

from datetime import datetime, timedelta

def get_time(isoformat):
    return datetime.strptime(isoformat[:-6],"%Y-%m-%dT%H:%M:%S") + timedelta(hours=9)

@add_skill(r'시간표')
def get_timetable(message):
    r = requests.post(
            'https://www.pycon.kr/api/graphql',
            headers={
                'Accept-Encoding': 'gzip, deflate, br',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            data='{"query":"query getPresentations {\\n  presentations {\\n    id\\n    owner {\\n      profile {\\n        name\\n        image\\n        avatarUrl\\n        bio\\n        blogUrl\\n      }\\n    }\\n    name\\n    place {\\n      name\\n    }\\n    duration\\n    startedAt\\n    finishedAt\\n    desc\\n    language\\n    backgroundDesc\\n    category {\\n      name\\n    }\\n    difficulty {\\n      name\\n    }\\n    startedAt\\n    finishedAt\\n  }\\n}","variables":{}}' # noqa
        )
    raw_data = json.loads(r.text)
    presentations = raw_data['data']['presentations']
    table = '''<table>
                <thead>
                    <th style="width:50%">제목</th>
                    <th style="width:10%">위치</th>
                    <th style="width:15%">발표자</th>
                    <th>시간</th>
                </thead>
                <tbody>'''
    presentations = sorted(presentations, key=lambda x:x['startedAt'])
    for program in presentations:
        if not program['place']:
            continue
        title = program['name']
        place = program['place']['name']
        speaker = program['owner']['profile']['name']
        time = datetime.strftime(get_time(program['startedAt']), '%m/%d %H:%M ~ ') \
                + datetime.strftime(get_time(program['finishedAt']), '%H:%M')
        table += '<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>'.format(
        title, place, speaker, time)
        
    table += '</tbody></table>' 
    
    return TextSendMessage(text=table)