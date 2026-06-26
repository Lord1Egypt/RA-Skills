#!/usr/bin/env python3
"""
OpenClaw 秘书式记忆系统 - 偏好自动提取
从会话内容中增量提取用户偏好，只增不改

用法:
    python3 profile_miner.py --session "用户说：喜欢简洁的回答"
    python3 profile_miner.py --file /path/to/session.log --dry-run
    python3 profile_miner.py --list  # 查看当前已提取的偏好
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import argparse

# ============== 配置 ==============
MEMORY_DIR = Path(os.environ.get("OPENCLAW_MEMORY_DIR", "/root/.openclaw/workspace/memory"))
PROFILE_DIR = MEMORY_DIR / "profile"
PREFERENCES_FILE = PROFILE_DIR / "preferences" / "preferences.md"
HABITS_FILE = PROFILE_DIR / "habits" / "habits.md"
CONTACTS_FILE = PROFILE_DIR / "contacts" / "contacts.md"


# ============== 用户图谱集成 ==============

def _get_user_model_integration():
    """延迟加载用户图谱集成"""
    from user_model import ProfileMinerIntegration
    return ProfileMinerIntegration()

# ============== 偏好提取器 ==============

class ProfileMiner:
    # 偏好模式定义
    PREFERENCE_PATTERNS = {
        "communication_style": [
            (r'(?:喜欢|偏好|倾向)[:：]\s*(.+?)(?:\n|$)', 'communication'),
            (r'(?:回答|回复)[:：]?\s*(简洁|详细|简短|具体)', 'communication'),
        ],
        "technical_background": [
            (r'(?:熟悉|掌握|擅长)[:：]\s*(.+?)(?:\n|$)', 'tech'),
            (r'(?:了解|学习)[:：]\s*(.+?)(?:\n|$)', 'tech'),
            (r'(?:技术栈|技术背景)[:：]\s*(.+?)(?:\n|$)', 'tech'),
        ],
        "format_preference": [
            (r'(?:格式|形式)[:：]?\s*(列表|表格|markdown|图表|代码)', 'format'),
            (r'(?:喜欢|偏好).+?(列表|表格|markdown)', 'format'),
        ],
    }

    HABIT_PATTERNS = {
        "work_timing": [
            (r'(?:工作|开发)[:：]?\s*(?:时间|时段|时间段)[:：]\s*(.+?)(?:\n|$)', 'timing'),
            (r'(?:早上|下午|晚上|深夜)[起止至到].+?工作', 'timing'),
        ],
        "project_management": [
            (r'(?:使用|习惯).+?(看板|敏捷|scrum|每日站会)', 'pm'),
            (r'(?:项目).+?(计划|里程碑|deadline|截止)', 'pm'),
        ],
        "tools": [
            (r'(?:使用|习惯|喜欢)[:：]\s*(.+?)(?:编辑器|IDE|工具)', 'tools'),
            (r'(?:编辑器|IDE)[:：]\s*(.+?)(?:\n|$)', 'tools'),
        ],
    }

    CONTACT_PATTERNS = {
        "name": [
            (r'(?:用户|客户|联系人)[:：]\s*([A-Za-z\u4e00-\u9fa5]{2,10})', 'name'),
        ],
        "email": [
            (r'[\w.-]+@[\w.-]+\.\w+', 'email'),
        ],
        "role": [
            (r'(?:职位|角色|title)[:：]\s*(.+?)(?:\n|$)', 'role'),
        ],
    }

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.ensure_profile_dirs()

    def ensure_profile_dirs(self):
        """确保 profile 目录结构存在"""
        (PROFILE_DIR / "preferences").mkdir(parents=True, exist_ok=True)
        (PROFILE_DIR / "habits").mkdir(parents=True, exist_ok=True)
        (PROFILE_DIR / "contacts").mkdir(parents=True, exist_ok=True)

    def read_file(self, path: Path) -> str:
        """读取文件内容，不存在则返回空"""
        if path.exists():
            return path.read_text(encoding="utf-8")
        return ""

    def file_contains(self, path: Path, text: str) -> bool:
        """检查文本是否已存在于文件中（避免重复添加）"""
        if not path.exists():
            return False
        content = path.read_text(encoding="utf-8")
        return text in content

    def extract_preferences(self, text: str) -> List[Tuple[str, str]]:
        """从文本中提取偏好，返回 [(category, value)] 列表"""
        results = []

        for category, patterns in self.PREFERENCE_PATTERNS.items():
            for pattern, subcat in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for m in matches:
                    if isinstance(m, tuple):
                        m = m[0] if m[0] else (m[1] if len(m) > 1 else "")
                    value = m.strip() if isinstance(m, str) else str(m).strip()
                    if value and len(value) >= 2:
                        results.append((f"preferences.{category}.{subcat}", value))

        return results

    def extract_habits(self, text: str) -> List[Tuple[str, str]]:
        """从文本中提取习惯，返回 [(category, value)] 列表"""
        results = []

        for category, patterns in self.HABIT_PATTERNS.items():
            for pattern, subcat in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for m in matches:
                    if isinstance(m, tuple):
                        m = m[0] if m[0] else (m[1] if len(m) > 1 else "")
                    value = m.strip() if isinstance(m, str) else str(m).strip()
                    if value and len(value) >= 2:
                        results.append((f"habits.{category}.{subcat}", value))

        return results

    def extract_contacts(self, text: str) -> List[Tuple[str, str]]:
        """从文本中提取联系人信息，返回 [(category, value)] 列表"""
        results = []

        for category, patterns in self.CONTACT_PATTERNS.items():
            for pattern, subcat in patterns:
                matches = re.findall(pattern, text)
                for m in matches:
                    value = m.strip() if isinstance(m, str) else str(m).strip()
                    if value and len(value) >= 2:
                        results.append((f"contacts.{category}.{subcat}", value))

        return results

    def append_to_file(self, path: Path, category: str, value: str) -> bool:
        """追加偏好到指定文件，返回是否成功"""
        timestamp = datetime.now().strftime("%Y-%m-%d")

        # 检查是否已存在
        if self.file_contains(path, value):
            return False

        content = self.read_file(path)

        # 如果文件为空或没有标题，添加标题
        if not content.strip():
            if "preferences" in str(path):
                content = "# 用户偏好\n\n"
            elif "habits" in str(path):
                content = "# 用户习惯\n\n"
            elif "contacts" in str(path):
                content = "# 联系人\n\n"

        # 检查是否已有该分类
        section_header = f"## {category.split('.')[-1].replace('_', ' ').title()}"
        if section_header not in content:
            content += f"\n{section_header}\n"

        # 添加新条目（带时间戳）
        new_entry = f"- [{timestamp}] {value}\n"
        content += new_entry

        if not self.dry_run:
            path.write_text(content, encoding="utf-8")

        return True

    def mine(self, text: str) -> Dict[str, List]:
        """从文本中挖掘所有类型的偏好"""
        all_extracted = {
            "preferences": [],
            "habits": [],
            "contacts": []
        }

        all_extracted["preferences"] = self.extract_preferences(text)
        all_extracted["habits"] = self.extract_habits(text)
        all_extracted["contacts"] = self.extract_contacts(text)

        return all_extracted

    def process(self, text: str) -> Dict[str, int]:
        """处理文本，提取并保存偏好，返回统计"""
        extracted = self.mine(text)

        stats = {
            "preferences": 0,
            "habits": 0,
            "contacts": 0,
            "skipped": 0
        }

        # 处理偏好
        for category, value in extracted["preferences"]:
            if self.append_to_file(PREFERENCES_FILE, category, value):
                stats["preferences"] += 1
            else:
                stats["skipped"] += 1

        # 处理习惯
        for category, value in extracted["habits"]:
            if self.append_to_file(HABITS_FILE, category, value):
                stats["habits"] += 1
            else:
                stats["skipped"] += 1

        # 处理联系人
        for category, value in extracted["contacts"]:
            if self.append_to_file(CONTACTS_FILE, category, value):
                stats["contacts"] += 1
            else:
                stats["skipped"] += 1

        # ========== 用户图谱更新 ==========
        if not self.dry_run and text.strip():
            try:
                integration = _get_user_model_integration()
                graph_result = integration.process_session(text)
                stats["graph_entities"] = graph_result.get("entities_found", 0)
                stats["graph_relations"] = graph_result.get("relations_found", 0)
            except Exception as e:
                print(f"[ProfileMiner] 图谱更新失败: {e}")
        # ========== 图谱更新结束 ==========

        return stats

    def list_current(self) -> str:
        """列出当前已提取的偏好"""
        output = ["## 当前用户画像\n"]

        # 偏好
        pref_content = self.read_file(PREFERENCES_FILE)
        if pref_content.strip():
            output.append("\n### 偏好\n")
            output.append(pref_content)
        else:
            output.append("\n### 偏好\n(暂无记录)\n")

        # 习惯
        habits_content = self.read_file(HABITS_FILE)
        if habits_content.strip():
            output.append("\n### 习惯\n")
            output.append(habits_content)
        else:
            output.append("\n### 习惯\n(暂无记录)\n")

        # 联系人
        contacts_content = self.read_file(CONTACTS_FILE)
        if contacts_content.strip():
            output.append("\n### 联系人\n")
            output.append(contacts_content)
        else:
            output.append("\n### 联系人\n(暂无记录)\n")

        return '\n'.join(output)


# ============== 主程序 ==============

def main():
    parser = argparse.ArgumentParser(description="OpenClaw 秘书式记忆系统 - 偏好提取")
    parser.add_argument("--session", "-s", default="", help="会话内容")
    parser.add_argument("--file", "-f", type=Path, help="从文件读取内容")
    parser.add_argument("--dry-run", action="store_true", help="预览将要提取的偏好，不写入")
    parser.add_argument("--list", "-l", action="store_true", help="列出当前已提取的偏好")
    parser.add_argument("--json", "-j", action="store_true", help="输出 JSON 格式")
    args = parser.parse_args()

    miner = ProfileMiner(dry_run=args.dry_run)

    # 列出当前偏好
    if args.list:
        print(miner.list_current())
        return

    # 获取要处理的内容
    text = ""
    if args.session:
        text = args.session
    if args.file:
        if args.file.exists():
            text = args.file.read_text(encoding="utf-8")
        else:
            print(f"[Error] 文件不存在: {args.file}")
            return

    if not text:
        parser.print_help()
        print("\n[Error] 请提供 --session 或 --file 参数")
        return

    if args.dry_run:
        print("[Dry Run] 预览提取结果:")
        extracted = miner.mine(text)
        print(json.dumps(extracted, ensure_ascii=False, indent=2))
        return

    if args.json:
        extracted = miner.mine(text)
        print(json.dumps(extracted, ensure_ascii=False, indent=2))
        return

    # 执行提取
    stats = miner.process(text)

    if stats["preferences"] + stats["habits"] + stats["contacts"] > 0:
        print(f"[OK] 提取完成:")
        print(f"  偏好: {stats['preferences']} 条")
        print(f"  习惯: {stats['habits']} 条")
        print(f"  联系人: {stats['contacts']} 条")
        if stats["skipped"] > 0:
            print(f"  跳过(已存在): {stats['skipped']} 条")
    else:
        print("[Info] 未提取到新偏好")


if __name__ == "__main__":
    main()
