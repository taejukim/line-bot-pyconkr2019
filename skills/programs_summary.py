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

@add_skill(r'프로그램요약')
def get_programs_summary(message):
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
    lst = list()
    for p in presentations:
        if not p['place']:
            continue
        lst.append('{0} | {1} | {2}'.format(p['name'], p['place']['name'], p['owner']['profile']['name']))
    return TextSendMessage(text='</br>'.join(lst))
