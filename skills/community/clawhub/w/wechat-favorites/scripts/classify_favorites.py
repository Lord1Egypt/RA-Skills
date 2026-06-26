# -*- coding: utf-8 -*-
"""
微信收藏智能分类脚本 v1.3.0
支持自定义分类体系（从 JSON 加载）

用法：
    python classify_favorites.py                                  # 使用默认 9 大类
    python classify_favorites.py --categories user_categories.json  # 使用自定义分类
    python classify_favorites.py --llm                            # 启用 LLM 二次分类
    python classify_favorites.py --llm-only                       # 仅 LLM（全量）
    python auto_discover.py && python classify_favorites.py --categories user_categories.json  # 自动发现 + 分类
"""
import csv, os, re, json, argparse
from collections import defaultdict
from llm_classify import classify as llm_classify_batch, load_custom_categories

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "exported_favorites")

# ============================================================
# 默认一级分类关键词体系（当未指定 --categories 时使用）
# ============================================================
DEFAULT_CATEGORIES = {
    "生物医药": ["创新药", "ADC", "CAR-T", "mRNA", "临床试验", "靶点", "抗体", "疫苗",
                "基因治疗", "细胞治疗", "PD-1", "肿瘤", "癌症", "新药", "FDA", "NMPA",
                "CDE", "IND", "NDA", "生物药", "小分子", "大分子", "GLP-1", "减肥药",
                "阿尔茨海默", "帕金森", "罕见病"],
    "AI科技": ["GPT", "大模型", "LLM", "Agent", "RAG", "AI", "人工智能", "机器学习",
              "深度学习", "神经网络", "Transformer", "芯片", "GPU", "NVIDIA", "OpenAI",
              "Claude", "Gemini", "算力", "训练", "推理", "多模态", "AIGC", "ChatGPT"],
    "投资金融": ["IPO", "上市", "融资", "估值", "科创板", "创业板", "基金", "投资",
              "VC", "PE", "募资", "退出", "并购", "M&A", "市值", "股票", "二级市场",
              "一级市场", "投资机构", "LP", "GP"],
    "科学研究": ["Nature", "Science", "Cell", "论文", "研究", "发现", "突破", "神经科学",
              "生物学", "物理学", "化学", "材料", "量子", "实验", "学术", "博士后",
              "教授", "实验室"],
    "商业财经": ["企业", "公司", "战略", "行业", "市场", "商业模式", "盈利", "营收",
              "增长", "竞争", "垄断", "监管", "政策", "经济", "宏观", "GDP", "消费", "零售"],
    "生活方式": ["健康", "运动", "饮食", "睡眠", "心理", "旅行", "美食", "读书", "电影",
              "音乐", "游戏", "咖啡", "茶", "养生"],
    "媒体资讯": ["新闻", "热点", "事件", "评论", "观点", "分析", "报道", "记者", "媒体",
              "舆论", "热搜"],
    "政治国际": ["国际", "外交", "地缘", "政治", "政府", "政策", "中美", "欧盟", "俄罗斯",
              "战争", "冲突", "制裁"],
}

# ============================================================
# 二级分类体系（仅默认分类使用）
# ============================================================
SUBCATEGORIES = {
    "生物医药": {
        "临床": r"临床|IND|NDA|CDE|FDA|NMPA|III期|II期|I期|获批|批准",
        "神经": r"阿尔茨海默|帕金森|神经|脑科学|抑郁|认知障碍|AD|渐冻症|ALS",
        "创新药": r"创新药|新药|首创新药|first-in-class|best-in-class|FIC|BIC",
        "肿瘤": r"肿瘤|癌症|癌|oncology|肺癌|乳腺癌|肝癌|胃癌|肠癌|白血病|淋巴瘤",
        "抗体": r"抗体|单抗|双抗|多抗|nanobody|双特异性|三特异性",
        "基因治疗": r"基因治疗|基因编辑|CRISPR|AAV|碱基编辑|基因修复",
        "CAR-T": r"CAR.T|细胞治疗|CAR-NK|TIL|TCR.T",
        "ADC": r"ADC|抗体偶联|antibody.drug.conjugate",
        "靶点": r"靶点|target|信号通路|pathway|新靶点",
        "mRNA": r"mRNA|RNAi|核酸|siRNA|核苷酸",
        "PD-1/PD-L1": r"PD.1|PD.L1|免疫检查点|CTLA.4|LAG.3|TIGIT",
        "罕见病": r"罕见病|孤儿药|rare.disease",
        "GLP-1": r"GLP.1|司美格鲁肽|替尔泊肽|减肥药|司美|Tirzepatide|Semaglutide|肥胖",
        "中药": r"中药|中医|草本|中医药|中成药",
    },
    "AI科技": {
        "AI应用": r"AI[^医]应用|AI\+|赋能|落地|智能化|智慧|数字化|AI驱动|AI助力|AI改造|AI改变|AI如何|AI时代|用AI|借助AI|通过AI",
        "大模型/LLM": r"大模型|LLM|GPT|Claude|Gemini|Llama|ChatGPT|开源模型|基座模型",
        "AI医疗": r"AI医疗|AI\+药|AI制药|数字医疗|智能诊断|计算生物学",
        "芯片/算力": r"芯片|GPU|NVIDIA|算力|CUDA|TPU|H100|H200|B200|NPU|国产芯片",
        "机器人": r"机器人|robot|具身智能|人形|机械臂|自动化",
        "Agent": r"Agent|智能体|自主|autonomous|Multi.Agent",
        "AIGC": r"AIGC|生成式|内容生成|文生图|文生视频|生成式AI",
        "多模态": r"多模态|视觉|图像生成|视频生成|Sora|DALL.E|Midjourney|Stable",
        "RAG": r"RAG|检索增强|知识库|知识图谱",
    },
    "投资金融": {
        "VC/PE": r"VC|PE|风投|私募|募资|LP|GP|投资机构|创投",
        "二级市场": r"股票|A股|港股|美股|基金|ETF|量化|交易|牛熊",
        "IPO/上市": r"IPO|上市|招股|破发|打新",
        "并购": r"并购|M&A|收购|合并|重组",
        "宏观": r"利率|降息|加息|央行|货币|通胀|CPI|通缩|放水",
        "估值": r"估值|市值|定价|折价|溢价",
    },
    "科学研究": {
        "神经科学": r"神经|脑|意识|认知|突触|记忆",
        "生物": r"生物学|进化|生态|基因组|蛋白质",
        "物理": r"物理|量子|相对论|粒子|凝聚态",
        "化学": r"化学|分子|催化|合成|有机",
        "材料": r"材料|纳米|超导|石墨烯|二维",
        "天文": r"天文|宇宙|黑洞|星|太空|望远镜|火星",
    },
    "商业财经": {
        "宏观经济": r"经济|GDP|消费|出口|投资|增速|衰退|复苏",
        "行业分析": r"行业|赛道|市场|竞争格局|产业链|规模",
        "企业战略": r"战略|转型|重组|组织|变革|管理",
        "互联网": r"互联网|平台|电商|社交|流量|短视频|直播",
        "监管政策": r"监管|合规|法规|审批|备案|牌照|反垄断",
    },
    "生活方式": {
        "读书": r"读书|书评|阅读|推荐书|书单|好书|书摘",
        "健康": r"健康|养生|睡眠|饮食|营养|体检|长寿",
        "音乐": r"音乐|歌|乐器|乐队|专辑|演唱会",
        "影视": r"电影|剧|纪录片|综艺|导演|奥斯卡",
        "旅行": r"旅行|旅游|出行|攻略|景点|自驾",
        "运动": r"运动|健身|跑步|瑜伽|马拉松|骑行",
        "美食": r"美食|烹饪|食谱|餐厅|烘焙|食材",
    },
}

# ============================================================
# 跨领域标签（仅默认分类使用）
# ============================================================
CROSS_DOMAIN_RULES = [
    ("生物医药+投资", "生物医药", r"融资|估值|IPO|上市|投资|市值|VC|PE|募资|退出|交易|并购"),
    ("AI+医疗",       "AI科技",   r"医疗|药|临床|诊断|医院|健康|医药|生物|影像|手术"),
    ("AI+投资",       "AI科技",   r"融资|估值|IPO|上市|投资|市值|VC|PE|募资|交易"),
    ("生物医药+AI",   "生物医药", r"AI|人工智能|机器学习|大模型|深度学习|计算|数字|算法|数据驱动"),
    ("科学+政策",     "科学研究", r"政策|监管|伦理|法规|禁止|限制|批准"),
    ("商业+政治",     "商业财经", r"制裁|贸易战|关税|脱钩|地缘|国际关系|中美"),
]

# ============================================================
# 标准化映射
# ============================================================
CN_TO_KEY = {
    "生物医药": "biomed",
    "AI科技": "ai",
    "投资金融": "invest",
    "科学研究": "science",
    "商业财经": "business",
    "生活方式": "lifestyle",
    "媒体资讯": "media",
    "政治国际": "politics",
}

KEY_TO_CN = {v: k for k, v in CN_TO_KEY.items()}


def parse_args():
    parser = argparse.ArgumentParser(description="微信收藏智能分类")
    parser.add_argument("--categories", type=str, default=None,
                        help="自定义分类 JSON 文件路径（来自 auto_discover.py）")
    parser.add_argument("--llm", action="store_true", help="启用 LLM 二次分类")
    parser.add_argument("--llm-only", action="store_true", help="仅使用 LLM 分类（全量）")
    parser.add_argument("--llm-threshold", type=float, default=0.4,
                        help="触发 LLM 的置信度阈值（默认 0.4）")
    parser.add_argument("--input", type=str, default=None, help="输入 CSV 路径")
    parser.add_argument("--output", type=str, default=None, help="输出 CSV 路径")
    return parser.parse_args()


def load_custom_categories(json_path: str) -> Dict[str, List[str]]:
    """从 JSON 加载自定义分类"""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    categories = {}
    for cat in data.get("categories", []):
        name = cat.get("name", "")
        keywords = cat.get("keywords", [])
        if name and keywords:
            categories[name] = keywords
    return categories


def classify_text(title, description, categories):
    """返回文本命中的分类列表和置信度"""
    text = f"{title} {description}".lower()
    tags = []
    matched_kws = {}
    for cat, keywords in categories.items():
        for kw in keywords:
            if kw.lower() in text:
                tags.append(cat)
                matched_kws[cat] = kw
                break
    confidence = 0.5 if len(tags) >= 2 else (0.3 if tags else 0.0)
    return tags if tags else ["未分类"], confidence, matched_kws


def classify_subcategory(title, description, primary_cat):
    """返回二级分类列表（仅默认分类使用）"""
    if primary_cat not in SUBCATEGORIES:
        return []
    text = f"{title} {description}"
    subcats = SUBCATEGORIES[primary_cat]
    matched = []
    for sub_name, pattern in subcats.items():
        if re.search(pattern, text, re.IGNORECASE):
            matched.append(sub_name)
    return matched


def classify_cross_domain(title, description, primary_cats):
    """返回跨领域标签列表（仅默认分类使用）"""
    text = f"{title} {description}"
    cross_tags = []
    for tag, primary_cat, pattern in CROSS_DOMAIN_RULES:
        if primary_cat in primary_cats:
            if re.search(pattern, text, re.IGNORECASE):
                cross_tags.append(tag)
    return cross_tags


def main():
    args = parse_args()

    print("=" * 60)
    print("  微信收藏智能分类 v1.3.0")
    print("=" * 60)

    input_path = args.input or os.path.join(OUTPUT_DIR, "favorites_all.csv")
    output_path = args.output or os.path.join(OUTPUT_DIR, "articles_final.csv")

    if not os.path.exists(input_path):
        print(f"[ERROR] 输入文件不存在: {input_path}")
        print(f"        请先运行 export_favorites.py 生成收藏数据")
        return

    # 加载分类
    use_custom = bool(args.categories)
    if use_custom:
        if not os.path.exists(args.categories):
            print(f"[ERROR] 分类文件不存在: {args.categories}")
            print(f"        请先运行 auto_discover.py 生成分类体系")
            return
        categories = load_custom_categories(args.categories)
        print(f"[INFO] 加载自定义分类: {args.categories} ({len(categories)} 个类别)")
        use_subcat = False
        use_cross = False
    else:
        categories = DEFAULT_CATEGORIES
        print(f"[INFO] 使用默认 9 大类")
        use_subcat = True
        use_cross = True

    # 传递自定义分类到 llm_classify 模块
    if use_custom:
        load_custom_categories(args.categories)

    records = []
    cat_counts = defaultdict(int)
    subcat_counts = defaultdict(int)
    cross_counts = defaultdict(int)
    low_conf_records = []

    with open(input_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        for row in reader:
            title = row.get("title", "")
            desc = row.get("desc", "")

            if args.llm_only:
                tags = ["待LLM分类"]
                confidence = 0.0
                low_conf_records.append({
                    "local_id": row.get("local_id", ""),
                    "title": title,
                    "source_account": row.get("source_account", ""),
                    "url": row.get("url", ""),
                    "_row": row,
                })
            else:
                tags, confidence, _ = classify_text(title, desc, categories)

                if args.llm and confidence < args.llm_threshold:
                    low_conf_records.append({
                        "local_id": row.get("local_id", ""),
                        "title": title,
                        "source_account": row.get("source_account", ""),
                        "url": row.get("url", ""),
                        "_row": row,
                    })

            row["categories"] = "|".join(tags)
            row["_confidence"] = confidence

            # 二级分类（仅默认分类）
            if use_subcat and tags and tags != ["未分类"]:
                primary = tags[0]
                subcats = classify_subcategory(title, desc, primary)
                row["subcategory"] = "|".join(subcats) if subcats else ""
                for sc in subcats:
                    subcat_counts[f"{primary}>{sc}"] += 1
            else:
                row["subcategory"] = ""

            # 跨领域标签（仅默认分类）
            if use_cross and tags and tags != ["未分类"]:
                cross_tags = classify_cross_domain(title, desc, tags)
                row["cross_domain"] = "|".join(cross_tags) if cross_tags else ""
                for ct in cross_tags:
                    cross_counts[ct] += 1
            else:
                row["cross_domain"] = ""

            records.append(row)

            for t in tags:
                cat_counts[t] += 1

    # LLM 二次分类
    if low_conf_records:
        print(f"\n[LLM 二次分类] {len(low_conf_records)} 条需重判...")
        llm_results = llm_classify_batch(low_conf_records, categories=categories if use_custom else None)
        llm_map = {r["local_id"]: r for r in llm_results}

        llm_fixed = 0
        for row in records:
            lid = row.get("local_id", "")
            if lid in llm_map:
                lr = llm_map[lid]
                row["categories"] = "|".join(lr.get("tags", [])) or "未分类"
                row["_llm_reason"] = lr.get("reason", "")
                row["_llm_confidence"] = lr.get("confidence", 0.0)
                row["_confidence"] = lr.get("confidence", 0.0)
                llm_fixed += 1

                for t in row["categories"].split("|"):
                    cat_counts[t] += 1

        print(f"[LLM 二次分类] 完成，修正 {llm_fixed} 条")

    # 确定主分类
    for row in records:
        if "category" not in row or not row["category"]:
            cats = row.get("categories", "")
            row["category"] = cats.split("|")[0] if cats else "other"

    # 清理内部字段
    for row in records:
        row.pop("_row", None)

    # 确定输出字段
    output_fields = []
    for f in fieldnames:
        if f not in output_fields:
            output_fields.append(f)
    for extra in ["category", "subcategory", "cross_domain", "_confidence"]:
        if extra not in output_fields:
            output_fields.append(extra)
    if args.llm:
        for extra in ["_llm_reason", "_llm_confidence"]:
            if extra not in output_fields and any(extra in r for r in records):
                output_fields.append(extra)

    # 写 CSV
    if records:
        with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=output_fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(records)

    print(f"\n已分类: {output_path} ({len(records)} 条)\n")

    # 打印统计
    print("分类统计:")
    total = len(records)
    final_cats = defaultdict(int)
    for row in records:
        cat = row.get("category", "other")
        final_cats[cat] += 1
    for cat, count in sorted(final_cats.items(), key=lambda x: -x[1]):
        pct = 100 * count / total if total else 0
        print(f"  {cat}: {count} ({pct:.1f}%)")

    # 二级分类统计（仅默认）
    if use_subcat and subcat_counts:
        print(f"\n二级分类统计 (top 20):")
        for key, count in sorted(subcat_counts.items(), key=lambda x: -x[1])[:20]:
            print(f"  {key}: {count}")

    # 跨领域统计（仅默认）
    if use_cross and cross_counts:
        print(f"\n跨领域标签统计:")
        for tag, count in sorted(cross_counts.items(), key=lambda x: -x[1]):
            print(f"  {tag}: {count}")

    # 导出各分类 CSV
    cat_files = defaultdict(list)
    for row in records:
        cat = row.get("category", "other")
        cat_files[cat].append(row)

    for cat, rows in cat_files.items():
        safe_name = cat.replace("/", "_").replace("\\", "_")
        cat_path = os.path.join(os.path.dirname(output_path), f"cat_{safe_name}.csv")
        with open(cat_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=output_fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)

    print(f"\n各分类文件: {os.path.join(os.path.dirname(output_path), 'cat_*.csv')}")


if __name__ == "__main__":
    main()
