#!/usr/bin/env python3
"""
技能优化师 - 自动评估技能是否符合 SKILL-STANDARD-v3.md

用法:
    python3 optimize-skill.py <skill_name> [--batch <dir>] [--report]
"""

import os
import re
import sys
import json
from datetime import datetime

# 配置
SKILLS_DIRS = [
    os.path.expanduser('~/.openclaw/workspace/skills'),
    os.path.expanduser('~/.openclaw/workspace/investment-framework-skill'),
    os.path.expanduser('~/.openclaw/workspace/investment-framework-skill/china-masters'),
]
STANDARD_FILE = os.path.expanduser('~/.openclaw/workspace/docs/SKILL-STANDARD-v3.md')

# 必填元数据字段（v3.0 标准：只要求 2 个）
REQUIRED_FIELDS = ['name', 'description']
RECOMMENDED_FIELDS = ['version', 'allowed-tools', 'author', 'created', 'skill_type', 'related_skills', 'tags']

# 必需章节（v3.0 轻量级模板）
REQUIRED_SECTIONS = [
    '## 📋 功能描述',
    '## ⚠️ 常见错误',
]

# 推荐章节
RECOMMENDED_SECTIONS = [
    '## 🧪 使用示例',
    '## 🔗 相关资源',
    '## 🔧 故障排查',
]


def load_standard():
    """加载标准文件"""
    if os.path.exists(STANDARD_FILE):
        with open(STANDARD_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    return None


def parse_skill_metadata(content):
    """解析技能元数据"""
    metadata = {}
    
    # 提取 YAML frontmatter
    match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        yaml_content = match.group(1)
        for line in yaml_content.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip().strip('"\'')
    
    return metadata


def check_metadata(metadata):
    """检查元数据"""
    results = {
        'required': {},
        'recommended': {},
        'issues': [],
    }
    
    # 检查必填字段
    for field in REQUIRED_FIELDS:
        if field in metadata and metadata[field]:
            results['required'][field] = {'status': '✅', 'value': metadata[field]}
        else:
            results['required'][field] = {'status': '❌', 'value': '缺失'}
            results['issues'].append(f'🔴 必填字段缺失：{field}')
    
    # 检查推荐字段
    for field in RECOMMENDED_FIELDS:
        if field in metadata and metadata[field]:
            results['recommended'][field] = {'status': '✅', 'value': metadata[field]}
        else:
            results['recommended'][field] = {'status': '⚠️', 'value': '缺失'}
    
    # 特殊检查：description 触发词
    if 'description' in metadata:
        desc = metadata['description']
        if '［何时使用］' not in desc and '[何时使用]' not in desc:
            results['issues'].append('🔴 description 缺少触发词［何时使用］')
        elif len(desc) > 1024:
            results['issues'].append('🟡 description 超过 1024 字符')
    
    # 特殊检查：skill_type 规范（如果有）
    if 'skill_type' in metadata:
        skill_type = metadata['skill_type']
        valid_types = ['核心🔴', '通用🟡', '实验🟢', '核心', '通用', '实验']
        if skill_type not in valid_types:
            results['issues'].append(f'🟡 skill_type 不规范：{skill_type}')
    else:
        # skill_type 是推荐字段，不强制
        pass
    
    return results


def check_structure(content):
    """检查正文结构"""
    results = {
        'required': {},
        'recommended': {},
        'issues': [],
    }
    
    # 检查必需章节
    for section in REQUIRED_SECTIONS:
        if section in content:
            results['required'][section] = {'status': '✅'}
        else:
            results['required'][section] = {'status': '❌'}
            results['issues'].append(f'🔴 缺少必需章节：{section}')
    
    # 检查推荐章节
    for section in RECOMMENDED_SECTIONS:
        if section in content:
            results['recommended'][section] = {'status': '✅'}
        else:
            results['recommended'][section] = {'status': '⚠️'}
    
    # 检查渐进式披露
    if 'references/' in content or '`references/' in content:
        results['progressive'] = {'status': '✅', 'note': '已实现渐进式披露'}
    else:
        # 检查文件长度
        lines = content.split('\n')
        if len(lines) > 200:
            results['progressive'] = {'status': '⚠️', 'note': f'文件过长 ({len(lines)}行)，建议渐进式披露'}
            results['issues'].append('🟡 文件过长，建议创建 references 目录')
        else:
            results['progressive'] = {'status': '✅', 'note': '文件长度合理'}
    
    return results


def calculate_score(metadata_results, structure_results):
    """计算质量评分（v3.0 标准）"""
    score = 0
    max_score = 100
    
    # 元数据评分（50 分）
    # 必填字段 30 分，推荐字段 20 分
    required_count = len([v for v in metadata_results['required'].values() if v['status'] == '✅'])
    required_total = len(metadata_results['required'])
    metadata_score = (required_count / required_total * 30) if required_total > 0 else 0
    
    recommended_count = len([v for v in metadata_results['recommended'].values() if v['status'] == '✅'])
    recommended_total = len(metadata_results['recommended'])
    metadata_score += (recommended_count / recommended_total * 20) if recommended_total > 0 else 0
    
    score += min(metadata_score, 50)
    
    # 结构评分（50 分）
    # 必需章节 30 分，推荐章节 20 分
    required_sections = len([v for v in structure_results['required'].values() if v['status'] == '✅'])
    required_total = len(structure_results['required'])
    structure_score = (required_sections / required_total * 30) if required_total > 0 else 0
    
    recommended_sections = len([v for v in structure_results['recommended'].values() if v['status'] == '✅'])
    recommended_total = len(structure_results['recommended'])
    structure_score += (recommended_sections / recommended_total * 20) if recommended_total > 0 else 0
    
    score += min(structure_score, 50)
    
    # 不扣分，只给建议
    # v3.0 标准：简约高效，不惩罚
    
    return max(0, min(100, score))


def get_rating(score):
    """获取评级"""
    if score >= 90:
        return '优秀', '🌟'
    elif score >= 75:
        return '良好', '✅'
    elif score >= 60:
        return '合格', '⚠️'
    else:
        return '需改进', '❌'


def generate_suggestions(metadata_results, structure_results):
    """生成优化建议"""
    suggestions = {
        'critical': [],  # 必须修复
        'recommended': [],  # 建议优化
        'optional': [],  # 可选改进
    }
    
    # 元数据问题
    for field, result in metadata_results['required'].items():
        if result['status'] == '❌':
            suggestions['critical'].append(f'补充必填字段：{field}')
    
    # description 触发词
    if any('缺少触发词' in issue for issue in metadata_results['issues']):
        suggestions['critical'].append('description 添加［何时使用］触发词')
    
    # 结构问题
    for section, result in structure_results['required'].items():
        if result['status'] == '❌':
            suggestions['critical'].append(f'添加必需章节：{section}')
    
    # 推荐字段
    for field, result in metadata_results['recommended'].items():
        if result['status'] == '⚠️' and field == 'allowed-tools':
            suggestions['recommended'].append(f'补充推荐字段：{field}')
    
    # 渐进式披露
    if structure_results.get('progressive', {}).get('status') == '⚠️':
        suggestions['recommended'].append('创建 references 目录，实现渐进式披露')
    
    return suggestions


def find_skill_file(skill_name):
    """查找技能文件"""
    for skills_dir in SKILLS_DIRS:
        # 直接查找
        skill_file = os.path.join(skills_dir, skill_name, 'SKILL.md')
        if os.path.exists(skill_file):
            return skill_file
        
        # 在子目录查找（如 china-masters）
        for root, dirs, files in os.walk(skills_dir):
            if 'SKILL.md' in files:
                dir_name = os.path.basename(root)
                if dir_name == skill_name or f'/{skill_name}/' in root:
                    return os.path.join(root, 'SKILL.md')
    
    return None


def optimize_skill(skill_name):
    """优化单个技能"""
    skill_file = find_skill_file(skill_name)
    
    if not skill_file:
        return {'error': f'技能文件不存在：{skill_name}'}
    
    # 读取技能文件
    with open(skill_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析元数据
    metadata = parse_skill_metadata(content)
    
    # 检查元数据
    metadata_results = check_metadata(metadata)
    
    # 检查结构
    structure_results = check_structure(content)
    
    # 计算评分
    score = calculate_score(metadata_results, structure_results)
    rating, rating_icon = get_rating(score)
    
    # 生成建议
    suggestions = generate_suggestions(metadata_results, structure_results)
    
    return {
        'skill_name': skill_name,
        'timestamp': datetime.now().isoformat(),
        'metadata': metadata_results,
        'structure': structure_results,
        'score': score,
        'rating': rating,
        'rating_icon': rating_icon,
        'suggestions': suggestions,
    }


def print_report(result):
    """打印评估报告"""
    if 'error' in result:
        print(f"❌ 错误：{result['error']}")
        return
    
    print("="*60)
    print(f"🔍 技能优化师：{result['skill_name']}")
    print("="*60)
    print(f"\n📊 评估时间：{result['timestamp']}")
    
    # 元数据检查
    print(f"\n📋 元数据检查")
    for field, check in result['metadata']['required'].items():
        print(f"   {check['status']} {field}: {check['value'][:50] if len(str(check['value'])) > 50 else check['value']}")
    
    print(f"\n   推荐字段:")
    for field, check in result['metadata']['recommended'].items():
        print(f"     {check['status']} {field}: {check['value']}")
    
    # 正文结构检查
    print(f"\n📑 正文结构检查")
    print(f"   必需章节:")
    for section, check in result['structure']['required'].items():
        print(f"     {check['status']} {section}")
    
    print(f"   推荐章节:")
    for section, check in result['structure']['recommended'].items():
        print(f"     {check['status']} {section}")
    
    print(f"   渐进式披露：{result['structure'].get('progressive', {}).get('note', 'N/A')}")
    
    # 质量评分
    print(f"\n📈 质量评分")
    print(f"   总分：{result['score']}/100 {result['rating_icon']}（{result['rating']}）")
    
    # 优化建议
    print(f"\n💡 优化建议")
    if result['suggestions']['critical']:
        print(f"\n   🔴 必须修复：")
        for suggestion in result['suggestions']['critical']:
            print(f"     • {suggestion}")
    
    if result['suggestions']['recommended']:
        print(f"\n   🟡 建议优化：")
        for suggestion in result['suggestions']['recommended']:
            print(f"     • {suggestion}")
    
    if result['suggestions']['optional']:
        print(f"\n   🟢 可选改进：")
        for suggestion in result['suggestions']['optional']:
            print(f"     • {suggestion}")
    
    if not any(result['suggestions'].values()):
        print(f"   ✅ 无需优化，符合标准！")
    
    print(f"\n{'='*60}")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python3 optimize-skill.py <skill_name> [--batch <dir>] [--report]")
        print("示例：python3 optimize-skill.py value-analyzer")
        print("       python3 optimize-skill.py --batch investment-framework-skill")
        return 1
    
    if '--batch' in sys.argv:
        # 批量检查
        batch_idx = sys.argv.index('--batch')
        if batch_idx + 1 < len(sys.argv):
            batch_dir = sys.argv[batch_idx + 1]
            # 支持绝对路径和相对路径
            if os.path.isabs(batch_dir):
                batch_path = batch_dir
            else:
                # 在多个技能目录中查找
                batch_path = None
                for skills_dir in SKILLS_DIRS:
                    test_path = os.path.join(skills_dir, batch_dir)
                    if os.path.exists(test_path):
                        batch_path = test_path
                        break
                if not batch_path:
                    print(f"错误：找不到目录 {batch_dir}")
                    return 1
            
            if os.path.exists(batch_path):
                print(f"🔍 批量检查：{batch_dir}")
                print("="*60)
                
                results = []
                for item in os.listdir(batch_path):
                    item_path = os.path.join(batch_path, item)
                    if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, 'SKILL.md')):
                        result = optimize_skill(item)
                        results.append(result)
                        print(f"\n{result['skill_name']}: {result['score']}/100 ({result['rating']})")
                
                # 汇总
                print(f"\n{'='*60}")
                print(f"📊 批量检查汇总")
                print(f"   检查技能：{len(results)} 个")
                avg_score = sum(r['score'] for r in results) / len(results) if results else 0
                print(f"   平均评分：{avg_score:.1f}/100")
                print(f"   优秀：{sum(1 for r in results if r['score'] >= 90)} 个")
                print(f"   良好：{sum(1 for r in results if 75 <= r['score'] < 90)} 个")
                print(f"   合格：{sum(1 for r in results if 60 <= r['score'] < 75)} 个")
                print(f"   需改进：{sum(1 for r in results if r['score'] < 60)} 个")
        else:
            print("错误：--batch 需要指定目录")
            return 1
    else:
        # 单个检查
        skill_name = sys.argv[1]
        result = optimize_skill(skill_name)
        print_report(result)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
