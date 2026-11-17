#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quicker Connector - 动作列表读取、搜索和调用模块
支持从 CSV 文件或 Quicker 数据库读取动作列表
"""

import csv
import json
import sqlite3
import subprocess
import os
import shutil
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict


# 默认路径配置
DEFAULT_CSV_PATH = r"G:\Data\Tools\Quicker\QuickerActions.csv"
DEFAULT_DB_PATH = r"C:\Users\Administrator\AppData\Local\Quicker\data\quicker.db"
DEFAULT_STARTER_PATH = r"C:\Program Files\Quicker\QuickerStarter.exe"


@dataclass
class QuickerAction:
    """Quicker 动作数据类"""
    id: str
    name: str
    description: str = ""
    icon: str = ""
    action_type: str = ""
    uri: str = ""
    panel: str = ""
    exe: str = ""
    associated_exe: str = ""
    position: str = ""
    size: str = ""
    create_time: str = ""
    update_time: str = ""
    source: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    def __repr__(self) -> str:
        return f"QuickerAction(id={self.id}, name={self.name})"


@dataclass
class QuickerActionResult:
    """Quicker 动作执行结果"""
    success: bool
    output: str
    error: Optional[str] = None
    exit_code: Optional[int] = None

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "output": self.output,
            "error": self.error,
            "exit_code": self.exit_code
        }


@dataclass
class MatchResult:
    """匹配结果"""
    action: QuickerAction
    score: float
    matched_keywords: List[str]

    def to_dict(self) -> dict:
        return {
            "action": self.action.to_dict(),
            "score": self.score,
            "matched_keywords": self.matched_keywords
        }


class EncodingDetector:
    """编码检测器"""

    ENCODINGS = ['utf-8-sig', 'utf-8', 'gbk', 'gb2312', 'gb18030', 'latin-1']

    @classmethod
    def detect(cls, file_path: str) -> Optional[str]:
        """
        检测文件编码

        Args:
            file_path: 文件路径

        Returns:
            检测到的编码，如果失败返回 None
        """
        for encoding in cls.ENCODINGS:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    # 尝试读取前几行来验证编码
                    f.read(1000)
                return encoding
            except (UnicodeDecodeError, LookupError):
                continue
        return None


class CSVActionReader:
    """CSV 格式动作列表读取器"""

    def __init__(self, csv_path: Optional[str] = None, encoding: Optional[str] = None):
        """
        初始化 CSV 读取器

        Args:
            csv_path: CSV 文件路径
            encoding: 文件编码，如果为 None 则自动检测
        """
        self.csv_path = csv_path or DEFAULT_CSV_PATH
        self.encoding = encoding
        self.actions_cache = None

    def read_all(self) -> List[QuickerAction]:
        """
        读取所有动作

        Returns:
            动作列表
        """
        if self.actions_cache is not None:
            return self.actions_cache

        if not Path(self.csv_path).exists():
            raise FileNotFoundError(f"CSV 文件不存在: {self.csv_path}")

        # 检测编码
        if self.encoding is None:
            self.encoding = EncodingDetector.detect(self.csv_path)
            if self.encoding is None:
                raise Exception(f"无法检测文件编码: {self.csv_path}")

        actions = []

        try:
            with open(self.csv_path, 'r', encoding=self.encoding, errors='replace') as f:
                # 跳过 sep=, 行
                first_line = f.readline()
                if not first_line.startswith('sep='):
                    f.seek(0)

                # 解析 CSV
                reader = csv.DictReader(f)

                for row in reader:
                    if not row.get('Id'):
                        continue

                    action = QuickerAction(
                        id=str(row.get('Id', '')),
                        name=str(row.get('名称', '')),
                        description=str(row.get('说明', '')),
                        icon=str(row.get('图标', '')),
                        action_type=str(row.get('类型', '')),
                        uri=str(row.get('Uri', '')),
                        panel=str(row.get('动作页', '')),
                        exe=str(row.get('EXE', '')),
                        associated_exe=str(row.get('关联Exe', '')),
                        position=str(row.get('位置', '')),
                        size=str(row.get('大小', '')),
                        create_time=str(row.get('创建或安装时间', '')),
                        update_time=str(row.get('最后更新', '')),
                        source=str(row.get('来源动作', ''))
                    )
                    actions.append(action)

            self.actions_cache = actions
            return actions

        except Exception as e:
            raise Exception(f"读取 CSV 文件失败: {e}")

    def search(self, keyword: str, fields: Optional[List[str]] = None) -> List[QuickerAction]:
        """
        搜索动作

        Args:
            keyword: 搜索关键词
            fields: 搜索字段列表，None 表示搜索所有字段

        Returns:
            匹配的动作列表
        """
        actions = self.read_all()

        if not keyword:
            return actions

        keyword_lower = keyword.lower()
        results = []

        for action in actions:
            if fields is None:
                # 搜索所有文本字段
                if (keyword_lower in action.name.lower() or
                    keyword_lower in action.description.lower() or
                    keyword_lower in action.panel.lower() or
                    keyword_lower in action.uri.lower()):
                    results.append(action)
            else:
                # 只搜索指定字段
                for field in fields:
                    field_value = getattr(action, field, '')
                    if keyword_lower in field_value.lower():
                        results.append(action)
                        break

        return results

    def get_by_id(self, action_id: str) -> Optional[QuickerAction]:
        """根据 ID 获取动作"""
        actions = self.read_all()
        for action in actions:
            if action.id == action_id:
                return action
        return None

    def get_by_name(self, name: str) -> Optional[QuickerAction]:
        """根据名称获取动作"""
        actions = self.read_all()
        for action in actions:
            if action.name == name:
                return action
        return None

    def get_by_panel(self, panel_name: str) -> List[QuickerAction]:
        """根据动作页获取动作"""
        actions = self.read_all()
        return [a for a in actions if panel_name.lower() in a.panel.lower()]


class DatabaseActionReader:
    """数据库格式动作列表读取器"""

    def __init__(self, db_path: Optional[str] = None):
        """
        初始化数据库读取器

        Args:
            db_path: Quicker 数据库路径
        """
        self.db_path = db_path or DEFAULT_DB_PATH
        self.actions_cache = None

    def read_all(self) -> List[QuickerAction]:
        """
        从数据库读取所有动作

        Returns:
            动作列表
        """
        if self.actions_cache is not None:
            return self.actions_cache

        if not Path(self.db_path).exists():
            raise FileNotFoundError(f"Quicker 数据库不存在: {self.db_path}")

        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            actions = []

            # 获取所有表
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]

            # 查找动作相关的表
            action_tables = []
            for table in tables:
                table_lower = table.lower()
                if any(keyword in table_lower for keyword in ['action', 'button', 'module']):
                    action_tables.append(table)

            # 从找到的表中读取数据
            for table in action_tables:
                try:
                    cursor.execute(f"PRAGMA table_info({table})")
                    columns = cursor.fetchall()
                    col_names = [col[1] for col in columns]
                    col_dict = {col[1]: idx for idx, col in enumerate(columns)}

                    # 查找关键字段
                    id_field = None
                    name_field = None
                    desc_field = None

                    for col_name in col_names:
                        col_lower = col_name.lower()
                        if id_field is None and ('id' in col_lower or 'guid' in col_lower):
                            id_field = col_name
                        elif name_field is None and 'name' in col_lower:
                            name_field = col_name
                        elif desc_field is None and ('desc' in col_lower or 'summary' in col_lower):
                            desc_field = col_name

                    if id_field and name_field:
                        cursor.execute(f"SELECT * FROM {table} LIMIT 500")
                        rows = cursor.fetchall()

                        for row in rows:
                            action_id = str(row[col_dict[id_field]])
                            action_name = str(row[col_dict[name_field]])
                            action_desc = str(row[col_dict[desc_field]]) if desc_field and desc_field in col_dict else ""

                            action = QuickerAction(
                                id=action_id,
                                name=action_name,
                                description=action_desc,
                                panel=table
                            )
                            actions.append(action)

                        if actions:
                            break

                except Exception:
                    continue

            conn.close()
            self.actions_cache = actions
            return actions

        except Exception as e:
            raise Exception(f"读取数据库失败: {e}")

    def search(self, keyword: str) -> List[QuickerAction]:
        """搜索动作"""
        actions = self.read_all()

        if not keyword:
            return actions

        keyword_lower = keyword.lower()
        return [
            action for action in actions
            if keyword_lower in action.name.lower()
            or keyword_lower in action.description.lower()
        ]

    def get_by_id(self, action_id: str) -> Optional[QuickerAction]:
        """根据 ID 获取动作"""
        actions = self.read_all()
        for action in actions:
            if action.id == action_id:
                return action
        return None

    def get_by_name(self, name: str) -> Optional[QuickerAction]:
        """根据名称获取动作"""
        actions = self.read_all()
        for action in actions:
            if action.name == name:
                return action
        return None


class ActionMatcher:
    """动作匹配器 - 根据用户需求匹配动作"""

    # 常用关键词映射
    KEYWORD_MAP = {
        "翻译": ["翻译", "translate", "translation"],
        "格式化": ["格式化", "format"],
        "大小写": ["大小写", "大写", "小写", "upper", "lower", "case"],
        "编码": ["编码", "解码", "encode", "decode", "base64"],
        "剪贴板": ["剪贴板", "clipboard", "复制", "粘贴"],
        "重命名": ["重命名", "rename"],
        "移动": ["移动", "move"],
        "复制": ["复制", "copy"],
        "删除": ["删除", "remove", "delete"],
        "下载": ["下载", "download"],
        "截图": ["截图", "screenshot", "screen"],
        "打开网页": ["打开", "网页", "浏览器", "browser"],
        "搜索": ["搜索", "search", "find"],
        "计算器": ["计算器", "calculator"],
    }

    def __init__(self, action_reader):
        """
        初始化动作匹配器

        Args:
            action_reader: 动作读取器（CSVActionReader 或 DatabaseActionReader）
        """
        self.reader = action_reader
        self.actions_cache = None

    def _get_actions(self) -> List[QuickerAction]:
        """获取动作列表（带缓存）"""
        if self.actions_cache is None:
            self.actions_cache = self.reader.read_all()
        return self.actions_cache

    def _extract_keywords(self, user_input: str) -> List[str]:
        """从用户输入中提取关键词"""
        import re
        keywords = []

        # 从关键词映射中查找
        for category, kw_list in self.KEYWORD_MAP.items():
            for kw in kw_list:
                if kw.lower() in user_input.lower():
                    keywords.append(kw)

        # 提取中文关键词
        chinese_keywords = re.findall(r'[\u4e00-\u9fff]{2,4}', user_input)
        keywords.extend(chinese_keywords)

        # 提取英文单词
        english_keywords = re.findall(r'[a-zA-Z]{2,}', user_input)
        keywords.extend(english_keywords)

        return list(set(keywords))

    def _calculate_score(self, action: QuickerAction, keywords: List[str]) -> tuple:
        """计算动作匹配分数"""
        if not keywords:
            return (0.0, [])

        score = 0.0
        matched_keywords = []
        action_text = f"{action.name} {action.description}".lower()

        for keyword in keywords:
            keyword_lower = keyword.lower()

            if keyword_lower in action.name.lower():
                score += 1.0
                matched_keywords.append(keyword)
            elif keyword_lower in action_text:
                score += 0.5
                matched_keywords.append(keyword)

        max_score = len(keywords) * 1.0
        if max_score > 0:
            score = min(score / max_score, 1.0)

        return (score, matched_keywords)

    def match(self, user_input: str, top_n: int = 5) -> List[Dict[str, Any]]:
        """
        根据用户输入匹配动作

        Args:
            user_input: 用户输入的文本
            top_n: 返回前 N 个匹配结果

        Returns:
            匹配结果列表
        """
        actions = self._get_actions()
        keywords = self._extract_keywords(user_input)

        results = []
        for action in actions:
            score, matched = self._calculate_score(action, keywords)

            if score > 0:
                results.append({
                    "action": action,
                    "score": score,
                    "matched_keywords": matched
                })

        # 按分数降序排序
        results.sort(key=lambda x: x["score"], reverse=True)

        return results[:top_n]

    def fuzzy_search(self, keyword: str, top_n: int = 10) -> List[Dict[str, Any]]:
        """
        模糊搜索动作

        Args:
            keyword: 搜索关键词
            top_n: 返回前 N 个结果

        Returns:
            搜索结果列表
        """
        actions = self._get_actions()
        keyword_lower = keyword.lower()

        results = []
        for action in actions:
            score = 0.0

            # 名称匹配
            if keyword_lower in action.name.lower():
                score += 0.7
            else:
                for word in action.name.lower().split():
                    if keyword_lower in word or word in keyword_lower:
                        score += 0.3
                        break

            # 描述匹配
            if keyword_lower in action.description.lower():
                score += 0.3

            if score > 0:
                results.append({
                    "action": action,
                    "score": min(score, 1.0),
                    "matched_keywords": [keyword]
                })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_n]

    def clear_cache(self):
        """清除动作缓存"""
        self.actions_cache = None


class QuickerActionRunner:
    """Quicker 动作执行器"""

    ALTERNATIVE_PATHS = [
        r"C:\Program Files (x86)\Quicker\QuickerStarter.exe",
        r"C:\Program Files\Quicker\QuickerStarter.exe",
        r"C:\Users\Administrator\AppData\Local\Quicker\QuickerStarter.exe",
    ]

    def __init__(self, starter_path: Optional[str] = None):
        """
        初始化动作执行器

        Args:
            starter_path: QuickerStarter.exe 路径
        """
        self.starter_path = starter_path or self._find_quicker_starter()

        if not self.starter_path or not Path(self.starter_path).exists():
            raise FileNotFoundError(
                f"未找到 QuickerStarter.exe\n"
                f"请确认 Quicker 已安装"
            )

    def _find_quicker_starter(self) -> Optional[str]:
        """自动查找 QuickerStarter.exe"""
        for path in self.ALTERNATIVE_PATHS:
            if Path(path).exists():
                return path
        return None

    def run_action(
        self,
        action_identifier: str,
        parameters: Optional[str] = None,
        wait_for_result: bool = False,
        timeout: int = 20
    ) -> QuickerActionResult:
        """
        运行 Quicker 动作

        Args:
            action_identifier: 动作标识（ID、名称或 URI）
            parameters: 传递给动作的参数
            wait_for_result: 是否等待动作返回结果
            timeout: 超时时间（秒）

        Returns:
            动作执行结果
        """
        try:
            cmd = [self.starter_path]

            if wait_for_result:
                cmd.append(f"-c{timeout}")

            # 构建动作调用参数
            if action_identifier.startswith('quicker:'):
                action_cmd = action_identifier
            else:
                action_cmd = f"runaction:{action_identifier}"

            if parameters:
                action_cmd = f"{action_cmd}?{parameters}"

            cmd.append(action_cmd)

            if wait_for_result:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding='utf-8',
                    shell=True
                )
                stdout, stderr = process.communicate(timeout=timeout)
                exit_code = process.returncode

                return QuickerActionResult(
                    success=exit_code == 0,
                    output=stdout.strip(),
                    error=stderr.strip() if stderr else None,
                    exit_code=exit_code
                )
            else:
                subprocess.Popen(
                    cmd,
                    shell=True,
                    creationflags=subprocess.DETACHED_PROCESS
                )

                return QuickerActionResult(
                    success=True,
                    output="动作已启动"
                )

        except subprocess.TimeoutExpired:
            return QuickerActionResult(
                success=False,
                output="",
                error=f"动作执行超时（{timeout}秒）"
            )
        except Exception as e:
            return QuickerActionResult(
                success=False,
                output="",
                error=f"执行失败: {str(e)}"
            )

    def run_by_uri(self, uri: str, wait_for_result: bool = False, timeout: int = 20) -> QuickerActionResult:
        """通过 URI 执行动作"""
        return self.run_action(uri, wait_for_result=wait_for_result, timeout=timeout)

    def run_by_id(self, action_id: str, parameters: Optional[str] = None,
                  wait_for_result: bool = False, timeout: int = 20) -> QuickerActionResult:
        """通过 ID 执行动作"""
        return self.run_action(action_id, parameters, wait_for_result, timeout)

    def run_by_name(self, action_name: str, parameters: Optional[str] = None,
                     wait_for_result: bool = False, timeout: int = 20) -> QuickerActionResult:
        """通过名称执行动作"""
        return self.run_action(action_name, parameters, wait_for_result, timeout)


PUSH_API_URL = "https://push.getquicker.cn/to/quicker"
PUSH_MAX_TIMEOUT = 30  # 推送服务最长等待 30 秒


class QuickerPushRunner:
    """
    Quicker 远程推送执行器
    通过 Quicker 云推送服务远程触发动作，支持传参和同步等待结果。
    需要在 Quicker 会员中心获取验证码：https://getquicker.net/user/connection
    """

    def __init__(self, user: str, code: str):
        """
        Args:
            user: Quicker 账号邮箱
            code: 会员中心的推送验证码
        """
        if not user or not code:
            raise ValueError("push_user 和 push_code 不能为空，请先在 config.json 中配置")
        self.user = user
        self.code = code

    def push_action(
        self,
        action: str,
        data: Optional[str] = None,
        wait: bool = True,
        timeout: int = 20
    ) -> QuickerActionResult:
        """
        通过推送服务远程执行动作。

        Args:
            action: 动作名称或 ID
            data:   传递给动作的参数字符串
            wait:   是否等待动作执行完成并返回结果
            timeout: 等待超时秒数（最大 30）

        Returns:
            QuickerActionResult
        """
        timeout = min(timeout, PUSH_MAX_TIMEOUT)

        payload = {
            "toUser": self.user,
            "code": self.code,
            "operation": "action",
            "action": action,
            "wait": wait,
        }
        if data:
            payload["data"] = data

        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        if len(body) > 30 * 1024:
            return QuickerActionResult(
                success=False,
                output="",
                error="请求体超过 30KB 限制，请减少 data 参数大小"
            )

        req = urllib.request.Request(
            PUSH_API_URL,
            data=body,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8")

            try:
                result_data = json.loads(raw)
            except json.JSONDecodeError:
                return QuickerActionResult(success=True, output=raw)

            # Quicker 推送服务返回格式：{"success": bool, "message": "...", "data": ...}
            ok = result_data.get("success", True)
            message = result_data.get("message", "")
            ret_data = result_data.get("data", "")
            output = str(ret_data) if ret_data else message

            return QuickerActionResult(
                success=ok,
                output=output,
                error=message if not ok else None
            )

        except urllib.error.HTTPError as e:
            body_text = e.read().decode("utf-8", errors="replace")
            return QuickerActionResult(
                success=False,
                output="",
                error=f"HTTP {e.code}: {body_text}"
            )
        except urllib.error.URLError as e:
            return QuickerActionResult(
                success=False,
                output="",
                error=f"网络错误: {e.reason}"
            )
        except TimeoutError:
            return QuickerActionResult(
                success=False,
                output="",
                error=f"推送请求超时（{timeout}秒）"
            )


class QuickerConnector:
    """
    Quicker 连接器 - 整合动作读取、搜索和调用功能
    """

    def __init__(
        self,
        source: str = "csv",
        csv_path: Optional[str] = None,
        db_path: Optional[str] = None
    ):
        """
        初始化 Quicker 连接器

        Args:
            source: 数据源类型，"csv" 或 "db"
            csv_path: CSV 文件路径（当 source="csv" 时使用）
            db_path: 数据库路径（当 source="db" 时使用）
        """
        self.source = source

        # 如果没有提供路径，从配置文件读取
        if source == "csv":
            if csv_path is None:
                csv_path = self._load_csv_path_from_config()
            self.reader = CSVActionReader(csv_path)
        elif source == "db":
            if db_path is None:
                db_path = self._load_db_path_from_config()
            self.reader = DatabaseActionReader(db_path)
        else:
            raise ValueError(f"不支持的数据源类型: {source}")

        self.matcher = ActionMatcher(self.reader)
        self.runner = None        # 延迟初始化（本地执行器）
        self.push_runner = None   # 延迟初始化（推送执行器）

    def _load_csv_path_from_config(self) -> Optional[str]:
        """从配置文件读取 CSV 路径"""
        config_path = Path(__file__).parent.parent / "config.json"
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    csv_path = config.get('csv_path', '')
                    if csv_path and Path(csv_path).exists():
                        return csv_path
            except Exception:
                pass
        return None

    def _load_db_path_from_config(self) -> Optional[str]:
        """从配置文件读取数据库路径"""
        config_path = Path(__file__).parent.parent / "config.json"
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    db_path = config.get('db_path', '')
                    if db_path and Path(db_path).exists():
                        return db_path
            except Exception:
                pass
        return None

    def _get_runner(self) -> QuickerActionRunner:
        """获取本地动作执行器（延迟初始化）"""
        if self.runner is None:
            self.runner = QuickerActionRunner()
        return self.runner

    def _get_push_runner(self) -> QuickerPushRunner:
        """获取推送执行器（延迟初始化），从 config.json 读取凭证"""
        if self.push_runner is None:
            config = get_config()
            user = config.get("push_user", "")
            code = config.get("push_code", "")
            self.push_runner = QuickerPushRunner(user=user, code=code)
        return self.push_runner

    def read_actions(self) -> List[QuickerAction]:
        """读取所有动作"""
        return self.reader.read_all()

    def search_actions(
        self,
        keyword: str,
        fields: Optional[List[str]] = None
    ) -> List[QuickerAction]:
        """
        搜索动作

        Args:
            keyword: 搜索关键词
            fields: 搜索字段列表

        Returns:
            匹配的动作列表
        """
        return self.reader.search(keyword, fields)

    def match_actions(self, user_input: str, top_n: int = 5) -> List[Dict[str, Any]]:
        """
        根据用户需求匹配动作

        Args:
            user_input: 用户输入的文本
            top_n: 返回前 N 个匹配结果

        Returns:
            匹配结果列表
        """
        return self.matcher.match(user_input, top_n)

    def fuzzy_search(self, keyword: str, top_n: int = 10) -> List[Dict[str, Any]]:
        """
        模糊搜索动作

        Args:
            keyword: 搜索关键词
            top_n: 返回前 N 个结果

        Returns:
            搜索结果列表
        """
        return self.matcher.fuzzy_search(keyword, top_n)

    def execute_action(
        self,
        action_id: str,
        parameters: Optional[str] = None,
        wait_for_result: bool = False,
        timeout: int = 20
    ) -> QuickerActionResult:
        """
        执行动作

        Args:
            action_id: 动作 ID 或名称
            parameters: 传递给动作的参数
            wait_for_result: 是否等待动作返回结果
            timeout: 超时时间（秒）

        Returns:
            动作执行结果
        """
        return self._get_runner().run_action(
            action_id, parameters, wait_for_result, timeout
        )

    def execute_by_uri(
        self,
        uri: str,
        wait_for_result: bool = False,
        timeout: int = 20
    ) -> QuickerActionResult:
        """
        通过 URI 执行动作

        Args:
            uri: Quicker URI
            wait_for_result: 是否等待动作返回结果
            timeout: 超时时间（秒）

        Returns:
            动作执行结果
        """
        return self._get_runner().run_by_uri(uri, wait_for_result, timeout)

    def get_statistics(self) -> Dict[str, Any]:
        """
        获取动作统计信息

        Returns:
            统计信息字典
        """
        actions = self.read_all()

        type_count = {}
        panel_count = {}

        for action in actions:
            action_type = action.action_type
            type_count[action_type] = type_count.get(action_type, 0) + 1

            panel = action.panel
            panel_count[panel] = panel_count.get(panel, 0) + 1

        return {
            "total": len(actions),
            "by_type": type_count,
            "by_panel": panel_count
        }

    def push_action(
        self,
        action: str,
        data: Optional[str] = None,
        wait: bool = True,
        timeout: int = 20
    ) -> QuickerActionResult:
        """
        通过 Quicker 云推送服务远程触发动作。

        前提：在 config.json 中配置 push_user（账号邮箱）和 push_code（验证码）。
        验证码获取地址：https://getquicker.net/user/connection

        Args:
            action:  动作名称或 ID
            data:    传递给动作的参数字符串
            wait:    是否同步等待结果（最长 30 秒）
            timeout: 超时秒数

        Returns:
            QuickerActionResult
        """
        return self._get_push_runner().push_action(action, data, wait, timeout)

    def export_to_json(self, output_path: str) -> None:
        """
        导出动作列表到 JSON 文件

        Args:
            output_path: 输出文件路径
        """
        actions = self.reader.read_all()
        data = {
            "total": len(actions),
            "actions": [action.to_dict() for action in actions]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def export_icons(self, out_dir: str, size: int = 48, max_workers: int = 8) -> dict:
        """
        批量导出动作图标为独立 PNG 文件（去重 + 并发解析 + 本地缓存优先）。

        输出 `<三位序号>_<动作名>_<图标短key>.png` 与 `icons_manifest.json`。

        Args:
            out_dir: 图标输出目录
            size: 图标像素尺寸
            max_workers: 并发线程数

        Returns:
            统计 dict：{"total","unique","files","from_cache","downloaded",
            "rendered","local","missing","elapsed_sec","out_dir","items"}

        Raises:
            ValueError: size 不是 >= 1 的整数
        """
        import sys as _sys
        _sys.path.insert(0, str(Path(__file__).resolve().parent))
        from icon_exporter import export_icons

        return export_icons(
            self.read_actions(),
            out_dir,
            size=size,
            max_workers=max_workers,
            log=lambda _m: None,
        )

    def export_to_excel(
        self,
        output_path: str,
        icon_size: int = 48,
        with_icons: bool = True,
        icon_mode: str = "embedded",
        icons_dir: Optional[str] = None,
        max_workers: int = 8,
    ) -> dict:
        """
        导出动作列表到 Excel（.xlsx），「图标」列写入真实图标图片。

        图标来源：
        - http(s) 图标：优先命中 Quicker 本地缓存（ImageCache，SHA1(URL).png），离线可用
        - fa:Style_Name 字体图标：用 Quicker 自带 FontAwesome5 SVG 数据栅格化渲染
        - 其余留空

        Args:
            output_path: 输出 .xlsx 路径
            icon_size:   图标像素尺寸（默认 48）
            with_icons:  总开关，False 等价于 icon_mode="none"（向后兼容）
            icon_mode:   embedded=嵌入图片（默认）/ path=图标列只写文件路径 / none=不处理
            icons_dir:   图标文件导出目录（给出时先批量导出图标文件）
            max_workers: 图标解析并发线程数

        Returns:
            统计 dict：{"total","with_icon","no_icon","output","icon_mode", ...}

        Raises:
            ValueError: icon_mode 非法或 icon_size < 1
            PermissionError: 目标文件被占用（原文件不会被破坏）
        """
        import sys as _sys
        _sys.path.insert(0, str(Path(__file__).resolve().parent))
        from export_actions_excel import export_actions_to_excel

        return export_actions_to_excel(
            self.read_actions(),
            output_path,
            icon_size=icon_size,
            with_icons=with_icons,
            icon_mode=icon_mode,
            icons_dir=icons_dir,
            max_workers=max_workers,
            log=lambda _m: None,
        )

    def read_all(self) -> List[QuickerAction]:
        """读取所有动作（兼容性别名）"""
        return self.read_actions()


# 便捷函数
def create_connector(source: str = "csv", **kwargs) -> QuickerConnector:
    """
    创建 Quicker 连接器

    Args:
        source: 数据源类型，"csv" 或 "db"
        **kwargs: 传递给连接器的其他参数

    Returns:
        QuickerConnector 实例
    """
    return QuickerConnector(source=source, **kwargs)


# 配置文件路径
CONFIG_FILE = str(Path(__file__).parent.parent / "config.json")


def is_initialized() -> bool:
    """
    检查技能是否已完成初始化配置

    Returns:
        如果已初始化返回 True，否则返回 False
    """
    if not Path(CONFIG_FILE).exists():
        return False

    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)

        csv_path = config.get('csv_path', '')
        db_path = config.get('db_path', '')

        if csv_path and Path(csv_path).exists():
            return True
        if db_path and Path(db_path).exists():
            return True

        return False
    except Exception:
        return False


def get_config() -> Dict[str, Any]:
    """
    获取配置文件内容

    Returns:
        配置字典，如果文件不存在返回空字典
    """
    if not Path(CONFIG_FILE).exists():
        return {}

    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def print_initialization_guide():
    """打印初始化引导信息"""
    print("\n" + "=" * 70)
    print("Quicker Connector 技能初始化引导")
    print("=" * 70)
    print()
    print("本技能需要 Quicker 动作列表才能正常工作。")
    print()
    print("-" * 70)
    print("请按照以下步骤导出 Quicker 动作列表：")
    print("-" * 70)
    print()
    print("1. 在 Quicker 面板中点击 \"...\" 按钮（更多菜单）")
    print("2. 选择 \"工具\" > \"导出动作列表(CSV)\"")
    print("3. 保存 CSV 文件到任意位置")
    print()
    print("-" * 70)
    print("配置方式：")
    print("-" * 70)
    print()
    print("方式 1：运行初始化脚本")
    print("  python scripts/init_quicker.py")
    print()
    print("方式 2：直接编辑配置文件")
    print(f"  配置文件路径: {CONFIG_FILE}")
    print('  内容格式: {"csv_path": "你的CSV文件路径"}')
    print()
    print("-" * 70)


def require_initialized():
    """
    检查初始化状态，如果未初始化则打印引导信息并退出

    Raises:
        SystemExit: 如果未初始化则退出
    """
    if not is_initialized():
        print_initialization_guide()
        print("\n未完成初始化，技能无法使用。")
        raise SystemExit(1)


# ============================================================
# 数据维护：export 目录配置映射（v1.3.0 新增）
# 映射知识库: data/quicker_export_map.json（功能→文件→字段 三级索引）
# ============================================================

DEFAULT_EXPORT_ROOT = r"G:\Data\Tools\Quicker\export"
DEFAULT_MAP_PATH = str(Path(__file__).parent.parent / "data" / "quicker_export_map.json")


class QuickerExportMap:
    """
    维护工具全量备份（export 目录）的配置映射读写器。

    用法：
        qm = QuickerExportMap()                       # 自动读 config.json 的 export_root + 映射
        qm.locate("扩展热键")                          # 定位：功能 → 文件类型/字段/实际文件
        qm.read_config("扩展热键")                     # 读取当前值 → (文件路径, 值)
        qm.update_config("左键增强", new_value)        # 修改并写回（自动 .bak 备份）
        qm.find_action("视频旋转修复版")               # actions\\ 下按 ID/名称定位动作文件
        qm.read_action_data("<动作ID>")               # 读取并解析动作 Data（步骤/变量）
        qm.list_actions()                             # 列出全部动作
    """

    def __init__(self, export_root: Optional[str] = None, map_path: Optional[str] = None):
        """
        Args:
            export_root: 维护工具备份目录；None 时依次读 config.json export_root → 默认路径
            map_path:    映射 JSON 路径；None 时用技能 data/ 下的知识库映射
        """
        self.export_root = export_root or self._resolve_export_root()
        self.map_path = Path(map_path) if map_path else Path(DEFAULT_MAP_PATH)
        self._map = self._load_map()
        self._files = self._index_files()

    # ---------- 初始化 ----------

    @staticmethod
    def _resolve_export_root() -> str:
        """从 config.json 读取 export_root，不存在则用默认路径"""
        cfg = get_config()
        root = cfg.get("export_root", "")
        if root and Path(root).exists():
            return root
        return DEFAULT_EXPORT_ROOT

    def _load_map(self) -> Dict[str, Any]:
        if not self.map_path.exists():
            raise FileNotFoundError(f"配置映射不存在: {self.map_path}")
        with open(self.map_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _index_files(self) -> Dict[str, List[str]]:
        """建立 file_type.id → 实际文件路径列表 的索引（按 pattern 匹配）"""
        index = {}
        root = Path(self.export_root)
        for ft in self._map.get("file_types", []):
            pattern = ft.get("pattern", "")
            rel_dir = pattern.split("\\")[0] if "\\" in pattern else ""
            pat = pattern.split("\\")[-1] if "\\" in pattern else pattern
            base = root / rel_dir if rel_dir else root
            matches = list(base.glob(pat)) if base.exists() else []
            index[ft["id"]] = [str(m) for m in matches]
        return index

    # ---------- 定位 ----------

    def locate(self, feature: str) -> Dict[str, Any]:
        """
        按功能关键词定位配置。

        Args:
            feature: 功能关键词（如"扩展热键""轮盘菜单""左键增强""定时任务"）

        Returns:
            {"feature", "file", "json_path", "writable", "match", "files"}

        Raises:
            KeyError: 映射中找不到该功能
        """
        feature_lower = feature.lower()
        for entry in self._map.get("config_index", []):
            if feature_lower in entry["feature"].lower():
                return {
                    "feature": entry["feature"],
                    "file": entry["file"],
                    "json_path": entry.get("json_path", "$root"),
                    "writable": entry.get("writable", False),
                    "match": entry.get("match"),
                    "files": self._files.get(entry["file"], []),
                }
        raise KeyError(
            f"映射中找不到功能: {feature}。可用关键词：{', '.join(self.list_features()[:10])} 等"
        )

    def list_features(self) -> List[str]:
        """列出映射支持的所有可定位功能"""
        return [e["feature"] for e in self._map.get("config_index", [])]

    def _resolve_config_file(self, entry: Dict[str, Any]) -> str:
        """把 config_index 条目解析到具体文件；match 用于多文件类型（如按 exe）过滤"""
        files = entry.get("files") or self._files.get(entry["file"], [])
        match = entry.get("match")
        if match and files:
            key = match.replace("<exe>", "")
            files = [f for f in files if key in Path(f).name]
        if not files:
            raise FileNotFoundError(
                f"未找到配置文件: file={entry['file']} match={entry.get('match')}（目录: {self.export_root}）"
            )
        return files[0]

    # ---------- 读取 ----------

    def read_config(self, feature: str):
        """
        读取某项配置的当前值。

        Returns:
            (文件路径, 提取的值)
        """
        entry = self.locate(feature)
        path = self._resolve_config_file(entry)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        jp = entry["json_path"]
        if jp == "$root":
            return path, data
        return path, self._json_get(data, jp)

    # ---------- 修改 ----------

    def update_config(self, feature: str, value: Any, backup: bool = True):
        """
        修改配置并写回。

        Args:
            feature: 功能关键词
            value:   新值（覆盖 json_path 指向的字段；$root 时覆盖整个文件内容）
            backup:  是否先备份原文件为 <文件>.bak

        Returns:
            (文件路径, True)
        """
        entry = self.locate(feature)
        path = self._resolve_config_file(entry)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        jp = entry["json_path"]
        if jp == "$root":
            data = value
        else:
            self._json_set(data, jp, value)
        if backup:
            shutil.copy2(path, path + ".bak")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path, True

    # ---------- 导入（导回）方案 ----------

    @staticmethod
    def _file_id_of_name(name: str) -> Optional[str]:
        """按文件名判断属于哪个 file_type（用于导回决策）"""
        n = name.replace("\\", "/").split("/")[-1]
        if n == "_action_adorn.json":
            return "action_adorn"
        if n.startswith("state_"):
            return "state"
        if n.startswith("actionpage_"):
            return "actionpage"
        if n.startswith("common_exe_"):
            return "exe_common"
        if n.startswith("common_shared_subprogram_"):
            return "shared_subprogram"
        if n.startswith("common_user_settings"):
            return "settings"
        if n.startswith("common_user_gestures"):
            return "gestures"
        if n.startswith("common_user_mouseActions"):
            return "mouse_actions"
        if n.startswith("common_user_powerKeys"):
            return "power_keys"
        if n.startswith("common_user_preferences"):
            return "preferences"
        if n.startswith("common_user_favorBlocks"):
            return "favor_blocks"
        if n.startswith("action_") or "/actions/" in name.replace("\\", "/"):
            return "action"
        return None

    def _import_info(self, file_id: str):
        """从映射取 file_type 的 import_mode + import_method"""
        for ft in self._map.get("file_types", []):
            if ft["id"] == file_id:
                return ft.get("import_mode", "batch"), ft.get("import_method", "")
        return "batch", ""

    def get_import_plan(self, items) -> Dict[str, Any]:
        """
        根据修改内容生成导入（导回）方案：判断单文件导回还是批量导入。

        Args:
            items: 修改项列表。每项可以是：
                - 功能关键词（如"扩展热键""左键增强"）——走 config_index 匹配
                - 文件路径或文件名（如 "actions\\action_5479d192-...json"、"common_user_settings.json"）
                - 动作 ID 或动作名称（定位到 actions\\ 文件）

        Returns:
            {
              "mode": "single" | "batch",     # 全部可单文件= single；含设置类= batch
              "plans": [ {item, kind, file_id, mode, method} ... ],
              "steps": [ ... ],                # 具体操作步骤
              "impact": "影响范围说明",
              "warning": "风险提示"
            }
        """
        plans = []
        for item in items:
            item = (item or "").strip()
            if not item:
                continue
            # 1) 功能关键词 → config_index
            try:
                entry = self.locate(item)
                mode = entry.get("import_mode") or self._import_info(entry["file"])[0]
                method = entry.get("import_method") or self._import_info(entry["file"])[1]
                plans.append({"item": item, "kind": "feature", "file_id": entry["file"],
                              "mode": mode, "method": method})
                continue
            except KeyError:
                pass
            # 2) 文件名 → file_type
            file_id = self._file_id_of_name(item)
            if file_id is None:
                # 3) 动作 ID / 名称
                try:
                    self.find_action(item)
                    file_id = "action"
                except Exception:
                    raise KeyError(
                        f"无法识别修改项: {item}（既不是已知功能关键词，也不是映射文件或动作）"
                    )
            mode, method = self._import_info(file_id)
            plans.append({"item": item, "kind": "file", "file_id": file_id,
                          "mode": mode, "method": method})

        if not plans:
            raise ValueError("items 为空，无法生成导入方案")

        has_batch = any(p["mode"] == "batch" for p in plans)
        mode = "batch" if has_batch else "single"
        guide = self._map.get("import_guide", {})

        if mode == "single":
            steps = [p["method"] for p in plans]
            impact = "影响范围：仅涉及修改的文件/动作本身，不影响其它配置。"
            warning = "导入动作时 ID 相同会覆盖原动作；如需保留旧版，先在 Quicker 中改名或导出备份。"
        else:
            steps = list(guide.get("batch_workflow", []))
            impact = "影响范围：批量分享导入；常规数据对同账号为覆盖式，请只勾选本次必要数据。"
            warning = guide.get("note", "批量导入常规数据会覆盖同账号已有设置，必须先导出再导入。")

        return {
            "mode": mode,
            "plans": plans,
            "steps": steps,
            "impact": impact,
            "warning": warning,
        }

    # ---------- 动作 ----------

    def find_action(self, action_id_or_name: str) -> str:
        """
        在 actions\\ 下按动作 ID 或名称定位动作文件。

        Returns:
            动作文件路径
        """
        actions_dir = Path(self.export_root) / "actions"
        if not actions_dir.exists():
            raise FileNotFoundError(f"actions 目录不存在: {actions_dir}")
        target = (action_id_or_name or "").strip()
        if not target:
            raise ValueError("action_id_or_name 不能为空")
        for f in actions_dir.glob("action_*.json"):
            if target in f.stem:
                return str(f)
        raise FileNotFoundError(f"在 {actions_dir} 未找到动作: {target}")

    def list_actions(self) -> List[tuple]:
        """
        列出 actions\\ 下所有动作。

        Returns:
            [(动作ID, 标题, 文件路径), ...]（按文件名排序）
        """
        actions_dir = Path(self.export_root) / "actions"
        result = []
        if actions_dir.exists():
            for f in sorted(actions_dir.glob("action_*.json")):
                rest = f.stem[len("action_"):]
                aid, _, title = rest.partition("_")
                result.append((aid, title, str(f)))
        return result

    def read_action(self, action_id_or_name: str) -> Dict[str, Any]:
        """读取动作定义（外层元数据，Data 仍为 JSON 字符串）"""
        path = self.find_action(action_id_or_name)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def read_action_data(self, action_id_or_name: str):
        """
        读取并解析动作 Data（步骤/变量定义）。

        Returns:
            (动作元数据 dict, 解析后的 Data dict)
        """
        action = self.read_action(action_id_or_name)
        raw = action.get("Data")
        if not raw:
            raise ValueError(f"动作 {action.get('Id')} 没有 Data")
        return action, json.loads(raw)

    # ---------- 工具 ----------

    @staticmethod
    def _json_get(obj: Any, json_path: str) -> Any:
        """按 'A.B.C' 式路径取值（'[]' 仅作标记忽略）。

        自动解析嵌套的 JSON 字符串字段（如 settings 的 HotKeysData 本身是字符串，
        但内部又是 JSON），对调用方透明返回解析后的对象。
        """
        segs = [s for s in json_path.replace("[]", "").split(".") if s]
        cur = obj
        for seg in segs:
            if isinstance(cur, str):
                s = cur.strip()
                if s.startswith("{") or s.startswith("["):
                    try:
                        cur = json.loads(cur)
                    except Exception:
                        raise KeyError(f"字段 {seg} 是非法 JSON 字符串（路径 {json_path}）")
                else:
                    raise KeyError(f"字段路径经过非 JSON 字符串: {seg}（路径 {json_path}）")
            if isinstance(cur, dict) and seg in cur:
                cur = cur[seg]
            else:
                raise KeyError(f"字段不存在: {seg}（路径 {json_path}）")
        return cur

    @staticmethod
    def _json_set(obj: Any, json_path: str, value: Any) -> None:
        """按 'A.B.C' 式路径写值（'[]' 仅作标记忽略）。

        若路径途经嵌套 JSON 字符串字段（如 HotKeysData），修改后自动把该字段重新
        序列化为 JSON 字符串写回，保持原始文件结构不变。
        """
        segs = [s for s in json_path.replace("[]", "").split(".") if s]
        if not segs:
            raise ValueError(f"无效路径: {json_path}")

        def is_json_str(v: Any) -> bool:
            return isinstance(v, str) and v.strip().startswith(("{", "["))

        def walk(cur: Any, idx: int) -> Any:
            if isinstance(cur, str):
                if is_json_str(cur):
                    try:
                        cur = json.loads(cur)
                    except Exception:
                        raise KeyError(f"字段 {segs[idx]} 是非法 JSON 字符串（路径 {json_path}）")
                else:
                    raise KeyError(f"字段路径经过非 JSON 字符串: {segs[idx]}（路径 {json_path}）")
            if idx == len(segs) - 1:
                if not isinstance(cur, dict):
                    raise KeyError(f"字段不存在: {segs[idx]}（路径 {json_path}）")
                cur[segs[idx]] = value
                return cur
            if not isinstance(cur, dict) or segs[idx] not in cur:
                raise KeyError(f"字段不存在: {segs[idx]}（路径 {json_path}）")
            orig = cur[segs[idx]]
            new_child = walk(orig, idx + 1)
            if is_json_str(orig):
                new_child = json.dumps(new_child, ensure_ascii=False)
            cur[segs[idx]] = new_child
            return cur

        walk(obj, 0)


# 测试代码
def test():
    """测试 QuickerConnector"""
    print("=" * 60)
    print("测试 Quicker Connector")
    print("=" * 60)

    try:
        # 尝试 CSV 模式
        try:
            connector = QuickerConnector(source="csv")
            actions = connector.read_actions()
            print(f"\nCSV 模式: 找到 {len(actions)} 个动作")
        except FileNotFoundError:
            # 尝试数据库模式
            try:
                connector = QuickerConnector(source="db")
                actions = connector.read_actions()
                print(f"\n数据库模式: 找到 {len(actions)} 个动作")
            except FileNotFoundError:
                print("\n无法找到 Quicker 数据源（CSV 或数据库）")
                print("请确保已导出 Quicker 动作列表到 CSV 文件")
                return

        if actions:
            print("\n前 5 个动作:")
            for action in actions[:5]:
                print(f"  - {action.name} ({action.id})")

        # 测试搜索
        print("\n测试搜索 '截图':")
        results = connector.search_actions("截图")
        print(f"  找到 {len(results)} 个结果")
        for r in results[:3]:
            print(f"  - {r.name}")

        # 测试匹配
        print("\n测试匹配 '帮我截图':")
        matches = connector.match_actions("帮我截图")
        for m in matches[:3]:
            print(f"  - {m['action'].name} (分数: {m['score']:.2f})")

        print("\n" + "=" * 60)
        print("测试完成")
        print("=" * 60)

    except Exception as e:
        print(f"\n测试失败: {e}")
        import traceback
        traceback.print_exc()


def test_export_map():
    """测试 QuickerExportMap（数据维护/配置映射）"""
    print("=" * 60)
    print("测试 QuickerExportMap（数据维护）")
    print("=" * 60)
    try:
        qm = QuickerExportMap()
        print(f"\nexport_root: {qm.export_root}")
        print(f"映射: {qm.map_path}")

        # 1. 定位
        info = qm.locate("扩展热键")
        print(f"\nlocate('扩展热键') → file={info['file']}, json_path={info['json_path']}, writable={info['writable']}")

        # 2. 读取
        path, hotkeys = qm.read_config("扩展热键")
        print(f"read_config('扩展热键') → {path}")
        if isinstance(hotkeys, list):
            print(f"  ActionHotkeys 数量: {len(hotkeys)}")
            for h in hotkeys[:3]:
                print(f"  - {h.get('Title')} [{h.get('Keys')}] → {h.get('ActionId')}")

        # 3. 动作定位
        p1 = qm.find_action("5479d192")
        p2 = qm.find_action("视频旋转修复版")
        print(f"\nfind_action('5479d192') → {p1}")
        print(f"find_action('视频旋转修复版') → {p2}")

        # 4. 动作 Data 解析
        action, data = qm.read_action_data("5479d192")
        print(f"\nread_action_data('5479d192') → Title={action.get('Title')}, 变量数={len(data.get('Variables', []))}, 步骤数={len(data.get('Steps', []))}")

        # 5. 全量清单
        acts = qm.list_actions()
        print(f"\nlist_actions() → 共 {len(acts)} 个动作")

        # 6. 所有可定位功能
        feats = qm.list_features()
        print(f"\n可定位功能 {len(feats)} 项:")
        for f in feats:
            print(f"  - {f}")

        print("\n" + "=" * 60)
        print("QuickerExportMap 测试完成")
        print("=" * 60)
    except Exception as e:
        print(f"\nQuickerExportMap 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test()
    test_export_map()