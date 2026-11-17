"""Configure persistent gateway publication alerts without a client scan loop."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import time
import uuid

from workflow_core import API, APIError, Job, atomic_json, digest, micros, read_json, select, workspace_lock

PRODUCT = "wechat-publication-alerts-api"
UPDATE_FIELDS = ("name", "status", "autoRenew", "renewPriceLimitMicros", "renewPeriodDays",
                 "includeDigest", "apiKeyId", "channelIds")
READS = ("options", "accounts", "events", "channels", "deliveries", "orders", "stats")


class Alerts:
    def __init__(self, api):
        self.api = api

    def read(self, action, **params):
        return self.api.request(PRODUCT, {"action": action, **params}, uuid.uuid4().hex)[0]

    def all_accounts(self):
        result = []
        for page in range(1, 102):
            data = self.read("accounts", page=page, pageSize=100)
            batch = data.get("items")
            if not isinstance(batch, list):
                raise ValueError("账号列表格式变化，停止订阅以避免重复购买")
            result.extend(batch)
            total = data.get("pagination", {}).get("total")
            if len(batch) < 100 or isinstance(total, int) and len(result) >= total:
                return result
        raise ValueError("账号列表超过单次安全读取范围，请缩小管理范围")

    def quote(self, inputs, plan_id, renew=False):
        if not inputs or len(inputs) > 100:
            raise ValueError("一次提供 1～100 个公众号")
        options = self.read("options")
        if not options.get("settings", {}).get("enabled") or not options.get("sourceReady"):
            raise ValueError("发文提醒当前暂不可开通；尚未购买或扣费")
        plans = options.get("plans") or options.get("settings", {}).get("plans") or []
        selected = next((p for p in plans if p["id"] == plan_id), None)
        if not selected:
            return {"needsPlan": True, "plans": plans, "serviceStatus": options.get("serviceStatus")}
        resolved = self.read("resolve", inputs=inputs).get("items", [])
        if len(resolved) != len(inputs):
            raise ValueError("账号识别结果不完整，停止购买")
        errors = [r for r in resolved if not isinstance(r.get("profile"), dict) or not r["profile"].get("biz")]
        if errors:
            return {"needsIdentity": True, "unresolved": errors, "chargeMicros": 0}
        profiles = {r["profile"]["biz"]: r["profile"] for r in resolved}
        existing = {a["biz"]: a for a in self.all_accounts()}
        if renew:
            if any(biz not in existing for biz in profiles):
                raise ValueError("续费范围包含尚未订阅的账号，请先 setup")
            targets = list(profiles)
        else:
            # Existing paused, cancelled and expired records are also never silently purchased again.
            targets = [biz for biz in profiles if biz not in existing]
        reused = [existing[biz] for biz in profiles if biz in existing and not renew]
        count = len(targets)
        if count and not selected["minAccounts"] <= count <= selected["maxAccounts"]:
            raise ValueError("实际新增/续费账号数不符合所选套餐，请换匹配套餐；不会重复购买已有账号凑数量")
        charge = selected["priceMicros"] * count if selected.get("billing") == "per_account" else selected["priceMicros"] if count else 0
        return {"plan": selected, "bizs": targets, "profiles": list(profiles.values()),
                "reused": reused, "chargeMicros": charge, "serviceStatus": options.get("serviceStatus"),
                "renewalAccounts": [existing[biz] for biz in targets] if renew else [],
                "digestPriceMicros": options.get("digestPriceMicros"),
                "note": "已有订阅保持原设置；暂停/到期请显式恢复或续费。摘要另计，自动续费须明确开启。"}

    def purchase(self, directory, quote, budget, channel_ids=None, auto_renew=None, include_digest=None, operation="setup"):
        if quote.get("needsPlan") or quote.get("needsIdentity"):
            raise ValueError("请先处理套餐或账号识别结果")
        if not quote["bizs"]:
            return {"purchased": False, "reused": quote["reused"], "message": "没有新增账号，未重复购买；已有设置保持原样"}
        if quote["chargeMicros"] > budget:
            raise ValueError("实时订阅费用超出授权金额，未购买")
        renewal = quote.get("renewalAccounts") or []
        inherited = {}
        if renewal:
            for field, supplied in (("channelIds", channel_ids), ("autoRenew", auto_renew), ("includeDigest", include_digest), ("apiKeyId", None)):
                if supplied is not None:
                    continue
                values = [a.get(field) for a in renewal]
                if any(v != values[0] for v in values):
                    raise ValueError("续费账号的 " + field + " 设置不同，请分组续费以保留原设置")
                inherited[field] = values[0]
        channel_ids = channel_ids if channel_ids is not None else inherited.get("channelIds") or []
        auto_renew = auto_renew if auto_renew is not None else inherited.get("autoRenew", False)
        include_digest = include_digest if include_digest is not None else inherited.get("includeDigest", False)
        channels = self.read("channels").get("items", [])
        enabled = {c["id"] for c in channels if c.get("enabled")}
        if set(channel_ids) - enabled:
            raise ValueError("存在未启用或不属于当前用户的通知渠道")
        plan = quote["plan"]
        params = {"action": "subscribe", "planId": plan["id"], "bizs": quote["bizs"],
                  "expectedPriceMicros": plan["priceMicros"], "expectedPeriodDays": plan["periodDays"],
                  "autoRenew": auto_renew, "includeDigest": include_digest, "channelIds": channel_ids}
        if inherited.get("apiKeyId"):
            params["apiKeyId"] = inherited["apiKeyId"]
        job = Job(directory, self.api, {"operation": operation, "params": params}, budget)
        order = job.call(PRODUCT, params, allowance=quote["chargeMicros"])
        return {"purchased": True, "order": order, "cost": job.totals(),
                "note": "订单成功不等于监听和通知已验证；请查看 monitorStatus、lastConfirmedAt 与 deliveries"}

    def update(self, subscription_id, changes, execute=False):
        if set(changes) - set(UPDATE_FIELDS):
            raise ValueError("不支持的订阅设置字段")
        current = next((a for a in self.all_accounts() if a["id"] == subscription_id), None)
        if current is None:
            raise ValueError("没有找到属于当前用户的订阅")
        if any(k not in current for k in UPDATE_FIELDS):
            raise ValueError("现有设置返回不完整，停止更新以避免覆盖其他设置")
        payload = {**select(current, UPDATE_FIELDS), **changes, "action": "update", "id": subscription_id}
        if payload["status"] == "cancelled":
            payload["autoRenew"] = False
        if not execute:
            return {"preview": payload, "needsExecution": True}
        result = self.api.request(PRODUCT, payload, uuid.uuid4().hex)[0]
        return {"result": result, "subscription": next((a for a in self.all_accounts() if a["id"] == subscription_id), None)}

    def status(self, ids=None):
        accounts = self.all_accounts()
        if ids:
            accounts = [a for a in accounts if a["id"] in ids]
        # Explicit status is checked before monitorStatus; expiry is never displayed as monitoring.
        for row in accounts:
            row["displayStatus"] = row.get("status") if row.get("status") != "active" else row.get("monitorStatus", "pending")
            until = row.get("paidUntil")
            if until:
                try:
                    expiry = datetime.fromisoformat(until.replace("Z", "+00:00"))
                    if expiry.tzinfo is None:
                        raise ValueError("expiry timezone missing")
                    if expiry <= datetime.now(timezone.utc):
                        row["displayStatus"] = "expired"
                except (TypeError, ValueError):
                    row["displayStatus"] = "expiry_unknown"
        return {"items": accounts, "service": self.read("options")}


def main():
    p = argparse.ArgumentParser(description="公众号发文提醒：云端持续运行，Skill 负责设置与核查")
    p.add_argument("command", choices=(*READS, "resolve", "quote", "setup", "renew", "status", "pause", "resume", "cancel", "update", "channel-save", "channel-test"))
    p.add_argument("--workspace", default="MangyunPublicationAlerts")
    p.add_argument("--account", action="append", default=[])
    p.add_argument("--plan-id", default="")
    p.add_argument("--channel-id", action="append", default=None)
    p.add_argument("--station-only", action="store_true", help="明确清空外部通知渠道，只保留站内动态")
    p.add_argument("--id")
    p.add_argument("--params", help="JSON 参数文件，不能包含凭证；渠道地址和密钥通过环境变量读取")
    p.add_argument("--destination-env", default="WM_NOTIFICATION_DESTINATION")
    p.add_argument("--secret-env", default="WM_NOTIFICATION_SECRET")
    p.add_argument("--budget", default="0")
    p.add_argument("--yes", action="store_true")
    p.add_argument("--auto-renew", action=argparse.BooleanOptionalAction, default=None)
    p.add_argument("--include-digest", action=argparse.BooleanOptionalAction, default=None)
    p.add_argument("--operation-id", help="每次新续费的独立业务标识；同次重试复用")
    p.add_argument("--wait-seconds", type=int, default=20)
    args = p.parse_args()
    try:
        if args.station_only and args.channel_id:
            raise ValueError("--station-only 与 --channel-id 不能同时使用")
        if args.station_only:
            args.channel_id = []
        api, params = API(), read_json(args.params) if args.params else {}
        if not isinstance(params, dict) or any(k in params for k in ("secret", "destination", "apiKey", "token", "action")):
            raise ValueError("参数文件须为不含凭证、通知地址或 action 的对象")
        alerts = Alerts(api)
        command = args.command
        if command in READS:
            result = alerts.read(command, **params)
        elif command == "resolve":
            result = alerts.read("resolve", inputs=args.account)
        elif command == "status":
            result = alerts.status([args.id] if args.id else None)
        elif command in ("quote", "setup", "renew"):
            renewing = command == "renew"
            if renewing and not args.operation_id:
                raise ValueError("续费必须设置 --operation-id；同次重试使用相同标识，新周期才换标识")
            quote = alerts.quote(args.account, args.plan_id, renewing)
            if command == "quote" or not args.yes or quote.get("needsPlan") or quote.get("needsIdentity"):
                result = {"quote": quote, "needsExecution": command != "quote"}
            else:
                operation = "renew:" + args.operation_id if renewing else "setup"
                intent = {"operation": operation, "accounts": args.account, "plan": args.plan_id,
                          "channels": args.channel_id, "digest": args.include_digest, "autoRenew": args.auto_renew}
                directory = Path(args.workspace) / digest([api.identity, intent])[:24]
                with workspace_lock(directory):
                    # Reuse the persisted purchase intent after an interrupted response: a new account
                    # may already exist remotely even though the previous local response was lost.
                    saved = directory / "purchase-intent.json"
                    if saved.exists():
                        quote = read_json(saved)
                    elif not quote.get("needsPlan") and not quote.get("needsIdentity"):
                        atomic_json(saved, quote)
                    result = alerts.purchase(directory, quote, micros(args.budget), args.channel_id,
                                             args.auto_renew, args.include_digest, operation)
                if result.get("purchased"):
                    ids = [a["id"] for a in result["order"].get("items", [])]
                    deadline = time.monotonic() + min(60, max(0, args.wait_seconds))
                    while True:
                        current = alerts.status(ids)
                        result["monitoring"] = current
                        if all(a.get("displayStatus") != "pending" for a in current["items"]) or time.monotonic() >= deadline:
                            break
                        time.sleep(min(3, max(0, deadline - time.monotonic())))
        elif command in ("pause", "resume", "cancel", "update"):
            if not args.id:
                raise ValueError("需要 --id 订阅ID")
            changes = params if command == "update" else {"status": {"pause": "paused", "resume": "active", "cancel": "cancelled"}[command]}
            result = alerts.update(args.id, changes, args.yes)
        elif command in ("channel-save", "channel-test"):
            action = command.replace("-", ".")
            if args.id:
                params["id"] = args.id
            if command == "channel-save":
                if os.environ.get(args.destination_env):
                    params["destination"] = os.environ[args.destination_env]
                if os.environ.get(args.secret_env):
                    params["secret"] = os.environ[args.secret_env]
            if not args.yes:
                result = {"needsExecution": True, "action": action,
                          "note": "保存渠道会修改通知配置；测试会向指定目标发送消息。用户授权后传 --yes。"}
            else:
                result = api.request(PRODUCT, {"action": action, **params}, uuid.uuid4().hex)[0]
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        return 0
    except (ValueError, APIError, OSError) as e:
        print(str(e), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
