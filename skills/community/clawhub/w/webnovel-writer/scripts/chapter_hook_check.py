#!/usr/bin/env python3
"""
章末钩子检测脚本 v2.2.1
扫描正文目录，检测每章最后200字是否有有效钩子，评估钩子强度和类型

用法：
  python3 chapter_hook_check.py --novel-dir <正文目录>
  python3 chapter_hook_check.py --novel-dir <正文目录> --suggest
  python3 chapter_hook_check.py --novel-dir <正文目录> --format json

检查项：
  1. 钩子类型识别（悬念/情感/反转/危机/秘密/决定/无钩子）
  2. 钩子强度评分（0-10）
  3. 连续弱结尾检测（节奏疲劳）
  4. --suggest：改善建议
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple

# ============================================================
# 常量定义
# ============================================================

VERSION = "v2.2.1"

# 钩子类型关键词映射
HOOK_PATTERNS: Dict[str, Dict[str, Any]] = {
    "悬念钩子": {
        "keywords": ["？", "?", "什么", "为什么", "怎么回事", "到底", "难道", "究竟",
                      "谁", "怎么会", "怎么可能", "不知道", "猜不透", "看不透",
                      "答案", "秘密", "谜", "真相", "背后"],
        "patterns": [
            r"[^。！？\n]*[？?][^。！？\n]*$",  # 以问句结尾
            r"到底[^。！？]*[？?]",
            r"难道[^。！？]*[？?]",
            r"他(还)?不知道",
            r"一切才刚刚开始",
        ],
        "base_score": 6,
    },
    "情感钩子": {
        "keywords": ["泪", "哭", "笑", "颤抖", "心碎", "崩溃", "窒息", "绝望",
                      "痛", "心酸", "红了眼眶", "沉默", "良久", "叹息", "苦笑",
                      "后悔", "愧疚", "感动", "温暖", "冰冷", "心如刀割",
                      "再也", "再也回不去", "再也见不到"],
        "patterns": [
            r"(泪水|眼泪|红了眼眶|心碎|崩溃|心如刀割)",
            r"(沉默|良久)([^。！？]*$)",
            r"(苦笑|叹息)",
        ],
        "base_score": 5,
    },
    "反转钩子": {
        "keywords": ["但", "可是", "然而", "竟然", "居然", "没想到", "出乎意料",
                      "不对", "等等", "不可能", "怎么会这样", "完全没想到",
                      "大吃一惊", "震惊", "瞪大眼睛", "愣住", "傻了"],
        "patterns": [
            r"(但|可是|然而|不过)[^。！？]*(竟然|居然|没想到|不可能)",
            r"(不对|等等|不可能)[^。！？]*$",
            r"完全[^。！？]*意外",
        ],
        "base_score": 7,
    },
    "危机钩子": {
        "keywords": ["危险", "死", "杀", "塌", "炸", "碎", "断", "裂", "崩",
                      "逼", "逼到", "绝路", "走投无路", "倒计时", "来不及了",
                      "来不及", "完了", "糟了", "出事了", "出大问题了",
                      "黑暗", "阴影", "逼近", "靠近", "威胁"],
        "patterns": [
            r"(来不及|完了|糟了|出事了)",
            r"(死|杀|危险|威胁)[^。！？]*$",
            r"(逼近|靠近|逼近)",
        ],
        "base_score": 7,
    },
    "秘密钩子": {
        "keywords": ["秘密", "隐藏", "背后", "另有隐情", "真相", "不为人知",
                      "隐瞒", "掩盖", "从未", "一直", "其实", "原来",
                      "不简单", "没那么简单", "暗藏", "另有"],
        "patterns": [
            r"(秘密|隐情|真相|隐藏)[^。！？]*$",
            r"(其实|原来|一直)[^。！？]*(瞒|隐瞒|没说|不说)",
            r"(不简单|没那么简单)",
        ],
        "base_score": 6,
    },
    "决定钩子": {
        "keywords": ["必须", "一定", "决定", "下定决心", "非...不可", "不能",
                      "该", "要么", "只有", "唯一的", "最后的机会",
                      "是时候", "该做了", "不能再拖", "别无选择"],
        "patterns": [
            r"(必须|一定|决定|下定决心)[^。！？]*$",
            r"(是时候|别无选择|只有[^。！？]*才)",
            r"(要么[^。！？]*要么)",
        ],
        "base_score": 5,
    },
}

# 额外加分的句式模式
STRONG_ENDING_PATTERNS = [
    (r"[^。！？]*[——…]+[^。！？]*$", 2, "破折号/省略号结尾，留白感强"),
    (r"[^。！？]*[？?]\s*$", 1, "问句结尾，引发好奇"),
    (r"(突然|忽然|猛地|刹那|一瞬间)", 1, "突发感"),
    (r"(他|她|它|这|那)(还|却|竟|才|就)(没|不|要|会|能)", 1, "转折语气"),
    (r"[^\u4e00-\u9fff\w]\s*$", -1, "非中文字符结尾（可能是格式问题）"),
]

# ============================================================
# 工具函数
# ============================================================

def read_file(path: str) -> str:
    """读取文件内容"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"[警告] 无法读取 {path}: {e}")
        return ""


def list_chapters(dir_path: str) -> List[Tuple[int, str, str]]:
    """列出章节文件，返回 [(章节号, 路径, 文件名)]"""
    if not os.path.isdir(dir_path):
        print(f"[错误] 正文目录不存在: {dir_path}")
        return []
    chapters = []
    for f in sorted(os.listdir(dir_path)):
        if f.endswith('.md') or f.endswith('.txt'):
            match = re.search(r'第(\d+)章', f)
            if match:
                num = int(match.group(1))
                chapters.append((num, os.path.join(dir_path, f), f))
    chapters.sort(key=lambda x: x[0])
    return chapters


def extract_ending(content: str, char_count: int = 200) -> str:
    """提取正文最后N个字符"""
    # 去掉标题行
    lines = content.strip().split('\n')
    body_lines = [l for l in lines if not l.strip().startswith('#')]
    body = '\n'.join(body_lines)
    # 只取中文字符范围
    return body[-char_count:] if len(body) > char_count else body


# ============================================================
# 钩子检测核心逻辑
# ============================================================

def detect_hook_type(ending: str) -> Tuple[str, float, List[str]]:
    """
    检测章末钩子类型和强度。
    
    Args:
        ending: 章节最后200字文本
        
    Returns:
        (钩子类型, 强度评分0-10, 匹配到的关键词列表)
    """
    if not ending or len(ending.strip()) < 10:
        return ("无钩子", 1.0, [])
    
    scores: Dict[str, float] = {}
    matched_details: Dict[str, List[str]] = {}
    
    for hook_type, config in HOOK_PATTERNS.items():
        score = 0.0
        matched = []
        
        # 关键词匹配
        for kw in config["keywords"]:
            count = ending.count(kw)
            if count > 0:
                score += min(count * 0.8, 3.0)  # 每个关键词+0.8，上限3分
                matched.append(kw)
        
        # 正则模式匹配
        for pattern in config["patterns"]:
            if re.search(pattern, ending):
                score += 1.5
                matched.append(f"模式:{pattern[:20]}")
        
        scores[hook_type] = score + config["base_score"] if score > 0 else 0
        matched_details[hook_type] = matched
    
    # 附加句式加分
    bonus = 0.0
    for pattern, add_score, _ in STRONG_ENDING_PATTERNS:
        if re.search(pattern, ending):
            bonus += add_score
    
    # 找得分最高的类型
    best_type = "无钩子"
    best_score = 2.0  # 无钩子基础分
    best_matched = []
    
    for hook_type, score in scores.items():
        final_score = score + bonus
        if final_score > best_score:
            best_score = final_score
            best_type = hook_type
            best_matched = matched_details[hook_type]
    
    # 限制在0-10范围
    best_score = max(0.0, min(10.0, best_score))
    
    return (best_type, round(best_score, 1), best_matched)


def check_consecutive_weak(chapter_results: List[Dict[str, Any]], threshold: float = 4.0) -> List[Dict[str, Any]]:
    """
    检测连续弱结尾（节奏疲劳）。
    
    Args:
        chapter_results: 每章的检测结果列表
        threshold: 弱钩子阈值
        
    Returns:
        节奏疲劳警告列表
    """
    warnings = []
    streak = 0
    streak_start = None
    
    for i, r in enumerate(chapter_results):
        if r["score"] < threshold:
            if streak == 0:
                streak_start = r["chapter"]
            streak += 1
        else:
            if streak >= 3:
                end_chapter = chapter_results[i - 1]["chapter"]
                warnings.append({
                    "type": "节奏疲劳",
                    "severity": "high" if streak >= 5 else "medium",
                    "detail": f"第{streak_start}-{end_chapter}章连续{streak}章钩子评分低于{threshold}，"
                              f"读者可能失去翻页动力",
                    "suggestion": _fatigue_suggestion(streak),
                })
            streak = 0
            streak_start = None
    
    # 尾部处理
    if streak >= 3 and chapter_results:
        end_chapter = chapter_results[-1]["chapter"]
        warnings.append({
            "type": "节奏疲劳",
            "severity": "high" if streak >= 5 else "medium",
            "detail": f"第{streak_start}-{end_chapter}章连续{streak}章钩子评分低于{threshold}，"
                      f"读者可能失去翻页动力",
            "suggestion": _fatigue_suggestion(streak),
        })
    
    return warnings


def _fatigue_suggestion(streak: int) -> str:
    """生成节奏疲劳的改善建议"""
    suggestions = [
        "在平淡结尾处插入突发转折（电话响起、门外脚步、意外来客）",
        "添加悬念元素（未回答的问题、神秘暗示、角色反常行为）",
        "制造情绪冲击（意外告白、真相揭露、生死危机）",
        "以角色内心独白结尾，暗示即将做出的重大决定",
    ]
    return "建议穿插使用以下手法打破平淡：" + "；".join(suggestions[:min(3, streak)])


def generate_hook_suggestion(ending: str, hook_type: str, score: float) -> Optional[str]:
    """
    生成章末钩子改善建议。
    
    Args:
        ending: 章节最后200字
        hook_type: 检测到的钩子类型
        score: 钩子强度评分
        
    Returns:
        改善建议字符串，评分为7+时返回None
    """
    if score >= 7:
        return None
    
    suggestions_map = {
        "无钩子": [
            "结尾过于平淡。尝试以问句、省略号、突发动作、角色内心独白结尾",
            "示例：他转身要走，却发现门把手上沾着血。",
            "示例：手机亮了。一条陌生号码的消息：我知道你做了什么。",
        ],
        "悬念钩子": [
            "悬念已建立但强度不够。尝试更具体化——把模糊的疑问变成迫在眉睫的威胁",
            "或用角色视角强化紧迫感：他意识到自己只剩24小时了。",
        ],
        "情感钩子": [
            "情感冲击可以更强。用具体行为代替抽象描述",
            "示例：她把照片翻过去，发现背面有行字。字迹是她的，但她完全不记得写过。",
        ],
        "反转钩子": [
            "反转信号弱。尝试在最后一句话加入与前面所有信息矛盾的新信息",
            "示例：一切都解释得通了——除了那枚不属于任何人的戒指。",
        ],
        "危机钩子": [
            "危机感不够紧迫。加倒计时或身体反应（冷汗、心跳加速）",
            "示例：倒计时还剩三分钟，而他还不知道炸弹在哪。",
        ],
        "秘密钩子": [
            "秘密暗示太模糊。给读者一个更具体的线索片段",
            "示例：文件最后一页被人撕掉了。撕得很急，纸边还是锯齿形的。",
        ],
        "决定钩子": [
            "决定感不够强烈。强化两难困境的矛盾性",
            "示例：左边是来时的路，右边是他发誓再也不会踏足的地方。他迈出了步子。",
        ],
    }
    
    lines = suggestions_map.get(hook_type, ["尝试在结尾添加更强的悬念或情感冲击"])
    return "\n".join(lines)


# ============================================================
# 主流程
# ============================================================

def check_single_chapter(chapter_num: int, content: str, char_count: int = 200) -> Dict[str, Any]:
    """
    检查单章的章末钩子。
    
    Args:
        chapter_num: 章节号
        content: 章节全文
        char_count: 提取最后N个字符
        
    Returns:
        检测结果字典
    """
    ending = extract_ending(content, char_count)
    hook_type, score, matched = detect_hook_type(ending)
    
    # 确定严重程度
    if score < 4:
        severity = "high"
    elif score < 6:
        severity = "medium"
    else:
        severity = "low"
    
    return {
        "chapter": chapter_num,
        "hook_type": hook_type,
        "score": score,
        "severity": severity,
        "ending_preview": ending[-80:] if len(ending) > 80 else ending,
        "matched_keywords": matched,
    }


def run_check(novel_dir: str, threshold: float = 4.0, suggest: bool = False) -> Dict[str, Any]:
    """
    执行章末钩子检测。
    
    Args:
        novel_dir: 正文目录路径
        threshold: 弱钩子阈值
        suggest: 是否输出改善建议
        
    Returns:
        检测结果汇总
    """
    print("=" * 60)
    print(f"🪝 章末钩子检测 {VERSION}")
    print("=" * 60)
    
    chapters = list_chapters(novel_dir)
    if not chapters:
        print("[错误] 未找到章节文件")
        return {"error": "未找到章节文件", "chapters": [], "warnings": []}
    
    print(f"\n📖 找到 {len(chapters)} 个章节（第{chapters[0][0]}章 ~ 第{chapters[-1][0]}章）")
    
    # 逐章检测
    chapter_results = []
    for num, path, fname in chapters:
        content = read_file(path)
        result = check_single_chapter(num, content)
        chapter_results.append(result)
    
    # 连续弱结尾检测
    fatigue_warnings = check_consecutive_weak(chapter_results, threshold)
    
    # 统计
    type_dist = defaultdict(int)
    score_sum = 0.0
    weak_count = 0
    for r in chapter_results:
        type_dist[r["hook_type"]] += 1
        score_sum += r["score"]
        if r["score"] < threshold:
            weak_count += 1
    
    avg_score = score_sum / len(chapter_results) if chapter_results else 0
    
    # 输出结果
    print(f"\n{'='*60}")
    print(f"📊 检测结果")
    print(f"{'='*60}")
    print(f"\n总章数: {len(chapters)} | 平均钩子评分: {avg_score:.1f} | 弱结尾(<{threshold}分): {weak_count}章")
    print(f"类型分布: {', '.join(f'{t}×{c}' for t, c in sorted(type_dist.items(), key=lambda x: -x[1]))}")
    
    # 逐章输出
    print(f"\n{'章节':>6} | {'类型':<8} | {'评分':>4} | 预览")
    print("-" * 70)
    for r in chapter_results:
        emoji = "🔴" if r["score"] < threshold else ("🟡" if r["score"] < 6 else "🟢")
        preview = r["ending_preview"].replace("\n", " ")[:40]
        print(f"第{r['chapter']:>3}章 | {r['hook_type']:<8} | {emoji}{r['score']:>4.1f} | {preview}...")
        if suggest and r["score"] < 7:
            suggestion = generate_hook_suggestion(r["ending_preview"], r["hook_type"], r["score"])
            if suggestion:
                for line in suggestion.split("\n"):
                    print(f"       💡 {line}")
    
    # 节奏疲劳警告
    if fatigue_warnings:
        print(f"\n⚠️  节奏疲劳警告：")
        for w in fatigue_warnings:
            emoji = "🔴" if w["severity"] == "high" else "🟡"
            print(f"  {emoji} {w['detail']}")
            if suggest:
                print(f"     💡 {w['suggestion']}")
    else:
        print(f"\n✅ 未检测到连续弱结尾")
    
    result = {
        "version": VERSION,
        "total_chapters": len(chapters),
        "average_score": round(avg_score, 1),
        "weak_count": weak_count,
        "type_distribution": dict(type_dist),
        "chapters": chapter_results,
        "fatigue_warnings": fatigue_warnings,
    }
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description="章末钩子检测脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--novel-dir", required=True, help="正文目录路径")
    parser.add_argument("--threshold", type=float, default=4.0, help="弱钩子评分阈值（默认4）")
    parser.add_argument("--suggest", action="store_true", help="输出改善建议")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="输出格式")
    parser.add_argument("--version", action="version", version=f"chapter_hook_check {VERSION}")
    
    args = parser.parse_args()
    
    result = run_check(args.novel_dir, args.threshold, args.suggest)
    
    if args.format == "json":
        # JSON输出时移除内部字段
        print("\n" + json.dumps(result, ensure_ascii=False, indent=2))
    elif "error" not in result:
        # 保存JSON报告
        report_dir = os.path.dirname(args.novel_dir.rstrip('/'))
        report_path = os.path.join(report_dir, "chapter_hook_report.json")
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"\n📄 报告已保存至: {report_path}")
        except Exception as e:
            print(f"\n[警告] 保存报告失败: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 chapter_hook_check.py --novel-dir <正文目录> [--threshold 4] [--suggest] [--format text|json]")
        sys.exit(1)
    main()
