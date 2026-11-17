#!/usr/bin/env python3
"""Produce a non-mutating migration report for normalized reminder rules.

This tool never connects to a scheduler.  A platform adapter exports its rules
as JSON and may apply the report only after a human has reviewed it.
"""

import argparse
import json
import sys
from pathlib import Path

from task_store import MAIN, StoreError, TaskStore


def load_rules(path):
    value = json.loads(Path(path).read_text(encoding='utf-8'))
    rules = value.get('rules') if isinstance(value, dict) else value
    if not isinstance(rules, list):
        raise ValueError('rules input must be an array or an object with a rules array')
    seen = set()
    for rule in rules:
        if not isinstance(rule, dict) or not isinstance(rule.get('id'), str) or not rule['id']:
            raise ValueError('every rule needs a non-empty string id')
        if rule['id'] in seen:
            raise ValueError('duplicate rule id: ' + rule['id'])
        seen.add(rule['id'])
        if 'taskId' in rule and not isinstance(rule['taskId'], str):
            raise ValueError('taskId must be a string')
        if 'dynamic' in rule and type(rule['dynamic']) is not bool:
            raise ValueError('dynamic must be boolean')
        if 'oneShot' in rule and type(rule['oneShot']) is not bool:
            raise ValueError('oneShot must be boolean')
    return rules


def report(data_dir, rules):
    doc = TaskStore(data_dir).execute({'op': 'read'})['ledgers'][MAIN]
    tasks = {task['id']: task for task in doc['tasks']}
    result = {'linked': [], 'pendingMigration': [], 'orphans': [], 'shouldDisable': [],
              'proposedChanges': []}
    for rule in rules:
        task_id = rule.get('taskId')
        if not isinstance(task_id, str) or not task_id:
            entry = {'ruleId': rule['id'], 'reason': 'missing_task_id', 'recommendedAction': 'pause'}
            result['orphans'].append(entry)
            result['shouldDisable'].append(entry)
            continue
        task = tasks.get(task_id)
        if task is None:
            entry = {'ruleId': rule['id'], 'taskId': task_id, 'reason': 'task_not_found',
                     'recommendedAction': 'pause'}
            result['orphans'].append(entry)
            result['shouldDisable'].append(entry)
            continue
        base = {'ruleId': rule['id'], 'taskId': task_id, 'taskStatus': task['status']}
        if task['status'] in ('done', 'cancelled') and rule.get('oneShot', False):
            result['shouldDisable'].append({**base, 'reason': 'inactive_one_shot',
                                            'recommendedAction': 'disable'})
            continue
        if rule.get('dynamic') is True:
            result['linked'].append(base)
        else:
            result['pendingMigration'].append(base)
            result['proposedChanges'].append({**base, 'action': 'update',
                'template': 'task_id_runtime_resolution',
                'note': 'Store only taskId and schedule; render content when the rule runs.'})
    result['summary'] = {key: len(value) for key, value in result.items() if isinstance(value, list)}
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', required=True, help='local team-tasks data directory')
    parser.add_argument('--rules', required=True, help='normalized adapter export JSON')
    args = parser.parse_args(argv)
    try:
        output = report(Path(args.data_dir), load_rules(args.rules))
        print(json.dumps({'ok': True, 'dryRun': True, **output}, ensure_ascii=False, indent=2))
        return 0
    except (StoreError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({'ok': False, 'message': str(exc)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    sys.exit(main())
