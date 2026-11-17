"""调用内网 exam-ocr 服务，把真题 PDF/图片解析为结构化 Markdown。
用法: python parse_ocr.py <试卷路径> [输出md路径] [--url http://exam-ocr:8000] [--owner 智能体名] [--sync]
服务地址：环境变量 EXAM_OCR_URL 或 --url，默认 http://exam-ocr:8000
（OpenClaw 容器内用 http://exam-ocr:8000；其它 AI 指向 http://<84宿主IP>:8000）

排队机制（v0.4.0）：
- 默认走异步接口 /parse-async + 轮询 /task/{id}，多人并发时按用户公平轮转，不会阻塞。
- --owner 参数用于标识调用方（用户/智能体），参与公平轮转排队。
- 加 --sync 可退回同步 /parse（兼容旧行为，单文件场景够用）。

仅用 Python 标准库（urllib），无第三方依赖，任何环境可直接运行。
"""
import sys, os, json, argparse, time, uuid, urllib.request, urllib.parse, urllib.error


def _post_file(url, path, fname, owner=None, sync=False, timeout=120):
    """上传文件，返回 (status, json)"""
    boundary = uuid.uuid4().hex
    with open(path, "rb") as f:
        data = f.read()
    body = (f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{fname}"\r\n'
            f"Content-Type: application/octet-stream\r\n\r\n").encode() + data + f"\r\n--{boundary}--\r\n".encode()
    req_url = f"{url}/parse" if sync else f"{url}/parse-async"
    if owner and not sync:
        req_url += "?" + urllib.parse.urlencode({"owner": owner})
    req = urllib.request.Request(
        req_url, data=body, method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            detail = json.loads(e.read().decode("utf-8"))
        except Exception:
            detail = {}
        return e.code, detail


def _get_json(url, timeout=30):
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _wait_task(url, task_id, timeout=900, poll=1.0):
    """轮询任务直到 done/failed，返回结果 dict"""
    deadline = time.time() + timeout
    while time.time() < deadline:
        st = _get_json(f"{url}/task/{task_id}")
        if st["status"] == "done":
            return st["result"]
        if st["status"] == "failed":
            raise RuntimeError(f"OCR 任务失败: {st.get('error')}")
        time.sleep(poll)
    raise TimeoutError(f"OCR 任务超时 ({timeout}s): {task_id}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="真题 PDF/图片路径")
    ap.add_argument("out", nargs="?", default=None, help="输出 markdown 路径")
    ap.add_argument("--url", default=os.environ.get("EXAM_OCR_URL", "http://exam-ocr:8000"))
    ap.add_argument("--owner", default=os.environ.get("EXAM_OCR_OWNER", "openclaw"), help="调用方标识（参与公平轮转）")
    ap.add_argument("--sync", action="store_true", help="用同步 /parse 接口（旧行为）")
    a = ap.parse_args()

    if not os.path.exists(a.path):
        raise SystemExit(f"文件不存在: {a.path}")

    fname = os.path.basename(a.path)
    status, resp = _post_file(a.url, a.path, fname, owner=a.owner, sync=a.sync)

    if a.sync:
        if status != 200:
            raise SystemExit(f"OCR 失败: HTTP {status} {resp}")
        data = resp
    else:
        if status == 429:
            raise SystemExit(f"[排队] {resp.get('detail', '队列已满，请稍后重试')}")
        if status != 200:
            raise SystemExit(f"提交失败: HTTP {status} {resp}")
        task_id = resp["task_id"]
        print(json.dumps({"task_id": task_id, "status": "queued"}, ensure_ascii=False), flush=True)
        data = _wait_task(a.url, task_id)

    md = data.get("markdown", "")
    out = a.out or (a.path + ".ocr.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(md)
    print(json.dumps(
        {"ok": True, "pages": data.get("pages"), "markdown_path": out, "markdown_len": len(md)},
        ensure_ascii=False,
    ))


if __name__ == "__main__":
    main()
