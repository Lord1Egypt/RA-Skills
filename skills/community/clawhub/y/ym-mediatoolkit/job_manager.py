import json
import queue
import re
import shutil
import threading
import time
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path


ACTIVE_STATUSES = {'queued', 'running'}
TERMINAL_STATUSES = {'success', 'partial', 'skipped', 'error'}
JOB_ID_PATTERN = re.compile(r'^[a-f0-9]{32}$')


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def collect_output_paths(value) -> list:
    paths = []
    seen = set()

    def add(path: str):
        if path in seen:
            return
        seen.add(path)
        paths.append(path)

    def walk(item):
        if isinstance(item, dict):
            for key, child in item.items():
                if key in ('output_path', 'saved_path', 'manifest_path', 'outputPath') and isinstance(child, str):
                    add(child)
                else:
                    walk(child)
        elif isinstance(item, list):
            for child in item:
                walk(child)

    walk(value)
    return paths

def protocol_error(code: str, message: str, status: str = 'error') -> dict:
    hints = {
        'invalid_action': '请传入当前 skill 支持的 action 名称。',
        'invalid_params': 'params 必须是 JSON object。',
        'invalid_job_id': 'job_id 必须是 32 位十六进制字符串。',
        'job_not_found': '请确认 job_id 是否正确，或任务文件是否仍存在。',
        'job_interrupted': '任务未完成，可能是服务重启或进程中断，请重新提交。',
        'job_failed': '任务执行失败，请查看 result 或 error 字段。',
        'invalid_json': '请求体必须是 JSON object。',
        'invalid_async_mode': 'async 仅支持 JSON boolean 或字符串 "auto"。',
        'invalid_wait_timeout': 'wait_timeout_sec 必须是 0 到 30 之间的数字。',
    }
    return {
        'status': status,
        'code': code,
        'message': message,
        'reply': f'没有处理成功：{message}' if status == 'error' else message,
        'hint': hints.get(code, '请查看 message 字段获取具体原因。'),
    }


class JobManager:
    def __init__(self, action_handlers: dict, jobs_dir: str = 'output/jobs', autostart: bool = True):
        self.action_handlers = action_handlers
        self.jobs_dir = Path(jobs_dir)
        self.jobs_dir.mkdir(parents=True, exist_ok=True)
        self.queue = queue.Queue()
        self._thread = None
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self._mark_interrupted_jobs()
        if autostart:
            self.start()

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(target=self._worker_loop, name='ym-job-worker', daemon=True)
        self._thread.start()

    def submit(self, action: str, params=None, metadata=None) -> dict:
        if action not in self.action_handlers:
            return protocol_error('invalid_action', f'Invalid action: {action}')
        if params is None:
            params = {}
        if not isinstance(params, dict):
            return protocol_error('invalid_params', 'params must be an object')
        if metadata is None:
            metadata = {}
        if not isinstance(metadata, dict):
            metadata = {}

        job_id = uuid.uuid4().hex
        job_path = self._job_path(job_id)
        job = {
            'job_id': job_id,
            'action': action,
            'params': params,
            'created_by': metadata.get('created_by'),
            'intent': metadata.get('intent'),
            'source': metadata.get('source'),
            'metadata': metadata,
            'status': 'queued',
            'code': 'ok',
            'reply': f'任务已提交：{job_id}',
            'hint': '可通过 poll_url 查询任务状态。',
            'created_at': utc_now(),
            'started_at': None,
            'finished_at': None,
            'result': None,
            'output_paths': [],
            'error': None,
        }
        self._write_job(job)
        self.queue.put(job_id)
        return {
            'status': 'queued',
            'code': 'ok',
            'reply': f'任务已提交：{job_id}',
            'job_id': job_id,
            'job_path': str(job_path),
            'poll_url': f'/skill/jobs/{job_id}',
            'created_by': metadata.get('created_by'),
            'intent': metadata.get('intent'),
            'action': action,
            'params': params,
        }

    def get_job(self, job_id: str) -> dict:
        if not self._valid_job_id(job_id):
            return protocol_error('invalid_job_id', f'Invalid job_id: {job_id}')
        path = self._job_path(job_id)
        if not path.exists():
            return protocol_error('job_not_found', f'Job not found: {job_id}')
        return self._read_job(path)

    def list_jobs(self, status: str = None, limit: int = 50) -> dict:
        try:
            limit = max(1, min(200, int(limit)))
        except (TypeError, ValueError):
            limit = 50

        jobs = []
        for path in self.jobs_dir.glob('*/job.json'):
            try:
                job = self._read_job(path)
            except (OSError, json.JSONDecodeError):
                continue
            if status and job.get('status') != status:
                continue
            jobs.append(job)

        jobs.sort(key=lambda item: item.get('created_at') or '', reverse=True)
        return {
            'status': 'success',
            'code': 'ok',
            'reply': '已获取任务列表。',
            'hint': '处理完成。',
            'total': len(jobs),
            'jobs': jobs[:limit],
        }

    def wait_for_job(self, job_id: str, timeout: float = 5.0) -> dict:
        deadline = time.time() + timeout
        while time.time() < deadline:
            job = self.get_job(job_id)
            if job.get('status') in TERMINAL_STATUSES:
                return job
            time.sleep(0.02)
        return self.get_job(job_id)

    def _worker_loop(self):
        while not self._stop_event.is_set():
            try:
                job_id = self.queue.get(timeout=0.2)
            except queue.Empty:
                continue
            try:
                self._run_job(job_id)
            finally:
                self.queue.task_done()

    def _run_job(self, job_id: str):
        job = self.get_job(job_id)
        if job.get('status') != 'queued':
            return

        job['status'] = 'running'
        job['started_at'] = utc_now()
        job['reply'] = f'任务执行中：{job_id}'
        job['hint'] = '任务正在执行，请稍后再次轮询。'
        self._write_job(job)

        action = job['action']
        handler = self.action_handlers.get(action)
        if handler is None:
            result = protocol_error('invalid_action', f'Invalid action: {action}')
        else:
            try:
                result = handler(job.get('params') or {})
            except Exception as e:
                result = protocol_error('job_failed', str(e))

        if not isinstance(result, dict):
            result = protocol_error('job_failed', f'Invalid action result for {action}')

        final_status = result.get('status') if result.get('status') in TERMINAL_STATUSES else 'error'
        job['status'] = final_status
        job['code'] = result.get('code') or ('ok' if final_status in ('success', 'partial', 'skipped') else 'error')
        job['reply'] = result.get('reply') or ('任务处理完成。' if final_status != 'error' else f"没有处理成功：{result.get('message', '未知错误')}")
        job['hint'] = result.get('hint') or ('处理完成。' if final_status != 'error' else '请查看 result 或 error 字段。')
        job['finished_at'] = utc_now()
        job['result'] = result
        job['output_paths'] = collect_output_paths(result)
        job['error'] = result.get('message') if final_status == 'error' else None
        self._write_job(job)

    def cleanup_jobs(self, retention_days: int = 7, max_jobs: int = 200) -> dict:
        now = datetime.now(timezone.utc)
        try:
            retention_days = max(0, int(retention_days))
        except (TypeError, ValueError):
            retention_days = 7
        try:
            max_jobs = max(1, int(max_jobs))
        except (TypeError, ValueError):
            max_jobs = 200

        terminal_jobs = []
        deleted = 0
        for path in self.jobs_dir.glob('*/job.json'):
            try:
                job = self._read_job(path)
            except (OSError, json.JSONDecodeError):
                continue
            if job.get('status') not in TERMINAL_STATUSES:
                continue
            stamp = self._parse_time(job.get('finished_at') or job.get('created_at'))
            terminal_jobs.append((stamp, path, job))

        cutoff_deleted = set()
        for stamp, path, _job in terminal_jobs:
            if stamp and now - stamp >= timedelta(days=retention_days):
                if self._delete_job_dir(path):
                    deleted += 1
                    cutoff_deleted.add(path)

        remaining = [item for item in terminal_jobs if item[1] not in cutoff_deleted]
        remaining.sort(key=lambda item: item[0] or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
        for _stamp, path, _job in remaining[max_jobs:]:
            if self._delete_job_dir(path):
                deleted += 1

        return {
            'status': 'success',
            'code': 'ok',
            'reply': f'已清理 {deleted} 个历史任务。',
            'deleted': deleted,
        }

    def _mark_interrupted_jobs(self):
        for path in self.jobs_dir.glob('*/job.json'):
            try:
                job = self._read_job(path)
            except (OSError, json.JSONDecodeError):
                continue
            if job.get('status') not in ACTIVE_STATUSES:
                continue
            job['status'] = 'error'
            job['code'] = 'job_interrupted'
            job['reply'] = f"没有处理成功：任务未完成，服务已重启或进程已中断"
            job['hint'] = '任务未完成，可能是服务重启或进程中断，请重新提交。'
            job['finished_at'] = utc_now()
            job['error'] = 'Job was interrupted before completion'
            self._write_job(job)

    def _job_path(self, job_id: str) -> Path:
        return self.jobs_dir / job_id / 'job.json'

    def _valid_job_id(self, job_id: str) -> bool:
        return isinstance(job_id, str) and JOB_ID_PATTERN.match(job_id) is not None

    def _read_job(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding='utf-8'))

    def _write_job(self, job: dict):
        path = self._job_path(job['job_id'])
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = path.with_suffix('.json.tmp')
        with self._lock:
            tmp_path.write_text(json.dumps(job, ensure_ascii=False, indent=2), encoding='utf-8')
            tmp_path.replace(path)

    def _parse_time(self, value: str):
        if not value:
            return None
        try:
            parsed = datetime.fromisoformat(value)
        except (TypeError, ValueError):
            return None
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)
        return parsed

    def _delete_job_dir(self, job_path: Path) -> bool:
        try:
            shutil.rmtree(job_path.parent)
            return True
        except OSError:
            return False
