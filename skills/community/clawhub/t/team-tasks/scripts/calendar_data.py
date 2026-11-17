#!/usr/bin/env python3
"""Read and validate the skill's offline, annual mainland China calendars."""

import datetime as dt
import json
import os
from pathlib import Path
import re
import stat
from urllib.parse import urlsplit


CN_TZ = dt.timezone(dt.timedelta(hours=8), name='Asia/Shanghai')
DEFAULT_CALENDAR_DIR = Path(__file__).resolve().parents[1] / 'references' / 'calendars' / 'CN'
YEAR_FILE = re.compile(r'([0-9]{4})\.json\Z')
DATE = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}\Z')
TIMESTAMP = re.compile(
    r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}'
    r'(?::[0-9]{2}(?:\.[0-9]+)?)?(?:Z|[+-][0-9]{2}:[0-9]{2})\Z')
MAX_CALENDAR_BYTES = 1024 * 1024


class CalendarError(ValueError):
    """A stable calendar error that callers can handle without parsing text."""

    def __init__(self, code, message, conflicts=None, missing_years=None):
        self.code = code
        self.conflicts = sorted(set(conflicts or []))
        self.missing_years = sorted(set(missing_years or []))
        super().__init__(message)


def require(condition, message, code='calendar_invalid'):
    if not condition:
        raise CalendarError(code, message)


def parse_date(value, field):
    require(isinstance(value, str) and DATE.fullmatch(value),
            field + ' 必须使用 YYYY-MM-DD 日期')
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise CalendarError('calendar_invalid', field + ' 包含无效日期: ' + value) from exc


def decode_document(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, '日历 JSON 包含重复字段: ' + key)
            result[key] = value
        return result
    try:
        return json.loads(raw, object_pairs_hook=pairs,
                          parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
    except (UnicodeError, ValueError) as exc:
        if isinstance(exc, CalendarError):
            raise
        raise CalendarError('calendar_invalid', '日历 JSON 无效: ' + str(exc)) from exc


def validate_document(document, expected_year=None):
    """Return a validated copy with dates sorted and deduplicated.

    Complete transcription of the official notice is the update assistant's
    responsibility; this offline validator checks the storage contract.
    """
    require(isinstance(document, dict), '年度日历必须是 JSON 对象')
    require(type(document.get('schemaVersion')) is int and document['schemaVersion'] == 1,
            '日历 schemaVersion 必须为 1')
    year = document.get('year')
    require(type(year) is int and 1 <= year <= 9999, '日历 year 必须为有效年份整数')
    require(expected_year is None or year == expected_year, '日历 year 与文件名年份不一致')
    require(document.get('region') == 'CN', '日历 region 必须为 CN')
    require(document.get('timezone') == 'Asia/Shanghai', '日历 timezone 必须为 Asia/Shanghai')
    source = document.get('source')
    require(isinstance(source, dict), '日历 source 必须是对象')
    url = source.get('url')
    require(isinstance(url, str) and url.strip() == url and
            not any(character.isspace() or ord(character) < 32 for character in url),
            '日历 source.url 必须是官方 HTTPS URL')
    try:
        parts = urlsplit(url)
        hostname = parts.hostname or ''
        official = (parts.scheme == 'https' and
                    (hostname == 'gov.cn' or hostname.endswith('.gov.cn')) and
                    parts.username is None and parts.password is None and
                    parts.port in (None, 443))
    except ValueError:
        official = False
    require(official, '日历 source.url 必须使用 gov.cn 政府网站的 HTTPS 地址')
    parse_date(source.get('publishedAt'), 'source.publishedAt')
    updated = document.get('updatedAt')
    require(isinstance(updated, str) and TIMESTAMP.fullmatch(updated),
            '日历 updatedAt 必须是带时区的 ISO 时间')
    try:
        stamp = dt.datetime.fromisoformat(updated.replace('Z', '+00:00'))
        require(stamp.utcoffset() is not None, '日历 updatedAt 必须包含时区')
    except ValueError as exc:
        raise CalendarError('calendar_invalid', '日历 updatedAt 无效') from exc

    normalized = dict(document)
    for field in ('holidays', 'makeupWorkdays'):
        values = document.get(field)
        require(isinstance(values, list), field + ' 必须是日期数组')
        days = set()
        for value in values:
            day = parse_date(value, field)
            require(day.year == year or (day.year == year - 1 and day.month == 12),
                    field + ' 只允许目标年份或前一年 12 月的日期: ' + value)
            days.add(day.isoformat())
        normalized[field] = sorted(days)
    require(any(parse_date(value, 'holidays').year == year for value in normalized['holidays']),
            '年度日历不能是空占位文件，holidays 必须包含目标年份的放假日期')
    conflicts = set(normalized['holidays']) & set(normalized['makeupWorkdays'])
    if conflicts:
        raise CalendarError('calendar_conflict', '同一天不能同时为休假和补班日期', conflicts=conflicts)
    try:
        json.dumps(normalized, ensure_ascii=False, allow_nan=False).encode('utf-8')
    except (TypeError, ValueError, UnicodeError) as exc:
        raise CalendarError('calendar_invalid', '年度日历包含不能保存为 UTF-8 JSON 的字段') from exc
    return normalized


def read_document(path, expected_year=None):
    """Read a regular file without following a file symlink."""
    descriptor = None
    try:
        # Nonblocking open lets us reject a FIFO before waiting for a writer.
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        require(stat.S_ISREG(os.fstat(descriptor).st_mode),
                '日历必须是普通文件', 'calendar_io_error')
        handle = os.fdopen(descriptor, 'rb')
        descriptor = None  # The file object now owns and closes this descriptor.
        with handle:
            raw = handle.read(MAX_CALENDAR_BYTES + 1)
        require(len(raw) <= MAX_CALENDAR_BYTES, '日历文件过大', 'calendar_invalid')
    except OSError as exc:
        raise CalendarError('calendar_io_error', '无法读取日历: ' + str(exc)) from exc
    finally:
        if descriptor is not None:
            os.close(descriptor)
    return validate_document(decode_document(raw), expected_year)


def load_documents(directory=None):
    """Read all annual files without creating directories or lock files."""
    directory = Path(directory) if directory is not None else DEFAULT_CALENDAR_DIR
    try:
        if not directory.exists():
            if directory.is_symlink():
                raise CalendarError('calendar_io_error', '日历目录不能是符号链接')
            return {}
        require(directory.is_dir() and not directory.is_symlink(),
                '日历目录必须是普通目录', 'calendar_io_error')
        paths = sorted(directory.iterdir())
    except OSError as exc:
        raise CalendarError('calendar_io_error', '无法读取日历目录: ' + str(exc)) from exc
    documents = {}
    for path in paths:
        match = YEAR_FILE.fullmatch(path.name)
        if match:
            year = int(match.group(1))
            documents[year] = read_document(path, year)
    return documents


def merge_documents(documents):
    holidays, makeup, years = set(), set(), set()
    for document in documents:
        document = validate_document(document)
        years.add(document['year'])
        holidays.update(dt.date.fromisoformat(value) for value in document['holidays'])
        makeup.update(dt.date.fromisoformat(value) for value in document['makeupWorkdays'])
    conflicts = holidays & makeup
    if conflicts:
        raise CalendarError('calendar_conflict', '年度日历合并后存在休假和补班冲突',
                            conflicts=[day.isoformat() for day in conflicts])
    return {'holidays': holidays, 'makeupWorkdays': makeup, 'coveredYears': years,
            'timezone': 'Asia/Shanghai'}


def load_builtin_calendar(directory=None):
    return merge_documents(load_documents(directory).values())


def require_years(calendar, years):
    """Enforce coverage only for built-in calendars, not legacy overrides."""
    if isinstance(calendar, dict) and 'coveredYears' in calendar:
        missing = set(years) - set(calendar['coveredYears'])
        if missing:
            raise CalendarError('calendar_missing_year', '内置日历缺少所需年份: ' +
                                ', '.join(str(year) for year in sorted(missing)),
                                missing_years=missing)

