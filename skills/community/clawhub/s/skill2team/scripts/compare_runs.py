#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
DEFAULT_WEIGHTS={'correctness':5,'completeness':3,'evidence_quality':5,'risk_control':5,'decision_usefulness':4,'clarity':3,'traceability':4,'maintainability':3,'reusability':2,'workflow_alignment':4,'platform_fit':3,'latency':2,'cost':2,'user_satisfaction':3}
HINTS={'correctness':'strengthen verifier/domain analyst','evidence_quality':'improve evidence verifier and source policy','risk_control':'tighten reviewer gate','workflow_alignment':'rebuild original workflow migration map','platform_fit':'regenerate target runtime adapter','latency':'add fast path or merge agents','clarity':'improve composer or preserve baseline style','cost':'reduce unnecessary agents/gates'}
def scores(x):
    if not isinstance(x,dict): return {}
    if isinstance(x.get('scores'),dict): return x['scores']
    if isinstance(x.get('metrics'),dict): raw=x['metrics']
    else: raw=x
    aliases={'accuracy':'correctness','output_quality':'clarity','speed':'latency'}
    out={}
    for k,v in raw.items():
        if isinstance(v,(int,float)): out[aliases.get(k,k)]=v
    return out
def weighted(s,w):
    total=wt=0
    for k,v in w.items():
        if k in s: total += float(s[k])*v; wt += v
    return round(total/wt,3) if wt else 0
def analyze(d):
    w={**DEFAULT_WEIGHTS, **d.get('weights',{})}; rows=[]; wins={'team':0,'baseline':0,'tie':0}; fixes=[]
    tasks=d.get('tasks')
    if not tasks and isinstance(d.get('baseline'),dict) and isinstance(d.get('team'),dict):
        tasks=[{'task_id':d.get('task_id','overall'),'baseline':d.get('baseline'),'team':d.get('team'),'known_issues':d.get('known_issues',[])}]
    for t in tasks or []:
        b=scores(t.get('baseline') or t.get('original')); tm=scores(t.get('team'))
        bs=weighted(b,w); ts=weighted(tm,w)
        win='team' if ts>bs+0.05 else 'baseline' if bs>ts+0.05 else 'tie'; wins[win]+=1
        reg=[]
        for m in w:
            if m in b and m in tm and tm[m]<b[m]: reg.append(m); fixes.append(HINTS.get(m,'inspect manually'))
        rows.append({'task_id':t.get('task_id','unknown'),'baseline_score':bs,'team_score':ts,'winner':win,'regressed_metrics':reg,'known_issues':t.get('known_issues',[])})
    decision='candidate_team_ready_for_guarded_rollout' if wins['baseline']==0 and wins['team']>=wins['tie'] else 'revise_team_then_limited_rollout' if wins['team']>wins['baseline'] else 'keep_baseline_or_revise_team_and_retest' if wins['baseline']>wins['team'] else 'hybrid_or_more_testing_needed'
    return {'summary':{**wins,'decision':decision},'task_rows':rows,'recommended_next_steps':sorted(set(fixes)) if fixes else ['continue monitoring']}
def md(r):
    out=['# Package Release Quality Comparison Report','','## Execution-path log','- **selected_route**: source-to-team','- **delivery**: package','- **execution_path**: direct-skill','- **meta_team_first_done**: false','- **current_run_fanout_status**: direct-skill-not-requested','- **target_subagent_fanout_supported**: runtime-dependent','- **execution_mode**: direct_skill','- **fallback_declaration**: not_applicable_direct_skill','','## Summary']
    s=r['summary']; out += [f"- Team wins: {s['team']}",f"- Baseline wins: {s['baseline']}",f"- Ties: {s['tie']}",f"- Decision: `{s['decision']}`",'', '| Task | Baseline | Team | Winner | Regressions | Issues |','|---|---:|---:|---|---|---|']
    for row in r['task_rows']: out.append(f"| {row['task_id']} | {row['baseline_score']} | {row['team_score']} | {row['winner']} | {', '.join(row['regressed_metrics'])} | {'; '.join(row['known_issues'])} |")
    out += ['','## Recommended next steps']+[f'- {x}' for x in r['recommended_next_steps']]
    return '\n'.join(out)+'\n'
def main():
    if len(sys.argv)!=2:
        print('Usage: compare_runs.py comparison.json', file=sys.stderr); return 2
    print(md(analyze(json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))))); return 0
if __name__=='__main__': raise SystemExit(main())
