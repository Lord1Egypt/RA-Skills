#!/usr/bin/env python3
"""
OpenClaw Session Token Monitor
分析会话 JSONL 文件，追踪各 skill 的 token 消耗（输入/输出/缓存命中）和成功率
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


def parse_args():
    parser = argparse.ArgumentParser(
        description="分析 OpenClaw 会话文件的 token 使用和性能"
    )
    parser.add_argument(
        "--session-file",
        type=str,
        help="指定要分析的会话 JSONL 文件路径",
    )
    parser.add_argument(
        "--project-dir",
        type=str,
        help="包含会话文件的项目目录路径",
    )
    parser.add_argument(
        "--skill",
        type=str,
        help="按特定 skill 名称筛选",
    )
    parser.add_argument(
        "--format",
        choices=["json", "markdown", "html"],
        default="markdown",
        help="输出格式",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="输出文件路径（默认：标准输出）",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="只分析最近 N 天的会话",
    )
    return parser.parse_args()


class SessionAnalyzer:
    """分析 OpenClaw 会话 JSONL 文件"""

    def __init__(self):
        self.sessions: List[Dict] = []
        self.skills_data: Dict[str, Dict] = defaultdict(
            lambda: {
                "调用次数": 0,
                "总tokens": 0,
                "输入tokens": 0,
                "输出tokens": 0,
                "缓存读取tokens": 0,
                "缓存写入tokens": 0,
                "成功次数": 0,
                "失败次数": 0,
                "延迟列表": [],
                "工具调用": defaultdict(int),
            }
        )
        self.global_stats = {
            "总会话数": 0,
            "总消息数": 0,
            "用户消息数": 0,
            "助手消息数": 0,
            "总工具调用数": 0,
            "总输入tokens": 0,
            "总输出tokens": 0,
            "总缓存读取tokens": 0,
            "总缓存写入tokens": 0,
            "总tokens": 0,
            "总错误数": 0,
        }
        # 动态加载已知的 skill 列表
        self.VALID_SKILLS = self._load_known_skills()
        # 明确不是 skill 的模式
        self.NON_SKILL_PATTERNS = {
            # 日期格式
            'yyyy-mm-dd', '2025-01-15', '2024-', '2023-', '2026-',
            # 纯数字
            '100k', '200k', '38', '127', '15', '5',
            # URL/路径相关
            'api', 'users', 'repos', 'github', 'issues', 'labels', 'pull',
            'u', 'avatars', 'events', 'subscriptions', 'starred', 'repo',
            'received_events', 'privacy', 'owner', 'other_user', 'orgs',
            'gists', 'gist_id', 'following', 'followers', 'status',
            'reactions', 'comments', 'mengqingyu04',
            # 通用单词（单个词，不是 skill）
            'home', 'infra', 'types', 'compact', 'assistant', 'agent', 'tool',
            'config', 'output', 'input', 'code', 'test', 'install', 'text',
            'write', 'read', 'new', 'end', 'main', 'src', 'stderr', 'different',
            'internal', 'capture', 'workspace', 'embedded', 'pr', 'sessions',
            'skill', 'rules', 'event', 'tools', 'commands', 'registry',
            'after_tool_call', 'session_jsonl_compaction_report',
            'flow-monitor-logs', 'claude-agent-acp', 'localhost', 'auth-profiles',
            'configuration', 'skills', 'skillhub', 'ws', 'o', 'compact', 'cmd',
            'applications', 'qianfan-code-latest', 'unknown', 'index',
            'liquidity', 'common', 'openclaw',
            # 系统组件/内部模块（不是用户使用的 skill）
            'service', 'hooks', 'agents', 'session-store', 'session-write-lock',
            'install-flow', 'token-optimization-verification', 'commands-system-prompt',
            'flow-monitor-test-record', 'openclaw-token-monitor-2026', 'agent-monitor-v2',
            'diagnostic-events', 'session-pruning', 'multi-agent', 'load-path',
            'token-monitor-2026', 'flow-monitor-plugin', 'flow-monitor-测试结果',
            'flow-monitor-v2',
        }

    def _load_known_skills(self) -> set:
        """从 ~/.claude/skills/ 目录加载已知的 skill 名称"""
        known_skills = set()
        skills_dir = Path.home() / ".claude" / "skills"
        if skills_dir.exists():
            for item in skills_dir.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    known_skills.add(item.name.lower())
        # 添加一些可能存在的但未安装的 skill
        known_skills.update({
            'flow-monitor', 'token-usage', 'acpx', 'extensions', 'concepts',
            'hooks', 'agents', 'service', 'sandbox-setup', 'whatsapp',
            'pi-coding-agent', 'auto-reply', 'oxlint', 'plugin-sdk',
        })
        return known_skills

    def load_session_file(self, filepath: str) -> List[Dict]:
        """加载并解析 JSONL 会话文件"""
        entries = []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                        entries.append(entry)
                    except json.JSONDecodeError:
                        print(f"警告: {filepath}:{line_num} 处 JSON 格式无效", file=sys.stderr)
                        continue
        except FileNotFoundError:
            print(f"错误: 文件未找到: {filepath}", file=sys.stderr)
            return []
        except Exception as e:
            print(f"错误读取 {filepath}: {e}", file=sys.stderr)
            return []
        return entries

    def is_valid_skill_name(self, name: str) -> bool:
        """验证是否为有效的 skill 名称"""
        if not name or len(name) < 3:
            return False
        name = name.lower()
        # 如果在白名单中，直接通过
        if name in self.VALID_SKILLS:
            return True
        # 如果在黑名单中，直接拒绝
        if name in self.NON_SKILL_PATTERNS:
            return False
        # 必须是连字符或下划线连接的格式（避免单个单词）
        if '-' not in name and '_' not in name:
            return False
        # 检查是否包含数字开头（如 127, 15 等）
        if name[0].isdigit():
            return False
        return True

    def extract_skill_name(self, entry: Dict) -> Optional[str]:
        """从会话条目中提取 skill 名称"""
        message = entry.get("message", {})
        content = message.get("content", [])

        # 收集文本内容
        text_content = ""
        if isinstance(content, str):
            text_content = content
        elif isinstance(content, list):
            for block in content:
                if isinstance(block, dict):
                    if block.get("type") == "text":
                        text_content += block.get("text", "") + " "
                    elif block.get("type") == "thinking":
                        text_content += block.get("thinking", "") + " "

        import re

        # 方法1: 查找 /skill-name 模式（必须是独立的 skill 调用）
        # 匹配 /skill-name，但后面要有空格或结束符，避免匹配 URL
        skill_pattern = r'/(\w[\w-]+)(?:\s|$|\n|\.|\?|!|:)'
        matches = re.findall(skill_pattern, text_content)
        for match in matches:
            skill_name = match.lower().strip()
            if self.is_valid_skill_name(skill_name):
                return skill_name

        # 方法2: 从 tool_calls 中提取 Skill 调用
        tool_calls = message.get("tool_calls", []) or message.get("toolCalls", [])
        for call in tool_calls:
            if isinstance(call, dict):
                name = call.get("name") or call.get("function", {}).get("name")
                if name == "Skill" or name == "skill":
                    # 从参数中提取 skill 名称
                    args = call.get("arguments") or call.get("input", {})
                    if isinstance(args, str):
                        try:
                            args = json.loads(args)
                        except:
                            args = {}
                    skill_name = args.get("skill") or args.get("name")
                    if skill_name and self.is_valid_skill_name(skill_name):
                        return skill_name.lower()

        # 方法3: 查找 "use skill" 或 "using skill" 模式
        use_skill_pattern = r'(?:use|using)\s+["\']?([\w-]+)["\']?\s+skill'
        match = re.search(use_skill_pattern, text_content, re.IGNORECASE)
        if match:
            skill_name = match.group(1).lower()
            if self.is_valid_skill_name(skill_name):
                return skill_name

        # 方法4: 从 skill 命令参数中提取
        skill_cmd_pattern = r'skill[:\s]+["\']?([\w-]+)["\']?'
        match = re.search(skill_cmd_pattern, text_content, re.IGNORECASE)
        if match:
            skill_name = match.group(1).lower()
            if self.is_valid_skill_name(skill_name):
                return skill_name

        return None

    def extract_usage(self, entry: Dict) -> Optional[Dict[str, int]]:
        """从条目中提取 token 使用情况"""
        message = entry.get("message", {})
        usage = message.get("usage", {})

        if not usage:
            return None

        return {
            "输入": usage.get("input_tokens", 0) or usage.get("input", 0),
            "输出": usage.get("output_tokens", 0) or usage.get("output", 0),
            "缓存读取": usage.get("cache_read_input_tokens", 0) or usage.get("cacheRead", 0),
            "缓存写入": usage.get("cache_creation_input_tokens", 0) or usage.get("cacheWrite", 0),
        }

    def is_success(self, entry: Dict) -> bool:
        """判断条目是否代表成功操作"""
        message = entry.get("message", {})

        # 检查 stop reason
        stop_reason = message.get("stop_reason")
        if stop_reason in ["error", "aborted", "timeout"]:
            return False

        # 检查内容中的错误
        content = message.get("content", [])
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict):
                    text = block.get("text", "").lower()
                    if "error" in text and "sorry" in text:
                        return False

        return True

    def extract_latency(self, entry: Dict) -> Optional[float]:
        """提取延迟（毫秒），如果可用"""
        message = entry.get("message", {})
        duration_ms = message.get("durationMs")
        if duration_ms:
            return float(duration_ms)
        return None

    def analyze_entry(self, entry: Dict):
        """分析单个会话条目"""
        message = entry.get("message", {})
        role = message.get("role")

        if role == "user":
            self.global_stats["用户消息数"] += 1
        elif role == "assistant":
            self.global_stats["助手消息数"] += 1

        self.global_stats["总消息数"] += 1

        # 提取 skill 名称
        skill_name = self.extract_skill_name(entry) or "unknown"

        # 提取使用情况
        usage = self.extract_usage(entry)
        if usage:
            total_tokens = usage["输入"] + usage["输出"] + usage["缓存读取"] + usage["缓存写入"]

            self.skills_data[skill_name]["调用次数"] += 1
            self.skills_data[skill_name]["输入tokens"] += usage["输入"]
            self.skills_data[skill_name]["输出tokens"] += usage["输出"]
            self.skills_data[skill_name]["缓存读取tokens"] += usage["缓存读取"]
            self.skills_data[skill_name]["缓存写入tokens"] += usage["缓存写入"]
            self.skills_data[skill_name]["总tokens"] += total_tokens

            # 更新全局统计
            self.global_stats["总输入tokens"] += usage["输入"]
            self.global_stats["总输出tokens"] += usage["输出"]
            self.global_stats["总缓存读取tokens"] += usage["缓存读取"]
            self.global_stats["总缓存写入tokens"] += usage["缓存写入"]
            self.global_stats["总tokens"] += total_tokens

            # 追踪成功/失败
            if self.is_success(entry):
                self.skills_data[skill_name]["成功次数"] += 1
            else:
                self.skills_data[skill_name]["失败次数"] += 1
                self.global_stats["总错误数"] += 1

            # 追踪延迟
            latency = self.extract_latency(entry)
            if latency:
                self.skills_data[skill_name]["延迟列表"].append(latency)

        # 统计工具调用
        tool_calls = message.get("tool_calls", []) or message.get("toolCalls", [])
        if tool_calls:
            self.global_stats["总工具调用数"] += len(tool_calls)
            for call in tool_calls:
                if isinstance(call, dict):
                    name = call.get("name") or call.get("function", {}).get("name", "unknown")
                    self.skills_data[skill_name]["工具调用"][name] += 1

    def analyze_session(self, entries: List[Dict]):
        """分析会话中的所有条目"""
        self.global_stats["总会话数"] += 1

        for entry in entries:
            self.analyze_entry(entry)

    def get_results(self) -> Dict:
        """获取分析结果"""
        results = {
            "汇总": self.global_stats,
            "skills": {},
        }

        for skill_name, data in self.skills_data.items():
            total_calls = data["成功次数"] + data["失败次数"]
            success_rate = data["成功次数"] / total_calls if total_calls > 0 else 0

            avg_latency = 0
            if data["延迟列表"]:
                avg_latency = sum(data["延迟列表"]) / len(data["延迟列表"])

            # 计算缓存命中率
            total_input = data["输入tokens"] + data["缓存读取tokens"]
            cache_hit_rate = data["缓存读取tokens"] / total_input if total_input > 0 else 0

            results["skills"][skill_name] = {
                "调用次数": data["调用次数"],
                "总tokens": data["总tokens"],
                "输入tokens": data["输入tokens"],
                "输出tokens": data["输出tokens"],
                "缓存读取tokens": data["缓存读取tokens"],
                "缓存写入tokens": data["缓存写入tokens"],
                "缓存命中率": round(cache_hit_rate * 100, 1),
                "成功率": round(success_rate * 100, 1),
                "成功次数": data["成功次数"],
                "失败次数": data["失败次数"],
                "平均延迟ms": round(avg_latency, 2),
                "工具调用": dict(data["工具调用"]),
            }

        # 按总 tokens 排序（降序）
        results["skills"] = dict(sorted(
            results["skills"].items(),
            key=lambda x: x[1]["总tokens"],
            reverse=True
        ))

        return results

    def to_markdown(self, results: Dict) -> str:
        """将结果转换为 Markdown 格式"""
        lines = []
        lines.append("# OpenClaw Token 使用报告")
        lines.append(f"\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("\n---\n")

        # 汇总
        summary = results["汇总"]
        lines.append("## 📊 汇总统计\n")
        lines.append(f"| 指标 | 数值 |")
        lines.append(f"|------|------|")
        lines.append(f"| 总会话数 | {summary['总会话数']} |")
        lines.append(f"| 总消息数 | {summary['总消息数']:,} |")
        lines.append(f"| 用户消息数 | {summary['用户消息数']:,} |")
        lines.append(f"| 助手消息数 | {summary['助手消息数']:,} |")
        lines.append(f"| 总工具调用数 | {summary['总工具调用数']:,} |")
        lines.append(f"| 总错误数 | {summary['总错误数']} |")
        lines.append(f"| **总输入 tokens** | **{summary['总输入tokens']:,}** |")
        lines.append(f"| **总输出 tokens** | **{summary['总输出tokens']:,}** |")
        lines.append(f"| **总缓存读取 tokens** | **{summary['总缓存读取tokens']:,}** |")
        lines.append(f"| **总缓存写入 tokens** | **{summary['总缓存写入tokens']:,}** |")
        lines.append(f"| **总 tokens** | **{summary['总tokens']:,}** |")

        # Token 分布饼图数据
        lines.append("\n## 📈 Token 分布\n")
        total = summary['总tokens']
        if total > 0:
            lines.append(f"- **输入**: {summary['总输入tokens']:,} ({summary['总输入tokens']/total*100:.1f}%)")
            lines.append(f"- **输出**: {summary['总输出tokens']:,} ({summary['总输出tokens']/total*100:.1f}%)")
            lines.append(f"- **缓存读取**: {summary['总缓存读取tokens']:,} ({summary['总缓存读取tokens']/total*100:.1f}%)")
            lines.append(f"- **缓存写入**: {summary['总缓存写入tokens']:,} ({summary['总缓存写入tokens']/total*100:.1f}%)")

        # Skills 明细
        lines.append("\n## 🔍 Skill 明细\n")
        lines.append("| Skill | 调用次数 | 输入 | 输出 | 缓存读取 | 总tokens | 缓存命中率 | 成功率 |")
        lines.append("|-------|----------|------|------|----------|----------|------------|--------|")

        for skill_name, data in results["skills"].items():
            lines.append(
                f"| {skill_name} | {data['调用次数']:,} | "
                f"{data['输入tokens']:,} | {data['输出tokens']:,} | "
                f"{data['缓存读取tokens']:,} | {data['总tokens']:,} | "
                f"{data['缓存命中率']:.1f}% | {data['成功率']:.0f}% |"
            )

        # 详细分析
        lines.append("\n## 📋 详细分析\n")
        for skill_name, data in results["skills"].items():
            lines.append(f"\n### {skill_name}\n")
            lines.append(f"- **调用次数**: {data['调用次数']:,}")
            lines.append(f"- **Token 明细**:")
            lines.append(f"  - 输入: {data['输入tokens']:,}")
            lines.append(f"  - 输出: {data['输出tokens']:,}")
            lines.append(f"  - 缓存读取: {data['缓存读取tokens']:,}")
            lines.append(f"  - 缓存写入: {data['缓存写入tokens']:,}")
            lines.append(f"  - **总计**: {data['总tokens']:,}")
            lines.append(f"- **缓存命中率**: {data['缓存命中率']:.1f}%")
            lines.append(f"- **成功率**: {data['成功率']:.1f}% ({data['成功次数']:,}/{data['成功次数'] + data['失败次数']:,})")
            lines.append(f"- **平均延迟**: {data['平均延迟ms']:.0f}ms")

            if data["工具调用"]:
                lines.append(f"- **工具调用**:")
                for tool, count in data["工具调用"].items():
                    lines.append(f"  - {tool}: {count:,}")

        return "\n".join(lines)

    def to_html(self, results: Dict) -> str:
        """将结果转换为 HTML 格式"""
        summary = results["汇总"]

        # 计算百分比
        total = summary['总tokens']
        input_pct = summary['总输入tokens']/total*100 if total > 0 else 0
        output_pct = summary['总输出tokens']/total*100 if total > 0 else 0
        cache_read_pct = summary['总缓存读取tokens']/total*100 if total > 0 else 0
        cache_write_pct = summary['总缓存写入tokens']/total*100 if total > 0 else 0

        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>OpenClaw Token 使用报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Microsoft YaHei', sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 1400px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 2px solid #e91e63; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        h3 {{ color: #666; }}
        .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .metric-card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #e91e63; }}
        .metric-value {{ font-size: 2em; font-weight: bold; color: #e91e63; }}
        .metric-label {{ color: #666; font-size: 0.9em; }}
        .token-bar {{ display: flex; height: 30px; border-radius: 4px; overflow: hidden; margin: 20px 0; }}
        .token-input {{ background: #4caf50; }}
        .token-output {{ background: #2196f3; }}
        .token-cache-read {{ background: #ff9800; }}
        .token-cache-write {{ background: #9c27b0; }}
        .legend {{ display: flex; gap: 20px; margin: 10px 0; flex-wrap: wrap; }}
        .legend-item {{ display: flex; align-items: center; gap: 5px; }}
        .legend-color {{ width: 16px; height: 16px; border-radius: 3px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 0.9em; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #f8f9fa; font-weight: 600; color: #333; }}
        tr:hover {{ background: #f5f5f5; }}
        .success-rate {{ font-weight: bold; }}
        .success-rate.high {{ color: #4caf50; }}
        .success-rate.medium {{ color: #ff9800; }}
        .success-rate.low {{ color: #f44336; }}
        .skill-detail {{ background: #f8f9fa; padding: 20px; margin: 10px 0; border-radius: 8px; }}
        .timestamp {{ color: #999; font-size: 0.9em; }}
        .token-detail {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin: 10px 0; }}
        .token-item {{ background: white; padding: 10px; border-radius: 4px; border: 1px solid #e0e0e0; }}
        .token-label {{ font-size: 0.8em; color: #666; }}
        .token-value {{ font-size: 1.2em; font-weight: bold; color: #333; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 OpenClaw Token 使用报告</h1>
        <p class="timestamp">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

        <h2>📈 汇总统计</h2>
        <div class="summary-grid">
            <div class="metric-card">
                <div class="metric-value">{summary['总会话数']}</div>
                <div class="metric-label">总会话数</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{summary['总消息数']:,}</div>
                <div class="metric-label">总消息数</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{summary['总tokens']:,}</div>
                <div class="metric-label">总 Tokens</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{summary['总错误数']}</div>
                <div class="metric-label">错误数</div>
            </div>
        </div>

        <h3>Token 分布</h3>
        <div class="token-bar">
            <div class="token-input" style="width: {input_pct:.1f}%" title="输入: {summary['总输入tokens']:,}"></div>
            <div class="token-output" style="width: {output_pct:.1f}%" title="输出: {summary['总输出tokens']:,}"></div>
            <div class="token-cache-read" style="width: {cache_read_pct:.1f}%" title="缓存读取: {summary['总缓存读取tokens']:,}"></div>
            <div class="token-cache-write" style="width: {cache_write_pct:.1f}%" title="缓存写入: {summary['总缓存写入tokens']:,}"></div>
        </div>
        <div class="legend">
            <div class="legend-item">
                <div class="legend-color" style="background: #4caf50;"></div>
                <span>输入: {summary['总输入tokens']:,} ({input_pct:.1f}%)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #2196f3;"></div>
                <span>输出: {summary['总输出tokens']:,} ({output_pct:.1f}%)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #ff9800;"></div>
                <span>缓存读取: {summary['总缓存读取tokens']:,} ({cache_read_pct:.1f}%)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #9c27b0;"></div>
                <span>缓存写入: {summary['总缓存写入tokens']:,} ({cache_write_pct:.1f}%)</span>
            </div>
        </div>

        <h2>🔍 Skill 明细</h2>
        <table>
            <thead>
                <tr>
                    <th>Skill</th>
                    <th>调用次数</th>
                    <th>输入</th>
                    <th>输出</th>
                    <th>缓存读取</th>
                    <th>总tokens</th>
                    <th>缓存命中率</th>
                    <th>成功率</th>
                </tr>
            </thead>
            <tbody>
"""

        for skill_name, data in results["skills"].items():
            rate_class = 'high' if data['成功率'] >= 90 else 'medium' if data['成功率'] >= 70 else 'low'

            html += f"""
                <tr>
                    <td><strong>{skill_name}</strong></td>
                    <td>{data['调用次数']:,}</td>
                    <td>{data['输入tokens']:,}</td>
                    <td>{data['输出tokens']:,}</td>
                    <td>{data['缓存读取tokens']:,}</td>
                    <td><strong>{data['总tokens']:,}</strong></td>
                    <td>{data['缓存命中率']:.1f}%</td>
                    <td class="success-rate {rate_class}">{data['成功率']:.0f}%</td>
                </tr>
"""

        html += """
            </tbody>
        </table>

        <h2>📋 详细分析</h2>
"""

        for skill_name, data in results["skills"].items():
            html += f"""
        <div class="skill-detail">
            <h3>{skill_name}</h3>
            <div class="token-detail">
                <div class="token-item">
                    <div class="token-label">调用次数</div>
                    <div class="token-value">{data['调用次数']:,}</div>
                </div>
                <div class="token-item">
                    <div class="token-label">输入 tokens</div>
                    <div class="token-value">{data['输入tokens']:,}</div>
                </div>
                <div class="token-item">
                    <div class="token-label">输出 tokens</div>
                    <div class="token-value">{data['输出tokens']:,}</div>
                </div>
                <div class="token-item">
                    <div class="token-label">缓存读取</div>
                    <div class="token-value">{data['缓存读取tokens']:,}</div>
                </div>
                <div class="token-item">
                    <div class="token-label">缓存写入</div>
                    <div class="token-value">{data['缓存写入tokens']:,}</div>
                </div>
                <div class="token-item">
                    <div class="token-label">总 tokens</div>
                    <div class="token-value" style="color: #e91e63;">{data['总tokens']:,}</div>
                </div>
                <div class="token-item">
                    <div class="token-label">缓存命中率</div>
                    <div class="token-value">{data['缓存命中率']:.1f}%</div>
                </div>
                <div class="token-item">
                    <div class="token-label">成功率</div>
                    <div class="token-value">{data['成功率']:.0f}%</div>
                </div>
            </div>
        </div>
"""

        html += """
    </div>
</body>
</html>
"""
        return html


def find_session_files(project_dir: str, days: int = 30) -> List[str]:
    """在项目目录中查找所有会话 JSONL 文件"""
    session_files = []
    cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)

    project_path = Path(project_dir)
    if not project_path.exists():
        return []

    for jsonl_file in project_path.glob("*.jsonl"):
        try:
            stat = jsonl_file.stat()
            if stat.st_mtime >= cutoff_time:
                session_files.append(str(jsonl_file))
        except Exception:
            continue

    return session_files


def main():
    args = parse_args()

    if not args.session_file and not args.project_dir:
        print("错误: 必须指定 --session-file 或 --project-dir", file=sys.stderr)
        sys.exit(1)

    analyzer = SessionAnalyzer()

    # 收集会话文件
    session_files = []
    if args.session_file:
        session_files.append(args.session_file)
    else:
        session_files = find_session_files(args.project_dir, args.days)
        print(f"在 {args.project_dir} 中找到 {len(session_files)} 个会话文件", file=sys.stderr)

    # 分析每个会话
    for filepath in session_files:
        entries = analyzer.load_session_file(filepath)
        if entries:
            analyzer.analyze_session(entries)
            print(f"已分析: {filepath} ({len(entries)} 条记录)", file=sys.stderr)

    # 获取结果
    results = analyzer.get_results()

    # 按 skill 筛选（如果指定）
    if args.skill:
        results["skills"] = {
            k: v for k, v in results["skills"].items()
            if args.skill.lower() in k.lower()
        }

    # 输出
    if args.format == "json":
        output = json.dumps(results, indent=2, ensure_ascii=False)
    elif args.format == "html":
        output = analyzer.to_html(results)
    else:
        output = analyzer.to_markdown(results)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"报告已保存至: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
