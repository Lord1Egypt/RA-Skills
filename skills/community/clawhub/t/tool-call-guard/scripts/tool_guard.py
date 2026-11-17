# -*- coding: utf-8 -*-
"""工具调用闸门：按副作用给 tool call 定级(读/写/删/外发/支付)，给 放行/拦截 决策。零依赖。"""
import argparse, json, pathlib, re

# 风险关键词 → 级别
RISK_MAP = [
    (4, ["delete", "remove", "rm", "drop", "truncate", "purge", "pay", "transfer", "order", "purchase", "refund", "销毁", "删除", "支付", "转账", "下单", "购买"]),
    (3, ["send", "email", "mail", "post", "publish", "tweet", "message", "notify", "reply", "发邮件", "发送", "发消息", "发布", "发表", "回复"]),
    (2, ["write", "create", "update", "insert", "save", "edit", "upload", "modify", "set", "写入", "创建", "更新", "保存", "修改", "上传", "编辑"]),
    (1, ["fetch", "http", "request", "get", "download", "调用", "请求", "下载"]),
    (0, ["read", "search", "list", "query", "lookup", "view", "读取", "搜索", "查询", "查看", "列出"]),
]

def classify(tool_name, args_text):
    txt = (tool_name or "") + " " + (args_text or "")
    txt_l = txt.lower()
    level = 0
    hit = []
    for lv, kws in RISK_MAP:
        for kw in kws:
            if kw.lower() in txt_l:
                if lv > level:
                    level = lv
                hit.append(kw)
    return level, hit

def decide(level):
    if level >= 3:
        return "BLOCK", "高危动作(外发/不可逆)，需人工确认，禁止自动执行"
    if level == 2:
        return "CONFIRM", "写入类动作，执行前需向用户确认"
    return "ALLOW", "只读/网络读，可放行(记日志)"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tool", required=True)
    ap.add_argument("--args", default="")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    try:
        args_text = json.dumps(json.loads(a.args), ensure_ascii=False) if a.args.strip().startswith("{") else a.args
    except Exception:
        args_text = a.args

    level, hit = classify(a.tool, args_text)
    action, reason = decide(level)
    names = ["只读", "网络读", "写入", "外发", "不可逆"]
    if a.json:
        print(json.dumps({"tool": a.tool, "level": level, "level_name": names[level],
                          "action": action, "reason": reason, "matched": hit}, ensure_ascii=False, indent=2))
    else:
        print(f"工具：{a.tool}  级别：L{level} {names[level]}  命中：{hit}")
        print(f"决策：{'🔒 拦截' if action=='BLOCK' else '⚠️ 需确认' if action=='CONFIRM' else '✅ 放行'}  {reason}")

if __name__ == "__main__":
    main()
