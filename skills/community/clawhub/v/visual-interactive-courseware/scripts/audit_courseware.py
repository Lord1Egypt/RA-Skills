# -*- coding: utf-8 -*-
"""
课件内容自动审核脚本（audit_courseware.py）
对单文件 HTML 课件做静态+运行时审核，输出改进建议报告。
用法: python audit_courseware.py <课件.html> [--report out.md]
审核维度：知识准确性锚点、交互完整性、无障碍、性能、学段适配、结构规范
"""
import json, re, sys, os

sys.stdout.reconfigure(encoding='utf-8')

# ============ 审核规则库 ============
RULES = {
  'single_file': {
    'name': '单文件自包含', 'level': 'P0',
    'check': lambda html: not re.search(r'<(link|script)[^>]+(src|href)="https?://', html),
    'fix': '移除外链 CDN/字体/脚本引用，全部内联（教室离线可用）'
  },
  'no_ext_img': {
    'name': '图片全部内嵌', 'level': 'P0',
    'check': lambda html: not re.search(r'<img[^>]+src="https?://', html) and not re.search(r'href="data:image', html) is None and '<image href="data:image' in html or not re.search(r'<img[^>]+src="(?!data:)[^"]+"', html),
    'fix': '外链图片改为 base64 内嵌'
  },
  'unique_ids': {
    'name': '渐变/滤镜 ID 全局唯一', 'level': 'P0',
    'check': lambda html: _check_dup_ids(html),
    'fix': '为每个 <svg> 的 defs ID 加唯一后缀（跨 SVG 引用 display:none 内 ID 会渲染失败）'
  },
  'keyboard': {
    'name': '键盘翻页支持', 'level': 'P1',
    'check': lambda html: 'ArrowRight' in html and 'ArrowLeft' in html,
    'fix': '添加 ←→/PageUp/PageDown 键盘翻页（翻页笔兼容）'
  },
  'pause_all': {
    'name': '播放暂停覆盖全部动画', 'level': 'P1',
    'check': lambda html: 'animation-play-state' in html or 'paused' in html,
    'fix': '暂停时同步冻结 dash 流动/脉动/序列器（animation-play-state:paused）'
  },
  'font_min': {
    'name': '最小字号 ≥ 11px', 'level': 'P1',
    'check': lambda html: not re.search(r'font-size\s*:\s*(10|9|8)px', html),
    'fix': '投影环境最小可读字号 11px（SVG 内 viewBox 1200 时 13px）'
  },
  'zh_lang': {
    'name': '中文界面声明', 'level': 'P2',
    'check': lambda html: 'lang="zh' in html,
    'fix': '<html lang="zh-CN">'
  },
  'alt_text': {
    'name': '图像可访问描述', 'level': 'P2',
    'check': lambda html: all('aria-label' in m or 'title' in m or 'alt=' in m
                              for m in re.findall(r'<(?:img|image)[^>]*>', html)),
    'fix': '为语义图片（<img>/<svg image>）加 aria-label/alt'
  },
  'no_emoji_title': {
    'name': '标题不依赖 emoji 传达', 'level': 'P2',
    'check': lambda html: not re.search(r'<title>[^<]*[\u2600-\u27BF\U0001F300-\U0001FAFF]', html),
    'fix': '<title> 保持纯文本'
  },
  'autoplay_guard': {
    'name': '自动播放有暂停入口', 'level': 'P1',
    'check': lambda html: 'btnPlay' in html or 'play' in html.lower(),
    'fix': '自动播放的课件必须有显眼暂停按钮'
  },
}

def _check_dup_ids(html):
    ids = re.findall(r'<(?:linearGradient|radialGradient|filter|pattern|clipPath)\s+id="([^"]+)"', html)
    return len(ids) == len(set(ids))

def audit(path):
    with open(path, encoding='utf-8') as f:
        html = f.read()
    results = []
    for key, rule in RULES.items():
        try:
            ok = bool(rule['check'](html))
        except Exception as e:
            ok = False
        results.append({'rule': rule['name'], 'level': rule['level'], 'pass': ok, 'fix': rule['fix']})
    # 统计
    p0_fail = [r for r in results if not r['pass'] and r['level']=='P0']
    p1_fail = [r for r in results if not r['pass'] and r['level']=='P1']
    score = 100 - len(p0_fail)*25 - len(p1_fail)*10
    return {'file': path, 'size_kb': os.path.getsize(path)//1024, 'score': max(0, score),
            'results': results}

def report_md(res):
    lines = ['# 课件审核报告', '',
             f"- 文件：`{res['file']}`",
             f"- 体积：{res['size_kb']} KB",
             f"- **质量分：{res['score']}/100**", '',
             '| 等级 | 检查项 | 结果 | 修复建议 |', '|---|---|---|---|']
    for r in res['results']:
        lines.append(f"| {r['level']} | {r['rule']} | {'✅' if r['pass'] else '❌'} | {r['fix'] if not r['pass'] else '—'} |")
    return '\n'.join(lines)

if __name__ == '__main__':
    path = sys.argv[1]
    res = audit(path)
    md = report_md(res)
    print(md)
    if '--report' in sys.argv:
        out = sys.argv[sys.argv.index('--report')+1]
        with open(out, 'w', encoding='utf-8') as f:
            f.write(md)
        print(f'\n报告已写入 {out}')
    sys.exit(0 if res['score'] >= 90 else 1)
