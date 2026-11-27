"""整理聊天预览，并为列表结果生成完整 JSONL 与可读 XLSX。"""

import json
import os
import tempfile
import zipfile
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Tuple
from xml.sax.saxutils import escape

from common import get_task_dir, get_task_result_file


INLINE_RECORD_LIMIT = 10
EXCEL_CELL_CHAR_LIMIT = 32767

COMPANY_STATUS_LABELS = {
    1: '在业',
    2: '注销',
    3: '吊销',
    4: '迁出',
    5: '经营异常',
}

ID_FIELDS = ('bus_id', 'busId', 'pid', 'hid', 'company_id', 'human_id', 'id')

HEADER_LABELS = {
    'pid': '公司ID',
    'hid': '人物ID',
    'bus_id': '业务ID',
    'busId': '业务ID',
    'company_name': '公司名称',
    'human_name': '姓名',
    'country_code': '国家/地区代码',
    'addresses': '地址',
    'industries': '行业',
    'human_industries': '人物行业',
    'company_industries': '公司行业',
    'products': '产品',
    'title_names': '职位',
    'employee': '企业规模',
    'employee_num': '员工人数',
    'revenue': '营收',
    'status': '经营状态',
    'email_num': '邮箱数量',
    'phone_num': '电话数量',
    'ws_num': 'WhatsApp数量',
    'contact_details': '具体联系方式',
    'emails': '邮箱',
    'phones': '电话',
    'whatsapp': 'WhatsApp',
    'whatsapps': 'WhatsApp',
    'socials': '社交媒体',
    'websites': '网站',
    'val': '实际值',
    'is_valid': '有效性',
    'is_ws': '是否WhatsApp',
    'phone_type': '电话类型',
    'international_number': '国际格式号码',
    'target_title_match': '目标职位匹配',
}


def load_jsonl_records(filepath: str) -> Tuple[List[Dict[str, Any]], int]:
    """读取 JSONL；返回有效记录和无效行数量。"""
    records: List[Dict[str, Any]] = []
    invalid_lines = 0
    if not os.path.exists(filepath):
        return records, invalid_lines

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                invalid_lines += 1
                continue
            if isinstance(item, dict):
                records.append(item)
            else:
                invalid_lines += 1
    return records, invalid_lines


def write_jsonl_records(filepath: str, records: List[Dict[str, Any]]) -> None:
    """原子重写 JSONL，用于把已付费联系方式合并回原列表。"""
    directory = os.path.dirname(os.path.abspath(filepath))
    os.makedirs(directory, exist_ok=True)
    fd, temp_path = tempfile.mkstemp(prefix='result.', suffix='.jsonl.tmp', dir=directory)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            for record in records:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
        os.replace(temp_path, filepath)
    except Exception:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise


def _plain_text(value: Any) -> str:
    if value is None:
        return ''
    if isinstance(value, list):
        if all(not isinstance(item, (dict, list)) for item in value):
            return '、'.join(str(item) for item in value if item not in (None, ''))
        return json.dumps(value, ensure_ascii=False, separators=(',', ':'))
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, separators=(',', ':'))
    return str(value)


def _list_summary(value: Any, limit: int) -> str:
    """把长列表压缩成适合聊天表格的摘要，不改变完整文件。"""
    if not isinstance(value, list):
        return _plain_text(value)
    items = [str(item).strip() for item in value if item not in (None, '')]
    if not items:
        return ''
    shown = items[:limit]
    text = '、'.join(shown)
    if len(items) > limit:
        text += f' 等（共{len(items)}项）'
    return text


def _primary_address(record: Dict[str, Any]) -> str:
    addresses = record.get('addresses')
    if not isinstance(addresses, list) or not addresses:
        return ''
    first = addresses[0]
    if isinstance(first, dict):
        return first.get('address') or ', '.join(
            str(first.get(key))
            for key in ('street', 'city_en', 'province_en', 'country_en')
            if first.get(key)
        )
    return _plain_text(first)


def _contact_inventory(record: Dict[str, Any]) -> str:
    labels = (
        ('邮箱', 'email_num'),
        ('电话', 'phone_num'),
        ('WhatsApp', 'ws_num'),
    )
    parts: List[str] = []
    for label, field in labels:
        value = record.get(field)
        if isinstance(value, (int, float)) and value > 0:
            parts.append(f'{label}{int(value)}个')
        elif isinstance(value, str) and value.strip() and value.strip() != '0':
            parts.append(f'{label}{value.strip()}个')
    return '、'.join(parts)


def _company_size(record: Dict[str, Any]) -> str:
    employee_range = _plain_text(record.get('employee')).strip()
    if employee_range:
        return employee_range
    employee_num = record.get('employee_num')
    if isinstance(employee_num, (int, float)) and employee_num > 0:
        return f'{int(employee_num)}人'
    return ''


def _company_status(record: Dict[str, Any]) -> str:
    status = record.get('status')
    if status in COMPANY_STATUS_LABELS:
        return COMPANY_STATUS_LABELS[status]
    if status in (None, '', 0, '0'):
        return ''
    return str(status)


def _drop_globally_empty_columns(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    if not rows:
        return rows
    ordered_columns = list(rows[0].keys())
    keep = [
        column for column in ordered_columns
        if column == '序号' or any(str(row.get(column, '')).strip() for row in rows)
    ]
    return [{column: row.get(column, '') for column in keep} for row in rows]


def _preferred_contact_value(item: Any) -> str:
    if isinstance(item, dict):
        for key in ('international_number', 'val', 'national_number', 'telephone', 'social_url', 'url'):
            value = item.get(key)
            if value not in (None, ''):
                return str(value)
        return ''
    if item in (None, ''):
        return ''
    return str(item)


def _iter_contact_sections(value: Any) -> Iterable[Tuple[str, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            lowered = str(key).lower().replace('-', '_')
            if lowered in {
                'email', 'emails', 'phone', 'phones', 'telephone', 'telephones',
                'whatsapp', 'whatsapps', 'ws', 'social', 'socials', 'website', 'websites'
            }:
                yield lowered, child
            if isinstance(child, (dict, list)):
                yield from _iter_contact_sections(child)
    elif isinstance(value, list):
        for child in value:
            if isinstance(child, (dict, list)):
                yield from _iter_contact_sections(child)


def extract_contact_values(record: Dict[str, Any]) -> Dict[str, str]:
    """提取已购买的具体联系方式；不把库存数量当成实际值。"""
    buckets: Dict[str, List[str]] = {
        '邮箱': [],
        '电话': [],
        'WhatsApp': [],
        '网站': [],
    }

    for section, raw_items in _iter_contact_sections(record):
        items = raw_items if isinstance(raw_items, list) else [raw_items]
        for item in items:
            value = _preferred_contact_value(item)
            if not value:
                continue
            if section in {'email', 'emails'}:
                buckets['邮箱'].append(value)
            elif section in {'whatsapp', 'whatsapps', 'ws'}:
                buckets['WhatsApp'].append(value)
            elif section in {'phone', 'phones', 'telephone', 'telephones'}:
                buckets['电话'].append(value)
                if isinstance(item, dict) and item.get('is_ws') in (1, '1', True):
                    buckets['WhatsApp'].append(value)
            elif section in {'website', 'websites'}:
                buckets['网站'].append(value)

    result: Dict[str, str] = {}
    for label, values in buckets.items():
        unique = list(dict.fromkeys(value.strip() for value in values if value.strip()))
        if unique:
            result[label] = '；'.join(unique)
    return result


def build_display_rows(records: List[Dict[str, Any]], entity_type: str) -> List[Dict[str, str]]:
    """生成默认预览；Agent 可依据用户问题进一步弹性删减或补充业务列。"""
    rows: List[Dict[str, str]] = []
    for index, record in enumerate(records, start=1):
        contacts = extract_contact_values(record)
        if entity_type == 'company':
            row = {
                '序号': str(index),
                '公司名称': _plain_text(record.get('company_name')),
                '国家/地区': _plain_text(record.get('country_code')),
                '行业': _list_summary(record.get('industries'), 3),
                '主要产品': _list_summary(record.get('products'), 5),
                '主要地址': _primary_address(record),
                '企业规模': _company_size(record),
                '状态': _company_status(record),
            }
        else:
            row = {
                '序号': str(index),
                '姓名': _plain_text(record.get('human_name')),
                '公司': _plain_text(record.get('company_name')),
                '职位': _list_summary(record.get('title_names'), 3),
                '国家/地区': _plain_text(record.get('country_code')),
                '行业': _list_summary(
                    record.get('company_industries') or record.get('human_industries'),
                    3,
                ),
            }

        if contacts:
            row.update(contacts)
        else:
            row['联系方式库存'] = _contact_inventory(record)
        rows.append(row)
    return _drop_globally_empty_columns(rows)


def _flatten_record(value: Any, prefix: str = '') -> Dict[str, Any]:
    """展开对象字段；复杂数组同时保留可读值与完整明细。"""
    result: Dict[str, Any] = {}
    if isinstance(value, dict):
        if not value and prefix:
            result[prefix] = ''
        for key, child in value.items():
            child_prefix = f'{prefix}.{key}' if prefix else str(key)
            result.update(_flatten_record(child, child_prefix))
        return result

    if isinstance(value, list):
        if not value:
            result[prefix] = ''
        elif all(not isinstance(item, (dict, list)) for item in value):
            result[prefix] = '\n'.join(str(item) for item in value if item not in (None, ''))
        else:
            readable = [_preferred_contact_value(item) for item in value]
            readable = [item for item in readable if item]
            if readable:
                result[prefix] = '\n'.join(readable)
                result[f'{prefix}.完整明细'] = json.dumps(value, ensure_ascii=False, separators=(',', ':'))
            else:
                result[prefix] = json.dumps(value, ensure_ascii=False, separators=(',', ':'))
        return result

    result[prefix or '值'] = value
    return result


def _split_long_cells(row: Dict[str, Any]) -> Dict[str, Any]:
    expanded: Dict[str, Any] = {}
    for key, value in row.items():
        if not isinstance(value, str) or len(value) <= EXCEL_CELL_CHAR_LIMIT:
            expanded[key] = value
            continue
        chunks = [value[i:i + EXCEL_CELL_CHAR_LIMIT] for i in range(0, len(value), EXCEL_CELL_CHAR_LIMIT)]
        for index, chunk in enumerate(chunks, start=1):
            chunk_key = key if index == 1 else f'{key}（续{index}）'
            expanded[chunk_key] = chunk
    return expanded


def _column_name(index: int) -> str:
    name = ''
    while index:
        index, remainder = divmod(index - 1, 26)
        name = chr(65 + remainder) + name
    return name


def _readable_header(header: str) -> str:
    """把 API 字段路径转换成可读列名，同时保留未知字段名。"""
    parts = str(header).split('.')
    labels = [HEADER_LABELS.get(part, part.replace('_', ' ')) for part in parts]
    return ' / '.join(labels)


def _xml_text(value: Any) -> str:
    text = '' if value is None else str(value)
    cleaned = ''.join(ch for ch in text if ch in '\t\n\r' or ord(ch) >= 32)
    return escape(cleaned)


def _sheet_cell(ref: str, value: Any, style: int) -> str:
    if isinstance(value, bool):
        value = '是' if value else '否'
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f'<c r="{ref}" s="{style}" t="n"><v>{value}</v></c>'
    return (
        f'<c r="{ref}" s="{style}" t="inlineStr">'
        f'<is><t xml:space="preserve">{_xml_text(value)}</t></is></c>'
    )


def write_xlsx(records: List[Dict[str, Any]], filepath: str) -> str:
    """仅用 Python 标准库生成兼容 Excel 的完整可读 XLSX。"""
    flattened = [_split_long_cells(_flatten_record(record)) for record in records]
    headers: List[str] = []
    seen = set()
    for row in flattened:
        for key in row:
            if key not in seen:
                seen.add(key)
                headers.append(key)
    if not headers:
        headers = ['结果']
        flattened = [{'结果': '没有有效记录'}]

    widths: List[float] = []
    for header in headers:
        sample_values = [str(row.get(header, '')) for row in flattened[:200]]
        longest = max([len(header)] + [max((len(part) for part in value.splitlines()), default=0) for value in sample_values])
        widths.append(min(max(longest + 2, 10), 50))

    rows_xml: List[str] = []
    header_cells = ''.join(
        _sheet_cell(f'{_column_name(column)}1', _readable_header(header), 1)
        for column, header in enumerate(headers, start=1)
    )
    rows_xml.append(f'<row r="1" ht="28" customHeight="1">{header_cells}</row>')
    for row_index, row in enumerate(flattened, start=2):
        cells = ''.join(
            _sheet_cell(f'{_column_name(column)}{row_index}', row.get(header, ''), 2)
            for column, header in enumerate(headers, start=1)
        )
        rows_xml.append(f'<row r="{row_index}">{cells}</row>')

    last_column = _column_name(len(headers))
    last_row = len(flattened) + 1
    cols_xml = ''.join(
        f'<col min="{index}" max="{index}" width="{width:.1f}" customWidth="1"/>'
        for index, width in enumerate(widths, start=1)
    )
    sheet_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<dimension ref="A1:{last_column}{last_row}"/>'
        '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>'
        '<sheetFormatPr defaultRowHeight="18"/>'
        f'<cols>{cols_xml}</cols>'
        f'<sheetData>{"".join(rows_xml)}</sheetData>'
        f'<autoFilter ref="A1:{last_column}{last_row}"/>'
        '<pageMargins left="0.3" right="0.3" top="0.5" bottom="0.5" header="0.2" footer="0.2"/>'
        '</worksheet>'
    )

    styles_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="2"><font><sz val="11"/><name val="Aptos"/></font><font><b/><color rgb="FFFFFFFF"/><sz val="11"/><name val="Aptos"/></font></fonts>
  <fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF1F4E78"/><bgColor indexed="64"/></patternFill></fill></fills>
  <borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="3"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/><xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="center" wrapText="1"/></xf><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf></cellXfs>
  <cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>'''
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>'''
    root_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>'''
    workbook_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="完整结果" sheetId="1" r:id="rId1"/></sheets></workbook>'''
    workbook_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>'''
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
    core_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:creator>UpKuaJing Skill</dc:creator><cp:lastModifiedBy>UpKuaJing Skill</cp:lastModifiedBy><dcterms:created xsi:type="dcterms:W3CDTF">{timestamp}</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">{timestamp}</dcterms:modified></cp:coreProperties>'''
    app_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>UpKuaJing Skill</Application></Properties>'''

    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    temp_path = f'{filepath}.tmp'
    with zipfile.ZipFile(temp_path, 'w', zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('[Content_Types].xml', content_types)
        archive.writestr('_rels/.rels', root_rels)
        archive.writestr('xl/workbook.xml', workbook_xml)
        archive.writestr('xl/_rels/workbook.xml.rels', workbook_rels)
        archive.writestr('xl/styles.xml', styles_xml)
        archive.writestr('xl/worksheets/sheet1.xml', sheet_xml)
        archive.writestr('docProps/core.xml', core_xml)
        archive.writestr('docProps/app.xml', app_xml)
    os.replace(temp_path, filepath)
    return os.path.abspath(filepath)


def _record_identifier(record: Dict[str, Any], entity_type: str = '') -> str:
    """按实体类型选择列表记录 ID，避免把人物所属公司的 pid 当成人物 ID。"""
    if entity_type == 'human':
        fields = ('bus_id', 'busId', 'hid', 'human_id', 'id')
    elif entity_type == 'company':
        fields = ('bus_id', 'busId', 'pid', 'company_id', 'id')
    else:
        fields = ID_FIELDS
    for field in fields:
        value = record.get(field)
        if value not in (None, ''):
            return str(value)
    return ''


def _normalize_contact_records(data: Any, requested_ids: List[str]) -> List[Tuple[str, Any]]:
    """把不同形状的联系方式响应映射到请求 ID。"""
    requested_ids = [str(item) for item in requested_ids]
    requested_set = set(requested_ids)
    if isinstance(data, dict):
        for key in ('list', 'records', 'items', 'results', 'contacts', 'data', 'result'):
            child = data.get(key)
            if isinstance(child, list):
                data = child
                break
            if isinstance(child, dict) and key in {'data', 'result'}:
                return _normalize_contact_records(child, requested_ids)
        else:
            keyed = [(str(key), value) for key, value in data.items() if str(key) in requested_ids]
            if keyed:
                return keyed
            if len(requested_ids) == 1:
                data = [data]
            else:
                data = []
    elif not isinstance(data, list):
        data = [] if data is None else [data]

    mapped: List[Tuple[str, Any]] = []
    for index, item in enumerate(data):
        item_id = ''
        if isinstance(item, dict):
            for field in ('bus_id', 'busId', 'pid', 'hid', 'company_id', 'human_id', 'business_id', 'businessId', 'entity_id', 'entityId'):
                candidate = item.get(field)
                if candidate not in (None, '') and str(candidate) in requested_set:
                    item_id = str(candidate)
                    break
        if not item_id and len(data) == len(requested_ids) and index < len(requested_ids):
            item_id = requested_ids[index]
        elif not item_id and len(requested_ids) == 1:
            item_id = requested_ids[0]
        if item_id:
            mapped.append((item_id, item))
    return mapped


def merge_contact_results(
    task_id: str,
    requested_ids: List[str],
    data: Any,
    entity_type: str = '',
    requested_contact_types: List[str] = None,
    contact_match: str = 'all',
) -> Dict[str, Any]:
    """将联系方式合并回列表 JSONL，并重新生成最终 Excel 与预览。"""
    raw_file = get_task_result_file(task_id)
    records, invalid_lines = load_jsonl_records(raw_file)
    if invalid_lines:
        raise ValueError(f'原列表 JSONL 包含 {invalid_lines} 行无效数据，已停止合并以避免覆盖原文件。')
    if not records:
        raise ValueError('原列表任务没有可合并的记录。')

    if not entity_type:
        entity_type = 'human' if any(record.get('hid') not in (None, '') for record in records) else 'company'
    if entity_type not in {'company', 'human'}:
        raise ValueError(f'不支持的联系方式实体类型：{entity_type}')

    normalized_requested_ids = list(dict.fromkeys(str(item) for item in requested_ids))
    contact_map = dict(_normalize_contact_records(data, normalized_requested_ids))
    merged_ids: set = set()
    mapped_ids: set = set()
    requested_labels = {
        'email': '邮箱',
        'phone': '电话',
        'whatsapp': 'WhatsApp',
    }
    for record in records:
        record_id = _record_identifier(record, entity_type)
        if record_id and record_id in contact_map:
            incoming = contact_map[record_id]
            mapped_ids.add(record_id)
            actual_contacts = extract_contact_values({'contact_details': incoming})
            if requested_contact_types:
                required_labels = {requested_labels[item] for item in requested_contact_types}
                actual_contacts = {
                    label: value for label, value in actual_contacts.items()
                    if label in required_labels
                }
                contact_values_match = (
                    bool(actual_contacts)
                    if contact_match == 'any'
                    else required_labels <= set(actual_contacts)
                )
            else:
                contact_values_match = bool(actual_contacts)
            if not contact_values_match:
                continue
            existing = record.get('contact_details')
            if existing is None:
                record['contact_details'] = incoming
            elif isinstance(existing, list):
                existing.append(incoming)
            else:
                record['contact_details'] = [existing, incoming]
            merged_ids.add(record_id)

    missing_ids = [item for item in normalized_requested_ids if item not in merged_ids]
    write_jsonl_records(raw_file, records)
    delivery = render_task_results(task_id, entity_type)
    delivery['contactMerge'] = {
        'requestedIdCount': len(normalized_requested_ids),
        'mappedIdCount': len(mapped_ids),
        'mergedIdCount': len(merged_ids),
        'emptyContactIdCount': len(mapped_ids) - len(merged_ids),
        'missingIds': missing_ids,
    }
    return delivery


def render_task_results(task_id: str, entity_type: str) -> Dict[str, Any]:
    """返回前 10 条预览，并生成完整 JSONL 与 XLSX。"""
    if entity_type not in {'company', 'human'}:
        raise ValueError(f'不支持的结果类型：{entity_type}')

    task_dir = get_task_dir(task_id)
    os.makedirs(task_dir, exist_ok=True)
    raw_file = get_task_result_file(task_id)
    excel_file = os.path.join(task_dir, 'result.xlsx')
    records, invalid_lines = load_jsonl_records(raw_file)
    write_xlsx(records, excel_file)
    matched_records = [
        record for record in records
        if record.get('target_title_match') in (1, '1', True)
    ]
    preview_records = (matched_records or records)[:INLINE_RECORD_LIMIT]
    display_rows = build_display_rows(preview_records, entity_type)
    remaining_count = max(0, len(records) - len(display_rows))

    instruction = (
        f'在当前回复中用简洁 Markdown 表格展示最多 {len(display_rows)} 条结果，并根据用户问题弹性选择有意义的列；'
        '不得展示ID、游标、内部评分或全空列。用户购买了具体联系方式时，必须展示完整邮箱、电话、WhatsApp等实际值，'
        '不能只显示存在状态或数量。必须同时提供 rawJsonlFile 和 excelFile；不要自动生成 CSV 或 Markdown 报告。'
        '告诉用户可以继续针对完整 JSONL 提问；读取和分析已有 JSONL 不调用 API、不产生查询费用。'
    )

    return {
        'deliveryStatus': 'required',
        'recordCount': len(records),
        'invalidJsonlLines': invalid_lines,
        'chatPreviewLimit': INLINE_RECORD_LIMIT,
        'displayedRecordCount': len(display_rows),
        'displayRows': display_rows,
        'remainingRecordCount': remaining_count,
        'rawJsonlFile': os.path.abspath(raw_file),
        'excelFile': os.path.abspath(excel_file),
        'followUpFromJsonl': {
            'enabled': True,
            'usesPaidApi': False,
            'allowed': ['筛选', '排序', '统计', '比较', '总结'],
            'sourceBoundary': '只能依据该JSONL；缺失信息必须明确说明，不得猜测或使用其他来源补充。',
        },
        'instruction': instruction,
    }


def _normalize_response_records(data: Any) -> List[Any]:
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ('list', 'records', 'items'):
            value = data.get(key)
            if isinstance(value, list):
                return value
        return [data]
    if data is None:
        return []
    return [data]


def render_data_results(data: Any, result_type: str) -> Dict[str, Any]:
    """为最多 20 条的详情/联系方式响应生成必须内联展示的数据。"""
    records = _normalize_response_records(data)
    return {
        'deliveryStatus': 'required',
        'resultType': result_type,
        'recordCount': len(records),
        'inlineDisplayComplete': True,
        'displayRows': records,
        'remainingRecordCount': 0,
        'instruction': '在当前回复中展示 displayRows 的全部记录和费用；联系方式必须展示完整实际值，不得只说查询成功或只输出文件路径。',
    }
