"""Read-only option lookup. Never probe invented dictionary endpoints."""
from oa_utils import REQ_TIMEOUT, _ensure_ok, OAAuth, load_credentials, resolve_base_url
import argparse
import json
import os
import re


from runtime_bootstrap import ensure_runtime


def main():
    ensure_runtime(['requests', 'ddddocr', 'PIL'])
    parser = argparse.ArgumentParser(description='只读 OA 选项查询；未知字典不猜测')
    parser.add_argument('--credentials', default=os.path.expanduser('~/.openclaw/workspace/memory/sn-work-record-credentials.md'))
    parser.add_argument('--base-url')
    parser.add_argument('--token')
    args = parser.parse_args()
    try:
        account, password, host = load_credentials(args.credentials)
        host = resolve_base_url(host, args.base_url)
        auth = OAAuth(host, account, password, args.token)
        result = auth.call(lambda session: discover_options(session, host))
    except Exception:
        parser.exit(1, '只读选项查询失败；未猜测字段，请提供 OA 表单选项证据。\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


def discover_options(session, base_url):
    response = session.post(base_url.rstrip('/') + '/sn/project/timeFeeDropDownPageList',
                            json={'page': 1, 'size': 8000}, timeout=REQ_TIMEOUT)
    response.raise_for_status()
    result = response.json()
    _ensure_ok(result, '查询项目选项失败')
    data = result.get('data')
    if not isinstance(data, dict) or not isinstance(data.get('content'), list):
        raise ValueError('无效项目选项响应')
    options, seen = [], set()
    for item in data['content']:
        if not isinstance(item, dict) or item.get('id') is None:
            raise ValueError('无效项目映射')
        status = item.get('boToPmStatus')
        if isinstance(status, bool) or status not in (0, 1):
            raise ValueError('项目缺少有效 boToPmStatus')
        label = item.get('projectPmName' if status == 1 else 'projectBoName')
        value = str(item['id'])
        if not isinstance(label, str) or not label.strip() or not value.strip() or value in seen:
            raise ValueError('空值或重复项目映射')
        seen.add(value)
        options.append({'value': value, 'label': label, 'bo_to_pm_status': status})
    output = {'project': {'status': 'available', 'options': options,
                          'source': 'POST /sn/project/timeFeeDropDownPageList',
                          'complete': len(options) < 8000 and data.get('totalElements', len(options)) == len(options)}}
    types = {'fill_type': 'sn_fill_type', 'project_phase': 'sn_fee_request_project_type', 'work_type': 'sn_job_type'}
    response = session.post(base_url.rstrip('/') + '/sn/system/dict/data/typeList',
                            json=list(types.values()), timeout=REQ_TIMEOUT)
    response.raise_for_status()
    result = response.json()
    _ensure_ok(result, '查询业务字典失败')
    if not isinstance(result.get('data'), list):
        raise ValueError('无效字典响应')
    for field, name in types.items():
        choices, seen = [], set()
        for item in result['data']:
            if not isinstance(item, dict):
                raise ValueError('无效字典记录')
            if item.get('dictType') != name:
                continue
            value, label = item.get('dictValue'), item.get('dictLabel')
            if isinstance(value, bool) or not isinstance(value, (str, int)) or not str(value).strip() or not isinstance(label, str) or not label.strip() or str(value) in seen:
                raise ValueError('无效或重复字典映射')
            seen.add(str(value))
            choices.append({'value': str(value), 'label': label})
        if not choices:
            raise ValueError('缺少业务字典: ' + name)
        output[field] = {'status': 'available', 'scope': 'system', 'options': choices,
                         'source': 'POST /sn/system/dict/data/typeList: ' + name}
    output['bo_to_pm_status'] = {'status': 'derived', 'options': [], 'source': 'selected project.boToPmStatus',
                                'reason': '项目/商机属性，由项目选择派生，不是独立用户选项。'}
    return output


def resolve_selection(catalog, choices):
    """Resolve exact labels/codes against fresh authenticated OA options."""
    from personal_settings import validate_fields
    if set(choices) - {'project', 'fill_type', 'work_type', 'project_phase', 'man_hour'}:
        raise ValueError('未知选择字段；boToPmStatus 由项目派生')
    def select(field):
        entry = catalog.get(field, {})
        if entry.get('status') != 'available' or entry.get('complete') is False:
            raise ValueError('选项不可用或不完整: ' + field)
        token = choices.get(field)
        if isinstance(token, bool) or not isinstance(token, (str, int)) or not str(token).strip():
            raise ValueError('缺少选择: ' + field)
        options = entry.get('options')
        if not isinstance(options, list) or not options:
            raise ValueError('缺少有效选项: ' + field)
        seen = set()
        for item in options:
            if (not isinstance(item, dict) or not isinstance(item.get('value'), str)
                    or not re.fullmatch(r'[0-9]+', item['value'])
                    or not isinstance(item.get('label'), str) or not item['label'].strip()
                    or item['value'] in seen):
                raise ValueError('无效或重复选项映射: ' + field)
            seen.add(item['value'])
        matches = [item for item in options if str(token) in (item['value'], item['label'])]
        if len(matches) != 1:
            raise ValueError('未知或歧义选项: ' + field)
        return matches[0]
    project = select('project')
    phase = select('project_phase')
    status = project.get('bo_to_pm_status')
    if isinstance(status, bool) or status not in (0, 1):
        raise ValueError('无效项目类型')
    if status == 0 and phase['value'] == '1':
        raise ValueError('商机不可选择研发/交付阶段')
    return validate_fields(dict(project_id=project['value'], project_name=project['label'],
                                bo_to_pm_status=status, project_phase=phase['value'],
                                fill_type=select('fill_type')['value'], work_type=select('work_type')['value'],
                                man_hour=choices.get('man_hour')))


if __name__ == '__main__':
    main()
