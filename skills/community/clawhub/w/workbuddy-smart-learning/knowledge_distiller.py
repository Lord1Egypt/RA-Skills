"""
WorkBuddy 智能学习系统 - 知识蒸馏模块
功能：将成功案例提炼为可复用模板；将失败案例沉淀为避坑规则
增强：自适应阈值 + 模板关键词匹配 + 避坑规则
"""

import json
import os
import re
import yaml
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Optional

# 自适应阈值基础值
BASE_AUTO_DISTILL_THRESHOLD = 5  # 正面反馈达到此数量则自动触发蒸馏


def _compute_adaptive_threshold(feedback_rate: float, base: int = BASE_AUTO_DISTILL_THRESHOLD) -> int:
    """
    根据反馈填写率计算自适应蒸馏阈值
    填写率高 → 低阈值（用户积极参与，可频繁蒸馏）
    填写率低 → 高阈值（避免基于少量数据误触发）
    """
    if feedback_rate <= 0:
        return base * 3
    effective_rate = max(feedback_rate, 0.05)
    adaptive = int(base / effective_rate)
    return max(adaptive, base)


class KnowledgeDistiller:
    """知识蒸馏器 - 将案例转化为模板"""

    def __init__(self, workspace_root: str):
        self.workspace = Path(workspace_root)
        self.templates_dir = self.workspace / ".workbuddy" / "memory" / "templates"
        self.avoid_dir = self.templates_dir / "failed_patterns"
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.avoid_dir.mkdir(parents=True, exist_ok=True)

    # ─── 核心蒸馏 ──────────────────────────────────────────

    def distill_from_feedback(self, good_feedbacks: list[dict]) -> list[dict]:
        """从正面反馈中提炼成功要素"""
        patterns = {"success_tags": [], "common_actions": [], "preferred_formats": []}

        for fb in good_feedbacks:
            patterns["success_tags"].extend(fb.get("tags", []))
            patterns["common_actions"].append(fb.get("task_id", ""))

        tag_freq = Counter(patterns["success_tags"])

        distilled = {
            "timestamp": datetime.now().isoformat(),
            "source": "feedback_analysis",
            "success_factors": [
                {"tag": tag, "frequency": count}
                for tag, count in tag_freq.most_common(10)
            ],
            "recommendations": self._generate_recommendations(tag_freq)
        }

        return distilled

    def distill_from_memory(self, memory_content: str, task_context: str) -> dict:
        """从记忆片段中提炼模板结构"""
        steps_pattern = r'步骤?\s*(\d+)[：:]\s*([^\n]+)'
        steps = re.findall(steps_pattern, memory_content)
        keywords = self._extract_keywords(task_context)

        template = {
            "template": {
                "name": f"自动生成模板 - {keywords[0] if keywords else '通用'}",
                "version": "1.0.0",
                "author": "auto-distilled",
                "created": datetime.now().isoformat(),
                "trigger": {"keywords": keywords, "confidence": 0.7},
                "process": {
                    "steps": [
                        {"id": int(s[0]), "action": s[1].strip()}
                        for s in steps
                    ] if steps else []
                },
                "metadata": {"source": "memory_distillation", "original_length": len(memory_content)}
            }
        }

        return template

    def distill_from_failed_feedback(self, failed_feedbacks: list[dict]) -> list[Path]:
        """
        从负面反馈中提炼避坑规则
        每个失败案例生成一条 avoid_*.yaml 规则
        """
        saved = []

        for fb in failed_feedbacks:
            tags = fb.get("tags", [])
            note = fb.get("note", "")
            task_id = fb.get("task_id", "unknown")
            timestamp = datetime.now().isoformat()

            # 构建避坑规则
            avoid_rule = {
                "type": "avoid_rule",
                "version": "1.0.0",
                "created": timestamp,
                "source_task": task_id,
                "triggers": {
                    "keywords": self._extract_keywords(note or task_id),
                    "tags": [t for t in tags if t not in ("good", "bad", "neutral")]
                },
                "problem": note or "执行结果未达预期",
                "avoid_actions": self._infer_avoid_actions(note),
                "suggested_fix": self._infer_fix(note)
            }

            safe_name = re.sub(r'[^\w\s-]', '', (note or task_id)[:40]).strip()
            safe_name = re.sub(r'\s+', '_', safe_name) or "unknown"
            filename = f"avoid_{safe_name}.yaml"
            out_file = self.avoid_dir / filename

            with open(out_file, "w", encoding="utf-8") as f:
                yaml.dump(avoid_rule, f, allow_unicode=True, default_flow_style=False)

            saved.append(out_file)

        return saved

    def _infer_avoid_actions(self, note: str) -> list[str]:
        """从备注中推断应避免的操作"""
        if not note:
            return []
        actions = []
        if any(w in note for w in ["跳过", "忽略", "遗漏"]):
            actions.append("不要跳过关键步骤")
        if any(w in note for w in ["顺序", "颠倒", "混乱"]):
            actions.append("保持正确的操作顺序")
        if any(w in note for w in ["格式", "输出"]):
            actions.append("注意输出格式和格式规范")
        return actions if actions else ["执行过程中出现问题，请参考上次失败备注"]

    def _infer_fix(self, note: str) -> str:
        """从备注推断修复建议"""
        if not note:
            return "建议重新执行并关注上次的不足之处"
        return f"参考上次备注修正：{note[:80]}"

    # ─── 自适应蒸馏触发 ────────────────────────────────────

    def check_and_auto_distill(
        self,
        good_feedbacks: list[dict],
        feedback_rate: float = 0.0
    ) -> dict:
        """
        检查是否满足自动蒸馏条件
        正面反馈 >= 自适应阈值 → 自动触发蒸馏
        """
        threshold = _compute_adaptive_threshold(feedback_rate)
        count = len(good_feedbacks)

        result = {
            "threshold": threshold,
            "current": count,
            "auto_triggered": count >= threshold,
            "message": ""
        }

        if result["auto_triggered"]:
            distilled = self.distill_from_feedback(good_feedbacks)
            result["distilled"] = distilled
            result["message"] = f"自动触发蒸馏（阈值={threshold}，当前={count}）"
        else:
            result["message"] = (
                f"未达自动蒸馏阈值（阈值={threshold}，当前={count}，"
                f"反馈率={feedback_rate:.1%}）"
            )

        return result

    # ─── 模板匹配 ─────────────────────────────────────────

    def match_template(self, user_request: str) -> list[dict]:
        """
        关键词匹配：用户请求 → 可用模板
        返回置信度排序的匹配结果
        """
        templates = self.list_templates()
        if not templates:
            return []

        request_keywords = set(self._extract_keywords(user_request, top_n=10))
        matches = []

        for tmpl in templates:
            try:
                with open(tmpl["file"], "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)

                tmpl_keywords = set(
                    data.get("template", {}).get("trigger", {}).get("keywords", [])
                )

                # Jaccard 相似度
                if request_keywords and tmpl_keywords:
                    intersection = len(request_keywords & tmpl_keywords)
                    union = len(request_keywords | tmpl_keywords)
                    confidence = round(intersection / union, 2) if union > 0 else 0.0
                else:
                    confidence = 0.0

                if confidence > 0:
                    matches.append({
                        "name": tmpl["name"],
                        "file": tmpl["file"],
                        "confidence": confidence,
                        "keywords_matched": list(request_keywords & tmpl_keywords),
                        "template_data": data.get("template", {})
                    })
            except (yaml.YAMLError, OSError):
                continue

        # 按置信度降序
        return sorted(matches, key=lambda x: x["confidence"], reverse=True)

    def generate_match_suggestion(self, user_request: str) -> Optional[str]:
        """
        生成匹配建议文本（供 AI 直接输出）
        命中高置信度模板 → 推荐执行
        命中低置信度 → 提供参考
        """
        matches = self.match_template(user_request)
        if not matches:
            return None

        top = matches[0]

        if top["confidence"] >= 0.5:
            lines = [
                f"[模板命中] 检测到与「{top['name']}」高度匹配（置信度 {top['confidence']*100:.0f}%）",
                f"  关键词: {', '.join(top['keywords_matched'])}"
            ]
            steps = top["template_data"].get("process", {}).get("steps", [])
            if steps:
                lines.append(f"  包含 {len(steps)} 个标准步骤")
            lines.append("")
            lines.append("  建议：是否使用此模板执行？")
            return "\n".join(lines)

        elif top["confidence"] >= 0.2:
            return (
                f"[参考模板] 发现相似模板「{top['name']}」（置信度 {top['confidence']*100:.0f}%）"
            )

        return None

    # ─── 工具方法 ─────────────────────────────────────────

    def _extract_keywords(self, text: str, top_n: int = 5) -> list[str]:
        """提取关键词"""
        stopwords = {
            "的", "了", "在", "是", "我", "有", "和", "就", "不", "人",
            "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去",
            "你", "会", "着", "没有", "看", "好", "自己", "这", "做", "进行"
        }

        words = re.findall(r'[\w]+', text)
        filtered = [w for w in words if w not in stopwords and len(w) >= 2]

        freq = Counter(filtered)
        return [word for word, _ in freq.most_common(top_n)]

    def _generate_recommendations(self, tag_freq) -> list[str]:
        """生成基于成功要素的建议"""
        recommendations = []
        for tag, count in tag_freq.most_common(5):
            if count >= 3:
                recommendations.append(
                    f"高频成功要素「{tag}」出现{count}次，建议固化为标准流程"
                )
        return recommendations

    def save_template(self, template: dict, name: str = None) -> Path:
        """保存模板为YAML文件"""
        template_name = name or template.get("template", {}).get("name", "unnamed")
        safe_name = re.sub(r'[^\w\s-]', '', template_name).strip()
        safe_name = re.sub(r'\s+', '_', safe_name) or "unnamed"

        output_file = self.templates_dir / f"{safe_name}.yaml"

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(template, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        return output_file

    def list_templates(self) -> list[dict]:
        """列出所有已保存的模板"""
        templates = []
        for tmpl_file in self.templates_dir.glob("*.yaml"):
            if "failed_patterns" in str(tmpl_file):
                continue
            try:
                with open(tmpl_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    templates.append({
                        "name": data.get("template", {}).get("name", tmpl_file.stem),
                        "version": data.get("template", {}).get("version", "?"),
                        "file": str(tmpl_file),
                        "created": data.get("template", {}).get("created", "未知")
                    })
            except (yaml.YAMLError, OSError):
                continue
        return templates

    def list_avoid_rules(self) -> list[dict]:
        """列出所有避坑规则"""
        rules = []
        for rule_file in self.avoid_dir.glob("avoid_*.yaml"):
            try:
                with open(rule_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    rules.append({
                        "file": str(rule_file),
                        "triggers": data.get("triggers", {}).get("keywords", []),
                        "problem": data.get("problem", ""),
                        "created": data.get("created", "未知")
                    })
            except (yaml.YAMLError, OSError):
                continue
        return rules

    def generate_distillation_report(self, distilled: dict, templates_created: int = 0) -> str:
        """生成蒸馏报告"""
        lines = ["## 知识蒸馏报告\n"]

        if "success_factors" in distilled:
            lines.append("### 成功要素分析\n")
            for sf in distilled["success_factors"][:5]:
                lines.append(f"- **{sf['tag']}**: {sf['frequency']} 次")

        if distilled.get("recommendations"):
            lines.append("\n### 优化建议\n")
            for rec in distilled["recommendations"]:
                lines.append(f"- {rec}")

        lines.append(f"\n---")
        lines.append(f"**本轮新增模板**: {templates_created} 个")

        return "\n".join(lines)


def run_distillation(
    workspace: str,
    good_feedbacks: list[dict] = None,
    feedback_rate: float = 0.0
) -> dict:
    """运行知识蒸馏主函数"""
    distiller = KnowledgeDistiller(workspace)

    if good_feedbacks:
        # 使用自适应阈值检查是否触发
        auto_result = distiller.check_and_auto_distill(good_feedbacks, feedback_rate)
        if auto_result["auto_triggered"]:
            return auto_result

        result = distiller.distill_from_feedback(good_feedbacks)
        result["auto_distill"] = auto_result
        return result
    else:
        return {
            "timestamp": datetime.now().isoformat(),
            "message": "无正面反馈数据，跳过蒸馏"
        }


if __name__ == "__main__":
    result = run_distillation("c:/Users/Administrator/WorkBuddy/20260412210819")
    distiller = KnowledgeDistiller("c:/Users/Administrator/WorkBuddy/20260412210819")
    print(distiller.generate_distillation_report(result))
    print(f"\n已有模板: {len(distiller.list_templates())} 个")
    print(f"已有避坑规则: {len(distiller.list_avoid_rules())} 个")
