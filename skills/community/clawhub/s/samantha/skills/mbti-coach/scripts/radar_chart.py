#!/usr/bin/env python3
"""
MBTI 八维认知功能雷达图
生成当前状态 vs 目标状态的对比图
"""
import json
import math
import sys
import os

def load_profile(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# 16种类型的"理想"功能分数（主导100, 辅助75, 第三50, 劣势25, 其余10）
TYPE_STACKS = {
    "ISTJ": {"Si":100,"Te":75,"Fi":50,"Ne":25,"Se":10,"Ti":10,"Fe":10,"Ni":10},
    "ISFJ": {"Si":100,"Fe":75,"Ti":50,"Ne":25,"Se":10,"Te":10,"Fi":10,"Ni":10},
    "INFJ": {"Ni":100,"Fe":75,"Ti":50,"Se":25,"Si":10,"Te":10,"Fi":10,"Ne":10},
    "INTJ": {"Ni":100,"Te":75,"Fi":50,"Se":25,"Si":10,"Ti":10,"Fe":10,"Ne":10},
    "ISTP": {"Ti":100,"Se":75,"Ni":50,"Fe":25,"Si":10,"Te":10,"Fi":10,"Ne":10},
    "ISFP": {"Fi":100,"Se":75,"Ni":50,"Te":25,"Si":10,"Ti":10,"Fe":10,"Ne":10},
    "INFP": {"Fi":100,"Ne":75,"Si":50,"Te":25,"Se":10,"Ti":10,"Fe":10,"Ni":10},
    "INTP": {"Ti":100,"Ne":75,"Si":50,"Fe":25,"Se":10,"Te":10,"Fi":10,"Ni":10},
    "ESTP": {"Se":100,"Ti":75,"Fe":50,"Ni":25,"Si":10,"Te":10,"Fi":10,"Ne":10},
    "ESFP": {"Se":100,"Fi":75,"Ti":50,"Ni":25,"Si":10,"Te":10,"Fe":10,"Ne":10},
    "ENFP": {"Ne":100,"Fi":75,"Te":50,"Si":25,"Se":10,"Ti":10,"Fe":10,"Ni":10},
    "ENTP": {"Ne":100,"Ti":75,"Fe":50,"Si":25,"Se":10,"Te":10,"Fi":10,"Ni":10},
    "ESTJ": {"Te":100,"Si":75,"Ne":50,"Fi":25,"Se":10,"Ti":10,"Fe":10,"Ni":10},
    "ESFJ": {"Fe":100,"Si":75,"Ne":50,"Ti":25,"Se":10,"Te":10,"Fi":10,"Ni":10},
    "ENFJ": {"Fe":100,"Ni":75,"Se":50,"Ti":25,"Si":10,"Te":10,"Fi":10,"Ne":10},
    "ENTJ": {"Te":100,"Ni":75,"Se":50,"Fi":25,"Si":10,"Ti":10,"Fe":10,"Ne":10},
}

FUNCTIONS = ["Te","Ti","Fe","Fi","Se","Si","Ne","Ni"]
FUNC_CN = {
    "Te":"外向思维","Ti":"内向思维","Fe":"外向情感","Fi":"内向情感",
    "Se":"外向感觉","Si":"内向感觉","Ne":"外向直觉","Ni":"内向直觉"
}

def get_current_scores(profile):
    """从 profile 中获取当前分数，缺失的补10"""
    cf = profile.get("cognitive_functions", {})
    scores = {}
    for fn in FUNCTIONS:
        if fn in cf:
            scores[fn] = cf[fn]["score"] if isinstance(cf[fn], dict) else cf[fn]
        else:
            scores[fn] = 10
    return scores

def get_target_scores(target_type):
    """获取目标类型的理想分数"""
    return TYPE_STACKS.get(target_type, {fn: 50 for fn in FUNCTIONS})

def generate_radar_chart(current_scores, target_scores, current_type, target_type, output_path):
    """用 matplotlib 生成雷达图"""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import matplotlib.font_manager as fm
        import numpy as np
    except ImportError:
        print("错误：需要安装 matplotlib。运行：pip install matplotlib numpy", file=sys.stderr)
        sys.exit(1)

    # 尝试使用中文字体
    for font_name in ['Microsoft YaHei', 'SimHei', 'PingFang SC', 'Noto Sans CJK SC', 'Arial Unicode MS']:
        if any(font_name.lower() in f.name.lower() for f in fm.fontManager.ttflist):
            plt.rcParams['font.sans-serif'] = [font_name]
            break
    plt.rcParams['axes.unicode_minus'] = False

    N = len(FUNCTIONS)
    angles = [n / float(N) * 2 * math.pi for n in range(N)]
    angles += angles[:1]  # 闭合

    current_vals = [current_scores[fn] for fn in FUNCTIONS] + [current_scores[FUNCTIONS[0]]]
    target_vals = [target_scores[fn] for fn in FUNCTIONS] + [target_scores[FUNCTIONS[0]]]

    labels = [f"{fn}\n{FUNC_CN[fn]}" for fn in FUNCTIONS]

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    # 目标（虚线，蓝色填充）
    ax.plot(angles, target_vals, 'o--', linewidth=2, color='#2563eb', label=f'目标: {target_type}')
    ax.fill(angles, target_vals, alpha=0.08, color='#2563eb')

    # 当前（实线，红色填充）
    ax.plot(angles, current_vals, 'o-', linewidth=2.5, color='#dc2626', label=f'当前: {current_type or "你"}')
    ax.fill(angles, current_vals, alpha=0.18, color='#dc2626')

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, size=11, color='#333333')
    ax.set_ylim(0, 105)
    ax.set_yticks([25, 50, 75, 100])
    ax.set_yticklabels(['25', '50', '75', '100'], size=8, color='#666666')
    ax.tick_params(colors='#666666')
    ax.spines['polar'].set_color('#cccccc')
    ax.grid(color='#dddddd', linewidth=0.5)

    # 在每个点旁标注差值
    for i, fn in enumerate(FUNCTIONS):
        diff = target_scores[fn] - current_scores[fn]
        if abs(diff) >= 10:
            color = '#dc2626' if diff > 0 else '#16a34a'
            sign = '+' if diff > 0 else ''
            r = max(current_scores[fn], target_scores[fn]) + 8
            ax.annotate(f'{sign}{diff}', xy=(angles[i], r),
                       fontsize=9, fontweight='bold', color=color,
                       ha='center', va='center')

    legend = ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1.1),
                      fontsize=12, facecolor='white', edgecolor='#cccccc',
                      labelcolor='#333333')

    title = f'MBTI 八维认知功能对比'
    if current_type:
        title += f'\n{current_type} → {target_type}'
    ax.set_title(title, size=16, color='#222222', pad=30, fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"图表已保存：{output_path}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, '..', 'data')
    profile_path = os.path.join(data_dir, 'profile.json')

    if not os.path.exists(profile_path):
        print("错误：未找到 profile.json，请先完成初始设置", file=sys.stderr)
        sys.exit(1)

    profile = load_profile(profile_path)
    current_type = profile.get("current_type", "")
    target_type = profile.get("target_type", "")

    if not target_type:
        print("错误：未设置目标类型", file=sys.stderr)
        sys.exit(1)

    current_scores = get_current_scores(profile)
    target_scores = get_target_scores(target_type)

    output_path = os.path.join(data_dir, 'radar_chart.png')
    generate_radar_chart(current_scores, target_scores, current_type, target_type, output_path)

    # 输出差距分析文本
    print("\n八维功能差距分析：")
    print(f"{'功能':<6} {'当前':>4} {'目标':>4} {'差距':>6}")
    print("-" * 24)
    gaps = []
    for fn in FUNCTIONS:
        c = current_scores[fn]
        t = target_scores[fn]
        diff = t - c
        marker = " !!!" if diff >= 40 else (" !" if diff >= 20 else "")
        print(f"{fn:<6} {c:>4} {t:>4} {diff:>+6}{marker}")
        if diff > 0:
            gaps.append((fn, diff))

    gaps.sort(key=lambda x: -x[1])
    if gaps:
        print(f"\n最需要发展的功能：")
        for fn, diff in gaps[:3]:
            print(f"  {fn}（{FUNC_CN[fn]}）：差距 {diff} 分")

if __name__ == "__main__":
    main()
