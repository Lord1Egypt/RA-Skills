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


if __name__ == "__main__":
    test()