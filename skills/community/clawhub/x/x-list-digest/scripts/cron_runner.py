"""Generate upcoming agent jobs; does not falsely install a scheduler."""
import argparse,json
from datetime import datetime
from zoneinfo import ZoneInfo
import yaml
from croniter import croniter
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--config',required=True);a=p.parse_args()
    config=yaml.safe_load(open(a.config));jobs=[]
    for j in config.get('cron_jobs',[]):
        if not j.get('enabled'):continue
        if not j.get('list_url','').startswith('https://x.com/i/lists/'):raise ValueError('configured list URL required')
        now=datetime.now(ZoneInfo(j.get('timezone','Asia/Bangkok')))
        jobs.append({**j,'next_run':croniter(j['schedule'],now).get_next(datetime).isoformat(),
          'prompt':f"Use x-list-digest for list {j['list_name']}, URL {j['list_url']}, window {j.get('window_hours',24)}h, output {j.get('output','both')}. Report partial coverage and stop on login/CAPTCHA."})
    print(json.dumps(jobs,ensure_ascii=False,indent=2))
