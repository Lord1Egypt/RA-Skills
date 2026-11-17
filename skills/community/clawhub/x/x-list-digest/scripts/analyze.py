"""Validate analysis made by the invoking agent and merge original fields."""
import argparse
from collections import Counter, defaultdict
from common import read, write, CATEGORIES, SENTIMENTS
def enrich(raw, analysis):
    by_id={str(r['tweet_id']):r for r in analysis}
    if len(by_id)!=len(analysis) or set(by_id)!={str(r['tweet_id']) for r in raw}:raise ValueError('analysis IDs must match raw exactly')
    result=[]
    fields=('category','subcategory','tickers','sentiment','key_thesis','is_actionable','confidence','is_thread_continuation','thread_root_id')
    for row in raw:
        a=by_id[str(row['tweet_id'])]
        if a['category'] not in CATEGORIES or a['sentiment'] not in SENTIMENTS:raise ValueError('invalid category/sentiment')
        if a['confidence'] not in ('high','med','low'):raise ValueError('invalid confidence')
        if not isinstance(a['tickers'],list) or not all(isinstance(t,str) and t for t in a['tickers']):raise ValueError('invalid tickers')
        if not isinstance(a['key_thesis'],str) or not isinstance(a['is_actionable'],bool) or not isinstance(a['is_thread_continuation'],bool):raise ValueError('invalid analysis types')
        merged={**row,**{k:a[k] for k in fields}}
        merged['tickers']=list(dict.fromkeys(t.lstrip('$').upper() for t in a['tickers']))
        result.append(merged)
    observed={r['tweet_id']:r for r in result}
    for r in result:
        root=r['thread_root_id']
        if r['is_thread_continuation']:
            parent=observed.get(root)
            if not isinstance(root,str) or not root.isdigit() or root==r['tweet_id'] or (parent and (parent['author_handle']!=r['author_handle'] or parent['is_thread_continuation'])):
                raise ValueError('thread root must be an observed root post by the same author')
            r['thread_root_observed']=parent is not None
        elif root is not None:
            raise ValueError('root post cannot have thread_root_id')
    return result
def aggregate(rows):
    authors=defaultdict(list);tickers=defaultdict(list)
    for r in rows:
        authors[r['author_handle']].append(r)
        for t in set(r['tickers']):tickers[t].append(r)
    return {'categories':dict(Counter(r['category'] for r in rows)),
      'authors':{a:{'total':len(rs),'categories':dict(Counter(r['category'] for r in rs)),'off_topic':sum(r['category'] in ('off_topic','other') for r in rs),
        'rate':sum(r['category'] in ('off_topic','other') for r in rs)/len(rs)} for a,rs in authors.items()},
      'tickers':{t:{'posts':rs,'author_votes':{a:('mixed' if len(ss)>1 else next(iter(ss))) for a,ss in
        ((a,{r['sentiment'] for r in rs if r['author_handle']==a}) for a in {r['author_handle'] for r in rs})}} for t,rs in tickers.items()}}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--raw',required=True);p.add_argument('--analysis',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    write(a.output,enrich(read(a.raw),read(a.analysis)))
