import argparse
from analyze import aggregate
from common import read
from pathlib import Path
import re
from collections import Counter
from zoneinfo import ZoneInfo
from common import iso
def literal(value):
    text=re.sub(r'([\\`*_\[\]$~<>#!+|{}()])',r'\\\1',str(value)).replace('\n',' ')
    return re.sub(r'^(\d+)\.',r'\1\\.',text)
def cell(s):return literal(s)
def link(row):
    ident=str(row['tweet_id']);handle=row['author_handle']
    if not ident.isdigit() or not re.fullmatch(r'[A-Za-z0-9_]{1,50}',handle):raise ValueError('invalid post identity')
    return f'https://x.com/{handle}/status/{ident}'
def stamp(value,meta):return iso(value).astimezone(ZoneInfo(meta.get('timezone','Asia/Bangkok'))).strftime('%Y-%m-%d %H:%M:%S %Z')
def render(rows, meta):
    stats=aggregate(rows);lines=[f"# X List「{literal(meta['list_name'])}」Digest",'',
      f"Total posts：{len(rows)}；Authors：{len(stats['authors'])}；Window：{stamp(meta['window_start'],meta)} — {stamp(meta['window_end'],meta)}",
      f"Coverage status：{meta.get('coverage','partial')}；Stop reason：{meta.get('stop_reason','unknown')}",'',
      '## Top summary']
    if meta.get('coverage','partial')=='partial':
        lines.insert(5,'**Partial coverage：this report includes only observed content，not all posts in the window。**')
    if 'window_coverage' in meta:
        lines.insert(5,f"Window evidence：{meta['window_coverage']}；Unexpanded posts：{meta.get('unexpanded_posts',0)}；Batch count overshoot：{meta.get('budget_overshoot',0)}")
    relevant=[r for r in rows if r['category'] not in ('off_topic','other')]
    ranked=[r for r in relevant if all(type(r.get('engagement',{}).get(k)) in (int,float) and r['engagement'][k]>=0 for k in ('likes','replies','reposts'))]
    lines.append('Ranking method：likes+replies+reposts，rank only relevant posts with three known engagement counts。')
    if len(ranked)<len(relevant):lines.append('Insufficient engagement data：some posts are excluded from rankings，cannot infer the hottest posts across the entire list。')
    for r in sorted(ranked,key=lambda r:sum(r['engagement'][k] for k in ('likes','replies','reposts')),reverse=True)[:3]:
        lines.append(f"- Popular：@{literal(r['author_handle'])} — {literal(r['key_thesis'])} [Original post]({link(r)})")
    seen=set()
    for r in sorted(relevant,key=lambda r:(r['is_actionable'],{'high':2,'med':1,'low':0}[r['confidence']]),reverse=True):
        thesis=' '.join(r['key_thesis'].split()).casefold()
        if thesis in seen:continue
        seen.add(thesis)
        lines.append(f"- Core thesis：@{literal(r['author_handle'])}：{literal(r['key_thesis'])}")
        if len(seen)>=6:break
    lines.append('Off-topic TOP 3（this window sample，not long-term behavior）：')
    offenders=sorted(((a,d) for a,d in stats['authors'].items() if d['off_topic']),key=lambda kv:(kv[1]['rate'],kv[1]['off_topic']),reverse=True)[:3]
    for a,d in offenders:lines.append(f"- @{literal(a)}：{d['off_topic']}/{d['total']}，{d['rate']:.0%}")
    if not offenders:lines.append('- no off-topic posts observed in this window。')
    if meta.get('feishu_doc_url'):lines.append(f"Full Feishu report：{meta['feishu_doc_url']}")
    lines+=['','## Category distribution','| Category | Count |','|---|---:|']
    lines += [f'| {k} | {v} |' for k,v in stats['categories'].items()]
    lines+=['','## Category details']
    for cat in stats['categories']:
        lines+=['',f'### {cat}']
        for r in rows:
            if r['category']==cat:lines.append(f"- @{literal(r['author_handle'])} / {stamp(r['timestamp_iso'],meta)} / {r['sentiment']}：{literal(r['key_thesis'])} [Original post]({link(r)})")
    lines+=['','## Cross-author comparisons（by ticker）']
    for t,data in sorted(stats['tickers'].items()):
        lines+=['',f'### {literal(t)}']
        for a,s in sorted(data['author_votes'].items()):lines.append(f'- @{literal(a)}：{s}')
        lines.append('Author votes：'+str(dict(Counter(data['author_votes'].values()))))
        lines.append('Evidence：')
        for r in data['posts']:lines.append(f"- @{literal(r['author_handle'])}：{literal(r['key_thesis'])} [Evidence]({link(r)})")
        comparison=meta.get('comparisons',{}).get(t,{})
        evidence={r['tweet_id']:r for r in data['posts']}
        for field,label in (('consensus','Consensus'),('disagreements','Disagreements')):
            for point in comparison.get(field,[]):
                ids=point.get('tweet_ids',[])
                if not ids or not all(ident in evidence for ident in ids):raise ValueError('comparison must cite observed posts for that ticker')
                if field=='consensus' and len({evidence[ident]['author_handle'] for ident in ids})<2:raise ValueError('consensus must cite at least two independent authors')
                lines.append(f"- {label}：{literal(point['text'])} "+' '.join(f'[Evidence]({link(evidence[ident])})' for ident in ids))
        lines.append('the above describes author viewpoints；consensus and disagreement require evidence，votes are not facts。')
    lines+=['','## Off-topic statistics','| Author | Total posts | Category counts | Off-topic | Off-topic rate | Suggestion |','|---|---:|---|---:|---:|---|']
    for a,d in sorted(stats['authors'].items(),key=lambda kv:kv[1]['rate'],reverse=True):
        suggestion='Consider removal（suggestion only）' if d['total']>=3 and d['rate']>=.5 else 'Observe'
        lines.append(f"| {cell(a)} | {d['total']} | {cell(d['categories'])} | {d['off_topic']} | {d['rate']:.0%} | {suggestion} |")
    lines+=['','## Individual post details']
    ordered=[]
    for root in (r for r in rows if not r['is_thread_continuation']):
        ordered.append(root)
        ordered.extend(sorted((r for r in rows if r['thread_root_id']==root['tweet_id']),key=lambda r:r['timestamp_iso']))
    known={r['tweet_id'] for r in rows}
    ordered.extend(r for r in rows if r['is_thread_continuation'] and r['thread_root_id'] not in known)
    for r in ordered:
        heading='#### Thread continuation' if r['is_thread_continuation'] else '### Root post'
        if r['is_thread_continuation'] and r['thread_root_id'] not in known:heading='### Thread continuation（root not observed in this window sample）'
        lines+=['',f"{heading} @{literal(r['author_handle'])} — {r['tweet_id']}",f"Category：{r['category']}/{literal(r['subcategory'])}；Ticker：{cell(r['tickers'])}；Sentiment：{r['sentiment']}；Actionable：{r['is_actionable']}；Confidence：{r['confidence']}",'\n'.join('> '+literal(line) for line in r['text'].splitlines()),f"[Original post]({link(r)})",f"Media：{cell(r.get('media',[]))}；Engagement：{cell(r.get('engagement',{}))}"]
        if r.get('expandable'):lines.append('Text completeness：full expanded text has not been obtained；analysis uses only observed text。')
    lines+=['','## Metadata']+[f'- {literal(k)}：{literal(v)}' for k,v in meta.items() if k != 'comparisons']
    return '\n'.join(lines)+'\n'
if __name__=='__main__':
    import json
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--metadata',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(render(read(a.input),json.loads(Path(a.metadata).read_text())))
