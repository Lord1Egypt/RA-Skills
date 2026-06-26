#!/usr/bin/env python3
"""
poll-pipeline.py
监听流水线运行，完成后以飞书卡片形式通知结果。
失败时自动获取失败 Job 的最后 50 行日志并附在卡片中。

凭证读取优先级：环境变量 > .env.local > ~/.openclaw/openclaw.json
必须设置：YUNXIAO_TOKEN / YUNXIAO_ORG_ID / FEISHU_USER_OPEN_ID

用法：
  python3 poll-pipeline.py <pipelineRunId> [pipelineId]
"""

import json, os, sys, urllib.request, urllib.error, time
from pathlib import Path

# ── 配置读取 ───────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent.resolve()

def load_env_file(path):
    result = {}
    try:
        for line in Path(path).read_text().splitlines():
            m = __import__('re').match(r'^([A-Z_]+)=(.*)', line)
            if m: result[m.group(1)] = m.group(2).strip().strip('"\'`')
    except Exception: pass
    return result

def load_openclaw_config():
    try:
        cfg = json.loads(Path.home().joinpath('.openclaw/openclaw.json').read_text())
        feishu = cfg.get('channels', {}).get('feishu', {})
        return {
            'FEISHU_APP_ID': feishu.get('appId', ''),
            'FEISHU_APP_SECRET': feishu.get('appSecret', ''),
        }
    except Exception: return {}

local_env = load_env_file(SCRIPT_DIR.parent / '.env.local')
oc_cfg = load_openclaw_config()

def cfg(key, fallback=''):
    return os.environ.get(key) or local_env.get(key) or oc_cfg.get(key) or fallback

YUNXIAO_TOKEN = cfg('YUNXIAO_TOKEN')
ORG_ID        = cfg('YUNXIAO_ORG_ID')
NOTIFY_OPEN_ID = cfg('FEISHU_USER_OPEN_ID')
FEISHU_APP_ID     = cfg('FEISHU_APP_ID') or cfg('FEISHU_APP_ID')
FEISHU_APP_SECRET = cfg('FEISHU_APP_SECRET')

if not YUNXIAO_TOKEN or not ORG_ID:
    print('[error] 缺少 YUNXIAO_TOKEN 或 YUNXIAO_ORG_ID 配置', flush=True)
    sys.exit(1)

DEFAULT_PIPELINE_ID = cfg('YUNXIAO_DEFAULT_PIPELINE_ID', '0')

# ── 参数解析 ───────────────────────────────────────────────────────────────────
TARGET_RUN_ID = None
PIPELINE_ID = DEFAULT_PIPELINE_ID

args = sys.argv[1:]
i = 0
while i < len(args):
    if args[i] == '--pipeline-id' and i + 1 < len(args):
        PIPELINE_ID = args[i + 1]; i += 2
    elif TARGET_RUN_ID is None and not args[i].startswith('-'):
        TARGET_RUN_ID = int(args[i]); i += 1
    elif PIPELINE_ID == DEFAULT_PIPELINE_ID and not args[i].startswith('-'):
        PIPELINE_ID = args[i]; i += 1
    else: i += 1

# ── 云效 REST API ─────────────────────────────────────────────────────────────
YUNXIAO_BASE = f'https://openapi-rdc.aliyuncs.com/oapi/v1/flow/organizations/{ORG_ID}'

def yunxiao_get(path):
    req = urllib.request.Request(
        f'https://openapi-rdc.aliyuncs.com/oapi/v1/flow/organizations/{ORG_ID}{path}',
        headers={'x-yunxiao-token': YUNXIAO_TOKEN},
    )
    try:
        resp = urllib.request.urlopen(req, timeout=20)
        body = resp.read()
    except urllib.error.HTTPError as e:
        body = e.read()
        raise RuntimeError(f'HTTP {e.code}: {body[:200]}')
    if not body:
        raise RuntimeError('响应体为空')
    return json.loads(body)

def get_pipeline_run(pipeline_id, run_id):
    """按精确 run_id 查询，不用 latestPipelineRun 避免竞态"""
    return yunxiao_get(f'/pipelines/{pipeline_id}/runs/{run_id}')

def get_job_log(job_id, pipeline_run_id):
    try:
        data = yunxiao_get(f'/pipelines/{PIPELINE_ID}/runs/{pipeline_run_id}/job/{job_id}/log')
        text = data if isinstance(data, str) else data.get('log', data.get('content', ''))
        lines = [l for l in str(text).strip().splitlines() if l.strip()]
        if not lines: return '（日志为空，可能任务尚未执行或已被取消）'
        return '\n'.join(lines[-50:] if len(lines) > 50 else lines)
    except Exception as e:
        return f'（日志获取失败：{e}）'

# ── 飞书 ───────────────────────────────────────────────────────────────────────
def get_feishu_token():
    req = urllib.request.Request(
        'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
        data=json.dumps({'app_id': FEISHU_APP_ID, 'app_secret': FEISHU_APP_SECRET}).encode(),
        headers={'Content-Type': 'application/json'},
    )
    return json.loads(urllib.request.urlopen(req).read())['tenant_access_token']

def send_card(card):
    token = get_feishu_token()
    req = urllib.request.Request(
        'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id',
        data=json.dumps({'receive_id': NOTIFY_OPEN_ID, 'msg_type': 'interactive',
                         'content': json.dumps(card)}).encode(),
        headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
    )
    req.get_method = lambda: 'POST'
    resp = json.loads(urllib.request.urlopen(req).read())
    if resp.get('code') != 0: raise RuntimeError(f'飞书发送失败: {resp}')
    return resp['data']['message_id']

# ── 卡片 ───────────────────────────────────────────────────────────────────────
STATUS_MAP = {'SUCCESS': ('✅','成功','green'), 'FAIL': ('❌','失败','red'),
              'CANCELED': ('⛔','已取消','grey'), 'RUNNING': ('🔄','运行中','blue')}

def fmt_status(s): return STATUS_MAP.get(s, ('❓', s, 'grey'))
def fmt_duration(start, end):
    if not start or not end: return '--'
    sec = round((end - start) / 1000)
    return f'{sec // 60}m {sec % 60}s' if sec >= 60 else f'{sec}s'
def fmt_time(ms):
    if not ms: return '--'
    import datetime
    dt = datetime.datetime.fromtimestamp(ms/1000, tz=datetime.timezone(datetime.timedelta(hours=8)))
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def build_card(run, fail_logs=None):
    status = run.get('status', '')
    emoji, label, color = fmt_status(status)
    run_id = run.get('pipelineRunId', '--')
    duration = fmt_duration(run.get('createTime'), run.get('updateTime'))
    gp = {p['key']: p['value'] for p in run.get('globalParams', [])}
    pipeline_name = gp.get('PIPELINE_NAME') or f'pipeline-{PIPELINE_ID}'
    branch = gp.get('CI_COMMIT_REF_NAME') or 'main'
    commit_id = gp.get('CI_COMMIT_ID') or '手动触发'
    commit_msg = gp.get('CI_COMMIT_TITLE') or ''
    stage_lines = []
    for s in run.get('stages', []):
        si = s.get('stageInfo', {})
        se, _, _ = fmt_status(si.get('status', ''))
        jobs = '\n'.join(f'　{fmt_status(j.get("status",""))[0]} {j.get("name","")}' for j in si.get('jobs', []))
        stage_lines.append(f'{se} **{s.get("name","")}**\n{jobs}')
    elements = [
        {'tag': 'div', 'text': {'tag': 'lark_md', 'content': f'**{pipeline_name}** · 运行 #{run_id}'}},
        {'tag': 'div', 'fields': [
            {'is_short': True, 'text': {'tag': 'lark_md', 'content': f'**分支**\n{branch}'}},
            {'is_short': True, 'text': {'tag': 'lark_md', 'content': f'**Commit**\n`{commit_id}` {commit_msg}'}},
            {'is_short': True, 'text': {'tag': 'lark_md', 'content': f'**触发时间**\n{fmt_time(run.get("createTime"))}'}},
            {'is_short': True, 'text': {'tag': 'lark_md', 'content': f'**耗时**\n{duration}'}},
        ]},
        {'tag': 'hr'},
        {'tag': 'div', 'text': {'tag': 'lark_md', 'content': '\n\n'.join(stage_lines) or '暂无阶段信息'}},
    ]
    if fail_logs:
        for job_name, log in fail_logs.items():
            elements += [{'tag': 'hr'}, {'tag': 'div', 'text': {'tag': 'lark_md',
                'content': f'**❌ {job_name} — 失败日志（最后50行）**\n```\n{log}\n```'}}]
    return {'config': {'wide_screen_mode': True},
            'header': {'title': {'tag': 'plain_text', 'content': f'🚀 流水线 #{run_id} {emoji} {label}'}, 'template': color},
            'elements': elements}

# ── 主循环 ─────────────────────────────────────────────────────────────────────
print(f'[info] 开始轮询 runId={TARGET_RUN_ID}', flush=True)
for i in range(90):
    time.sleep(10)
    try:
        run = get_pipeline_run(PIPELINE_ID, TARGET_RUN_ID)
    except Exception as e:
        print(f'[warn] 查询失败: {e}', flush=True); continue
    status = run.get('status')
    run_id_actual = run.get('pipelineRunId')
    print(f'[{(i+1)*10}s] runId={run_id_actual} status={status}', flush=True)
    if status in ('SUCCESS', 'FAIL', 'CANCELED'):
        fail_logs = {}
        if status == 'FAIL':
            for s in run.get('stages', []):
                for j in s.get('stageInfo', {}).get('jobs', []):
                    if j.get('status') == 'FAIL':
                        jid = j.get('id')
                        print(f'[info] 获取失败 job 日志: {j.get("name")} (id={jid})', flush=True)
                        fail_logs[j.get('name', str(jid))] = get_job_log(jid, latest_id)
        card = build_card(run, fail_logs or None)
        try:
            msg_id = send_card(card)
            print(f'[info] 卡片已发送 message_id={msg_id}', flush=True)
        except Exception as e:
            print(f'[error] 卡片发送失败: {e}', flush=True)
        break
else:
    card = {'config': {}, 'header': {'title': {'tag': 'plain_text', 'content': '⚠️ 流水线轮询超时'}, 'template': 'yellow'},
            'elements': [{'tag': 'div', 'text': {'tag': 'lark_md', 'content': f'流水线 #{TARGET_RUN_ID} 轮询超时（15分钟），请手动检查云效。'}}]}
    try: send_card(card)
    except Exception as e: print(f'[error] {e}', flush=True)
