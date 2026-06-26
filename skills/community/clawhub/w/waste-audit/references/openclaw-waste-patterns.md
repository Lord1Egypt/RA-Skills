# OpenClaw Waste Audit — Reference Bank

## Observed Waste Patterns

### Pattern 1: Health Probe Loop (D8 CLEAN_LOOP)
- Job: Health monitoring job — high run count, 0% errors, 0% delivered
- Model: actual model from `payload.model` in jobs.json (not EXEC_SCRIPT tag)
- Frequency: hourly or more frequent
- Signature: `delivered=false` + `status=ok` + repetitive "all clear" summaries — structurally silent, zero external value
- Signal: EXEC_SCRIPT tag ≠ bash. Always check `payload.model` in jobs.json.
- Verdict: No delivery means output is discarded. Zero value despite 100% success rate.

### Pattern 2: Zero-Value Log Verification
- Job: Log analyzer job — runs but log format doesn't match parser
- Latest summary: "ERROR: 0 | WARN: 0" — job runs successfully but produces nothing useful
- Frequency: every 6h or more frequent — excessive for zero-value output
- Signal: Both wrong frequency AND wrong logic. Double waste.
- Critical signal: `delivered=false` + zero content = structural failure, not just over-scheduling.

### Pattern 3: High-Frequency Midnight Burner
- Job: Embedding/job scheduled 4x/day at midnight hours
- Signal: Midnight runs unlikely to need human attention anyway
- Verdict: 4x/day is excessive. 1x or 2x sufficient.

### Pattern 4: tmp-auto-cleanup (Hybrid Failure + Silent)
- Job: cleanup job with intermittent output
- Frequency: every 4h or more
- Signal: Mix of `status=error` and `status=ok` with `(no output)` — unreliable execution
- Delivered: false
- Problem: 50% error rate + 50% silent success = no reliable output ever delivered

### Pattern 5: Disk/Memory Monitor (UNCLEAR + No Delivery)
- Jobs: monitor-type jobs (disk, memory, etc.)
- Frequency: every 6h or daily
- Problem: Classified UNCLEAR, delivered=false, no visible value
- Rule of thumb: Any monitor job with delivered=false and no external target is waste by definition

## Diagnostic Command Cheatsheet

```bash
# Run ClawSetup diagnostic (primary in this env — always available)
python3 ~/.hermes/scripts/clawsetup_diagnostic.py

# Get top 10 by token burn
python3 ~/.hermes/scripts/clawsetup_diagnostic.py 2>&1 | grep -A12 "TOP 10"

# List all jobs with model info from jobs.json
cat ~/.openclaw/cron/jobs.json | python3 -c "
import json,sys
d=json.load(sys.stdin)
for j in d.get('jobs',[]):
    model=j.get('payload',{}).get('model','null')
    if model and model not in ('null','None',''):
        print(f'{j[\"name\"]}: {model}')
"

# Check actual token burn from JSONL runs (use usage.total_tokens, NOT top-level totalTokens)
python3 -c "
import json, glob, os
runs_dir = os.environ.get('OPENCLAW_HOME', os.path.expanduser('~/.openclaw'))
runs_dir = os.path.join(runs_dir, 'cron', 'runs')
for f in glob.glob(f'{runs_dir}/*.jsonl'):
    total = 0
    count = 0
    with open(f) as fh:
        for line in fh:
            try:
                d = json.loads(line)
                total += d.get('usage',{}).get('total_tokens',0)
                count += 1
            except: pass
    if total > 0:
        print(f'{f.split(\"/\")[-1]}: {count} runs, {total:,} tokens')
"

# Inspect specific job runs
openclaw-env cron runs --id <job_id> --limit 3

# Show last N run summaries for a job (to detect CLEAN_LOOP pattern)
python3 -c "
import json
fpath = os.path.join(os.environ.get('OPENCLAW_HOME', os.path.expanduser('~/.openclaw')), 'cron', 'runs', '<job_id>.jsonl')
with open(fpath) as f:
    lines = f.readlines()
for line in lines[-3:]:
    d = json.loads(line)
    print(f'status={d[\"status\"]} | delivered={d[\"delivered\"]} | summary={d.get(\"summary\",\"\")[:150]}')
"
```

## Actual Audit Results (2026-05-20)

Real data from live cron jobs — 22 jobs tracked, $21.75 total monthly cost.

### Top 3 Waste Findings

**1. Health Check - 60min** (D8 + D9)
- Schedule: `0 */6 * * *` | Model: MiniMax-M2.7
- Runs: 1,802 | Tokens: 33,526,887 (40.6% of total)
- Errors: 6% | Delivered: 0% | Summary median: **19 chars**
- Verdict: CLEAN_LOOP — LLM model burning 33M tokens per month outputting only 19-char summaries. No delivery. Fix: reduce to daily or disable.
- Real signal: `delivered=false` + LLM model + summary_median=19 = definitive waste.

**2. daily-backup** (D8 suspected)
- Schedule: `0 4 * * *` | EXEC_SCRIPT
- Runs: 56 | Tokens: 1,176,008
- Errors: 0% | Delivered: 0% | Summary median: **25 chars**
- Verdict: Silent job consuming 1.18M tokens, outputting 25-char summaries, no delivery. Likely obsolete. Check before disabling.

**3. Agent控制权_每日特别提醒** (D8 suspected)
- Schedule: `0 20 * * *` | EXEC_SCRIPT
- Runs: 66 | Tokens: 1,783,630
- Errors: 9% | Delivered: 42% | Summary median: **8 chars**
- Verdict: Outputs "NO_REPLY" most runs, 8-char median. Burn rate high for 42% delivery. Review frequency or need.

### jobs.json Structure (for reference)
```
{"version": 1, "jobs": [...]}  ← top-level has 'version' and 'jobs' key
jobs[j]['payload']['model']     ← ground truth for LLM presence
jobs[j]['schedule']['kind']     ← 'cron' | 'at' | 'every'
jobs[j]['schedule']['expr']     ← cron expression string
jobs[j]['schedule']['everyMs']  ← interval in ms
jobs[j]['delivery']['mode']     ← 'announce' | 'none' | ...
```

### Quick Audit Command
```bash
python3 -c "
import json, glob, os
with open(os.path.expanduser('~/.openclaw/cron/jobs.json')) as f:
    job_map = {j['id']: j for j in json.load(f)['jobs']}
runs_dir = os.path.join(os.environ.get('OPENCLAW_HOME', os.path.expanduser('~/.openclaw')), 'cron', 'runs')
results = []
for f in sorted(glob.glob(f'{runs_dir}/*.jsonl')):
    jid = os.path.basename(f).replace('.jsonl','')
    total=count=errors=delivered=0; summary_lens=[]
    with open(f) as fh:
        for line in fh:
            try:
                d=json.loads(line)
                total+=d.get('usage',{}).get('total_tokens',0);count+=1
                errors+=1 if d.get('error') else 0
                delivered+=1 if d.get('delivered') else 0
                summary_lens.append(len(str(d.get('summary','') or '')))
            except: pass
    if count>0 and jid in job_map:
        j=job_map[jid]; med=sorted(summary_lens)[len(summary_lens)//2]
        results.append({'name':j['name'],'schedule':j.get('schedule',{}).get('expr',''),
            'model':j.get('payload',{}).get('model',''),'count':count,'tokens':total,
            'errors':errors,'delivered':delivered,'summary_median':med})
results.sort(key=lambda x: x['tokens'], reverse=True)
for r in results: print(f\"{r['name']} | runs={r['count']} tokens={r['tokens']:,} err={r['errors']/r['count']*100:.0f}% med={r['summary_median']}\")
"
```

## Key Lessons

1. **EXEC_SCRIPT tag is unreliable.** Use `payload.model` from jobs.json as ground truth — a job's name suggests "simple script" but it may still call LLM internally.
2. **delivery=false + status=ok = structural waste.** The job runs successfully but produces no external value. This is the primary waste signature.
3. **delivery.mode "none" = by design, not waste.** Check actual deliveryStatus for external channels — internal jobs that announce to own session are not waste.
4. **Schedule parsing matters.** Raw cron string can be misleading — parse `schedule.kind` + `schedule.expr` / `schedule.everyMs`.
5. **Token counting:** JSONL top-level `totalTokens` is always 0. Real data is at `usage.total_tokens`.
6. **Error rate vs delivery rate:** High error rate = failure loop. Low delivery rate = wrong target or broken logic. Both together = D8 CLEAN_LOOP.
7. **CLEAN_LOOP diagnosis:** Look for `delivered=false` + `status=ok` + repetitive "all good" summaries across 50+ runs. This is the definitive signature — not just high run count.
8. **jobs.json is not a plain list.** It has `{"version": 1, "jobs": [...]}`. Access `.jobs` before iterating.
9. **D10: Script-wrapper agentTurn detection.** When `payload.kind == "agentTurn"` + `payload.model` set + message is just a script path/exec command (no real LLM judgment needed) + summary median ≤50 chars → convert to EXEC_SCRIPT. Health Check and Log Analyzer are canonical examples — they run scripts but use LLM only to format output, wasting ~16K tokens/run.