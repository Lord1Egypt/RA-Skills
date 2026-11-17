"""Markdown 报告生成器：对齐标准六章模板（见用户定稿周度复盘）。

标准结构（固化底座）：
1. 一页看板（指标表 + 一句话结论 + 可选 PNG 辅助图路径）
2. 分项目分析（主题小节 + 维度表；其他用简表）
3. 问题清单 + 根因三类归因 + 正面范本
4. 本周动作台账（当场已改 / 观察 / 待落实）
5. 待对齐开放会话
6. 自动化概览
7. 事实更正（可选）

图表：定稿以「辅助图表」引用 PNG 为准，不以 Mermaid 为主视觉。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from utils import truncate


class ReportBuilder:
    """从标准 review-input JSON 渲染 Markdown（贴合定稿模板）。"""

    def __init__(self, data: dict[str, Any]):
        self.data = data or {}

    def build(self) -> str:
        period = self.data.get("period") or {}
        start = period.get("start") or "—"
        end = period.get("end") or "—"
        meta = self.data.get("meta") or {}
        source = self.data.get("source") or {}

        title = meta.get("title") or f"{end} 周度复盘（weekly-review skill · 六章结构）"
        source_line = source.get("note") or source.get("label") or "由宿主 Agent 采集并整理"
        methodology = meta.get("methodology") or (
            "本版按 `weekly-review` skill 六章固定结构组织；"
            "归因遵循三类框架（思路/记忆/流程），禁止一刀切「收敛到单一工作区」。"
        )

        lines: list[str] = [
            f"# {title}\n",
            f"> **统计周期**：{start}（周一）～ {end}（周日）",
            f"> **数据来源**：{source_line}",
            f"> **方法论**：{methodology}",
        ]
        if meta.get("version_note"):
            lines.append(f"> **版本说明**：{meta['version_note']}")
        if meta.get("task_split"):
            lines.append(f"> **任务分离**：{meta['task_split']}")
        lines.extend(["", "---", ""])

        lines.extend(self._section_dashboard())
        lines.extend(["---", ""])
        lines.extend(self._section_projects())
        lines.extend(["---", ""])
        lines.extend(self._section_problems())
        lines.extend(["---", ""])
        lines.extend(self._section_action_log())
        lines.extend(["---", ""])
        lines.extend(self._section_open_sessions())
        lines.extend(["---", ""])
        lines.extend(self._section_automations())

        corrections = self.data.get("corrections") or []
        if corrections or self.data.get("corrections_lesson"):
            lines.extend(["---", ""])
            lines.extend(self._section_corrections())

        return "\n".join(lines).rstrip() + "\n"

    def _section_dashboard(self) -> list[str]:
        d = self.data.get("dashboard") or {}
        out = ["## 一、一页看板\n", "| 指标 | 数值 | 口径说明 |", "|---|---|---|"]

        metrics = d.get("metrics")
        if metrics:
            for m in metrics:
                name = m.get("name") or "—"
                value = m.get("value") or "—"
                note = m.get("note") or "—"
                out.append(f"| {name} | {value} | {note} |")
        else:
            # 兼容旧扁平字段
            wall = d.get("wall_clock_hours")
            active = d.get("active_hours")
            credits = d.get("credits")
            tokens = d.get("tokens") or d.get("token_usage")
            sessions = d.get("session_count")
            theme = d.get("main_theme") or "—"
            if wall is not None:
                out.append(
                    f"| 原始 wall-clock 时长 | **≈{wall}h** | {d.get('wall_clock_note') or '—'} |"
                )
            if active is not None:
                out.append(
                    f"| **真实活跃时长** | **≈{active}h** | {d.get('active_note') or '—'} |"
                )
            if tokens is not None:
                out.append(
                    f"| Token 消耗 | **≈{tokens}** | {d.get('tokens_note') or '—'} |"
                )
            elif credits is not None:
                out.append(
                    f"| Credit / 用量 | **≈{credits}** | {d.get('credits_note') or '—'} |"
                )
            if sessions is not None:
                out.append(
                    f"| 会话数 | **{sessions} 个** | {d.get('sessions_note') or '—'} |"
                )
            out.append(f"| 主力主题 | {theme} | {d.get('theme_note') or '—'} |")
            if d.get("major_correction"):
                out.append(
                    f"| **本周重大更正** | {d['major_correction']} | {d.get('major_correction_note') or '—'} |"
                )

        out.append("")
        summary = d.get("summary") or d.get("one_liner")
        if summary:
            out.append(f"**一句话结论**：{summary}")
            out.append("")

        charts = d.get("charts") or []
        if charts:
            out.append("### 辅助图表\n")
            for c in charts:
                path = str(c)
                # 支持 {path, title} 或纯字符串路径
                if isinstance(c, dict):
                    path = str(c.get("path") or c.get("file") or "")
                    title = str(c.get("title") or Path(path).stem)
                else:
                    title = Path(path).stem
                if not path:
                    continue
                out.append(f"![{title}]({path})")
                out.append("")
            # 同时保留路径清单，方便核对文件
            joined = "、".join(
                f"`{c if isinstance(c, str) else c.get('path')}`" for c in charts
            )
            out.append(f"文件：{joined}。")
            out.append("")
        return out

    def _section_projects(self) -> list[str]:
        out = ["## 二、分项目分析\n"]
        projects = self.data.get("projects") or []
        if not projects:
            out.append("本周无分项目数据（由 Agent 按主题聚合后填入）。\n")
            return out

        for i, p in enumerate(projects, 1):
            title = p.get("title") or p.get("name") or f"主题 {i}"
            out.append(f"### 2.{i} {title}\n")
            dims = p.get("dimensions")
            if isinstance(dims, dict) and dims:
                out.append("| 维度 | 内容 |")
                out.append("|---|---|")
                for k, v in dims.items():
                    out.append(f"| **{k}** | {v} |")
                out.append("")
            elif isinstance(dims, list) and dims:
                out.append("| 维度 | 内容 |")
                out.append("|---|---|")
                for row in dims:
                    out.append(
                        f"| **{row.get('name') or row.get('key') or '—'}** | "
                        f"{row.get('value') or row.get('content') or '—'} |"
                    )
                out.append("")
            else:
                # 兼容旧扁平项目
                hours = p.get("hours")
                sessions = p.get("sessions")
                notes = p.get("notes") or "—"
                bits = []
                if hours is not None:
                    bits.append(f"时长 ≈{hours}h")
                if sessions is not None:
                    bits.append(f"会话 {sessions}")
                out.append("| 维度 | 内容 |")
                out.append("|---|---|")
                out.append(f"| **概要** | {'；'.join(bits) if bits else '—'} |")
                out.append(f"| **备注** | {notes} |")
                out.append("")

        other = self.data.get("other_projects") or []
        if other:
            n = len(projects) + 1
            out.append(f"### 2.{n} 其他\n")
            out.append("| 项目 | 时长 | 评价 |")
            out.append("|---|---|---|")
            for o in other:
                out.append(
                    f"| {o.get('name') or '—'} | {o.get('hours') or o.get('duration') or '—'} "
                    f"| {o.get('note') or o.get('评价') or '—'} |"
                )
            out.append("")
        return out

    def _section_problems(self) -> list[str]:
        problems = self.data.get("problems") or []
        out = [
            "## 三、问题清单 + 根因三类归因\n",
            (
                "> 归因三类框架：**① 思路问题**（边做边开新目录没规划）；"
                "**② 记忆问题**（忘了之前做过）；"
                "**③ 流程问题**（合理分工但缺索引）。"
                "三者对应完全不同的建议，禁止一刀切「收敛到单一工作区」。\n"
            ),
            "| # | 问题 | 归因类别 | 根因 | 建议 |",
            "|---|---|---|---|---|",
        ]
        if not problems:
            out.append("| — | 暂无人工标注问题 | — | — | 请在对话中补充 |")
        for i, p in enumerate(problems, 1):
            out.append(
                f"| {i} | {p.get('description', '—')} | {p.get('category', '—')} "
                f"| {p.get('root_cause', '—')} | {p.get('suggestion', '—')} |"
            )
        out.append("")

        goods = self.data.get("positives") or self.data.get("good_examples") or []
        if goods:
            out.append("**做得好的（正面范本）**：")
            for g in goods:
                out.append(f"- {g}")
            out.append("")
        return out

    def _section_action_log(self) -> list[str]:
        actions = self.data.get("actions") or {}
        out = ["## 四、本周动作台账 ★\n"]

        out.append("### 4.1 当场已改\n")
        done = actions.get("done") or []
        if not done:
            out.append("暂无。\n")
        else:
            out.append("| # | 动作 | 触发来源 | 改了什么 |")
            out.append("|---|---|---|---|")
            for i, a in enumerate(done, 1):
                out.append(
                    f"| A{i} | {a.get('action', '—')} | {a.get('trigger', '—')} "
                    f"| {a.get('change', '—')} |"
                )
            out.append("")

        out.append("### 4.2 已改、需后续观察效果\n")
        observing = actions.get("observing") or []
        if not observing:
            out.append("暂无。\n")
        else:
            out.append("| # | 动作 | 怎么判断\"见效了\" |")
            out.append("|---|---|---|")
            for i, a in enumerate(observing, 1):
                out.append(
                    f"| O{i} | {a.get('action', '—')} | {a.get('criteria', '—')} |"
                )
            out.append("")

        pending = actions.get("pending") or []
        # 若 pending 条目带 result，用「执行结果」表头
        has_result = any(p.get("result") for p in pending)
        if has_result:
            out.append("### 4.3 待落实 → 执行结果\n")
            out.append("| # | 原建议 | 结果 | 状态 |")
            out.append("|---|---|---|---|")
            for i, a in enumerate(pending, 1):
                out.append(
                    f"| P{i} | {a.get('suggestion') or a.get('action') or '—'} "
                    f"| {a.get('result', '—')} | **{a.get('status', '待开始')}** |"
                )
        else:
            out.append("### 4.3 待落实\n")
            if not pending:
                out.append("暂无。\n")
            else:
                out.append("| # | 建议 | 优先级 | 截止 | 状态 |")
                out.append("|---|---|---|---|---|")
                for i, a in enumerate(pending, 1):
                    out.append(
                        f"| P{i} | {a.get('suggestion', '—')} | {a.get('priority', '—')} "
                        f"| {a.get('deadline', '—')} | {a.get('status', '待开始')} |"
                    )
        out.append("")
        return out

    def _section_open_sessions(self) -> list[str]:
        out = ["## 五、待对齐开放会话\n"]
        sessions = self.data.get("open_sessions") or []
        out.append("| 会话（标题前30字 + 时间 + 目录） | 跨度 | 处置结果 | 后续 |")
        out.append("|---|---|---|---|")
        if not sessions:
            out.append("| — | — | 本周无跨周/跨夜 idle 会话 | — |")
        for s in sessions:
            title = truncate(str(s.get("title") or "未命名"), 30)
            created = s.get("created") or "—"
            cwd = s.get("cwd_tail") or s.get("cwd") or "—"
            label = s.get("label") or f"「{title}」（{created}, {cwd}）"
            span = s.get("span") or (
                f"{created}→{s.get('last_active')}" if s.get("last_active") else "—"
            )
            decision = s.get("decision") or "待拍板"
            follow = s.get("follow_up") or "关闭/迁移/继续"
            out.append(f"| {label} | {span} | {decision} | {follow} |")
        out.append("")
        out.append(
            "> 机制：每周复盘交付时列出跨周(>48h)/跨夜 idle 会话，当场拍板，不留悬空。\n"
        )
        return out

    def _section_automations(self) -> list[str]:
        out = ["## 六、自动化概览\n"]
        auto = self.data.get("automations") or {}
        narrative = auto.get("narrative") or auto.get("summary")
        if narrative:
            if isinstance(narrative, list):
                for line in narrative:
                    out.append(f"- {line}")
            else:
                out.append(str(narrative))
            out.append("")
            return out

        items = auto.get("items") or []
        total = auto.get("runs_total")
        success = auto.get("runs_success")
        if total is not None:
            fail = max(int(total) - int(success or 0), 0)
            out.append(
                f"- 本周自动化运行 **{total}** 次，成功 **{success or 0}** 次，"
                f"失败/未知 **{fail}** 次。"
            )
        if items:
            for r in items:
                title = r.get("title") or "未命名"
                status = r.get("status") or "—"
                result = r.get("result") or "—"
                detail = r.get("detail") or ""
                line = f"- **{title}**：状态 `{status}`，结果 {result}"
                if detail:
                    line += f"。{detail}"
                out.append(line)
        if not narrative and total is None and not items:
            out.append("本周无自动化运行记录（或本平台无此概念）。")
        out.append("")
        return out

    def _section_corrections(self) -> list[str]:
        out = [
            "## 七、事实更正（最重要的一课）\n",
        ]
        lesson = self.data.get("corrections_lesson")
        if lesson:
            out.append(f"> {lesson}\n")
        rows = self.data.get("corrections") or []
        if rows:
            out.append("| 原报告结论 | 声称的目录/事实 | 核对结果 |")
            out.append("|---|---|---|")
            for r in rows:
                out.append(
                    f"| {r.get('was') or r.get('original') or '—'} "
                    f"| {r.get('claimed') or '—'} "
                    f"| {r.get('actual') or r.get('verified') or '—'} |"
                )
            out.append("")
        takeaway = self.data.get("corrections_takeaway")
        if takeaway:
            out.append(f"**教训**：{takeaway}\n")
        return out
