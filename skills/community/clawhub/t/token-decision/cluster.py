"""
Embedding 自动聚类 + 关键词自动更新 — v2.0
开发者：乙春
用法:
  python cluster.py              # 仅分析，显示当前聚类
  python cluster.py --update     # 分析并自动更新 token_eval.py 的 TASK_KEYWORDS
  python cluster.py --force      # 强制更新（即使低置信度）
"""
import sys
import sqlite3
import os
import re
from collections import Counter, defaultdict
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "benchmark.db")
SKILL_PATH = os.path.join(os.path.dirname(__file__), "token_eval.py")


def get_usage_prompts():
    """从 usage_log 获取所有用户 prompt"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, prompt, task_type FROM usage_log WHERE prompt IS NOT NULL ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return rows


def _load_current_keywords() -> dict:
    """从 token_eval.py 读取当前 TASK_KEYWORDS"""
    try:
        with open(SKILL_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        import ast
        # 找到 TASK_KEYWORDS = { ... }
        match = re.search(r"TASK_KEYWORDS\s*=\s*(\{.*?\n\})", content, re.DOTALL)
        if not match:
            return {}
        dict_str = match.group(1)
        dict_str = re.sub(r",\s*\}", "}", dict_str)
        dict_str = re.sub(r",\s*\]", "]", dict_str)
        return ast.literal_eval(dict_str)
    except Exception:
        return {}


def extract_candidate_keywords(prompts_by_task: dict, min_freq: int = 3) -> dict:
    """从各任务类型的 prompt 中提取高频候选关键词"""
    known_keywords = set()
    for kws in _load_current_keywords().values():
        known_keywords.update(kws)

    candidates = {}
    for task, prompts in prompts_by_task.items():
        word_freq = Counter()
        for prompt in prompts:
            words = re.findall(r'[\u4e00-\u9fff]{2,4}|\w{2,}', prompt)
            for w in words:
                w = w.strip()
                if w and w not in known_keywords and len(w) >= 2:
                    word_freq[w] += 1
        candidates[task] = [(w, c) for w, c in word_freq.most_common(20) if c >= min_freq]
    return candidates


def update_keywords(new_keywords: dict) -> bool:
    """自动更新 token_eval.py 中的 TASK_KEYWORDS"""
    try:
        with open(SKILL_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        current = _load_current_keywords()
        updated = {k: list(v) for k, v in current.items()}
        changes = 0
        for task, words in new_keywords.items():
            if task not in updated:
                updated[task] = []
            for word, count in words:
                if word not in updated[task]:
                    exists = any(word in kw or kw in word for kw in updated[task])
                    if not exists:
                        updated[task].append(word)
                        changes += 1

        if changes == 0:
            print("  ✅ 无新关键词需要添加")
            return False

        # 重建 TASK_KEYWORDS 段
        kw_start = content.find("TASK_KEYWORDS = {")
        if kw_start == -1:
            print("  ❌ 未找到 TASK_KEYWORDS 定义")
            return False

        # 找到结束的 }
        i = kw_start + len("TASK_KEYWORDS = ")
        while i < len(content) and content[i] != "{":
            i += 1
        i += 1  # skip {
        depth = 1
        while i < len(content) and depth > 0:
            if content[i] == "{":
                depth += 1
            elif content[i] == "}":
                depth -= 1
            i += 1

        prefix = content[:kw_start]
        suffix = content[i:]

        # 生成新 TASK_KEYWORDS
        kw_lines = ["TASK_KEYWORDS = {"]
        task_order = ["写作", "编程", "翻译", "分析", "知识问答", "总结摘要", "数学推理", "闲聊"]
        for task in task_order:
            if task in updated:
                words = sorted(set(updated[task]))
                formatted = []
                for j in range(0, len(words), 6):
                    chunk = words[j:j+6]
                    formatted.append('              ' + ', '.join(f'"{w}"' for w in chunk))
                kw_lines.append(f'    "{task}":   [')
                kw_lines.append(",\n".join(formatted) + "],")
        for task in sorted(updated):
            if task not in task_order:
                words = sorted(set(updated[task]))
                formatted = []
                for j in range(0, len(words), 6):
                    chunk = words[j:j+6]
                    formatted.append('              ' + ', '.join(f'"{w}"' for w in chunk))
                kw_lines.append(f'    "{task}":   [')
                kw_lines.append(",\n".join(formatted) + "],")
        kw_lines.append("}")

        new_content = prefix + "\n".join(kw_lines) + suffix
        with open(SKILL_PATH, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"  ✅ 已添加 {changes} 个新关键词到 {len(new_keywords)} 个任务类型")
        return True
    except Exception as e:
        print(f"  ❌ 更新失败: {e}")
        return False


def analyze_clusters():
    """分析使用日志，发现新任务簇"""
    rows = get_usage_prompts()
    if len(rows) < 5:
        print("\n⚠️  数据不足（<5条），继续积累使用数据")
        print("   每次用 /token决策 都会自动记录")
        return None, None

    task_counts = Counter(r[2] for r in rows)
    print(f"\n📊 已积累 {len(rows)} 条 prompt")
    print(f"\n{'任务类型':<10} {'数量':>5} {'占比':>6}")
    print("-" * 25)
    for task, count in task_counts.most_common():
        pct = count / len(rows) * 100
        bar = "█" * int(pct / 5)
        print(f"{task:<10} {count:>5} {pct:>5.1f}% {bar}")

    prompts_by_task = defaultdict(list)
    for _, prompt, task in rows:
        prompts_by_task[task].append(prompt)

    min_freq = max(2, len(rows) // 10)
    candidates = extract_candidate_keywords(prompts_by_task, min_freq=min_freq)
    print(f"\n🔍 候选新关键词（频次≥{min_freq}）:")
    found = False
    for task, words in candidates.items():
        if words:
            found = True
            print(f"\n  [{task}]:")
            for w, c in words[:10]:
                print(f"     {w}: {c}次")
    if not found:
        print("  （暂无显著新词，继续积累）")

    print(f"\n📋 建议:")
    chat_pct = task_counts.get("闲聊", 0) / len(rows) * 100
    unknown_pct = task_counts.get("未知", 0) / len(rows) * 100
    if unknown_pct > 20:
        print(f"   ⚠️  未知分类占比 {unknown_pct:.0f}%，需要改进关键词或增加新任务类型")
    elif chat_pct > 30:
        print(f"   ⚠️  闲聊占比 {chat_pct:.0f}%，可能有 prompt 被误分类")
    elif len(task_counts) < 3:
        print("   📝 任务类型单一，鼓励多样使用")
    else:
        print("   ✅ 分类分布健康")

    return task_counts, candidates


if __name__ == "__main__":
    do_update = "--update" in sys.argv or "--force" in sys.argv
    do_force = "--force" in sys.argv

    task_counts, candidates = analyze_clusters()

    if do_update and candidates:
        high_conf = {}
        for task, words in candidates.items():
            filtered = [(w, c) for w, c in words if c >= 3 or do_force]
            if filtered:
                high_conf[task] = filtered

        if high_conf:
            print(f"\n🔄 自动更新 TASK_KEYWORDS...")
            update_keywords(high_conf)
        else:
            print(f"\n📝 无高频候选关键词（频次<3），跳过更新")
            print("   使用 --force 强制更新低频关键词")
    elif do_update:
        print("\n📝 无候选关键词，跳过更新")
