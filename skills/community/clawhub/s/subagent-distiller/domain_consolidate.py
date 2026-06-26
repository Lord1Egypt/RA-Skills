#!/usr/bin/env python3
"""
domain_consolidate.py - 域聚合器 v3.0

功能：
- 按域分类所有卡片（Polymarket/OpenClaw/Research/System）
- 每域合并成专书（消除重复，统一格式）
- 支持增量更新（只处理变更的卡片）
"""

import json
import hashlib
import re
from pathlib import Path
from datetime import datetime

WORKSPACE = Path("/home/aqukin/.openclaw/workspace")
SKILL_DIR = WORKSPACE / "skills/subagent-distiller"
TOPICS_DIR = WORKSPACE / "memory/topics"
CONSOLIDATED_DIR = WORKSPACE / "memory/domains"
STATE_FILE = SKILL_DIR / "consolidation_state.json"

# 域分类规则
DOMAIN_RULES = {
    'Polymarket': [
        r'^polymarket_',
        r'_trader_',
        r'_trading_',
        r'_market_',
        r'_order_',
        r'_position_',
        r'_balance_',
        r'_clob_',
        r'_auto_sell_',
        r'_take_profit_',
        r'_stop_loss_',
    ],
    'OpenClaw': [
        r'^openclaw_',
        r'^subagent_',
        r'^sessions_spawn_',
        r'^gateway_',
        r'^browser_',
        r'^hook_',
        r'^cron_',
        r'^distill_',
        r'^memory_',
        r'^skill_',
        r'^agent_cluster_',
    ],
    'Research': [
        r'^eeg_',
        r'^crf_',
        r'^phd_',
        r'^dataset_',
        r'^paradigm_',
        r'^preprocessing_',
        r'^visualization_',
        r'^experiment_',
    ],
    'System': [
        r'^conda_',
        r'^wsl2_',
        r'^docker_',
        r'^git_',
        r'^config_',
        r'^deploy_',
        r'^setup_',
    ]
}

def ensure_dirs():
    CONSOLIDATED_DIR.mkdir(parents=True, exist_ok=True)

def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {'domains': {}, 'cards': {}}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def compute_hash(content):
    return hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]

def classify_domain_dynamic(card_name, cards_data=None):
    """动态发现域 - 从卡片名称提取前缀作为域"""
    # 从卡片名称提取前缀（第一个下划线前的部分）
    if '_' in card_name:
        prefix = card_name.split('_')[0].lower()
    else:
        prefix = 'misc'
    
    # 返回首字母大写的域名称
    return prefix.capitalize()

def discover_domains(cards):
    """自动发现所有域"""
    domain_cards = {}
    
    for card_path in cards:
        domain = classify_domain_dynamic(card_path.name)
        if domain not in domain_cards:
            domain_cards[domain] = []
        domain_cards[domain].append(card_path)
    
    return domain_cards

def parse_card(card_path):
    """解析卡片内容"""
    with open(card_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析 frontmatter
    metadata = {}
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                metadata = yaml_safe_load(parts[1])
                content = parts[2].strip()
            except:
                content = content
    
    # 提取章节
    sections = {}
    current_section = None
    current_content = []
    
    for line in content.split('\n'):
        if line.startswith('# ') and not line.startswith('# 🏷️'):
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            current_section = line[2:].strip()
            current_content = []
        elif line.startswith('## '):
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            current_section = line[3:].strip()
            current_content = []
        else:
            current_content.append(line)
    
    if current_section:
        sections[current_section] = '\n'.join(current_content)
    
    return {
        'metadata': metadata,
        'sections': sections,
        'raw': content,
        'name': card_path.stem
    }

def yaml_safe_load(text):
    """简易 YAML 解析"""
    result = {}
    for line in text.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"')
            result[key] = value
    return result

def get_consolidation_prompt(domain, cards_data):
    """生成域合并提示词"""
    cards_summary = []
    for card in cards_data:
        cards_summary.append(f"""
【卡片: {card['name']}】
状态: {card['metadata'].get('status', 'unknown')}
时效: {card['metadata'].get('temporal', 'unknown')}
摘要: {card['metadata'].get('summary', '无')}

内容:
{card['raw'][:500]}...  # 截断，避免过长
""")
    
    return f"""你是一位专业的知识管理专家。请将以下 {domain} 域的 {len(cards_data)} 个知识卡片合并成一本结构化的"专书"。

【要求】：
1. **按主题归类**：将相关卡片归类到同一章节（如"架构设计"、"避坑指南"、"配置参考"）
2. **消除重复**：相同知识点只保留一次
3. **更新状态**：
   - 多个 PENDING 合并 → 保持 PENDING 并列出所有待办
   - 有 RESOLVED 覆盖 PENDING → 标记为 RESOLVED
   - ABANDONED 单独成章（避坑专用）
4. **时效性处理**：
   - short-term 内容（市场分析、体育预测）→ 移至附录或标记为"历史参考"
   - long-term 内容（架构、配置）→ 作为主体
5. **格式统一**：使用一致的 Markdown 格式

【输出格式】：
```markdown
# 📚 {domain} 知识专书

## 版本信息
- 生成时间: {datetime.now().strftime('%Y-%m-%d')}
- 来源卡片数: {len(cards_data)}
- 状态统计: RESOLVED X个, PENDING Y个, ABANDONED Z个

## 目录
1. [架构设计](#架构设计)
2. [核心流程](#核心流程)
3. [避坑指南](#避坑指南)
4. [配置参考](#配置参考)
5. [待办事项](#待办事项)
6. [历史归档](#历史归档)

## 架构设计
...

## 核心流程
...

## 避坑指南
...

## 配置参考
...

## 待办事项
- [ ] ...

## 历史归档
（短期时效内容归档此处）
```

【待合并卡片】：
{''.join(cards_summary[:5])}  # 最多显示5个，避免超出上下文

【注意】：
- 只输出 Markdown 内容，不要其他文字
- 确保逻辑连贯，消除矛盾
- Polymarket 具体市场分析（胜率、赔率）归入"历史归档"
- Polymarket 代码/架构保留在主体章节
"""

def consolidate_domain(domain, cards, state):
    """合并单个域"""
    print(f"\n📚 正在合并 {domain} 域...")
    print(f"   卡片数: {len(cards)}")
    
    # 解析所有卡片
    cards_data = []
    for card_path in cards:
        try:
            data = parse_card(card_path)
            data['path'] = str(card_path)
            cards_data.append(data)
        except Exception as e:
            print(f"   ⚠️  解析失败 {card_path.name}: {e}")
    
    if not cards_data:
        print(f"   ⚠️  没有可合并的卡片")
        return
    
    # 生成提示词（用于子代理）
    prompt = get_consolidation_prompt(domain, cards_data)
    
    # 保存任务
    task = {
        'domain': domain,
        'card_count': len(cards_data),
        'prompt': prompt,
        'cards': [c['name'] for c in cards_data]
    }
    
    task_file = SKILL_DIR / f'consolidation_task_{domain}.json'
    with open(task_file, 'w') as f:
        json.dump(task, f, indent=2)
    
    print(f"   📝 生成合并任务: {task_file}")
    print(f"   🚀 下一步: 主代理使用 sessions_spawn 处理此任务")
    
    return task

def main():
    print("📚 域聚合器 v3.0")
    print("=" * 50)
    
    ensure_dirs()
    state = load_state()
    
    # 获取所有卡片
    all_cards = list(TOPICS_DIR.glob('*.md'))
    if not all_cards:
        print("没有找到知识卡片")
        return
    
    print(f"发现 {len(all_cards)} 个知识卡片")
    print()
    
    # 动态发现域（自下而上聚类）
    domain_cards = discover_domains(all_cards)
    
    # 显示分类结果
    print("动态发现的域:")
    for domain, cards in sorted(domain_cards.items(), key=lambda x: -len(x[1])):
        print(f"   {domain}: {len(cards)} 个卡片")
    print()
    
    # 为每个域生成合并任务
    pending_tasks = []
    for domain, cards in domain_cards.items():
        if not cards:
            continue
        
        # 检查是否有变更
        current_hashes = [compute_hash(c.read_text()) for c in cards]
        last_hashes = state['domains'].get(domain, {}).get('card_hashes', [])
        
        if current_hashes == last_hashes:
            print(f"   ⏭️  {domain} 域无变更，跳过")
            continue
        
        task = consolidate_domain(domain, cards, state)
        if task:
            pending_tasks.append(domain)
            
            # 更新状态
            state['domains'][domain] = {
                'card_hashes': current_hashes,
                'last_consolidated': datetime.now().isoformat(),
                'card_count': len(cards)
            }
    
    save_state(state)
    
    print()
    print("=" * 50)
    if pending_tasks:
        print(f"✅ 生成 {len(pending_tasks)} 个域合并任务:")
        for domain in pending_tasks:
            print(f"   - {domain}")
        print()
        print("🚀 下一步：主代理使用 sessions_spawn 处理这些任务")
        print("   处理完成后将生成:")
        for domain in pending_tasks:
            print(f"      {CONSOLIDATED_DIR}/{domain}.md")
    else:
        print("✅ 所有域已是最新状态")

def finalize_consolidation(domain, result_file):
    """完成合并，保存专书"""
    with open(result_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    output_path = CONSOLIDATED_DIR / f"{domain}.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已保存: {output_path}")
    print(f"   体积: {len(content)} 字符")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--finalize':
        if len(sys.argv) >= 4:
            finalize_consolidation(sys.argv[2], sys.argv[3])
        else:
            print("用法: python3 domain_consolidate.py --finalize <domain> <result_file>")
    else:
        main()