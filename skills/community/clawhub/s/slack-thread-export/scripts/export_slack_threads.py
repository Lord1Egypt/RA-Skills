#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
import time
from pathlib import Path
from typing import Iterable

JS_TEMPLATE = r'''
async () => {
  const channel = '__CHANNEL__';
  const page = __PAGE__;
  const teamId = '__TEAM_ID__';
  const userId = '__USER_ID__';
  const after = '__AFTER__';
  const before = '__BEFORE__';
  const cfg = JSON.parse(localStorage.getItem('localConfig_v2'));
  const token = cfg.teams[teamId].token;
  const parts = [`from:<@${userId}>`, 'is:thread', `in:#${channel}`];
  if (after) parts.push(`after:${after}`);
  if (before) parts.push(`before:${before}`);
  const query = parts.join(' ');
  const params = new URLSearchParams({token, query, count:'100', page:String(page)});
  const res = await fetch('/api/search.messages', {
    method:'POST',
    credentials:'include',
    headers:{'content-type':'application/x-www-form-urlencoded; charset=UTF-8'},
    body:params.toString()
  });
  const json = await res.json();
  if (!json.ok) return {ok:false, error:json.error, channel, page, query};
  const matches = json.messages?.matches || [];
  const rows = [];
  for (const item of matches) {
    const permalink = item.permalink || '';
    if (!permalink.includes('thread_ts=')) continue;
    const ch = item.channel || {};
    if (ch.is_im || ch.is_mpim) continue;
    const text = (item.text || '').replace(/\s+/g, ' ').trim();
    rows.push({
      datetime_utc: item.ts ? new Date(parseFloat(item.ts)*1000).toISOString() : '',
      channel_name: ch.name || channel,
      channel_id: ch.id || '',
      thread_ts: (() => { try { return new URL(permalink).searchParams.get('thread_ts') || ''; } catch(e) { return ''; } })(),
      username: item.username || '',
      text: text || '[non-text/attachment-only]',
      permalink,
      source_query_channel: channel,
      query,
    });
  }
  return {ok:true, channel, page, count: matches.length, rows};
}
'''

DEFAULT_WORK_KEYWORDS = [
    'api','deploy','deployment','release','server','infra','security','domain','dns','notion','slack','workflow','bot',
    'ec2','vercel','supabase','oauth','token','key','billing','invoice','cost','payment','saas','ai','model','openai','chatgpt',
    '개발','배포','보안','서버','도메인','세팅','비용','결제','인프라','워크플로우','데이터','서비스'
]
DEFAULT_CHANNEL_HINTS = [
    'tech','ax','dev','moonlight','product','ops','backoffice','agentic','engineering','partnership','onboarding','rocket','openai','cms','corca','daily'
]

FIELDS = ['datetime_utc','channel_name','channel_id','thread_ts','username','text','permalink','source_query_channel','query']


def read_lines(path: str | None) -> list[str]:
    if not path:
        return []
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    out = []
    for line in p.read_text(encoding='utf-8').splitlines():
        s = line.strip()
        if not s or s.startswith('#'):
            continue
        out.append(s)
    return out


def run_eval(target_id: str, channel: str, page: int, user_id: str, team_id: str, after: str | None, before: str | None) -> dict:
    fn = (JS_TEMPLATE
          .replace('__CHANNEL__', channel)
          .replace('__PAGE__', str(page))
          .replace('__TEAM_ID__', team_id)
          .replace('__USER_ID__', user_id)
          .replace('__AFTER__', after or '')
          .replace('__BEFORE__', before or ''))
    cmd = [
        'openclaw', 'browser', '--browser-profile', 'chrome', '--timeout', '120000',
        'evaluate', '--target-id', target_id, '--fn', fn, '--json'
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or r.stdout.strip())
    outer = json.loads(r.stdout)
    return outer.get('result', {})


def work_like(row: dict, channel_hints: list[str], keywords: list[str]) -> bool:
    cname = (row.get('channel_name') or '').lower()
    text = (row.get('text') or '').lower()
    if any(h.lower() in cname for h in channel_hints):
        return True
    return any(k.lower() in text for k in keywords)


def load_resume_rows(path: str | None) -> list[dict]:
    if not path:
        return []
    p = Path(path)
    if not p.exists():
        return []
    rows = []
    for line in p.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    with path.open('a', encoding='utf-8') as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')


def dedupe_rows(rows: list[dict]) -> list[dict]:
    uniq = []
    seen = set()
    for row in rows:
        key = row.get('permalink')
        if not key or key in seen:
            continue
        seen.add(key)
        uniq.append(row)
    return uniq


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for row in sorted(rows, key=lambda x: (x.get('datetime_utc',''), x.get('channel_name',''), x.get('thread_ts',''))):
            w.writerow({k: row.get(k, '') for k in FIELDS})


def estimate_preflight(channels_info: dict[str, dict], max_pages: int, sleep_seconds: float) -> dict:
    estimated_requests = 0
    estimated_upper_rows = 0
    risk = 'low'
    large_channels = []
    for ch, info in channels_info.items():
        if not info.get('ok'):
            continue
        page1 = info.get('page1_match_count', 0)
        if page1 >= 100:
            estimated_pages = max_pages
        elif page1 == 0:
            estimated_pages = 0
        else:
            estimated_pages = 1
        estimated_requests += estimated_pages
        estimated_upper_rows += page1 * max(1, estimated_pages)
        if page1 >= 80:
            large_channels.append(ch)

    if estimated_requests >= 40 or len(large_channels) >= 3:
        risk = 'high'
    elif estimated_requests >= 15 or len(large_channels) >= 1:
        risk = 'medium'

    if risk == 'low':
        recommendation = 'Run as-is.'
    elif risk == 'medium':
        recommendation = 'Prefer a shorter date range or smaller channel batch before full export.'
    else:
        recommendation = 'Split the export into smaller channel groups and/or add a tighter date range before running.'

    est_duration = round(estimated_requests * max(sleep_seconds, 0.1), 2)
    return {
        'estimated_requests_lower_bound': estimated_requests,
        'estimated_upper_bound_rows': estimated_upper_rows,
        'estimated_sleep_only_seconds': est_duration,
        'risk': risk,
        'large_channels': large_channels,
        'recommendation': recommendation,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description='Export Slack thread messages from an attached Chrome Slack tab')
    ap.add_argument('--target-id', required=True)
    ap.add_argument('--user-id', required=True)
    ap.add_argument('--team-id', required=True)
    ap.add_argument('--channels', nargs='*', default=[])
    ap.add_argument('--channel-file', help='Text file with one channel name per line')
    ap.add_argument('--after')
    ap.add_argument('--before')
    ap.add_argument('--max-pages', type=int, default=60, help='Maximum pages per channel; keep this modest to reduce timeout/rate-limit risk')
    ap.add_argument('--sleep-seconds', type=float, default=0.5, help='Delay between normal page requests; on ratelimit the script sleeps 4x or at least 3s')
    ap.add_argument('--out-csv', required=True)
    ap.add_argument('--out-jsonl', required=True)
    ap.add_argument('--summary-json', help='Optional summary JSON output path')
    ap.add_argument('--failed-channels-out', help='Write failed channel names here for targeted retry')
    ap.add_argument('--resume-from-jsonl', help='Resume from a previous raw JSONL file; existing rows are loaded before new collection')
    ap.add_argument('--mode', choices=['strict','raw','heuristic'], default='heuristic', help='strict=channel/date only, raw=no work filter, heuristic=channel hints + keyword filter')
    ap.add_argument('--keyword', action='append', default=[], help='Additional work-related keyword; repeatable')
    ap.add_argument('--channel-hint', action='append', default=[], help='Additional work-related channel hint; repeatable')
    ap.add_argument('--preflight', action='store_true', help='Sample only first-page volumes per channel and print counts without exporting full history')
    args = ap.parse_args()

    channels = []
    channels.extend(args.channels)
    channels.extend(read_lines(args.channel_file))
    seen_channels = set()
    channels = [c for c in channels if not (c in seen_channels or seen_channels.add(c))]
    if not channels:
        raise SystemExit('No channels provided. Use --channels or --channel-file.')

    out_csv = Path(args.out_csv)
    out_jsonl = Path(args.out_jsonl)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    out_jsonl.parent.mkdir(parents=True, exist_ok=True)

    channel_hints = DEFAULT_CHANNEL_HINTS + args.channel_hint
    keywords = DEFAULT_WORK_KEYWORDS + args.keyword

    resumed_rows = load_resume_rows(args.resume_from_jsonl)
    all_rows = list(resumed_rows)
    stats: dict[str, int] = {}
    failed: list[str] = []
    completed: list[str] = []
    ratelimit_retries = 0
    total_requests = 0
    start_ts = time.time()

    if args.preflight:
        summary = {'mode': 'preflight', 'channels': {}, 'after': args.after, 'before': args.before, 'max_pages': args.max_pages, 'sleep_seconds': args.sleep_seconds}
        for ch in channels:
            total_requests += 1
            data = run_eval(args.target_id, ch, 1, args.user_id, args.team_id, args.after, args.before)
            if not data.get('ok'):
                summary['channels'][ch] = {'ok': False, 'error': data.get('error')}
                continue
            summary['channels'][ch] = {'ok': True, 'page1_match_count': data.get('count', 0), 'page1_thread_rows': len(data.get('rows', []))}
        summary['estimate'] = estimate_preflight(summary['channels'], args.max_pages, args.sleep_seconds)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0

    if args.resume_from_jsonl:
        out_jsonl.write_text(Path(args.resume_from_jsonl).read_text(encoding='utf-8'), encoding='utf-8')
    else:
        out_jsonl.write_text('', encoding='utf-8')

    resumed_channels = {r.get('source_query_channel') for r in resumed_rows if r.get('source_query_channel')}

    for ch in channels:
        if ch in resumed_channels:
            stats[ch] = sum(1 for r in resumed_rows if r.get('source_query_channel') == ch)
            completed.append(ch)
            continue
        chan_rows = 0
        channel_failed = False
        for page in range(1, args.max_pages + 1):
            total_requests += 1
            data = run_eval(args.target_id, ch, page, args.user_id, args.team_id, args.after, args.before)
            if not data.get('ok'):
                err = data.get('error')
                if err == 'ratelimited':
                    ratelimit_retries += 1
                    time.sleep(max(3.0, args.sleep_seconds * 4))
                    total_requests += 1
                    data = run_eval(args.target_id, ch, page, args.user_id, args.team_id, args.after, args.before)
                    if not data.get('ok'):
                        channel_failed = True
                        failed.append(ch)
                        break
                else:
                    channel_failed = True
                    failed.append(ch)
                    break
            matches = data.get('count', 0)
            if matches == 0:
                break
            rows = data.get('rows', [])
            chan_rows += len(rows)
            write_jsonl(out_jsonl, rows)
            all_rows.extend(rows)
            if matches < 100:
                break
            time.sleep(args.sleep_seconds)
        stats[ch] = chan_rows
        if not channel_failed:
            completed.append(ch)

    uniq = dedupe_rows(all_rows)
    if args.mode == 'raw':
        keep = uniq
    elif args.mode == 'strict':
        keep = uniq
    else:
        keep = [r for r in uniq if work_like(r, channel_hints, keywords)]

    write_csv(out_csv, keep)

    if args.failed_channels_out:
        p = Path(args.failed_channels_out)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text('\n'.join(failed) + ('\n' if failed else ''), encoding='utf-8')

    summary = {
        'channels': stats,
        'completed_channels': completed,
        'failed_channels': failed,
        'total_raw': len(all_rows),
        'unique_raw': len(uniq),
        'filtered_keep': len(keep),
        'out_csv': str(out_csv),
        'out_jsonl': str(out_jsonl),
        'mode': args.mode,
        'after': args.after,
        'before': args.before,
        'operational_defaults': {
            'count_per_request': 100,
            'max_pages_per_channel': args.max_pages,
            'sleep_seconds': args.sleep_seconds,
            'ratelimit_sleep_seconds': max(3.0, args.sleep_seconds * 4),
        },
        'telemetry': {
            'ratelimit_retries': ratelimit_retries,
            'total_requests': total_requests,
            'duration_seconds': round(time.time() - start_ts, 2),
        }
    }
    if args.summary_json:
        p = Path(args.summary_json)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
