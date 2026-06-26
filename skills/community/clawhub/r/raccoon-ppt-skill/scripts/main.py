#!/usr/bin/env python3

import argparse
from datetime import datetime, timezone
import fcntl
import json
import os
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, Optional
from urllib import error, request


class APIError(Exception):
    def __init__(self, message: str, code: Optional[int] = None):
        super().__init__(message)
        self.message = message
        self.code = code


FINAL_STATUSES = {"succeeded", "failed", "canceled"}
PENDING_STATUSES = {"queued", "running", "waiting_user_input"}
DEFAULT_REGISTRY_PATH = "./output/job_registry.json"
DEFAULT_INITIAL_WAIT = 0
DEFAULT_POLL_INTERVAL = 10
DEFAULT_SHORT_MAX_POLLS = 0
DEFAULT_BLOCK_MAX_POLLS = 180


CATEGORY_OPTIONS = {
    "role": [
        "企业管理者（CEO/总监/经理）",
        "学生",
        "研究人员",
        "销售",
        "市场",
        "营销",
        "产品经理",
        "项目经理",
        "教师",
        "培训师",
        "财务",
        "会计",
        "行政",
        "人力资源",
    ],
    "scene": [
        "工作汇报",
        "市场调研",
        "培训教学",
        "学术演讲",
        "商业提案",
        "活动策划",
    ],
    "audience": [
        "公司内部（上级/同事/下属）",
        "外部客户",
        "投资人",
        "学生",
        "大众群体",
        "专业人士",
    ],
}


CATEGORY_ALIASES = {
    "role": {
        "老板": "企业管理者（CEO/总监/经理）",
        "高管": "企业管理者（CEO/总监/经理）",
        "总监": "企业管理者（CEO/总监/经理）",
        "经理": "企业管理者（CEO/总监/经理）",
        "主管": "企业管理者（CEO/总监/经理）",
        "创业者": "企业管理者（CEO/总监/经理）",
        "创始人": "企业管理者（CEO/总监/经理）",
        "联合创始人": "企业管理者（CEO/总监/经理）",
        "学生": "学生",
        "博士": "研究人员",
        "研究员": "研究人员",
        "科研": "研究人员",
        "学者": "研究人员",
        "销售": "销售",
        "商务": "销售",
        "市场": "市场",
        "市场运营": "市场",
        "营销": "营销",
        "运营": "营销",
        "增长": "营销",
        "产品": "产品经理",
        "产品负责人": "产品经理",
        "项目": "项目经理",
        "项目负责人": "项目经理",
        "老师": "教师",
        "讲师": "教师",
        "授课": "教师",
        "培训": "培训师",
        "教练": "培训师",
        "财务": "财务",
        "finance": "财务",
        "会计": "会计",
        "出纳": "会计",
        "行政": "行政",
        "助理": "行政",
        "hr": "人力资源",
        "hrbp": "人力资源",
        "招聘": "人力资源",
        "人力": "人力资源",
    },
    "scene": {
        "汇报": "工作汇报",
        "复盘": "工作汇报",
        "总结": "工作汇报",
        "周报": "工作汇报",
        "月报": "工作汇报",
        "季度": "工作汇报",
        "年终": "工作汇报",
        "调研": "市场调研",
        "竞品": "市场调研",
        "洞察": "市场调研",
        "分析": "市场调研",
        "培训": "培训教学",
        "内训": "培训教学",
        "课程": "培训教学",
        "workshop": "培训教学",
        "教学": "培训教学",
        "学术": "学术演讲",
        "答辩": "学术演讲",
        "论文": "学术演讲",
        "研究汇报": "学术演讲",
        "路演": "商业提案",
        "pitch": "商业提案",
        "提案": "商业提案",
        "融资": "商业提案",
        "客户方案": "商业提案",
        "活动": "活动策划",
        "发布会": "活动策划",
        "沙龙": "活动策划",
        "峰会": "活动策划",
        "策划": "活动策划",
    },
    "audience": {
        "内部": "公司内部（上级/同事/下属）",
        "上级": "公司内部（上级/同事/下属）",
        "同事": "公司内部（上级/同事/下属）",
        "团队": "公司内部（上级/同事/下属）",
        "员工": "公司内部（上级/同事/下属）",
        "客户": "外部客户",
        "甲方": "外部客户",
        "合作伙伴": "外部客户",
        "渠道": "外部客户",
        "投资人": "投资人",
        "投资机构": "投资人",
        "vc": "投资人",
        "学生": "学生",
        "学员": "学生",
        "本科生": "学生",
        "研究生": "学生",
        "大众": "大众群体",
        "公众": "大众群体",
        "小白": "大众群体",
        "新手": "大众群体",
        "专家": "专业人士",
        "同行": "专业人士",
        "从业者": "专业人士",
        "专业": "专业人士",
    },
}


def stderr(msg: str) -> None:
    print(msg, file=sys.stderr)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_category(kind: str, value: str) -> Dict[str, str]:
    """简化的分类归一化：优先使用稳定枚举，否则直接使用用户输入"""
    raw = (value or "").strip()
    if not raw:
        raise APIError(f"{kind} 不能为空")

    # 服务端不做强校验，但建议保持简短
    if len(raw) > 20:
        raise APIError(f"{kind} 建议不超过 20 个字符，当前为 {len(raw)} 个字符")

    options = CATEGORY_OPTIONS[kind]

    # 精确匹配稳定枚举
    if raw in options:
        return {"value": raw, "source": "exact"}

    # 简单 alias 映射（仅精确匹配）
    aliases = CATEGORY_ALIASES[kind]
    if raw in aliases:
        return {"value": aliases[raw], "source": "alias"}

    # 直接使用用户输入
    return {"value": raw, "source": "passthrough"}



class PPTClient:
    REQUEST_TIMEOUT = 180

    def __init__(self, host: Optional[str] = None, token: Optional[str] = None):
        self.host = (host or os.environ.get("RACCOON_API_HOST", "https://xiaohuanxiong.com")).rstrip("/")
        self.token = token or os.environ.get("RACCOON_API_TOKEN", "")
        if not self.host:
            raise APIError("未设置 RACCOON_API_HOST")
        if not self.token:
            raise APIError("未设置 RACCOON_API_TOKEN")

    @property
    def base_url(self) -> str:
        return f"{self.host}/api/open/office/v2"

    def _request(self, method: str, path: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        body = None
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }
        if payload is not None:
            body = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"

        req = request.Request(url, data=body, headers=headers, method=method)
        try:
            with request.urlopen(req, timeout=self.REQUEST_TIMEOUT) as resp:
                raw = resp.read().decode("utf-8")
        except TimeoutError as exc:
            raise APIError(f"请求超时，请检查网络连接或稍后重试") from exc
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            parsed_code = None
            parsed_message = detail
            try:
                body = json.loads(detail)
                parsed_code = body.get("code")
                parsed_message = body.get("message") or detail
            except json.JSONDecodeError:
                pass

            if exc.code in (502, 503, 504):
                raise APIError(f"服务暂时不可用 (HTTP {exc.code})，请稍后重试", code=parsed_code) from exc
            raise APIError(f"HTTP {exc.code}: {parsed_message}", code=parsed_code) from exc
        except error.URLError as exc:
            raise APIError(f"请求失败: {exc}") from exc

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise APIError(f"响应不是合法 JSON: {raw}") from exc

        if data.get("code") != 0:
            code = data.get("code")
            message = data.get("message") or "unknown error"

            if code == 600020:
                raise APIError("当前有多个 PPT 任务正在执行，请稍后再试", code=code)
            elif code == 600021:
                raise APIError("任务当前不可回复，请先查看最新状态", code=code)

            raise APIError(message, code=code)
        return data.get("data", {})

    def create_job(self, prompt: str, role: str, scene: str, audience: str) -> Dict[str, Any]:
        # 校验 prompt 长度（官方建议 1-2000 字）
        prompt = prompt.strip()
        if not prompt:
            raise APIError("prompt 不能为空")
        if len(prompt) > 2000:
            raise APIError(f"prompt 不能超过 2000 个字符，当前为 {len(prompt)} 个字符")

        return self._request(
            "POST",
            "/ppt_jobs",
            {
                "prompt": prompt,
                "role": role,
                "scene": scene,
                "audience": audience,
            },
        )

    def get_job(self, job_id: str) -> Dict[str, Any]:
        return self._request("GET", f"/ppt_jobs/{job_id}")

    def reply_job(self, job_id: str, answer: str) -> Dict[str, Any]:
        return self._request("POST", f"/ppt_jobs/{job_id}/reply", {"answer": answer})


def normalize_state(data: Dict[str, Any], current: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    state = dict(current or {})
    for key in [
        "prompt",
        "role",
        "scene",
        "audience",
        "job_id",
        "status",
        "question",
        "download_url",
        "error_message",
    ]:
        if key in data and data[key] is not None:
            state[key] = data[key]
    state.setdefault("question", "")
    state.setdefault("download_url", "")
    state.setdefault("error_message", "")
    return state


def save_state(state: Dict[str, Any], state_path: str) -> None:
    path = Path(state_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_state(state_path: str) -> Dict[str, Any]:
    return json.loads(Path(state_path).read_text(encoding="utf-8"))


def default_state_path(job_id: str) -> str:
    return f"./output/jobs/{job_id}.json"


def load_registry(registry_path: str) -> Dict[str, Any]:
    path = Path(registry_path)
    if not path.exists():
        return {"jobs": []}
    return json.loads(path.read_text(encoding="utf-8"))


def save_registry(registry: Dict[str, Any], registry_path: str) -> None:
    path = Path(registry_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8") as tmp:
        tmp.write(json.dumps(registry, ensure_ascii=False, indent=2) + "\n")
        tmp_path = Path(tmp.name)
    os.replace(tmp_path, path)


def with_registry_lock(registry_path: str):
    path = Path(registry_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = path.with_name(f"{path.name}.lock")
    lock_file = lock_path.open("w", encoding="utf-8")
    fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
    return lock_file


def upsert_registry_entry(state: Dict[str, Any], state_path: str, registry_path: str) -> None:
    job_id = state.get("job_id", "")
    if not job_id:
        return

    lock_file = with_registry_lock(registry_path)
    try:
        registry = load_registry(registry_path)
        jobs = registry.setdefault("jobs", [])

        entry = {
            "job_id": job_id,
            "status": state.get("status", ""),
            "prompt": state.get("prompt", ""),
            "role": state.get("role", ""),
            "scene": state.get("scene", ""),
            "audience": state.get("audience", ""),
            "question": state.get("question", ""),
            "download_url": state.get("download_url", ""),
            "error_message": state.get("error_message", ""),
            "state_path": state_path,
            "updated_at": utc_now(),
        }

        for idx, item in enumerate(jobs):
            if item.get("job_id") == job_id:
                created_at = item.get("created_at", utc_now())
                entry["created_at"] = created_at
                jobs[idx] = entry
                save_registry(registry, registry_path)
                return

        entry["created_at"] = utc_now()
        jobs.append(entry)
        save_registry(registry, registry_path)
    finally:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
        lock_file.close()


def find_latest_job(
    registry_path: str,
    statuses: Optional[set[str]] = None,
    prompt_keyword: str = "",
) -> Optional[Dict[str, Any]]:
    registry = load_registry(registry_path)
    jobs = registry.get("jobs", [])
    prompt_keyword = (prompt_keyword or "").strip()

    def matched(job: Dict[str, Any]) -> bool:
        if statuses and job.get("status") not in statuses:
            return False
        if prompt_keyword and prompt_keyword not in job.get("prompt", ""):
            return False
        return True

    filtered = [job for job in jobs if matched(job)]
    if not filtered:
        return None
    filtered.sort(key=lambda item: item.get("updated_at", ""), reverse=True)
    return filtered[0]


def format_api_error(exc: APIError) -> str:
    text = exc.message or "请求失败，请稍后再试。"
    if exc.code == 600020:
        return "当前有多个 PPT 任务仍在执行中，请稍后再试或稍后回来查看之前的任务结果。"
    if exc.code == 600021:
        return "当前这份 PPT 任务暂时不处于可补充信息状态，请先查看最新进度，再决定是否继续补充。"
    if "未完成任务" in text or "任务数" in text or "上限" in text or "多个任务执行中" in text:
        return "当前有多个 PPT 任务仍在执行中，请稍后再试或稍后回来查看之前的任务结果。"
    return text


def pretty_output(state: Dict[str, Any], state_path: Optional[str] = None) -> None:
    status = state.get("status", "")
    if status == "succeeded":
        print(f"PPT 已生成完成，可下载：{state.get('download_url', '')}")
        return
    if status == "waiting_user_input":
        print("PPT 生成需要补充信息。")
        print(f"请继续回答：{state.get('question', '').strip()}")
        if state_path:
            print(f"继续任务请使用本地状态文件：{state_path}")
        return
    if status == "failed":
        print(f"PPT 生成失败：{state.get('error_message', '请稍后重试')}")
        return
    if status == "canceled":
        print("PPT 任务已取消，请重新发起。")
        return
    print(json.dumps(state, ensure_ascii=False, indent=2))


def pretty_pending_output(state: Dict[str, Any], state_path: str) -> None:
    print("PPT 任务已受理。创建或回复后的前置处理通常会在 2 分钟内完成，但最终生成通常仍需要 30 分钟到 2 小时。")
    print("当前先不阻塞等待结果。后续你可以让我继续查看这个任务的进度或结果。")
    print(f"本地状态文件：{state_path}")


def pretty_recent_job_output(job: Dict[str, Any]) -> None:
    print("已找到最近一个相关任务。")
    print(f"当前状态：{job.get('status', '')}")
    print(f"任务摘要：{job.get('prompt', '')}")
    print(f"本地状态文件：{job.get('state_path', '')}")


def poll_until_terminal(
    client: PPTClient,
    state: Dict[str, Any],
    poll_interval: int,
    initial_wait: int,
    max_polls: int,
    raise_on_timeout: bool = True,
) -> Dict[str, Any]:
    job_id = state.get("job_id", "")
    if not job_id:
        raise APIError("缺少 job_id，无法轮询")

    if initial_wait > 0:
        time.sleep(initial_wait)

    for idx in range(max_polls):
        latest = client.get_job(job_id)
        state = normalize_state(latest, state)
        status = state.get("status", "")
        if status in FINAL_STATUSES or status == "waiting_user_input":
            return state
        if idx < max_polls - 1:
            time.sleep(poll_interval)

    if raise_on_timeout:
        raise APIError("轮询超时，任务仍未结束")
    return state


def cmd_auth_check(_args: argparse.Namespace) -> int:
    host = os.environ.get("RACCOON_API_HOST", "")
    token = os.environ.get("RACCOON_API_TOKEN", "")
    if not host:
        stderr("错误: 未设置 RACCOON_API_HOST")
        return 1
    if not token:
        stderr("错误: 未设置 RACCOON_API_TOKEN")
        return 1
    print(f"RACCOON_API_HOST={host}")
    print(f"RACCOON_API_TOKEN=已设置({len(token)}字符)")
    return 0


def build_client(args: argparse.Namespace) -> PPTClient:
    return PPTClient(host=args.host, token=args.token)


def cmd_create_job(args: argparse.Namespace) -> int:
    client = build_client(args)
    role_info = normalize_category("role", args.role)
    scene_info = normalize_category("scene", args.scene)
    audience_info = normalize_category("audience", args.audience)
    data = client.create_job(
        args.prompt,
        role_info["value"],
        scene_info["value"],
        audience_info["value"],
    )
    state = normalize_state(
        {
            "prompt": args.prompt,
            "role": role_info["value"],
            "scene": scene_info["value"],
            "audience": audience_info["value"],
            **data,
        }
    )
    print(json.dumps(state, ensure_ascii=False, indent=2))
    return 0


def cmd_poll_job(args: argparse.Namespace) -> int:
    client = build_client(args)
    state = normalize_state({"job_id": args.job_id})
    state = poll_until_terminal(client, state, args.poll_interval, args.initial_wait, args.max_polls)
    print(json.dumps(state, ensure_ascii=False, indent=2))
    return 0


def cmd_reply_job(args: argparse.Namespace) -> int:
    client = build_client(args)
    data = client.reply_job(args.job_id, args.answer)
    state = normalize_state({"job_id": args.job_id, **data})
    print(json.dumps(state, ensure_ascii=False, indent=2))
    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    client = build_client(args)
    state_path = args.state_path
    registry_path = args.registry_path
    if args.resume_state:
        state = load_state(args.resume_state)
        state_path = args.resume_state
        answer = args.prompt.strip()
        if not answer:
            raise APIError("继续任务时，--prompt 需要填写用户对补充问题的回答")
        if state.get("status") != "waiting_user_input":
            raise APIError("当前状态不是 waiting_user_input，不能继续回复")
        data = client.reply_job(state["job_id"], answer)
        state = normalize_state({"prompt": answer, **data}, state)
    else:
        missing = [name for name in ["prompt", "role", "scene", "audience"] if not getattr(args, name)]
        if missing:
            raise APIError(f"缺少创建任务所需字段: {', '.join(missing)}")
        role_info = normalize_category("role", args.role)
        scene_info = normalize_category("scene", args.scene)
        audience_info = normalize_category("audience", args.audience)
        data = client.create_job(
            args.prompt,
            role_info["value"],
            scene_info["value"],
            audience_info["value"],
        )
        state = normalize_state(
            {
                "prompt": args.prompt,
                "role": role_info["value"],
                "scene": scene_info["value"],
                "audience": audience_info["value"],
                **data,
            }
        )
        if state.get("job_id") and args.state_path == "./output/ppt_job_state.json":
            state_path = default_state_path(state["job_id"])

    status = state.get("status", "")
    if status not in FINAL_STATUSES and status != "waiting_user_input":
        max_polls = args.max_polls
        if args.wait_mode == "block" and max_polls == DEFAULT_SHORT_MAX_POLLS:
            max_polls = DEFAULT_BLOCK_MAX_POLLS
        if args.wait_mode == "block":
            state = poll_until_terminal(
                client,
                state,
                args.poll_interval,
                args.initial_wait,
                max_polls,
                raise_on_timeout=True,
            )
        else:
            state = poll_until_terminal(
                client,
                state,
                args.poll_interval,
                args.initial_wait,
                max_polls,
                raise_on_timeout=False,
            )

    save_state(state, state_path)
    upsert_registry_entry(state, state_path, registry_path)
    if state.get("status") in {"queued", "running"} and args.wait_mode == "short":
        pretty_pending_output(state, state_path)
    else:
        pretty_output(state, state_path)
    return 0


def cmd_list_jobs(args: argparse.Namespace) -> int:
    registry = load_registry(args.registry_path)
    jobs = registry.get("jobs", [])
    if args.status:
        jobs = [job for job in jobs if job.get("status") == args.status]
    print(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=2))
    return 0


def cmd_check_job(args: argparse.Namespace) -> int:
    client = build_client(args)
    if args.state_path:
        state = load_state(args.state_path)
    elif args.job_id:
        state = {"job_id": args.job_id}
    else:
        raise APIError("需要提供 --state-path 或 --job-id")

    latest = client.get_job(state["job_id"])
    state = normalize_state(latest, state)
    state_path = args.state_path or default_state_path(state["job_id"])
    save_state(state, state_path)
    upsert_registry_entry(state, state_path, args.registry_path)
    pretty_output(state, state_path)
    return 0


def cmd_find_recent_job(args: argparse.Namespace) -> int:
    statuses = set(args.statuses.split(",")) if args.statuses else None
    job = find_latest_job(
        registry_path=args.registry_path,
        statuses=statuses,
        prompt_keyword=args.prompt_keyword,
    )
    if not job:
        print(json.dumps({"job": None}, ensure_ascii=False, indent=2))
        return 0
    if args.json:
        print(json.dumps({"job": job}, ensure_ascii=False, indent=2))
    else:
        pretty_recent_job_output(job)
    return 0


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--host", help="覆盖 RACCOON_API_HOST")
    parser.add_argument("--token", help="覆盖 RACCOON_API_TOKEN")


def main() -> int:
    parser = argparse.ArgumentParser(description="Raccoon PPT OpenAPI skill CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    auth_check = subparsers.add_parser("auth-check", help="检查环境变量")
    auth_check.set_defaults(func=cmd_auth_check)

    create_job = subparsers.add_parser("create-job", help="创建 PPT 任务")
    add_common_args(create_job)
    create_job.add_argument("--prompt", required=True)
    create_job.add_argument("--role", required=True)
    create_job.add_argument("--scene", required=True)
    create_job.add_argument("--audience", required=True)
    create_job.set_defaults(func=cmd_create_job)

    poll_job = subparsers.add_parser("poll-job", help="轮询任务直到结束")
    add_common_args(poll_job)
    poll_job.add_argument("--job-id", required=True)
    poll_job.add_argument("--initial-wait", type=int, default=DEFAULT_INITIAL_WAIT)
    poll_job.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL)
    poll_job.add_argument("--max-polls", type=int, default=DEFAULT_BLOCK_MAX_POLLS)
    poll_job.set_defaults(func=cmd_poll_job)

    reply_job = subparsers.add_parser("reply-job", help="回复补充问题")
    add_common_args(reply_job)
    reply_job.add_argument("--job-id", required=True)
    reply_job.add_argument("--answer", required=True)
    reply_job.set_defaults(func=cmd_reply_job)

    list_jobs = subparsers.add_parser("list-jobs", help="查看本地已记录的任务")
    list_jobs.add_argument("--registry-path", default=DEFAULT_REGISTRY_PATH)
    list_jobs.add_argument("--status", choices=["queued", "running", "waiting_user_input", "succeeded", "failed", "canceled"])
    list_jobs.set_defaults(func=cmd_list_jobs)

    check_job = subparsers.add_parser("check-job", help="查看一个已记录任务的最新状态")
    add_common_args(check_job)
    check_job.add_argument("--job-id")
    check_job.add_argument("--state-path")
    check_job.add_argument("--registry-path", default=DEFAULT_REGISTRY_PATH)
    check_job.set_defaults(func=cmd_check_job)

    find_recent = subparsers.add_parser("find-recent-job", help="查找最近的相关任务")
    find_recent.add_argument("--registry-path", default=DEFAULT_REGISTRY_PATH)
    find_recent.add_argument("--statuses", help="逗号分隔的状态过滤，如 queued,running,waiting_user_input")
    find_recent.add_argument("--prompt-keyword", default="")
    find_recent.add_argument("--json", action="store_true")
    find_recent.set_defaults(func=cmd_find_recent_job)

    normalize = subparsers.add_parser("normalize-category", help="归一化分类值")
    normalize.add_argument("kind", choices=["role", "scene", "audience"])
    normalize.add_argument("value")
    normalize.set_defaults(
        func=lambda args: (
            print(json.dumps(normalize_category(args.kind, args.value), ensure_ascii=False, indent=2)) or 0
        )
    )

    generate = subparsers.add_parser("generate", help="统一创建/继续/轮询入口")
    add_common_args(generate)
    generate.add_argument("--prompt", required=True, help="首次为任务需求，继续时为用户回答")
    generate.add_argument("--role")
    generate.add_argument("--scene")
    generate.add_argument("--audience")
    generate.add_argument("--resume-state", help="继续已有 waiting_user_input 任务")
    generate.add_argument("--state-path", default="./output/ppt_job_state.json")
    generate.add_argument("--registry-path", default=DEFAULT_REGISTRY_PATH)
    generate.add_argument("--wait-mode", choices=["short", "block"], default="short")
    generate.add_argument("--initial-wait", type=int, default=DEFAULT_INITIAL_WAIT)
    generate.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL)
    generate.add_argument("--max-polls", type=int, default=DEFAULT_SHORT_MAX_POLLS)
    generate.set_defaults(func=cmd_generate)

    args = parser.parse_args()
    try:
        return args.func(args)
    except APIError as exc:
        stderr(f"错误: {format_api_error(exc)}")
        return 1
    except FileNotFoundError as exc:
        stderr(f"错误: 找不到文件: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
