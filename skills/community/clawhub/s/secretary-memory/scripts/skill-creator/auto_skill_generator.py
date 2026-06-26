#!/usr/bin/env python3
"""
OpenClaw Skill Creator - 自动 Skill 生成系统
检测复杂/重复任务，自动生成新的 skill

用法:
    python3 auto_skill_generator.py --detect              # 检测复杂任务
    python3 auto_skill_generator.py --generate --name "xxx"  # 生成新 Skill
    python3 auto_skill_generator.py --register --skill "xxx" --triggers "a,b,c"
    python3 auto_skill_generator.py --stats              # 查看统计
    python3 auto_skill_generator.py --improve            # 自我改进

触发时机: 同一问题出现 3 次以上时自动建议
"""

import os
import re
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from collections import defaultdict
import argparse

# ============== 配置 ==============
MEMORY_DIR = Path(os.environ.get("OPENCLAW_MEMORY_DIR", "/root/.openclaw/workspace/memory"))
SKILLS_DIR = MEMORY_DIR / ".generated_skills"  # 生成的 skill 存放目录
PATTERN_DB = MEMORY_DIR / ".task_patterns.json"  # 任务模式数据库
TRIGGER_DB = MEMORY_DIR / ".skill_triggers.json"  # 触发词数据库
SKILL_CREATOR_DIR = Path(__file__).parent  # skill-creator 目录

# 阈值
COMPLEXITY_THRESHOLD = 3  # 出现 N 次视为复杂
SKILL_SIMILARITY_THRESHOLD = 0.8  # 相似度阈值


# ============== 周期性提醒器 ==============

class ReminderChecker:
    """周期性检查是否有什么值得记住"""

    # 值得记住的模式（用户可能忘记的）
    WORTH_REMEMBERING = {
        "decision": {
            "keywords": ["决定", "采用", "选择", "定了", "最终方案", "结论"],
            "weight": 2.0,
            "suggestion": "这像个重要决策，值得写入记忆"
        },
        "preference": {
            "keywords": ["喜欢", "偏好", "习惯", "不要", "避免", "宁愿"],
            "weight": 1.8,
            "suggestion": "这像是个用户偏好，值得记录"
        },
        "commitment": {
            "keywords": ["会做", "答应", "承诺", "下次", "稍后", "回头"],
            "weight": 1.5,
            "suggestion": "这是个待办承诺，记得写入 agenda"
        },
        "complex_solution": {
            "keywords": ["复杂", "绕路", "hack", " workaround", "临时方案"],
            "weight": 1.3,
            "suggestion": "这是个复杂的技术方案，值得沉淀到 knowledge"
        }
    }

    def __init__(self):
        self.memory_dir = MEMORY_DIR

    def scan_recent_sessions(self, days: int = 3) -> List[Dict]:
        """扫描近期会话，找出值得记住的内容

        Args:
            days: 扫描近几天的会话

        Returns:
            值得记住的建议列表
        """
        suggestions = []
        daily_dir = self.memory_dir / "daily"

        if not daily_dir.exists():
            return suggestions

        cutoff = datetime.now() - timedelta(days=days)

        for f in daily_dir.glob("*.md"):
            try:
                # 解析日期
                date_str = f.stem  # 如 "2026-04-30"
                try:
                    file_date = datetime.strptime(date_str, "%Y-%m-%d")
                    if file_date < cutoff:
                        continue
                except ValueError:
                    continue

                content = f.read_text(encoding="utf-8")
                file_suggestions = self._analyze_content(content, date_str)
                suggestions.extend(file_suggestions)

            except Exception:
                pass

        return suggestions

    def _analyze_content(self, content: str, date: str) -> List[Dict]:
        """分析内容，找出值得记住的部分"""
        suggestions = []
        lines = content.split("\n")

        for i, line in enumerate(lines):
            line_lower = line.lower()

            for pattern_type, pattern_info in self.WORTH_REMEMBERING.items():
                for kw in pattern_info["keywords"]:
                    if kw.lower() in line_lower:
                        # 找到上下文（前后各2行）
                        context_start = max(0, i - 2)
                        context_end = min(len(lines), i + 3)
                        context = "\n".join(lines[context_start:context_end])

                        suggestions.append({
                            "type": pattern_type,
                            "date": date,
                            "keyword": kw,
                            "suggestion": pattern_info["suggestion"],
                            "context": context.strip()[:300],
                            "line": i + 1
                        })
                        break  # 每个模式只匹配一次

        return suggestions

    def check_forgotten(self, days: int = 3) -> Dict:
        """检查是否有值得记住但还没记住的内容

        Returns:
            {
                "total_found": int,
                "suggestions": [...],
                "memory_reminders": [...]  # 格式化后可直接使用的提醒
            }
        """
        suggestions = self.scan_recent_sessions(days)

        # 去重
        seen = set()
        unique = []
        for s in suggestions:
            key = (s["type"], s["context"][:50])
            if key not in seen:
                seen.add(key)
                unique.append(s)

        # 格式化为提醒
        reminders = []
        for s in unique:
            reminders.append({
                "date": s["date"],
                "type": s["type"],
                "reminder": s["suggestion"],
                "context": s["context"]
            })

        return {
            "total_found": len(unique),
            "suggestions": unique,
            "memory_reminders": reminders
        }


# ============== 模式检测器 ==============

class PatternDetector:
    """复杂任务模式检测器"""

    # 复杂任务模式
    COMPLEX_PATTERNS = {
        "task_tracking": {
            "keywords": ["任务", "todo", "追踪", "待办", "计划", "进度"],
            "weight": 1.5,
            "suggested_name": "task-tracker"
        },
        "code_review": {
            "keywords": ["代码审查", "review", "PR", "merge", "代码检查"],
            "weight": 1.5,
            "suggested_name": "code-review"
        },
        "bug_triage": {
            "keywords": ["bug", "修复", "问题", "错误", "缺陷", "issue"],
            "weight": 1.3,
            "suggested_name": "bug-triage"
        },
        "meeting_notes": {
            "keywords": ["会议", "meeting", "纪要", "议程", "notes"],
            "weight": 1.2,
            "suggested_name": "meeting-notes"
        },
        "data_analysis": {
            "keywords": ["分析", "数据", "报表", "统计", "analytics"],
            "weight": 1.4,
            "suggested_name": "data-analysis"
        },
        "doc_generation": {
            "keywords": ["文档", "doc", "生成", "markdown", "README"],
            "weight": 1.3,
            "suggested_name": "doc-generator"
        },
        "test_generation": {
            "keywords": ["测试", "test", "用例", "coverage"],
            "weight": 1.4,
            "suggested_name": "test-generator"
        },
        "deployment": {
            "keywords": ["部署", "deploy", "发布", "上线", "release"],
            "weight": 1.5,
            "suggested_name": "deploy-helper"
        },
        "api_design": {
            "keywords": ["API", "接口", "rest", "endpoint", "endpoint"],
            "weight": 1.4,
            "suggested_name": "api-designer"
        },
        "db_schema": {
            "keywords": ["数据库", "schema", "表结构", "migration", "db"],
            "weight": 1.4,
            "suggested_name": "db-schema-manager"
        }
    }

    def __init__(self):
        self.patterns = self._load_patterns()

    def _load_patterns(self) -> Dict:
        """加载任务模式数据库"""
        if PATTERN_DB.exists():
            try:
                return json.loads(PATTERN_DB.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {
            "detected_patterns": {},  # {pattern_id: {type, count, first_seen, last_seen, examples}}
            "version": 1
        }

    def _save_patterns(self):
        """保存任务模式数据库"""
        PATTERN_DB.write_text(
            json.dumps(self.patterns, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def detect_from_text(self, text: str, session_id: str = "") -> List[Dict]:
        """从文本中检测复杂任务模式

        Returns:
            检测到的模式列表 [{type, keywords, count, confidence}]
        """
        text_lower = text.lower()
        detected = []

        for pattern_type, pattern_info in self.COMPLEX_PATTERNS.items():
            matches = []
            for kw in pattern_info["keywords"]:
                if kw.lower() in text_lower:
                    matches.append(kw)

            if matches:
                confidence = len(matches) / len(pattern_info["keywords"])

                # 更新模式计数
                pattern_id = pattern_type
                if pattern_id not in self.patterns["detected_patterns"]:
                    self.patterns["detected_patterns"][pattern_id] = {
                        "type": pattern_type,
                        "count": 0,
                        "first_seen": datetime.now().isoformat(),
                        "last_seen": None,
                        "examples": [],
                        "keywords": matches
                    }

                self.patterns["detected_patterns"][pattern_id]["count"] += 1
                self.patterns["detected_patterns"][pattern_id]["last_seen"] = datetime.now().isoformat()

                # 记录示例
                if session_id and len(self.patterns["detected_patterns"][pattern_id]["examples"]) < 5:
                    self.patterns["detected_patterns"][pattern_id]["examples"].append({
                        "session_id": session_id,
                        "text": text[:200],
                        "timestamp": datetime.now().isoformat()
                    })

                detected.append({
                    "type": pattern_type,
                    "suggested_name": pattern_info["suggested_name"],
                    "matched_keywords": matches,
                    "confidence": confidence,
                    "count": self.patterns["detected_patterns"][pattern_id]["count"],
                    "is_complex": self.patterns["detected_patterns"][pattern_id]["count"] >= COMPLEXITY_THRESHOLD
                })

        if detected:
            self._save_patterns()

        return detected

    def get_complex_patterns(self) -> List[Dict]:
        """获取已达到复杂度阈值的模式"""
        complex = []

        for pattern_id, info in self.patterns["detected_patterns"].items():
            if info["count"] >= COMPLEXITY_THRESHOLD:
                pattern_info = self.COMPLEX_PATTERNS.get(pattern_id, {})
                complex.append({
                    "type": pattern_id,
                    "suggested_name": pattern_info.get("suggested_name", pattern_id),
                    "count": info["count"],
                    "first_seen": info["first_seen"],
                    "last_seen": info["last_seen"],
                    "examples": info.get("examples", [])
                })

        # 按出现次数排序
        complex.sort(key=lambda x: -x["count"])
        return complex

    def analyze_task_pattern(self, text: str) -> Dict:
        """分析任务模式，返回建议

        Returns:
            {
                "is_complex": bool,
                "pattern_type": str,
                "suggested_skill_name": str,
                "extracted_steps": [...],
                "confidence": float
            }
        """
        detected = self.detect_from_text(text)

        if not detected:
            return {"is_complex": False}

        # 找最匹配的模式
        best = max(detected, key=lambda x: (x["confidence"], x["count"]))

        if not best["is_complex"]:
            return {"is_complex": False}

        # 提取解决步骤
        steps = self._extract_steps(text)

        return {
            "is_complex": True,
            "pattern_type": best["type"],
            "suggested_skill_name": best["suggested_name"],
            "matched_keywords": best["matched_keywords"],
            "count": best["count"],
            "extracted_steps": steps,
            "confidence": best["confidence"]
        }

    def _extract_steps(self, text: str) -> List[str]:
        """从文本中提取任务步骤"""
        steps = []

        # 数字列表
        number_pattern = r'(?:^\d+[.、)]\s*.+)'
        matches = re.findall(number_pattern, text, re.MULTILINE)
        steps.extend([m.strip() for m in matches if len(m.strip()) > 5])

        # 破折号列表
        dash_pattern = r'(?:^-+\s*.+)'
        matches = re.findall(dash_pattern, text, re.MULTILINE)
        steps.extend([m.strip() for m in matches if len(m.strip()) > 5])

        # 提取的步骤去重
        seen = set()
        unique = []
        for s in steps:
            key = s[:50].lower()
            if key not in seen:
                seen.add(key)
                unique.append(s)

        return unique[:10]  # 最多10步


# ============== Skill 生成器 ==============

class SkillGenerator:
    """Skill 文件生成器"""

    def __init__(self):
        self.skills_dir = SKILLS_DIR
        self.skills_dir.mkdir(parents=True, exist_ok=True)

    def generate_skill(
        self,
        name: str,
        pattern_type: str,
        description: str = "",
        steps: List[str] = None,
        triggers: List[str] = None
    ) -> Tuple[bool, str]:
        """生成新的 Skill

        Args:
            name: Skill 名称（英文，简短）
            pattern_type: 模式类型
            description: 描述
            steps: 执行步骤
            triggers: 触发词列表

        Returns:
            (成功标志, 消息/Skill路径)
        """
        # 清理名称
        safe_name = re.sub(r'[^a-zA-Z0-9_-]', '-', name.lower())
        skill_dir = self.skills_dir / safe_name

        if skill_dir.exists():
            return False, f"Skill 已存在: {safe_name}"

        try:
            # 创建目录结构
            skill_dir.mkdir(parents=True, exist_ok=True)
            (skill_dir / "scripts").mkdir(exist_ok=True)
            (skill_dir / "references").mkdir(exist_ok=True)

            # 生成 SKILL.md
            self._generate_skill_md(skill_dir, name, pattern_type, description, steps, triggers)

            # 生成主脚本
            self._generate_main_script(skill_dir, name, pattern_type, steps)

            # 生成 README.md
            self._generate_readme(skill_dir, name, description, triggers)

            # 记录生成信息
            self._save_skill_meta(skill_dir, name, pattern_type, triggers)

            return True, str(skill_dir)

        except Exception as e:
            # 清理失败创建的目录
            if skill_dir.exists():
                import shutil
                shutil.rmtree(skill_dir)
            return False, f"生成失败: {e}"

    def _generate_skill_md(
        self,
        skill_dir: Path,
        name: str,
        pattern_type: str,
        description: str,
        steps: List[str],
        triggers: List[str]
    ):
        """生成 SKILL.md"""
        steps_text = ""
        if steps:
            steps_text = "\n## 执行步骤\n\n" + "\n".join([f"{i+1}. {s}" for i, s in enumerate(steps)])

        triggers_text = ""
        if triggers:
            triggers_text = "\n## 触发词\n\n" + ", ".join(triggers)

        content = f"""# {name}

自动生成的 Skill - {pattern_type}

## 功能

{description or f'自动化处理 {pattern_type} 相关任务'}

{steps_text}
{triggers_text}

## 使用方式

```bash
python3 scripts/{name}.py [参数]
```

## 自动生成信息

- 生成时间: {datetime.now().isoformat()}
- 模式类型: {pattern_type}
- 来源: secretary-memory auto-skill-generator
"""

        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")

    def _generate_main_script(
        self,
        skill_dir: Path,
        name: str,
        pattern_type: str,
        steps: List[str]
    ):
        """生成主脚本"""
        steps_json = json.dumps(steps or [], ensure_ascii=False)

        content = f'''#!/usr/bin/env python3
"""
{name} - 自动生成的 Skill
模式类型: {pattern_type}
"""

import sys
import json
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent

def main():
    """主入口"""
    import argparse

    parser = argparse.ArgumentParser(description="{name}")
    parser.add_argument("--input", "-i", help="输入数据")
    parser.add_argument("--output", "-o", help="输出文件")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    args = parser.parse_args()

    # 预设步骤
    steps = {steps_json}

    if args.verbose:
        print(f"[{name}] 模式类型: {pattern_type}")
        print(f"[{name}] 步骤数: {{len(steps)}}")

    # TODO: 实现自动化逻辑
    print(f"[{name}] TODO: 实现自动化逻辑")

    return 0

if __name__ == "__main__":
    sys.exit(main())
'''

        script_path = skill_dir / "scripts" / f"{name}.py"
        script_path.write_text(content, encoding="utf-8")

    def _generate_readme(
        self,
        skill_dir: Path,
        name: str,
        description: str,
        triggers: List[str]
    ):
        """生成 README.md"""
        triggers_text = ""
        if triggers:
            triggers_text = "\n## 触发词\n\n" + ", ".join(triggers) + "\n"

        content = f"""# {name}

{description or f'自动化处理 {name} 相关任务'}

{triggers_text}

## 使用方法

1. 安装依赖（如有）
2. 运行主脚本

```bash
python3 scripts/{name}.py --help
```
"""

        (skill_dir / "README.md").write_text(content, encoding="utf-8")

    def _save_skill_meta(self, skill_dir: Path, name: str, pattern_type: str, triggers: List[str]):
        """保存 Skill 元数据"""
        meta = {
            "name": name,
            "path": str(skill_dir),
            "pattern_type": pattern_type,
            "triggers": triggers or [],
            "created_at": datetime.now().isoformat(),
            "usage_count": 0,
            "feedback": []
        }

        (skill_dir / ".meta.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def list_generated_skills(self) -> List[Dict]:
        """列出所有已生成的 Skill"""
        skills = []

        if not self.skills_dir.exists():
            return skills

        for skill_dir in self.skills_dir.iterdir():
            if skill_dir.is_dir():
                meta_file = skill_dir / ".meta.json"
                if meta_file.exists():
                    try:
                        meta = json.loads(meta_file.read_text(encoding="utf-8"))
                        skills.append(meta)
                    except Exception:
                        pass

        return sorted(skills, key=lambda x: -x.get("usage_count", 0))


# ============== 触发词注册器 ==============

class TriggerRegistry:
    """触发词注册器"""

    def __init__(self):
        self.triggers = self._load_triggers()

    def _load_triggers(self) -> Dict:
        """加载触发词数据库"""
        if TRIGGER_DB.exists():
            try:
                return json.loads(TRIGGER_DB.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {
            "triggers": {},  # {trigger_word: skill_name}
            "skills": {},    # {skill_name: {triggers: [], registered_at: ...}}
            "version": 1
        }

    def _save_triggers(self):
        """保存触发词数据库"""
        TRIGGER_DB.write_text(
            json.dumps(self.triggers, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def register(self, skill_name: str, triggers: List[str]) -> bool:
        """注册触发词

        Args:
            skill_name: Skill 名称
            triggers: 触发词列表

        Returns:
            是否成功
        """
        for trigger in triggers:
            trigger = trigger.strip().lower()
            if trigger:
                self.triggers["triggers"][trigger] = skill_name

        self.triggers["skills"][skill_name] = {
            "triggers": triggers,
            "registered_at": datetime.now().isoformat()
        }

        self._save_triggers()
        return True

    def lookup(self, text: str) -> Optional[str]:
        """查找文本匹配的 Skill

        Args:
            text: 输入文本

        Returns:
            匹配的 Skill 名称
        """
        text_lower = text.lower()

        # 精确匹配
        for trigger, skill_name in self.triggers["triggers"].items():
            if trigger in text_lower:
                return skill_name

        return None

    def get_skill_triggers(self, skill_name: str) -> List[str]:
        """获取 Skill 的所有触发词"""
        if skill_name in self.triggers["skills"]:
            return self.triggers["skills"][skill_name].get("triggers", [])
        return []

    def unregister(self, skill_name: str) -> bool:
        """取消注册"""
        if skill_name not in self.triggers["skills"]:
            return False

        # 移除所有触发词
        triggers_to_remove = []
        for trigger, sname in self.triggers["triggers"].items():
            if sname == skill_name:
                triggers_to_remove.append(trigger)

        for trigger in triggers_to_remove:
            del self.triggers["triggers"][trigger]

        del self.triggers["skills"][skill_name]

        self._save_triggers()
        return True


# ============== 自我改进器 ==============

class SelfImprover:
    """Skill 自我改进器"""

    def __init__(self):
        self.detector = PatternDetector()
        self.generator = SkillGenerator()
        self.registry = TriggerRegistry()

    def record_usage(self, skill_name: str, success: bool, feedback: str = "", context: str = ""):
        """记录 Skill 使用情况

        Args:
            skill_name: Skill 名称
            success: 是否成功
            feedback: 用户反馈
            context: 执行上下文（用于后续分析）
        """
        skills = self.generator.list_generated_skills()
        for skill in skills:
            if skill["name"] == skill_name:
                skill["usage_count"] += 1
                skill["feedback"].append({
                    "success": success,
                    "feedback": feedback,
                    "context": context[:200] if context else "",
                    "timestamp": datetime.now().isoformat()
                })

                # 限制反馈数量（保留最近50条）
                if len(skill["feedback"]) > 50:
                    skill["feedback"] = skill["feedback"][-50:]

                # 保存更新
                meta_file = Path(skill["path"]) / ".meta.json"
                meta_file.write_text(
                    json.dumps(skill, ensure_ascii=False, indent=2),
                    encoding="utf-8"
                )

                # 同时更新主数据库
                self._update_main_db(skill_name, success, feedback)
                break

    def _update_main_db(self, skill_name: str, success: bool, feedback: str):
        """更新主数据库（用于自我改进分析）"""
        db_path = MEMORY_DIR / ".skill_performance.json"
        db = {}
        if db_path.exists():
            try:
                db = json.loads(db_path.read_text(encoding="utf-8"))
            except Exception:
                pass

        if skill_name not in db:
            db[skill_name] = {"records": [], "last_improve": None}

        db[skill_name]["records"].append({
            "success": success,
            "feedback": feedback,
            "timestamp": datetime.now().isoformat()
        })

        # 只保留最近100条
        if len(db[skill_name]["records"]) > 100:
            db[skill_name]["records"] = db[skill_name]["records"][-100:]

        db_path.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")

    def analyze_feedback(self, skill_name: str) -> Dict:
        """分析 Skill 反馈，生成改进建议"""
        skills = self.generator.list_generated_skills()
        skill = None
        for s in skills:
            if s["name"] == skill_name:
                skill = s
                break

        if not skill:
            return {"error": "Skill not found"}

        feedback_list = skill.get("feedback", [])

        if not feedback_list:
            return {"suggestions": [], "score": 0}

        # 统计成功率
        successful = sum(1 for f in feedback_list if f.get("success"))
        success_rate = successful / len(feedback_list) if feedback_list else 0

        # 分析失败原因
        common_issues = []
        for f in feedback_list:
            if not f.get("success") and f.get("feedback"):
                # 简单关键词分析
                fb = f["feedback"].lower()
                if "不工作" in fb or "失败" in fb:
                    common_issues.append("执行失败")
                if "慢" in fb:
                    common_issues.append("性能问题")
                if "缺少" in fb or "没有" in fb:
                    common_issues.append("功能不完整")

        suggestions = list(set(common_issues))

        return {
            "skill_name": skill_name,
            "usage_count": skill.get("usage_count", 0),
            "success_rate": round(success_rate * 100, 1),
            "common_issues": suggestions,
            "suggestions": [f"考虑优化: {s}" for s in suggestions] if suggestions else ["当前表现良好"]
        }

    def improve(self, skill_name: str = None, dry_run: bool = False) -> Dict:
        """执行自我改进

        Args:
            skill_name: 可选，指定要改进的 Skill
            dry_run: True 则只分析不实际改进

        Returns:
            改进结果
        """
        # 加载性能数据库
        db_path = MEMORY_DIR / ".skill_performance.json"
        db = {}
        if db_path.exists():
            try:
                db = json.loads(db_path.read_text(encoding="utf-8"))
            except Exception:
                pass

        def analyze_and_improve(sname: str) -> Dict:
            """分析单个 Skill 并应用改进"""
            records = db.get(sname, {}).get("records", [])
            if not records:
                return {"skill_name": sname, "analysis": {"success_rate": 100}, "improvements_applied": []}

            # 统计分析
            successful = sum(1 for r in records if r.get("success"))
            success_rate = successful / len(records) if records else 100

            # 分析失败原因，生成改进建议
            issues = []
            for r in records:
                if not r.get("success") and r.get("feedback"):
                    fb = r["feedback"].lower()
                    if any(kw in fb for kw in ["不工作", "失败", "error", "crash"]):
                        issues.append("执行失败")
                    if any(kw in fb for kw in ["慢", "timeout", "卡"]):
                        issues.append("性能问题")
                    if any(kw in fb for kw in ["缺少", "没有", "不支持"]):
                        issues.append("功能不完整")

            issues = list(set(issues))
            improvements = []

            # 根据问题应用真实改进
            if not dry_run and issues:
                for issue in issues:
                    if issue == "功能不完整":
                        # 更新 SKILL.md，标记为 TODO
                        skill_path = SKILLS_DIR / sname / "SKILL.md"
                        if skill_path.exists():
                            content = skill_path.read_text(encoding="utf-8")
                            if "## 已知问题" not in content:
                                content += f"\n\n## 已知问题\n\n- 此功能有待完善\n"
                            skill_path.write_text(content, encoding="utf-8")
                            improvements.append("已更新 SKILL.md 标注待完善")

                    elif issue == "性能问题":
                        # 更新 meta 标记低分
                        skills = self.generator.list_generated_skills()
                        for s in skills:
                            if s["name"] == sname:
                                s["performance_issue"] = True
                                meta_file = Path(s["path"]) / ".meta.json"
                                meta_file.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")
                                improvements.append("已标记性能问题")
                                break

            return {
                "skill_name": sname,
                "analysis": {
                    "success_rate": round(success_rate * 100, 1),
                    "total_runs": len(records),
                    "common_issues": issues
                },
                "improvements_applied": improvements if not dry_run else ["(dry-run) " + i for i in improvements]
            }

        if skill_name:
            return analyze_and_improve(skill_name)

        # 改进所有 Skill
        skills = self.generator.list_generated_skills()
        results = []

        for skill in skills:
            analysis_result = analyze_and_improve(skill["name"])
            if analysis_result["analysis"].get("success_rate", 100) < 70 or analysis_result["improvements_applied"]:
                results.append(analysis_result)

            # 更新最后改进时间
            if skill_name in db:
                db[skill_name]["last_improve"] = datetime.now().isoformat()

        # 保存数据库
        if not dry_run:
            db_path.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")

        return {
            "skills_analyzed": len(skills),
            "needs_improvement": len([r for r in results if r["analysis"].get("success_rate", 100) < 70]),
            "improvements_made": len([r for r in results if r["improvements_applied"]]),
            "details": results,
            "dry_run": dry_run
        }


# ============== 主程序 ==============

def main():
    parser = argparse.ArgumentParser(description="OpenClaw 自动 Skill 生成器")
    parser.add_argument("--detect", "-d", action="store_true", help="检测复杂任务")
    parser.add_argument("--remind", action="store_true", help="[NEW] 周期性提醒：检查值得记住的内容")
    parser.add_argument("--days", type=int, default=3, help="提醒扫描近几天（默认3天）")
    parser.add_argument("--generate", "-g", action="store_true", help="生成新 Skill")
    parser.add_argument("--name", "-n", help="Skill 名称")
    parser.add_argument("--pattern", "-p", help="模式类型")
    parser.add_argument("--description", help="Skill 描述")
    parser.add_argument("--steps", nargs="+", help="执行步骤")
    parser.add_argument("--triggers", "-t", help="触发词（逗号分隔）")
    parser.add_argument("--register", "-r", action="store_true", help="注册触发词")
    parser.add_argument("--skill", "-s", help="Skill 名称")
    parser.add_argument("--stats", action="store_true", help="查看统计")
    parser.add_argument("--improve", "-i", action="store_true", help="自我改进")
    parser.add_argument("--dry-run", action="store_true", help="改进预览（不实际应用）")
    parser.add_argument("--record", action="store_true", help="[NEW] 记录 Skill 执行结果")
    parser.add_argument("--success", action="store_true", help="执行成功")
    parser.add_argument("--feedback", help="执行反馈")
    parser.add_argument("--context", help="执行上下文")
    parser.add_argument("--list", "-l", action="store_true", help="列出已生成的 Skills")
    args = parser.parse_args()

    # 检测复杂任务
    if args.detect:
        detector = PatternDetector()

        # 扫描 memory 中的历史记录
        print("[检测] 分析历史记录...")
        daily_dir = MEMORY_DIR / "daily"
        if daily_dir.exists():
            for f in daily_dir.glob("*.md"):
                try:
                    text = f.read_text(encoding="utf-8")
                    detector.detect_from_text(text)
                except Exception:
                    pass

        complex_patterns = detector.get_complex_patterns()

        if complex_patterns:
            print(f"\n## 检测到 {len(complex_patterns)} 个复杂任务模式:\n")
            for p in complex_patterns:
                print(f"### {p['type']}")
                print(f"  - 出现次数: {p['count']}")
                print(f"  - 建议名称: {p['suggested_name']}")
                print(f"  - 首次出现: {p['first_seen'][:10]}")
                print(f"  - 最近出现: {p['last_seen'][:10]}")
                if p.get('examples'):
                    print(f"  - 示例数: {len(p['examples'])}")
                print()
        else:
            print("[检测] 未发现复杂任务模式")
        return

    # 生成新 Skill
    if args.generate:
        if not args.name:
            print("[Error] 请提供 --name 参数")
            return

        generator = SkillGenerator()

        # 解析触发词
        triggers = []
        if args.triggers:
            triggers = [t.strip() for t in args.triggers.split(",")]

        # 解析步骤
        steps = args.steps or []

        success, result = generator.generate_skill(
            name=args.name,
            pattern_type=args.pattern or "custom",
            description=args.description or "",
            steps=steps,
            triggers=triggers
        )

        if success:
            print(f"[OK] Skill 已生成: {result}")
            print(f"[OK] 目录: {result}")

            # 自动注册触发词
            if triggers:
                registry = TriggerRegistry()
                registry.register(args.name, triggers)
                print(f"[OK] 触发词已注册: {', '.join(triggers)}")
        else:
            print(f"[Error] {result}")
        return

    # 注册触发词
    if args.register:
        if not args.skill or not args.triggers:
            print("[Error] 请提供 --skill 和 --triggers 参数")
            return

        registry = TriggerRegistry()
        triggers = [t.strip() for t in args.triggers.split(",")]
        registry.register(args.skill, triggers)
        print(f"[OK] 触发词已注册 for {args.skill}: {', '.join(triggers)}")
        return

    # 查看统计
    if args.stats:
        detector = PatternDetector()
        generator = SkillGenerator()
        registry = TriggerRegistry()

        complex_patterns = detector.get_complex_patterns()
        skills = generator.list_generated_skills()

        print("## Skill Creator 统计\n")
        print(f"检测到的复杂模式: {len(complex_patterns)}")
        print(f"已生成的 Skills: {len(skills)}")
        print(f"注册的触发词: {len(registry.triggers['triggers'])}")

        if complex_patterns:
            print("\n### 复杂模式 (建议生成 Skill)")
            for p in complex_patterns[:5]:
                print(f"  - {p['type']} ({p['count']}次) -> {p['suggested_name']}")
        return

    # 列出生成的 Skills
    if args.list:
        generator = SkillGenerator()
        skills = generator.list_generated_skills()

        if skills:
            print(f"## 已生成的 Skills ({len(skills)})\n")
            for s in skills:
                print(f"### {s['name']}")
                print(f"  - 路径: {s['path']}")
                print(f"  - 使用次数: {s.get('usage_count', 0)}")
                print(f"  - 触发词: {', '.join(s.get('triggers', []))}")
                print(f"  - 创建时间: {s.get('created_at', 'N/A')}")
                print()
        else:
            print("[Info] 暂无已生成的 Skills")
        return

    # 周期性提醒：检查值得记住的内容
    if args.remind:
        checker = ReminderChecker()
        result = checker.check_forgotten(days=args.days)

        print(f"## 记忆提醒扫描（近 {args.days} 天）\n")
        print(f"找到 {result['total_found']} 条值得记住的内容\n")

        if result["memory_reminders"]:
            print("### 建议写入记忆：\n")
            for i, r in enumerate(result["memory_reminders"], 1):
                print(f"**{i}. [{r['type']}] {r['date']}**")
                print(f"   提醒: {r['reminder']}")
                print(f"   内容: {r['context'][:150]}...")
                print()
        else:
            print("[OK] 近期没有发现特别值得记住的内容")
        return

    # 记录 Skill 执行结果
    if args.record:
        if not args.skill:
            print("[Error] 请提供 --skill 参数")
            return

        improver = SelfImprover()
        improver.record_usage(
            skill_name=args.skill,
            success=args.success,
            feedback=args.feedback or "",
            context=args.context or ""
        )
        print(f"[OK] 已记录执行结果: {args.skill} (success={args.success})")
        return

    # 自我改进
    if args.improve:
        improver = SelfImprover()
        result = improver.improve(skill_name=args.skill, dry_run=args.dry_run)

        print("## 自我改进结果")
        if args.dry_run:
            print(" [预览模式，不实际应用]\n")
        else:
            print()

        if "skills_analyzed" in result:
            print(f"分析了 {result['skills_analyzed']} 个 Skills")
            print(f"需要改进的: {result['needs_improvement']}")
            if "improvements_made" in result:
                print(f"已实际改进: {result['improvements_made']}")

            for detail in result.get("details", []):
                print(f"\n### {detail['skill_name']}")
                print(f"  成功率: {detail['analysis'].get('success_rate', 'N/A')}%")
                if detail['analysis'].get('total_runs'):
                    print(f"  总执行次数: {detail['analysis'].get('total_runs')}")
                if detail['analysis'].get('common_issues'):
                    print(f"  常见问题: {', '.join(detail['analysis'].get('common_issues', []))}")
                for imp in detail.get('improvements_applied', []):
                    print(f"  + {imp}")
        else:
            print(f"分析: {result.get('analysis', {})}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()