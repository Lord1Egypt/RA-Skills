#!/usr/bin/env python3
"""
超脑自动记录脚本
每次对话后自动执行，记录洞察、学习模式、检测盲区
"""

import sqlite3
import json
import re
from datetime import datetime
from pathlib import Path

DB_PATH = Path.home() / '.openclaw' / 'super-brain.db'

def get_connection():
    return sqlite3.connect(DB_PATH)

def extract_insight(user_msg, ai_msg):
    """提取对话洞察"""
    return {
        'topic': extract_topic(user_msg),
        'key_facts': extract_facts(user_msg, ai_msg),
        'mood': detect_mood(user_msg),
        'timestamp': datetime.now().isoformat()
    }

def extract_topic(msg):
    """提取主题"""
    # 简单的关键词提取
    keywords = ['超脑', '技能', '数据库', '代码', '设计', 'AI', '学习', '项目']
    for kw in keywords:
        if kw in msg:
            return kw
    return 'general'

def extract_facts(user_msg, ai_msg):
    """提取关键事实"""
    facts = []
    # 检测偏好
    if '简洁' in user_msg or '简单' in user_msg:
        facts.append('偏好简洁回复')
    if '详细' in user_msg or '展开' in user_msg:
        facts.append('偏好详细解释')
    if '表格' in user_msg:
        facts.append('偏好表格形式')
    return facts

def detect_mood(msg):
    """检测情绪"""
    positive = ['好', '赞', '👍', '谢谢', '太棒', '完美']
    negative = ['不对', '错', '差', '糟糕', '烦']
    confused = ['?', '？', '不懂', '没懂', '什么意思']
    
    if any(s in msg for s in positive):
        return 'positive'
    elif any(s in msg for s in negative):
        return 'negative'
    elif any(s in msg for s in confused):
        return 'confused'
    return 'neutral'

def classify_response(user_reaction):
    """分类响应模式"""
    effective = ['谢谢', '好的', '明白了', '对', '赞', '👍', '完美', '太棒', '可以', '懂了']
    ineffective = ['不对', '错了', '没懂', '不是', '???', '再说', '不明白', '不对', '错了']
    
    reaction_lower = user_reaction.lower()
    
    # 先检查ineffective，避免被effective误判
    if any(s in reaction_lower for s in ineffective):
        return 'ineffective'
    elif any(s in reaction_lower for s in effective):
        return 'effective'
    return 'neutral'

def record_session(user_id, session_id, messages):
    """记录完整会话"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # 1. 记录洞察
        for i in range(0, len(messages), 2):
            user_msg = messages[i] if i < len(messages) else ''
            ai_msg = messages[i+1] if i+1 < len(messages) else ''
            
            insight = extract_insight(user_msg, ai_msg)
            
            cursor.execute('''
                INSERT INTO conversation_insights 
                (id, user_id, session_id, topic, key_facts, user_mood, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', [
                f'insight-{session_id}-{i//2}',
                user_id,
                session_id,
                insight['topic'],
                json.dumps(insight['key_facts']),
                insight['mood'],
                insight['timestamp']
            ])
        
        # 2. 记录响应模式
        for i in range(1, len(messages)-1, 2):
            if i+1 < len(messages):
                ai_response = messages[i]
                user_reaction = messages[i+1]
                
                pattern_type = classify_response(user_reaction)
                
                if pattern_type != 'neutral':
                    cursor.execute('''
                        INSERT INTO response_patterns 
                        (id, user_id, pattern_type, trigger_context, what_i_did, 
                         user_reaction, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', [
                        f'pattern-{session_id}-{i//2}',
                        user_id,
                        pattern_type,
                        messages[i-1] if i > 0 else '',
                        ai_response[:200],  # 只存储前200字符
                        user_reaction,
                        datetime.now().isoformat()
                    ])
        
        # 3. 更新会话计数
        cursor.execute('''
            UPDATE user_profile 
            SET total_sessions = total_sessions + 1,
                last_session = ?
            WHERE user_id = ?
        ''', [datetime.now().isoformat(), user_id])
        
        conn.commit()
        print(f'✅ 会话 {session_id} 已记录')
        
    except Exception as e:
        print(f'❌ 记录失败: {e}')
        conn.rollback()
    finally:
        conn.close()

def detect_knowledge_gap(user_msg, ai_msg, user_id):
    """检测知识盲区"""
    # 用户不满意信号
    signals = ['不对', '错了', '不是', '不懂', '?', '???', '没明白']
    
    if any(s in user_msg for s in signals):
        conn = get_connection()
        cursor = conn.cursor()
        
        topic = extract_topic(user_msg)
        
        # 检查是否已存在
        cursor.execute('''
            SELECT id, frequency FROM knowledge_gaps 
            WHERE user_id = ? AND topic = ? AND status = 'detected'
        ''', [user_id, topic])
        
        existing = cursor.fetchone()
        
        if existing:
            # 更新频率
            cursor.execute('''
                UPDATE knowledge_gaps 
                SET frequency = frequency + 1, last_occurred = ?
                WHERE id = ?
            ''', [datetime.now().isoformat(), existing[0]])
        else:
            # 新增盲区
            cursor.execute('''
                INSERT INTO knowledge_gaps 
                (id, user_id, topic, context, frequency, suggested_action)
                VALUES (?, ?, ?, ?, 1, ?)
            ''', [
                f'gap-{datetime.now().strftime("%Y%m%d%H%M%S")}',
                user_id,
                topic,
                user_msg[:100],
                f'建议学习{topic}相关知识'
            ])
        
        conn.commit()
        conn.close()
        print(f'⚠️ 检测到知识盲区: {topic}')

def meta_analyze_session(user_id, session_id):
    """元认知分析会话"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 获取本次会话的洞察
    cursor.execute('''
        SELECT * FROM conversation_insights 
        WHERE user_id = ? AND session_id = ?
    ''', [user_id, session_id])
    
    insights = cursor.fetchall()
    
    # 获取响应模式
    cursor.execute('''
        SELECT pattern_type, COUNT(*) as cnt 
        FROM response_patterns 
        WHERE user_id = ? AND timestamp > datetime('now', '-1 day')
        GROUP BY pattern_type
    ''', [user_id])
    
    patterns = {row[0]: row[1] for row in cursor.fetchall()}
    
    # 计算性能指标
    total = patterns.get('effective', 0) + patterns.get('ineffective', 0)
    effective_rate = patterns.get('effective', 0) / total if total > 0 else 0.5
    
    # 记录进化日志
    cursor.execute('''
        INSERT INTO self_evolution_log 
        (id, user_id, evolution_type, after_state, improvement_score)
        VALUES (?, ?, ?, ?, ?)
    ''', [
        f'evo-{datetime.now().strftime("%Y%m%d%H%M%S")}',
        user_id,
        'performance_analysis',
        json.dumps({
            'effective_rate': effective_rate,
            'insights_count': len(insights),
            'patterns': patterns
        }),
        effective_rate
    ])
    
    # 记录性能指标
    cursor.execute('''
        INSERT INTO performance_metrics 
        (user_id, metric_name, metric_value)
        VALUES (?, ?, ?)
    ''', [user_id, 'effective_rate', effective_rate])
    
    conn.commit()
    conn.close()
    
    print(f'📊 元认知分析完成: 有效率 {effective_rate:.1%}')
    
    return effective_rate

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print('用法: python auto_record.py <user_id> <session_id> [messages_json]')
        sys.exit(1)
    
    user_id = sys.argv[1]
    session_id = sys.argv[2]
    
    if len(sys.argv) > 3:
        messages = json.loads(sys.argv[3])
        record_session(user_id, session_id, messages)
    
    meta_analyze_session(user_id, session_id)
