#!/usr/bin/env python3
"""
添加 PubMed 文献综述任务
用法: python3 scripts/add_pubmed_task.py "<主题词>"
"""
import sys
import os
import json
import random
import string
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
TASKS_DIR = os.path.join(BASE_DIR, 'tasks')
TASKS_FILE = os.path.join(TASKS_DIR, 'ablesci_tasks.json')
os.makedirs(TASKS_DIR, exist_ok=True)

def random_id(length=4):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

def add_pubmed_task(topic, max_articles=20):
    now = datetime.now()
    task_id = f"pubmed_{int(now.timestamp() * 1000)}_{random_id()}"
    first_check = now + timedelta(minutes=1)

    new_task = {
        'id': task_id,
        'type': 'pubmed_review',
        'payload': {
            'topic': topic,
            'max_articles': max_articles
        },
        'processor': 'pubmed_summary',
        'status': 'pending',
        'enabled': True,
        'created_at': now.isoformat() + 'Z',
        'fetched_count': 0,
        'error': None
    }

    tasks = load_tasks()
    tasks.append(new_task)
    save_tasks(tasks)

    return task_id, new_task

def main():
    if len(sys.argv) < 2:
        print("用法: python3 scripts/add_pubmed_task.py <主题词>")
        sys.exit(1)

    topic = sys.argv[1]
    if len(sys.argv) > 2:
        max_articles = int(sys.argv[2])
    else:
        max_articles = 20

    task_id, task = add_pubmed_task(topic, max_articles)
    print(f"✅ 任务已创建: {task_id}")
    print(f"   主题: {topic}")
    print(f"   类型: pubmed_review")
    print(f"   processor: pubmed_summary")
    print(f"   状态: pending")
    print(f"   最大文章数: {max_articles}")

if __name__ == '__main__':
    main()
