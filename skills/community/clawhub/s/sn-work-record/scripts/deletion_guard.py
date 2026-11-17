"""Internal offline fake workflow only; not wired to production OA entrypoints.

No verified server recovery contract exists. Local locks are not server CAS;
fake readback does not establish isolation or reversibility. Never use this
callback-based experimental flow for real OA deletion/restoration.
"""
import json
import os
import re
from submission_guard import (SubmissionUncertain, normalized_host, token_fingerprint,
    digest, guard_root, day_lock, private_open, save_journal)

FIELDS = ('id', 'fillDate', 'projectId', 'projectName', 'projectPhase', 'workType',
          'manHour', 'jobDesc', 'boToPmStatus', 'fillType', 'state', 'isDeleted')
VOLATILE = ('updatedTime', 'updateTime', 'updatedAt', 'isDeleted')


def _context(session, host):
    context = getattr(session, '_sn_submission_context', None)
    if not isinstance(context, tuple) or len(context) != 3 or context[0] != normalized_host(host) or not re.fullmatch('[a-f0-9]{64}', str(context[1])) or context[2] != token_fingerprint(session):
        raise ValueError('删除/恢复会话未绑定当前账号、地址、认证头')
    import requests
    if isinstance(session, requests.Session):
        adapter = session.get_adapter(normalized_host(host) + '/sn/timeEntry/update')
        if type(adapter) is not requests.adapters.HTTPAdapter or adapter.max_retries.total not in (0, False):
            raise ValueError('删除/恢复禁止自动 HTTP 重试')
    return context


def _valid(detail, entry_id):
    if not isinstance(detail, dict) or any(k not in detail or detail[k] is None for k in FIELDS) or str(detail['id']) != entry_id or str(detail['isDeleted']) not in ('0', '1'):
        raise ValueError('完整记录字段或目标 ID 无法确认')
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}( 00:00:00)?', str(detail['fillDate'])):
        raise ValueError('记录日期无法确认')
    return detail


def _same(detail, backup, deleted):
    return (str(detail.get('isDeleted')) == str(deleted) and
            {k:v for k,v in detail.items() if k not in VOLATILE} ==
            {k:v for k,v in backup.items() if k not in VOLATILE})


def protected_change(session, host, entry_id, *, action, confirmation, read, write):
    if action not in ('delete', 'restore') or not isinstance(entry_id, str) or not re.fullmatch('[0-9]+', entry_id) or confirmation != entry_id:
        raise ValueError('必须显式确认目标记录及删除/恢复授权')
    context = _context(session, host)
    before = _valid(read(), entry_id)
    root = guard_root()
    scope = digest([context[0], context[1], before['fillDate'][:10]])
    path = root / ('deletion-' + digest([context[0], context[1], entry_id]) + '.json')
    with day_lock(root / (scope + '.lock')):
        before = _valid(read(), entry_id)
        if digest([context[0], context[1], before['fillDate'][:10]]) != scope:
            raise ValueError('记录日期在加锁期间变化；禁止写入')
        if _context(session, host) != context:
            raise ValueError('认证绑定已变化')
        try:
            fd = private_open(path, os.O_RDONLY)
        except FileNotFoundError:
            marker = None
        else:
            with os.fdopen(fd) as stream:
                try:
                    marker = json.load(stream)
                except Exception:
                    raise SubmissionUncertain('删除恢复日志损坏；禁止写入') from None
            if (not isinstance(marker, dict) or marker.get('scope') != scope or marker.get('binding') != list(context[:2]) or marker.get('backup_digest') != digest(marker.get('backup')) or marker.get('status') not in ('delete-pending', 'delete-confirmed', 'restore-pending', 'restore-confirmed')):
                raise SubmissionUncertain('删除恢复日志无效；禁止写入')
            _valid(marker['backup'], entry_id)
        deleted = 1 if action == 'delete' else 0
        if marker:
            backup = marker['backup']
            if marker['status'] == action + '-confirmed' and _same(before, backup, deleted):
                return dict(verified=True, status=action + '-already-confirmed')
            if marker['status'].endswith('-pending'):
                if marker['status'] == action + '-pending' and _same(before, backup, deleted):
                    save_journal(path, {**marker, 'status': action + '-confirmed'})
                    return dict(verified=True, status=action + '-observed-without-resend')
                raise SubmissionUncertain('历史删除/恢复结果未知；禁止重发')
            if action != 'restore' or marker['status'] != 'delete-confirmed' or not _same(before, backup, 1):
                raise SubmissionUncertain('历史删除恢复意图或字段冲突；禁止写入')
        else:
            if action != 'delete' or str(before['isDeleted']) != '0':
                raise ValueError('无原始备份或不是有效记录；禁止写入')
            marker = dict(scope=scope, binding=list(context[:2]), backup=before,
                          backup_digest=digest(before), status='delete-pending')
            backup = before
        marker = {**marker, 'status': action + '-pending'}
        save_journal(path, marker)  # Full backup and intent fsynced before write.
        try:
            write(deleted)  # Exactly once; failures do not authorize retransmission.
        except Exception:
            pass
        try:
            after = _valid(read(), entry_id)
            if _context(session, host) != context or not _same(after, backup, deleted):
                raise ValueError('readback mismatch')
        except Exception:
            raise SubmissionUncertain('删除/恢复结果未知；保留完整备份及保护日志，禁止重发') from None
        save_journal(path, {**marker, 'status': action + '-confirmed'})
        return dict(verified=True, status=action + '-confirmed')
