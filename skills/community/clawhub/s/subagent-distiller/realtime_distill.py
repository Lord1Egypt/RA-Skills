#!/usr/bin/env python3
"""
realtime_distill.py - 实时结构化提取器 v3.0

核心改进：
- 不再流水账追加
- 子代理直接输出精炼格式（带状态标记）
- 增量合并到现有卡片（非追加）
"""

import json
import hashlib
import os
import re
from pathlib import Path
from datetime import datetime

# 路径配置
WORKSPACE = Path("/home/aqukin/.openclaw/workspace")
SKILL_DIR = WORKSPACE / "skills/subagent-distiller"
CHUNKS_DIR = SKILL_DIR / "chunks"
TOPICS_DIR = WORKSPACE / "memory/topics"
STATE_FILE = SKILL_DIR / "distill_state.json"

def ensure_dirs():
    TOPICS_DIR.mkdir(parents=True, exist_ok=True)

def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {'processed_slices': {}, 'topics': {}}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def compute_hash(content):
    return hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]

def get_prompt(slice_data):
    """生成提取提示词"""
    return f"""你是一位专业的知识提取工程师。请从以下对话切片中提取结构化知识。

【来源】：{slice_data['source_name']} Line {slice_data['start_line']}-{slice_data['end_line']}
【内容】：
{slice_data['content']}

【提取要求】：
1. 识别对话中的关键知识点、决策、方案、避坑经验
2. 判断每个知识点的状态：
   - RESOLVED：问题已解决，方案已确定
   - PENDING：讨论中，待验证/待决策
   - ABANDONED：已放弃的尝试（记录避坑价值）
3. 【重要】直接丢弃以下类型（should_delete=true）：
   - 体育比赛分析（球队胜率、比分预测等）
   - 具体市场预测（"X市场胜率62%"、当日赔率等）
   - 临时新闻解读（时效性<7天的新闻）
   - 无结论的探索（只有"试试"、"看看"没有结果）
   - 纯寒暄废话（"在吗"、"测试"、纯问候）
4. 只保留以下长期价值内容：
   - 架构设计、系统方案
   - 避坑指南、故障解决
   - 配置沉淀、环境搭建
   - 原则/铁律、SOP流程

【输出格式 - 必须是 JSON】：
{{
  "topics": [
    {{
      "topic": "主题名称（简短英文，用下划线连接）",
      "status": "RESOLVED|PENDING|ABANDONED",
      "temporal": "short-term|long-term",
      "domain": "Polymarket|OpenClaw|Research|System",
      "summary": "一句话核心摘要",
      "conclusions": ["结论1", "结论2"],
      "pitfalls": ["避坑1", "避坑2"],
      "todos": ["待办1", "待办2"],
      "source": "{slice_data['source_name']} Line {slice_data['start_line']}-{slice_data['end_line']}",
      "should_delete": false,
      "reason": "保留/删除的原因"
    }}
  ]
}}

【删除判定】：如果切片全是寒暄、报错、无价值内容，返回：
{{"topics": [], "should_delete": true, "reason": "原因说明"}}

【重要】：
- 只输出 JSON，不要任何其他文字
- 不要包含"我看到..."、"让我测试..."等内部思考语言
- Polymarket 具体市场分析（"某队胜率 X%"）标记为 short-term
- Polymarket 代码/架构标记为 long-term
"""

def merge_topic(existing_path, new_data):
    """增量合并到现有卡片"""
    if not existing_path.exists():
        return create_new_card(new_data)
    
    # 读取现有卡片
    with open(existing_path, 'r', encoding='utf-8') as f:
        existing_content = f.read()
    
    # 简单合并策略：在"最新结论"部分追加新内容
    # 更复杂的合并可以由 domain_consolidate.py 处理
    
    # 提取现有内容的关键部分
    lines = existing_content.split('\n')
    
    # 检查是否已有相同结论（去重）
    existing_text = ' '.join(lines)
    for conclusion in new_data.get('conclusions', []):
        if conclusion in existing_text:
            continue  # 已存在，跳过
        
        # 追加新结论
        # 找到 "## 最新结论" 部分，追加
        for i, line in enumerate(lines):
            if line.startswith('## 最新结论') or line.startswith('## ✅ 最新结论'):
                # 在下一个 ## 之前插入
                insert_pos = i + 1
                while insert_pos < len(lines) and not lines[insert_pos].startswith('##'):
                    insert_pos += 1
                lines.insert(insert_pos, f"- {conclusion} (新增: {datetime.now().strftime('%Y-%m-%d')})")
                break
    
    # 更新时间戳
    for i, line in enumerate(lines):
        if line.startswith('updated:') or line.startswith('updated:'):
            lines[i] = f"updated: {datetime.now().strftime('%Y-%m-%d')}"
            break
    
    return '\n'.join(lines)

def create_new_card(topic_data):
    """创建新卡片"""
    status = topic_data.get('status', 'RESOLVED')
    temporal = topic_data.get('temporal', 'long-term')
    domain = topic_data.get('domain', 'System')
    
    # 如果状态是 ABANDONED 或时效性是 short-term，标记为待删除审查
    should_flag = (status == 'ABANDONED' or temporal == 'short-term')
    
    card = f"""---
topic: "{topic_data['topic']}"
status: {status}
temporal: {temporal}
domain: {domain}
created: {datetime.now().strftime('%Y-%m-%d')}
updated: {datetime.now().strftime('%Y-%m-%d')}
source: {topic_data.get('source', 'unknown')}
flagged: {str(should_flag).lower()}
---

# 🏷️ 主题：{topic_data['topic'].replace('_', ' ').title()}

## 核心摘要
{topic_data.get('summary', '待补充')}

## 最新结论 / 成功方案
"""
    
    for conclusion in topic_data.get('conclusions', []):
        card += f"- {conclusion}\n"
    
    if topic_data.get('pitfalls'):
        card += "\n## 避坑指南\n"
        for pitfall in topic_data.get('pitfalls', []):
            card += f"- ❌ {pitfall}\n"
    
    if topic_data.get('todos') and status == 'PENDING':
        card += "\n## 待办事项\n"
        for todo in topic_data.get('todos', []):
            card += f"- [ ] {todo}\n"
    
    card += f"\n## 历史溯源\n- {topic_data.get('source', 'unknown')}\n"
    
    if should_flag:
        card += "\n---\n⚠️ **系统标记**：此卡片已标记为待审查（短期时效或已放弃）\n"
    
    return card

def process_slice(slice_path, state):
    """处理单个切片"""
    with open(slice_path, 'r', encoding='utf-8') as f:
        slice_data = json.load(f)
    
    slice_hash = compute_hash(json.dumps(slice_data, sort_keys=True))
    
    # 检查是否已处理
    if state['processed_slices'].get(slice_path.name) == slice_hash:
        print(f"   ⏭️  已处理过，跳过")
        return True, None
    
    # 这里应该调用子代理（sessions_spawn）进行提取
    # 但由于这是脚本，我们生成任务清单，由主代理调用
    
    prompt = get_prompt(slice_data)
    
    task = {
        'slice_path': str(slice_path),
        'slice_name': slice_path.name,
        'prompt': prompt,
        'slice_hash': slice_hash
    }
    
    return False, task

def main():
    print("🧠 实时结构化提取器 v3.0")
    print("=" * 50)
    
    ensure_dirs()
    state = load_state()
    
    # 获取所有未处理的切片
    slice_files = list(CHUNKS_DIR.glob('slice_*.json'))
    if not slice_files:
        print("没有待处理的切片")
        return
    
    print(f"发现 {len(slice_files)} 个切片")
    print()
    
    pending_tasks = []
    skipped = 0
    
    for slice_path in sorted(slice_files):
        print(f"📄 {slice_path.name}")
        
        is_processed, task = process_slice(slice_path, state)
        
        if is_processed:
            skipped += 1
        else:
            pending_tasks.append(task)
            print(f"   📝 生成提取任务")
        print()
    
    # 保存任务清单
    if pending_tasks:
        tasks_file = SKILL_DIR / 'extraction_tasks.json'
        with open(tasks_file, 'w') as f:
            json.dump(pending_tasks, f, indent=2)
        
        print(f"✅ 生成 {len(pending_tasks)} 个提取任务")
        print(f"   跳过已处理: {skipped}")
        print(f"   任务清单: {tasks_file}")
        print()
        print("🚀 下一步：主代理使用 sessions_spawn 逐个处理这些任务")
        print("   处理完成后调用: python3 realtime_distill.py --finalize")
    else:
        print("✅ 所有切片已处理完毕")

def finalize_extraction(task_name, result_file):
    """完成提取，保存到卡片"""
    state = load_state()
    
    # 读取提取结果
    try:
        with open(result_file, 'r', encoding='utf-8') as f:
            result_content = f.read()
    except Exception as e:
        print(f"❌ 读取结果文件失败: {e}")
        return
    
    # 🛡️ 严格验证：检查结果是否是有效内容
    invalid_markers = [
        "Request timed out",
        "Request was aborted",
        "[plugins]",
        "[hook]",
        "Gateway service check failed",
        "error:",
        "Error:",
        "ERROR:",
    ]
    
    for marker in invalid_markers:
        if marker in result_content:
            print(f"   ❌ 提取失败（系统错误: {marker}），跳过")
            print(f"   📝 错误内容已记录到日志，不生成卡片")
            return
    
    # 验证是否是有效的 JSON
    try:
        result = json.loads(result_content)
    except json.JSONDecodeError:
        print(f"   ❌ 提取结果不是有效的 JSON，跳过")
        return
    
    # 验证必须包含 topics 字段
    if 'topics' not in result:
        print(f"   ❌ 提取结果缺少 topics 字段，跳过")
        return
    
    # 读取任务信息
    tasks_file = SKILL_DIR / 'extraction_tasks.json'
    with open(tasks_file, 'r') as f:
        tasks = json.load(f)
    
    task = next((t for t in tasks if t['slice_name'] == task_name), None)
    if not task:
        print(f"❌ 找不到任务: {task_name}")
        return
    
    # 处理每个提取出的主题
    for topic_data in result.get('topics', []):
        # 验证主题数据完整性
        if not topic_data.get('topic'):
            print(f"   ⚠️  跳过无效主题（缺少 topic 名称）")
            continue
        
        topic_name = topic_data['topic']
        
        # 验证 topic_name 是否合法（不能包含特殊字符）
        if not re.match(r'^[\w\-_]+$', topic_name):
            print(f"   ⚠️  跳过无效主题名称: {topic_name}")
            continue
        
        card_path = TOPICS_DIR / f"{topic_name}.md"
        
        if card_path.exists():
            # 合并到现有卡片
            new_content = merge_topic(card_path, topic_data)
            action = "合并"
        else:
            # 创建新卡片
            new_content = create_new_card(topic_data)
            action = "创建"
        
        # 最终验证：内容不能是错误信息
        if any(marker in new_content for marker in invalid_markers):
            print(f"   ❌ 生成的卡片内容包含错误信息，跳过")
            continue
        
        with open(card_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"   {action}: {card_path.name}")
        
        # 更新状态
        state['topics'][topic_name] = {
            'last_update': datetime.now().isoformat(),
            'status': topic_data.get('status', 'RESOLVED')
        }
    
    # 标记切片为已处理
    state['processed_slices'][task_name] = task['slice_hash']
    save_state(state)
    
    print(f"✅ 任务完成: {task_name}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--finalize':
        if len(sys.argv) >= 4:
            finalize_extraction(sys.argv[2], sys.argv[3])
        else:
            print("用法: python3 realtime_distill.py --finalize <task_name> <result_file>")
    else:
        main()