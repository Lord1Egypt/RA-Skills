#!/usr/bin/env python3
"""
Fill timesheet for a Zrise task.

Usage:
    python3 fill_timesheet.py --task-id 42341 --hours 1.5 --description "Phân tích requirement"
    python3 fill_timesheet.py --task-id 42341 --hours 0.5 --description "Review kết quả"
    python3 fill_timesheet.py --task-id 42341 --minutes 30 --description "Soạn checklist"

Fills account.analytic.line linked to the task.
"""
import argparse
import json
import sys
import xmlrpc.client
from datetime import datetime, date, timezone

from zrise_utils import connect_zrise



def fill_timesheet(task_id, hours, description):
    db, uid, secret, models, _url = connect_zrise()

    # Get task info
    tasks = models.execute_kw(db, uid, secret, 'project.task', 'read',
                              [[task_id]], {'fields': ['id', 'name', 'project_id', 'company_id']})
    if not tasks:
        print(f"❌ Task {task_id} not found")
        return False

    task = tasks[0]
    project_id = task.get('project_id', [None])[0]
    company_id = task.get('company_id')
    if isinstance(company_id, list):
        company_id = company_id[0]

    # Get employee for current user
    employees = models.execute_kw(db, uid, secret, 'hr.employee', 'search_read',
                                  [[('user_id', '=', uid)]],
                                  {'fields': ['id', 'name'], 'limit': 1})
    employee_id = employees[0]['id'] if employees else False
    employee_name = employees[0]['name'] if employees else f'User {uid}'

    # Create timesheet entry
    today_str = date.today().isoformat()
    values = {
        'name': description or f'AI workflow - Task #{task_id}',
        'task_id': task_id,
        'project_id': project_id,
        'unit_amount': hours,
        'date': today_str,
        'user_id': uid,
        'employee_id': employee_id,
        'company_id': company_id,
        'category': 'billable_time',
    }

    try:
        line_id = models.execute_kw(db, uid, secret, 'account.analytic.line', 'create', [values])
        print(f"✅ Timesheet logged: {hours}h for task #{task_id}")
        print(f"   Employee: {employee_name}")
        print(f"   Description: {description or values['name']}")
        print(f"   Date: {today_str}")
        print(f"   Line ID: {line_id}")
        return True
    except xmlrpc.client.Fault as e:
        # Try without category if that fails
        if 'category' in str(e):
            values.pop('category', None)
            try:
                line_id = models.execute_kw(db, uid, secret, 'account.analytic.line', 'create', [values])
                print(f"✅ Timesheet logged (no category): {hours}h for task #{task_id}")
                print(f"   Line ID: {line_id}")
                return True
            except xmlrpc.client.Fault as e2:
                print(f"❌ Timesheet create failed: {e2}")
                return False
        print(f"❌ Timesheet create failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Fill timesheet for Zrise task')
    parser.add_argument('--task-id', type=int, required=True, help='Zrise task ID')
    parser.add_argument('--hours', type=float, default=0, help='Hours worked')
    parser.add_argument('--minutes', type=float, default=0, help='Minutes worked')
    parser.add_argument('--description', default=None, help='Description of work done')
    args = parser.parse_args()

    total_hours = args.hours + (args.minutes / 60.0)
    if total_hours <= 0:
        print("❌ Cần chỉ định --hours hoặc --minutes")
        sys.exit(1)

    success = fill_timesheet(args.task_id, total_hours, args.description)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
