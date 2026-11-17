"""优稿降 AI 复检：原文检测 → 改写 → 复检 → 有界重试。Python 3.10+。"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import html
import json
from pathlib import Path
import re
import sys
import time
import uuid

import skill_client as client_tools
from yougao import APIError, Client, private_write

VERSION = "1.0.0"
METRICS = {"ai": "AI 特征", "combined": "AI 特征＋疑似 AI"}
REASONS = {
    "ready": "已预览，尚未执行", "running": "继续当前任务", "awaiting_retry": "未达目标，等待是否再试一次",
    "target_met": "已达到所选检测指标的目标", "no_improvement": "本轮未改善，保留此前效果更好的版本",
    "retry_limit": "已用完约定重试次数", "no_retry": "已完成一次改写与复检，不再重试",
    "unchanged": "改写未产生新的正文，停止重复花费", "budget_limit": "剩余点数预算不足，未开始下一项操作",
    "needs_attention": "原任务需要处理，未创建替代付费任务", "invalid_report": "报告缺失或与正文不匹配，不能据此重试",
    "quality_review": "候选稿需要检查，已暂停后续处理", "finished": "已按要求结束并保留当前最佳版本",
}
TERMINAL = {"target_met", "no_improvement", "retry_limit", "no_retry", "unchanged", "budget_limit", "finished", "quality_review", "invalid_report"}


def stamp():
    return datetime.now(timezone.utc).isoformat()


def expired(value):
    # Go emits RFC3339Nano; Python 3.10 accepts only microseconds.
    text = re.sub(r"(\.\d{6})\d+", r"\1", value).replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(text)
        if dt.tzinfo is None:
            raise ValueError()
        return dt <= datetime.now(timezone.utc)
    except ValueError:
        raise APIError("计划到期时间无法识别，先核对原计划，不开始消费。") from None


def money(value):
    try:
        number = Decimal(str(value))
        if isinstance(value, bool) or not number.is_finite() or number < 0 or number != number.to_integral_value():
            raise InvalidOperation()
        return int(number)
    except (InvalidOperation, ValueError):
        raise APIError("费用尚未核清，保留原任务，不开始下一笔消费。") from None


def cap_units(value):
    if value is None:
        return None
    try:
        amount = Decimal(str(value)) * 10000
        return money(amount)
    except (InvalidOperation, APIError):
        raise APIError("点数上限须为非负数，最多四位小数；不填表示不另设总点数上限。") from None


def text_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical(text):
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def numbers(text):
    body = re.sub(r"(?m)^\s*\d+[.)、]\s*", "", text)
    return Counter(re.findall(r"\d+(?:[.,]\d+)*(?:%|％)?", body))


def policy(target=20, metric="ai", retries=2, mode="ask", max_points=None):
    try:
        value = Decimal(str(target))
        if not value.is_finite() or not 0 <= value <= 100:
            raise ValueError()
    except (InvalidOperation, ValueError):
        raise APIError("目标比例应在 0–100 之间。") from None
    if metric not in METRICS or mode not in ("ask", "auto", "never") or type(retries) is not int or not 0 <= retries <= 5:
        raise APIError("重试模式为 ask/auto/never，最多额外重试 0–5 次。")
    return {"target": str(value), "metric": metric, "maxRetries": retries, "retryMode": mode, "maxMicros": cap_units(max_points)}


def save(folder, task):
    private_write(folder / "refine.json", task)


def request_for(text, feature, remaining=None):
    request = {"input": {"text": text}, "params": {}}
    if remaining is not None:
        request["budget"] = {"maxChargeMicros": str(remaining)}
    return request


def initialize(client, folder, source, settings):
    if not isinstance(source, str) or not 100 <= len(canonical(source)) <= 10000:
        raise APIError("综合处理支持 100–10000 字完整正文，不会截断或补字。")
    if re.search(r"!\[[^\]]*\]\(|<\s*(?:img|table|video|audio|iframe)\b", source, re.I):
        raise APIError("本技能处理正文文本；图文稿请在优稿保留图片与排版，不会静默丢弃后重建。")
    identity = client_tools.fingerprint({"original": source, "policy": settings})
    path = folder / "refine.json"
    if path.exists():
        task = client_tools.read_json(path)
        client_tools.bind(task, client)
        if task["inputHash"] != identity:
            raise APIError("目录已有不同任务，请保留原目录；新文章使用新目录。")
        return task
    # Quotes only. No paid operation occurs during preparation.
    quotes = {}
    for feature in ("detection", "rewriting"):
        preview = client.call(feature, "preview", request_for(canonical(source), feature))
        if not preview.get("id") or not isinstance(preview.get("runnable"), bool):
            raise APIError("未取得完整费用预览，不开始执行。")
        quotes[feature] = {"micros": money(preview.get("totalMicros")), "runnable": preview["runnable"], "issues": preview.get("issues") or []}
    task = {"version": VERSION, "base": client.base, "credentialHash": client_tools.fingerprint(client.key),
            "inputHash": identity, "original": source, "policy": settings, "quotes": quotes, "createdAt": stamp(),
            "status": "ready", "next": {"round": 0, "feature": "detection", "text": canonical(source)},
            "operations": [], "versions": [], "retryApprovals": [], "bestRound": None}
    save(folder, task)
    return task


def inspect_report(run, expected):
    state = run.get("state") or {}
    current = state.get("text")
    if not isinstance(current, str) or canonical(current) != canonical(expected) or state.get("textHash") != text_hash(current):
        raise APIError("送检正文与本次版本不匹配。")
    matches = [r for r in state.get("reports") or [] if isinstance(r, dict) and r.get("text") == current and r.get("textHash") == text_hash(current)]
    if len(matches) != 1:
        raise APIError("缺少唯一对应本次正文的检测报告。")
    report = matches[0]
    data = report.get("result")
    for _ in range(5):
        if not isinstance(data, dict) or "labels_ratio" in data:
            break
        data = data.get("data")
    raw = data.get("labels_ratio") if isinstance(data, dict) else None
    try:
        if not isinstance(raw, dict) or any(type(raw.get(str(i))) not in (int, float) for i in range(3)):
            raise ValueError()
        values = [Decimal(str(raw[str(i)])) for i in range(3)]
        if any(not n.is_finite() or n < 0 for n in values):
            raise ValueError()
        if max(values) <= 1 and abs(sum(values) - 1) <= Decimal("0.001"):
            values = [n * 100 for n in values]
        elif max(values) > 100 or abs(sum(values) - 100) > Decimal("0.1"):
            raise ValueError()
    except (ValueError, InvalidOperation):
        raise APIError("检测三类占比不完整或无效，不能当作 0%。") from None
    return {"human": str(values[0]), "ai": str(values[1]), "suspected": str(values[2]), "combined": str(values[1] + values[2])}, report


def rank(version, settings):
    rates = version["rates"]
    # Equal primary score: prefer lower secondary score; a complete tie keeps the earlier draft.
    secondary = "combined" if settings["metric"] == "ai" else "ai"
    return Decimal(rates[settings["metric"]]), Decimal(rates[secondary])


def total(task):
    return sum(op["chargedMicros"] for op in task["operations"])


def summary(task, folder):
    settings = task["policy"]
    best = next((v for v in task["versions"] if v["round"] == task["bestRound"]), None)
    detection = task["quotes"]["detection"]["micros"]
    rewrite = task["quotes"]["rewriting"]["micros"]
    ret = {"status": task["status"], "message": REASONS.get(task["status"], task["status"]), "taskDir": str(folder),
           "target": settings["target"], "metric": METRICS[settings["metric"]], "retryMode": settings["retryMode"],
           "maxRetries": settings["maxRetries"], "maxPoints": client_tools.points(settings["maxMicros"]) if settings["maxMicros"] is not None else None,
           "firstPassEstimatePoints": client_tools.points(detection * 2 + rewrite),
           "retryEstimatePoints": client_tools.points(detection + rewrite), "settledPoints": client_tools.points(total(task)),
           "estimateNote": "按当前原文预览；每次执行重新按实际正文报价，总预算包含所有检测和改写。",
           "bestRound": task["bestRound"], "bestRates": best["rates"] if best else None,
           "targetMet": bool(best and rank(best, settings)[0] <= Decimal(settings["target"])),
           "attempts": [{k: v[k] for k in ("round", "rates", "editUrl", "runUrl")} for v in task["versions"]]}
    ret["runnable"] = all(q["runnable"] for q in task["quotes"].values())
    ret["issues"] = [issue for q in task["quotes"].values() for issue in q["issues"]]
    if task.get("detail"):
        ret["detail"] = task["detail"]
    if task.get("pending"):
        ret["pending"] = {k: task["pending"].get(k) for k in ("round", "feature", "runId", "status", "reservedPoints", "chargedPoints")}
        ret["billingNote"] = "已结算合计不含当前待核对操作；不能把未提供的费用视为零。"
    if task["status"] == "awaiting_retry":
        ret["nextRound"] = task["next"]["round"]
        ret["question"] = f"尚未达到{METRICS[settings['metric']]} ≤ {settings['target']}%。是否再改写并复检一次？可选再试一次或保留当前稿。"
    return ret


def consume(folder, task, operation, run):
    """Commit settled charge and next state together; replaying a receipt is harmless."""
    charged, reserved = money(run.get("chargedMicros")), money(run.get("reservedMicros"))
    if reserved:
        raise APIError("当前操作仍有预留点数，先核对原结果。")
    stage = task["next"]
    task["operations"].append({"folder": operation.name, "feature": stage["feature"], "round": stage["round"],
                               "runId": run["id"], "chargedMicros": charged})
    task.pop("pending", None)
    if stage["feature"] == "rewriting":
        body = (run.get("state") or {}).get("text")
        if not isinstance(body, str) or not 100 <= len(canonical(body)) <= 10000:
            task.update(status="quality_review", detail="改写结果缺失或超出完整检测范围；候选在原记录，未截断送检。")
        elif any(canonical(body) == canonical(v["text"]) for v in task["versions"]):
            task.update(status="unchanged")
        else:
            task["candidate"] = {"round": stage["round"], "text": body, "draftId": run["state"].get("draftId"), "runId": run["id"]}
            if numbers(body) != numbers(task["original"]):
                task.update(status="quality_review", detail="候选稿中的数字与原文不同，需核对事实后再处理；未将低分置于内容准确性之前。")
            else:
                task["next"] = {"round": stage["round"], "feature": "detection", "text": body}
        return
    try:
        rates, report = inspect_report(run, stage["text"])
    except APIError as exc:
        task.update(status="invalid_report", detail=str(exc))
        return
    site = task["base"].removesuffix("/api/v1")
    candidate = task.get("candidate") if stage["round"] else None
    draft = candidate.get("draftId") if candidate else None
    version = {"round": stage["round"], "text": report["text"], "rates": rates, "report": report,
               "editUrl": site + "/app/editor/" + client_tools.urllib_id(draft) if draft else None,
               "runUrl": site + "/app/workflows/runs/" + client_tools.urllib_id(run["id"])}
    prior = next((v for v in task["versions"] if v["round"] == task["bestRound"]), None)
    task["versions"].append(version)
    improved = prior is None or rank(version, task["policy"]) < rank(prior, task["policy"])
    if improved:
        task["bestRound"] = version["round"]
    best = version if improved else prior
    task.pop("candidate", None)
    settings = task["policy"]
    if rank(best, settings)[0] <= Decimal(settings["target"]):
        task["status"] = "target_met"
    elif stage["round"] and not improved:
        task["status"] = "no_improvement"
    elif stage["round"] >= settings["maxRetries"] + 1:
        task["status"] = "retry_limit"
    elif stage["round"] and settings["retryMode"] == "never":
        task["status"] = "no_retry"
    else:
        task["next"] = {"round": stage["round"] + 1, "feature": "rewriting", "text": best["text"]}
        task["status"] = "awaiting_retry" if stage["round"] and settings["retryMode"] == "ask" else "running"


def advance(client, folder, task, approved=False, retry_round=None, timeout=55):
    client_tools.bind(task, client)
    if time.time() < task.get("notBefore", 0):
        return summary(task, folder)
    if task["status"] in TERMINAL:
        return summary(task, folder)
    if not task.get("approvedAt"):
        if not approved:
            raise APIError("先核对点数与重试范围；已有用户授权时用 run --approved，不需要逐步重复确认。")
        task["approvedAt"] = stamp()
    if retry_round is not None:
        if retry_round not in task["retryApprovals"]:
            if task["status"] != "awaiting_retry" or retry_round != task["next"]["round"]:
                raise APIError("只能批准当前等待的轮次，请先查看 status。")
            task["retryApprovals"].append(retry_round)
            task["status"] = "running"
    if task["status"] == "awaiting_retry":
        return summary(task, folder)
    task["status"] = "running"
    task.pop("detail", None)
    save(folder, task)
    deadline = time.monotonic() + timeout
    while task["status"] == "running" and time.monotonic() < deadline:
        stage = task["next"]
        op_folder = folder / f"{stage['round']:02}-{stage['feature']}"
        try:
            # Persist active work before any network side effect. A crash resumes this exact folder.
            task.setdefault("pending", {"round": stage["round"], "feature": stage["feature"]})
            save(folder, task)
            with client_tools.task_lock(op_folder):
                marker = op_folder / "task.json"
                if marker.exists():
                    op = client_tools.read_json(marker)
                    client_tools.bind(op, client)
                else:
                    remaining = None if task["policy"]["maxMicros"] is None else max(0, task["policy"]["maxMicros"] - total(task))
                    op = client_tools.prepare(client, stage["feature"], request_for(stage["text"], stage["feature"], remaining), op_folder)
                plan = op["plan"]
                cap = task["policy"]["maxMicros"]
                if not op.get("startAttemptedAt"):
                    if cap is not None and total(task) + money(plan["totalMicros"]) > cap:
                        task.update(status="budget_limit")
                        task.pop("pending", None)
                        break
                    if not plan["runnable"]:
                        raise APIError("当前计划不可执行：" + "；".join(plan.get("issues") or []))
                    # Expired but never submitted: a fresh preview is safe. Never replace an attempted plan.
                    expires = plan.get("expiresAt")
                    if expires and expired(expires):
                        task.update(status="needs_attention", detail="未提交的计划已过期，使用 reprice 重新报价；原目录保留。")
                        break
                # Successful settled receipts survive a crash after export but before parent commit.
                receipt = op_folder / "result.json"
                run = client_tools.read_json(receipt) if receipt.exists() else None
                settled = run and run.get("status") == "succeeded" and str(run.get("reservedMicros")) == "0" and "chargedMicros" in run
                if not settled:
                    client_tools.execute(client, op, op_folder, approved=True, timeout=max(1, min(30, int(deadline - time.monotonic()))), recover=bool(op.get("startAttemptedAt")))
                    run = client_tools.read_json(receipt)
                if run.get("id") != op.get("runId"):
                    raise APIError("原运行编号不匹配，请核对任务文件，不能继续扣点。")
                task["pending"].update(runId=run.get("id"), status=run.get("status"),
                    chargedPoints=client_tools.points(run["chargedMicros"]) if "chargedMicros" in run else None,
                    reservedPoints=client_tools.points(run["reservedMicros"]) if "reservedMicros" in run else None)
                if run.get("status") in ("queued", "running"):
                    break
                if run.get("status") != "succeeded":
                    raise APIError("原运行状态：" + str(run.get("status")) + "。" + str(run.get("error", "请查看原任务，不新建付费操作。")))
                consume(folder, task, op_folder, run)
                save(folder, task)
        except APIError as exc:
            marker = op_folder / "task.json"
            if task.get("pending") is not None and marker.exists():
                task["pending"]["runId"] = client_tools.read_json(marker).get("runId")
            task.update(status="needs_attention", detail=str(exc), retryAfter=exc.retry_after)
            if exc.retry_after:
                task["notBefore"] = time.time() + exc.retry_after
            break
    save(folder, task)
    return summary(task, folder)


def reprice(client, folder, task):
    client_tools.bind(task, client)
    if task["status"] != "needs_attention" or not task.get("pending"):
        raise APIError("仅未提交的待处理计划可重新报价。")
    stage = task["next"]
    op_folder = folder / f"{stage['round']:02}-{stage['feature']}"
    with client_tools.task_lock(op_folder):
        op = client_tools.read_json(op_folder / "task.json")
        if op.get("startAttemptedAt") or op.get("runId"):
            raise APIError("此计划曾尝试提交，只能 resume 查询原任务，不能重新报价。")
        request = json.loads(json.dumps(op["request"]))
        if op["feature"] == "rewriting":
            request["input"]["document"] = client_tools.plain_document(request["input"].pop("text"))
        new = client.call(op["feature"], "preview", request)
        if not new.get("id") or not isinstance(new.get("runnable"), bool):
            raise APIError("未取得完整新报价。")
        money(new.get("totalMicros"))
        op["plan"] = new
        private_write(op_folder / "task.json", op)
    task["status"] = "ready"
    task.pop("approvedAt", None)
    task.pop("pending", None)
    task.pop("detail", None)
    save(folder, task)
    return {**summary(task, folder), "newEstimatePoints": client_tools.points(new["totalMicros"])}


def deliver(folder, task):
    dest = folder / ("delivery-" + uuid.uuid4().hex[:10])
    dest.mkdir(mode=0o700)
    result = summary(task, folder)
    files = {}
    def write(name, body):
        client_tools.write_new(dest / name, body)
        files[name] = str(dest / name)
    write("original.md", task["original"])
    best = next((v for v in task["versions"] if v["round"] == task["bestRound"]), None)
    if best:
        write("article.md", task["original"] if best["round"] == 0 else best["text"])
        result["editUrl"], result["runUrl"] = best["editUrl"], best["runUrl"]
    if task.get("candidate"):
        write("candidate-unverified.md", task["candidate"]["text"])
    lines = ["优稿 · 降 AI 改写与复检", result["message"],
             f"目标：{result['metric']} ≤ {result['target']}%", "已核清扣点：" + result["settledPoints"],
             "检测仅供分析参考，不证明作者身份或原创性；AI 特征达标不代表疑似 AI 已消失。"]
    if result.get("pending"):
        lines.extend([result["billingNote"], json.dumps(result["pending"], ensure_ascii=False)])
    if result.get("detail"):
        lines.append(result["detail"])
    rows = []
    for version in task["versions"]:
        label = "原文" if version["round"] == 0 else f"第 {version['round']} 轮"
        rates = version["rates"]
        values = [label] + [f"{Decimal(rates[k]):.2f}%" for k in ("human", "suspected", "ai")]
        lines.append(" / ".join(values) + ("（当前最佳）" if version == best else ""))
        rows.append("<tr>" + "".join("<td>" + html.escape(v) + "</td>" for v in values) + "</tr>")
        write(f"round-{version['round']}-detection.txt", client_tools.detection_text(version["report"], text_hash(version["text"])))
        if version["round"]:
            write(f"round-{version['round']}.md", version["text"])
    if result.get("question"):
        lines.append(result["question"])
    write("report.txt", "\n".join(lines))
    write("result.json", json.dumps(result, ensure_ascii=False, indent=2))
    body = "<h1>降 AI 改写与复检</h1><section><pre>" + html.escape("\n".join(lines[:5])) + "</pre></section>"
    body += '<section style="overflow-x:auto"><table style="width:100%;text-align:left"><thead><tr><th>版本</th><th>人工特征</th><th>疑似 AI</th><th>AI 特征</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table></section>"
    body += "<section><h2>交付文件</h2>" + "<br>".join('<a href="' + name + '">' + name + "</a>" for name in files) + "</section>"
    if best:
        body += '<section><h2>当前最佳版本' + (' · 原文' if best['round'] == 0 else f" · 第 {best['round']} 轮") + '</h2><a href="' + html.escape(best["editUrl"] or best["runUrl"], quote=True) + '">在优稿继续查看</a><pre>' + html.escape(best["text"]) + "</pre></section>"
    if task.get("detail") or result.get("question"):
        body += "<section><pre>" + html.escape(task.get("detail") or result["question"]) + "</pre></section>"
    write("index.html", client_tools.page("优稿 · 降 AI 改写与复检", body))
    return {**result, "files": files}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version=VERSION)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prepare", help="只预览费用，保存原文与处理目标")
    p.add_argument("--text-file", required=True)
    p.add_argument("--target", default="20", help="目标百分比，默认 AI 特征不超过20%%")
    p.add_argument("--metric", choices=tuple(METRICS), default="ai")
    p.add_argument("--retry", choices=("ask", "auto", "never"), default="ask")
    p.add_argument("--max-retries", type=int, default=2, help="首次改写之外最多额外重试次数，0–5")
    p.add_argument("--max-points", help="整个流程点数上限；不填不限，0禁止消费")
    parsers = [p]
    for name in ("run", "resume", "retry", "finish", "status", "export", "reprice"):
        p = sub.add_parser(name)
        parsers.append(p)
        if name in ("run", "resume", "retry"):
            p.add_argument("--timeout", type=int, default=55)
        if name == "run":
            p.add_argument("--approved", action="store_true")
        if name == "retry":
            p.add_argument("--round", type=int, required=True, help="status返回的下一轮编号，同一批准可安全重复")
    for p in parsers:
        p.add_argument("--dir", required=True)
    args = parser.parse_args(argv)
    folder = Path(args.dir).resolve()
    if hasattr(args, "timeout") and not 1 <= args.timeout <= 60:
        raise APIError("每次等待 1–60 秒，超时用 resume 接续，不会取消运行。")
    with client_tools.task_lock(folder):
        if args.command == "prepare":
            source = Path(args.text_file).read_text(encoding="utf-8-sig")
            return summary(initialize(Client(), folder, source, policy(args.target, args.metric, args.max_retries, args.retry, args.max_points)), folder)
        task = client_tools.read_json(folder / "refine.json")
        if args.command == "status":
            return summary(task, folder)
        if args.command == "finish":
            if task["status"] != "awaiting_retry":
                raise APIError("当前不是等待重试状态；进行中的任务用 resume 查询，不能当成已取消。")
            task["status"] = "finished"
            save(folder, task)
        elif args.command == "reprice":
            return reprice(Client(), folder, task)
        elif args.command != "export":
            advance(Client(), folder, task, getattr(args, "approved", False), getattr(args, "round", None), args.timeout)
        return deliver(folder, task)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    try:
        result = main()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if result["status"] not in TERMINAL | {"ready"}:
            sys.exit(2)
    except (APIError, ValueError, OSError, KeyError, TypeError) as exc:
        print(json.dumps({"error": str(exc) if isinstance(exc, APIError) else "输入或任务记录无法读取，请保留原目录并检查。",
                          "retryAfter": getattr(exc, "retry_after", 0)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
