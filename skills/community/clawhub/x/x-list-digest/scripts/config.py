import re
from pathlib import Path
import yaml
URL=re.compile(r'^https://x\.com/i/lists/([0-9]+)$')
def load(path):
    config=yaml.safe_load(Path(path).read_text()) or {}
    if not isinstance(config,dict):raise ValueError('config must be a mapping')
    lists=config.get('lists',{})
    if not isinstance(lists,dict):raise ValueError('lists must map aliases to objects')
    for alias,item in lists.items():
        if not isinstance(item,dict) or not URL.fullmatch(item.get('url','')):raise ValueError(f'invalid URL for {alias}')
    return config
def resolve(config,value):
    if URL.fullmatch(value):return {'name':f"X List {URL.fullmatch(value)[1]}",'url':value}
    lists=config.get('lists',{})
    if value in lists:return {'name':lists[value].get('name',value),'url':lists[value]['url']}
    matches=[i for i in lists.values() if i.get('name')==value]
    if len(matches)==1:return matches[0]
    raise ValueError(f'unknown/ambiguous list: {value}')
