"""Deduplicate archive snapshots and render an editorial daily report."""
import json
from collections import Counter,defaultdict
from pathlib import Path
from zoneinfo import ZoneInfo
from common import iso
from render import literal,link

CATEGORY_NAMES={'crypto':'Crypto markets','us_stock':'US equities／US industry','hk_stock':'Hong Kong equities','a_stock':'A equities','macro':'Macro','trading_psychology':'Trading psychology','other':'Other topics'}


def merge(directories):
    sources=[];posts={}
    for directory in sorted({str(Path(p).resolve()) for p in directories}):
        p=Path(directory);meta=json.loads((p/'metadata.json').read_text())
        receipt=json.loads((p/'receipt.json').read_text())
        rows=json.loads((p/'enriched.json').read_text())
        sources.append({'run_dir':str(p),'metadata':meta,'receipt':receipt,'rows':rows})
    sources.sort(key=lambda s:iso(s['metadata']['window_end']))
    for source in sources:
        for row in source['rows']:
            if not iso(source['metadata']['window_start'])<=iso(row['timestamp_iso'])<=iso(source['metadata']['window_end']):raise ValueError('post outside source window')
            previous=posts.get(row['tweet_id'])
            merged=dict(row)
            merged['source_lists']=sorted(set((previous or {}).get('source_lists',[])+[source['metadata']['list_name']]))
            if previous:
                if len(previous['text'])>len(row['text']):
                    merged['text']=previous['text'];merged['expandable']=previous.get('expandable',False)
                merged['engagement']={**previous.get('engagement',{}),**{k:v for k,v in row.get('engagement',{}).items() if v is not None}}
            posts[row['tweet_id']]=merged
    return sorted(posts.values(),key=lambda r:iso(r['timestamp_iso']),reverse=True),sources


def ranked(rows):
    return sorted((r for r in rows if r['category']!='off_topic' and r['text'] and not r['subcategory'].startswith('AI\u56fe\u50cf')
                   and all(type(r.get('engagement',{}).get(k)) in (int,float) and r['engagement'][k]>=0 for k in ('likes','replies','reposts'))),
                  key=lambda r:(sum(r['engagement'][k] for k in ('likes','replies','reposts')),iso(r['timestamp_iso'])),reverse=True)[:5]


def render_daily(rows,sources,date,editorial=None):
    editorial=editorial or {};top=ranked(rows);core=[r for r in rows if r['category']!='off_topic'];counts=Counter(r['category'] for r in core)
    lines=['# Daily X List Writing Reference','',f'Date: {date}. Unique posts: {len(rows)}; authors: {len({r["author_handle"] for r in rows})}; lists: {len({s["metadata"]["list_url"] for s in sources})}.',
           'Partial coverage: merged observations do not establish a complete calendar day or full 24-hour coverage. Text, media and threads may remain incomplete.' if any(s['metadata']['coverage']=='partial' for s in sources) else 'Checked against source-run coverage.',
           'Same-day runs are deduplicated by post ID. Their window end times may differ; run counts are not added.','', '## Top 5 and writing directions','',
           'Method: likes + replies + reposts. Only relevant posts with observed text and all three known counts participate. Unknown counts are not zero. Counts are collection-time snapshots; popularity does not prove accuracy.',
           '| Rank | Core topic | Engagement (likes/replies/reposts; total) | Writing directions | Author/source |','|---|---|---|---|---|']
    for i,r in enumerate(top,1):
        item=editorial.get(r['tweet_id'],{})
        e=r['engagement'];score=sum(e[k] for k in ('likes','replies','reposts'))
        lines.append(f'| {i} | {literal(item.get("topic",r["key_thesis"]))} | {e["likes"]}/{e["replies"]}/{e["reposts"]}；{score} | {literal(item.get("writing_direction","A grounded writing direction is required"))} | @{literal(r["author_handle"])} [Original post]({link(r)}) |')
    if len(top)<5:lines.append(f'Insufficient comparable engagement data: only {len(top)} posts ranked; no invented items.')
    lines+=['','## Category details and statistics','','Only core-scope content is shown. Non-core evidence remains local; author off-topic statistics are weekly.','', '| Category | Unique posts | Authors |','|---|---:|---:|']
    for cat,count in counts.items():
        rs=[r for r in rows if r['category']==cat]
        lines.append(f'| {CATEGORY_NAMES.get(cat,cat)} | {count} | {len({r["author_handle"] for r in rs})} |')
    lines+=['','| Category | Author | Thesis summary | Source |','|---|---|---|---|']
    for r in sorted(core,key=lambda r:(r['category'],iso(r['timestamp_iso']))):
        lines.append(f'| {CATEGORY_NAMES.get(r["category"],r["category"])} | @{literal(r["author_handle"])} | {literal(r["key_thesis"])} | [Original post]({link(r)}) |')
    lines+=['','## Cross-author ticker comparisons','','Method: one vote per author per ticker; conflicting sentiment is mixed. Votes are not consensus. These are author claims, not independently verified facts.',
            '| Ticker | Posts | Independent authors | Sentiment votes | Viewpoints and evidence |','|---|---:|---:|---|---|']
    tickers=defaultdict(list)
    for r in core:
        for ticker in set(r['tickers']):tickers[ticker].append(r)
    for ticker,rs in sorted(tickers.items()):
        votes={a:({r['sentiment'] for r in rs if r['author_handle']==a}) for a in {r['author_handle'] for r in rs}}
        counts_votes=Counter('mixed' if len(v)>1 else next(iter(v)) for v in votes.values())
        entries='；'.join(f'@{literal(r["author_handle"])}：{literal(r["key_thesis"])} [Original post]({link(r)})' for r in rs)
        lines.append(f'| {literal(ticker)} | {len(rs)} | {len(votes)} | {literal(dict(counts_votes))} | {entries} |')
    return '\n'.join(lines)+'\n'


def render_weekly(rows,sources):
    days={iso(s['metadata']['window_end']).astimezone(ZoneInfo(s['metadata']['timezone'])).date() for s in sources}
    lines=['## Weekly off-topic statistics','',f'Observed archive days: {len(days)}. Deduplicated by post ID. The other category is not automatically off-topic. Insufficient samples below three archive days; do not infer long-term author behavior.',
           '| Author | Unique posts | Off-topic posts | Off-topic rate |','|---|---:|---:|---:|']
    for author in sorted({r['author_handle'] for r in rows}):
        rs=[r for r in rows if r['author_handle']==author];off=sum(r['category']=='off_topic' for r in rs)
        lines.append(f'| {literal(author)} | {len(rs)} | {off} | {off/len(rs):.0%} |')
    return '\n'.join(lines)+'\n'
