#!/usr/bin/env python3
import json
import sys


def main():
    data = json.loads(sys.stdin.read())
    title = data.get('task_name') or data.get('activity_summary') or '(no title)'
    project = data.get('project_name') or '-'
    stage = data.get('stage') or '-'
    deadline = data.get('deadline') or '-'
    link = data.get('link') or '-'
    wid = data['work_item_id']
    lines = [
        f"Zrise item mới: {title}",
        f"- Work item: {wid}",
        f"- Project: {project}",
        f"- Stage: {stage}",
        f"- Deadline: {deadline}",
        f"- Link: {link}",
        "",
        "Quick actions:",
        f"- {wid} phân tích trước",
        f"- {wid} làm luôn",
        f"- {wid} bỏ qua",
        "",
        "Nếu cần comment tự do thì reply bình thường."
    ]
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
