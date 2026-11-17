#!/usr/bin/env python3
"""腾讯云接入体检：凭证、身份、各服务权限，一次输出 JSON。只发只读请求，不花钱，也不改任何东西。
纯标准库，Python 3.8+，Windows/macOS/Linux 通用，不依赖 tccli。

用法：
    python doctor.py [--profile agent-ops] [--region ap-hongkong]

输出：
    {"ok": bool,
     "credential": "env | profile:<name> | missing",
     "identity": {"uin", "owner_uin", "type"},
     "access": {"dnspod": "allowed|denied|error:<code>", ...},
     "next": [ {action...}, ... ]}      # next 为空，就可以开始干活
access 的含义：对该服务发一个只读调用，看是否放行。写权限以 references/agent-ops-policy.json 为准。
"""
import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tcapi  # noqa: E402
from tc_error import classify_code  # noqa: E402

# 服务 → (只读 Action, 参数, 所属路径)。finance 预期为 denied
PROBES = {
    "dnspod":     ("DescribeDomainList", {"Limit": 1}, "R1 DNS"),
    "teo":        ("DescribeZones", {}, "R2 EdgeOne"),
    "ssl":        ("DescribeCertificates", {"Limit": 1}, "证书"),
    "lighthouse": ("DescribeInstances", {}, "R3 轻量服务器"),
    "tat":        ("DescribeCommands", {}, "R3 远程执行命令"),
    "domain":     ("CheckDomain", {"DomainName": "agentops-probe-zq81x.com"}, "R0 域名查询"),
}


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", default=tcapi.DEFAULT_PROFILE)
    ap.add_argument("--region", default=None, help="地域服务（lighthouse/tat）的探测地域，默认取 profile 配置")
    a = ap.parse_args()
    res = {"ok": False, "credential": "missing", "identity": {}, "access": {}, "next": []}

    def done():
        res["ok"] = not res["next"]
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0 if res["ok"] else 1

    if os.environ.get("TENCENTCLOUD_SECRET_ID"):
        res["credential"] = "env"
    elif tcapi.cred_path(a.profile).exists():
        res["credential"] = f"profile:{a.profile}"     # 只检查文件在不在，不读出内容
    else:
        res["next"].append({"type": "notify_user", "card": "C0",
                            "say": "还没有连上腾讯云。我会打开一个本地网页，带你一步步完成（约 5 分钟）。",
                            "run": "python scripts/setup.py"})
        return done()

    try:
        ident = tcapi.call("sts", "GetCallerIdentity", profile=a.profile, region=a.region)
    except tcapi.TcError as e:
        res["next"].append(classify_code(e.code, e.message, "GetCallerIdentity")["action"])
        return done()
    res["identity"] = {"uin": ident.get("UserId"), "owner_uin": ident.get("AccountId"), "type": ident.get("Type")}
    if ident.get("Type") != "CAMUser":
        res["next"].append({"type": "notify_user", "card": "C0",
                            "say": "现在用的是主账号密钥，权限太大。建议重新走一遍接入向导，改用 agent-ops 子用户。"})

    for svc, (action, params, route) in PROBES.items():
        try:
            tcapi.call(svc, action, params, region=a.region, profile=a.profile)
            res["access"][svc] = "allowed"
        except tcapi.TcError as e:
            c = classify_code(e.code, e.message, action)
            if c["kind"] in ("not_found",):
                # 查不到数据：腾讯云可能先校验资源再校验权限，所以这只能算"未验证"，不算放行
                res["access"][svc] = "unverified"
                res["notes"] = res.get("notes", []) + [f"{svc}：账号下暂无数据，权限未能实测（{e.code}）"]
            elif c["kind"] in ("permission", "human_only"):
                res["access"][svc] = "denied"
                res["next"].append({"type": "notify_user", "card": "grant", "service": svc, "route": route,
                                    "say": f"agent-ops 没有 {svc} 权限，{route} 用不了。请确认子用户挂的是 agent-ops-web 策略。"})
            else:   # 网络错误、服务异常等：不确定 ≠ 通过，必须进 next
                res["access"][svc] = f"error:{e.code}"
                res["next"].append({**c["action"], "service": svc, "route": route,
                                    "say": f"{svc} 探测没有得到明确结果（{e.code}），暂时不能确认 {route} 可用。"})

    # 权限不能过大：这几项必须被明确拒绝（计费、管理子用户、云服务器 CVM 不在 agent-ops 范围内）
    for svc, action, label in (("billing", "DescribeAccountBalance", "finance"), ("cam", "ListUsers", "cam"),
                               ("cvm", "DescribeInstances", "cvm")):
        try:
            tcapi.call(svc, action, {}, region=a.region or "ap-hongkong", profile=a.profile)
            res["access"][label] = "allowed"
            res["next"].append({"type": "notify_user", "card": "C0", "say":
                                f"这个子用户能调用 {svc}:{action}，权限超出了 agent 需要的范围。请确认 agent-ops 只挂了 agent-ops-web 策略。"})
        except tcapi.TcError as e:
            kind = classify_code(e.code, e.message, action)["kind"]
            if kind in ("permission", "human_only"):
                res["access"][label] = "denied"
            else:
                res["access"][label] = f"error:{e.code}"
                res["next"].append({"type": "retry", "after_seconds": 10,
                                    "say": f"没能确认 {label} 权限是否被拒（{e.code}），稍后重跑 doctor。"})
    return done()


if __name__ == "__main__":
    sys.exit(main())
