"""优稿技能助手：一次连接、预览费用、执行接续、离线交付。Python 3.10+ 标准库。"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import getpass
import hashlib
import html
import json
import math
import os
from pathlib import Path
import sys
import uuid

from yougao import APIError, Client, VERSION, DEFAULT_BASE, KEY_URL, config_path, load_connection, private_write, save_connection
from documents import plain_document, markdown_document

FEATURES = ("formatting", "detection", "rewriting", "generation", "workflow", "publishing")
LABELS = {"succeeded": "已完成", "partial": "部分完成", "queued": "排队中", "running": "处理中",
          "awaiting_review": "等待审阅", "awaiting_input": "等待补充内容", "awaiting_service": "等待服务恢复",
          "needs_reconciliation": "结果待核对", "failed": "未完成", "cancelled": "已取消",
          "waiting_device": "等待本机客户端", "waiting_input": "需要处理", "draft_saved": "已存草稿",
          "submitted": "已提交，公开状态以平台为准", "needs_review": "发布结果待核对", "editing": "平台编辑中"}


def read_json(path: Path):
    if path.stat().st_size > 20 * 1024 * 1024:
        raise APIError("文件过大，请使用本次任务的 JSON 记录。")
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
        if not isinstance(value, dict):
            raise ValueError()
        return value
    except (ValueError, UnicodeError):
        raise APIError("JSON 文件格式不正确，需要 UTF-8 对象。") from None


def points(value) -> str:
    try:
        number = Decimal(str(value)) / 10000
        if not number.is_finite() or number < 0:
            raise InvalidOperation()
        return format(number, "f").rstrip("0").rstrip(".") if "." in format(number, "f") else str(number)
    except InvalidOperation:
        raise APIError("服务未返回有效费用，请查询原任务核对。") from None


def fingerprint(value) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


@contextmanager
def task_lock(folder: Path):
    folder.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (folder / ".lock").open("a+b") as stream:
        if stream.tell() == 0:
            stream.write(b"0")
            stream.flush()
        stream.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            raise APIError("该任务正在被另一个进程处理，请稍后查询原任务。") from None
        try:
            yield
        finally:
            if os.name == "nt":
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream, fcntl.LOCK_UN)


def bind(task, client):
    if task["base"] != client.base or task["credentialHash"] != fingerprint(client.key):
        raise APIError("任务属于另一连接，请恢复原站点和密钥再接续；不要换账户重跑。")


def prepare(client, feature, request, folder):
    request = dict(request)
    if request.pop("action", "preview") != "preview":
        raise APIError("prepare 只接受预览参数，不能执行其他 action。")
    marker = folder / "task.json"
    if marker.exists():
        task = read_json(marker)
        bind(task, client)
        if task["feature"] != feature or task["inputHash"] != fingerprint(request):
            raise APIError("此目录已有不同任务。新内容使用新目录；重试原任务用 recover。")
        return task
    if feature not in FEATURES:
        raise APIError("不支持的功能。")
    api_request = json.loads(json.dumps(request))
    # Passing a document lets the service canonicalize boundary newlines before
    # paragraph alignment. Plain input ending in a newline otherwise differs
    # from its generated document and fails AFTER a paid rewrite.
    input_data = api_request.get("input", {})
    rewrites = feature == "rewriting" or any(s.get("tool") == "rewriting" and s.get("enabled") for s in api_request.get("spec", {}).get("steps", []))
    if rewrites and input_data.get("text") and not input_data.get("document") and not input_data.get("manuscriptId"):
        input_data["document"] = plain_document(input_data.pop("text"))
    plan = client.call(feature, "preview", api_request)
    if feature == "publishing" and isinstance(plan, dict) and plan.get("id") and plan.get("destinations"):
        # The publishing API validates on preview and has no runnable field.
        plan = {**plan, "runnable": True, "issues": []}
    if not isinstance(plan, dict) or not plan.get("id") or not isinstance(plan.get("runnable"), bool):
        raise APIError("未取得完整计划，不会开始执行。")
    points(plan.get("totalMicros"))
    task = {"version": 1, "base": client.base, "credentialHash": fingerprint(client.key),
            "feature": feature, "inputHash": fingerprint(request), "request": request, "plan": plan,
            "requestId": str(uuid.uuid4()), "createdAt": datetime.now(timezone.utc).isoformat()}
    private_write(marker, task)
    return task


def task_summary(task, folder):
    plan = task["plan"]
    return {"taskDir": str(folder), "feature": task["feature"], "planId": plan["id"],
            "runId": task.get("runId"), "runnable": plan["runnable"], "issues": plan.get("issues") or [],
            "estimatedPoints": points(plan["totalMicros"]), "quotaUnits": plan.get("quotaUnits", 0),
            "title": plan.get("title") or plan.get("input", {}).get("title"),
            "mode": plan.get("mode"), "destinations": plan.get("destinations", []),
            "warnings": plan.get("warnings", []), "steps": plan.get("executionSteps") or plan.get("spec", {}).get("steps", []),
            "settings": plan.get("spec", {}).get("settings"),
            "expiresAt": plan.get("expiresAt"), "message": "费用为预留上限，实际按结果结算。预览未开始执行。"}


def execute(client, task, folder, approved=False, timeout=60, recover=False):
    bind(task, client)
    if not task.get("runId"):
        if recover and not task.get("startAttemptedAt"):
            raise APIError("此任务尚未提交，recover 不会替你开始。确认费用后使用 execute。")
        plan = task["plan"]
        if not plan["runnable"]:
            raise APIError("计划不可执行：" + "；".join(plan.get("issues") or []))
        # --approved records user intent once; it is not an instruction to ask again each time.
        paid = Decimal(points(plan["totalMicros"])) > 0 or int(plan.get("quotaUnits", 0)) > 0
        delivery = (plan.get("spec", {}).get("settings", {}).get("delivery") or {})
        external = task["feature"] == "publishing" or delivery.get("mode") in ("draft", "publish")
        always = (plan.get("spec", {}).get("settings") or {}).get("confirmation") == "always"
        if (paid or external or always) and not (approved or task.get("approvedAt")):
            raise APIError("需要核对本次费用及目标是否在用户已授权范围内；已有授权时加 --approved 继续。")
        if approved:
            task["approvedAt"] = datetime.now(timezone.utc).isoformat()
        task.setdefault("startAttemptedAt", datetime.now(timezone.utc).isoformat())
        private_write(folder / "task.json", task)
        run = client.call(task["feature"], "start", {"planId": plan["id"]}, task["requestId"])
        if not isinstance(run, dict) or not run.get("id"):
            raise APIError("未取得运行编号，保留此目录后使用 recover，不能另建任务。")
        task["runId"] = run["id"]
        private_write(folder / "task.json", task)
        private_write(folder / "result.json", run)
    run = (client.publishing_run(task["runId"]) if task["feature"] == "publishing"
           else client.wait(task["runId"], timeout=timeout, feature=task["feature"]))
    private_write(folder / "result.json", run)
    # Creation success and platform success are separate. This query never submits anything.
    publication = run.get("state", {}).get("publishingRunId")
    if publication:
        try:
            status = client.publishing_run(publication)
            private_write(folder / "publishing.json", status)
        except APIError as exc:
            private_write(folder / "publishing.json", {"id": publication, "queryError": str(exc), "status": "unknown"})
    return export_result(folder, task, run)


def detection_text(report, current_hash):
    data = report.get("result")
    for _ in range(4):
        if not isinstance(data, dict) or "labels_ratio" in data:
            break
        data = data.get("data")
    raw = data.get("labels_ratio") if isinstance(data, dict) else None
    ratios = [raw.get(str(i)) for i in range(3)] if isinstance(raw, dict) else []
    valid = len(ratios) == 3 and all(type(v) in (float, int) and math.isfinite(v) and v >= 0 for v in ratios)
    scale = 0
    if valid:
        if max(ratios) <= 1 and abs(sum(ratios) - 1) <= .001:
            scale = 1
        elif max(ratios) <= 100 and abs(sum(ratios) - 100) <= .1:
            scale = 100
    lines = ["AI 率检测", "送检版本：" + report.get("textHash", "未提供")]
    if current_hash and report.get("textHash") != current_hash:
        lines.append("注意：此报告对应先前正文，当前文章已修改。")
    if scale:
        for label, name in ((0, "人工特征"), (2, "疑似 AI"), (1, "AI 特征")):
            lines.append(f"{name}：{ratios[label] / scale * 100:.2f}%")
    else:
        lines.append("检测占比不完整或格式异常，不能显示分数。原始报告已保存，请查询优稿任务。")
    lines += ["检测是模型分析参考，不证明作者身份或原创性。", "", "送检原文", report.get("text", "")]
    if isinstance(data, dict):
        segments = data.get("segment_labels", data.get("segments", []))
        if isinstance(segments, list):
            labels = {"0": "人工特征", "1": "AI 特征", "2": "疑似 AI"}
            for item in segments:
                if isinstance(item, dict) and isinstance(item.get("text"), str):
                    label = str(item.get("label")).removesuffix(".0")
                    if label in labels:
                        lines.extend(["", labels[label], item["text"]])
    return "\n".join(lines)


def page(title, body):
    return '<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + html.escape(title) + '</title><style>body{margin:0;background:#f5f6f8;color:#202a35;font:16px/1.8 system-ui,"Microsoft YaHei",sans-serif}main{max-width:960px;margin:auto;padding:32px 20px}section{background:white;border:1px solid #e5e7eb;border-radius:10px;padding:24px;margin:20px 0}h1{line-height:1.3}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}a{color:#3158aa}iframe{width:100%;height:640px;border:0}small{color:#626a75}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}.grid section{margin:0;min-width:0}.grid iframe{height:430px}</style><main>' + body + '</main></html>'


def write_new(path, text):
    with path.open("x", encoding="utf-8") as out:
        out.write(text)


def export_result(folder, task=None, run=None):
    # Export is intentionally offline and does not require a configured key.
    task = task or read_json(folder / "task.json")
    run = run or read_json(folder / "result.json")
    dest = folder / ("delivery-" + uuid.uuid4().hex[:10])
    dest.mkdir(mode=0o700)
    state = run.get("state") or {}
    origin = task["base"].removesuffix("/api/v1")
    run_id = urllib_id(run.get("id", task.get("runId", "")))
    url = origin + ("/app/publish?run=" if task["feature"] == "publishing" else "/app/workflows/runs/") + run_id
    edit = origin + "/app/editor/" + urllib_id(state["draftId"]) if state.get("draftId") else None
    status = run.get("status", "unknown")
    if task["feature"] == "publishing":
        statuses = {d.get("status", "unknown") for d in run.get("deliveries") or []}
        status = next(iter(statuses)) if len(statuses) == 1 else "multiple_targets"
    lines = ["优稿 · 任务交付", "状态：" + LABELS.get(status, status), "运行记录：" + url]
    if "chargedMicros" in run:
        lines.extend(["实际扣点：" + points(run["chargedMicros"]), "仍预留：" + points(run.get("reservedMicros", 0))])
    if edit:
        lines.append("继续编辑：" + edit)
    if run.get("error"):
        lines.append("未完成原因：" + str(run["error"]))
    for step in run.get("steps") or []:
        if step.get("error"):
            lines.append(str(step.get("tool", "步骤")) + "：" + str(step["error"]))
    lines.extend(state.get("warnings") or [])
    if state.get("publishingError"):
        lines.append("发布排队受阻：" + str(state["publishingError"]))
    if status != "succeeded" and task["feature"] != "publishing":
        lines.append("以下为本次已有内容，不能视为全部完成。保留任务目录，用 recover 查询原任务。")
    files = {}
    for name, content in (("article.md", state.get("text")), ("article.html", state.get("html")), ("original.md", task.get("request", {}).get("input", {}).get("text") or state.get("sourceText"))):
        if content:
            write_new(dest / name, content)
            files[name] = str(dest / name)
    reports = state.get("reports") or []
    report_sections = []
    for index, report in enumerate(reports, 1):
        detail = detection_text(report, state.get("textHash"))
        name = f"detection-{index}.txt"
        write_new(dest / name, detail)
        files[name] = str(dest / name)
        report_sections.append("<section><pre>" + html.escape(detail) + "</pre></section>")
    publishing = run if task["feature"] == "publishing" else (read_json(folder / "publishing.json") if (folder / "publishing.json").exists() else None)
    if publishing:
        lines.append("发布进度与文章处理状态分别核对：")
        lines.append("以各目标回执为准；已提交不代表已公开。")
        for item in publishing.get("deliveries") or []:
            lines.append(str(item.get("title", item.get("targetId", "目标"))) + "：" + str(item.get("statusLabel", item.get("status", "待核对"))) + "；" + str(item.get("nextStep", "")))
        if publishing.get("queryError"):
            lines.append(publishing["queryError"])
    private_write(dest / "result.json", run)
    files["result.json"] = str(dest / "result.json")
    write_new(dest / "report.txt", "\n".join(lines))
    files["report.txt"] = str(dest / "report.txt")
    body = '<h1>优稿 · 任务交付</h1><section><pre>' + html.escape("\n".join(lines[1:])) + '</pre><a href="' + html.escape(edit or url, quote=True) + '">在优稿继续' + ('编辑' if edit else '查看') + '</a></section>'
    body += '<section><h2>交付文件</h2>' + '<br>'.join('<a href="' + html.escape(name) + '">' + html.escape(name) + '</a>' for name in files) + '</section>'
    body += "".join(report_sections)
    if state.get("html"):
        body += '<section><h2>排版预览</h2><iframe sandbox="" referrerpolicy="no-referrer" srcdoc="' + html.escape(state["html"], quote=True) + '"></iframe></section>'
    elif state.get("text") and not reports:
        body += '<section><h2>文章</h2><pre>' + html.escape(state["text"]) + '</pre></section>'
    write_new(dest / "index.html", page("优稿任务交付", body))
    files["index.html"] = str(dest / "index.html")
    return {"status": status, "statusLabel": LABELS.get(status, status), "runId": run.get("id"),
            "runUrl": url, "editUrl": edit, "chargedPoints": points(run["chargedMicros"]) if "chargedMicros" in run else None,
            "reservedPoints": points(run.get("reservedMicros", 0)), "files": files, "taskDir": str(folder),
            "next": "交付文件及编辑链接。" if status == "succeeded" else "展示真实进度；使用 recover 查询原记录，不能重建任务。"}


def urllib_id(value):
    from urllib.parse import quote
    return quote(str(value), safe="")


def theme_gallery(client, output):
    themes = client.call("formatting", "themes")
    if not isinstance(themes, list) or not themes:
        raise APIError("主题目录未返回，请稍后查询。")
    cards = []
    for theme in themes:
        cards.append('<section><h2>' + html.escape(theme["name"]) + '</h2><small>' + html.escape(theme["id"]) + '</small><p>' + html.escape(theme.get("description", "")) + '</p><iframe sandbox="" referrerpolicy="no-referrer" srcdoc="' + html.escape(theme.get("previewHTML", "<p>此基础主题请在排版后查看。</p>"), quote=True) + '"></iframe></section>')
    output.parent.mkdir(parents=True, exist_ok=True)
    write_new(output, page("优稿主题预览", '<h1>选一套适合文章的版式</h1><p>来自优稿当前主题目录。告诉助手主题名称即可，换主题不会改写正文。</p><div class="grid">' + "".join(cards) + '</div>'))
    return {"output": str(output), "count": len(themes), "themes": [{k: t.get(k) for k in ("id", "name", "category", "description")} for t in themes]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version=VERSION)
    sub = parser.add_subparsers(dest="command", required=True)
    configure = sub.add_parser("configure", help="一次连接，六个技能共用；密钥从标准输入或隐藏输入读取")
    configure.add_argument("--base", default=DEFAULT_BASE)
    configure.add_argument("--key-stdin", action="store_true")
    sub.add_parser("status", help="检查本机是否已配置，不显示密钥，不联网")
    sub.add_parser("check", help="只读验证连接，不执行任务或扣点")
    sub.add_parser("disconnect", help="删除本机共用连接；不会撤销网站上的 Key")
    themes = sub.add_parser("themes", help="生成可浏览的真实主题预览，不扣点")
    themes.add_argument("--output", required=True)
    prep = sub.add_parser("prepare", help="预览输入和费用，保存可恢复的任务；不开始执行")
    prep.add_argument("feature", choices=FEATURES)
    prep.add_argument("--dir", required=True, help="本次任务独立目录；接续必须沿用")
    sources = prep.add_mutually_exclusive_group(required=True)
    sources.add_argument("--file", help="完整 JSON 预览参数，支持保存流程和图文稿件")
    sources.add_argument("--text-file", help="UTF-8 正文，适用于排版/改写/检测")
    sources.add_argument("--topic", help="生成主题")
    prep.add_argument("--title", default="")
    prep.add_argument("--theme", default=None)
    prep.add_argument("--target-chars", type=int, default=None)
    for command in ("execute", "recover", "export"):
        child = sub.add_parser(command, help={"execute": "执行已预览的同一任务并导出成果", "recover": "查询原任务或恢复同一提交，绝不新建任务", "export": "离线重导出已保存结果，无需 Key、不扣点"}[command])
        child.add_argument("--dir", required=True)
        if command != "export":
            child.add_argument("--timeout", type=int, default=60, help="本次最多等待1–600秒，等待结束不取消任务")
        if command == "execute":
            child.add_argument("--approved", action="store_true", help="费用/发布目标在用户已授权范围内")
    args = parser.parse_args(argv)
    if args.command == "configure":
        key = sys.stdin.readline(4098).strip() if args.key_stdin else getpass.getpass("优稿 API Key（隐藏输入）：")
        return save_connection(key, args.base)
    if args.command == "disconnect":
        config_path().unlink(missing_ok=True)
        return {"configured": False, "message": "已移除本机共享连接，环境变量不受影响；撤销密钥请到 " + KEY_URL}
    if args.command == "status":
        try:
            client = Client()
        except APIError as exc:
            return {"configured": False, "message": str(exc), "keyUrl": KEY_URL}
        return {"configured": True, "base": client.base, "message": "已配置，check 可只读验证有效性。"}
    if args.command == "export":
        return export_result(Path(args.dir).resolve())
    if args.command in ("execute", "recover") and not 1 <= args.timeout <= 600:
        raise APIError("等待时间应为1–600秒。")
    if args.command == "prepare":
        if args.file:
            if args.title or args.theme is not None or args.target_chars is not None:
                raise APIError("--file 使用完整参数，不与标题/主题/篇幅快捷参数混用。")
            payload = read_json(Path(args.file))
        else:
            if args.topic and args.feature != "generation":
                raise APIError("主题仅用于文章生成；复杂流程请使用 --file。")
            if args.text_file and args.feature not in ("formatting", "rewriting", "detection"):
                raise APIError("此功能请使用 --file 提供完整参数。")
            payload = {"input": {"title": args.title}, "params": {}}
            if args.text_file:
                text = Path(args.text_file).read_text(encoding="utf-8-sig")
                if not text.strip():
                    raise APIError("正文为空，请先提供文章。")
                if args.feature == "detection" and not 100 <= len(text) <= 10000:
                    raise APIError("AI 率检测支持100–10000字，不会自动截断或补写正文。")
                payload["input"]["text"] = text
                if args.feature == "formatting" and Path(args.text_file).suffix.lower() in (".md", ".markdown"):
                    payload["input"]["document"] = markdown_document(text)
                    del payload["input"]["text"]
            else:
                payload["input"]["brief"] = args.topic
            if args.theme is not None:
                if args.feature != "formatting":
                    raise APIError("主题仅用于排版。")
                payload["params"]["theme"] = args.theme
            if args.target_chars is not None and args.feature != "generation":
                raise APIError("篇幅目标仅用于生成，不会改变原文长度。")
            if args.feature == "generation":
                count = args.target_chars if args.target_chars is not None else 1500
                if not 300 <= count <= 10000:
                    raise APIError("生成篇幅目标为300–10000字。")
                payload["params"]["targetChars"] = count
        client = Client()
        folder = Path(args.dir).resolve()
        with task_lock(folder):
            return task_summary(prepare(client, args.feature, payload, folder), folder)
    client = Client()
    if args.command == "check":
        client.call("workflow", "list")
        return {"connected": True, "base": client.base, "message": "优稿连接正常。具体工具权限及点数在任务预览时检查。"}
    if args.command == "themes":
        return theme_gallery(client, Path(args.output).resolve())
    folder = Path(args.dir).resolve()
    with task_lock(folder):
        return execute(client, read_json(folder / "task.json"), folder, getattr(args, "approved", False), args.timeout, args.command == "recover")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    try:
        result = main()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if result.get("status") and result["status"] != "succeeded":
            sys.exit(2)
    except (APIError, ValueError, OSError, KeyError, TypeError) as exc:
        message = str(exc) if isinstance(exc, APIError) else "本机输入或任务文件无法读取，请检查文件路径与格式，保留原任务目录。"
        print(json.dumps({"error": message, "status": getattr(exc, "status", 0), "retryAfter": getattr(exc, "retry_after", 0)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
