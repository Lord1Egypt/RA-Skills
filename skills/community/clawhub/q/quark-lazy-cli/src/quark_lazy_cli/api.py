"""
QasApi - QAS API封装（纯 Token 模式）

所有QAS操作封装为方法
认证方式：所有请求统一使用 query 参数 token=...
Token 来源：优先使用构造参数 token；否则从环境变量 QAS_API_TOKEN 读取。
不依赖 Cookie/Session 登录态；不发送 Cookie header。
"""

from __future__ import annotations

import concurrent.futures
import os
import sys
import requests
from quark_lazy_cli.config import settings
from typing import Iterator, Optional


class QasApiError(Exception):
    """QAS API异常"""

    pass


class QasApi:
    """
    QAS API 封装（纯 token）

    架构：
    1. __init__ 时调用 get_data() 获取全部 data 并保存到 self._data
    2. 所有读操作基于 self._data（内存）
    3. update_config(tasklist) 发送完整 tasklist 到后端
    """

    ENV_TOKEN_KEY = "QAS_API_TOKEN"
    TIMEOUT = 30

    def __init__(self, host: Optional[str] = None, token: Optional[str] = None):
        """
        Args:
            host - QAS服务地址，如 http://192.168.31.18:15305（可选；默认从环境变量读取）
            token - api_token（可选；不传则从环境变量读取）
        """
        from quark_lazy_cli.config import get_settings
        # 统一从 Config 读取，.env 加载由 config.py 负责
        try:
            cfg = get_settings()
            resolved = host or cfg.qas_host
            resolved_token = token or cfg.qas_token
        except RuntimeError as e:
            raise QasApiError(str(e)) from e
        self.host = resolved.rstrip("/")
        self.api_token = resolved_token
        if not self.api_token:
            raise QasApiError(
                f"缺少 token：请设置环境变量 {self.ENV_TOKEN_KEY} 或在构造时传入 token"
            )
        self._session = requests.Session()
        self._session.headers.update({"Content-Type": "application/json"})

        # 初始化时立即获取完整 data（token 无效则抛异常）
        self._data = self._fetch_data()

    def _fetch_data(self) -> dict:
        """
        从 QAS 获取完整 data 并保存到内存
        /data 接口返回 login_token + api_token + tasklist
        """
        raw = self._get("/data")
        if not raw.get("success"):
            msg = raw.get("message", "unknown")
            if "未登录" in str(msg) or "401" in str(msg):
                raise QasApiError(f"QAS未登录或Token无效: {msg}")
            raise QasApiError(f"获取data失败: {msg}")
        return raw

    def _ensure_token(self) -> None:
        """确保有 api_token（纯 token 模式必须具备）"""
        if not self.api_token:
            raise QasApiError(
                f"缺少 token：请设置环境变量 {self.ENV_TOKEN_KEY} 或在构造时传入 token"
            )

    def _get(self, path: str, *, params: Optional[dict] = None, **kwargs) -> dict:
        """GET请求（带token）"""
        self._ensure_token()
        url = f"{self.host}{path}"
        merged = dict(params or {})
        merged["token"] = self.api_token
        resp = self._session.get(url, params=merged, timeout=self.TIMEOUT, **kwargs)
        if not resp.ok:
            raise QasApiError(f"请求失败: {resp.status_code} {resp.text}")
        return resp.json()

    def _post(self, path: str, *, params: Optional[dict] = None, **kwargs) -> dict:
        """POST请求"""
        self._ensure_token()
        url = f"{self.host}{path}"
        merged = dict(params or {})
        merged["token"] = self.api_token
        resp = self._session.post(url, params=merged, timeout=self.TIMEOUT, **kwargs)
        if not resp.ok:
            raise QasApiError(f"请求失败: {resp.status_code} {resp.text}")
        return resp.json()

    # ==========================================
    # 1. 基础数据
    # ==========================================
    def get_data(self) -> dict:
        """
        返回内存中缓存的完整 data
        """
        return self._data

    def list_tasks(self) -> list[dict]:
        """返回任务列表"""
        return self._data.get("data", {}).get("tasklist", [])

    def update_task_config(self, tasklist: list[dict]) -> dict:
        """
        POST /update
        通过 tasklist 全量更新任务配置（QAS 是全量替换）
        同时更新本地缓存的 _data
        """
        result = self._post("/update", json={"tasklist": tasklist})
        if result.get("success"):
            # 更新本地缓存
            self._data["data"]["tasklist"] = tasklist
        return result

    def get_task_by_keyword(self, keyword: str) -> dict | None:
        """
        从 tasklist 中模糊匹配 taskname 包含 keyword 的任务。
        返回第一个匹配的任务的副本。
        """
        tasklist = self._data.get("data", {}).get("tasklist", [])
        for t in tasklist:
            if keyword.lower() in t.get("taskname", "").lower():
                return t.copy()
        return None

    def update_task_qas_config(self, cli_task: dict) -> dict:
        """
        用 cli_task 替换 tasklist 中同名的任务，POST 到 QAS。
        cli_task 包含更新后的完整任务字段。
        """
        tasklist = self._data.get("data", {}).get("tasklist", [])
        updated_tasklist = [
            cli_task if t.get("taskname") == cli_task.get("taskname") else t
            for t in tasklist
        ]
        result = self._post("/update", json={"tasklist": updated_tasklist})
        if result.get("success"):
            self._data["data"]["tasklist"] = updated_tasklist
        return result

    # ==========================================
    # 2. 搜索
    # ==========================================
    def task_suggestions(self, query: str, deep: bool = False) -> dict:
        """
        GET /task_suggestions?q={query}&d={0|1}&token={login_token}
        搜索夸克资源
        deep=True → 深度搜索
        返回：{"success": bool, "data": [...], "message": str}
        """
        d = 1 if deep else 0
        return self._get("/task_suggestions", params={"q": query, "d": d})

    # ==========================================
    # 3. 分享详情
    # ==========================================
    def get_share_detail(
        self, shareurl: str, stoken: str = None, task: dict = None
    ) -> dict:
        """
        POST /get_share_detail
        获取分享链接的详细信息
        返回：{file_list: [{name, fid, size, type, ...}]}
        task 参数用于 QAS 内部 preview_regex() 处理，返回 file_name_re 和 file_name_saved
        """
        payload = {"shareurl": shareurl}
        if stoken:
            payload["stoken"] = stoken
        if task:
            payload["task"] = task
            magic_regex = self._data.get("magic_regex", {})
            if magic_regex:
                payload["magic_regex"] = magic_regex
        return self._post("/get_share_detail", json=payload)

    # ==========================================
    # 4. 文件操作
    # ==========================================
    def get_savepath_detail(self, path: str = None, fid: str = None) -> dict:
        """
        GET /get_savepath_detail
        path 或 fid 二选一
        """
        if path:
            return self._get("/get_savepath_detail", params={"path": path})
        elif fid:
            return self._get("/get_savepath_detail", params={"fid": fid})
        else:
            raise QasApiError("path或fid必须提供一个")

    # ==========================================
    # 5. 手动执行
    # ==========================================
    @property
    def supports_run_scp_json(self) -> bool:
        """JSON 模式尚未实现，目前固定使用 SSE。"""
        # TODO: QAS 后端实现 JSON run_script_now 后再按服务能力探测开启。
        return False

    # 注解 QAS原代码尚未支持，不能使用
        # def run_script_now_json(self, tasklist: list[dict] | None = None) -> dict:
        #     """调用支持 JSON 的 run_script_now 接口（一次性返回，需等待所有文件处理完成）"""
        #     payload = {} if tasklist is None else {"tasklist": tasklist}
        #     self._ensure_token()
        #     params = {"token": self.api_token, "json": 1}
        #     resp = self._session.post(
        #         f"{self.host}/run_script_now",
        #         params=params,
        #         json=payload,
        #         timeout=300,  # JSON 模式一次性返回，等待时间设置 5 分钟
        #     )
        #     if not resp.ok:
        #         raise QasApiError(f"请求失败: {resp.status_code}")
        #     return resp.json()

    VERIFY_SHARE_LINKS_CONCURRENCY = 3
    VERIFY_SHARE_LINKS_TIMEOUT = 5

    def verify_share_links_with_details(self, items: list[dict]) -> dict:
        """
        详细验证分享链接有效性，返回完整诊断信息：

        {
            "valid_items": [...],          # 有效链接
            "invalid_items": [             # 死链（已验证失效）
                {"item": item, "reason": reason}
            ],
            "unknown_kept_items": [...]   # 超时/异常保留（可能有效）
        }

        死链关键词：("分享地址已失效", "好友已取消了分享", "分享内容不存在")
        超时/异常/未知错误 → 归入 unknown_kept_items
        保持原排序。
        """
        enabled = os.environ.get("LAZY_CLI_VERIFY_SHARE_LINKS", "true").lower() == "true"
        if not enabled:
            return {"valid_items": list(items), "invalid_items": [], "unknown_kept_items": []}
        if not items:
            return {"valid_items": [], "invalid_items": [], "unknown_kept_items": []}

        concurrency = self.VERIFY_SHARE_LINKS_CONCURRENCY
        timeout = self.VERIFY_SHARE_LINKS_TIMEOUT

        INVALID_KEYWORDS = ("分享地址已失效", "好友已取消了分享", "分享内容不存在")
        UNKNOWN_MARKER = "__unknown__"

        # 每个元素 (is_valid, reason)
        results: list[tuple[bool, str]] = [(True, "") for _ in items]

        def check_one(idx: int, item: dict) -> None:
            shareurl = item.get("shareurl", "")
            if not shareurl:
                return
            try:
                resp = self._session.post(
                    f"{self.host}/get_share_detail",
                    params={"token": self.api_token},
                    json={"shareurl": shareurl},
                    timeout=timeout,
                )
                data = resp.json()
                if data.get("success") is not True:
                    error_msg = data.get("data", {}).get("error", "")
                    if any(kw in error_msg for kw in INVALID_KEYWORDS):
                        results[idx] = (False, error_msg)
                    else:
                        results[idx] = (True, error_msg)
                else:
                    results[idx] = (True, "")
            except Exception:
                results[idx] = (True, UNKNOWN_MARKER)

        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
                futures = [executor.submit(check_one, i, item) for i, item in enumerate(items)]
                concurrent.futures.wait(futures)
        except Exception as e:
            if settings.debug:
                sys.stderr.write(f"[verify_share_links_with_details] system error: {e}\n")
            return {"valid_items": list(items), "invalid_items": [], "unknown_kept_items": []}

        valid_items = []
        invalid_items = []
        unknown_kept_items = []
        for i, (is_valid, reason) in enumerate(results):
            if is_valid and reason == UNKNOWN_MARKER:
                valid_items.append(items[i])
                unknown_kept_items.append(items[i])
            elif is_valid:
                valid_items.append(items[i])
            else:
                invalid_items.append({"item": items[i], "reason": reason})

        valid_count = len(valid_items)
        invalid_count = len(invalid_items)
        unknown_kept = len(unknown_kept_items)

        if settings.debug:
            sys.stderr.write(
                f"[verify_share_links] total={len(items)} valid={valid_count} "
                f"invalid={invalid_count} unknown_kept={unknown_kept} "
                f"concurrency={concurrency} timeout={timeout}s\n"
            )

        return {
            "valid_items": valid_items,
            "invalid_items": invalid_items,
            "unknown_kept_items": unknown_kept_items,
        }

    def verify_share_links(self, items: list[dict]) -> tuple[list[dict], int]:
        """
        轻量验证分享链接有效性，返回有效列表和失效数量。
        内部调用 verify_share_links_with_details，保留向后兼容。
        """
        details = self.verify_share_links_with_details(items)
        return details["valid_items"], len(details["invalid_items"])

    def run_script_now(self, tasklist: list[dict] | None = None) -> str:
        """
        POST /run_script_now
        API 读完整 SSE 流，检测到结束信号才返回完整报文
        失败时抛出异常，携带错误报文
        """
        #if self.supports_run_scp_json:
        #    return self.run_script_now_json(tasklist)

        payload = {} if tasklist is None else {"tasklist": tasklist}
        self._ensure_token()
        resp = self._session.post(
            f"{self.host}/run_script_now",
            params={"token": self.api_token},
            json=payload,
            stream=True,
            timeout=self.TIMEOUT,
        )
        if not resp.ok:
            raise QasApiError(f"请求失败: {resp.status_code}")

        lines = []
        for line in resp.iter_lines():
            if line:
                decoded = line.decode("utf-8")
                if decoded.startswith("data: "):
                    content = decoded[6:]
                    lines.append(content)
                    if "程序结束" in content or "运行时长" in content:
                        return "\n".join(lines)

        # 没收到结束信号，SSE 流异常
        partial_text = "\n".join(lines)
        raise QasApiError(f"SSE 流异常：未收到结束信号，收到 {len(lines)} 行\n{partial_text[:500]}")

# ============================================================
# quark_auto_save.py 日志解析工具
# ============================================================

from dataclasses import dataclass, field


@dataclass
class SaveResult:
    """单个文件的转存结果"""

    filename: str
    success: bool
    action: str = ""  # 转存/重命名/创建目录
    new_filename: Optional[str] = None
    error: Optional[str] = None
    raw: str = ""


@dataclass
class TaskResult:
    """一个任务的执行结果"""

    taskname: str
    success: bool
    saved_files: list[SaveResult] = field(default_factory=list)
    renamed_files: list[SaveResult] = field(default_factory=list)
    failed_files: list[SaveResult] = field(default_factory=list)
    created_dirs: list[str] = field(default_factory=list)
    error: Optional[str] = None
    raw_logs: list[str] = field(default_factory=list)


def parse_save_logs(raw_output: str) -> TaskResult:
    """解析 quark_auto_save.py 的日志输出"""
    import re

    lines = [ln.strip() for ln in raw_output.split("\n") if ln.strip()]

    task_result = TaskResult(taskname="", success=False)

    for line in lines:
        task_result.raw_logs.append(line)

        # 任务最终状态
        if match := re.search(r"(✅|❌)《(.+?)》", line):
            task_result.success = match.group(1) == "✅"
            task_result.taskname = match.group(2)
            continue

        # 通知消息
        if line.startswith("📢"):
            task_result.error = line[1:].strip()
            continue

        # 重命名成功
        if match := re.search(r"重命名：(.+?) → (.+)", line):
            task_result.renamed_files.append(
                SaveResult(
                    filename=match.group(1).strip(),
                    success=True,
                    action="重命名",
                    new_filename=match.group(2).strip(),
                    raw=line,
                )
            )
            continue

        # 重命名失败
        if "↑ 失败，" in line:
            error_msg = line.split("↑ 失败，", 1)[1].strip()
            task_result.failed_files.append(
                SaveResult(
                    filename="",
                    success=False,
                    action="重命名",
                    error=error_msg,
                    raw=line,
                )
            )
            continue

        # 创建目录
        if match := re.search(r"创建文件夹：(.+?)(?:\s*失败,\s*(.+))?$", line):
            dirname, error = match.groups()
            if error:
                task_result.failed_files.append(
                    SaveResult(
                        filename=dirname.strip(),
                        success=False,
                        action="创建目录",
                        error=error.strip(),
                        raw=line,
                    )
                )
            else:
                task_result.created_dirs.append(dirname.strip())
            continue

        # 转存成功（单行 emoji）
        if "✅" in line and ("转存" in line or "测试成功" in line):
            filename_match = re.search(r"转存文件:\s*(.+)", line)
            if filename_match:
                task_result.saved_files.append(
                    SaveResult(
                        filename=filename_match.group(1).strip(),
                        success=True,
                        action="转存",
                        raw=line,
                    )
                )
            continue

        # 转存失败（❌）
        if "❌" in line:
            if "《" in line:
                task_result.success = False
            filename_match = re.search(r"转存文件:\s*(.+)", line)
            if filename_match:
                task_result.failed_files.append(
                    SaveResult(
                        filename=filename_match.group(1).strip(),
                        success=False,
                        action="转存",
                        error=line,
                        raw=line,
                    )
                )
            continue

    return task_result


def print_save_result(result: TaskResult) -> None:
    """打印解析结果"""
    print(f"\n{'=' * 50}")
    print(f"任务: {result.taskname}")
    print(f"状态: {'✅ 成功' if result.success else '❌ 失败'}")

    if result.saved_files:
        print(f"\n📁 转存文件 ({len(result.saved_files)}):")
        for f in result.saved_files:
            print(f"   ✅ {f.filename}")

    if result.renamed_files:
        print(f"\n📝 重命名 ({len(result.renamed_files)}):")
        for f in result.renamed_files:
            print(f"   {f.filename} → {f.new_filename}")

    if result.failed_files:
        print(f"\n❌ 失败 ({len(result.failed_files)}):")
        for f in result.failed_files:
            print(f"   {f.filename}: {f.error or '未知错误'}")

    if result.created_dirs:
        print(f"\n📂 创建目录 ({len(result.created_dirs)}):")
        for d in result.created_dirs:
            print(f"   ✅ {d}")

    if result.error:
        print(f"\n💬 通知: {result.error}")
