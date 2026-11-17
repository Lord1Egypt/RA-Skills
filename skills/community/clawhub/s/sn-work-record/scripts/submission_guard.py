"""Fail-closed ordinary-submission guard shared by CLI and imported API."""
from decimal import Decimal, InvalidOperation
from datetime import date
import hashlib
import re
import json
import os
import stat
import tempfile
from pathlib import Path
from contextlib import contextmanager
from urllib.parse import urlsplit


def normalized_host(host):
    if not isinstance(host, str):
        raise ValueError('无效 OA 地址')
    parsed = urlsplit(host)
    if parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path not in ('', '/'):
        raise ValueError('OA 地址必须为无凭据的 HTTP(S) origin')
    port = parsed.port
    authority = parsed.hostname.lower()
    if ':' in authority:
        authority = '[' + authority + ']'
    if port and port != (443 if parsed.scheme == 'https' else 80):
        authority += ':' + str(port)
    return parsed.scheme.lower() + '://' + authority


def token_fingerprint(session):
    headers = getattr(session, 'headers', None)
    if headers is None:
        raise ValueError('认证会话缺失')
    bearer = headers.get('Authorization')
    token = headers.get('Admin-OA-Token')
    if not isinstance(token, str) or not token or bearer != 'Bearer ' + token:
        raise ValueError('认证头缺失或不一致')
    return hashlib.sha256(token.encode()).hexdigest()


def bind_submission_session(session, host, account):
    """Explicitly bind a trusted authenticated session to its real OA account."""
    if not isinstance(account, str) or not account.strip():
        raise ValueError('提交必须绑定当前真实账号')
    session._sn_submission_context = (normalized_host(host), hashlib.sha256(account.encode()).hexdigest(), token_fingerprint(session))
    return session


def validate_scope(session, host, payload):
    expected = payload['timeEntryList'][0]
    if type(payload['saveOrSubmit']) is not int or payload['saveOrSubmit'] != 1:
        raise ValueError('草稿写入暂不支持安全去重；仅可预览，禁止写入')
    if expected['fillType'] != '1':
        raise ValueError('仅支持普通工作提交')
    if not isinstance(expected['projectName'], str) or not expected['projectName'].strip() or expected['boToPmStatus'] not in (0, 1):
        raise ValueError('项目名称必须为非空文字；项目属性必须为 0 或 1')
    fill_date = expected['fillDate']
    if not isinstance(fill_date, str) or not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', fill_date):
        raise ValueError('日期必须为 YYYY-MM-DD')
    date.fromisoformat(fill_date)
    for field in CODE_FIELDS:
        value = expected[field]
        if isinstance(value, bool) or not isinstance(value, (str, int)) or not re.fullmatch(r'0|[1-9][0-9]*', str(value)):
            raise ValueError('业务代码格式无效')
    import requests
    if isinstance(session, requests.Session):
        adapter = session.get_adapter(normalized_host(host) + '/sn/timeEntry/saveOrUpdate')
        if type(adapter) is not requests.adapters.HTTPAdapter or adapter.max_retries.total not in (0, False):
            raise ValueError('提交会话必须使用无自动重试的标准 HTTPAdapter')
    context = getattr(session, '_sn_submission_context', None)
    if not isinstance(context, tuple) or len(context) != 3 or context[0] != normalized_host(host) or not isinstance(context[1], str) or not re.fullmatch('[a-f0-9]{64}', context[1]) or context[2] != token_fingerprint(session):
        raise ValueError('提交会话未绑定当前 OA 地址/账号/认证头；请使用 OAAuth 或显式 bind_submission_session')
    return context

class SubmissionUncertain(RuntimeError):
    """A write may have happened; never resend without reconciliation."""


CODE_FIELDS = ('projectId', 'projectPhase', 'workType', 'boToPmStatus', 'fillType')


def same_record(record, expected, accepted_states=('20', '30')):
    if not isinstance(record, dict):
        return False
    try:
        for field in expected:
            actual = record[field]
            wanted = expected[field]
            if field == 'manHour':
                if isinstance(actual, bool) or not Decimal(str(actual)).is_finite() or Decimal(str(actual)) != Decimal(str(wanted)):
                    return False
            elif field == 'fillDate':
                # OA list returns a midnight timestamp; do not truncate arbitrary dates.
                if actual not in (wanted, wanted + ' 00:00:00'):
                    return False
            elif field in CODE_FIELDS:
                if isinstance(actual, bool) or not isinstance(actual, (str, int)) or str(actual) != str(wanted):
                    return False
            elif actual != wanted:
                return False
        return str(record['state']) in accepted_states and str(record['isDeleted']) == '0'
    except (KeyError, InvalidOperation, ValueError, TypeError):
        return False


def read_records(session, host, fill_date, query):
    records, raw = query(session, host, fill_date)
    if not isinstance(raw, dict) or not isinstance(raw.get('data'), list) or records != raw['data']:
        raise ValueError('工时查询缺失或格式不完整；禁止写入')
    if any(raw.get(flag, True) is not True for flag in ('isOk', 'complete', 'last')):
        raise ValueError('工时查询显式失败或不完整；禁止写入')
    if any(raw.get(flag, False) is not False for flag in ('hasMore', 'has_more')) or type(raw.get('total', len(records))) is not int or raw.get('total', len(records)) != len(records):
        raise ValueError('工时查询不完整；禁止写入')
    return records


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


def request_digest(expected):
    values = dict(expected)
    hours = format(Decimal(str(values['manHour'])), 'f')
    values['manHour'] = hours.rstrip('0').rstrip('.') if '.' in hours else hours
    for field in CODE_FIELDS:
        values[field] = str(values[field])
    return digest(values)


def guard_root():
    root = Path(os.environ.get('SN_WORK_RECORD_GUARD_DIR', Path.home() / '.local/state/sn-work-record/submission-guard')).expanduser().absolute()
    if any(part.is_symlink() for part in (root, *root.parents)):
        raise ValueError('提交保护目录不得包含符号链接')
    root.mkdir(parents=True, mode=0o700, exist_ok=True)
    info = root.stat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
        raise ValueError('提交保护目录必须为当前用户私有 0700 目录')
    return root


def private_open(path, flags):
    fd = os.open(path, flags | os.O_NOFOLLOW, 0o600)
    info = os.fstat(fd)
    if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077 or info.st_nlink != 1:
        os.close(fd)
        raise ValueError('提交保护文件必须为当前用户私有常规文件')
    return fd


def read_journal(path, scope):
    try:
        fd = private_open(path, os.O_RDONLY)
    except FileNotFoundError:
        return None
    with os.fdopen(fd) as stream:
        try:
            value = json.load(stream)
        except (ValueError, TypeError):
            raise SubmissionUncertain('提交保护日志损坏；禁止重发，请人工核实') from None
    if not isinstance(value, dict) or set(value) != {'version','scope','request','status'} or value['version'] != 1 or value['scope'] != scope or value['status'] not in ('pending','observed') or not isinstance(value['request'], str) or not re.fullmatch('[a-f0-9]{64}', value['request']):
        raise SubmissionUncertain('提交保护日志不匹配；禁止重发，请人工核实')
    return value


def save_journal(path, value):
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix='.journal-')
    try:
        with os.fdopen(fd, 'w') as stream:
            os.fchmod(stream.fileno(), 0o600)
            json.dump(value, stream, sort_keys=True)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@contextmanager
def day_lock(path):
    try:
        import fcntl
    except ImportError:
        raise ValueError('当前平台不支持安全本地锁；禁止写入') from None
    fd = private_open(path, os.O_RDWR | os.O_CREAT)
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            raise ValueError('同账号同日提交正在处理或无法加锁；禁止写入') from None
        yield
    finally:
        os.close(fd)  # Release automatically on exit/crash; never unlink locks.


def guarded_submit(session, host, payload, query, write):
    context = validate_scope(session, host, payload)
    expected = payload['timeEntryList'][0]
    scope = digest([context[0], context[1], expected['fillDate']])
    path = guard_root() / (scope + '.json')
    with day_lock(path.with_suffix('.lock')):
        return submit_locked(session, host, payload, query, write, path, scope, context)


def submit_locked(session, host, payload, query, write, path, scope, context):
    expected = payload['timeEntryList'][0]
    historical = read_journal(path, scope)
    fingerprint = request_digest(expected)
    records = read_records(session, host, expected['fillDate'], query)
    if validate_scope(session, host, payload) != context:
        raise ValueError('提交过程中认证绑定变化；禁止写入')
    if historical and historical['request'] != fingerprint:
        raise SubmissionUncertain('同日存在其他历史写入意图；禁止重发或覆盖，请人工核实')
    if len(records) == 1 and same_record(records[0], expected):
        if historical:
            save_journal(path, {**historical, 'status':'observed'})
        return dict(code=200, submission_status='skipped-existing', verified=True)
    if historical:
        raise SubmissionUncertain('历史写入结果尚无法确认；禁止重发，请只读核实')
    if records:
        raise ValueError('同日存在工时或记录状态/字段无法确认；禁止覆盖，请人工核实')
    marker = dict(version=1, scope=scope, request=fingerprint, status='pending')
    save_journal(path, marker)  # Durable intent before entering any write call.
    uncertain = False
    try:
        write()  # Exactly one attempt, regardless of HTTP/application outcome.
    except Exception:
        uncertain = True
    for attempt in range(3):
        try:
            if validate_scope(session, host, payload) != context:
                raise ValueError('binding changed')
        except Exception:
            raise SubmissionUncertain('写入后认证绑定变化；结果无法核实，禁止重发') from None
        if attempt:
            import time
            time.sleep(0.2)
        try:
            records = read_records(session, host, expected['fillDate'], query)
        except Exception:
            continue
        try:
            if validate_scope(session, host, payload) != context:
                raise ValueError('binding changed')
        except Exception:
            raise SubmissionUncertain('查询后认证绑定变化；结果无法核实，禁止重发') from None
        if len(records) == 1 and same_record(records[0], expected, accepted_states=('20',)):
            save_journal(path, {**marker, 'status':'observed'})
            return dict(code=200, submission_status='observed-after-uncertain' if uncertain else 'submitted-confirmed', verified=True)
        if records:
            raise SubmissionUncertain('写入后工时字段或状态存在冲突/缺失；禁止重发，请人工核实')
    raise SubmissionUncertain('工时写入结果未知或冲突；禁止重发，请只读核实服务端记录')
