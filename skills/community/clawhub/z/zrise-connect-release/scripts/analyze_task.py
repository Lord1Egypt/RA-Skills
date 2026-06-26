#!/usr/bin/env python3
"""
Analyze task and create plan. Reads task from folder, saves plan to folder.

Usage:
    python3 analyze_task.py --task-dir /path/to/.tasks/42356 --message "tạo checklist"
    # Reads: task.json
    # Writes: plan.json (with workflow, agent, plan text)
"""
import argparse
import json
import sys
from pathlib import Path

WORKFLOW_AGENTS = {
    'requirement-analysis': {'keywords': ['yêu cầu', 'requirement', 'checklist', 'phân tích nghiệp vụ', 'BRD', 'SRS', 'user story', 'use case'], 'agent': 'demo-ba', 'role': 'Business Analyst'},
    'email-draft': {'keywords': ['email', 'thư', 'soạn email', 'notification', 'thông báo'], 'agent': 'ai-company', 'role': 'Email Writer'},
    'technical-design': {'keywords': ['thiết kế', 'design', 'architecture', 'schema', 'API', 'database', 'technical'], 'agent': 'demo-architect', 'role': 'Technical Architect'},
    'ui-design': {'keywords': ['UI', 'UX', 'giao diện', 'mockup', 'wireframe', 'layout'], 'agent': 'demo-design', 'role': 'UI/UX Designer'},
    'development': {'keywords': ['code', 'lập trình', 'implement', 'develop', 'build', 'fix bug', 'refactor'], 'agent': 'demo-be', 'role': 'Developer'},
    'testing': {'keywords': ['test', 'qa', 'kiểm thử', 'test case', 'bug', 'verify'], 'agent': 'demo-qc', 'role': 'QA Engineer'},
    'general': {'keywords': [], 'agent': 'ai-company', 'role': 'AI Assistant'},
}


def detect_workflow(name, description, user_message):
    combined = f"{name} {description} {user_message}".lower()
    best_match = 'general'
    best_score = 0
    for wf, config in WORKFLOW_AGENTS.items():
        if wf == 'general':
            continue
        score = sum(1 for kw in config['keywords'] if kw.lower() in combined)
        if score > best_score:
            best_score = score
            best_match = wf
    return best_match


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--task-dir', required=True, help='Path to task folder')
    parser.add_argument('--message', default='')
    parser.add_argument('--task-id', type=int, default=0)
    args = parser.parse_args()
    # Strip whitespace from task_dir
    if hasattr(args, 'task_dir') and args.task_dir:
        args.task_dir = args.task_dir.strip()

    task_dir = Path(args.task_dir)
    task_file = task_dir / 'task.json'
    task = json.loads(task_file.read_text(encoding='utf-8'))

    workflow = detect_workflow(task.get('name', ''), task.get('description', ''), args.message)
    wf_config = WORKFLOW_AGENTS.get(workflow, WORKFLOW_AGENTS['general'])

    plan = {
        'task_id': task['task_id'],
        'intent': args.message or task.get('name', ''),
        'workflow': workflow,
        'suggested_agent': wf_config['agent'],
        'suggested_role': wf_config['role'],
        'plan': f"## Hướng xử lý: {task['name']}\n\n**Workflow:** {workflow}\n**Agent:** {wf_config['agent']} ({wf_config['role']})\n**Mô tả:** {(task.get('description','') or '')[:300]}\n\n### Steps:\n1. Đọc kỹ task\n2. Phân tích theo workflow `{workflow}`\n3. Tạo output chất lượng\n4. Review trước khi gửi\n",
        'task_context': task,
    }

    plan_file = task_dir / 'plan.json'
    plan_file.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(plan, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
