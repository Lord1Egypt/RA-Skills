"""Combine completed list reports into one daily Markdown archive."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from zoneinfo import ZoneInfo
from common import iso,write
from daily_report import merge,ranked,render_daily,render_weekly
from datetime import date as archive_date,timedelta


def bundle(directories,keywords,output,editorial=None,weekly=False):
    rows,records=merge(directories)
    if ranked(rows) and (not editorial or any(not editorial.get(r['tweet_id'],{}).get(k) for r in ranked(rows) for k in ('topic','writing_direction'))):
        raise ValueError('each ranked post requires a grounded topic and writing_direction')
    dates={iso(r['metadata']['window_end']).astimezone(ZoneInfo(r['metadata']['timezone'])).strftime('%Y-%m-%d') for r in records}
    if len(dates)!=1:raise ValueError('daily bundle must have exactly one archive date')
    words=[]
    for word in keywords:
        word=re.sub(r'[\s/\\\x00-\x1f_]+','',word).strip()
        word=word[:20]
        if word and word not in words:words.append(word)
    if not words:words.append('No valuable topic')
    for status in ['Partial coverage' if any(r['metadata']['coverage']=='partial' for r in records) else 'Window checked','Low information','Single topic']:
        if len(words)<3 and status not in words:words.append(status)
    words=words[:3];date=next(iter(dates));title=date+'_'+'_'.join(words)
    body=render_daily(rows,records,date,editorial)
    weekly=weekly or archive_date.fromisoformat(date).weekday()==6
    if weekly:
        end=iso(records[-1]['metadata']['window_end']).astimezone(ZoneInfo(records[-1]['metadata']['timezone'])).date()
        paths=[]
        for r in records:
            for receipt in Path(r['metadata']['data_dir']).glob('runs/*/*/receipt.json'):
                m=json.loads((receipt.parent/'metadata.json').read_text())
                day=iso(m['window_end']).astimezone(ZoneInfo(m['timezone'])).date()
                if end-timedelta(days=6)<=day<=end:paths.append(receipt.parent)
        wr,ws=merge(paths);body+='\n'+render_weekly(wr,ws)
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True);output.write_text(body)
    manifest={'date':date,'month':date[:7],'title':title,'keywords':words,'report_path':str(output.resolve()),'tweet_ids':[r['tweet_id'] for r in rows],'published_tweet_ids':[r['tweet_id'] for r in rows if r['category']!='off_topic'],'content_sha256':hashlib.sha256(body.encode()).hexdigest(),'unique_posts':len(rows),'sources':[{'run_dir':r['run_dir'],'run_id':r['metadata']['run_id'],'list_url':r['metadata']['list_url'],'report_sha256':hashlib.sha256(Path(r['receipt']['report_path']).read_bytes()).hexdigest()} for r in records]}
    manifest['weekly_required']=archive_date.fromisoformat(date).weekday()==6
    manifest['weekly_included']=weekly
    write(output.with_suffix('.json'),manifest)
    return manifest


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run-dir',action='append',required=True)
    p.add_argument('--keyword',action='append',default=[]);p.add_argument('--output',required=True)
    p.add_argument('--editorial');p.add_argument('--weekly',action='store_true')
    a=p.parse_args();print(json.dumps(bundle(a.run_dir,a.keyword,a.output,json.loads(Path(a.editorial).read_text()) if a.editorial else None,a.weekly),ensure_ascii=False))
