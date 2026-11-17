"""Normalize browser-collected JSON/JSONL; does not claim to drive a local Mac."""
import argparse
from datetime import datetime, timedelta, timezone
from common import read, write, iso
def normalize(rows, end, hours, maximum):
    start=end-timedelta(hours=hours); result={}
    for row in rows:
        if start <= iso(row['timestamp_iso']) <= end:
            ident=str(row['tweet_id'])
            if not ident.isdigit(): raise ValueError('invalid tweet_id')
            result[ident]={**row,'tweet_id':ident}
    # maximum is a collection stop budget, never a destructive export slice.
    return sorted(result.values(),key=lambda r:iso(r['timestamp_iso']),reverse=True)
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--input',required=True);p.add_argument('--output',required=True)
    p.add_argument('--window',type=int,default=24);p.add_argument('--max-tweets',type=int,default=300);p.add_argument('--end')
    a=p.parse_args()
    if a.window<=0 or a.max_tweets<=0:p.error('limits must be positive')
    write(a.output,normalize(read(a.input),iso(a.end) if a.end else datetime.now(timezone.utc),a.window,a.max_tweets))
