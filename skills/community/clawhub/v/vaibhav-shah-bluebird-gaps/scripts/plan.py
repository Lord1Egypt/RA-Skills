"""Original standalone class-calendar gap planner. Python standard library only."""
from datetime import datetime
import argparse
import json
from pathlib import Path

def timestamp(value):
    result=datetime.fromisoformat(value.replace('Z','+00:00'))
    if result.tzinfo is None: raise ValueError('All timestamps must have a timezone')
    return result

def plan(data,minutes):
    if not 1<=minutes<=480: raise ValueError('Duration must be 1-480 minutes')
    start,end=timestamp(data['work_start']),timestamp(data['work_end'])
    if end<=start: raise ValueError('Work end must follow start')
    events=[]
    for item in data['events']:
        a,b=timestamp(item['start']),timestamp(item['end'])
        if b<=a: raise ValueError('Event end must follow start')
        events.append((a,b,item['title']))
    events.sort()
    conflicts=[]
    for i,(a,b,title) in enumerate(events):
        for c,d,other in events[i+1:]:
            if a<d and c<b: conflicts.append([title,other])
    cursor,gaps=start,[]
    for a,b,_ in events:
        if b<=start or a>=end: continue
        if a>cursor: gaps.append((cursor,min(a,end)))
        cursor=max(cursor,b)
    if cursor<end: gaps.append((cursor,end))
    slots=[{'start':a.isoformat(),'end':b.isoformat(),'minutes':int((b-a).total_seconds()/60)} for a,b in gaps]
    return {'conflicts':conflicts,'free_slots':slots,'suitable_slots':[slot for slot in slots if slot['minutes']>=minutes]}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('calendar_json',type=Path)
    parser.add_argument('--minutes',type=int,default=45)
    args=parser.parse_args()
    print(json.dumps(plan(json.loads(args.calendar_json.read_text(encoding='utf-8')),args.minutes),indent=2))
