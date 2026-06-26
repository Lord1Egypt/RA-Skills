#!/usr/bin/env python3
"""
invoke_agent_for_task.py — Wrapper to invoke OpenClaw Agent for task processing.

This script is called by Lobster workflows to process tasks via OpenClaw Agent.
Replaces direct Gemini API calls with OpenClaw Agent invocation.

Usage:
    python3 invoke_agent_for_task.py --task-id 42174 --workflow general
    python3 invoke_agent_for_task.py --task-id 42174 --workflow requirement-analysis --feedback "add details"
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPTS_DIR))

from zrise_utils import get_root, connect_zrise

ROOT = get_root()

WORKFLOW_PROMPTS = {
    'general': """Bạn là AI Assistant xử lý task tổng quát.

Hãy xử lý task này. Output:
1. **Summary** — Tóm tắt vấn đề
2. **Analysis** — Phân tích chi tiết
3. **Recommendations** — Đề xuất hành động
4. **Next steps** — Bước tiếp theo cụ thể
5. **Risks** — Rủi ro cần lưu ý

Viết bằng tiếng Việt, rõ ràng, actionable.""",

    'requirement-analysis': """Bạn là Business Analyst. Hãy phân tích requirement cho task này.

Output:
1. **User Stories** — Format: 'As a [role], I want [feature] so that [benefit]'
2. **Acceptance Criteria** — Measurable, testable
3. **Questions cần làm rõ** — List questions cho PO/Stakeholder
4. **Assumptions** — Giả định đang có
5. **Priority recommendation** — P0/P1/P2 với lý do
6. **Risks** — Identify key risks

Viết bằng tiếng Việt, concrete, actionable.""",

    'technical-design': """Bạn là Solution Architect. Hãy thiết kế kỹ thuật cho task này.

Output:
1. **Architecture overview** — Component diagram description
2. **Data model changes** — Tables/fields cần thêm/sửa
3. **API endpoints** — Method, path, request/response
4. **Integration points** — Hệ thống cần kết nối
5. **Technical decisions** — Choice + rationale
6. **Non-functional requirements** — Performance, security, scalability

Viết bằng tiếng Việt, technical, detailed.""",

    'implementation': """Bạn là Developer. Hãy phân tích implementation cho task này.

Output:
1. **Files cần thay đổi** — List với mô tả changes
2. **Implementation plan** — Từng bước cụ thể
3. **Code patterns** — Patterns/frameworks nên dùng
4. **Dependencies** — Packages, services cần thêm
5. **Estimated effort** — Số giờ, complexity
6. **Potential issues** — Edge cases, gotchas

Viết bằng tiếng Việt, technical, actionable.""",

    'code-review': """Bạn là Senior Developer/Reviewer. Hãy review code/design cho task này.

Output:
1. **Strengths** — Điểm tốt
2. **Issues** — Bugs, code smells, security issues
3. **Suggestions** — Improvements cụ thể
4. **Risk assessment** — Impact của các issue
5. **Priority** — Issues nên fix trước
6. **Overall verdict** — Approve / Request changes / Reject

Viết bằng tiếng Việt, critical but constructive.""",

    'testing': """Bạn là QA Engineer. Hãy lên kế hoạch test cho task này.

Output:
1. **Test scenarios** — Happy path + edge cases
2. **Test cases** — Input, expected output, priority
3. **Automation candidates** — Cases nên automate
4. **Test data needed** — Mock data, fixtures
5. **Coverage gaps** — Areas dễ bỏ sót
6. **Acceptance checklist** — Go/no-go criteria

Viết bằng tiếng Việt, comprehensive, testable.""",

    'documentation': """Bạn là Technical Writer. Hãy tạo documentation cho task này.

Output:
1. **Document structure** — Outline tài liệu cần viết
2. **Content draft** — Nội dung chính
3. **Target audience** — Ai sẽ đọc tài liệu này
4. **Missing info** — Thông tin cần thu thập thêm
5. **Related docs** — Tài liệu liên quan cần reference

Viết bằng tiếng Việt, clear, structured.""",
}


def fetch_task_data(task_id):
    """Fetch task from Zrise."""
    import re
    db, uid, secret, models, url = connect_zrise()
    tasks = models.execute_kw(db, uid, secret, 'project.task', 'read',
                              [[task_id]], {'fields': ['id', 'name', 'description',
                                                      'stage_id', 'project_id',
                                                      'date_deadline', 'priority']})
    if not tasks:
        return None
    t = tasks[0]
    desc = re.sub('<[^<]+?>', '', t.get('description', ''))
    return {
        'task_id': t['id'],
        'name': t.get('name'),
        'description': desc[:3000] if desc else '',
        'stage': (t.get('stage_id') or [None, 'Unknown'])[1],
        'project': (t.get('project_id') or [None, 'Unknown'])[1],
        'deadline': t.get('date_deadline'),
        'priority': t.get('priority', '0'),
        'link': f"{url}/web#id={t['id']}&model=project.task&view_type=form",
    }


def invoke_agent(task_id, workflow, feedback=''):
    """Invoke OpenClaw Agent to process task."""
    
    # Fetch task
    task = fetch_task_data(task_id)
    if not task:
        return {'error': f'Task {task_id} not found'}
    
    # Get prompt template
    prompt_template = WORKFLOW_PROMPTS.get(workflow, WORKFLOW_PROMPTS['general'])
    
    # Build full prompt
    feedback_section = f"\n\n**Feedback từ review (cần xử lý):**\n{feedback}\n" if feedback else ""
    
    full_prompt = f"""{prompt_template}

## Task Context
- **Task ID:** {task['task_id']}
- **Name:** {task['name']}
- **Project:** {task['project']}
- **Stage:** {task['stage']}
- **Priority:** {task['priority']}
- **Deadline:** {task['deadline'] or 'N/A'}

## Description
{task['description'][:2000]}
{feedback_section}
"""
    
    # Invoke OpenClaw Agent via subprocess
    # Note: In real implementation, this would use openclaw.invoke or sessions_spawn
    # For now, we'll use a simple subprocess call to simulate
    
    try:
        # Method 1: Try using openclaw CLI if available
        result = subprocess.run(
            ['openclaw', 'invoke', '--agent', 'zrise-analyst', '--task', full_prompt],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            output = result.stdout.strip()
        else:
            # Fallback: Generate template output
            output = generate_fallback_output(task, workflow, feedback)
    
    except FileNotFoundError:
        # openclaw CLI not found - use fallback
        output = generate_fallback_output(task, workflow, feedback)
    except subprocess.TimeoutExpired:
        return {'error': 'Agent invocation timeout'}
    except Exception as e:
        output = generate_fallback_output(task, workflow, feedback)
    
    return {
        'task_id': task_id,
        'workflow': workflow,
        'task_name': task['name'],
        'project': task['project'],
        'result': output,
        'task_context': task,
        'source': 'openclaw-agent',
    }


def generate_fallback_output(task, workflow, feedback=''):
    """Generate template output when OpenClaw Agent unavailable."""
    prompt = WORKFLOW_PROMPTS.get(workflow, WORKFLOW_PROMPTS['general'])
    feedback_section = f"\n\n**Feedback cần xử lý:** {feedback}" if feedback else ""
    
    return f"""# {workflow.replace('-', ' ').title()} — Workflow Output

## Task Info
- **Task ID:** {task['task_id']}
- **Name:** {task['name']}
- **Project:** {task['project']}
- **Stage:** {task['stage']}

## Workflow: {workflow}

{prompt[:500]}

## Lưu ý
⚠️ OpenClaw Agent không khả dụng. Output này là template cơ bản.

## Next Steps
1. Đảm bảo OpenClaw Agent được cấu hình đúng
2. Chạy lại workflow khi Agent available
3. Review kết quả
{feedback_section}

---
*Generated by fallback template (OpenClaw Agent unavailable)*
"""


def main():
    parser = argparse.ArgumentParser(description='Invoke OpenClaw Agent for task')
    parser.add_argument('--task-id', type=int, required=True)
    parser.add_argument('--workflow', default='general')
    parser.add_argument('--feedback', default='')
    parser.add_argument('--stdin', action='store_true', help='Read task_id from stdin JSON')
    args = parser.parse_args()
    
    if args.stdin:
        input_data = json.loads(sys.stdin.read())
        task_id = input_data.get('task_id', args.task_id)
        workflow = input_data.get('workflow', args.workflow)
        feedback = input_data.get('feedback', args.feedback)
    else:
        task_id = args.task_id
        workflow = args.workflow
        feedback = args.feedback
    
    result = invoke_agent(task_id, workflow, feedback)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
