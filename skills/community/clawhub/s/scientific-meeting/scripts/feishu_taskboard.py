#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书多维表格 · 会议任务中控台 (Feishu Bitable Task Console)
==========================================================
配套 scientific-meeting skill 使用：把会议纪要提取出的任务写入飞书多维表格，
团队在飞书里直接打勾，Hermes 下次会前拉回看板检查完成度。

零依赖：只用 Python 标准库 (urllib)。

命令：
  init    --url <多维表格链接>                 校验连通、自动补齐字段、打印看板
  add     --task "..." --owner "..." [--ddl 2026-08-15] [--priority 高|中|低]
          [--source "会议名"] [--note "..."]   添加一条任务
  batch   --file tasks.json                    批量添加（会议拆解一次入库）
  list    [--owner 某人] [--status 已完成|未完成|卡住|进行中|未开始] [--json]
                                              拉取看板（默认只看未完成）
  update  --record-id <id> --status <状态>     改状态（Hermes 同步用；人勾选在飞书里点）
  fields                                        打印当前字段结构

配置文件：~/.config/feishu-task-console.json  (chmod 600，含 app_id/app_secret)
  {"app_id":"...","app_secret":"...","app_token":"...","table_id":"..."}

凭证获取：open.feishu.cn 创建企业自建应用 → 开通 bitable:app / bitable:record 权限
→ 把应用加为目标多维表格协作者 → 表格链接填进 init --url。
"""
import argparse
import datetime
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

API_BASE = "https://open.feishu.cn/open-apis"
CONFIG_PATH = os.path.expanduser("~/.config/feishu-task-console.json")
TOKEN_CACHE = os.path.expanduser("~/.config/feishu-token-cache.json")

FIELDS = [
    ("任务", 1, None),                      # 多行文本
    ("负责人", 1, None),                    # 多行文本（团队小，文本比人员字段省事）
    ("DDL", 5, None),                       # 日期
    ("状态", 3, ["未开始", "进行中", "已完成", "卡住"]),   # 单选
    ("优先级", 3, ["高", "中", "低"]),       # 单选
    ("来源会议", 1, None),                  # 多行文本
    ("备注", 1, None),                      # 多行文本
]


def die(msg):
    print(f"[错误] {msg}", file=sys.stderr)
    sys.exit(1)


def load_config():
    if not os.path.exists(CONFIG_PATH):
        die(
            f"配置文件不存在: {CONFIG_PATH}\n"
            "1) 去 open.feishu.cn 创建企业自建应用，开 bitable:app / bitable:record 权限\n"
            "2) 把应用加为目标多维表格的协作者\n"
            "3) 运行: 本脚本 init --url <多维表格链接>"
        )
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    for k in ("app_id", "app_secret", "app_token", "table_id"):
        if not cfg.get(k):
            die(f"配置缺少字段: {k}")
    return cfg


def get_token(cfg):
    now = time.time()
    if os.path.exists(TOKEN_CACHE):
        try:
            with open(TOKEN_CACHE) as f:
                cache = json.load(f)
            if cache.get("expire_at", 0) - now > 300:
                return cache["tenant_access_token"]
        except Exception:
            pass
    body = json.dumps({"app_id": cfg["app_id"], "app_secret": cfg["app_secret"]}).encode()
    # 直接请求：飞书该接口把 tenant_access_token 放在响应顶层（非 data 内），兼容两种返回
    req = urllib.request.Request(
        API_BASE + "/auth/v3/tenant_access_token/internal",
        data=body, headers={"Content-Type": "application/json"}, method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            resp = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        die(f"HTTP {e.code}: {e.read().decode()[:300]}")
    except urllib.error.URLError as e:
        die(f"网络错误: {e.reason}")
    if resp.get("code", 0) != 0:
        die(f"API 错误 code={resp.get('code')} msg={resp.get('msg')}")
    tok = resp.get("tenant_access_token") or (resp.get("data") or {}).get("tenant_access_token")
    expire = resp.get("expire", 7200)
    if not tok:
        die(f"无法获取 tenant_access_token: {str(resp)[:200]}")
    with open(TOKEN_CACHE, "w") as f:
        json.dump({"tenant_access_token": tok, "expire_at": now + expire}, f)
    os.chmod(TOKEN_CACHE, 0o600)
    return tok


def api_call(path, body=None, need_token=True, no_retry=False, method=None):
    url = API_BASE + path
    headers = {"Content-Type": "application/json"}
    if need_token:
        cfg = load_config()
        headers["Authorization"] = "Bearer " + get_token(cfg)
    if method is None:
        method = "POST" if body is not None else "GET"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        if not no_retry and e.code == 401:
            # token 过期，清缓存重试一次
            if os.path.exists(TOKEN_CACHE):
                os.remove(TOKEN_CACHE)
            return api_call(path, body, need_token=True, no_retry=True, method=method)
        die(f"HTTP {e.code}: {raw[:300]}")
    except urllib.error.URLError as e:
        die(f"网络错误: {e.reason}")
    if data.get("code", 0) != 0:
        die(f"API 错误 code={data.get('code')} msg={data.get('msg')} 详情={str(data.get('errors'))[:200]}")
    return data.get("data", {})


def parse_table_url(url):
    m = re.search(r"/base/([A-Za-z0-9]+)", url)
    if not m:
        die("链接格式不对，应为: https://xxx.feishu.cn/base/<app_token>?table=<table_id>")
    app_token = m.group(1)
    m2 = re.search(r"[?&]table=([A-Za-z0-9]+)", url)
    table_id = m2.group(1) if m2 else None
    return app_token, table_id


def list_tables(cfg, app_token):
    data = api_call(f"/bitable/v1/apps/{app_token}/tables?page_size=100")
    return data.get("items", [])


def ensure_fields(cfg):
    """补齐字段，返回 {字段名: field_id}"""
    data = api_call(f"/bitable/v1/apps/{cfg['app_token']}/tables/{cfg['table_id']}/fields?page_size=100")
    existing = {it["field_name"]: it for it in data.get("items", [])}
    for name, ftype, opts in FIELDS:
        if name in existing:
            continue
        body = {"field_name": name, "type": ftype}
        if opts:
            body["property"] = {"options": [{"name": o} for o in opts]}
        api_call(
            f"/bitable/v1/apps/{cfg['app_token']}/tables/{cfg['table_id']}/fields",
            json.dumps(body).encode(),
        )
        print(f"[字段] 已创建: {name}")
    return {it["field_name"]: it["field_id"] for it in api_call(
        f"/bitable/v1/apps/{cfg['app_token']}/tables/{cfg['table_id']}/fields?page_size=100"
    ).get("items", [])}


def date_to_ms(datestr):
    try:
        dt = datetime.datetime.strptime(datestr, "%Y-%m-%d")
    except ValueError:
        die(f"DDL 格式应为 YYYY-MM-DD，收到: {datestr}")
    # 按 UTC+8 零点入库
    ts = dt.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=8))).timestamp()
    return int(ts * 1000)


def ms_to_date(ms):
    return datetime.datetime.fromtimestamp(ms / 1000, datetime.timezone(datetime.timedelta(hours=8))).strftime("%m-%d")


def build_fields_dict(args, note=None):
    f = {}
    if args.task:
        f["任务"] = args.task
    if args.owner:
        f["负责人"] = args.owner
    if args.ddl:
        f["DDL"] = date_to_ms(args.ddl)
    if args.status:
        f["状态"] = args.status
    if args.priority:
        f["优先级"] = args.priority
    if args.source:
        f["来源会议"] = args.source
    if note:
        f["备注"] = note
    return f


def cmd_init(args):
    app_token, table_id = parse_table_url(args.url)
    # 写入配置（保留已有 app_id/app_secret）
    cfg = {}
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            cfg = json.load(f)
    cfg["app_token"] = app_token
    cfg["table_id"] = table_id
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    os.chmod(CONFIG_PATH, 0o600)
    print(f"[配置] 已写入 {CONFIG_PATH} (app_token={app_token})")
    if not cfg.get("app_id"):
        die("还缺 app_id/app_secret —— 打开配置文件手动填入，或重跑本脚本前先填好")
    # 校验连通 + 找 table
    if not table_id:
        tables = list_tables(cfg, app_token)
        if not tables:
            die("该多维表格里没有数据表，请先在飞书里建一个空表")
        table_id = tables[0]["table_id"]
        cfg["table_id"] = table_id
        with open(CONFIG_PATH, "w") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
        print(f"[配置] 未指定 table，自动选了: {tables[0]['name']} ({table_id})")
    ensure_fields(cfg)
    print("[OK] 连通正常。字段就绪，可以 add / batch 了。")


def cmd_add(args):
    cfg = load_config()
    ensure_fields(cfg)
    body = {"fields": build_fields_dict(args)}
    api_call(
        f"/bitable/v1/apps/{cfg['app_token']}/tables/{cfg['table_id']}/records",
        json.dumps(body).encode(),
    )
    print(f"[添加] {args.task} → 负责人:{args.owner or '未定'} DDL:{args.ddl or '未定'}")


def cmd_batch(args):
    if not os.path.exists(args.file):
        die(f"文件不存在: {args.file}")
    with open(args.file) as f:
        tasks = json.load(f)
    if not isinstance(tasks, list):
        die("batch 文件必须是 JSON 数组: [{\"task\":..., \"owner\":..., \"ddl\":...}, ...]")
    cfg = load_config()
    ensure_fields(cfg)
    for t in tasks:
        missing = [k for k in ("task",) if not t.get(k)]
        if missing:
            die(f"任务缺少字段 {missing}: {t}")
        body = {"fields": {
            "任务": t["task"],
            "负责人": t.get("owner", ""),
            "来源会议": t.get("source", ""),
            "备注": t.get("note", ""),
        }}
        if t.get("ddl"):
            body["fields"]["DDL"] = date_to_ms(t["ddl"])
        if t.get("priority"):
            body["fields"]["优先级"] = t["priority"]
        if t.get("status"):
            body["fields"]["状态"] = t["status"]
        api_call(
            f"/bitable/v1/apps/{cfg['app_token']}/tables/{cfg['table_id']}/records",
            json.dumps(body).encode(),
        )
        print(f"[批量] +{t['task']} (@{t.get('owner','未定')} {t.get('ddl','')})")
    print(f"[完成] 共写入 {len(tasks)} 条")


def cmd_list(args):
    cfg = load_config()
    params = "?page_size=100"
    data = api_call(f"/bitable/v1/apps/{cfg['app_token']}/tables/{cfg['table_id']}/records{params}")
    items = data.get("items", [])
    rows = []
    for it in items:
        rf = it.get("fields", {})
        def text(field):
            v = rf.get(field)
            if v is None:
                return ""
            if isinstance(v, list):
                return ",".join(x.get("text", "") for x in v if isinstance(x, dict))
            if isinstance(v, dict):
                return v.get("text", "")
            return str(v)
        ddl = rf.get("DDL")
        rows.append({
            "record_id": it.get("record_id"),
            "任务": text("任务"),
            "负责人": text("负责人"),
            "DDL": ms_to_date(ddl) if isinstance(ddl, (int, float)) else (text("DDL") or ""),
            "状态": text("状态") or "未开始",
            "优先级": text("优先级"),
            "来源": text("来源会议"),
        })
    # 过滤
    if args.owner:
        rows = [r for r in rows if args.owner in r["负责人"]]
    if args.status:
        if args.status == "未完成":
            rows = [r for r in rows if r["状态"] != "已完成"]
        else:
            rows = [r for r in rows if r["状态"] == args.status]
    else:
        rows = [r for r in rows if r["状态"] != "已完成"]
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return
    if not rows:
        print("（无未完成任务 🎉）")
        return
    ico = {"已完成": "✅", "进行中": "🟡", "卡住": "🔴", "未开始": "⚪"}
    print(f"未完成 {len(rows)} 条：")
    for r in rows:
        ddl = f" DDL:{r['DDL']}" if r["DDL"] else ""
        pri = f" [{r['优先级']}]" if r["优先级"] else ""
        print(f"  {ico.get(r['状态'], '⚪')} {r['任务']} | @{r['负责人'] or '未定'}{ddl}{pri} | {r['来源']} | id:{r['record_id']}")


def cmd_update(args):
    cfg = load_config()
    body = {"fields": {"状态": args.status}}
    api_call(
        f"/bitable/v1/apps/{cfg['app_token']}/tables/{cfg['table_id']}/records/{args.record_id}",
        json.dumps(body).encode(),
        method="PUT",
    )
    print(f"[更新] {args.record_id} → {args.status}")


def cmd_fields(args):
    cfg = load_config()
    data = api_call(f"/bitable/v1/apps/{cfg['app_token']}/tables/{cfg['table_id']}/fields?page_size=100")
    for it in data.get("items", []):
        print(f"  {it['field_name']} (type={it['type']}, id={it['field_id']})")


def main():
    p = argparse.ArgumentParser(description="飞书多维表格 · 会议任务中控台")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="校验连通+补齐字段")
    p_init.add_argument("--url", required=True)
    p_init.set_defaults(func=cmd_init)

    p_add = sub.add_parser("add", help="添加一条任务")
    p_add.add_argument("--task", required=True)
    p_add.add_argument("--owner")
    p_add.add_argument("--ddl")
    p_add.add_argument("--priority", choices=["高", "中", "低"])
    p_add.add_argument("--source")
    p_add.add_argument("--status", choices=["未开始", "进行中", "已完成", "卡住"])
    p_add.set_defaults(func=cmd_add)

    p_batch = sub.add_parser("batch", help="批量添加")
    p_batch.add_argument("--file", required=True)
    p_batch.set_defaults(func=cmd_batch)

    p_list = sub.add_parser("list", help="拉取看板")
    p_list.add_argument("--owner")
    p_list.add_argument("--status", help="未完成/已完成/未开始/进行中/卡住")
    p_list.add_argument("--json", action="store_true")
    p_list.set_defaults(func=cmd_list)

    p_upd = sub.add_parser("update", help="改状态")
    p_upd.add_argument("--record-id", required=True)
    p_upd.add_argument("--status", required=True, choices=["未开始", "进行中", "已完成", "卡住"])
    p_upd.set_defaults(func=cmd_update)

    p_fields = sub.add_parser("fields", help="查看字段")
    p_fields.set_defaults(func=cmd_fields)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
