"""Existing-record amendment; never route through the new-submission API.

The captured existing-edit contract uses a weekday suffix on save, while all
same-day list requests use a pure ISO date. Identity/business fields are copied
from the current row; UI-only metadata is deliberately not resent.
"""
from datetime import date
import re
import submission_guard as sg

BUSINESS = ('id', 'projectId', 'projectName', 'projectPhase', 'workType',
            'boToPmStatus', 'manHour', 'fillType', 'fillUserId', 'isDeleted')


def _http(session, host, endpoint, payload=None):
    method = session.get if payload is None else session.post
    kwargs = dict(timeout=30, allow_redirects=False)
    if payload is not None:
        kwargs['json'] = payload
    response = method(host + endpoint, **kwargs)
    response.raise_for_status()
    if not 200 <= response.status_code < 300:
        raise ValueError('OA 响应不是成功状态；禁止继续')
    result = response.json()
    code = result.get('code') if isinstance(result, dict) else None
    if (type(code) not in (str, int) or code not in (200, '200')
            or result.get('isOk', True) is not True):
        raise ValueError('OA 请求失败；禁止继续')
    return result


def _identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r'[1-9][0-9]*', value):
        raise ValueError('工时/填写人 ID 必须为原始规范数字字符串；禁止修正')


def _day(value):
    if not isinstance(value, str) or not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}( 00:00:00)?', value):
        raise ValueError('工时日期格式无法确认')
    day = value[:10]
    date.fromisoformat(day)
    return day


def _validate_row(row, entry_id, day):
    from decimal import Decimal, InvalidOperation
    if not isinstance(row, dict) or any(key not in row for key in (*BUSINESS, 'fillDate', 'jobDesc', 'state', 'procInsId')):
        raise ValueError('工时记录缺失必填字段')
    _identifier(row['id'])
    _identifier(row['fillUserId'])
    if row['id'] != entry_id or _day(row['fillDate']) != day:
        raise ValueError('工时 ID/日期不匹配')
    if type(row['state']) not in (str, int) or str(row['state']) != '20' or type(row['isDeleted']) not in (str, int) or str(row['isDeleted']) != '0':
        raise ValueError('仅支持未删除的审批中工时；禁止撤回')
    proc = row['procInsId']
    if not isinstance(proc, str) or not re.fullmatch(r'[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*', proc):
        raise ValueError('缺少规范流程实例 ID；禁止撤回')
    if not isinstance(row['jobDesc'], str) or not row['jobDesc'].strip():
        raise ValueError('原描述无法确认')
    try:
        hours = Decimal(str(row['manHour']))
        if isinstance(row['manHour'], bool) or not hours.is_finite() or not 0 < hours <= 24:
            raise ValueError('工时时长无效')
    except InvalidOperation:
        raise ValueError('工时时长无效') from None


def _context(session, host):
    context = getattr(session, '_sn_submission_context', None)
    if not isinstance(context, tuple) or len(context) != 3 or context[0] != host or not isinstance(context[1], str) or not re.fullmatch('[a-f0-9]{64}', context[1]) or context[2] != sg.token_fingerprint(session):
        raise ValueError('认证绑定无效或变化；禁止继续')
    import requests
    if isinstance(session, requests.Session):
        # Check every mounted adapter, including endpoint-specific mounts.
        # Recheck at each boundary so a changed mount cannot enable a replay.
        for adapter in session.adapters.values():
            if type(adapter) is not requests.adapters.HTTPAdapter or adapter.max_retries.total not in (0, False):
                raise ValueError('修改会话必须使用无自动重试的标准 HTTPAdapter')
    return context


def _read_journal(path, scope):
    import json
    import os
    try:
        fd = sg.private_open(path, os.O_RDONLY)
    except FileNotFoundError:
        return None
    with os.fdopen(fd) as stream:
        try:
            value = json.load(stream)
        except (ValueError, TypeError):
            raise sg.SubmissionUncertain('修改日志损坏；撤回可能已发生，未重新提交；禁止重发') from None
    if (not isinstance(value, dict) or set(value) != {'version','scope','request','base','target','status'}
            or type(value['version']) is not int or value['version'] != 1 or value['scope'] != scope
            or value['status'] not in ('stop-pending','withdrawn','save-pending','observed')
            or any(not isinstance(value[key], str) or not re.fullmatch('[a-f0-9]{64}', value[key]) for key in ('request','base','target'))):
        raise sg.SubmissionUncertain('修改日志不匹配；撤回可能已发生，未重新提交；禁止重发')
    return value


def _record_digest(row, day, description=None):
    values = {key:row[key] for key in BUSINESS}
    values.update(fillDate=day, jobDesc=row['jobDesc'] if description is None else description)
    return sg.digest(values)


def amend_time_entry(session, host, entry_id, job_desc, *, preview=False, withdraw_resubmit=False):
    """Read/preview or explicitly withdraw and amend ONE existing ordinary row.

    All writes are single attempts. Durable uncertain phases only reconcile by
    reads; neither a new description nor another invocation may replace them.
    The lock filename is exactly the ordinary submission guard's account/day lock.
    """
    _identifier(entry_id)
    if not isinstance(job_desc, str) or not job_desc.strip():
        raise ValueError('必须提供非空新描述')
    if not preview and not withdraw_resubmit:
        raise ValueError('撤回重提必须明确授权 --withdraw-resubmit')
    host = sg.normalized_host(host)
    context = _context(session, host)

    def stable():
        if _context(session, host) != context:
            raise ValueError('认证绑定变化；禁止继续')

    def fetch(endpoint, payload=None):
        stable()
        result = _http(session, host, endpoint, payload)
        stable()
        return result

    detail = fetch('/sn/timeEntry/details/' + entry_id).get('data')
    if not isinstance(detail, dict):
        raise ValueError('详情不完整')
    day = _day(detail.get('fillDate'))

    def read():
        def query(s, h, d):
            raw = fetch('/sn/timeEntry/findEveryDayList', {'fillDate':d})
            return raw.get('data'), raw
        rows = sg.read_records(session, host, day, query)
        if len(rows) != 1 or not isinstance(rows[0], dict):
            raise ValueError('必须恰有一条完整同日工时')
        return rows[0]

    def initial():
        _validate_row(detail, entry_id, day)
        scope_payload = {'timeEntryList':[{**detail,'fillType':str(detail['fillType']),'fillDate':day}], 'saveOrSubmit':1}
        if sg.validate_scope(session, host, scope_payload) != context:
            raise ValueError('认证绑定变化；禁止继续')
        row = read()
        _validate_row(row, entry_id, day)
        if sg.validate_scope(session, host, {'timeEntryList':[{**row,'fillType':str(row['fillType']),'fillDate':day}], 'saveOrSubmit':1}) != context:
            raise ValueError('认证绑定变化；禁止继续')
        for key in (*BUSINESS, 'jobDesc', 'procInsId'):
            if type(row[key]) is not type(detail[key]) or row[key] != detail[key]:
                raise ValueError('详情与当日列表不一致；禁止撤回')
        return row

    if preview:
        row = initial()
        return dict(amendment_status='skipped-existing' if row['jobDesc'] == job_desc else 'preview',
                    verified=row['jobDesc'] == job_desc, detail={**row,'jobDesc':job_desc})

    scope = sg.digest([context[0], context[1], day])
    root = sg.guard_root()
    path = root / (scope + '.amend.json')
    with sg.day_lock(root / (scope + '.lock')):
        historical = _read_journal(path, scope)
        ordinary = sg.read_journal(root / (scope + '.json'), scope)
        if ordinary and ordinary['status'] != 'observed':
            raise sg.SubmissionUncertain('普通提交仍有未核实意图；禁止撤回或重新提交')
        request = sg.digest([scope, entry_id, job_desc])
        if historical and historical['status'] != 'observed':
            # Do not replace an unresolved intent, even with different wording.
            if historical['request'] != request:
                raise sg.SubmissionUncertain('历史撤回可能已发生；重新提交结果未知；禁止覆盖意图或重发')
            try:
                row = initial()
                if _record_digest(row, day) == historical['target']:
                    sg.save_journal(path, {**historical,'status':'observed'})
                    return dict(amendment_status='skipped-existing', verified=True, detail=row)
            except Exception:
                pass
            raise sg.SubmissionUncertain('历史撤回可能已发生；重新提交结果未知；禁止重发，请只读核实') from None
        row = initial()
        if historical and _record_digest(row, day) != historical['target']:
            raise sg.SubmissionUncertain('已核实修改后的记录发生变化；禁止覆盖或重发')
        if row['jobDesc'] == job_desc:
            return dict(amendment_status='skipped-existing', verified=True, detail=row)
        marker = dict(version=1, scope=scope, request=request,
                      base=sg.digest(row), target=_record_digest(row, day, job_desc), status='stop-pending')
        stable()
        sg.save_journal(path, marker)
        try:
            result = fetch('/sn/workflow/task/stopProcess', {'procInsId':row['procInsId']})
            if result.get('isOk') is not True:
                raise ValueError('撤回响应缺少明确成功')
            withdrawn = read()
            expected = {**row, 'state':withdrawn.get('state')}
            if type(withdrawn.get('state')) not in (str,int) or str(withdrawn['state']) != '-1' or sg.digest(withdrawn) != sg.digest(expected):
                raise ValueError('撤回后字段不匹配')
            stable()
            sg.save_journal(path, {**marker,'status':'withdrawn'})
        except Exception:
            raise sg.SubmissionUncertain('撤回可能已发生；未重新提交，禁止重发，请只读核实') from None
        outgoing = {key:row[key] for key in BUSINESS}
        weekday = '一二三四五六日'[date.fromisoformat(day).weekday()]
        outgoing.update(fillDate=day + '(周' + weekday + ')', jobDesc=job_desc, state='-1')
        uncertain = False
        try:
            stable()
            sg.save_journal(path, {**marker,'status':'save-pending'})
            fetch('/sn/timeEntry/saveOrUpdate', {'timeEntryList':[outgoing], 'saveOrSubmit':1})
        except Exception:
            uncertain = True
        try:
            final = read()  # A single read, never another write after any failure.
            _validate_row(final, entry_id, day)
            if _record_digest(final, day) != marker['target']:
                raise ValueError('最终字段不匹配')
            stable()
            sg.save_journal(path, {**marker,'status':'observed'})
        except Exception:
            raise sg.SubmissionUncertain('撤回已观察；重新提交结果未知，禁止重发，请只读核实') from None
        return dict(amendment_status='observed-after-uncertain' if uncertain else 'amended-confirmed', verified=True, detail=final)
