#!/usr/bin/env python3
"""
One-Page Executive Report - translate technical findings into decision language.

Three sections, zero jargon, Chinese:
  1. 风险结论 (risk conclusion)
  2. 业务影响 (business impact, via category->impact phrase table)
  3. 处置建议 (装 / 不装 / 装前改, three-way)

Renders a single self-contained HTML file (print-friendly -> PDF).
The category->impact mapping is externalizable to JSON via impact_map_path so
the wording can be customized without code changes (死规则9: configurable).

Pure stdlib. Author: njskills@agent.qq.com
Version: 1.0.0
"""

import json
from pathlib import Path
from datetime import datetime

VERSION = "1.0.0"

# Default category -> business-impact phrase table (zero jargon).
DEFAULT_IMPACT_MAP = {
    'prompt_injection': '可能被诱导执行非预期指令，导致配置被篡改',
    'command_injection': '可能执行任意系统命令，危及整机安全',
    'ssrf': '可能被利用访问内网资源，造成内部信息外泄',
    'credential_leak': '可能外传密钥或账号密码，导致凭据泄露',
    'path_traversal': '可能读写预期范围外的文件，造成数据泄露或被篡改',
    'dangerous_functions': '可能调用高风险函数，引发不可控行为',
    'taint_chain': '存在从用户输入到危险操作的完整数据流，可能被直接利用',
    'malicious_fingerprint': '命中已知恶意样本指纹，强烈建议不要安装',
    'known_malicious': '命中已知恶意样本指纹，强烈建议不要安装',
    'dependency_cve': '依赖存在已知漏洞，可能被攻击者利用入侵',
    'typo_squatting': '依赖包名疑似钓鱼，可能引入恶意代码',
    'permission': '申请了超出需要的权限，可能获得不该有的系统控制能力',
    'compliance_permission': '申请了超出需要的权限，可能获得不该有的系统控制能力',
    'health_quality': '文档与元数据不完整，可能影响后续维护与可信度',
    'health_structure': '包结构异常，可能夹带不该有的文件',
    'supply_chain': '供应链存在风险，可能在安装或运行时引入威胁',
}

DEFAULT_IMPACT = '存在安全风险，建议进一步确认后再决定是否安装'

SEVERITY_LABEL = {
    'critical': '严重', 'high': '高危', 'medium': '中等', 'low': '低', 'info': '提示'
}


def load_impact_map(path=None):
    """Load (and merge over default) an external category->impact JSON map."""
    impact = dict(DEFAULT_IMPACT_MAP)
    if path:
        try:
            data = json.loads(Path(path).read_text(encoding='utf-8'))
            if isinstance(data, dict):
                impact.update(data)
        except Exception:
            pass
    return impact


def derive_verdict(report):
    """Derive a three-way decision from a full report. Consistent with quick verdict."""
    stats = report.get('statistics', {}) or {}
    results = report.get('results', []) or []
    categories = {str(r.get('category', '')) for r in results}

    # Malicious force-categories
    force = {'malicious_fingerprint', 'known_malicious'}
    if (stats.get('critical', 0) > 0) or (categories & force):
        return 'do_not_install'
    if stats.get('high', 0) > 0 or stats.get('medium', 0) > 0:
        return 'install_with_changes'
    if stats.get('low', 0) > 0 or stats.get('info', 0) > 0:
        return 'install_with_changes'
    return 'install'


def build_onepager(report, impact_map=None):
    """Build the structured one-page dict from a full report."""
    impact = impact_map if impact_map is not None else load_impact_map()
    results = report.get('results', []) or []
    stats = report.get('statistics', {}) or {}
    verdict = derive_verdict(report)
    meta = report.get('meta', {}) or {}
    skill_name = meta.get('skill_name', 'unknown')

    # Pick top risks by severity
    sev_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3, 'info': 4}
    top = sorted(results, key=lambda r: sev_order.get(str(r.get('severity', '')), 5))[:3]

    impacts = []
    seen = set()
    for r in top:
        cat = str(r.get('category', ''))
        phrase = impact.get(cat, DEFAULT_IMPACT)
        if phrase in seen:
            continue
        seen.add(phrase)
        impacts.append(phrase)

    conclusion_map = {
        'do_not_install': (
            '不建议安装',
            f'共发现 {stats.get("critical", 0)} 项严重问题，风险较高。'),
        'install_with_changes': (
            '建议修改后再安装',
            f'发现 {stats.get("high", 0)} 项高危、{stats.get("medium", 0)} 项中等风险，'
            '建议先处理再使用。'),
        'install': (
            '可以安装',
            '未发现明显安全问题，可正常使用。'),
    }
    title, detail = conclusion_map[verdict]

    action_map = {
        'do_not_install': '不装：直接放弃该 Skill，或等待作者修复后重新评估。',
        'install_with_changes': '装前改：按建议处理风险项（如收紧权限、替换可疑依赖）后再安装。',
        'install': '装：风险可控，可正常安装使用，建议定期关注更新。',
    }

    return {
        'meta': {
            'tool': 'skill-security-checker',
            'version': VERSION,
            'generated_at': datetime.now().isoformat(timespec='seconds'),
            'skill_name': skill_name,
            'source_report_version': meta.get('version', ''),
        },
        'verdict': verdict,
        'conclusion': {'title': title, 'detail': detail},
        'business_impact': impacts or ['未发现需要特别说明的业务影响'],
        'recommendation': action_map[verdict],
        'top_risks': [
            {
                'severity': SEVERITY_LABEL.get(str(r.get('severity', '')), r.get('severity', '')),
                'message': r.get('message', ''),
                'suggestion': r.get('suggestion', ''),
            }
            for r in top
        ],
    }


def to_html(onepager, output_path=None):
    """Render the one-pager to a single self-contained, print-friendly HTML."""
    c = onepager['conclusion']
    impacts = ''.join(f'<li>{_e(x)}</li>' for x in onepager['business_impact'])
    risks = ''
    for r in onepager.get('top_risks', []):
        risks += (f'<div class="risk"><span class="sev">{_e(r["severity"])}</span>'
                  f'<div><div class="msg">{_e(r["message"])}</div>'
                  f'<div class="sug">建议：{_e(r["suggestion"])}</div></div></div>')
    verdict_class = {
        'do_not_install': 'bad',
        'install_with_changes': 'warn',
        'install': 'good',
    }.get(onepager['verdict'], 'warn')

    html = f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Skill 安全一页纸 - {_e(onepager['meta']['skill_name'])}</title>
<style>
  body {{ font-family: -apple-system, "Microsoft YaHei", sans-serif; margin: 0; padding: 32px;
         color: #1a1a1a; background: #fff; line-height: 1.65; }}
  .page {{ max-width: 760px; margin: 0 auto; }}
  h1 {{ font-size: 22px; margin: 0 0 4px; }}
  .sub {{ color: #888; font-size: 12px; margin-bottom: 24px; }}
  .verdict {{ border-radius: 12px; padding: 20px 24px; margin-bottom: 22px; }}
  .verdict.bad {{ background: #fdecec; border-left: 5px solid #c0392b; }}
  .verdict.warn {{ background: #fdf3e2; border-left: 5px solid #d68910; }}
  .verdict.good {{ background: #eaf7ee; border-left: 5px solid #1e8449; }}
  .verdict h2 {{ margin: 0 0 6px; font-size: 26px; }}
  .verdict p {{ margin: 0; font-size: 14px; }}
  h3 {{ font-size: 15px; margin: 22px 0 10px; border-bottom: 1px solid #eee; padding-bottom: 6px; }}
  ul {{ margin: 0; padding-left: 22px; }}
  li {{ margin: 6px 0; font-size: 14px; }}
  .risk {{ display: flex; gap: 12px; padding: 10px 0; border-bottom: 1px dashed #eee; }}
  .sev {{ flex: 0 0 44px; font-size: 12px; font-weight: bold; color: #c0392b; }}
  .msg {{ font-size: 14px; }}
  .sug {{ font-size: 12px; color: #666; margin-top: 3px; }}
  .reco {{ background: #f4f6f8; border-radius: 8px; padding: 14px 18px; font-size: 14px; }}
  .foot {{ margin-top: 28px; color: #aaa; font-size: 11px; text-align: center; }}
  @media print {{ body {{ padding: 0; }} .page {{ max-width: none; }} }}
</style></head><body><div class="page">
  <h1>Skill 安全评估 · 一页纸</h1>
  <div class="sub">对象：{_e(onepager['meta']['skill_name'])} ｜ 生成：{_e(onepager['meta']['generated_at'])}</div>
  <div class="verdict {verdict_class}">
    <h2>{_e(c['title'])}</h2>
    <p>{_e(c['detail'])}</p>
  </div>
  <h3>可能带来的影响</h3>
  <ul>{impacts}</ul>
  <h3>需要处理的主要问题</h3>
  {risks or '<p style="font-size:14px;color:#888">无</p>'}
  <h3>怎么处理</h3>
  <div class="reco">{_e(onepager['recommendation'])}</div>
  <div class="foot">有更好建议：njskills@agent.qq.com ｜ 由 Skill 安全审计扫描器生成</div>
</div></body></html>'''
    if output_path:
        Path(output_path).write_text(html, encoding='utf-8')
    return html


def _e(text):
    """HTML-escape."""
    import html as _html
    return _html.escape(str(text if text is not None else ''))


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description='One-page executive security report')
    p.add_argument('report_json', help='Full report JSON file')
    p.add_argument('-o', '--output', help='Output HTML file')
    p.add_argument('--impact-map', help='External category->impact JSON map')
    a = p.parse_args()
    data = json.loads(Path(a.report_json).read_text(encoding='utf-8'))
    op = build_onepager(data, load_impact_map(a.impact_map))
    html = to_html(op, a.output)
    if not a.output:
        print(json.dumps(op, ensure_ascii=False, indent=2))
    else:
        print(f"一页纸报告已生成：{a.output}")
