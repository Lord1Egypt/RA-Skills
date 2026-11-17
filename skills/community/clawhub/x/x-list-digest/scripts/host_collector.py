"""Fixed collection loop; browser access is supplied by the native host tool.

Hermes browser_exec: collect(run_dir, js, scroll, goto_url).
No browser library, credentials, subprocess browser, or connection is created here.
"""
import json
import random
import time
from pathlib import Path
from collector_record import record,freeze_history
from common import iso,write
from browser_tabs import OwnedTabs


def authorize_resume(directory,maximum=500,max_steps=300,timeout_seconds=2700):
    """Resume a budget stop, preserving its window, observations and used budget."""
    directory=Path(directory);meta=json.loads((directory/'metadata.json').read_text())
    if (directory/'receipt.json').exists():raise ValueError('Finished runs cannot resume')
    if not meta.get('collector_stopped') or meta['stop_reason'] not in ('max_steps','max_tweets','timeout','invocation_budget'):
        raise ValueError('Only budget-stopped runs can resume')
    raw=directory/'raw.jsonl'
    rows=[json.loads(s) for s in raw.read_text().splitlines()] if raw.exists() else []
    in_window=sum(iso(meta['window_start'])<=iso(r['timestamp_iso'])<=iso(meta['window_end']) for r in rows)
    if maximum<=in_window or max_steps<=meta['steps'] or timeout_seconds<=meta.get('elapsed_seconds',0):
        raise ValueError('New limits must leave remaining budget')
    sequence=meta.get('resume_count',0)+1
    write(directory/f'resume-{sequence:04d}.json',{'before':meta,'limits':{'max_tweets':maximum,'max_steps':max_steps,'timeout_seconds':timeout_seconds}})
    meta['max_tweets']=maximum;meta['collector_limits']['max_steps']=max_steps
    meta['collector_limits']['timeout_seconds']=timeout_seconds
    meta['collector_stopped']=False;meta['stop_reason']='collecting';meta['resume_count']=sequence
    write(directory/'metadata.json',meta)
    return meta


def run_native(directory,resume=False):
    """Run only inside Hermes browser_exec using its installed native helpers."""
    from browser_harness import helpers
    directory=Path(directory)
    meta=json.loads((directory/'metadata.json').read_text())
    owner=OwnedTabs(directory,helpers)
    if resume:
        tab=helpers.current_tab()
        if (tab.get('url') or '').split('?')[0]!=meta['list_url']:
            raise ValueError('Resume requires the same session attached to its list tab')
        list_tab=tab['targetId']
        if owner.state['tabs'].get(list_tab,{}).get('role')!='list':
            raise ValueError('Resume requires the recorded run-owned list tab')
        authorize_resume(directory)
    else:
        if owner.path.exists() or meta.get('collector_stopped') or meta.get('steps'):
            raise ValueError('Use a fresh run or resume the recorded paused run')
        owner.sweep()
        list_tab=None
    detail_tab=None
    def navigate(url):
        nonlocal detail_tab
        if url:
            if detail_tab is None:
                detail_tab=owner.create('detail',url)
                helpers.switch_tab(detail_tab,activate=True)
            else:
                helpers.switch_tab(detail_tab,activate=True);owner.destination(detail_tab,url)
            helpers.wait_for_load()
        else:
            helpers.switch_tab(list_tab,activate=True)
    owner.state['state']='active';owner.save()
    result=None
    try:
        if list_tab is None:
            list_tab=owner.create('list',meta['list_url']);helpers.wait_for_load()
        helpers.switch_tab(list_tab,activate=True)
        result=collect(directory,helpers.js,helpers.scroll,navigate,resume=resume)
        return result
    except Exception as error:
        current=json.loads((directory/'metadata.json').read_text())
        current['collector_stopped']=True;current['stop_reason']='browser_exception';current['coverage']='partial'
        write(directory/'metadata.json',current)
        write(directory/'browser-error.json',{'error_type':type(error).__name__,'steps':current['steps']})
        raise
    finally:
        paused=result is not None and result.get('stop') in ('invocation_budget','max_steps','max_tweets','timeout')
        try:
            owner.finish('paused' if paused else 'finished' if result is not None else 'failed',keep=list_tab if paused else None)
        except OSError as cleanup_error:
            print(json.dumps({'browser_cleanup_warning':type(cleanup_error).__name__}),flush=True)


def collect(directory,js,scroll,navigate,*,resume=False,clock=time.monotonic,sleep=time.sleep,choose=random.uniform):
    directory=Path(directory)
    meta=json.loads((directory/'metadata.json').read_text())
    if meta.get('collector_stopped') or (not resume and (meta['steps'] or (directory/'collector-events.jsonl').exists())):
        raise ValueError('Use a fresh run; stopped or previously collected runs cannot restart')
    if resume and not meta.get('resume_count'):raise ValueError('Resume must be authorized first')
    excluded=freeze_history(directory)
    invocation_started=clock()
    limits=meta['collector_limits'];started=invocation_started-(meta.get('elapsed_seconds',0) if resume else 0);pause=0.0;visited=set()
    if resume:
        for path in directory.glob('snapshot-*.json'):
            previous=json.loads(path.read_text())
            if previous.get('kind')=='detail' and previous.get('status')=='ok':
                visited.update(r['tweet_id'] for r in previous.get('tweets',[]) if not r.get('expandable'))
    expression='('+ (Path(__file__).with_name('collect.js')).read_text().strip() +')()'
    def terminal(result,in_detail=False):
        if result['stop'] or clock()-invocation_started>=1500:
            if in_detail:
                navigate(None)
                current=json.loads((directory/'metadata.json').read_text())
                current['elapsed_seconds']=clock()-started
                write(directory/'metadata.json',current)
            if not result['stop']:
                current=json.loads((directory/'metadata.json').read_text())
                current['collector_stopped']=True;current['stop_reason']='invocation_budget'
                current['elapsed_seconds']=clock()-started
                write(directory/'metadata.json',current)
                write(directory/f'invocation-pause-{current["steps"]:04d}.json',{'elapsed_seconds':current['elapsed_seconds'],'steps':current['steps'],'reason':'native tool segment; resume same session with remaining total budget'})
                result={**result,'stop':'invocation_budget'}
            return result
        return None
    while True:
        snapshot=js(expression)
        if not isinstance(snapshot,dict):raise ValueError('Native browser did not return a snapshot')
        snapshot['kind']='list_batch'
        # Sorting is evidence from the page, never inferred from one batch.
        snapshot.setdefault('sorting','unknown')
        result=record(directory,snapshot,clock()-started,pause)
        print(json.dumps({'step':json.loads((directory/'metadata.json').read_text())['steps'],**result}),flush=True)
        stopped=terminal(result)
        if stopped:return stopped
        # Expand observed roots while they remain reachable. A detail counts toward
        # the same budget; its content is merged by the authoritative recorder.
        for row in snapshot.get('tweets',[]):
            if str(row['tweet_id']) in excluded or not row.get('expandable') or row['tweet_id'] in visited:continue
            if not iso(meta['window_start'])<=iso(row['timestamp_iso'])<=iso(meta['window_end']):continue
            navigate(row['url'])
            visited.add(row['tweet_id'])
            slept=_wait(1,sleep,clock,started,limits['timeout_seconds'])
            detail=js(expression)
            detail['kind']='detail';detail['sorting']='unknown'
            # Only an exact ID/timestamp match can update this root.
            detail['tweets']=[r for r in detail.get('tweets',[]) if str(r['tweet_id'])==str(row['tweet_id']) and iso(r['timestamp_iso'])==iso(row['timestamp_iso'])]
            if not detail['tweets']:
                current=json.loads((directory/'metadata.json').read_text());current['thread_failures']+=1;write(directory/'metadata.json',current)
            result=record(directory,detail,clock()-started,slept)
            stopped=terminal(result,in_detail=True)
            if stopped:return stopped
            if detail.get('status')!='ok':
                wait=result['next_pause_seconds']
                slept=_wait(wait if isinstance(wait,(int,float)) else choose(*wait),sleep,clock,started,limits['timeout_seconds'])
                detail=js(expression);detail['kind']='detail';detail['sorting']='unknown'
                detail['tweets']=[r for r in detail.get('tweets',[]) if str(r['tweet_id'])==str(row['tweet_id']) and iso(r['timestamp_iso'])==iso(row['timestamp_iso'])]
                result=record(directory,detail,clock()-started,slept)
                stopped=terminal(result,in_detail=True)
                if stopped:return stopped
                if detail.get('status')!='ok':
                    raise ValueError('Unexpected nonterminal detail retry; stop for inspection')
            # Reattach to the untouched list tab; no history navigation or reload.
            navigate(None)
        current=json.loads((directory/'metadata.json').read_text())
        previously_unverified=set(current.get('unverified_thread_ids',[]))
        pending_threads={str(r['tweet_id']) for r in snapshot.get('tweets',[]) if str(r['tweet_id']) not in excluded
                         and iso(meta['window_start'])<=iso(r['timestamp_iso'])<=iso(meta['window_end'])
                         and (r.get('engagement',{}).get('replies') or 0)>0}-previously_unverified
        if meta.get('expand_threads') and pending_threads:
            # This fixed loop does not prove same-author reply relationships.
            # Preserve that missing verification instead of silently claiming full threads.
            current['thread_failures']+=len(pending_threads)
            current['unverified_thread_ids']=sorted(previously_unverified|pending_threads)
            write(directory/'metadata.json',current)
        if clock()-started>=limits['timeout_seconds']:
            return record(directory,{'status':'ok','kind':'detail','tweets':[]},clock()-started,0)
        if snapshot['status']=='ok':
            point=snapshot['viewport']
            distance=max(limits['scroll_px'],int(point.get('height',0)*.85))
            scroll(point['x'],point['y'],dy=distance)
        wait=result['next_pause_seconds']
        if isinstance(wait,list):
            interval=limits['long_pause_seconds'] if current['steps']%limits['long_pause_every']==0 else wait
            wait=choose(*interval)
        pause=_wait(wait,sleep,clock,started,limits['timeout_seconds'])


def _wait(seconds,sleep,clock,started,timeout):
    before=clock()
    remaining=min(seconds,max(0,timeout-(before-started)))
    while remaining>0:
        part=min(remaining,60);sleep(part);remaining-=part
    return clock()-before
