#!/usr/bin/env python3
"""把 tccli 的报错输出翻译成 agent 能直接执行的动作。

用法：
    tccli dnspod ... 2>&1 | python3 tc_error.py
    python3 tc_error.py --action TerminateInstances < err.txt   # 带上调用的 Action 名，判断更准

输出一行 JSON：{"kind", "code", "message", "action": {"type", ...}}
action.type 取值：
    fix_args     参数写错了，按 hint 改了再调
    fix_env      本机环境问题（缺依赖/没凭证），agent 自己修
    retry        等 after_seconds 秒后重试
    continue     不是失败（如"查无记录"），当作空结果继续
    change_route 这条路走不通，换路径（如没备案 → overseas）
    notify_user  需要人做，附 card（见 references/human-cards.md）
无报错时输出 {"kind": "ok"}。纯标准库，Python 3.8+。
"""
import json
import re
import sys
from pathlib import Path

# 我们的 agent-ops 策略里故意 deny 的动作 → 被拒是预期的，转人工，不要去要权限
POLICY = Path(__file__).resolve().parent.parent / "references" / "agent-ops-policy.json"


def _denied_by_design() -> set:
    try:
        st = json.loads(POLICY.read_text())["statement"]
        return {a.split(":", 1)[1] for s in st if s["effect"] == "deny" for a in s["action"]}
    except Exception:
        return set()


def classify(text: str, action_name: str = "") -> dict:
    """解析 tccli 风格的报错文本（兼容旧用法）。tcapi.py 直接调用 classify_code。"""
    m = re.search(r"code:([A-Za-z0-9.]+)\s+message:(.*?)(?:\s+requestId:|$)", text, re.S)
    code, msg = (m.group(1), m.group(2).strip()) if m else ("", "")
    if not code:
        lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
        msg = lines[-1] if lines else ""

    def out(kind, action):
        return {"kind": kind, "code": code, "message": msg[:300], "action": action}

    if "No module named 'crcmod'" in text:
        return out("env", {"type": "fix_env", "hint": "用 tccli 所在的 python 执行 pip install crcmod；或者改用 scripts/tcapi.py（不依赖 tccli）"})
    if re.search(r"secretId is invalid", text):
        return classify_code("AuthFailure.SecretIdNotFound", msg, action_name)
    if not code and re.search(r"Unknown options|ambiguous option|invalid choice|invalid int value|Invalid JSON|Invalid choice", text):
        return out("bad_args", {"type": "fix_args", "hint": (
            "tccli 参数语法问题。建议改用 scripts/tcapi.py（Key=字符串 / Key:=JSON）。"
            "如果坚持用 tccli：参数名区分大小写、会前缀匹配；嵌套参数传 JSON，或加 --cli-unfold-argument；"
            "全局参数小写（--region --profile）；zsh 下变量不分词，改用 bash。")})
    if not text.strip():
        return {"kind": "ok"}
    if not code:
        return out("unknown", {"type": "fix_args", "hint": "没有 API 错误码，看 message，多半是 CLI 层的问题"})
    return classify_code(code, msg, action_name)


def classify_code(code: str, msg: str = "", action_name: str = "") -> dict:
    """按腾讯云 API 错误码分类，返回 {kind, code, message, action}。"""
    def out(kind, action):
        return {"kind": kind, "code": code, "message": (msg or "")[:300], "action": action}

    if code in ("Local.NoCredential",) or re.search(r"SecretIdNotFound|InvalidCredential|SignatureFailure|SecretKey", code):
        return out("credential", {"type": "notify_user", "card": "C0",
                                  "say": "腾讯云密钥无效、已被删除或还没配置，需要重新走一次接入向导（setup.py）。"})
    if code == "Local.BadArgs":
        return out("bad_args", {"type": "fix_args", "hint": "服务名/接口名不合法：服务名是小写产品缩写（如 dnspod），接口名首字母大写（如 DescribeRecordList）"})
    if code in ("Local.HTTPError", "Local.BadResponse"):
        return out("provider_error", {"type": "retry", "after_seconds": 30, "max_attempts": 1,
                                      "then": "notify_user：腾讯云返回了非标准响应，可能是网络或代理问题"})
    if code == "Local.NetworkError":
        return out("network", {"type": "retry", "after_seconds": 10,
                               "hint": "连不上 *.tencentcloudapi.com：检查网络或代理"})

    # —— 权限 ——
    if "UnauthorizedOperation" in code or "CamNoAuth" in code or "NoPermission" in code:
        act = action_name
        if not act:
            mm = re.search(r"operation \(\w+:(\w+)\)|operation `(\w+)`|执行 `(\w+)`|action\W+\w+:(\w+)", msg)
            act = next((g for g in mm.groups() if g), "") if mm else ""
        if act and act in _denied_by_design():
            return out("human_only", {"type": "notify_user", "card": "human_op",
                                      "say": f"{act} 涉及付费或不可逆操作，按约定由你在控制台完成。"})
        if "finance" in msg:
            return out("human_only", {"type": "notify_user", "card": "human_op",
                                      "say": "这一步要付费，需要你在控制台完成。"})
        # 超出 agent-ops 策略范围：交给人在控制台做。agent 不申请、也不建议追加任何权限
        return out("permission", {"type": "notify_user", "card": "human_op",
                                  "say": f"这一步（{act or code}）不在我的权限范围内，需要你在腾讯云控制台操作。"
                                         "我不会去申请额外权限。"})

    # —— 业务语义 ——
    if code == "OperationDenied.DomainNoICP":
        return out("icp_required", {"type": "change_route",
                                    "hint": "域名未备案：EdgeOne 改用 Area=overseas，或用香港/海外服务器（见 R2/R3）"})
    if code in ("InvalidParameterValue.InvalidDomainStatus",) or "Status" in code and code.startswith("OperationDenied"):
        return out("not_ready", {"type": "retry", "after_seconds": 60, "hint": "资源还在部署中，等 online 再操作"})
    if code.startswith("ResourceNotFound") or code == "ResourceNotFound.NoDataOfRecord":
        return out("not_found", {"type": "continue", "hint": "查无数据，按空结果处理（不是失败）"})
    if code.startswith("RequestLimitExceeded") or code.startswith("LimitExceeded.Frequency"):
        return out("rate_limit", {"type": "retry", "after_seconds": 5})
    if code.startswith(("InvalidParameter", "MissingParameter", "UnknownParameter")):
        return out("bad_args", {"type": "fix_args",
                                "hint": "看 message 改参数；注意腾讯云会先校验参数和资源是否存在，再校验权限"})
    if code.startswith(("InternalError", "FailedOperation")):
        return out("provider_error", {"type": "retry", "after_seconds": 30, "max_attempts": 1,
                                      "then": "notify_user：附 code+message，可能需要控制台操作或提工单"})
    return out("other", {"type": "notify_user", "card": "human_op", "say": f"腾讯云返回 {code}：{msg[:120]}"})


if __name__ == "__main__":
    act = ""
    if "--action" in sys.argv:
        act = sys.argv[sys.argv.index("--action") + 1]
    print(json.dumps(classify(sys.stdin.read(), act), ensure_ascii=False))
