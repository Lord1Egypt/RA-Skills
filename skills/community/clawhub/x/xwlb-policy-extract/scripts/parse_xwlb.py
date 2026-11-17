#!/usr/bin/env python3
"""
新闻联播内容解析与政策提取脚本

功能：
1. 解析新闻联播文字稿，拆分为单条新闻
2. 根据关键词识别宏观经济政策相关内容
3. 按重要性分级（直接影响金融市场 vs 间接影响）
4. 输出结构化摘要

用法：
  python parse_xwlb.py <input_file> [--date DATE] [--output OUTPUT]
  
  或从 stdin 读取:
  echo "新闻联播文字稿..." | python parse_xwlb.py --stdin
"""

import re
import sys
import json
import argparse
from pathlib import Path
from collections import OrderedDict


# ============================================================
# 宏观政策关键词库（分层级）
# ============================================================

# 一级关键词：直接涉及金融市场定价因素
TIER1_KEYWORDS = OrderedDict({
    "货币政策": [
        "降准", "降息", "存款准备金", "公开市场操作", "逆回购", 
        "MLF", "中期借贷便利", "SLF", "LPR", "贷款市场报价利率",
        "货币政策", "流动性", "货币供应", "M2", "社会融资规模",
        "利率", "汇率", "人民币汇率", "外汇", "跨境资本",
    ],
    "财政政策": [
        "减税降费", "税收优惠", "留抵退税", "特别国债", "专项债",
        "赤字率", "财政政策", "政府债务", "地方债",
    ],
    "资本市场": [
        "注册制", "科创板", "北交所", "退市制度", "资本市场改革",
        "养老金入市", "保险资金", "长期资金入市", "机构投资者",
        "IPO", "再融资", "并购重组",
    ],
    "金融监管": [
        "金融监管", "防范化解金融风险", "系统性金融风险",
        "金融稳定", "宏观审慎", "影子银行",
    ],
    "房地产政策": [
        "房住不炒", "保交楼", "房地产市场", "房地产调控",
        "限购", "限贷", "首付比例", "保障性住房", "城中村改造",
        "房地产税",
    ],
})

# 二级关键词：重大产业/区域政策，间接影响市场
TIER2_KEYWORDS = OrderedDict({
    "产业政策": [
        "新质生产力", "人工智能", "数字经济", "集成电路", "芯片",
        "半导体", "新能源", "新能源汽车", "光伏", "风电", "储能",
        "氢能", "生物医药", "高端装备", "新材料", "航空航天",
        "低空经济", "商业航天", "机器人",
    ],
    "基础设施": [
        "新基建", "重大工程", "基础设施建设", "东数西算",
        "算力基础设施", "水利工程",
    ],
    "区域战略": [
        "一带一路", "粤港澳大湾区", "长三角一体化", "京津冀协同",
        "长江经济带", "海南自贸港", "自贸区", "自由贸易港",
        "西部大开发", "东北振兴",
    ],
    "改革开放": [
        "营商环境", "外资准入", "负面清单", "制度型开放",
        "稳外资", "稳外贸", "市场化改革",
    ],
    "绿色低碳": [
        "碳达峰", "碳中和", "绿色金融", "碳排放权交易",
        "能耗双控", "绿色转型",
    ],
    "平台经济": [
        "平台经济", "反垄断", "数字经济监管", "数据安全",
    ],
})

# 三级关键词：一般性政策，市场关注度较低但可参考
TIER3_KEYWORDS = [
    "就业", "居民收入", "消费促进", "内需扩大",
    "社会保障", "养老金", "医保", "乡村振兴", "新型城镇化",
    "共同富裕", "收入分配",
]

# 人物标记关键词
PERSON_INDICATORS = [
    "习近平", "李强", "总理", "主席", "总书记",
    "主持召开", "出席会议", "发表重要讲话", "作出重要指示",
    "国务院常务会议", "国常会", "中央政治局", "中央经济工作会议",
    "中央财经委员会", "中央金融委员会", "中央深改委",
    "央行", "人民银行", "发改委", "财政部", "工信部", "住建部",
    "证监会", "银保监会", "金融监管总局", "商务部",
    "国新办", "新闻发布会",
]


def load_text(filepath=None):
    """加载文字稿文本"""
    if filepath:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return sys.stdin.read()


def split_news_items(text):
    """
    将新闻联播文字稿拆分为单条新闻。
    通常每条新闻以换行+关键词开头，或以序号开头。
    """
    # 清理多余空白
    text = re.sub(r'\n{3,}', '\n\n', text.strip())
    
    # 常见的新闻分隔标记
    # 1. 以序号开头: "1.", "一、", "（一）"
    # 2. 以日期换行
    # 3. 以【标题】开头
    
    # 先按双换行分块
    blocks = re.split(r'\n\s*\n', text)
    
    # 合并过短的块
    items = []
    buffer = ""
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        if len(block) < 30 and buffer:
            buffer += "\n" + block
        elif len(block) < 30:
            buffer = block
        else:
            if buffer:
                items.append(buffer)
            buffer = block
    if buffer:
        items.append(buffer)
    
    # 如果分块太少，尝试按新闻标题模式分割
    if len(items) <= 1:
        items = re.split(
            r'(?=(?:【|\[|（[一二三四五六七八九十\d]）|\d+[\.、]|\n(?:(?:国家|我国|全国|中央|国务院|习近平|李强))))',
            text
        )
        items = [i.strip() for i in items if i.strip() and len(i.strip()) > 20]
    
    return items


def match_keywords(text, keyword_dict):
    """检查文本是否包含关键词，返回匹配的分类"""
    matches = []
    for category, keywords in keyword_dict.items():
        for kw in keywords:
            if kw in text:
                matches.append((category, kw))
                break
    return matches


def is_macro_policy_item(text):
    """判断是否为宏观政策相关新闻"""
    # 检查一级关键词
    tier1_matches = match_keywords(text, TIER1_KEYWORDS)
    tier2_matches = match_keywords(text, TIER2_KEYWORDS)
    
    # 检查是否有人物/机构标记
    has_person = any(p in text for p in PERSON_INDICATORS)
    
    # 检查三级关键词
    tier3_matches = [kw for kw in TIER3_KEYWORDS if kw in text]
    
    if tier1_matches:
        return "tier1", tier1_matches
    elif tier2_matches:
        return "tier2", tier2_matches
    elif tier3_matches and has_person:
        return "tier3", [("民生/社会政策", kw) for kw in tier3_matches]
    
    return None, []

def extract_title(text, max_len=60):
    """从新闻文本中提取标题/概要"""
    # 尝试找【】或[]中的内容
    bracket_match = re.search(r'[【\[](.+?)[】\]]', text)
    if bracket_match:
        return bracket_match.group(1)[:max_len]
    
    # 取第一句话
    first_sentence = re.split(r'[。；\n]', text)[0]
    first_sentence = re.sub(r'^(央视网消息|新华社消息|本台消息|央视新闻)[：:]', '', first_sentence)
    
    if len(first_sentence) > max_len:
        return first_sentence[:max_len] + "…"
    return first_sentence.strip()


def analyze(text, date=""):
    """
    分析新闻联播文字稿，输出结构化结果
    
    返回:
        dict: {
            "date": "日期",
            "total_items": 总条数,
            "policy_items": [政策新闻列表],
            "other_summary": "其他新闻摘要"
        }
    """
    items = split_news_items(text)
    
    policy_items = []
    other_items = []
    
    for idx, item in enumerate(items):
        title = extract_title(item)
        tier, matches = is_macro_policy_item(item)
        
        if tier:
            categories = list(set(c for c, _ in matches))
            keywords = list(set(kw for _, kw in matches))
            
            policy_items.append({
                "index": idx + 1,
                "title": title,
                "tier": tier,
                "tier_label": {
                    "tier1": "🔴 直接影响金融市场",
                    "tier2": "🟡 重大产业/区域政策",
                    "tier3": "🟢 一般性政策参考",
                }.get(tier, tier),
                "categories": categories,
                "keywords": keywords,
                "content_preview": item[:200] + ("…" if len(item) > 200 else ""),
            })
        else:
            other_items.append(title)
    
    # 合并同类项
    merged = _merge_similar(policy_items)
    
    return {
        "date": date,
        "total_items": len(items),
        "policy_count": len(policy_items),
        "tier1_count": sum(1 for p in policy_items if p["tier"] == "tier1"),
        "tier2_count": sum(1 for p in policy_items if p["tier"] == "tier2"),
        "tier3_count": sum(1 for p in policy_items if p["tier"] == "tier3"),
        "policy_items": merged,
        "other_summary": other_items[:10],  # 最多10条
    }


def _merge_similar(items):
    """合并内容相近的政策条目"""
    if len(items) <= 1:
        return items
    
    merged = []
    used = set()
    
    for i, item in enumerate(items):
        if i in used:
            continue
        group = [item]
        
        for j in range(i + 1, len(items)):
            if j in used:
                continue
            # 如果类别有交集，合并
            common = set(item["categories"]) & set(items[j]["categories"])
            if common:
                group.append(items[j])
                used.add(j)
        
        if len(group) > 1:
            # 合并：保留第一条的标题和预览，合并关键词和类别
            item["keywords"] = list(set(kw for g in group for kw in g["keywords"]))
            item["categories"] = list(set(c for g in group for c in g["categories"]))
            # 取最高级别
            tiers = [g["tier"] for g in group]
            if "tier1" in tiers:
                item["tier"] = "tier1"
                item["tier_label"] = "🔴 直接影响金融市场"
            elif "tier2" in tiers:
                item["tier"] = "tier2"
                item["tier_label"] = "🟡 重大产业/区域政策"
        
        merged.append(item)
    
    return merged


def format_output(result, fmt="markdown"):
    """格式化输出结果"""
    if fmt == "json":
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    # Markdown 格式
    lines = []
    date_str = f" ({result['date']})" if result['date'] else ""
    lines.append(f"# 📺 新闻联播政策摘报{date_str}")
    lines.append("")
    lines.append(f"> 本日共 {result['total_items']} 条新闻，其中政策相关 {result['policy_count']} 条")
    lines.append(f"> 🔴 直接影响金融市场: {result['tier1_count']} 条 | 🟡 重大产业/区域政策: {result['tier2_count']} 条 | 🟢 一般性政策: {result['tier3_count']} 条")
    lines.append("")
    
    if result['policy_items']:
        lines.append("---")
        lines.append("")
        lines.append("## 🎯 重点政策摘要")
        lines.append("")
        
        for item in result['policy_items']:
            lines.append(f"### {item['tier_label']}")
            lines.append(f"**{item['title']}**")
            lines.append("")
            lines.append(f"📌 关键词：{'、'.join(item['keywords'])}")
            lines.append("")
            lines.append(f"{item['content_preview']}")
            lines.append("")
            lines.append("---")
            lines.append("")
    else:
        lines.append("⚠️ 未检测到宏观经济政策相关内容。")
        lines.append("")
    
    if result['other_summary']:
        lines.append("## 📋 其他要闻速览")
        lines.append("")
        for i, title in enumerate(result['other_summary'], 1):
            lines.append(f"{i}. {title}")
        lines.append("")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="新闻联播内容解析与政策提取工具"
    )
    parser.add_argument(
        "input", nargs="?", default=None,
        help="新闻联播文字稿文件路径（不提供则从 stdin 读取）"
    )
    parser.add_argument(
        "--date", "-d", default="",
        help="新闻联播日期，如 2026-08-02"
    )
    parser.add_argument(
        "--stdin", action="store_true",
        help="从标准输入读取（优先级高于文件）"
    )
    parser.add_argument(
        "--output", "-o", default="",
        help="输出文件路径（默认输出到 stdout）"
    )
    parser.add_argument(
        "--format", "-f", choices=["markdown", "json", "json-only-policy"],
        default="markdown",
        help="输出格式"
    )
    
    args = parser.parse_args()
    
    # 加载文本
    if args.stdin or (not args.input and sys.stdin.isatty() is False):
        text = load_text()
    elif args.input:
        text = load_text(args.input)
    else:
        # 无输入时输出帮助
        print("错误：请提供新闻联播文字稿（文件路径或管道输入）", file=sys.stderr)
        print("用法：python parse_xwlb.py <文字稿文件> 或 echo '文字稿' | python parse_xwlb.py --stdin", file=sys.stderr)
        sys.exit(1)
    
    # 分析
    result = analyze(text, args.date)
    
    # 格式化
    if args.format == "json":
        output = json.dumps(result, ensure_ascii=False, indent=2)
    elif args.format == "json-only-policy":
        output = json.dumps(result["policy_items"], ensure_ascii=False, indent=2)
    else:
        output = format_output(result, "markdown")
    
    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"✅ 已保存到: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
