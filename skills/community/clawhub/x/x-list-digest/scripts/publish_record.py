"""Record a native CLI publication after checking its fetched Markdown."""
import argparse
import hashlib
import json
import re
import sqlite3
from pathlib import Path
from urllib.parse import urlparse
from common import write


def finalize(directory, document_id, document_url, fetched):
    directory=Path(directory)
    receipt=json.loads((directory/'receipt.json').read_text())
    meta=json.loads((directory/'metadata.json').read_text())
    state=json.loads((directory/'publish-state.json').read_text())
    parsed=urlparse(document_url)
    if parsed.scheme!='https' or not (parsed.hostname or '').endswith('.feishu.cn'):
        raise ValueError('expected native Feishu document URL')
    if state.get('document_id')!=document_id or state.get('doc_url')!=document_url:
        raise ValueError('document must match saved native CLI creation receipt')
    report=Path(receipt['report_path'])
    body=report.read_text()
    if state.get('verified'):
        if receipt.get('feishu_doc_url')!=document_url:raise ValueError('publication receipt inconsistent')
        return receipt
    suffix='\nFull Feishu report：'+document_url+'\n'
    original=body[:-len(suffix)] if body.endswith(suffix) else body
    if hashlib.sha256(original.encode()).hexdigest()!=state['content_sha256']:
        raise ValueError('report changed after publication started')
    remote=Path(fetched).read_text()
    # Import/export may change whitespace; all nonempty lines must retain content.
    def normalize(text):
        text=re.sub(r'\\([\\`*_\[\]$~<>#!+|{}().])',r'\1',text)
        text=re.sub(r'(?m)^\s*(?:>\s*)+','',text)
        return re.sub(r'\s+','',text)
    normalized=normalize(remote)
    cursor=0
    for line in original.splitlines():
        if not line.strip() or re.fullmatch(r'[|: >-]+',line):continue
        needle=normalize(line)
        position=normalized.find(needle,cursor)
        if position<0:raise ValueError('fetched document does not contain complete ordered report')
        cursor=position+len(needle)
    with sqlite3.connect(Path(meta['data_dir'])/'digest.db') as db:
        row=db.execute('SELECT metadata,feishu_doc_url FROM digests WHERE id=?',(receipt['digest_id'],)).fetchone()
        if not row or json.loads(row[0]).get('run_id')!=meta['run_id']:
            raise ValueError('digest does not belong to this run')
        if row[1] and row[1]!=document_url:raise ValueError('digest already has another publication')
        db.execute('UPDATE digests SET feishu_doc_url=? WHERE id=?',(document_url,receipt['digest_id']))
    if not body.endswith(suffix):
        with report.open('a') as output:output.write(suffix)
    receipt['feishu_doc_url']=document_url
    write(directory/'receipt.json',receipt)
    state.update(verified=True,pending=None,fetched_sha256=hashlib.sha256(remote.encode()).hexdigest())
    write(directory/'publish-state.json',state)
    return receipt


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--run-dir',required=True);p.add_argument('--document-id',required=True)
    p.add_argument('--document-url',required=True);p.add_argument('--fetched',required=True)
    a=p.parse_args()
    print(json.dumps(finalize(a.run_dir,a.document_id,a.document_url,a.fetched),ensure_ascii=False))
