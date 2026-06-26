#!/usr/bin/env python3
"""
章节标题质量检查脚本 v2.2.1
扫描正文目录的文件名，检测章节标题质量

用法：
  python3 chapter_title_check.py --novel-dir <正文目录>

检查项：
  1. 标题长度（最佳8-20字）
  2. 标题吸引力（平淡型/标题党/信息过量）
  3. 标题格式一致性（第X章格式、数字统一）
  4. 钩子检测（悬念词）
"""

import os
import re
import json
import argparse
from pathlib import Path
from collections import Counter
from typing import Any, Dict, List, Optional, Tuple

VERSION = 'v2.2.1'

# ============================================================
# 常量定义
# ============================================================

# 平淡型标题关键词
FLAT_PATTERNS = [
    r'^第\d+章$',           # 只有"第X章"无标题
    r'^今天$', r'^昨天$', r'^明天$',
    r'^早上$', r'^中午$', r'^下午$', r'^晚上$', r'^深夜$',
    r'^第二天$', r'^第三天$',
    r'^开始$', r'^结束$', r'^结局$', r'^尾声$',
    r'^新的.*$', r'^继续$',
    r'^第\d+天$',            # "第X天"直接做标题
]

# 标题党关键词（过度使用扣分）
CLICKBAIT_WORDS = ['震惊', '竟然', '意想不到', '万万没想到', '不敢相信',
                   '所有人都', '99%的人', '绝对', '史上最']

# 悬念/钩子词
HOOK_WORDS = ['秘密', '真相', '阴谋', '命运', '背叛', '陷阱', '危机',
              '抉择', '代价', '代价', '预言', '诅咒', '禁忌', '谜团',
              '隐藏', '线索', '反转', '悬念', '暗流', '杀机', '伏笔',
              '意外', '变故', '风暴', '深渊', '迷雾', '陷阱', '暗算']

# 透露结局/信息过多的关键词
SPOILER_WORDS = ['死了', '结局', '最终', '终于', '成功', '失败',
                 '胜利', '沦陷', '覆灭', '身亡', '复活']


# ============================================================
# 工具函数
# ============================================================

def list_chapter_files(novel_dir: str) -> List[Tuple[int, str]]:
    """列出章节文件，返回 [(章节号, 文件名), ...]
    
    只处理 .md 和 .txt 文件，按章节号排序。
    """
    if not os.path.isdir(novel_dir):
        print(f"[错误] 目录不存在: {novel_dir}")
        return []
    
    chapters = []
    for fname in sorted(os.listdir(novel_dir)):
        if not (fname.endswith('.md') or fname.endswith('.txt')):
            continue
        match = re.search(r'第(\d+)章', fname)
        if match:
            num = int(match.group(1))
            chapters.append((num, fname))
    chapters.sort(key=lambda x: x[0])
    return chapters


def extract_title(fname: str) -> str:
    """从文件名提取标题部分（去掉'第X章'前缀和扩展名）"""
    # 去掉扩展名
    name = os.path.splitext(fname)[0]
    # 去掉"第X章"前缀及分隔符
    title = re.sub(r'^第\d+章[\s_\-—]*', '', name).strip()
    return title


def title_char_count(title: str) -> int:
    """统计标题中的中文字符数"""
    return len(re.findall(r'[\u4e00-\u9fff]', title))


# ============================================================
# 检查函数
# ============================================================

def check_title_length(title: str, num: int, min_len: int = 5, max_len: int = 25) -> List[Dict[str, Any]]:
    """检查标题长度"""
    issues = []
    char_count = title_char_count(title)
    
    if not title:
        issues.append({
            'type': '无标题',
            'severity': 'high',
            'chapter': num,
            'detail': f'第{num}章没有标题（只有章节号）',
            'suggestion': '添加有信息量的标题，8-20字最佳'
        })
    elif char_count < min_len:
        issues.append({
            'type': '标题过短',
            'severity': 'medium',
            'chapter': num,
            'detail': f'第{num}章标题「{title}」仅{char_count}字，可能太笼统',
            'suggestion': '补充信息量，8-20字最佳'
        })
    elif char_count > max_len:
        issues.append({
            'type': '标题过长',
            'severity': 'medium',
            'chapter': num,
            'detail': f'第{num}章标题「{title}」有{char_count}字，可能太啰嗦',
            'suggestion': '精简标题，8-20字最佳'
        })
    
    return issues


def check_title_attractiveness(title: str, num: int) -> List[Dict[str, Any]]:
    """检查标题吸引力"""
    issues = []
    if not title:
        return issues
    
    # 平淡型标题
    for pattern in FLAT_PATTERNS:
        if re.match(pattern, title):
            issues.append({
                'type': '平淡标题',
                'severity': 'high',
                'chapter': num,
                'detail': f'第{num}章标题「{title}」过于平淡，缺乏吸引力',
                'suggestion': '用具体事件或悬念替代时间/状态描述'
            })
            break
    
    # 标题党检测
    clickbait_hits = [w for w in CLICKBAIT_WORDS if w in title]
    if len(clickbait_hits) >= 2:
        issues.append({
            'type': '标题党',
            'severity': 'medium',
            'chapter': num,
            'detail': f'第{num}章标题「{title}」含{len(clickbait_hits)}个标题党词：{"、".join(clickbait_hits)}',
            'suggestion': '适度悬念可以，过度标题党会降低信任'
        })
    
    # 信息过量（透露结局）
    spoiler_hits = [w for w in SPOILER_WORDS if w in title]
    if spoiler_hits:
        issues.append({
            'type': '信息过量',
            'severity': 'medium',
            'chapter': num,
            'detail': f'第{num}章标题「{title}」可能透露剧情：{"、".join(spoiler_hits)}',
            'suggestion': '标题应引发好奇而非给出答案'
        })
    
    return issues


def check_format_consistency(filenames: List[Tuple[int, str]]) -> List[Dict[str, Any]]:
    """检查标题格式一致性"""
    issues = []
    if len(filenames) < 2:
        return issues
    
    formats = []  # 收集每章的格式特征
    for num, fname in filenames:
        fmt = {
            'num': num,
            'fname': fname,
            'has_prefix': bool(re.match(r'^第\d+章', fname)),
            'separator': '',  # 分隔符类型
            'number_padded': False,  # 数字是否补零
        }
        
        # 检测分隔符
        sep_match = re.match(r'^第\d+章([_\s\-—])', fname)
        if sep_match:
            fmt['separator'] = sep_match.group(1)
        
        # 检测数字补零
        num_match = re.match(r'^第(0*)(\d+)章', fname)
        if num_match and num_match.group(1):
            fmt['number_padded'] = True
        
        formats.append(fmt)
    
    # 检查分隔符一致性
    separators = [f['separator'] for f in formats if f['separator']]
    if separators:
        sep_counter = Counter(separators)
        main_sep = sep_counter.most_common(1)[0][0]
        inconsistent = [f for f in formats if f['separator'] and f['separator'] != main_sep]
        if inconsistent:
            for f in inconsistent:
                issues.append({
                    'type': '格式不统一',
                    'severity': 'low',
                    'chapter': f['num'],
                    'detail': f'第{f["num"]}章文件名分隔符为「{f["separator"]}」，与主流「{main_sep}」不一致',
                    'suggestion': f'统一使用「{main_sep}」作为分隔符'
                })
    
    # 检查数字补零一致性
    padded_count = sum(1 for f in formats if f['number_padded'])
    if 0 < padded_count < len(formats):
        issues.append({
            'type': '编号格式不统一',
            'severity': 'low',
            'chapter': 0,
            'detail': f'部分章节编号补零（{padded_count}个），部分未补零（{len(formats)-padded_count}个）',
            'suggestion': '统一编号格式，建议三位数补零（第001章）'
        })
    
    # 检查中英文混搭
    for num, fname in filenames:
        # 检查文件名中是否有不合理的英文（排除常见扩展名前的内容）
        name_part = os.path.splitext(fname)[0]
        english_parts = re.findall(r'[a-zA-Z]+', name_part)
        # 过滤掉合理的英文（如draft、WIP等标记）
        allowed = {'draft', 'wip', 'DRAFT', 'WIP', 'v'}
        suspicious = [e for e in english_parts if e not in allowed and len(e) > 1]
        if suspicious:
            issues.append({
                'type': '中英混搭',
                'severity': 'low',
                'chapter': num,
                'detail': f'第{num}章文件名含英文：{"、".join(suspicious)}',
                'suggestion': '文件名建议纯中文+数字'
            })
    
    return issues


def check_hooks(title: str, num: int) -> List[Dict[str, Any]]:
    """检查标题是否带有钩子/悬念"""
    issues = []
    if not title:
        return issues
    
    hook_hits = [w for w in HOOK_WORDS if w in title]
    if not hook_hits:
        # 没有任何悬念词，标记为缺少钩子（但不一定有问题）
        # 仅当标题较长（>6字）且无钩子时才提示
        if title_char_count(title) > 6:
            issues.append({
                'type': '缺少钩子',
                'severity': 'low',
                'chapter': num,
                'detail': f'第{num}章标题「{title}」无悬念词，可能难以引发读者好奇',
                'suggestion': f'考虑加入悬念元素，如：{", ".join(HOOK_WORDS[:5])}等'
            })
    
    return issues


# ============================================================
# 生成建议
# ============================================================

def generate_suggestion(title: str, num: int, issues: List[Dict[str, Any]]) -> str:
    """根据问题生成综合修改建议"""
    if not issues:
        return f'第{num}章标题「{title}」质量良好 ✓'
    
    suggestions = []
    for issue in issues:
        suggestions.append(f'  · [{issue["type"]}] {issue.get("suggestion", "")}')
    
    return f'第{num}章标题「{title}」\n' + '\n'.join(suggestions)


# ============================================================
# 主流程
# ============================================================

def run_check(novel_dir: str, min_len: int = 5, max_len: int = 25,
              suggest: bool = False, output_format: str = 'text') -> Dict[str, Any]:
    """执行章节标题质量检查
    
    Args:
        novel_dir: 章节目录路径
        min_len: 最短标题字数
        max_len: 最长标题字数
        suggest: 是否输出修改建议
        output_format: 输出格式 'text' 或 'json'
    
    Returns:
        检查结果字典
    """
    chapters = list_chapter_files(novel_dir)
    if not chapters:
        return {'error': f'未找到章节文件: {novel_dir}', 'issues': [], 'stats': {}}
    
    all_issues = []
    suggestions = []
    
    # 每章检查
    for num, fname in chapters:
        title = extract_title(fname)
        chapter_issues = []
        
        # 1. 长度检查
        chapter_issues.extend(check_title_length(title, num, min_len, max_len))
        
        # 2. 吸引力检查
        chapter_issues.extend(check_title_attractiveness(title, num))
        
        # 3. 钩子检查
        chapter_issues.extend(check_hooks(title, num))
        
        all_issues.extend(chapter_issues)
        
        if suggest:
            suggestions.append(generate_suggestion(title, num, chapter_issues))
    
    # 格式一致性检查（全局）
    all_issues.extend(check_format_consistency(chapters))
    
    # 统计
    total = len(chapters)
    no_title_count = sum(1 for _, f in chapters if not extract_title(f))
    has_hook_count = sum(1 for _, f in chapters 
                        if any(w in extract_title(f) for w in HOOK_WORDS))
    flat_count = sum(1 for _, f in chapters 
                    if any(re.match(p, extract_title(f)) for p in FLAT_PATTERNS))
    
    # 按严重程度统计
    severity_counts = Counter(i.get('severity', 'medium') for i in all_issues)
    
    stats = {
        'total_chapters': total,
        'no_title': no_title_count,
        'has_hook': has_hook_count,
        'flat_title': flat_count,
        'hook_rate': f'{has_hook_count/total:.0%}' if total else '0%',
        'total_issues': len(all_issues),
        'high': severity_counts.get('high', 0),
        'medium': severity_counts.get('medium', 0),
        'low': severity_counts.get('low', 0),
    }
    
    result = {'issues': all_issues, 'stats': stats}
    
    # 输出
    if output_format == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        _print_text_result(result, suggest, suggestions)
    
    return result


def _print_text_result(result: Dict[str, Any], suggest: bool, suggestions: List[str]) -> None:
    """文本格式输出"""
    stats = result['stats']
    issues = result['issues']
    
    print('=' * 60)
    print(f'📖 章节标题质量检查 {VERSION}')
    print('=' * 60)
    print(f'\n📊 统计：共{stats["total_chapters"]}章')
    print(f'   无标题：{stats["no_title"]}章')
    print(f'   平淡标题：{stats["flat_title"]}章')
    print(f'   含悬念词：{stats["has_hook"]}章（{stats["hook_rate"]}）')
    print(f'   问题总数：{stats["total_issues"]}（🔴{stats["high"]} 🟡{stats["medium"]} 🟢{stats["low"]}）')
    
    if not issues:
        print('\n✅ 未发现标题质量问题')
    else:
        # 按严重程度输出
        for sev, label, emoji in [('high', '严重', '🔴'), ('medium', '中等', '🟡'), ('low', '轻微', '🟢')]:
            sev_issues = [i for i in issues if i.get('severity') == sev]
            if not sev_issues:
                continue
            print(f'\n### {emoji} {label}问题（{len(sev_issues)}个）')
            for issue in sev_issues:
                ch = issue.get('chapter', 0)
                ch_label = f'第{ch}章' if ch > 0 else '全局'
                print(f'  • [{issue["type"]}] {ch_label}：{issue["detail"]}')
                if issue.get('suggestion'):
                    print(f'    💡 {issue["suggestion"]}')
    
    if suggest and suggestions:
        print(f'\n{"="*60}')
        print('📝 修改建议')
        print('=' * 60)
        for s in suggestions:
            print(f'\n{s}')


def main():
    parser = argparse.ArgumentParser(description='章节标题质量检查')
    parser.add_argument('--novel-dir', required=True, help='章节目录路径')
    parser.add_argument('--min-len', type=int, default=5, help='最短标题字数（默认5）')
    parser.add_argument('--max-len', type=int, default=25, help='最长标题字数（默认25）')
    parser.add_argument('--suggest', action='store_true', help='输出修改建议')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='输出格式')
    parser.add_argument('--version', action='version', version=f'chapter_title_check {VERSION} (novel-writer skill)')
    args = parser.parse_args()
    
    run_check(args.novel_dir, args.min_len, args.max_len, args.suggest, args.format)


if __name__ == '__main__':
    main()
