#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
禅道 API 客户端 - 老 API (Legacy API)
"""

import json
import hashlib
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any


class ZenTaoClient:
    """禅道 API 客户端（老 API）"""

    def __init__(
        self,
        endpoint: str,
        username: str,
        password: str,
        session_dir: Optional[str] = None,
        auto_save: bool = True,
        auto_load: bool = True,
    ):
        """初始化禅道客户端

        Args:
            endpoint: 禅道地址，如 http://127.0.0.1:8080
            username: 用户名
            password: 密码
            session_dir: Session 存储目录
                - 默认 None: 存储在项目根目录的 .zentao/sessions/
                - 也可指定其他路径
            auto_save: 是否自动保存 Session
            auto_load: 是否自动加载已有 Session
        """
        self.endpoint = endpoint.rstrip("/")
        self.username = username
        self.password = password
        self.auto_save = auto_save
        self.auto_load = auto_load

        # 老 API 配置
        self.old_api_base = self.endpoint
        self.session = None
        self.sid = None

        # Session 存储目录
        if session_dir:
            self.session_dir = Path(session_dir)
        else:
            # 默认存储在项目根目录的 .zentao/sessions/
            self.session_dir = Path(__file__).parent.parent / ".zentao" / "sessions"
        self.session_dir.mkdir(parents=True, exist_ok=True)

    def _get_session_file(self) -> Path:
        """获取 Session 文件路径"""
        key = f"{self.endpoint}:{self.username}"
        key_hash = hashlib.md5(key.encode()).hexdigest()[:16]
        return self.session_dir / f"{key_hash}.json"

    def _save_session(self) -> bool:
        """保存 Session 到文件"""
        try:
            if not self.sid or not self.session:
                return False

            session_file = self._get_session_file()
            data = {
                "endpoint": self.endpoint,
                "username": self.username,
                "sid": self.sid,
                "cookies": self.session.cookies.get_dict(),
            }
            session_file.write_text(json.dumps(data, ensure_ascii=False, indent=2))
            return True
        except Exception as e:
            print(f"Session 保存失败：{e}")
            return False

    def _load_session(self) -> bool:
        """从文件加载 Session"""
        try:
            session_file = self._get_session_file()
            if not session_file.exists():
                return False

            data = json.loads(session_file.read_text())

            # 验证 endpoint 和 username 匹配
            if (
                data.get("endpoint") != self.endpoint
                or data.get("username") != self.username
            ):
                return False

            self.sid = data.get("sid")
            self.session = requests.session()
            self.session.cookies.update(data.get("cookies", {}))

            # 验证 Session 是否有效
            if self._validate_session():
                return True
            else:
                self.sid = None
                self.session = None
                return False
        except Exception as e:
            print(f"Session 加载失败：{e}")
            return False

    def _validate_session(self) -> bool:
        """验证 Session 是否有效"""
        try:
            url = f"{self.old_api_base}/user-refresh.html"
            response = self.session.get(url, timeout=10)
            # 如果返回登录页面，说明 Session 无效
            if "登录" in response.text or "login" in response.text.lower():
                return False
            return True
        except Exception:
            return False

    def clear_session(self) -> bool:
        """清除保存的 Session"""
        try:
            session_file = self._get_session_file()
            if session_file.exists():
                session_file.unlink()
            self.sid = None
            self.session = None
            return True
        except Exception as e:
            print(f"Session 清除失败：{e}")
            return False

    # ==================== 认证相关 ====================

    def get_session(self, force_refresh: bool = False) -> Optional[str]:
        """获取 Session

        Args:
            force_refresh: 是否强制刷新 Session

        Returns:
            sessionID 或 None
        """
        # 尝试加载已有 Session
        if not force_refresh and self.auto_load and not self.sid:
            if self._load_session():
                return self.sid

        # 获取新 Session
        try:
            sid_url = f"{self.old_api_base}/api-getSessionID.json"
            response = requests.get(sid_url, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    self.sid = json.loads(result["data"])["sessionID"]

                    # 登录
                    login_url = (
                        f"{self.old_api_base}/user-login.json?zentaosid={self.sid}"
                    )
                    self.session = requests.session()
                    login_data = {
                        "account": self.username,
                        "password": self.password,
                        "keepLogin[]": "on",
                        "referer": f"{self.old_api_base}/my/",
                    }
                    login_response = self.session.post(
                        login_url, data=login_data, timeout=30
                    )
                    if login_response.status_code == 200:
                        login_result = login_response.json()
                        if login_result.get("status") == "success":
                            # 自动保存 Session
                            if self.auto_save:
                                self._save_session()
                            return self.sid
            return None
        except Exception as e:
            print(f"Session 获取异常：{e}")
            return None

    def old_request(
        self, method: str, path: str, data: Optional[Dict] = None
    ) -> Tuple[bool, Any]:
        """老 API 请求"""
        if not self.sid:
            self.get_session()

        if not self.sid:
            return False, "认证失败"

        url = f"{self.old_api_base}/{path.lstrip('/')}"
        if "?" in url:
            url += f"&zentaosid={self.sid}"
        else:
            url += f"?zentaosid={self.sid}"

        try:
            if method.upper() == "GET":
                response = self.session.get(url, timeout=30)
            elif method.upper() == "POST":
                response = self.session.post(url, data=data, timeout=30)
            else:
                return False, f"不支持的方法：{method}"

            if response.status_code == 200:
                try:
                    result = response.json()
                except Exception:
                    try:
                        result = json.loads(response.text)
                    except Exception:
                        result = {"raw": response.text}

                if (
                    result.get("status") == "success"
                    or result.get("result") == "success"
                ):
                    return True, result
                else:
                    return False, result
            else:
                return False, f"HTTP {response.status_code}"
        except Exception as e:
            return False, str(e)

    # ==================== 老 API 方法 ====================

    def get_product_list_old(self) -> Dict[str, str]:
        """获取产品列表（老 API）- 返回 {产品名：ID}"""
        success, result = self.old_request("GET", "/product-index-no.json")
        if success and "data" in result:
            data = json.loads(result["data"])
            products = data.get("products", [])
            return {p["name"]: str(p["id"]) for p in products}
        return {}

    def get_project_list_old(self, status: str = "all") -> Dict[str, str]:
        """获取项目列表（老 API）

        Returns:
            {项目ID: 项目名} 例如 {'1': 'config', '2': 'project2'}
        """
        success, result = self.old_request("GET", "/project-browse-all.json")
        if success and "data" in result:
            data = json.loads(result["data"])
            projects = data.get("projects", {})
            return projects
        return {}

    def get_bug_list_old(self, product_id: str, branch: str = "0") -> List[Dict]:
        """获取缺陷列表（老 API）

        Args:
            product_id: 产品ID
            branch: 分支ID，默认 "0"

        Returns:
            Bug列表
        """
        success, result = self.old_request(
            "GET", f"/bug-browse-{product_id}-{branch}-all.json"
        )
        if success and "data" in result:
            return json.loads(result["data"])
        return []

    def get_productplan_list_old(
        self, product_id: str, branch: str = "0"
    ) -> Dict[str, str]:
        """获取发布计划列表（老 API）

        Args:
            product_id: 产品ID
            branch: 分支ID，默认 "0"

        Returns:
            {计划名：ID}
        """
        success, result = self.old_request(
            "GET", f"/productplan-browse-{product_id}-{branch}-all.json"
        )
        if success and "data" in result:
            data = json.loads(result["data"])
            plans = data.get("productPlansNum", {})
            return {v["title"]: v["id"] for k, v in plans.items()}
        return {}

    def get_project_tasks_old(
        self,
        project_id: str,
        status: str = "all",
        module_id: str = "0",
        limit: int = 2000,
        page: int = 1,
    ) -> Dict:
        """获取项目任务列表（老 API）

        Args:
            project_id: 项目ID
            status: 任务状态，默认 "all" 获取所有状态
            module_id: 模块ID，默认 "0" 获取所有模块
            limit: 每页数量，默认 2000
            page: 页码，默认 1

        Returns:
            任务字典 {任务ID: 任务信息}

        Note:
            已取消的任务可能不显示在列表中，请使用 get_task_detail 查询单个任务状态
        """
        success, result = self.old_request(
            "GET",
            f"/project-task-{project_id}-{status}-id_desc-{module_id}-{limit}-{page}.json",
        )
        if success and "data" in result:
            data = json.loads(result["data"])
            tasks = data.get("tasks", {})
            return tasks
        return {}

    def get_task_detail(self, task_id: str) -> Tuple[bool, Dict]:
        """获取单个任务详情（老 API）

        Args:
            task_id: 任务ID

        Returns:
            (success, task_info) task_info 包含 id, name, status, parent, assignedTo 等字段

        Note:
            此方法可获取任务的真实状态（包括已取消状态），适用于验证操作结果
        """
        success, result = self.old_request("GET", f"/task-view-{task_id}.json")
        if success and "data" in result:
            data = json.loads(result["data"])
            task = data.get("task", {})
            return True, task
        return False, {}

    # ==================== 写操作方法（需要确认）====================

    def create_story(
        self,
        product_id: str,
        execution_id: str,
        title: str,
        module: str = "0",
        plan_id: str = "0",
        branch: str = "0",
        reviewer: str = "",
    ) -> Tuple[bool, Dict]:
        """新建需求（老 API）

        Args:
            product_id: 产品ID
            execution_id: 执行/项目ID
            title: 需求标题
            module: 模块ID，默认 "0"
            plan_id: 计划ID，默认 "0"
            branch: 分支ID，默认 "0"
            reviewer: 评审人，默认为空

        Returns:
            (success, result)
        """
        post_data = {
            "product": product_id,
            "module": module,
            "modules[0]": module,
            "plans[0]": plan_id,
            "title": title,
            "plan": plan_id,
            "reviewer[]": reviewer or "xuzn",
        }
        # URL: /story-create-{product}-{module}-{story}-{plan}-{execution}-{branch}-{module}-{type}.json
        return self.old_request(
            "POST",
            f"/story-create-{product_id}-{module}-0-{plan_id}-{execution_id}-{branch}-{module}-0-story.json",
            post_data,
        )

    def create_subtasks(
        self,
        execution_id: str,
        parent_id: str,
        tasks: list,
        story_id: str = "0",
        module_id: str = "0",
    ) -> Tuple[bool, Dict]:
        """创建子任务（老 API）

        Args:
            execution_id: 执行/项目ID
            parent_id: 父任务ID
            tasks: 任务列表，每个任务包含 name, estimate, assignedTo 等
            story_id: 需求ID，默认 "0"
            module_id: 模块ID，默认 "0"

        Returns:
            (success, result)
        """

        # 构建 multipart/form-data
        boundary = "----WebKitFormBoundary" + "".join(
            [chr(ord("A") + i % 26) for i in range(16)]
        )

        lines = []
        for i, task in enumerate(tasks):
            name = task.get("name", "")
            estimate = task.get("estimate", "")
            assigned_to = task.get("assignedTo", "admin")
            task_type = task.get("type", "devel")
            pri = task.get("pri", "3")

            # 第一个任务用实际值
            if i == 0:
                lines.append(f"--{boundary}")
                lines.append('Content-Disposition: form-data; name="module[0]"')
                lines.append("")
                lines.append("0")

                lines.append(f"--{boundary}")
                lines.append('Content-Disposition: form-data; name="parent[0]"')
                lines.append("")
                lines.append(parent_id)

                lines.append(f"--{boundary}")
                lines.append('Content-Disposition: form-data; name="name[0]"')
                lines.append("")
                lines.append(name)

                lines.append(f"--{boundary}")
                lines.append('Content-Disposition: form-data; name="type[0]"')
                lines.append("")
                lines.append(task_type)

                lines.append(f"--{boundary}")
                lines.append('Content-Disposition: form-data; name="assignedTo[0]"')
                lines.append("")
                lines.append(assigned_to)

                lines.append(f"--{boundary}")
                lines.append('Content-Disposition: form-data; name="estimate[0]"')
                lines.append("")
                lines.append(str(estimate))

                lines.append(f"--{boundary}")
                lines.append('Content-Disposition: form-data; name="pri[0]"')
                lines.append("")
                lines.append(str(pri))
            else:
                # 后续任务用 ditto
                for field in ["module", "parent", "story"]:
                    lines.append(f"--{boundary}")
                    lines.append(f'Content-Disposition: form-data; name="{field}[{i}]"')
                    lines.append("")
                    lines.append("ditto" if field in ["parent", "story"] else "0")

                lines.append(f"--{boundary}")
                lines.append(f'Content-Disposition: form-data; name="name[{i}]"')
                lines.append("")
                lines.append(name)

                lines.append(f"--{boundary}")
                lines.append(f'Content-Disposition: form-data; name="type[{i}]"')
                lines.append("")
                lines.append("ditto")

                lines.append(f"--{boundary}")
                lines.append(f'Content-Disposition: form-data; name="assignedTo[{i}]"')
                lines.append("")
                lines.append("ditto")

                lines.append(f"--{boundary}")
                lines.append(f'Content-Disposition: form-data; name="estimate[{i}]"')
                lines.append("")
                lines.append(str(estimate))

                lines.append(f"--{boundary}")
                lines.append(f'Content-Disposition: form-data; name="pri[{i}]"')
                lines.append("")
                lines.append("ditto")

        lines.append(f"--{boundary}--")

        body = "\r\n".join(lines)

        url = f"{self.old_api_base}/task-batchCreate-{execution_id}-{story_id}-{module_id}-{parent_id}.html"
        headers = {"Content-Type": f"multipart/form-data; boundary={boundary}"}

        response = self.session.post(
            url, data=body, headers=headers, params={"zentaosid": self.sid}, timeout=30
        )

        if response.status_code == 200:
            return True, {
                "message": "创建子任务成功",
                "status_code": response.status_code,
            }
        else:
            return False, {
                "message": f"创建失败: HTTP {response.status_code}",
                "status_code": response.status_code,
            }

    def delete_task(self, task_id: str) -> Tuple[bool, Dict]:
        """删除任务（老 API）

        Args:
            task_id: 任务ID

        Returns:
            (success, result)
        """
        return self.old_request("POST", f"/task-delete-{task_id}.json")

    def cancel_task(self, task_id: str, comment: str = "") -> Tuple[bool, Dict]:
        """取消任务（老 API）

        Args:
            task_id: 任务ID
            comment: 取消原因

        Returns:
            (success, result) result 包含 status 和 data

        Note:
            取消后任务状态变为 'cancel'，但可能不显示在项目任务列表中。
            建议使用 get_task_detail(task_id) 验证取消结果。

        Example:
            >>> success, result = client.cancel_task("6", "功能暂缓开发")
            >>> if success:
            >>>     # 验证取消结果
            >>>     ok, task = client.get_task_detail("6")
            >>>     print(f"任务状态: {task.get('status')}")  # 应为 'cancel'
        """
        # 先获取任务详情
        success, task = self.get_task_detail(task_id)
        if not success:
            return False, {"message": f"获取任务失败: {task}"}

        # 基础字段
        data = {
            "status": "cancel",
            "assignedTo": task.get("assignedTo", ""),
            "name": task.get("name", ""),
            "type": task.get("type", "devel"),
            "pri": str(task.get("pri", "3")),
            "estimate": str(task.get("estimate", "0")),
            "left": str(task.get("left", "0")),
            "consumed": str(task.get("consumed", "0")),
        }

        # 子任务需要传 parent，一级任务不需要
        parent = task.get("parent", "0")
        if parent and parent != "0":
            data["parent"] = str(parent)

        if comment:
            data["comment"] = comment

        url = f"{self.old_api_base}/task-edit-{task_id}.json?zentaosid={self.sid}"
        response = self.session.post(url, data=data, timeout=30)

        if response.status_code == 200:
            return True, {
                "message": "取消任务成功",
                "status_code": response.status_code,
            }
        else:
            return False, {"message": f"取消失败: HTTP {response.status_code}"}

    def close_task(self, task_id: str, comment: str = "") -> Tuple[bool, Dict]:
        """关闭任务（老 API）

        Args:
            task_id: 任务ID
            comment: 关闭备注（可选）

        Returns:
            (success, result)
            注意：即使返回 success=False（因为返回HTML），任务也可能已关闭。
            请使用 get_task_detail(task_id) 验证结果。

        Note:
            关闭后任务状态变为 'closed'。
            可直接关闭 wait 状态的任务，无需先完成。

        Example:
            >>> success, result = client.close_task("7", "已完成")
            >>> # 验证关闭结果
            >>> ok, task = client.get_task_detail("7")
            >>> print(f"任务状态: {task.get('status')}")  # 应为 'closed'
            >>> print(f"关闭人: {task.get('closedBy')}")
        """
        data = {}
        if comment:
            data["comment"] = comment
        return self.old_request("POST", f"/task-close-{task_id}.json", data=data)

    def start_task(self, task_id: str, comment: str = "") -> Tuple[bool, Dict]:
        """开始任务（老 API）

        Args:
            task_id: 任务ID
            comment: 开始备注（可选）

        Returns:
            (success, result)
            注意：即使返回 success=False（因为返回HTML），任务也可能已开始。
            请使用 get_task_detail(task_id) 验证结果。

        Note:
            开始后任务状态变为 'doing'。
            实际使用 task-edit 接口修改状态，因为 task-start 接口会直接完成任务。

        Example:
            >>> success, result = client.start_task("10", "开始开发")
            >>> # 验证开始结果
            >>> ok, task = client.get_task_detail("10")
            >>> print(f"任务状态: {task.get('status')}")  # 应为 'doing'
        """
        # 先获取任务详情
        ok, task = self.get_task_detail(task_id)
        if not ok:
            return False, {"error": "无法获取任务详情"}

        # 用 task-edit 修改状态为 doing
        edit_data = {
            "id": task_id,
            "parent": task.get("parent", "0"),
            "project": task.get("project", "0"),
            "module": task.get("module", "0"),
            "story": task.get("story", "0"),
            "name": task.get("name", ""),
            "type": task.get("type", "devel"),
            "pri": task.get("pri", "3"),
            "estimate": task.get("estimate", "0"),
            "left": task.get("left", "0"),
            "consumed": task.get("consumed", "0"),
            "assignedTo": task.get("assignedTo", "admin"),
            "status": "doing",
        }
        if comment:
            edit_data["comment"] = comment

        return self.old_request("POST", f"/task-edit-{task_id}.json", edit_data)

    def record_estimate(
        self, task_id: str, records: List[Dict[str, str]]
    ) -> Tuple[bool, Dict]:
        """记录任务工时（老 API）

        Args:
            task_id: 任务ID
            records: 工时记录列表，每条记录包含:
                - date: 日期 (YYYY-MM-DD)
                - consumed: 本次消耗工时
                - left: 剩余工时
                - work: 工作内容

        Returns:
            (success, result) 注意：返回 HTML 页面，解析会失败。
            请使用 get_task_detail(task_id) 验证 consumed 和 left 是否更新。

        Note:
            - 索引从 1 开始，不是 0
            - 必须使用 .html?onlybody=yes 端点
            - 可以一次提交多条工时记录

        Example:
            >>> from datetime import datetime
            >>> today = datetime.now().strftime("%Y-%m-%d")
            >>> records = [
            ...     {"date": today, "consumed": "2", "left": "6", "work": "开发功能A"},
            ...     {"date": today, "consumed": "1", "left": "5", "work": "测试"}
            ... ]
            >>> success, result = client.record_estimate("13", records)
            >>> ok, task = client.get_task_detail("13")
            >>> print(f"消耗: {task['consumed']}, 剩余: {task['left']}")
        """
        data = {}
        for i, record in enumerate(records, start=1):
            data[f"id[{i}]"] = record.get("id", "")
            data[f"dates[{i}]"] = record.get("date", "")
            data[f"consumed[{i}]"] = record.get("consumed", "")
            data[f"left[{i}]"] = record.get("left", "")
            data[f"work[{i}]"] = record.get("work", "")

        url = f"{self.old_api_base}/task-recordEstimate-{task_id}.html?onlybody=yes"
        response = self.session.post(
            url, data=data, params={"zentaosid": self.sid}, timeout=30
        )

        if response.status_code == 200:
            return True, {
                "message": "记录工时成功",
                "status_code": response.status_code,
            }
        else:
            return False, {
                "message": f"记录失败: HTTP {response.status_code}",
                "status_code": response.status_code,
            }

    def get_estimate(self, estimate_id: str) -> Tuple[bool, Dict]:
        """获取工时记录详情（老 API）

        Args:
            estimate_id: 工时记录ID

        Returns:
            (success, estimate_info)
        """
        success, result = self.old_request(
            "GET", f"/task-editEstimate-{estimate_id}.json"
        )
        if success and "data" in result:
            data = json.loads(result["data"])
            estimate = data.get("estimate", {})
            return True, estimate
        return False, {}

    def edit_estimate(
        self, estimate_id: str, consumed: str = None, left: str = None, work: str = None
    ) -> Tuple[bool, Dict]:
        """编辑工时记录（老 API）

        Args:
            estimate_id: 工时记录ID
            consumed: 消耗工时（可选）
            left: 剩余工时（可选）
            work: 工作内容（可选）

        Returns:
            (success, result) 注意：返回 HTML 页面。
            请使用 get_estimate(estimate_id) 验证修改结果。

        Example:
            >>> success, result = client.edit_estimate("1", consumed="5", left="3", work="修改记录")
            >>> ok, estimate = client.get_estimate("1")
            >>> print(f"消耗: {estimate['consumed']}, 剩余: {estimate['left']}")
        """
        data = {}
        if consumed is not None:
            data["consumed"] = consumed
        if left is not None:
            data["left"] = left
        if work is not None:
            data["work"] = work

        url = f"{self.old_api_base}/task-editEstimate-{estimate_id}.json"
        response = self.session.post(
            url, data=data, params={"zentaosid": self.sid}, timeout=30
        )

        if response.status_code == 200:
            return True, {
                "message": "编辑工时成功",
                "status_code": response.status_code,
            }
        else:
            return False, {
                "message": f"编辑失败: HTTP {response.status_code}",
                "status_code": response.status_code,
            }

    def delete_estimate(self, estimate_id: str) -> Tuple[bool, Dict]:
        """删除工时记录（老 API）

        Args:
            estimate_id: 工时记录ID

        Returns:
            (success, result) 注意：返回 HTML 页面。
            请使用 get_estimate(estimate_id) 验证删除结果（应返回失败）。

        Note:
            删除工时记录后，任务的 consumed 和 left 会自动更新。

        Example:
            >>> success, result = client.delete_estimate("1")
            >>> ok, estimate = client.get_estimate("1")
            >>> if not ok:
            >>>     print("工时记录已删除")
        """
        url = f"{self.old_api_base}/task-deleteEstimate-{estimate_id}-yes.json"
        response = self.session.get(url, params={"zentaosid": self.sid}, timeout=30)

        if response.status_code == 200:
            return True, {
                "message": "删除工时成功",
                "status_code": response.status_code,
            }
        else:
            return False, {
                "message": f"删除失败: HTTP {response.status_code}",
                "status_code": response.status_code,
            }

    def finish_task(self, task_id: str, comment: str = "") -> Tuple[bool, Dict]:
        """完成任务（老 API）

        Args:
            task_id: 任务ID
            comment: 完成备注（可选）

        Returns:
            (success, result) 注意：返回 HTML 页面。
            请使用 get_task_detail(task_id) 验证完成结果。

        Note:
            - 任务状态变为 'done'
            - 会记录 finishedBy 和 finishedDate
            - 建议先记录工时（left=0）再完成任务

        Example:
            >>> # 先记录工时
            >>> client.record_estimate("15", [{"date": "2026-03-27", "consumed": "3", "left": "0", "work": "完成"}])
            >>> # 再完成任务
            >>> success, result = client.finish_task("15", "已完成")
            >>> ok, task = client.get_task_detail("15")
            >>> print(f"状态: {task['status']}")  # done
            >>> print(f"完成人: {task['finishedBy']}")
        """
        data = {}
        if comment:
            data["comment"] = comment

        url = f"{self.old_api_base}/task-finish-{task_id}.json"
        response = self.session.post(
            url, data=data, params={"zentaosid": self.sid}, timeout=30
        )

        if response.status_code == 200:
            return True, {
                "message": "完成任务成功",
                "status_code": response.status_code,
            }
        else:
            return False, {
                "message": f"完成失败: HTTP {response.status_code}",
                "status_code": response.status_code,
            }

    def pause_task(self, task_id: str, comment: str = "") -> Tuple[bool, Dict]:
        """暂停任务（老 API）

        Args:
            task_id: 任务ID
            comment: 暂停备注（可选）

        Returns:
            (success, result) 注意：返回 HTML 页面。
            请使用 get_task_detail(task_id) 验证暂停结果。

        Note:
            - 任务状态变为 'pause'
            - 仅对 doing 状态的任务有效

        Example:
            >>> success, result = client.pause_task("17", "暂停开发")
            >>> ok, task = client.get_task_detail("17")
            >>> print(f"状态: {task['status']}")  # pause
        """
        data = {}
        if comment:
            data["comment"] = comment

        url = f"{self.old_api_base}/task-pause-{task_id}.json"
        response = self.session.post(
            url, data=data, params={"zentaosid": self.sid}, timeout=30
        )

        if response.status_code == 200:
            return True, {
                "message": "暂停任务成功",
                "status_code": response.status_code,
            }
        else:
            return False, {
                "message": f"暂停失败: HTTP {response.status_code}",
                "status_code": response.status_code,
            }

    def restart_task(self, task_id: str, comment: str = "") -> Tuple[bool, Dict]:
        """继续任务（老 API）

        Args:
            task_id: 任务ID
            comment: 继续备注（可选）

        Returns:
            (success, result) 注意：返回 HTML 页面。
            请使用 get_task_detail(task_id) 验证继续结果。

        Note:
            - 将 pause 状态的任务恢复为 doing
            - 仅对 pause 状态的任务有效

        Example:
            >>> success, result = client.restart_task("17", "继续开发")
            >>> ok, task = client.get_task_detail("17")
            >>> print(f"状态: {task['status']}")  # doing
        """
        data = {}
        if comment:
            data["comment"] = comment

        url = f"{self.old_api_base}/task-restart-{task_id}.json"
        response = self.session.post(
            url, data=data, params={"zentaosid": self.sid}, timeout=30
        )

        if response.status_code == 200:
            return True, {
                "message": "继续任务成功",
                "status_code": response.status_code,
            }
        else:
            return False, {
                "message": f"继续失败: HTTP {response.status_code}",
                "status_code": response.status_code,
            }

    def activate_task(self, task_id: str, comment: str = "") -> Tuple[bool, Dict]:
        """激活任务（老 API）

        Args:
            task_id: 任务ID
            comment: 激活备注（可选）

        Returns:
            (success, result) 注意：返回 HTML 页面。
            请使用 get_task_detail(task_id) 验证激活结果。

        Note:
            - 将 done/closed 状态的任务恢复为 doing
            - 对于 cancel 状态的任务可能无法激活

        Example:
            >>> success, result = client.activate_task("17", "重新开始")
            >>> ok, task = client.get_task_detail("17")
            >>> print(f"状态: {task['status']}")  # doing
        """
        data = {}
        if comment:
            data["comment"] = comment

        url = f"{self.old_api_base}/task-activate-{task_id}.json"
        response = self.session.post(
            url, data=data, params={"zentaosid": self.sid}, timeout=30
        )

        if response.status_code == 200:
            return True, {
                "message": "激活任务成功",
                "status_code": response.status_code,
            }
        else:
            return False, {
                "message": f"激活失败: HTTP {response.status_code}",
                "status_code": response.status_code,
            }

    def assign_task(
        self, task_id: str, assigned_to: str, comment: str = ""
    ) -> Tuple[bool, Dict]:
        """指派任务（老 API）

        Args:
            task_id: 任务ID
            assigned_to: 指派给谁（用户名）
            comment: 指派备注（可选）

        Returns:
            (success, result) 注意：返回空响应。
            请使用 get_task_detail(task_id) 验证指派结果。

        Example:
            >>> success, result = client.assign_task("17", "zhangsan", "请处理")
            >>> ok, task = client.get_task_detail("17")
            >>> print(f"指派给: {task['assignedTo']}")  # zhangsan
        """
        data = {"assignedTo": assigned_to}
        if comment:
            data["comment"] = comment

        url = f"{self.old_api_base}/task-assignTo-{task_id}.json"
        response = self.session.post(
            url, data=data, params={"zentaosid": self.sid}, timeout=30
        )

        if response.status_code == 200:
            return True, {
                "message": "指派任务成功",
                "status_code": response.status_code,
            }
        else:
            return False, {
                "message": f"指派失败: HTTP {response.status_code}",
                "status_code": response.status_code,
            }

    def create_task(
        self,
        project: str,
        name: str,
        type: str = "devel",
        story: str = "0",
        module: str = "0",
        assignedTo: str = "",
        pri: str = "3",
        desc: str = "",
        estimate: str = "0",
        **kwargs,
    ) -> Tuple[bool, Dict]:
        """创建任务（老 API）

        Args:
            project: 所属项目ID *必填
            name: 任务名称 *必填
            type: 任务类型 *必填，取值: design, devel, test, study, discuss, ui, affair, misc
            story: 相关需求ID
            module: 所属模块ID
            assignedTo: 指派给（用户名）
            pri: 优先级 (0-4)
            desc: 任务描述
            estimate: 预计工时

        Returns:
            (success, result)

        Example:
            >>> success, result = client.create_task(
            ...     project="1",
            ...     name="用户登录功能开发",
            ...     type="devel",
            ...     assignedTo="admin",
            ...     pri="3"
            ... )
        """
        return self.create_tasks(
            project=project,
            tasks=[
                {
                    "name": name,
                    "type": type,
                    "story": story,
                    "module": module,
                    "assignedTo": assignedTo or "admin",
                    "pri": pri,
                    "desc": desc,
                    "estimate": estimate,
                }
            ],
            **kwargs,
        )

    def create_tasks(
        self,
        project: str,
        tasks: List[Dict],
        story_id: str = "0",
        module_id: str = "0",
        parent_id: str = "0",
        **kwargs,
    ) -> Tuple[bool, Dict]:
        """批量创建任务（老 API）

        Args:
            project: 所属项目ID *必填
            tasks: 任务列表，每个任务包含 name, type, story, module, assignedTo, pri, desc, estimate
            story_id: 需求ID，默认 "0"
            module_id: 模块ID，默认 "0"
            parent_id: 父任务ID，默认 "0"

        Returns:
            (success, result)

        Example:
            >>> success, result = client.create_tasks(
            ...     project="1",
            ...     tasks=[
            ...         {"name": "任务1", "type": "devel", "assignedTo": "admin"},
            ...         {"name": "任务2", "type": "test", "assignedTo": "admin"}
            ...     ]
            ... )
        """
        if not self.sid:
            self.get_session()

        data = {}
        for i, task in enumerate(tasks):
            data[f"module[{i}]"] = task.get("module", "0")
            data[f"story[{i}]"] = task.get("story", "0")
            data[f"parent[{i}]"] = task.get("parent", "0")
            data[f"name[{i}]"] = task.get("name", "")
            data[f"type[{i}]"] = task.get("type", "devel")
            data[f"assignedTo[{i}]"] = task.get("assignedTo", "admin")
            data[f"estimate[{i}]"] = str(task.get("estimate", "0"))
            data[f"pri[{i}]"] = str(task.get("pri", "3"))
            data[f"desc[{i}]"] = task.get("desc", "")

        return self.old_request(
            "POST",
            f"/task-batchCreate-{project}-{story_id}-{module_id}-{parent_id}.json",
            data,
        )

    def get_my_tasks(self, task_type: str = "assignedTo") -> Tuple[bool, List[Dict]]:
        """获取我的任务列表（老 API）

        Args:
            task_type: 任务类型，可选值: assignedTo(指派给我), openedBy(由我创建), finishedBy(由我完成), closedBy(由我关闭), canceledBy(由我取消)

        Returns:
            (success, tasks) 任务列表

        Example:
            >>> success, tasks = client.get_my_tasks("assignedTo")
            >>> for task in tasks:
            ...     print(f"[{task['id']}] {task['name']} ({task['status']})")
        """
        success, result = self.old_request("GET", f"/my-task-{task_type}.json")
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data.get("tasks", [])
        return False, []

    def get_my_bugs(
        self, bug_type: str = "assignedTo", order_by: str = "id_desc"
    ) -> Tuple[bool, List[Dict]]:
        """获取我的Bug列表（老 API）

        Args:
            bug_type: Bug类型，可选值: assignedTo(指派给我), openedBy(由我创建), resolvedBy(由我解决), closedBy(由我关闭)
            order_by: 排序字段，默认 id_desc

        Returns:
            (success, bugs) Bug列表

        Example:
            >>> success, bugs = client.get_my_bugs("assignedTo")
            >>> for bug in bugs:
            ...     print(f"[{bug['id']}] {bug['title']} ({bug['status']})")
        """
        success, result = self.old_request("GET", f"/my-bug-{bug_type}-{order_by}.json")
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data.get("bugs", [])
        return False, []

    def get_my_stories(self, story_type: str = "assignedTo") -> Tuple[bool, List[Dict]]:
        """获取我的需求列表（老 API）

        Args:
            story_type: 需求类型，可选值: assignedTo(指派给我), openedBy(由我创建), reviewedBy(由我评审), closedBy(由我关闭)

        Returns:
            (success, stories) 需求列表

        Example:
            >>> success, stories = client.get_my_stories("assignedTo")
            >>> for story in stories:
            ...     print(f"[{story['id']}] {story['title']} ({story['status']})")
        """
        success, result = self.old_request("GET", f"/my-story-{story_type}.json")
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data.get("stories", [])
        return False, []

    def get_my_projects(self) -> Tuple[bool, List[Dict]]:
        """获取我的项目列表（老 API）

        Returns:
            (success, projects) 项目列表

        Example:
            >>> success, projects = client.get_my_projects()
            >>> for project in projects:
            ...     print(f"[{project['id']}] {project['name']}")
        """
        success, result = self.old_request("GET", "/my-project.json")
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data.get("projects", [])
        return False, []

    # ==================== Bug 相关方法 ====================

    def get_project_bugs(
        self, project_id: str, status: str = "all"
    ) -> Tuple[bool, List[Dict]]:
        """获取项目的Bug列表（老 API）

        Args:
            project_id: 项目ID
            status: Bug状态，默认 "all" 获取所有状态

        Returns:
            (success, bugs) Bug列表

        Example:
            >>> success, bugs = client.get_project_bugs("1")
            >>> for bug in bugs:
            ...     print(f"[{bug['id']}] {bug['title']} ({bug['status']})")
        """
        success, result = self.old_request("GET", f"/project-bug-{project_id}.json")
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data.get("bugs", [])
        return False, []

    def get_bug(self, bug_id: str) -> Tuple[bool, Dict]:
        """获取Bug详情（老 API）

        Args:
            bug_id: BugID

        Returns:
            (success, bug_info) Bug详情

        Example:
            >>> success, bug = client.get_bug("1")
            >>> print(f"标题: {bug['title']}, 状态: {bug['status']}")
        """
        success, result = self.old_request("GET", f"/bug-view-{bug_id}.json")
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data.get("bug", {})
        return False, {}

    def create_bug(
        self,
        product_id: str,
        title: str,
        opened_build: str = "trunk",
        project_id: str = None,
        case_id: str = None,
        **kwargs,
    ) -> Tuple[bool, Dict]:
        """创建Bug（老 API）

        Args:
            product_id: 产品ID
            title: Bug标题
            opened_build: 影响版本，默认 "trunk"
            project_id: 项目ID（可选）
            case_id: 测试用例ID（可选，用于关联测试用例）
            **kwargs: 其他参数，如:
                - module: 模块ID
                - severity: 严重程度 (1-4)
                - pri: 优先级 (0-4)
                - type: Bug类型 (codeerror, config, install, security, performance, standard, automation, designdefect, others)
                - steps: 重现步骤
                - assignedTo: 指派给
                - deadline: 截止日期 (YYYY-MM-DD)

        Returns:
            (success, result) 创建结果

        Note:
            创建Bug需要产品存在且有权限。
            传入 case_id 可以关联测试用例。

        Example:
            >>> success, result = client.create_bug(
            ...     product_id="1",
            ...     title="测试Bug",
            ...     severity="3",
            ...     pri="3",
            ...     assignedTo="admin"
            ... )
            >>> # 从测试用例创建Bug
            >>> success, result = client.create_bug(
            ...     product_id="1",
            ...     title="从测试用例创建的Bug",
            ...     case_id="8",
            ...     steps="测试用例8发现的问题"
            ... )
        """
        data = {
            "product": product_id,
            "title": title,
            "openedBuild": opened_build,
        }
        if project_id:
            data["project"] = project_id
        if case_id:
            data["case"] = case_id
        data.update(kwargs)

        # 构建URL
        url = f"/bug-create-{product_id}-0"
        if project_id:
            url += f"-projectID={project_id}"
        url += ".json"

        success, result = self.old_request("POST", url, data)

        if success:
            return True, {"message": "创建Bug请求已发送", "result": result}
        else:
            return False, result

    def create_bug_from_testcase(
        self,
        case_id: str,
        product_id: str = None,
        title: str = None,
        **kwargs,
    ) -> Tuple[bool, Dict]:
        """从测试用例创建Bug（老 API）

        Args:
            case_id: 测试用例ID *必填
            product_id: 产品ID（可选，不传则从测试用例获取）
            title: Bug标题（可选，不传则使用测试用例标题）
            **kwargs: 其他参数，如:
                - severity: 严重程度 (1-4)
                - pri: 优先级 (0-4)
                - type: Bug类型
                - steps: 重现步骤（可选，不传则使用测试用例步骤）
                - assignedTo: 指派给
                - opened_build: 影响版本，默认 "trunk"

        Returns:
            (success, result) 创建结果

        Example:
            >>> success, result = client.create_bug_from_testcase(
            ...     case_id="8",
            ...     title="登录功能测试发现Bug",
            ...     severity="3"
            ... )
        """
        # 获取测试用例详情
        success, case = self.get_testcase(case_id)
        if not success:
            return False, {"message": f"测试用例 {case_id} 不存在"}

        # 使用测试用例信息填充默认值
        if not product_id:
            product_id = case.get("product", "0")

        if not title:
            title = f"[测试用例{case_id}] {case.get('title', '')}"

        # 准备Bug数据
        data = {
            "case": case_id,
            "product": product_id,
            "title": title,
            "openedBuild": kwargs.pop("opened_build", "trunk"),
        }

        # 如果测试用例有步骤，转换为Bug重现步骤
        if "steps" not in kwargs and case.get("steps"):
            steps_text = ""
            for step_id, step in case.get("steps", {}).items():
                if isinstance(step, dict):
                    desc = step.get("desc", "")
                    expect = step.get("expect", "")
                    if desc:
                        steps_text += f"{desc}"
                        if expect:
                            steps_text += f" (预期: {expect})"
                        steps_text += "\n"
            if steps_text:
                data["steps"] = steps_text.strip()

        data.update(kwargs)

        # 构建URL
        url = f"/bug-create-{product_id}-0.json"

        success, result = self.old_request("POST", url, data)

        if success:
            return True, {
                "message": "从测试用例创建Bug成功",
                "case_id": case_id,
                "result": result,
            }
        else:
            return False, result

    def resolve_bug(
        self,
        bug_id: str,
        resolution: str = "fixed",
        resolved_build: str = "trunk",
        comment: str = "",
    ) -> Tuple[bool, Dict]:
        """解决Bug（老 API）

        Args:
            bug_id: BugID
            resolution: 解决方案，可选值: fixed, postponed, willnotfix, duplicate, tostory
            resolved_build: 解决版本，默认 "trunk"
            comment: 解决备注

        Returns:
            (success, result)

        Note:
            解决后Bug状态变为 'resolved'。
            建议使用 .html 端点。

        Example:
            >>> success, result = client.resolve_bug("1", "fixed", "trunk", "已修复")
        """
        data = {
            "resolution": resolution,
            "resolvedBuild": resolved_build,
            "comment": comment,
        }

        url = f"{self.old_api_base}/bug-resolve-{bug_id}.html?onlybody=yes"
        response = self.session.post(
            url, data=data, params={"zentaosid": self.sid}, timeout=30
        )

        if response.status_code == 200:
            return True, {"message": "解决Bug成功", "status_code": response.status_code}
        else:
            return False, {
                "message": f"解决失败: HTTP {response.status_code}",
                "status_code": response.status_code,
            }

    def close_bug(self, bug_id: str, comment: str = "") -> Tuple[bool, Dict]:
        """关闭Bug（老 API）

        Args:
            bug_id: BugID
            comment: 关闭备注

        Returns:
            (success, result)

        Note:
            关闭后Bug状态变为 'closed'。

        Example:
            >>> success, result = client.close_bug("1", "已验证关闭")
        """
        data = {}
        if comment:
            data["comment"] = comment

        success, result = self.old_request("POST", f"/bug-close-{bug_id}.json", data)
        return success, result

    def activate_bug(self, bug_id: str, comment: str = "") -> Tuple[bool, Dict]:
        """激活Bug（老 API）

        Args:
            bug_id: BugID
            comment: 激活备注

        Returns:
            (success, result)

        Note:
            激活后Bug状态变为 'active'。

        Example:
            >>> success, result = client.activate_bug("1", "问题重现，重新打开")
        """
        data = {}
        if comment:
            data["comment"] = comment

        success, result = self.old_request("POST", f"/bug-activate-{bug_id}.json", data)
        return success, result

    def assign_bug(
        self, bug_id: str, assigned_to: str, comment: str = ""
    ) -> Tuple[bool, Dict]:
        """指派Bug（老 API）

        Args:
            bug_id: BugID
            assigned_to: 指派给谁（用户名）
            comment: 指派备注

        Returns:
            (success, result)

        Example:
            >>> success, result = client.assign_bug("1", "zhangsan", "请处理")
        """
        data = {"assignedTo": assigned_to}
        if comment:
            data["comment"] = comment

        url = f"{self.old_api_base}/bug-assignTo-{bug_id}.json"
        response = self.session.post(
            url, data=data, params={"zentaosid": self.sid}, timeout=30
        )

        if response.status_code == 200:
            return True, {"message": "指派Bug成功", "status_code": response.status_code}
        else:
            return False, {
                "message": f"指派失败: HTTP {response.status_code}",
                "status_code": response.status_code,
            }

    def confirm_bug(self, bug_id: str, comment: str = "") -> Tuple[bool, Dict]:
        """确认Bug（老 API）

        Args:
            bug_id: BugID
            comment: 确认备注

        Returns:
            (success, result)

        Example:
            >>> success, result = client.confirm_bug("1", "确认是Bug")
        """
        data = {}
        if comment:
            data["comment"] = comment

        success, result = self.old_request(
            "POST", f"/bug-confirmBug-{bug_id}.json", data
        )
        return success, result

    def delete_bug(self, bug_id: str) -> Tuple[bool, Dict]:
        """删除Bug（老 API）

        Args:
            bug_id: BugID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.delete_bug("1")
        """
        return self.old_request("GET", f"/bug-delete-{bug_id}-yes.json")

    # ==================== 产品相关方法 ====================

    def get_products(self) -> Tuple[bool, List[Dict]]:
        """获取所有产品列表（老 API）

        Returns:
            (success, products) 产品列表

        Example:
            >>> success, products = client.get_products()
            >>> for pid, name in products.items():
            ...     print(f"[{pid}] {name}")
        """
        success, result = self.old_request("GET", "/product-all.json")
        if success and "data" in result:
            data = json.loads(result["data"])
            products = data.get("products", {})
            return True, products
        return False, {}

    def get_product(self, product_id: str) -> Tuple[bool, Dict]:
        """获取产品详情（老 API）

        Args:
            product_id: 产品ID

        Returns:
            (success, product_info) 产品详情

        Example:
            >>> success, product = client.get_product("1")
            >>> print(f"产品名: {product['name']}")
        """
        success, result = self.old_request("GET", f"/product-view-{product_id}.json")
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data.get("product", {})
        return False, {}

    def create_product(
        self,
        name: str,
        code: str,
        type: str = "normal",
        po: str = "",
        qd: str = "",
        rd: str = "",
        status: str = "normal",
        desc: str = "",
    ) -> Tuple[bool, Dict]:
        """创建产品（老 API）

        Args:
            name: 产品名称
            code: 产品代码
            type: 产品类型 (normal, branch, platform)
            po: 产品负责人
            qd: 测试负责人
            rd: 发布负责人
            status: 状态 (normal, closed)
            desc: 产品描述

        Returns:
            (success, result)

        Example:
            >>> success, result = client.create_product(
            ...     name="新产品",
            ...     code="NEW",
            ...     po="admin"
            ... )
        """
        data = {
            "name": name,
            "code": code,
            "type": type,
            "status": status,
            "desc": desc,
        }
        if po:
            data["PO"] = po
        if qd:
            data["QD"] = qd
        if rd:
            data["RD"] = rd

        return self.old_request("POST", "/product-create.json", data)

    def edit_product(self, product_id: str, **kwargs) -> Tuple[bool, Dict]:
        """编辑产品（老 API）

        Args:
            product_id: 产品ID
            **kwargs: 要修改的字段 (name, code, type, PO, QD, RD, status, desc等)

        Returns:
            (success, result)

        Example:
            >>> success, result = client.edit_product("1", name="新名称", status="closed")
        """
        return self.old_request("POST", f"/product-edit-{product_id}.json", kwargs)

    def close_product(self, product_id: str) -> Tuple[bool, Dict]:
        """关闭产品（老 API）

        Args:
            product_id: 产品ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.close_product("1")
        """
        return self.old_request("POST", f"/product-close-{product_id}.json")

    def delete_product(self, product_id: str) -> Tuple[bool, Dict]:
        """删除产品（老 API）

        Args:
            product_id: 产品ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.delete_product("1")
        """
        return self.old_request("GET", f"/product-delete-{product_id}-yes.json")

    # ==================== 需求相关方法 ====================

    def get_story(self, story_id: str) -> Tuple[bool, Dict]:
        """获取需求详情（老 API）

        Args:
            story_id: 需求ID

        Returns:
            (success, story_info) 需求详情

        Example:
            >>> success, story = client.get_story("1")
            >>> print(f"需求标题: {story['title']}")
        """
        success, result = self.old_request("GET", f"/story-view-{story_id}.json")
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data.get("story", {})
        return False, {}

    def create_story(
        self,
        product_id: str,
        title: str,
        module: str = "0",
        plan: str = "0",
        execution_id: str = "0",
        branch: str = "0",
        **kwargs,
    ) -> Tuple[bool, Dict]:
        """创建需求（老 API）

        Args:
            product_id: 产品ID
            title: 需求标题
            module: 模块ID，默认 "0"
            plan: 计划ID，默认 "0"
            execution_id: 执行/项目ID，默认 "0"
            branch: 分支ID，默认 "0"
            **kwargs: 其他参数:
                - source: 需求来源
                - pri: 优先级 (0-4)
                - estimate: 预计工时
                - spec: 需求描述
                - verify: 验收标准
                - assignedTo: 指派给
                - reviewer: 评审人

        Returns:
            (success, result)

        Example:
            >>> success, result = client.create_story(
            ...     product_id="1",
            ...     title="新需求",
            ...     pri="3",
            ...     spec="需求描述"
            ... )
        """
        data = {
            "product": product_id,
            "title": title,
            "module": module,
        }
        data.update(kwargs)

        # URL: /story-create-{product}-{module}-{story}-{plan}-{execution}-{branch}-{module}-{type}.json
        return self.old_request(
            "POST",
            f"/story-create-{product_id}-{module}-0-{plan}-{execution_id}-{branch}-{module}-0-story.json",
            data,
        )

    def edit_story(self, story_id: str, **kwargs) -> Tuple[bool, Dict]:
        """编辑需求（老 API）

        Args:
            story_id: 需求ID
            **kwargs: 要修改的字段

        Returns:
            (success, result)

        Example:
            >>> success, result = client.edit_story("1", title="新标题", pri="2")
        """
        return self.old_request("POST", f"/story-edit-{story_id}.json", kwargs)

    def close_story(self, story_id: str) -> Tuple[bool, Dict]:
        """关闭需求（老 API）

        Args:
            story_id: 需求ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.close_story("1")
        """
        return self.old_request("POST", f"/story-close-{story_id}.json")

    def activate_story(self, story_id: str) -> Tuple[bool, Dict]:
        """激活需求（老 API）

        Args:
            story_id: 需求ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.activate_story("1")
        """
        return self.old_request("POST", f"/story-activate-{story_id}.json")

    def delete_story(self, story_id: str) -> Tuple[bool, Dict]:
        """删除需求（老 API）

        Args:
            story_id: 需求ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.delete_story("1")
        """
        return self.old_request("GET", f"/story-delete-{story_id}-yes.json")

    # ==================== 计划相关方法 ====================

    def get_plans(self, product_id: str) -> Tuple[bool, List[Dict]]:
        """获取产品计划列表（老 API）

        Args:
            product_id: 产品ID

        Returns:
            (success, plans) 计划列表

        Example:
            >>> success, plans = client.get_plans("1")
            >>> for plan in plans:
            ...     print(f"[{plan['id']}] {plan['title']}")
        """
        success, result = self.old_request(
            "GET", f"/productplan-browse-{product_id}.json"
        )
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data.get("plans", [])
        return False, []

    def create_plan(
        self,
        product_id: str,
        title: str,
        begin: str = "",
        end: str = "",
        desc: str = "",
    ) -> Tuple[bool, Dict]:
        """创建产品计划（老 API）

        Args:
            product_id: 产品ID
            title: 计划标题
            begin: 开始日期 (YYYY-MM-DD)
            end: 结束日期 (YYYY-MM-DD)
            desc: 计划描述

        Returns:
            (success, result)

        Example:
            >>> success, result = client.create_plan(
            ...     product_id="1",
            ...     title="1.0版本",
            ...     begin="2026-03-01",
            ...     end="2026-03-31"
            ... )
        """
        data = {
            "product": product_id,
            "title": title,
            "begin": begin,
            "end": end,
            "desc": desc,
        }
        return self.old_request("POST", f"/productplan-create-{product_id}.json", data)

    def delete_plan(self, plan_id: str) -> Tuple[bool, Dict]:
        """删除产品计划（老 API）

        Args:
            plan_id: 计划ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.delete_plan("1")
        """
        return self.old_request("GET", f"/productplan-delete-{plan_id}-yes.json")

    # ==================== 项目管理方法 ====================

    def create_project(
        self,
        name: str,
        begin: str,
        end: str,
        code: str = "",
        days: str = "",
        products: List[str] = None,
        plans: List[str] = None,
        desc: str = "",
        **kwargs,
    ) -> Tuple[bool, Dict]:
        """创建项目（老 API）

        Args:
            name: 项目名称
            begin: 开始日期 (YYYY-MM-DD)
            end: 结束日期 (YYYY-MM-DD)
            code: 项目代号
            days: 可用工时天数
            products: 关联产品ID列表
            plans: 关联计划ID列表（需与products一一对应）
            desc: 项目描述
            **kwargs: 其他参数 (acl, whitelist, team, etc.)

        Returns:
            (success, result)

        Example:
            >>> success, result = client.create_project(
            ...     name="V1.0开发项目",
            ...     begin="2026-04-01",
            ...     end="2026-04-30",
            ...     code="V1",
            ...     days="22",
            ...     products=["1"],
            ...     plans=["1"]
            ... )
        """
        data = {
            "name": name,
            "begin": begin,
            "end": end,
        }
        if code:
            data["code"] = code
        if days:
            data["days"] = days
        if desc:
            data["desc"] = desc

        # 关联产品和计划
        if products:
            for i, product_id in enumerate(products):
                data[f"products[{i}]"] = product_id
                if plans and i < len(plans):
                    data[f"plans[{i}]"] = plans[i]

        data.update(kwargs)

        return self.old_request("POST", "/project-create.json", data)

    def get_project(self, project_id: str) -> Tuple[bool, Dict]:
        """获取项目详情（老 API）

        Args:
            project_id: 项目ID

        Returns:
            (success, project)

        Example:
            >>> success, project = client.get_project("1")
            >>> print(project['name'])
        """
        success, result = self.old_request("GET", f"/project-view-{project_id}.json")
        if success and "data" in result:
            data = result["data"]
            if isinstance(data, str):
                data = json.loads(data)
            return True, data.get("project", data)
        return success, result

    def start_project(self, project_id: str) -> Tuple[bool, Dict]:
        """启动项目（老 API）

        Args:
            project_id: 项目ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.start_project("1")
        """
        return self.old_request("GET", f"/project-start-{project_id}.json")

    def close_project(self, project_id: str) -> Tuple[bool, Dict]:
        """关闭项目（老 API）

        Args:
            project_id: 项目ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.close_project("1")
        """
        return self.old_request("GET", f"/project-close-{project_id}.json")

    # ==================== 发布相关方法 ====================

    def get_releases(self, product_id: str) -> Tuple[bool, List[Dict]]:
        """获取产品发布列表（老 API）

        Args:
            product_id: 产品ID

        Returns:
            (success, releases) 发布列表

        Example:
            >>> success, releases = client.get_releases("1")
            >>> for release in releases:
            ...     print(f"[{release['id']}] {release['name']}")
        """
        success, result = self.old_request("GET", f"/release-browse-{product_id}.json")
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data.get("releases", [])
        return False, []

    # ==================== 测试相关方法 ====================

    def get_testcases(
        self, product_id: str, browse_type: str = "all"
    ) -> Tuple[bool, List[Dict]]:
        """获取测试用例列表（老 API）

        Args:
            product_id: 产品ID
            browse_type: 浏览类型 (all, bymodule, assignedtome)

        Returns:
            (success, cases) 测试用例列表

        Example:
            >>> success, cases = client.get_testcases("1")
            >>> for case in cases:
            ...     print(f"[{case['id']}] {case['title']}")
        """
        success, result = self.old_request(
            "GET", f"/testcase-browse-{product_id}-{browse_type}.json"
        )
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data.get("cases", [])
        return False, []

    def get_testcase(self, case_id: str) -> Tuple[bool, Dict]:
        """获取测试用例详情（老 API）

        Args:
            case_id: 用例ID

        Returns:
            (success, case_info) 用例详情

        Example:
            >>> success, case = client.get_testcase("1")
            >>> print(f"标题: {case['title']}")
        """
        success, result = self.old_request("GET", f"/testcase-view-{case_id}.json")
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data.get("case", {})
        return False, {}

    def create_testcase(
        self,
        product_id: str,
        title: str,
        case_type: str = "feature",
        module: str = "0",
        story: str = "0",
        branch: str = "0",
        **kwargs,
    ) -> Tuple[bool, Dict]:
        """创建测试用例（老 API）

        Args:
            product_id: 产品ID
            title: 用例标题
            case_type: 用例类型 (feature, performance, config, install, security, interface, unit, other)
            module: 模块ID，默认 "0"
            story: 需求ID，默认 "0"
            branch: 分支ID，默认 "0"
            **kwargs: 其他参数:
                - stage: 适用阶段 (unittest, feature, intergrate, system, smoke, bvt)
                - pri: 优先级 (0-4)
                - precondition: 前置条件
                - steps: 用例步骤（字符串，按换行分割）
                - expect: 预期结果（字符串，按换行分割）
                - steps_list: 步骤列表（列表格式，与steps二选一）
                - expects_list: 预期结果列表（列表格式，与expect二选一）

        Returns:
            (success, result)

        Example:
            >>> # 字符串格式（自动按换行分割）
            >>> success, result = client.create_testcase(
            ...     product_id="1",
            ...     title="测试登录功能",
            ...     case_type="feature",
            ...     steps="1. 打开登录页面\\n2. 输入用户名密码\\n3. 点击登录",
            ...     expect="登录成功"
            ... )
            >>> # 列表格式（精确控制）
            >>> success, result = client.create_testcase(
            ...     product_id="1",
            ...     title="测试登录功能",
            ...     module="1",
            ...     story="5",
            ...     steps_list=["打开登录页面", "输入用户名密码", "点击登录"],
            ...     expects_list=["显示登录表单", "输入成功", "登录成功"]
            ... )
        """
        data = {
            "product": product_id,
            "title": title,
            "type": case_type,
        }

        # 处理步骤和预期结果
        steps_text = kwargs.pop("steps", None)
        expect_text = kwargs.pop("expect", None)
        steps_list = kwargs.pop("steps_list", None)
        expects_list = kwargs.pop("expects_list", None)

        # 转换步骤格式
        if steps_list:
            # 直接使用列表
            for i, step in enumerate(steps_list, start=1):
                data[f"steps[{i}]"] = step
        elif steps_text:
            # 按换行分割
            steps = [s.strip() for s in steps_text.split("\n") if s.strip()]
            for i, step in enumerate(steps, start=1):
                data[f"steps[{i}]"] = step

        # 转换预期结果格式
        if expects_list:
            # 直接使用列表
            for i, exp in enumerate(expects_list, start=1):
                data[f"expects[{i}]"] = exp
        elif expect_text:
            # 按换行分割
            expects = [e.strip() for e in expect_text.split("\n") if e.strip()]
            for i, exp in enumerate(expects, start=1):
                data[f"expects[{i}]"] = exp

        # 其他参数
        data.update(kwargs)

        # 构建URL: /testcase-create-{product}-{module}-{story}-{branch}-{0}
        return self.old_request(
            "POST",
            f"/testcase-create-{product_id}-{module}-{story}-{branch}-0.json",
            data,
        )

    def delete_testcase(self, case_id: str, confirm: str = "yes") -> Tuple[bool, Dict]:
        """删除测试用例（老 API）

        Args:
            case_id: 用例ID
            confirm: 确认删除，可选值: "yes"（删除）| "no"（不删除），默认 "yes"

        Returns:
            (success, result)

        Note:
            - 禅道使用软删除机制，删除后用例的 deleted 字段标记为 '1'
            - 删除后用例不再显示在列表中，但数据仍保留在数据库
            - 返回 HTML 响应表示删除成功

        Example:
            >>> success, result = client.delete_testcase("10")
            >>> # 验证删除
            >>> success, case = client.get_testcase("10")
            >>> if case.get('deleted') == '1':
            ...     print("已删除")
        """
        return self.old_request("GET", f"/testcase-delete-{case_id}-{confirm}.json")

    def get_testsuites(self, product_id: str) -> Tuple[bool, List[Dict]]:
        """获取测试套件列表（老 API）

        Args:
            product_id: 产品ID

        Returns:
            (success, suites) 测试套件列表

        Example:
            >>> success, suites = client.get_testsuites("1")
            >>> for suite in suites:
            ...     print(f"[{suite['id']}] {suite['name']}")
        """
        success, result = self.old_request(
            "GET", f"/testsuite-browse-{product_id}.json"
        )
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data.get("suites", [])
        return False, []

    def get_testsuite(self, suite_id: str) -> Tuple[bool, Dict]:
        """获取测试套件详情（老 API）

        Args:
            suite_id: 套件ID

        Returns:
            (success, suite_info) 套件详情

        Example:
            >>> success, suite = client.get_testsuite("1")
            >>> print(f"套件名: {suite['name']}")
        """
        success, result = self.old_request("GET", f"/testsuite-view-{suite_id}.json")
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data.get("suite", {})
        return False, {}

    def create_testsuite(
        self, product_id: str, name: str, desc: str = ""
    ) -> Tuple[bool, Dict]:
        """创建测试套件（老 API）

        Args:
            product_id: 产品ID
            name: 套件名称
            desc: 套件描述

        Returns:
            (success, result)

        Example:
            >>> success, result = client.create_testsuite("1", "冒烟测试套件", "冒烟测试用例集合")
        """
        data = {"product": product_id, "name": name, "desc": desc}
        return self.old_request("POST", f"/testsuite-create-{product_id}.json", data)

    def delete_testsuite(self, suite_id: str) -> Tuple[bool, Dict]:
        """删除测试套件（老 API）

        Args:
            suite_id: 套件ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.delete_testsuite("1")
        """
        return self.old_request("GET", f"/testsuite-delete-{suite_id}-yes.json")

    def get_testtasks(
        self, product_id: str, task_type: str = "all"
    ) -> Tuple[bool, List[Dict]]:
        """获取测试任务列表（老 API）

        Args:
            product_id: 产品ID
            task_type: 任务类型 (all, wait, doing, done, blocked)

        Returns:
            (success, tasks) 测试任务列表

        Example:
            >>> success, tasks = client.get_testtasks("1")
            >>> for task in tasks:
            ...     print(f"[{task['id']}] {task['name']}")
        """
        success, result = self.old_request(
            "GET", f"/testtask-browse-{product_id}-{task_type}.json"
        )
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data.get("tasks", [])
        return False, []

    def get_testtask(self, task_id: str) -> Tuple[bool, Dict]:
        """获取测试任务详情（老 API）

        Args:
            task_id: 任务ID

        Returns:
            (success, task_info) 任务详情

        Example:
            >>> success, task = client.get_testtask("1")
            >>> print(f"任务名: {task['name']}")
        """
        success, result = self.old_request("GET", f"/testtask-view-{task_id}.json")
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data.get("task", {})
        return False, {}

    def create_testtask(
        self, product_id: str, name: str, begin: str = "", end: str = "", desc: str = ""
    ) -> Tuple[bool, Dict]:
        """创建测试任务（老 API）

        Args:
            product_id: 产品ID
            name: 任务名称
            begin: 开始日期 (YYYY-MM-DD)
            end: 结束日期 (YYYY-MM-DD)
            desc: 任务描述

        Returns:
            (success, result) 注意：可能返回HTML

        Example:
            >>> success, result = client.create_testtask(
            ...     product_id="1",
            ...     name="Sprint1测试",
            ...     begin="2026-03-01",
            ...     end="2026-03-15"
            ... )
        """
        data = {
            "product": product_id,
            "name": name,
            "begin": begin,
            "end": end,
            "desc": desc,
        }
        return self.old_request("POST", f"/testtask-create-{product_id}.json", data)

    def delete_testtask(self, task_id: str) -> Tuple[bool, Dict]:
        """删除测试任务（老 API）

        Args:
            task_id: 任务ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.delete_testtask("1")
        """
        return self.old_request("GET", f"/testtask-delete-{task_id}-yes.json")

    def start_testtask(self, task_id: str) -> Tuple[bool, Dict]:
        """开始测试任务（老 API）

        Args:
            task_id: 任务ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.start_testtask("1")
        """
        return self.old_request("POST", f"/testtask-start-{task_id}.json")

    def close_testtask(self, task_id: str) -> Tuple[bool, Dict]:
        """关闭测试任务（老 API）

        Args:
            task_id: 任务ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.close_testtask("1")
        """
        return self.old_request("POST", f"/testtask-close-{task_id}.json")

    def block_testtask(self, task_id: str) -> Tuple[bool, Dict]:
        """阻塞测试任务（老 API）

        Args:
            task_id: 任务ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.block_testtask("1")
        """
        return self.old_request("POST", f"/testtask-block-{task_id}.json")

    def activate_testtask(self, task_id: str) -> Tuple[bool, Dict]:
        """激活测试任务（老 API）

        Args:
            task_id: 任务ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.activate_testtask("1")
        """
        return self.old_request("POST", f"/testtask-activate-{task_id}.json")

    def get_testreports(
        self, product_id: str, project_id: str = "0"
    ) -> Tuple[bool, List[Dict]]:
        """获取测试报告列表（老 API）

        Args:
            product_id: 产品ID
            project_id: 项目ID，默认 "0"

        Returns:
            (success, reports) 测试报告列表

        Example:
            >>> success, reports = client.get_testreports("1")
            >>> for report in reports:
            ...     print(f"[{report['id']}] {report['title']}")
        """
        success, result = self.old_request(
            "GET", f"/testreport-browse-{product_id}-product-{project_id}.json"
        )
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data.get("reports", [])
        return False, []

    def delete_testreport(self, report_id: str) -> Tuple[bool, Dict]:
        """删除测试报告（老 API）

        Args:
            report_id: 报告ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.delete_testreport("1")
        """
        return self.old_request("GET", f"/testreport-delete-{report_id}-yes.json")

    # ==================== 任务模块补充方法 ====================

    def edit_task(self, task_id: str, **kwargs) -> Tuple[bool, Dict]:
        """编辑任务（老 API）

        Args:
            task_id: 任务ID
            **kwargs: 要修改的字段 (name, type, pri, estimate, left, assignedTo, status, etc.)

        Returns:
            (success, result)

        Example:
            >>> success, result = client.edit_task("10", name="新任务名", pri="2")
        """
        return self.old_request("POST", f"/task-edit-{task_id}.json", kwargs)

    def move_task(self, task_id: str, project_id: str) -> Tuple[bool, Dict]:
        """移动任务到其他项目（老 API）

        Args:
            task_id: 任务ID
            project_id: 目标项目ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.move_task("10", "2")
        """
        return self.old_request("POST", f"/task-move-{task_id}-{project_id}.json")

    def copy_task(self, task_id: str, project_id: str = None) -> Tuple[bool, Dict]:
        """复制任务（老 API）

        Args:
            task_id: 任务ID
            project_id: 目标项目ID（可选，不传则复制到当前项目）

        Returns:
            (success, result)

        Example:
            >>> success, result = client.copy_task("10", "2")
        """
        if project_id:
            return self.old_request("POST", f"/task-copy-{task_id}-{project_id}.json")
        return self.old_request("POST", f"/task-copy-{task_id}.json")

    def get_task_subtasks(self, task_id: str) -> Tuple[bool, List[Dict]]:
        """获取任务的子任务列表（老 API）

        Args:
            task_id: 任务ID

        Returns:
            (success, subtasks) 子任务列表

        Example:
            >>> success, subtasks = client.get_task_subtasks("10")
            >>> for task in subtasks:
            ...     print(f"[{task['id']}] {task['name']}")
        """
        success, result = self.old_request("GET", f"/task-viewSubtasks-{task_id}.json")
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data.get("children", [])
        return False, []

    def link_task_story(self, task_id: str, story_id: str) -> Tuple[bool, Dict]:
        """任务关联需求（老 API）

        Args:
            task_id: 任务ID
            story_id: 需求ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.link_task_story("10", "5")
        """
        return self.old_request("POST", f"/task-linkStory-{task_id}-{story_id}.json")

    def link_task_bug(self, task_id: str, bug_id: str) -> Tuple[bool, Dict]:
        """任务关联Bug（老 API）

        Args:
            task_id: 任务ID
            bug_id: BugID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.link_task_bug("10", "3")
        """
        return self.old_request("POST", f"/task-linkBug-{task_id}-{bug_id}.json")

    def get_task_history(self, task_id: str) -> Tuple[bool, List[Dict]]:
        """获取任务历史记录（老 API）

        Args:
            task_id: 任务ID

        Returns:
            (success, history) 历史记录列表

        Example:
            >>> success, history = client.get_task_history("10")
            >>> for record in history:
            ...     print(f"{record['date']}: {record['action']}")
        """
        success, result = self.old_request("GET", f"/task-history-{task_id}.json")
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data.get("history", [])
        return False, []

    # ==================== Bug模块补充方法 ====================

    def edit_bug(self, bug_id: str, **kwargs) -> Tuple[bool, Dict]:
        """编辑Bug（老 API）

        Args:
            bug_id: BugID
            **kwargs: 要修改的字段 (title, severity, pri, type, status, assignedTo, etc.)

        Returns:
            (success, result)

        Example:
            >>> success, result = client.edit_bug("1", title="新标题", severity="2")
        """
        return self.old_request("POST", f"/bug-edit-{bug_id}.json", kwargs)

    def link_bug_story(self, bug_id: str, story_id: str) -> Tuple[bool, Dict]:
        """Bug关联需求（老 API）

        Args:
            bug_id: BugID
            story_id: 需求ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.link_bug_story("1", "5")
        """
        return self.old_request("POST", f"/bug-linkStory-{bug_id}-{story_id}.json")

    def unlink_bug_story(self, bug_id: str, story_id: str) -> Tuple[bool, Dict]:
        """取消Bug关联需求（老 API）

        Args:
            bug_id: BugID
            story_id: 需求ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.unlink_bug_story("1", "5")
        """
        return self.old_request("GET", f"/bug-unlinkStory-{bug_id}-{story_id}.json")

    def link_bug_task(self, bug_id: str, task_id: str) -> Tuple[bool, Dict]:
        """Bug关联任务（老 API）

        Args:
            bug_id: BugID
            task_id: 任务ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.link_bug_task("1", "10")
        """
        return self.old_request("POST", f"/bug-linkTask-{bug_id}-{task_id}.json")

    def unlink_bug_task(self, bug_id: str, task_id: str) -> Tuple[bool, Dict]:
        """取消Bug关联任务（老 API）

        Args:
            bug_id: BugID
            task_id: 任务ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.unlink_bug_task("1", "10")
        """
        return self.old_request("GET", f"/bug-unlinkTask-{bug_id}-{task_id}.json")

    def get_bug_statistics(
        self, product_id: str, branch: str = "0"
    ) -> Tuple[bool, Dict]:
        """获取Bug统计信息（老 API）

        Args:
            product_id: 产品ID
            branch: 分支ID，默认 "0"

        Returns:
            (success, statistics) Bug统计信息

        Example:
            >>> success, stats = client.get_bug_statistics("1")
            >>> print(f"总Bug数: {stats['total']}, 未解决: {stats['active']}")
        """
        success, result = self.old_request(
            "GET", f"/bug-statistic-{product_id}-{branch}.json"
        )
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data
        return False, {}

    def add_bug_comment(self, bug_id: str, comment: str) -> Tuple[bool, Dict]:
        """添加Bug评论（老 API）

        Args:
            bug_id: BugID
            comment: 评论内容

        Returns:
            (success, result)

        Example:
            >>> success, result = client.add_bug_comment("1", "这是一个测试评论")
        """
        return self.old_request(
            "POST", f"/bug-addComment-{bug_id}.json", {"comment": comment}
        )

    # ==================== 需求模块补充方法 ====================

    def change_story(self, story_id: str, **kwargs) -> Tuple[bool, Dict]:
        """变更需求（老 API）

        Args:
            story_id: 需求ID
            **kwargs: 变更参数 (title, spec, verify, etc.)

        Returns:
            (success, result)

        Example:
            >>> success, result = client.change_story("1", title="新标题", spec="新描述")
        """
        return self.old_request("POST", f"/story-change-{story_id}.json", kwargs)

    def review_story(
        self, story_id: str, result: str, comment: str = ""
    ) -> Tuple[bool, Dict]:
        """评审需求（老 API）

        Args:
            story_id: 需求ID
            result: 评审结果 (pass, revert, clarify, reject)
            comment: 评审意见

        Returns:
            (success, result)

        Example:
            >>> success, result = client.review_story("1", "pass", "评审通过")
        """
        data = {"result": result}
        if comment:
            data["comment"] = comment
        return self.old_request("POST", f"/story-review-{story_id}.json", data)

    def get_story_tasks(
        self, story_id: str, project_id: str = "0"
    ) -> Tuple[bool, List[Dict]]:
        """获取需求关联的任务（老 API）

        Args:
            story_id: 需求ID
            project_id: 项目ID，默认 "0" 获取所有项目

        Returns:
            (success, tasks) 任务列表

        Example:
            >>> success, tasks = client.get_story_tasks("1")
            >>> for task in tasks:
            ...     print(f"[{task['id']}] {task['name']}")
        """
        success, result = self.old_request(
            "GET", f"/story-tasks-{story_id}-{project_id}.json"
        )
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data.get("tasks", [])
        return False, []

    def get_story_bugs(self, story_id: str) -> Tuple[bool, List[Dict]]:
        """获取需求关联的Bug（老 API）

        Args:
            story_id: 需求ID

        Returns:
            (success, bugs) Bug列表

        Example:
            >>> success, bugs = client.get_story_bugs("1")
            >>> for bug in bugs:
            ...     print(f"[{bug['id']}] {bug['title']}")
        """
        success, result = self.old_request("GET", f"/story-bugs-{story_id}.json")
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data.get("bugs", [])
        return False, []

    def get_story_cases(self, story_id: str) -> Tuple[bool, List[Dict]]:
        """获取需求关联的测试用例（老 API）

        Args:
            story_id: 需求ID

        Returns:
            (success, cases) 测试用例列表

        Example:
            >>> success, cases = client.get_story_cases("1")
            >>> for case in cases:
            ...     print(f"[{case['id']}] {case['title']}")
        """
        success, result = self.old_request("GET", f"/story-cases-{story_id}.json")
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data.get("cases", [])
        return False, []

    def link_story_project(self, story_id: str, project_id: str) -> Tuple[bool, Dict]:
        """需求关联项目（老 API）

        Args:
            story_id: 需求ID
            project_id: 项目ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.link_story_project("1", "2")
        """
        return self.old_request(
            "POST", f"/story-linkProject-{story_id}-{project_id}.json"
        )

    def unlink_story_project(self, story_id: str, project_id: str) -> Tuple[bool, Dict]:
        """取消需求关联项目（老 API）

        Args:
            story_id: 需求ID
            project_id: 项目ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.unlink_story_project("1", "2")
        """
        return self.old_request(
            "GET", f"/story-unlinkProject-{story_id}-{project_id}.json"
        )

    # ==================== 项目模块补充方法 ====================

    def edit_project(self, project_id: str, **kwargs) -> Tuple[bool, Dict]:
        """编辑项目（老 API）

        Args:
            project_id: 项目ID
            **kwargs: 要修改的字段 (name, code, begin, end, days, status, etc.)

        Returns:
            (success, result)

        Example:
            >>> success, result = client.edit_project("1", name="新项目名", status="doing")
        """
        return self.old_request("POST", f"/project-edit-{project_id}.json", kwargs)

    def get_project_stories(
        self, project_id: str, order_by: str = "id_desc"
    ) -> Tuple[bool, List[Dict]]:
        """获取项目需求列表（老 API）

        Args:
            project_id: 项目ID
            order_by: 排序方式，默认 "id_desc"

        Returns:
            (success, stories) 需求列表

        Example:
            >>> success, stories = client.get_project_stories("1")
            >>> for story in stories:
            ...     print(f"[{story['id']}] {story['title']}")
        """
        success, result = self.old_request(
            "GET", f"/project-story-{project_id}-{order_by}.json"
        )
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data.get("stories", [])
        return False, []

    def manage_project_members(
        self, project_id: str, members: List[Dict]
    ) -> Tuple[bool, Dict]:
        """管理项目成员（老 API）

        Args:
            project_id: 项目ID
            members: 成员列表，每个成员包含:
                - account: 用户账号
                - role: 角色 (如 developer, tester, pm)
                - hours: 可用工时

        Returns:
            (success, result)

        Example:
            >>> members = [
            ...     {"account": "user1", "role": "developer", "hours": "8"},
            ...     {"account": "user2", "role": "tester", "hours": "8"}
            ... ]
            >>> success, result = client.manage_project_members("1", members)
        """
        data = {}
        for i, member in enumerate(members):
            data[f"accounts[{i}]"] = member.get("account", "")
            data[f"roles[{i}]"] = member.get("role", "developer")
            data[f"hours[{i}]"] = member.get("hours", "8")

        return self.old_request(
            "POST", f"/project-manageMembers-{project_id}.json", data
        )

    def link_project_story(self, project_id: str, story_id: str) -> Tuple[bool, Dict]:
        """项目关联需求（老 API）

        Args:
            project_id: 项目ID
            story_id: 需求ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.link_project_story("1", "5")
        """
        return self.old_request(
            "POST", f"/project-linkStory-{project_id}.json", {"story": story_id}
        )

    def unlink_project_story(self, project_id: str, story_id: str) -> Tuple[bool, Dict]:
        """取消项目关联需求（老 API）

        Args:
            project_id: 项目ID
            story_id: 需求ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.unlink_project_story("1", "5")
        """
        return self.old_request(
            "GET", f"/project-unlinkStory-{project_id}-{story_id}.json"
        )

    def get_project_team(self, project_id: str) -> Tuple[bool, List[Dict]]:
        """获取项目团队成员（老 API）

        Args:
            project_id: 项目ID

        Returns:
            (success, team) 团队成员列表

        Example:
            >>> success, team = client.get_project_team("1")
            >>> for member in team:
            ...     print(f"{member['account']}: {member['role']}")
        """
        success, result = self.old_request("GET", f"/project-team-{project_id}.json")
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data.get("team", [])
        return False, []

    def get_project_dynamic(
        self, project_id: str, dynamic_type: str = "all"
    ) -> Tuple[bool, List[Dict]]:
        """获取项目动态（老 API）

        Args:
            project_id: 项目ID
            dynamic_type: 动态类型 (all, today, yesterday, thisweek, lastweek, thismonth, lastmonth)

        Returns:
            (success, dynamics) 动态列表

        Example:
            >>> success, dynamics = client.get_project_dynamic("1", "today")
            >>> for dynamic in dynamics:
            ...     print(f"{dynamic['date']}: {dynamic['action']}")
        """
        success, result = self.old_request(
            "GET", f"/project-dynamic-{project_id}-{dynamic_type}.json"
        )
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data.get("dynamics", [])
        return False, []

    # ==================== 测试用例模块补充方法 ====================

    def edit_testcase(self, case_id: str, **kwargs) -> Tuple[bool, Dict]:
        """编辑测试用例（老 API）

        Args:
            case_id: 用例ID
            **kwargs: 要修改的字段 (title, type, pri, module, story, steps, expects, etc.)

        Returns:
            (success, result)

        Example:
            >>> success, result = client.edit_testcase("1", title="新标题", pri="2")
        """
        return self.old_request("POST", f"/testcase-edit-{case_id}.json", kwargs)

    def batch_create_testcases(
        self, product_id: str, cases: List[Dict]
    ) -> Tuple[bool, Dict]:
        """批量创建测试用例（老 API）

        Args:
            product_id: 产品ID
            cases: 用例列表，每个用例包含:
                - title: 用例标题
                - type: 用例类型
                - module: 模块ID
                - story: 需求ID
                - steps: 步骤列表
                - expects: 预期结果列表

        Returns:
            (success, result)

        Example:
            >>> cases = [
            ...     {"title": "测试用例1", "type": "feature"},
            ...     {"title": "测试用例2", "type": "performance"}
            ... ]
            >>> success, result = client.batch_create_testcases("1", cases)
        """
        data = {}
        for i, case in enumerate(cases):
            data[f"title[{i}]"] = case.get("title", "")
            data[f"type[{i}]"] = case.get("type", "feature")
            if case.get("module"):
                data[f"module[{i}]"] = case.get("module")
            if case.get("story"):
                data[f"story[{i}]"] = case.get("story")

        return self.old_request(
            "POST", f"/testcase-batchCreate-{product_id}.json", data
        )

    def import_testcases(self, product_id: str, file_path: str) -> Tuple[bool, Dict]:
        """导入测试用例（老 API）

        Args:
            product_id: 产品ID
            file_path: 导入文件路径

        Returns:
            (success, result)

        Note:
            这个方法需要上传文件，暂时返回错误信息

        Example:
            >>> success, result = client.import_testcases("1", "/path/to/import.csv")
        """
        # TODO: 需要实现文件上传
        return False, {"message": "文件导入功能暂未实现"}

    def export_testcases(self, product_id: str) -> Tuple[bool, Dict]:
        """导出测试用例（老 API）

        Args:
            product_id: 产品ID

        Returns:
            (success, result) 注意：返回文件内容

        Example:
            >>> success, result = client.export_testcases("1")
        """
        return self.old_request("POST", f"/testcase-export-{product_id}.json")

    def link_testcase_story(self, case_id: str, story_id: str) -> Tuple[bool, Dict]:
        """测试用例关联需求（老 API）

        Args:
            case_id: 用例ID
            story_id: 需求ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.link_testcase_story("1", "5")
        """
        return self.old_request(
            "POST", f"/testcase-linkStory-{case_id}-{story_id}.json"
        )

    def unlink_testcase_story(self, case_id: str, story_id: str) -> Tuple[bool, Dict]:
        """取消测试用例关联需求（老 API）

        Args:
            case_id: 用例ID
            story_id: 需求ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.unlink_testcase_story("1", "5")
        """
        return self.old_request(
            "GET", f"/testcase-unlinkStory-{case_id}-{story_id}.json"
        )

    # ==================== 发布模块补充方法 ====================

    def create_release(
        self,
        product_id: str,
        name: str,
        branch: str = "0",
        build: str = "",
        date: str = "",
        desc: str = "",
    ) -> Tuple[bool, Dict]:
        """创建发布（老 API）

        Args:
            product_id: 产品ID
            name: 发布名称
            branch: 分支ID，默认 "0"
            build: 版本ID
            date: 发布日期 (YYYY-MM-DD)
            desc: 发布描述

        Returns:
            (success, result)

        Example:
            >>> success, result = client.create_release(
            ...     product_id="1",
            ...     name="V1.0",
            ...     build="1",
            ...     date="2026-04-01"
            ... )
        """
        data = {
            "product": product_id,
            "name": name,
            "branch": branch,
        }
        if build:
            data["build"] = build
        if date:
            data["date"] = date
        if desc:
            data["desc"] = desc

        return self.old_request(
            "POST", f"/release-create-{product_id}-{branch}.json", data
        )

    def edit_release(self, release_id: str, **kwargs) -> Tuple[bool, Dict]:
        """编辑发布（老 API）

        Args:
            release_id: 发布ID
            **kwargs: 要修改的字段 (name, date, build, desc, status, etc.)

        Returns:
            (success, result)

        Example:
            >>> success, result = client.edit_release("1", name="V1.0.1", status="released")
        """
        return self.old_request("POST", f"/release-edit-{release_id}.json", kwargs)

    def get_release(self, release_id: str) -> Tuple[bool, Dict]:
        """获取发布详情（老 API）

        Args:
            release_id: 发布ID

        Returns:
            (success, release_info) 发布详情

        Example:
            >>> success, release = client.get_release("1")
            >>> print(f"发布名: {release['name']}")
        """
        success, result = self.old_request("GET", f"/release-view-{release_id}.json")
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data.get("release", {})
        return False, {}

    def delete_release(self, release_id: str) -> Tuple[bool, Dict]:
        """删除发布（老 API）

        Args:
            release_id: 发布ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.delete_release("1")
        """
        return self.old_request("GET", f"/release-delete-{release_id}-yes.json")

    def link_release_story(
        self, release_id: str, story_ids: List[str]
    ) -> Tuple[bool, Dict]:
        """发布关联需求（老 API）

        Args:
            release_id: 发布ID
            story_ids: 需求ID列表

        Returns:
            (success, result)

        Example:
            >>> success, result = client.link_release_story("1", ["5", "6", "7"])
        """
        data = {}
        for i, story_id in enumerate(story_ids):
            data[f"stories[{i}]"] = story_id

        return self.old_request("POST", f"/release-linkStory-{release_id}.json", data)

    def unlink_release_story(self, release_id: str, story_id: str) -> Tuple[bool, Dict]:
        """取消发布关联需求（老 API）

        Args:
            release_id: 发布ID
            story_id: 需求ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.unlink_release_story("1", "5")
        """
        return self.old_request(
            "GET", f"/release-unlinkStory-{release_id}-{story_id}.json"
        )

    def link_release_bug(
        self, release_id: str, bug_ids: List[str], bug_type: str = "bug"
    ) -> Tuple[bool, Dict]:
        """发布关联Bug（老 API）

        Args:
            release_id: 发布ID
            bug_ids: BugID列表
            bug_type: Bug类型 (bug, leftBug)

        Returns:
            (success, result)

        Example:
            >>> success, result = client.link_release_bug("1", ["10", "11"])
        """
        data = {}
        for i, bug_id in enumerate(bug_ids):
            data[f"bugs[{i}]"] = bug_id

        return self.old_request(
            "POST", f"/release-linkBug-{release_id}-all-all-bug.json", data
        )

    def unlink_release_bug(
        self, release_id: str, bug_id: str, bug_type: str = "bug"
    ) -> Tuple[bool, Dict]:
        """取消发布关联Bug（老 API）

        Args:
            release_id: 发布ID
            bug_id: BugID
            bug_type: Bug类型 (bug, leftBug)

        Returns:
            (success, result)

        Example:
            >>> success, result = client.unlink_release_bug("1", "10")
        """
        return self.old_request(
            "GET", f"/release-unlinkBug-{release_id}-{bug_id}-{bug_type}.json"
        )

    # ==================== 版本模块补充方法 ====================

    def create_build(
        self,
        project_id: str,
        name: str,
        product_id: str = "0",
        build: str = "",
        desc: str = "",
    ) -> Tuple[bool, Dict]:
        """创建版本（老 API）

        Args:
            project_id: 项目ID
            name: 版本名称
            product_id: 产品ID，默认 "0"
            build: 版本号
            desc: 版本描述

        Returns:
            (success, result)

        Example:
            >>> success, result = client.create_build(
            ...     project_id="1",
            ...     name="Sprint1 Build",
            ...     product_id="1",
            ...     build="1.0.0"
            ... )
        """
        data = {
            "project": project_id,
            "name": name,
        }
        if product_id:
            data["product"] = product_id
        if build:
            data["build"] = build
        if desc:
            data["desc"] = desc

        return self.old_request(
            "POST", f"/build-create-{project_id}-{product_id}.json", data
        )

    def edit_build(self, build_id: str, **kwargs) -> Tuple[bool, Dict]:
        """编辑版本（老 API）

        Args:
            build_id: 版本ID
            **kwargs: 要修改的字段 (name, build, desc, etc.)

        Returns:
            (success, result)

        Example:
            >>> success, result = client.edit_build("1", name="New Build Name")
        """
        return self.old_request("POST", f"/build-edit-{build_id}.json", kwargs)

    def get_build(self, build_id: str) -> Tuple[bool, Dict]:
        """获取版本详情（老 API）

        Args:
            build_id: 版本ID

        Returns:
            (success, build_info) 版本详情

        Example:
            >>> success, build = client.get_build("1")
            >>> print(f"版本名: {build['name']}")
        """
        success, result = self.old_request("GET", f"/build-view-{build_id}.json")
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data.get("build", {})
        return False, {}

    def delete_build(self, build_id: str) -> Tuple[bool, Dict]:
        """删除版本（老 API）

        Args:
            build_id: 版本ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.delete_build("1")
        """
        return self.old_request("GET", f"/build-delete-{build_id}-yes.json")

    def link_build_story(
        self, build_id: str, story_ids: List[str]
    ) -> Tuple[bool, Dict]:
        """版本关联需求（老 API）

        Args:
            build_id: 版本ID
            story_ids: 需求ID列表

        Returns:
            (success, result)

        Example:
            >>> success, result = client.link_build_story("1", ["5", "6"])
        """
        data = {}
        for i, story_id in enumerate(story_ids):
            data[f"stories[{i}]"] = story_id

        return self.old_request("POST", f"/build-linkStory-{build_id}.json", data)

    def unlink_build_story(self, build_id: str, story_id: str) -> Tuple[bool, Dict]:
        """取消版本关联需求（老 API）

        Args:
            build_id: 版本ID
            story_id: 需求ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.unlink_build_story("1", "5")
        """
        return self.old_request("GET", f"/build-unlinkStory-{story_id}-yes.json")

    def link_build_bug(self, build_id: str, bug_ids: List[str]) -> Tuple[bool, Dict]:
        """版本关联Bug（老 API）

        Args:
            build_id: 版本ID
            bug_ids: BugID列表

        Returns:
            (success, result)

        Example:
            >>> success, result = client.link_build_bug("1", ["10", "11"])
        """
        data = {}
        for i, bug_id in enumerate(bug_ids):
            data[f"bugs[{i}]"] = bug_id

        return self.old_request("POST", f"/build-linkBug-{build_id}.json", data)

    def unlink_build_bug(self, build_id: str, bug_id: str) -> Tuple[bool, Dict]:
        """取消版本关联Bug（老 API）

        Args:
            build_id: 版本ID
            bug_id: BugID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.unlink_build_bug("1", "10")
        """
        return self.old_request("GET", f"/build-unlinkBug-{build_id}-{bug_id}.json")

    # ==================== 计划模块补充方法 ====================

    def get_plan(self, plan_id: str) -> Tuple[bool, Dict]:
        """获取计划详情（老 API）

        Args:
            plan_id: 计划ID

        Returns:
            (success, plan_info) 计划详情

        Example:
            >>> success, plan = client.get_plan("1")
            >>> print(f"计划名: {plan['title']}")
        """
        success, result = self.old_request("GET", f"/productplan-view-{plan_id}.json")
        if success and "data" in result:
            data = json.loads(result["data"])
            return True, data.get("plan", {})
        return False, {}

    def edit_plan(self, plan_id: str, **kwargs) -> Tuple[bool, Dict]:
        """编辑计划（老 API）

        Args:
            plan_id: 计划ID
            **kwargs: 要修改的字段 (title, begin, end, desc, etc.)

        Returns:
            (success, result)

        Example:
            >>> success, result = client.edit_plan("1", title="新计划名", begin="2026-04-01")
        """
        return self.old_request("POST", f"/productplan-edit-{plan_id}.json", kwargs)

    def link_plan_story(self, plan_id: str, story_ids: List[str]) -> Tuple[bool, Dict]:
        """计划关联需求（老 API）

        Args:
            plan_id: 计划ID
            story_ids: 需求ID列表

        Returns:
            (success, result)

        Example:
            >>> success, result = client.link_plan_story("1", ["5", "6", "7"])
        """
        data = {}
        for i, story_id in enumerate(story_ids):
            data[f"stories[{i}]"] = story_id

        return self.old_request("POST", f"/productplan-linkStory-{plan_id}.json", data)

    def unlink_plan_story(self, plan_id: str, story_id: str) -> Tuple[bool, Dict]:
        """取消计划关联需求（老 API）

        Args:
            plan_id: 计划ID
            story_id: 需求ID

        Returns:
            (success, result)

        Example:
            >>> success, result = client.unlink_plan_story("1", "5")
        """
        return self.old_request(
            "GET", f"/productplan-unlinkStory-{plan_id}-{story_id}.json"
        )


def read_credentials() -> Optional[Dict[str, str]]:
    """从 TOOLS.md 读取禅道凭证"""
    tools_path = Path(__file__).parent.parent / "TOOLS.md"

    if not tools_path.exists():
        return None

    content = tools_path.read_text(encoding="utf-8")

    # 查找禅道配置部分
    zentao_section_start = -1
    zentao_section_end = -1

    lines = content.split("\n")
    for i, line in enumerate(lines):
        if "## 禅道 API" in line or "## 禅道" in line:
            zentao_section_start = i
        elif (
            zentao_section_start >= 0
            and line.strip().startswith("## ")
            and zentao_section_start not in [i]
        ):
            zentao_section_end = i
            break

    if zentao_section_start < 0:
        return None

    # 提取禅道配置部分
    if zentao_section_end < 0:
        zentao_section = "\n".join(lines[zentao_section_start:])
    else:
        zentao_section = "\n".join(lines[zentao_section_start:zentao_section_end])

    endpoint = None
    username = None
    password = None

    for line in zentao_section.split("\n"):
        line = line.strip()
        if "API 地址" in line and "：" in line:
            endpoint = line.split("：")[-1].strip().strip("*").strip()
        elif "用户名" in line and "：" in line:
            username = line.split("：")[-1].strip().strip("*").strip()
        elif "密码" in line and "：" in line:
            password = line.split("：")[-1].strip().strip("*").strip()

    if endpoint and username and password:
        return {"endpoint": endpoint, "username": username, "password": password}

    return None
