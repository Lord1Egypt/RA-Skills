"""Persist each host browser batch and enforce the recorded collection limits."""
import argparse
import json
from pathlib import Path
from common import iso,write


def freeze_history(directory):
    directory=Path(directory);path=directory/'history-excluded.json'
    if path.exists():return set(json.loads(path.read_text())['tweet_ids'])
    meta=json.loads((directory/'metadata.json').read_text());identifiers=set();sources=[]
    for receipt in sorted(Path(meta['data_dir']).glob('runs/*/*/receipt.json')):
        if receipt.parent.resolve()==directory.resolve():continue
        rows=json.loads((receipt.parent/'enriched.json').read_text())
        identifiers.update(str(row['tweet_id']) for row in rows)
        sources.append(str(receipt.parent))
    write(path,{'tweet_ids':sorted(identifiers),'source_runs':sources})
    return identifiers


def record(directory,snapshot,elapsed,pause):
    directory=Path(directory)
    meta=json.loads((directory/'metadata.json').read_text())
    if elapsed<0 or pause<0:raise ValueError('elapsed and pause must be nonnegative')
    if meta.get('collector_stopped'):raise ValueError('collector already stopped')
    limits=meta['collector_limits']
    log=directory/'collector-events.jsonl'
    events=[json.loads(s) for s in log.read_text().splitlines()] if log.exists() else []
    if events and elapsed<events[-1]['elapsed_seconds']:raise ValueError('elapsed must be monotonic')
    status=snapshot.get('status','ok')
    kind=snapshot.get('kind','list_batch')
    if kind not in ('list_batch','detail'):raise ValueError('invalid snapshot kind')
    if snapshot.get('logged_in') is False:status='login_required'
    if status not in ('ok','captcha','login_required','rate_limited','transient_error','disconnected'):raise ValueError('invalid browser status')
    raw=directory/'raw.jsonl'
    observed={str(r['tweet_id']):r for r in (json.loads(s) for s in raw.read_text().splitlines())} if raw.exists() else {}
    excluded=freeze_history(directory)
    visible=set(meta.get('seen_visible_ids',observed))
    new_visible=[]
    known=set(observed)
    new=[]
    for row in snapshot.get('tweets',[]):
        if not str(row['tweet_id']).isdigit():raise ValueError('invalid tweet ID')
        iso(row['timestamp_iso'])
        ident=str(row['tweet_id'])
        if ident not in visible:new_visible.append(row);visible.add(ident)
        if ident in excluded and ident not in observed:continue
        if str(row['tweet_id']) not in known:
            new.append(row);known.add(str(row['tweet_id']))
        ident=str(row['tweet_id']);previous=observed.get(ident,{})
        merged={**previous,**row}
        if len(previous.get('text',''))>len(row.get('text','')):
            merged['text']=previous['text']
            merged['expandable']=previous.get('expandable',False)
        merged['engagement']={**previous.get('engagement',{}),**{k:v for k,v in row.get('engagement',{}).items() if v is not None}}
        observed[ident]=merged
    # Keep every source batch separately; raw.jsonl is the merged per-ID view.
    write(directory/f"snapshot-{len(events)+1:04d}.json",snapshot)
    raw.write_text(''.join(json.dumps(row,ensure_ascii=False)+'\n' for row in observed.values()))
    meta['steps']+=1
    meta['seen_visible_ids']=sorted(visible)
    meta['historical_skipped']=len(visible & excluded)
    previous_empty=events[-1]['empty_batches'] if events else 0
    empty=((0 if new_visible else previous_empty+1) if kind=='list_batch' else previous_empty) if status=='ok' else 0
    in_window=sum(iso(meta['window_start'])<=iso(r['timestamp_iso'])<=iso(meta['window_end']) for r in (json.loads(s) for s in raw.read_text().splitlines()))
    previous_old=events[-1].get('old_batches',0) if events else 0
    old_batches=previous_old
    times=[iso(r['timestamp_iso']) for r in snapshot.get('tweets',[])]
    chronological=snapshot.get('sorting')=='chronological'
    if kind=='list_batch':
        # Stop wasteful historical traversal even when the UI sort is unknown.
        # This observation is a stopping rule, never proof of complete coverage.
        frontier=meta.get('observed_old_frontier')
        observed_old=(status=='ok' and bool(new_visible) and bool(times)
                      and all(t<iso(meta['window_start']) for t in times)
                      and times==sorted(times,reverse=True))
        if observed_old and frontier and max(iso(r['timestamp_iso']) for r in new_visible)>iso(frontier):observed_old=False
        meta['observed_old_batches']=meta.get('observed_old_batches',0)+1 if observed_old else 0
        meta['observed_old_frontier']=min(times).isoformat() if observed_old else None
        meta['sorting_verified']=meta.get('sorting_verified',True) and chronological
        qualifies=(status=='ok' and meta['sorting_verified'] and bool(new_visible) and bool(times)
                   and all(t<iso(meta['window_start']) for t in times)
                   and times==sorted(times,reverse=True))
        prior_frontier=meta.get('old_frontier')
        new_times=[iso(r['timestamp_iso']) for r in new_visible]
        if qualifies and prior_frontier and max(new_times)>iso(prior_frontier):qualifies=False
        old_batches=previous_old+1 if qualifies else 0
        meta['old_frontier']=min(times).isoformat() if qualifies else None
    stop=None
    if status in ('captcha','login_required'):stop=status
    elif status!='ok':
        previous=sum(e['status']==status for e in events)
        meta['retries']+=1
        if previous:stop=status
    if not stop and elapsed>=limits['timeout_seconds']:stop='timeout'
    if not stop and in_window>=meta['max_tweets']:stop='max_tweets'
    if not stop and meta['steps']>=limits['max_steps']:stop='max_steps'
    if not stop and kind=='list_batch' and empty>=5:
        position=snapshot.get('scroll_position')
        at_bottom=position and position['y']+position['viewport_height']>=position['height']-5
        stop='pagination_stalled' if position and not at_bottom else 'exhausted_observed'
    if not stop and kind=='list_batch' and old_batches>=3:stop='boundary_observed'
    if not stop and kind=='list_batch' and meta.get('observed_old_batches',0)>=3:stop='window_boundary_unverified'
    event={'step':meta['steps'],'kind':kind,'elapsed_seconds':elapsed,'pause_seconds':pause,'status':status,'new_posts':len(new),'empty_batches':empty,'old_batches':old_batches,'sorting':snapshot.get('sorting','unknown'),'stop':stop}
    if 'scroll_position' in snapshot:event['scroll_position']=snapshot['scroll_position']
    event['observed_old_batches']=meta.get('observed_old_batches',0)
    event['historical_skipped']=meta['historical_skipped']
    with log.open('a') as f:f.write(json.dumps(event)+'\n')
    meta['elapsed_seconds']=elapsed
    meta['stop_reason']=stop or 'collecting'
    meta['coverage']='boundary_observed' if stop=='boundary_observed' else 'partial'
    meta['collector_stopped']=bool(stop)
    write(directory/'metadata.json',meta)
    return {'stop':stop,'next_pause_seconds':limits['rate_limit_wait_seconds'] if status=='rate_limited' else limits['pause_seconds'],'new_posts':len(new),'in_window':in_window}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run-dir',required=True);p.add_argument('--snapshot',required=True)
    p.add_argument('--elapsed',type=float,required=True);p.add_argument('--pause',type=float,required=True)
    a=p.parse_args();print(json.dumps(record(a.run_dir,json.loads(Path(a.snapshot).read_text()),a.elapsed,a.pause)))
