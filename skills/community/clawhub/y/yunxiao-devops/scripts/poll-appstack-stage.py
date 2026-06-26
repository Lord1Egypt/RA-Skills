#!/usr/bin/env python3
"""
poll-appstack-stage.py
轮询 AppStack 工作流阶段执行结果，完成后发飞书卡片通知。

凭证读取优先级：环境变量 > .env.local > ~/.openclaw/openclaw.json
必须设置：YUNXIAO_TOKEN / YUNXIAO_ORG_ID / FEISHU_USER_OPEN_ID

用法：
  python3 poll-appstack-stage.py <appName> <releaseWorkflowSn> <releaseStageSn> <executionNumber> [stageName]
"""

import json, sys, os, time, urllib.request, datetime, subprocess
from pathlib import Path
import re

# ── 配置读取 ───────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent.resolve()

def load_env_file(path):
    result = {}
    try:
        for line in Path(path).read_text().splitlines():
            m = re.match(r'^([A-Z_]+)=(.*)', line)
            if m: result[m.group(1)] = m.group(2).strip().strip('"\'`')
    except Exception: pass
    return result

def load_openclaw_config():
    try:
        cfg = json.loads(Path.home().joinpath('.openclaw/openclaw.json').read_text())
        feishu = cfg.get('channels', {}).get('feishu', {})
        return {'FEISHU_APP_ID': feishu.get('appId',''), 'FEISHU_APP_SECRET': feishu.get('appSecret','')}
    except Exception: return {}

local_env = load_env_file(SCRIPT_DIR.parent / '.env.local')
oc_cfg = load_openclaw_config()

def cfg(key, fallback=''):
    return os.environ.get(key) or local_env.get(key) or oc_cfg.get(key) or fallback

YUNXIAO_TOKEN  = cfg('YUNXIAO_TOKEN')
ORG_ID         = cfg('YUNXIAO_ORG_ID')
NOTIFY_OPEN_ID = cfg('FEISHU_USER_OPEN_ID')
FEISHU_APP_ID     = cfg('FEISHU_APP_ID')
FEISHU_APP_SECRET = cfg('FEISHU_APP_SECRET')
BASE = 'https://openapi-rdc.aliyuncs.com/oapi/v1'

if not YUNXIAO_TOKEN or not ORG_ID:
    print('[error] 缺少 YUNXIAO_TOKEN 或 YUNXIAO_ORG_ID 配置', flush=True)
    sys.exit(1)

# ── 参数 ───────────────────────────────────────────────────────────────────────
args = sys.argv[1:]
if len(args) < 4:
    print('Usage: poll-appstack-stage.py <appName> <releaseWorkflowSn> <releaseStageSn> <executionNumber> [stageName]')
    sys.exit(1)

APP_NAME, WORKFLOW_SN, STAGE_SN, EXECUTION_NUM = args[0], args[1], args[2], args[3]
STAGE_NAME = args[4] if len(args) > 4 else '阶段'
STAGE_URL  = f'https://devops.aliyun.com/appstack/app/{APP_NAME}/workflow/{WORKFLOW_SN}/stage/{STAGE_SN}'
PIPELINE_ID     = os.environ.get('APPSTACK_PIPELINE_ID')
PIPELINE_RUN_ID = os.environ.get('APPSTACK_PIPELINE_RUN_ID')

# ── HTTP 工具（直接调 REST API）─────────────────────────────────────────────────
def yx_get(path):
    req = urllib.request.Request(f'{BASE}{path}', headers={'x-yunxiao-token': YUNXIAO_TOKEN})
    with urllib.request.urlopen(req, timeout=20) as r: return json.loads(r.read())

def yx_post(path, body):
    req = urllib.request.Request(f'{BASE}{path}',
        data=json.dumps(body).encode(),
        headers={'x-yunxiao-token': YUNXIAO_TOKEN, 'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req, timeout=20) as r: return json.loads(r.read())

def get_feishu_token():
    req = urllib.request.Request(
        'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
        data=json.dumps({'app_id': FEISHU_APP_ID, 'app_secret': FEISHU_APP_SECRET}).encode(),
        headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())['tenant_access_token']

def send_card(card):
    token = get_feishu_token()
    req = urllib.request.Request(
        'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id',
        data=json.dumps({'receive_id': NOTIFY_OPEN_ID, 'msg_type': 'interactive',
                         'content': json.dumps(card)}).encode(),
        headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req, timeout=10) as r:
        resp = json.loads(r.read())
    if resp.get('code') != 0: raise RuntimeError(f'飞书发送失败: {resp}')
    return resp['data']['message_id']

def get_pipeline_run_status(pipeline_id, pipeline_run_id):
    try:
        data = yx_get(f'/flow/organizations/{ORG_ID}/pipelines/{pipeline_id}/runs/{pipeline_run_id}')
        return data if isinstance(data, dict) else {}
    except Exception as e:
        print(f'[warn] 查流水线状态失败: {e}', flush=True); return {}

def get_job_log(pipeline_id, job_id, pipeline_run_id=None):
    try:
        path = f'/flow/organizations/{ORG_ID}/pipelines/{pipeline_id}/jobs/{job_id}/log'
        if pipeline_run_id: path += f'?pipelineRunId={pipeline_run_id}'
        data = yx_get(path)
        text = data.get('content', '') if isinstance(data, dict) else str(data)
        text = re.sub(r'\x1b\[[0-9;]*m', '', text)
        lines = [l for l in text.splitlines() if l.strip()]
        return '\n'.join(lines[-50:]) if lines else '（日志为空）'
    except Exception as e:
        return f'（日志获取失败：{e}）'

def get_stage_run():
    try:
        data = yx_post(f'/appstack/organizations/{ORG_ID}/apps/{APP_NAME}/changeOrders/api',
                       {'pagination': 'keyset', 'orderBy': 'id', 'perPage': 5})
        for r in data.get('records', []):
            src = r.get('source') or {}
            if src.get('stageSn') == STAGE_SN and str(src.get('buildId', '')) == str(EXECUTION_NUM):
                return r
    except Exception as e:
        print(f'[warn] 查部署单失败: {e}', flush=True)
    return None

# ── 状态映射 / 卡片 ────────────────────────────────────────────────────────────
STATE_MAP = {'SUCCESS': ('✅','成功','green'), 'FAIL': ('❌','失败','red'),
             'FAILURE': ('❌','失败','red'), 'FAILED': ('❌','失败','red'),
             'CANCEL': ('⛔','已取消','grey'), 'RUNNING': ('🔄','运行中','blue')}

def fmt(state): return STATE_MAP.get((state or '').upper(), ('❓', state or '未知', 'grey'))
def now_str():
    dt = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    return dt.strftime('%H:%M:%S')

def build_card(state, order=None, pipeline_run=None, fail_logs=None):
    emoji, label, color = fmt(state)
    fields = [
        {'is_short': True, 'text': {'tag': 'lark_md', 'content': f'**应用**\n{APP_NAME}'}},
        {'is_short': True, 'text': {'tag': 'lark_md', 'content': f'**阶段**\n{STAGE_NAME}'}},
        {'is_short': True, 'text': {'tag': 'lark_md', 'content': f'**状态**\n{emoji} {label}'}},
        {'is_short': True, 'text': {'tag': 'lark_md', 'content': f'**完成时间**\n{now_str()}'}},
    ]
    elements = [{'tag': 'div', 'fields': fields}]
    if pipeline_run:
        stage_lines = []
        for s in pipeline_run.get('stages', []):
            si = s.get('stageInfo', {})
            se = fmt(si.get('status',''))[0]
            jobs = '\n'.join(f'　{fmt(j.get("status",""))[0]} {j.get("name","")}' for j in si.get('jobs',[]))
            stage_lines.append(f'{se} **{s.get("name","")}**\n{jobs}')
        if stage_lines:
            elements += [{'tag': 'hr'}, {'tag': 'div', 'text': {'tag': 'lark_md', 'content': '\n\n'.join(stage_lines)}}]
    if fail_logs:
        for job_name, log in fail_logs.items():
            elements += [{'tag': 'hr'}, {'tag': 'div', 'text': {'tag': 'lark_md',
                'content': f'**❌ {job_name} — 失败日志（最后50行）**\n```\n{log}\n```'}}]
    elements += [{'tag': 'hr'}, {'tag': 'action', 'actions': [
        {'tag': 'button', 'text': {'tag': 'plain_text', 'content': '🔗 查看云效'}, 'type': 'primary', 'url': STAGE_URL}
    ]}]
    return {'config': {'wide_screen_mode': True},
            'header': {'title': {'tag': 'plain_text', 'content': f'📦 {APP_NAME} · {STAGE_NAME} {emoji} {label}'}, 'template': color},
            'elements': elements}

# ── 主循环 ─────────────────────────────────────────────────────────────────────
print(f'[info] 开始轮询 {APP_NAME}/{STAGE_NAME} execution={EXECUTION_NUM}', flush=True)
final_state = final_order = final_pipeline_run = None

for i in range(90):
    time.sleep(10)
    if PIPELINE_RUN_ID and PIPELINE_ID:
        pr = get_pipeline_run_status(PIPELINE_ID, PIPELINE_RUN_ID)
        state = pr.get('status', '')
        print(f'[{(i+1)*10}s] 流水线状态: {state}', flush=True)
        if state in ('SUCCESS', 'FAIL', 'CANCELED'):
            final_state, final_pipeline_run = state, pr; break
    else:
        order = get_stage_run()
        if order:
            state = order.get('state', '')
            print(f'[{(i+1)*10}s] 部署单状态: {state}', flush=True)
            if state in ('SUCCESS', 'FAIL', 'FAILURE', 'FAILED', 'CANCEL'):
                final_state, final_order = state, order; break
        else:
            print(f'[{(i+1)*10}s] 等待部署单...', flush=True)

if final_state is None:
    card = {'config': {}, 'header': {'title': {'tag': 'plain_text', 'content': f'⚠️ {APP_NAME}·{STAGE_NAME} 轮询超时'}, 'template': 'yellow'},
            'elements': [{'tag': 'div', 'text': {'tag': 'lark_md', 'content': f'执行 #{EXECUTION_NUM} 超过15分钟未完成。'}},
                         {'tag': 'action', 'actions': [{'tag': 'button', 'text': {'tag': 'plain_text', 'content': '🔗 查看云效'}, 'type': 'primary', 'url': STAGE_URL}]}]}
    try: send_card(card)
    except Exception as e: print(f'[error] {e}', flush=True)
    sys.exit(0)

fail_logs = {}
if final_state.upper() in ('FAIL','FAILURE','FAILED') and final_pipeline_run:
    for s in final_pipeline_run.get('stages', []):
        for j in s.get('stageInfo', {}).get('jobs', []):
            if j.get('status','').upper() in ('FAIL','FAILURE','FAILED'):
                jid = j.get('id')
                print(f'[info] 获取失败 job 日志: {j.get("name")}', flush=True)
                fail_logs[j.get('name', str(jid))] = get_job_log(PIPELINE_ID, jid, PIPELINE_RUN_ID)

card = build_card(final_state, final_order, final_pipeline_run, fail_logs or None)
try:
    msg_id = send_card(card)
    print(f'[info] 卡片已发送 message_id={msg_id}', flush=True)
except Exception as e:
    print(f'[error] {e}', flush=True)
