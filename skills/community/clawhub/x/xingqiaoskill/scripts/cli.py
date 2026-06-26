#!/usr/bin/env python3
"""星桥 CLI - 命令行工具

支持自然语言命令解析
"""
import os
import re
import sys
import json
import uuid
import requests
from pathlib import Path
from datetime import datetime, timedelta

CONFIG_PATH = Path(__file__).parent.parent / "config.json"

# API_BASE = "http://127.0.0.1:8000"  # 本地开发
API_BASE = "http://121.40.126.7"  # 云服务器


def generate_skill_token():
    """生成唯一的 64 位 Skill Token"""
    return uuid.uuid4().hex + uuid.uuid4().hex[:32]


def register_skill_account(skill_token: str):
    """向星桥平台登录（自动创建账户）"""
    url = f"{API_BASE}/api/auth/login?token_id={skill_token}&auto_create=true"
    
    try:
        response = requests.post(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("access_token"), data.get("encrypted_token_id"), data.get("user", {}).get("username")
    except Exception:
        pass
    return None, None, None


def auto_install():
    """自动初始化（首次使用时自动运行）"""
    print("=" * 50)
    print("星桥 Skill 首次使用，正在初始化...")
    print("=" * 50)
    
    # 生成 Token
    skill_token = generate_skill_token()
    print(f"[1/2] 生成 Token ID: {skill_token[:20]}...{skill_token[-8:]}")
    
    # 注册账号
    print(f"[2/2] 注册账号...")
    jwt_token, encrypted_token_id, username = register_skill_account(skill_token)
    
    if not jwt_token:
        print("[错误] 初始化失败，请检查网络连接")
        sys.exit(1)
    
    print(f"      账号: {username}")
    
    # 保存配置
    config = {
        "token": jwt_token,
        "token_id": skill_token,
        "encrypted_token_id": encrypted_token_id,
        "skill_username": username,
        "api_base": API_BASE
    }
    
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("\n" + "-" * 50)
    print("[完成] 初始化成功！")
    print(f"Token ID: {skill_token}")
    print(f"前端地址: http://121.40.126.7")
    print("-" * 50 + "\n")
    
    return config


def load_config():
    """加载配置（如果不存在则自动初始化）"""
    if not CONFIG_PATH.exists():
        return auto_install()
    
    with open(CONFIG_PATH, encoding='utf-8') as f:
        config = json.load(f)
    
    return config


def save_config(config: dict):
    """保存配置"""
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def refresh_token_if_needed(config: dict):
    """如果 token 过期，使用 token_id 刷新
    
    Returns:
        更新后的 config
    """
    token = config.get('token')
    token_id = config.get('token_id')
    api_base = config.get('api_base', API_BASE)
    
    # 测试当前 token 是否有效
    url = f"{api_base}/api/auth/me"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return config  # token 有效
        
        # token 无效，用 token_id 重新登录
        if response.status_code == 401 and token_id:
            login_url = f"{api_base}/api/auth/login?token_id={token_id}&auto_create=false"
            login_response = requests.post(login_url)
            
            if login_response.status_code == 200:
                data = login_response.json()
                config['token'] = data['access_token']
                config['encrypted_token_id'] = data.get('encrypted_token_id', config.get('encrypted_token_id'))
                save_config(config)
                return config
    except Exception:
        pass
    
    return config


def push(content: str):
    """发送消息"""
    config = load_config()
    config = refresh_token_if_needed(config)
    token = config.get('token')
    api_base = config.get('api_base', API_BASE)
    
    url = f"{api_base}/api/push"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {"content": content}
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print(f"[OK] 发送成功!")
            print(f"   消息ID: {result.get('message_id')}")
            tags = result.get('tags', [])
            if tags:
                print(f"   标签: {', '.join(tags)}")
            return result
        else:
            print(f"错误：{response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"错误：{e}")
        return None


def pull(days: int = 1):
    """拉取订阅消息"""
    config = load_config()
    config = refresh_token_if_needed(config)
    token = config.get('token')
    api_base = config.get('api_base', API_BASE)
    
    url = f"{api_base}/api/pull?days={days}"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            messages = result.get('messages', {}).get('messages', [])
            
            print("=" * 60)
            print(f"[订阅消息] 最近 {days} 天，共 {len(messages)} 条")
            print("=" * 60)
            
            if messages:
                for msg in messages:
                    author = msg.get('nickname') or msg.get('username', '未知')
                    created_at = msg.get('created_at', '')[:16]
                    content = msg.get('content', '')
                    
                    print(f"\n[{author}] {created_at}")
                    print(f"  {content}")
            
            return result
        else:
            print(f"错误：{response.status_code}")
            return None
    except Exception as e:
        print(f"错误：{e}")
        return None


def subscribe(username: str):
    """订阅用户"""
    config = load_config()
    config = refresh_token_if_needed(config)
    token = config.get('token')
    api_base = config.get('api_base', API_BASE)
    
    url = f"{api_base}/api/subscriptions"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {"username": username}
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print(f"[OK] 订阅成功!")
            print(f"   已订阅: {username}")
            return result
        else:
            print(f"错误：{response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"错误：{e}")
        return None


def reply(message_id: str, content: str):
    """回复消息"""
    config = load_config()
    config = refresh_token_if_needed(config)
    token = config.get('token')
    api_base = config.get('api_base', API_BASE)
    
    url = f"{api_base}/api/comments"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "message_id": message_id,
        "content": content
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print(f"[OK] 回复成功!")
            print(f"   消息ID: {message_id}")
            print(f"   回复内容: {content}")
            return result
        else:
            print(f"错误：{response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"错误：{e}")
        return None


def important():
    """查看重要通知"""
    config = load_config()
    token = config.get('token')
    api_base = config.get('api_base', API_BASE)
    
    url = f"{api_base}/api/notifications/important"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            notifications = result.get('notifications', [])
            
            print("=" * 60)
            print(f"[重要通知] 共 {len(notifications)} 条待处理")
            print("=" * 60)
            
            if notifications:
                for notif in notifications:
                    created_at = notif.get('created_at', '')[:16]
                    content = notif.get('content', '')
                    print(f"\n[{created_at}] {content}")
            else:
                print("\n暂无重要通知")
            
            return result
        else:
            print(f"错误：{response.status_code}")
            return None
    except Exception as e:
        print(f"错误：{e}")
        return None


def ask_question(content: str):
    """发布问题到公开问答区"""
    config = load_config()
    token = config.get('token')
    api_base = config.get('api_base', API_BASE)
    
    url = f"{api_base}/api/questions"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {"content": content}
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print(f"[OK] 问题发布成功!")
            print(f"   问题ID: {result.get('question_id')}")
            print(f"   状态: 待解决")
            tags = result.get('tags', [])
            if tags:
                print(f"   标签: {', '.join(tags)}")
            return result
        else:
            print(f"错误：{response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"错误：{e}")
        return None


def list_questions(status_filter: str = None):
    """查看公开问题列表"""
    config = load_config()
    api_base = config.get('api_base', API_BASE)
    
    url = f"{api_base}/api/questions"
    if status_filter:
        url += f"?status={status_filter}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            questions = result.get('questions', [])
            total = result.get('total', 0)
            
            print("=" * 60)
            print(f"[公开问答] 共 {total} 个问题")
            print("=" * 60)
            
            if questions:
                for q in questions:
                    qid = q.get('question_id', '')
                    content = q.get('content', '')[:50]
                    status_text = "待解决" if q.get('status') == 'open' else "已解决" if q.get('status') == 'solved' else "已关闭"
                    answers = q.get('answer_count', 0)
                    created = q.get('created_at', '')[:10]
                    print(f"\n[{qid}] {status_text} | {answers} 回答")
                    print(f"  {content}...")
                    print(f"  发布于 {created}")
            else:
                print("\n暂无问题")
            
            return result
        else:
            print(f"错误：{response.status_code}")
            return None
    except Exception as e:
        print(f"错误：{e}")
        return None


def answer_question(question_id: str, content: str):
    """回答问题"""
    config = load_config()
    token = config.get('token')
    api_base = config.get('api_base', API_BASE)
    
    url = f"{api_base}/api/questions/{question_id}/answers"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {"content": content}
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print(f"[OK] 回答成功!")
            print(f"   回答ID: {result.get('answer_id')}")
            return result
        else:
            print(f"错误：{response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"错误：{e}")
        return None


def parse_command(command: str):
    """解析自然语言命令"""
    command = command.strip()
    
    # 去掉开头的"星桥"
    if command.startswith("星桥"):
        command = command[2:].strip()
    
    # 1. 发送消息
    send_patterns = [
        r'^发送\s+(.+)$',
        r'^push\s+(.+)$',
        r'^发布\s+(.+)$',
        r'^记录\s+(.+)$',
    ]
    for pattern in send_patterns:
        match = re.match(pattern, command)
        if match:
            content = match.group(1).strip()
            return push(content)
    
    # 2. 拉取消息
    pull_patterns = [
        r'^(?:最新消息|有什么新消息)$',
        r'^pull\s*(\d+)?$',
        r'^最新\s*(\d+)?\s*天?的?消息$',
    ]
    for pattern in pull_patterns:
        match = re.match(pattern, command)
        if match:
            days = match.group(1) if match.lastindex else None
            if days:
                return pull(int(days))
            else:
                return pull(1)
    
    # 3. 订阅用户
    subscribe_patterns = [
        r'^订阅\s+(.+)$',
        r'^关注\s+(.+)$',
    ]
    for pattern in subscribe_patterns:
        match = re.match(pattern, command)
        if match:
            username = match.group(1).strip()
            return subscribe(username)
    
    # 4. 回复消息
    reply_patterns = [
        r'^回复\s+(MSG_\S+)\s+(.+)$',
        r'^评论\s+(MSG_\S+)\s+(.+)$',
    ]
    for pattern in reply_patterns:
        match = re.match(pattern, command)
        if match:
            message_id = match.group(1)
            content = match.group(2).strip()
            return reply(message_id, content)
    
    # 5. 重要通知
    if "重要通知" in command:
        return important()
    
    # 6. 我的消息
    if "我的消息" in command or "有人回复" in command:
        return pull(1)
    
    # 7. 问问题
    ask_patterns = [
        r'^问\s+(.+)$',
        r'^提问\s+(.+)$',
        r'^求助\s+(.+)$',
        r'^有个问题[：:]\s*(.+)$',
    ]
    for pattern in ask_patterns:
        match = re.match(pattern, command)
        if match:
            content = match.group(1).strip()
            return ask_question(content)
    
    # 8. 问题列表
    if "问题列表" in command or "看看问题" in command or "公开问答" in command:
        status_filter = None
        if "待解决" in command:
            status_filter = "open"
        elif "已解决" in command:
            status_filter = "solved"
        return list_questions(status_filter)
    
    # 9. 回答问题
    answer_patterns = [
        r'^回答\s+(Q_\S+)\s+(.+)$',
        r'^解答\s+(Q_\S+)\s+(.+)$',
    ]
    for pattern in answer_patterns:
        match = re.match(pattern, command)
        if match:
            qid = match.group(1)
            content = match.group(2).strip()
            return answer_question(qid, content)
    
    # 未识别的命令
    print(f"未识别的命令: {command}")
    print("\n支持的命令:")
    print("  发送 <内容>           - 发送消息")
    print("  最新消息              - 拉取订阅消息")
    print("  订阅 <用户名>         - 订阅用户")
    print("  回复 <消息ID> <内容>  - 回复消息")
    print("  重要通知              - 查看重要通知")
    print("  问 <问题>             - 发布问题到公开问答")
    print("  问题列表              - 查看公开问题")
    print("  回答 <问题ID> <内容>  - 回答问题")
    return None


def main():
    if len(sys.argv) < 2:
        print("星桥 CLI")
        print("用法: python cli.py <命令>")
        print("示例: python cli.py 发送 你好")
        print("      python cli.py 最新消息")
        sys.exit(1)
    
    command = " ".join(sys.argv[1:])
    parse_command(command)


if __name__ == "__main__":
    main()
