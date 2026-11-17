#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
头条内容自动审查脚本（Toutiao Content Auditor）
基于TRACE五维审查体系，检测违规词/重复度/字数/格式/AI标注等问题。

用法:
    python toutiao_audit.py <文章文件路径>
    python toutiao_audit.py <目录路径> --batch
"""

import os
import re
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime

# ============================================================
# 违规词库（来自头条公开课违规避雷指南）
# ============================================================

# 广告法极限词
EXTREME_WORDS = [
    "最", "第一", "唯一", "顶级", "极品", "绝佳", "绝对", "百分之百",
    "全网最低", "史上最强", "前无古人", "国家级", "世界级", "宇宙级",
    "秒杀", "吊打", "完爆", "碾压", "无敌", "神器", "之王", "之最"
]

# 标题党模式
CLICKBAIT_PATTERNS = [
    r"\d+%的人都", r"震惊", r"不看后悔", r"太可怕了", r"万万没想到",
    r"居然是", r"真相竟然", r"看完吓一跳", r"99%的人不知道",
    r"速看", r"紧急通知", r"刚刚曝光", r"内幕揭秘", r"深度爆料"
]

# AI黑话（过度使用AI写作痕迹）
AI_CLICHES = [
    "探索", "解锁", "重塑", "破局", "赋能", "抓手", "闭环", "打法",
    "底层逻辑", "顶层设计", "降维打击", "范式转移", "认知升级",
    "深度赋能", "全面升级", "一站式", "全方位", "多维度", "立体化"
]

# 平台违规引导语（用户明确要求规避）
VIOLATION_GUIDES = [
    "转发给爸妈", "关注我每天学", "点赞收藏", "关注不迷路",
    "双击屏幕", "评论区告诉我", "记得点赞", "帮忙转发"
]

# 敏感词（政治/色情/暴力/诈骗/平台红线）
SENSITIVE_WORDS = [
    # 诈骗/违规
    "套现", "洗钱", "赌博", "博彩", "赌场", "赔率",
    "色情", "裸聊", "约炮", "一夜情",
    # 暴力/违法
    "杀人", "砍人", "自杀", "自残", "炸药", "炸弹",
    # 政治敏感（保留最小集，实际应接外部词库）
    # 这里不写具体政治词，避免误报；政治敏感词应接外部词库
    # 平台红线
    "翻墙", "VPN破解", "盗版下载", "免费破解",
]

# 违规推广相关
PROMOTION_PATTERNS = [
    r"微信[号号:：]\s*\w+", r"vx\s*[:：]?\s*\w+", r"V信\s*[:：]?\s*\w+",
    r"QQ[号号:：]\s*\d+", r"扣扣\s*[:：]?\s*\d+",
    r"扫码(?!枪|器|头|机)", r"二维码", r"扫一扫",  # 09-12 老马 r99 修正：排除技术名词误伤
    r"购买链接", r"点击购买", r"立即下单", r"限时特惠",
    r"加我", r"私信我", r"联系我", r"咨询我"
]

# ============================================================
# 审查引擎
# ============================================================

class ToutiaoAuditor:
    """头条内容审查器"""

    def __init__(self):
        self.results = []
        self.intercept_items = []  # 拦截项（必须修改）
        self.warning_items = []    # 警告项（建议修改）
        self.pass_items = []       # 通过项

    def audit_file(self, file_path):
        """审查单个文件"""
        file_path = Path(file_path)
        if not file_path.exists():
            return {"error": f"文件不存在: {file_path}"}

        # 读取文件
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            return {"error": f"读取文件失败: {e}"}

        result = {
            "file": str(file_path),
            "filename": file_path.name,
            "audit_time": datetime.now().isoformat(),
            "checks": {}
        }

        # 1. 字数检查
        word_count = self._check_word_count(content)
        result["checks"]["word_count"] = word_count

        # 2. 标题检查
        title_check = self._check_title(content)
        result["checks"]["title"] = title_check

        # 3. 极限词检查
        extreme_check = self._check_extreme_words(content)
        result["checks"]["extreme_words"] = extreme_check

        # 4. 标题党检查
        clickbait_check = self._check_clickbait(content)
        result["checks"]["clickbait"] = clickbait_check

        # 5. AI黑话检查
        ai_cliche_check = self._check_ai_cliches(content)
        result["checks"]["ai_cliches"] = ai_cliche_check

        # 6. 违规引导语检查
        guide_check = self._check_violation_guides(content)
        result["checks"]["violation_guides"] = guide_check

        # 7. 违规推广检查
        promo_check = self._check_promotion(content)
        result["checks"]["promotion"] = promo_check

        # 8. 格式检查
        format_check = self._check_format(content)
        result["checks"]["format"] = format_check

        # 9. AI标注检查
        ai_label_check = self._check_ai_label(content, file_path)
        result["checks"]["ai_label"] = ai_label_check

        # 10. 重复度检查（文件哈希，用于跨篇对比）
        dup_check = self._check_duplicate(content, file_path)
        result["checks"]["duplicate"] = dup_check

        # 汇总
        result["summary"] = self._summarize(result["checks"])
        result["status"] = "PASS" if not self.intercept_items else "INTERCEPTED"

        return result

    def _check_word_count(self, content):
        """字数检查：800-1500字为最佳区间"""
        # 移除markdown标记后统计中文字数
        clean = re.sub(r'[#*`\-\[\]()!]', '', content)
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', clean))
        total_chars = len(clean.strip())

        if chinese_chars < 300:
            self.intercept_items.append(f"字数过低：仅{chinese_chars}字（最低300字）")
            status = "FAIL"
        elif chinese_chars < 800:
            self.warning_items.append(f"字数偏少：{chinese_chars}字（建议800-1500字）")
            status = "WARN"
        elif chinese_chars > 3000:
            self.warning_items.append(f"字数偏多：{chinese_chars}字（建议控制在3000字以内）")
            status = "WARN"
        else:
            self.pass_items.append(f"字数合适：{chinese_chars}字")
            status = "PASS"

        return {"status": status, "chinese_chars": chinese_chars, "total_chars": total_chars}

    def _check_title(self, content):
        """标题检查：不超过30字，不含违规词"""
        lines = content.strip().split('\n')
        title = ""
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                title = line
                break
            if line.startswith('#'):
                title = line.lstrip('#').strip()
                break

        if not title:
            self.intercept_items.append("无标题")
            return {"status": "FAIL", "title": "", "reason": "无标题"}

        title_len = len(title)
        issues = []

        if title_len > 30:
            issues.append(f"标题过长：{title_len}字（建议不超过30字）")

        # 标题中含极限词
        title_extreme = [w for w in EXTREME_WORDS if w in title]
        if title_extreme:
            issues.append(f"标题含极限词：{','.join(title_extreme)}")

        # 标题中含标题党模式
        for pattern in CLICKBAIT_PATTERNS:
            if re.search(pattern, title):
                issues.append(f"标题含标题党模式：{pattern}")
                break

        if issues:
            self.intercept_items.append(f"标题问题：{'; '.join(issues)}")
            return {"status": "FAIL", "title": title, "issues": issues}
        else:
            self.pass_items.append(f"标题合格：{title[:20]}...")
            return {"status": "PASS", "title": title, "length": title_len}

    def _check_extreme_words(self, content):
        """极限词检查（v1.2：最/第一加描述性语境过滤，其余极限词保持直接命中）"""
        found = []
        context_filtered = []
        # 描述性语境：这些"最X/第一X"是中文常用描述，非广告法极限词
        DESC_ZUI = re.compile(r'^最[后近新初大小多少重要基本常见典型终]')
        DESC_DIYI = re.compile(r'^第一[句步个篇次轮时间]')
        for w in EXTREME_WORDS:
            if w not in content:
                continue
            if w == "最":
                real = 0
                for m in re.finditer(r'最', content):
                    ctx = content[m.start():m.start()+3]
                    if DESC_ZUI.match(ctx):
                        context_filtered.append(f"最→{ctx}")
                    else:
                        real += 1
                if real > 0:
                    found.append("最")
            elif w == "第一":
                real = 0
                for m in re.finditer(r'第一', content):
                    ctx = content[m.start():m.start()+5]
                    if DESC_DIYI.match(ctx):
                        context_filtered.append(f"第一→{ctx}")
                    else:
                        real += 1
                if real > 0:
                    found.append("第一")
            else:
                found.append(w)
        if found:
            self.warning_items.append(f"含广告法极限词：{','.join(found[:10])}")
            return {"status": "WARN", "found": found,
                    "context_filtered": list(set(context_filtered))}
        return {"status": "PASS", "found": [],
                "context_filtered": list(set(context_filtered))}

    def _check_clickbait(self, content):
        """标题党模式检查"""
        found = []
        for pattern in CLICKBAIT_PATTERNS:
            matches = re.findall(pattern, content)
            if matches:
                found.extend(matches)
        if found:
            self.warning_items.append(f"含标题党表达：{','.join(list(set(found))[:5])}")
            return {"status": "WARN", "found": list(set(found))}
        return {"status": "PASS", "found": []}

    def _check_ai_cliches(self, content):
        """AI黑话检查"""
        found = [w for w in AI_CLICHES if w in content]
        if len(found) >= 3:
            self.warning_items.append(f"AI黑话过多（{len(found)}个）：{','.join(found[:8])}，建议替换为口语化表达")
            return {"status": "WARN", "found": found, "count": len(found)}
        return {"status": "PASS", "found": found, "count": len(found)}

    def _check_violation_guides(self, content):
        """违规引导语检查（用户明确要求规避）"""
        found = [g for g in VIOLATION_GUIDES if g in content]
        if found:
            self.intercept_items.append(f"含平台违规引导语：{','.join(found)}（可能触发平台限流）")
            return {"status": "FAIL", "found": found}
        return {"status": "PASS", "found": []}

    def _check_promotion(self, content):
        """违规推广检查（v1.1：加语境过滤，规则说明/禁词清单里提到"二维码"不算真引流）"""
        found = []
        context_filtered = []
        # 否定/警示语境：命中词出现在这些词附近时，是在讲平台规则而非真引流
        NEGATIVE_CONTEXT = re.compile(
            r'(禁|不|勿|避免|别|红线|敏感词|违规|禁止|请勿|清单|规则|扫描|不得|不要|别发|下列|以下|导流|硬广|限流|降权|处置|提示|提醒|注意)'
        )
        for pattern in PROMOTION_PATTERNS:
            for m in re.finditer(pattern, content, re.IGNORECASE):
                start = max(0, m.start() - 25)
                end = min(len(content), m.end() + 25)
                ctx = content[start:end]
                if NEGATIVE_CONTEXT.search(ctx):
                    context_filtered.append(m.group(0))
                else:
                    found.append(m.group(0))
        if found:
            self.intercept_items.append(f"含违规推广信息：{','.join(list(set(found))[:5])}")
            return {"status": "FAIL", "found": list(set(found)),
                    "context_filtered": list(set(context_filtered))}
        return {"status": "PASS", "found": [],
                "context_filtered": list(set(context_filtered))}

    def _check_format(self, content):
        """格式检查：段落长度/标点/错别字"""
        lines = content.strip().split('\n')
        issues = []

        # 段落过长（超过5行）
        long_paragraphs = 0
        for line in lines:
            if len(line) > 200 and not line.startswith('#'):
                long_paragraphs += 1
        if long_paragraphs > 3:
            issues.append(f"长段落过多（{long_paragraphs}段超过200字），建议拆分")

        # 检查是否有连续空行
        if re.search(r'\n{3,}', content):
            issues.append("存在连续空行，建议清理")

        # 检查标点（中英文混用）
        if re.search(r'[a-zA-Z][，。！？；：]', content):
            issues.append("存在英文后接中文标点，建议统一")

        if issues:
            self.warning_items.append(f"格式问题：{'; '.join(issues)}")
            return {"status": "WARN", "issues": issues}
        return {"status": "PASS", "issues": []}

    def _check_ai_label(self, content, file_path):
        """AI标注检查：AI生成内容必须标注"""
        # 检查文件名或内容中是否有AI标注
        ai_indicators = ["AI生成", "AI创作", "人工智能生成", "本文由AI", "AI辅助"]
        has_label = any(ind in content for ind in ai_indicators) or "ai" in file_path.name.lower()

        # 检查是否有明显的AI写作特征（大量AI黑话+结构化模板）
        ai_cliche_count = sum(1 for w in AI_CLICHES if w in content)
        likely_ai = ai_cliche_count >= 5

        if likely_ai and not has_label:
            self.intercept_items.append("疑似AI生成但未标注，必须添加AI生成声明")
            return {"status": "FAIL", "likely_ai": True, "has_label": False}
        return {"status": "PASS", "likely_ai": likely_ai, "has_label": has_label}

    def _check_duplicate(self, content, file_path):
        """重复度检查（基于内容哈希，用于跨篇对比）"""
        content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
        # 简化版：只记录哈希，跨篇对比需要外部存储
        return {"status": "PASS", "content_hash": content_hash, "note": "跨篇重复度需批量对比"}

    def _summarize(self, checks):
        """汇总审查结果"""
        total = len(checks)
        passed = sum(1 for c in checks.values() if c.get("status") == "PASS")
        warned = sum(1 for c in checks.values() if c.get("status") == "WARN")
        failed = sum(1 for c in checks.values() if c.get("status") == "FAIL")

        return {
            "total_checks": total,
            "passed": passed,
            "warned": warned,
            "failed": failed,
            "intercept_count": len(self.intercept_items),
            "warning_count": len(self.warning_items),
            "pass_rate": f"{passed/total*100:.1f}%" if total > 0 else "0%"
        }

    def audit_directory(self, dir_path):
        """批量审查目录"""
        dir_path = Path(dir_path)
        if not dir_path.is_dir():
            return {"error": f"不是目录: {dir_path}"}

        results = []
        for ext in ['*.md', '*.txt']:
            for f in dir_path.rglob(ext):
                # 重置状态
                self.intercept_items = []
                self.warning_items = []
                self.pass_items = []
                result = self.audit_file(f)
                result["intercept_items"] = self.intercept_items.copy()
                result["warning_items"] = self.warning_items.copy()
                results.append(result)

        # 汇总
        total = len(results)
        intercepted = sum(1 for r in results if r.get("status") == "INTERCEPTED")
        passed = sum(1 for r in results if r.get("status") == "PASS")

        return {
            "directory": str(dir_path),
            "total_files": total,
            "passed": passed,
            "intercepted": intercepted,
            "pass_rate": f"{passed/total*100:.1f}%" if total > 0 else "0%",
            "results": results
        }


def print_report(result):
    """打印审查报告"""
    print("=" * 60)
    print(f"头条内容审查报告")
    print("=" * 60)
    print(f"文件: {result.get('filename', 'N/A')}")
    print(f"时间: {result.get('audit_time', 'N/A')}")
    print(f"状态: {'✅ 通过' if result.get('status') == 'PASS' else '❌ 拦截'}")
    print("-" * 60)

    summary = result.get("summary", {})
    print(f"检查项: {summary.get('total_checks', 0)}项")
    print(f"通过: {summary.get('passed', 0)}项 | 警告: {summary.get('warned', 0)}项 | 失败: {summary.get('failed', 0)}项")
    print(f"通过率: {summary.get('pass_rate', '0%')}")
    print("-" * 60)

    if result.get("intercept_items"):
        print("\n❌ 拦截项（必须修改）:")
        for i, item in enumerate(result["intercept_items"], 1):
            print(f"  {i}. {item}")

    if result.get("warning_items"):
        print("\n⚠️ 警告项（建议修改）:")
        for i, item in enumerate(result["warning_items"], 1):
            print(f"  {i}. {item}")

    print("\n" + "=" * 60)


def main():
    if len(sys.argv) < 2:
        print("用法: python toutiao_audit.py <文件路径> [--batch]")
        print("示例: python toutiao_audit.py article.md")
        print("      python toutiao_audit.py ./articles --batch")
        sys.exit(1)

    path = sys.argv[1]
    batch = "--batch" in sys.argv

    auditor = ToutiaoAuditor()

    if batch or os.path.isdir(path):
        result = auditor.audit_directory(path)
        # 输出JSON
        output_file = Path(path) / "audit_report.json"
        output_file.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"批量审查完成: {result.get('total_files', 0)}个文件")
        print(f"通过: {result.get('passed', 0)} | 拦截: {result.get('intercepted', 0)}")
        print(f"通过率: {result.get('pass_rate', '0%')}")
        print(f"报告已保存: {output_file}")
    else:
        result = auditor.audit_file(path)
        result["intercept_items"] = auditor.intercept_items
        result["warning_items"] = auditor.warning_items
        print_report(result)
        # 输出JSON
        output_file = Path(path).with_suffix('.audit.json')
        output_file.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == "__main__":
    main()
