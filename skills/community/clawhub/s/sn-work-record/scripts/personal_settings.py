"""Confirmed, identity-bound non-secret preferences; no business defaults."""
import math
import hashlib
import json
import os
from pathlib import Path
import tempfile

DEFAULT_SETTINGS = Path.home() / '.config/sn-work-record/personal-settings.json'


def binding(account, base_url):
    if not account or not base_url:
        raise ValueError('账号和地址不能为空')
    return hashlib.sha256(account.encode()).hexdigest(), base_url.rstrip('/')


def save_settings(path, account, base_url, values, *, confirmed=False):
    if confirmed is not True:
        raise ValueError('保存个人设置需要用户明确确认')
    values = validate_fields(values)
    if set(values) != set(FIELDS):
        raise ValueError('设置包含未知字段')
    account_hash, host = binding(account, base_url)
    path = Path(path).expanduser()
    if Path(__file__).resolve().parents[1] in path.resolve().parents:
        raise ValueError('个人设置必须保存在技能目录之外')
    path.parent.mkdir(parents=True, mode=0o700, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix='.settings-')
    try:
        with os.fdopen(fd, 'w') as stream:
            os.fchmod(stream.fileno(), 0o600)
            json.dump(dict(version=1, confirmed=True, account_hash=account_hash,
                           base_url=host, fields=values), stream, ensure_ascii=False)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def resolve_settings(path, account, base_url, overrides):
    if set(overrides) - set(FIELDS):
        raise ValueError('未知覆盖字段')
    values = {}
    path = Path(path).expanduser()
    if path.exists():
        try:
            if path.is_symlink() or path.stat().st_mode & 0o077:
                raise ValueError('设置权限必须为 0600')
            data = json.loads(path.read_text())
            account_hash, host = binding(account, base_url)
            if not isinstance(data, dict) or data.get('version') != 1 or data.get('confirmed') is not True:
                raise ValueError('无效设置')
            if data.get('account_hash') != account_hash or data.get('base_url') != host:
                raise ValueError('个人设置与当前账号或地址不符；请使用独立设置文件')
            values = data['fields']
            if not isinstance(values, dict) or set(values) != set(FIELDS):
                raise ValueError('无效设置字段')
            validate_fields(values)
        except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError('无法读取个人设置；请重新明确确认配置') from exc
    project_keys = [key for key in ('project_id', 'project_name') if overrides.get(key) is not None]
    if len(project_keys) == 1:
        raise ValueError('项目覆盖必须同时提供 ID 和名称')
    values = {**values, **{key: value for key, value in overrides.items() if value is not None}}
    return validate_fields(values)

FIELDS = ('project_id', 'project_name', 'man_hour', 'project_phase', 'work_type', 'bo_to_pm_status', 'fill_type')


def validate_fields(values):
    missing = [key for key in FIELDS if values.get(key) is None or str(values[key]).strip() in ('', 'None', 'null')]
    if missing:
        raise ValueError('缺少已确认字段: ' + ', '.join(missing))
    for key in ('project_id', 'project_name', 'project_phase', 'work_type', 'fill_type'):
        if isinstance(values[key], bool) or not isinstance(values[key], (str, int)):
            raise ValueError('无效字段类型: ' + key)
    if isinstance(values['bo_to_pm_status'], bool) or not isinstance(values['bo_to_pm_status'], int):
        raise ValueError('bo_to_pm_status 必须是已确认整数')
    hours = values['man_hour']
    if isinstance(hours, bool) or not isinstance(hours, (int, float)) or not math.isfinite(hours) or hours <= 0:
        raise ValueError('时长必须为有限正数')
    return dict(values)
