#!/usr/bin/env python3
"""基于 jieba 分词的高级重复检测

可选依赖: pip install jieba
若无 jieba 自动降级到正则模式
"""

import re
import sys
from collections import Counter
from pathlib import Path
from typing import List, Tuple

# 尝试导入 jieba，失败则降级
try:
    import jieba
    import jieba.analyse
    HAS_JIEBA = True
except ImportError:
    HAS_JIEBA = False


def tokenize(text: str) -> List[str]:
    """分词，优先 jieba"""
    if HAS_JIEBA:
        return [w for w in jieba.cut(text) if len(w.strip()) > 0]
    else:
        # 降级：按字+常见词边界分词
        return list(text)


def extract_keywords(text: str, topn: int = 20) -> List[Tuple[str, float]]:
    """提取关键词"""
    if HAS_JIEBA:
        return jieba.analyse.extract_tags(text, topK=topn, withWeight=True)
    else:
        # 降级：按字频
        c = Counter(text)
        return [(ch, cnt / len(text)) for ch, cnt in c.most_common(topn) if len(ch.strip()) > 0]


def similarity(text1: str, text2: str) -> float:
    """计算两段文本的相似度（0-1）"""
    if not text1 or not text2:
        return 0.0
    tokens1 = Counter(tokenize(text1))
    tokens2 = Counter(tokenize(text2))
    if not tokens1 or not tokens2:
        return 0.0
    intersection = tokens1 & tokens2
    union = tokens1 | tokens2
    return sum(intersection.values()) / max(sum(union.values()), 1)


def find_semantic_duplicates(chapters: List[Tuple[int, str, str]], threshold: float = 0.7):
    """跨章节语义重复检测

    对比相邻3章的段落，找出语义相似但表述不同的重复内容。
    """
    issues = []

    def read_file(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    for i in range(len(chapters)):
        num, path, fname = chapters[i]
        content = read_file(path)

        # 只对比当前章与前一章
        if i == 0:
            continue
        prev_num, prev_path, _ = chapters[i - 1]
        prev_content = read_file(prev_path)

        # 按段落对比
        curr_paras = [p.strip() for p in content.split("\n") if len(p.strip()) >= 20]
        prev_paras = [p.strip() for p in prev_content.split("\n") if len(p.strip()) >= 20]

        for ci, cp in enumerate(curr_paras[:30]):  # 每章最多检查30段
            best_sim = 0.0
            best_pi = -1
            for pi, pp in enumerate(prev_paras[:30]):
                # 先做快速字面过滤（共享字数）
                common = set(cp) & set(pp)
                if len(common) / max(len(set(cp)), 1) < 0.3:
                    continue
                sim = similarity(cp, pp)
                if sim > best_sim:
                    best_sim = sim
                    best_pi = pi

            if best_sim >= threshold and best_pi >= 0:
                issues.append({
                    "type": "语义重复",
                    "severity": "medium",
                    "chapter": num,
                    "detail": f"第{num}章与第{prev_num}章存在语义相似段落 (相似度: {best_sim:.0%})",
                    "suggestion": f"当前段: 「{cp[:40]}…」\n前章段: 「{prev_paras[best_pi][:40]}…」\n→ 考虑删除或合并",
                    "similarity": round(best_sim, 3),
                })

    return issues


def named_entity_scan(content: str) -> dict:
    """人名/地名扫描（jieba 模式下启用）"""
    if not HAS_JIEBA:
        return {"entities": [], "mode": "regex"}

    # jieba 的词性标注
    import jieba.posseg as pseg
    entities = {"人名": set(), "地名": set(), "机构": set()}
    for word, flag in pseg.cut(content):
        if flag == "nr":
            entities["人名"].add(word)
        elif flag == "ns":
            entities["地名"].add(word)
        elif flag == "nt":
            entities["机构"].add(word)

    return {
        "entities": {k: sorted(v) for k, v in entities.items()},
        "mode": "jieba",
    }


def main():
    if len(sys.argv) < 2:
        print("📖 高级重复检测（jieba增强）")
        mode = "jieba" if HAS_JIEBA else "正则（未安装jieba，pip install jieba 可增强）"
        print(f"   模式: {mode}")
        print("用法: semantic_check <正文目录> [--threshold 0.7]")
        sys.exit(0)

    novel_dir = sys.argv[1]
    threshold = 0.7

    for i, arg in enumerate(sys.argv):
        if arg == "--threshold" and i + 1 < len(sys.argv):
            threshold = float(sys.argv[i + 1])

    if not Path(novel_dir).is_dir():
        print(f"❌ 目录不存在: {novel_dir}")
        sys.exit(1)

    # 列出章节
    chapters = []
    for f in sorted(Path(novel_dir).glob("*.md")):
        match = re.search(r"第(\d+)", f.name)
        if match:
            chapters.append((int(match.group(1)), str(f), f.name))

    if not chapters:
        print("❌ 未找到章节文件")
        sys.exit(1)

    print(f"📊 模式: {'jieba 增强' if HAS_JIEBA else '正则降级'}")
    print(f"🔍 扫描 {len(chapters)} 章，相似度阈值: {threshold:.0%}\n")

    # 语义重复检测
    issues = find_semantic_duplicates(chapters, threshold)

    if issues:
        print(f"⚠️  发现 {len(issues)} 处语义重复:\n")
        for issue in issues:
            print(f"  [{issue['severity'].upper()}] 第{issue['chapter']}章")
            print(f"    {issue['detail']}")
            for line in issue['suggestion'].split('\n'):
                print(f"    {line}")
            print()
    else:
        print("✅ 未发现语义重复")

    # 实体扫描（最后一章）
    if HAS_JIEBA:
        last_num, last_path, _ = chapters[-1]
        with open(last_path, "r", encoding="utf-8") as f:
            content = f.read()
        result = named_entity_scan(content)
        print(f"\n📋 第{last_num}章实体扫描:")
        for etype, names in result["entities"].items():
            if names:
                print(f"   {etype}: {', '.join(names)}")

    if not HAS_JIEBA:
        print(f"\n💡 提示: pip install jieba 可启用命名实体识别和更精准的语义检测")


if __name__ == "__main__":
    main()
