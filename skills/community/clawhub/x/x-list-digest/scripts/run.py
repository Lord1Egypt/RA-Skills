"""Host-neutral digest orchestration. Agents supply browser snapshots and LLM analysis."""
import argparse,json,os,re,uuid,sys
from pathlib import Path
from datetime import datetime,timedelta,timezone
from zoneinfo import ZoneInfo
from common import read,write,iso
from config import load,resolve
from collect import normalize
from analyze import enrich
from render import render
from persist import persist
ROOT=Path(__file__).resolve().parents[1]
def initialize(config, selected, data_dir, hours=24, maximum=500, output='both',end=None,rhythm='conservative',expand_threads=True):
    if hours<=0 or maximum<=0:raise ValueError('window and maximum must be positive')
    end=end or datetime.now(timezone.utc);jobs=[]
    for value in selected:
        item=resolve(config,value);ident=item['url'].rsplit('/',1)[-1]
        run_id=end.strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
        directory=Path(data_dir)/'runs'/ident/run_id;directory.mkdir(parents=True,exist_ok=False)
        meta={'list_name':item.get('name',value),'list_url':item['url'],'window_hours':hours,
          'window_start':(end-timedelta(hours=hours)).isoformat(),'window_end':end.isoformat(),
          'timezone':config.get('timezone','Asia/Bangkok'),'max_tweets':maximum,'output':output,
          'coverage':'partial','stop_reason':'not_collected','steps':0,'retries':0,'thread_failures':0,
          'run_id':run_id,'data_dir':str(Path(data_dir).resolve()),'rhythm':rhythm,'expand_threads':expand_threads,
          'collector_limits':{'default':{'scroll_px':400,'pause_seconds':[1.5,3.5],'long_pause_every':10,'long_pause_seconds':[4,8],'max_steps':80,'rate_limit_wait_seconds':60,'timeout_seconds':480},'conservative':{'scroll_px':600,'pause_seconds':[1,2],'long_pause_every':10,'long_pause_seconds':[3,5],'max_steps':300,'rate_limit_wait_seconds':120,'timeout_seconds':2700},'aggressive':{'scroll_px':600,'pause_seconds':[.8,1.8],'long_pause_every':15,'long_pause_seconds':[2,4],'max_steps':120,'rate_limit_wait_seconds':30,'timeout_seconds':360}}[rhythm]}
        write(directory/'metadata.json',meta);jobs.append({'run_dir':str(directory.resolve()),**meta})
    return jobs

def finish(directory):
    directory=Path(directory);meta=json.loads((directory/'metadata.json').read_text())
    if (directory/'receipt.json').exists():return json.loads((directory/'receipt.json').read_text())
    if meta['stop_reason']=='not_collected':raise ValueError('collector must set stop_reason/coverage before finishing')
    if meta['coverage'] not in ('partial','boundary_observed','exhausted_observed'):raise ValueError('invalid coverage')
    rows=normalize(read(directory/'raw.jsonl'),iso(meta['window_end']),meta['window_hours'],meta['max_tweets'])
    log=directory/'collector-events.jsonl'
    events=[json.loads(s) for s in log.read_text().splitlines()] if log.exists() else []
    boundary=bool(events and events[-1].get('stop')=='boundary_observed'
                  and events[-1].get('old_batches',0)>=3 and meta['stop_reason']=='boundary_observed')
    meta['window_coverage']='boundary_observed' if boundary else 'partial'
    meta['unexpanded_posts']=sum(bool(r.get('expandable')) for r in rows)
    meta['coverage']='boundary_observed' if boundary and rows and not meta['unexpanded_posts'] and not meta.get('thread_failures',0) else 'partial'
    meta['collected_in_window']=len(rows)
    meta['budget_overshoot']=max(0,len(rows)-meta['max_tweets'])
    write(directory/'metadata.json',meta)
    rows=enrich(rows,read(directory/'analysis.json'))
    if (directory/'comparisons.json').exists():meta['comparisons']=json.loads((directory/'comparisons.json').read_text())
    write(directory/'raw.json',normalize(read(directory/'raw.jsonl'),iso(meta['window_end']),meta['window_hours'],meta['max_tweets']))
    write(directory/'enriched.json',rows)
    end=iso(meta['window_end']).astimezone(ZoneInfo(meta['timezone']))
    ident=meta['list_url'].rsplit('/',1)[-1]
    report=Path(meta['data_dir'])/'digests'/end.strftime('%Y-%m-%d')/f"{ident}-{meta['window_hours']}h-{meta['run_id']}.md"
    report.parent.mkdir(parents=True,exist_ok=True);report.write_text(render(rows,meta))
    did=persist(str(Path(meta['data_dir'])/'digest.db'),rows,meta,str(directory/'raw.json'),str(directory/'enriched.json'))
    receipt={'digest_id':did,'report_path':str(report.resolve()),'tweet_count':len(rows),'coverage':meta['coverage'],'output':meta['output']}
    write(directory/'receipt.json',receipt);return receipt
def parse_init(argv=None):
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest='action',required=True)
    init=sub.add_parser('init');init.add_argument('--config',default=str(ROOT/'config.yaml'));init.add_argument('--list',action='append',required=True)
    init.add_argument('--window');init.add_argument('--max-tweets',type=int);init.add_argument('--output',choices=['chat','file','both','feishu'])
    init.add_argument('--data-dir',default=os.environ.get('X_LIST_DIGEST_DATA_DIR',str(Path.home()/'.local/share/x-list-digest')));init.add_argument('--end')
    init.add_argument('--rhythm',choices=['default','conservative','aggressive']);init.add_argument('--expand-threads',action=argparse.BooleanOptionalAction,default=None)
    done=sub.add_parser('finish');done.add_argument('--run-dir',required=True);a=p.parse_args(argv)
    config=load(a.config) if a.action=='init' else None
    if config is not None:
        if a.rhythm is None:a.rhythm=config.get('default_rhythm','conservative')
        if a.rhythm not in ('default','conservative','aggressive'):raise ValueError('invalid rhythm')
        if a.expand_threads is None:a.expand_threads=config.get('expand_threads',True)
        if type(a.expand_threads) is not bool:raise ValueError('expand_threads must be boolean')
        if a.window is None:a.window=str(config.get('default_window_hours',24))+'h'
        if a.max_tweets is None:a.max_tweets=config.get('default_max_tweets',500)
        if a.output is None:a.output=config.get('default_output','both')
        if not re.fullmatch(r'[1-9][0-9]*h',a.window):raise ValueError('window format: 24h / 168h')
        if type(a.max_tweets) is not int or a.max_tweets<=0:raise ValueError('max tweets must be a positive integer')
        if a.output not in ('chat','file','both','feishu'):raise ValueError('invalid default output')
    return a,config

if __name__=='__main__':
    try:
        a,config=parse_init()
        if a.action=='init':
            result=initialize(config,a.list,a.data_dir,int(a.window[:-1]),a.max_tweets,a.output,iso(a.end) if a.end else None,a.rhythm,a.expand_threads)
        else:result=finish(a.run_dir)
        print(json.dumps(result,ensure_ascii=False,indent=2))
    except (ValueError,FileNotFoundError,KeyError) as e:
        print(str(e),file=sys.stderr)
        sys.exit(2)
