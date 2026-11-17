#!/usr/bin/env python3
"""
企业微信语音消息 Agent - 会话管理器
管理对话上下文，支持创建、查询、清理会话
新增：情感状态跟踪（v2.2）
新增：方言检测跟踪 + 工单关联（v2.3）
"""

import json
import sys
import os
import hashlib
import time
from datetime import datetime

# 会话存储目录
SESSION_DIR = os.path.join(os.path.dirname(__file__), '..', 'temp_sessions')

def ensure_dir():
    """确保存储目录存在"""
    if not os.path.exists(SESSION_DIR):
        os.makedirs(SESSION_DIR)

def make_session_id(userid):
    """根据用户ID生成会话ID"""
    ts = int(time.time())
    raw = f"{userid}_{ts}"
    return hashlib.md5(raw.encode()).hexdigest()[:16]

def create_session(userid, max_history=5):
    """创建新会话"""
    ensure_dir()
    session_id = make_session_id(userid)
    
    session = {
        "session_id": session_id,
        "userid": userid,
        "messages": [],
        "current_intent": None,
        "collected_entities": {},
        "awaiting": None,
        "created_at": int(time.time()),
        "updated_at": int(time.time()),
        "max_history": max_history,
        "active": True,
        "emotion_state": {
            "current_emotion": "neutral",
            "consecutive_negative": 0,
            "emotion_history": [],
            "should_escalate": False
        },
        "dialect_state": {
            "detected_dialect": "mandarin",
            "confidence": 0.0,
            "dialect_history": []
        },
        "ticket_ids": []
    }
    
    save_session(session)
    return session

def save_session(session):
    """保存会话到文件"""
    ensure_dir()
    filepath = os.path.join(SESSION_DIR, f"{session['session_id']}.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(session, f, ensure_ascii=False, indent=2)

def get_session(session_id):
    """获取会话"""
    filepath = os.path.join(SESSION_DIR, f"{session_id}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def get_active_session(userid):
    """获取用户的活跃会话（最近2分钟内有更新的）"""
    ensure_dir()
    threshold = int(time.time()) - 120
    for filename in os.listdir(SESSION_DIR):
        if filename.endswith('.json'):
            filepath = os.path.join(SESSION_DIR, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    session = json.load(f)
                if session.get('userid') == userid and session.get('updated_at', 0) > threshold:
                    return session
            except:
                continue
    return None

def add_message(session_id, role, content, intent=None, emotion=None):
    """向会话添加消息
    
    Args:
        session_id: 会话ID
        role: user 或 assistant
        content: 消息内容
        intent: 意图类型
        emotion: 情感类型 (angry/anxious/satisfied/confused/neutral)
    """
    session = get_session(session_id)
    if not session:
        return None
    
    message = {
        "role": role,
        "content": content,
        "timestamp": int(time.time()),
        "intent": intent
    }
    
    # 如果有情感信息，添加到消息中
    if emotion:
        message["emotion"] = emotion
    
    session['messages'].append(message)
    session['updated_at'] = int(time.time())
    
    # 更新情感状态
    if emotion:
        update_emotion_state(session, emotion)
    
    # 压缩历史消息（仅当 max_history >= 2 时执行）
    if session['max_history'] >= 2 and len(session['messages']) > session['max_history']:
        # 保留第一条 + 最近 max_history-2 条
        first = session['messages'][0]
        last_n = session['messages'][-(session['max_history']-2):]
        session['messages'] = [first] + last_n
    elif session['max_history'] < 2 and len(session['messages']) > 2:
        # max_history < 2 时只保留最近 1 条
        session['messages'] = session['messages'][-1:]
    
    save_session(session)
    return session


def update_emotion_state(session, emotion):
    """更新会话的情感状态
    
    Args:
        session: 会话对象
        emotion: 情感类型字符串
    """
    # 确保 emotion_state 存在
    if "emotion_state" not in session:
        session["emotion_state"] = {
            "current_emotion": "neutral",
            "consecutive_negative": 0,
            "emotion_history": [],
            "should_escalate": False
        }
    
    state = session["emotion_state"]
    
    # 更新当前情感
    state["current_emotion"] = emotion
    
    # 记录情感历史
    state["emotion_history"].append({
        "emotion": emotion,
        "timestamp": int(time.time())
    })
    
    # 限制历史记录长度
    if len(state["emotion_history"]) > 10:
        state["emotion_history"] = state["emotion_history"][-10:]
    
    # 负面情感计数
    negative_emotions = {"angry", "anxious"}
    if emotion in negative_emotions:
        state["consecutive_negative"] += 1
    else:
        state["consecutive_negative"] = 0
    
    # 判断是否应升级（超过阈值2）
    state["should_escalate"] = state["consecutive_negative"] > 2
    
    # 更新到会话中
    session["emotion_state"] = state


def get_emotion_state(session_id):
    """获取会话的情感状态
    
    Args:
        session_id: 会话ID
        
    Returns:
        dict: 情感状态，不存在返回 None
    """
    session = get_session(session_id)
    if not session:
        return None
    return session.get("emotion_state", {
        "current_emotion": "neutral",
        "consecutive_negative": 0,
        "emotion_history": [],
        "should_escalate": False
    })

def update_dialect_state(session_id, dialect, confidence=0.0):
    """更新会话的方言状态
    
    Args:
        session_id: 会话ID
        dialect: 检测到的方言类型字符串
        confidence: 置信度
    """
    session = get_session(session_id)
    if not session:
        return None
    
    # 确保 dialect_state 存在
    if "dialect_state" not in session:
        session["dialect_state"] = {
            "detected_dialect": "mandarin",
            "confidence": 0.0,
            "dialect_history": []
        }
    
    state = session["dialect_state"]
    state["detected_dialect"] = dialect
    state["confidence"] = confidence
    state["dialect_history"].append({
        "dialect": dialect,
        "confidence": confidence,
        "timestamp": int(time.time())
    })
    
    # 限制历史长度
    if len(state["dialect_history"]) > 10:
        state["dialect_history"] = state["dialect_history"][-10:]
    
    session["dialect_state"] = state
    session["updated_at"] = int(time.time())
    save_session(session)
    return session


def get_dialect_state(session_id):
    """获取会话的方言状态
    
    Args:
        session_id: 会话ID
        
    Returns:
        dict: 方言状态，不存在返回 None
    """
    session = get_session(session_id)
    if not session:
        return None
    return session.get("dialect_state", {
        "detected_dialect": "mandarin",
        "confidence": 0.0,
        "dialect_history": []
    })


def add_ticket_id(session_id, ticket_id):
    """为会话添加工单ID关联
    
    Args:
        session_id: 会话ID
        ticket_id: 工单ID
    """
    session = get_session(session_id)
    if not session:
        return None
    
    if ticket_id not in session["ticket_ids"]:
        session["ticket_ids"].append(ticket_id)
        session["updated_at"] = int(time.time())
        save_session(session)
    
    return session


def get_session_tickets(session_id):
    """获取会话关联的工单ID列表
    
    Args:
        session_id: 会话ID
        
    Returns:
        list: 工单ID列表
    """
    session = get_session(session_id)
    if not session:
        return []
    return session.get("ticket_ids", [])


def cleanup_expired(timeout=120):
    """清理过期会话"""
    ensure_dir()
    threshold = int(time.time()) - timeout
    removed = []
    
    for filename in os.listdir(SESSION_DIR):
        if filename.endswith('.json'):
            filepath = os.path.join(SESSION_DIR, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    session = json.load(f)
                if session.get('updated_at', 0) < threshold:
                    os.remove(filepath)
                    removed.append(session['session_id'])
            except:
                continue
    
    return removed

def get_stats():
    """获取会话统计"""
    ensure_dir()
    files = [f for f in os.listdir(SESSION_DIR) if f.endswith('.json')]
    files.sort()
    
    sessions = []
    for filename in files:
        filepath = os.path.join(SESSION_DIR, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                session = json.load(f)
                sessions.append({
                    "session_id": session['session_id'],
                    "userid": session['userid'],
                    "msg_count": len(session['messages']),
                    "created_at": datetime.fromtimestamp(session['created_at']).strftime("%H:%M:%S"),
                    "updated_at": datetime.fromtimestamp(session['updated_at']).strftime("%H:%M:%S"),
                    "active": time.time() - session['updated_at'] < 120
                })
        except:
            continue
    
    return sessions

def show_help():
    """显示帮助信息"""
    help_text = """
企业微信语音消息 Agent - 会话管理器

用法：
    python session_manager.py <action> [options]

命令：
    create   创建新会话
        --userid  <用户ID>
        [--max-history <最大消息数，默认5>]

    get      获取会话信息
        --session-id <会话ID>
        --format <输出格式: json|table>

    find     查找用户活跃会话
        --userid <用户ID>

    add      向会话添加消息
        --session-id <会话ID>
        --role <角色: user|assistant>
        --content <消息内容>
        [--intent <意图类型>]

    cleanup  清理过期会话
        [--timeout <超时秒数，默认120>]

    stats    列出所有会话统计

    help     显示帮助信息

示例：
    python session_manager.py create --userid zhangsan
    python session_manager.py get --session-id abc123 --format table
    python session_manager.py find --userid zhangsan
    python session_manager.py add --session-id abc123 --user --content "您好"
    python session_manager.py cleanup --timeout 180
    python session_manager.py stats
"""
    print(help_text)

def main():
    """主函数"""
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    action = sys.argv[1]
    
    # 简单的参数解析
    args = {}
    i = 2
    while i < len(sys.argv):
        if sys.argv[i].startswith('--'):
            key = sys.argv[i][2:]
            if i + 1 < len(sys.argv) and not sys.argv[i+1].startswith('--'):
                args[key] = sys.argv[i+1]
                i += 2
            else:
                args[key] = True
                i += 1
        else:
            i += 1
    
    if action == 'create':
        userid = args.get('userid', 'unknown')
        max_history = int(args.get('max_history', 5))
        session = create_session(userid, max_history)
        print(json.dumps({"status": "success", "session_id": session['session_id']}, ensure_ascii=False))
    
    elif action == 'get':
        session_id = args.get('session_id', '')
        output_format = args.get('format', 'json')
        session = get_session(session_id)
        
        if not session:
            print(json.dumps({"status": "error", "message": "会话不存在"}, ensure_ascii=False))
            sys.exit(1)
        
        if output_format == 'table':
            print(f"\n{'='*60}")
            print(f"📋 会话信息")
            print(f"{'='*60}")
            print(f"会话ID: {session['session_id']}")
            print(f"用户: {session['userid']}")
            print(f"消息数: {len(session['messages'])}")
            print(f"创建时间: {datetime.fromtimestamp(session['created_at']).strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"最后活动: {datetime.fromtimestamp(session['updated_at']).strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"活跃状态: {'🟢' if time.time() - session['updated_at'] < 120 else '🔴'}")
            print(f"当前意图: {session.get('current_intent', '无')}")
            print(f"实体信息: {json.dumps(session.get('collected_entities', {}), ensure_ascii=False)}")
            print(f"{'='*60}\n")
            if session['messages']:
                print("📜 消息历史:")
                for msg in session['messages']:
                    role = '👤' if msg['role'] == 'user' else '🤖'
                    ts = datetime.fromtimestamp(msg['timestamp']).strftime('%H:%M:%S')
                    print(f"  {role} [{ts}] {msg['content']}")
        else:
            print(json.dumps(session, ensure_ascii=False, indent=2))
    
    elif action == 'find':
        userid = args.get('userid', '')
        session = get_active_session(userid)
        if session:
            print(json.dumps(session, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({"status": "no_active_session", "userid": userid}, ensure_ascii=False))
    
    elif action == 'add':
        session_id = args.get('session_id', '')
        role = args.get('role', 'user')
        content = args.get('content', '')
        intent = args.get('intent')
        
        session = add_message(session_id, role, content, intent)
        if session:
            print(json.dumps({"status": "success", "session_id": session['session_id']}, ensure_ascii=False))
        else:
            print(json.dumps({"status": "error", "message": "会话不存在"}, ensure_ascii=False))
            sys.exit(1)
    
    elif action == 'cleanup':
        timeout = int(args.get('timeout', 120))
        removed = cleanup_expired(timeout)
        print(json.dumps({"status": "success", "removed": removed, "count": len(removed)}, ensure_ascii=False))
    
    elif action == 'stats':
        sessions = get_stats()
        if not sessions:
            print("当前没有活跃会话")
            return
        
        print(f"\n{'='*70}")
        print(f"📊 会话统计（共 {len(sessions)} 个）")
        print(f"{'='*70}")
        print(f"{'会话ID':<18} {'用户':<12} {'消息数':<8} {'创建时间':<10} {'状态':<6}")
        print(f"{'-'*70}")
        for s in sessions:
            status = '🟢' if s['active'] else '🔴'
            print(f"{s['session_id']:<18} {s['userid']:<12} {s['msg_count']:<8} {s['created_at']:<10} {status}")
        print(f"{'='*70}\n")
    
    elif action == 'help':
        show_help()
    
    else:
        print(f"未知命令: {action}")
        show_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
