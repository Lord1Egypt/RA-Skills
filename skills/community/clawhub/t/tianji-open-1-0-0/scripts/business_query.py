#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天机我要查 (免费版) · 企业信息查询脚本（可选批量加速器）
================================================
TianJi-Open — optional batch accelerator for enterprise info query.

本脚本是「天机我要查 (免费版)」技能的**可选**加速器：当用户已安装 baidu-search 技能时，
可批量构造多维度检索式并汇总结果。未安装 baidu-search 时，核心查询由对话
内置的网络搜索完成，本脚本会友好提示并退出，不影响技能正常使用。

用法:
    python business_query.py "<公司全称>" [--type TYPE] [--count COUNT]

参数:
    <公司全称>   必填，建议用工商注册全称
    --type       查询维度: basic|shareholder|risk|finance|news|contact|all(默认)
    --count      每维度返回条数，默认 8
"""

import json
import os
import subprocess
import sys
from datetime import datetime

# baidu-search 技能搜索脚本路径（用户主目录下，跨机器自适应）
BAIDU_SEARCH_SCRIPT = os.path.expanduser(
    "~/.workbuddy/skills/baidu-search/scripts/search.py"
)

SEARCH_TEMPLATES = {
    "basic": "{name} 工商信息 注册资本 成立时间 经营状态 统一社会信用代码",
    "shareholder": "{name} 股东 法人代表 实控人 大股东 持股比例",
    "risk": "{name} 失信 被执行人 诉讼 行政处罚 经营异常",
    "finance": "{name} 融资 IPO 上市 投资 估值",
    "news": "{name} 最新 新闻 动态 媒体报道",
    "contact": "{name} 联系方式 地址 电话 官网",
    "bidding": "{name} 招标 中标 采购 投标 候选人 公示",
    "qualification": "{name} 资质 证书 许可 专利 商标 软件著作权",
    "sentiment": "{name} 舆情 负面 投诉 争议 处罚",
}

TYPE_LABELS = {
    "basic": "工商基本信息",
    "shareholder": "股东与实控人",
    "risk": "经营风险",
    "finance": "融资与上市",
    "news": "新闻舆情",
    "contact": "联系方式",
    "bidding": "招标与采购动态",
    "qualification": "资质与知识产权",
    "sentiment": "舆情与争议",
}


class BusinessSearch:
    """商业信息查询（可选加速器）。"""

    def __init__(self):
        self.available = os.path.exists(BAIDU_SEARCH_SCRIPT)

    def search(self, query: str, count: int = 8):
        """调用 baidu-search 执行一次检索；不可用时返回 None。"""
        if not self.available:
            return None
        try:
            proc = subprocess.run(
                [
                    sys.executable,
                    BAIDU_SEARCH_SCRIPT,
                    json.dumps({"query": query, "count": count}, ensure_ascii=False),
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if proc.returncode == 0 and proc.stdout.strip():
                return json.loads(proc.stdout)
        except subprocess.TimeoutExpired:
            print("搜索超时，请稍后重试或减少维度。", file=sys.stderr)
        except Exception as exc:  # noqa: BLE001
            print(f"搜索异常: {exc}", file=sys.stderr)
        return []

    def query(self, company: str, qtype: str = "all", count: int = 8) -> dict:
        """按维度执行检索，返回 {维度: 结果列表}。"""
        templates = (
            SEARCH_TEMPLATES
            if qtype == "all"
            else {qtype: SEARCH_TEMPLATES.get(qtype, SEARCH_TEMPLATES["basic"])}
        )
        results = {}
        for t, tpl in templates.items():
            q = tpl.format(name=company)
            print(f"[检索] {TYPE_LABELS.get(t, t)}: {q}", file=sys.stderr)
            results[t] = self.search(q, count)
        return results

    def render(self, company: str, results: dict) -> str:
        """生成 Markdown 报告（逐条附来源）。"""
        out = []
        out.append("## 企业信息查询报告 · 天机我要查 (免费版)")
        out.append(f"- 查询对象：{company}")
        out.append(f"- 采集时间：{datetime.now().strftime('%Y-%m-%d')}")
        out.append("- 数据说明：基于 baidu-search 公开检索整理，仅供参考；重要结论请以官方渠道核验")
        out.append("")
        for t, items in results.items():
            out.append(f"### {TYPE_LABELS.get(t, t)}")
            if not items:
                out.append("- 未检索到相关信息（或需以官方渠道核验）")
                out.append("")
                continue
            for it in items[:8]:
                if isinstance(it, dict):
                    title = it.get("title", "")
                    url = it.get("url", "")
                    snippet = it.get("snippet", "")
                    line = f"- {title}" if title else "- (无标题)"
                    if snippet:
                        line += f"：{snippet[:120]}"
                    if url:
                        line += f" ｜ 来源：[{title or '链接'}]({url})"
                    out.append(line)
                else:
                    out.append(f"- {it}")
            out.append("")
        out.append(
            "> 风险提示：高风险结论（失信 / 处罚 / 诉讼）务必以国家企业信用信息公示系统、"
            "中国执行信息公开网等官方渠道核验。"
        )
        return "\n".join(out)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    company = sys.argv[1]
    qtype, count = "all", 8
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--type" and i + 1 < len(sys.argv):
            qtype = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--count" and i + 1 < len(sys.argv):
            count = int(sys.argv[i + 1])
            i += 2
        else:
            i += 1

    bs = BusinessSearch()
    if not bs.available:
        print(
            "提示：未检测到 baidu-search 技能，批量脚本不可用。\n"
            "「天机我要查 (免费版)」仍可通过对话内置的网络搜索正常使用——直接在对话中告诉我"
            f"「查一下 {company}」即可。",
            file=sys.stderr,
        )
        sys.exit(0)

    results = bs.query(company, qtype, count)
    print(bs.render(company, results))


if __name__ == "__main__":
    main()
