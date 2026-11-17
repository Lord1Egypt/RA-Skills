import argparse,json,sqlite3
from datetime import datetime,timezone
from common import read
from pathlib import Path
def persist(db,rows,meta,raw_path,enriched_path):
    Path(db).parent.mkdir(parents=True,exist_ok=True)
    with sqlite3.connect(db) as c:
        c.execute('PRAGMA foreign_keys=ON')
        c.executescript('''CREATE TABLE IF NOT EXISTS digests(id INTEGER PRIMARY KEY,created_at TEXT,list_name TEXT,list_url TEXT,window_hours INTEGER,tweet_count INTEGER,metadata TEXT,raw_tweets_json_path TEXT,enriched_tweets_json_path TEXT,feishu_doc_url TEXT,feishu_msg_id TEXT);
        CREATE TABLE IF NOT EXISTS tweets(tweet_id TEXT PRIMARY KEY,author_handle TEXT,timestamp_iso TEXT,category TEXT,subcategory TEXT,tickers TEXT,sentiment TEXT,key_thesis TEXT,raw_json TEXT);
        CREATE TABLE IF NOT EXISTS digest_tweets(digest_id INTEGER REFERENCES digests(id),tweet_id TEXT REFERENCES tweets(tweet_id),PRIMARY KEY(digest_id,tweet_id));''')
        c.execute("CREATE UNIQUE INDEX IF NOT EXISTS digest_run ON digests(json_extract(metadata,'$.run_id')) WHERE json_extract(metadata,'$.run_id') IS NOT NULL")
        if meta.get('run_id'):
            existing=c.execute("SELECT id FROM digests WHERE json_extract(metadata,'$.run_id')=?",(meta['run_id'],)).fetchone()
            if existing:return existing[0]
        did=c.execute('INSERT INTO digests(created_at,list_name,list_url,window_hours,tweet_count,metadata,raw_tweets_json_path,enriched_tweets_json_path) VALUES(?,?,?,?,?,?,?,?)',
          (datetime.now(timezone.utc).isoformat(),meta['list_name'],meta['list_url'],meta['window_hours'],len(rows),json.dumps(meta,ensure_ascii=False),raw_path,enriched_path)).lastrowid
        for r in rows:
            c.execute('INSERT INTO tweets VALUES(?,?,?,?,?,?,?,?,?) ON CONFLICT(tweet_id) DO UPDATE SET category=excluded.category,subcategory=excluded.subcategory,tickers=excluded.tickers,sentiment=excluded.sentiment,key_thesis=excluded.key_thesis',
              (r['tweet_id'],r['author_handle'],r['timestamp_iso'],r['category'],r['subcategory'],json.dumps(r['tickers']),r['sentiment'],r['key_thesis'],json.dumps(r,ensure_ascii=False)))
            c.execute('INSERT INTO digest_tweets VALUES(?,?)',(did,r['tweet_id']))
    return did
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--db',required=True);p.add_argument('--input',required=True);p.add_argument('--raw',required=True);p.add_argument('--metadata',required=True);a=p.parse_args()
    print(persist(a.db,read(a.input),json.loads(Path(a.metadata).read_text()),a.raw,a.input))
