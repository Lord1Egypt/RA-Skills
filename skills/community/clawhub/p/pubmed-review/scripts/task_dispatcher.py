#!/usr/bin/env python3
import json
import os
import socket
import time
import fcntl
import subprocess

# 路径配置（去硬编码）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)  # scripts/ 的父目录即为项目根目录
TASK_FILE = os.path.join(BASE_DIR, 'tasks', 'ablesci_tasks.json')
LOCK_FILE = os.environ.get('DISPATCHER_LOCK', os.path.join(BASE_DIR, '.locks', 'dispatcher.lock'))

def load_tasks():
    with open(TASK_FILE, 'r') as f:
        return json.load(f)

def save_tasks(tasks):
    tmp = TASK_FILE + '.tmp.' + str(os.getpid())
    with open(tmp, 'w') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, TASK_FILE)

def claim_task(task, my_pid):
    lock = task.get('lock', {})
    stored_pid = lock.get('pid')
    if stored_pid:
        if stored_pid == my_pid:
            return True
        if time.time() - lock.get('locked_at', 0) > 600:
            task['lock'] = {'pid': None, 'hostname': None, 'locked_at': None}
            return True
        try:
            os.kill(stored_pid, 0)
            return False
        except OSError:
            task['lock'] = {'pid': None, 'hostname': None, 'locked_at': None}
            return True
    task['lock'] = {'pid': my_pid, 'hostname': socket.gethostname(), 'locked_at': time.time()}
    return True

def clear_lock(task):
    task['lock'] = {'pid': None, 'hostname': None, 'locked_at': None}

def run_ablesci(task):
    # pubmed-review-skill 不处理 ablesci 任务，仅记录日志
    doi = task.get('payload', {}).get('doi', 'unknown')
    print(f'[SKIP] ablesci task not supported in pubmed-review-skill: {doi}')

def run_pubmed(task):
    task_id = task['id']
    topic = task['payload']['topic']
    processor = task.get('processor', 'pubmed_summary')
    print(f'[RUN] pubmed_review {task_id} [topic={topic}] [processor={processor}]')
    os.chdir(BASE_DIR)
    subprocess.run(['python3', 'scripts/run_pubmed_review.py', task_id], check=False)

def dispatch():
    my_pid = os.getpid()
    lock_fd = open(LOCK_FILE, 'w')
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print(f'[SKIP] 另一个 dispatcher 正在运行 (PID from lock file)')
        return

    tasks = load_tasks()
    changed = False
    for task in tasks:
        if not task.get('enabled', True):
            continue

        if task.get('type') == 'ablesci':
            if not claim_task(task, my_pid):
                print(f'[SKIP] {task["payload"]["doi"]} 已被 PID={task["lock"]["pid"]} 领取')
                continue
            changed = True
            save_tasks(tasks)
            try:
                run_ablesci(task)
            finally:
                clear_lock(task)
                save_tasks(tasks)

        elif task.get('type') == 'pubmed_review':
            # 一次性任务：跳过已完成/失败的任务
            if task.get('status') in ('completed', 'failed'):
                continue
            if not claim_task(task, my_pid):
                print(f'[SKIP] pubmed_review {task["id"]} 已被领取')
                continue
            changed = True
            save_tasks(tasks)
            try:
                run_pubmed(task)
            finally:
                # run_pubmed_review.py 已管理 status 和 enabled，这里只清 lock
                clear_lock(task)
                # 重新加载最新状态再保存，避免用旧 in-memory 数据覆盖
                tasks = load_tasks()
                for t in tasks:
                    if t['id'] == task['id']:
                        t['lock'] = {'pid': None, 'hostname': None, 'locked_at': None}
                        break
                save_tasks(tasks)

    fcntl.flock(lock_fd, fcntl.LOCK_UN)

if __name__ == '__main__':
    dispatch()
