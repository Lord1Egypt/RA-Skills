"""Verify the daily editorial document and record its source associations."""
import argparse
import hashlib
import json
import re
import sqlite3
from pathlib import Path
from datetime import date
from common import write


def finalize(manifest_path,fetched):
    path=Path(manifest_path);state=json.loads(path.read_text())
    url=state.get('doc_url','');document_id=state.get('document_id','')
    if not re.fullmatch(r'https://[A-Za-z0-9.-]+\.feishu\.cn/docx/'+re.escape(document_id),url) or not document_id:
        raise ValueError('saved native Feishu document receipt required')
    body=Path(state['report_path']).read_text();remote=Path(fetched).read_text()
    if date.fromisoformat(state['date']).weekday()==6:
        if '## Weekly off-topic statistics' not in body or 'Weekly off-topic statistics' not in remote:
            raise ValueError('Sunday archive requires weekly statistics in body and readback')
    if hashlib.sha256(body.encode()).hexdigest()!=state['content_sha256']:raise ValueError('daily body changed')
    def normalize(text):
        text=re.sub(r'\\([\\`*_\[\]$~<>#!+|{}().])',r'\1',text)
        return re.sub(r'\s+','',text)
    content=normalize(remote);cursor=0
    for line in body.splitlines():
        if not line.strip() or re.fullmatch(r'[|: >-]+',line):continue
        needle=normalize(line);position=content.find(needle,cursor)
        if position<0:raise ValueError('daily readback missing ordered content')
        cursor=position+len(needle)
    for tweet_id in state.get('published_tweet_ids',state['tweet_ids']):
        if '/status/'+tweet_id not in remote:raise ValueError('daily readback missing source')
    checked=[]
    for source in state['sources']:
        directory=Path(source['run_dir']);receipt=json.loads((directory/'receipt.json').read_text());meta=json.loads((directory/'metadata.json').read_text())
        if hashlib.sha256(Path(receipt['report_path']).read_bytes()).hexdigest()!=source['report_sha256']:raise ValueError('source report changed')
        with sqlite3.connect(Path(meta['data_dir'])/'digest.db') as db:
            row=db.execute('SELECT metadata,feishu_doc_url FROM digests WHERE id=?',(receipt['digest_id'],)).fetchone()
            if not row or json.loads(row[0]).get('run_id')!=source['run_id']:raise ValueError('source digest ownership mismatch')
            if row[1] and row[1]!=url:raise ValueError('source digest already published elsewhere')
        checked.append((directory,receipt,meta))
    for directory,receipt,meta in checked:
        with sqlite3.connect(Path(meta['data_dir'])/'digest.db') as db:
            db.execute('UPDATE digests SET feishu_doc_url=? WHERE id=?',(url,receipt['digest_id']))
        receipt.update(feishu_doc_url=url,daily_manifest=str(path.resolve()))
        write(directory/'receipt.json',receipt)
    state.update(verified=True,pending=None,fetched_sha256=hashlib.sha256(remote.encode()).hexdigest())
    write(path,state)
    return state


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--manifest',required=True);p.add_argument('--fetched',required=True)
    a=p.parse_args();print(json.dumps(finalize(a.manifest,a.fetched),ensure_ascii=False))
