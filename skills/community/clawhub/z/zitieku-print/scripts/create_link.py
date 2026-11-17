#!/usr/bin/env python3
"""离线生成与字帖库网站兼容的规范字帖链接。"""
import argparse
import base64
from copy import deepcopy
import json
import re
from pathlib import Path
import sys
from urllib.parse import urlencode
import unicodedata
import zlib

SCRIPT_VERSION = '0.5.2'
CONTRACT = json.loads((Path(__file__).resolve().parents[1] / 'references/contract-v2.json').read_text(encoding='utf-8'))

ERROR_MESSAGES = {
    'INVALID_INPUT': '输入必须是一个 JSON 对象。',
    'INVALID_JSON': '输入不是有效的 JSON。',
    'INPUT_READ_FAILED': '无法读取输入文件。',
    'INPUT_TOO_LONG': '输入内容过长。',
    'INTERNAL_ERROR': '脚本内部错误，请反馈脚本版本和输入。',
    'UNKNOWN_FIELD': '输入包含当前方案不支持的字段。',
    'UNKNOWN_TEMPLATE': '找不到这个字帖方案，请先查看可用方案。',
    'MISSING_NAME': '姓名练字需要填写 student_name。',
    'NAME_TOO_LONG': '姓名最多支持 6 个字符。',
    'MISSING_CONTENT': '这个字帖方案需要填写非空的 text。',
    'NO_CJK_CONTENT': 'text 中没有可练习的汉字。',
    'INCOMPATIBLE_CONTENT': '当前方案不能同时使用这些内容字段。',
    'INVALID_CLASS': 'student_class 必须是字符串。',
    'INVALID_STUDENT_ID': 'student_id 必须是字符串。',
    'INVALID_TITLE': 'title 必须是字符串。',
    'INVALID_GRID': 'grid_type 仅支持 mi、tian 或 square。',
    'UNSUPPORTED_COLUMNS': '当前字帖方案不支持调整每行格数。',
    'INVALID_COLUMNS': 'columns 必须是 4 到 16 的整数。',
    'INVALID_ORIENTATION': '当前字帖方案不支持这个页面方向。',
    'INVALID_PINYIN': '当前字帖方案不支持这个拼音设置。',
    'INVALID_TRACE_STYLE': '当前字帖方案不支持这个描红形态。',
    'INVALID_TRACE_DENSITY': '当前字帖方案不支持这个描红浓度。',
    'INVALID_PRACTICE_GRADIENT': '当前字帖方案不支持这个练习梯度。',
    'INVALID_SOURCE': 'source 不是允许的来源标识。',
    'CONTENT_TOO_LONG': '字帖配置内容过长，无法生成链接。',
    'LINK_TOO_LONG': '生成后的字帖链接过长，请减少内容后重试。',
}

class SkillInputError(ValueError):
    def __init__(self, code, field=None, allowed_values=None):
        self.code = code
        self.field = field or {
            'MISSING_NAME':'student_name', 'NAME_TOO_LONG':'student_name',
            'MISSING_CONTENT':'text', 'NO_CJK_CONTENT':'text', 'INVALID_CLASS':'student_class',
            'INVALID_STUDENT_ID':'student_id', 'INVALID_TITLE':'title',
            'INVALID_SOURCE':'source',
        }.get(code)
        self.allowed_values = allowed_values
        super().__init__(ERROR_MESSAGES.get(code, '输入不符合当前字帖规则。'))

    def as_dict(self):
        return {'error_code': self.code, 'message': str(self), 'field': self.field, 'allowed_values': self.allowed_values}

class SkillInputErrors(ValueError):
    """All problems found in one request, so callers can fix them in a single retry."""
    def __init__(self, errors):
        self.errors = errors
        super().__init__(str(errors[0]))

def fail(code, field=None, allowed_values=None):
    raise SkillInputError(code, field, allowed_values)

def compact_document(document):
    c, e, a, l, g, s, h, f = (document[key] for key in ('content','exercise','annotations','layout','grid','style','header','footer'))
    return [document['version'],
        [c['kind'],c['text'],c['title'],c['studentName'],c['studentClass'],c['studentId'],c['foundationPattern']],
        [e['kind'],[[stage['role'],stage['count']] for stage in e['stages']],e['traceStyle'],e['traceDensity']],
        [a['pinyin'],a['strokeCount'],a['radical'],a['structure']],
        [l['paper'],l['orientation'],l['flow'],l['columnDirection'],l['columns'],l['overflow'],l['poetryLayout']],
        [g['type'],g['color']],[s['fontId'],s['masterColor'],s['traceColor']],
        [h['enabled'],h['fields'],h['showStars']],[f['reprint'],f['tip']]]

def encode_document(document):
    printable = deepcopy(document)
    fields = set(printable['header']['fields']) if printable['header']['enabled'] else set()
    if 'class' not in fields: printable['content']['studentClass'] = ''
    if 'studentId' not in fields: printable['content']['studentId'] = ''
    if not printable['header']['enabled']: printable['header']['fields'] = []
    json_text = json.dumps(compact_document(printable), ensure_ascii=False, separators=(',', ':'))
    if len(json_text.encode('utf-16-le')) // 2 > 20000: fail('CONTENT_TOO_LONG')
    raw = json_text.encode()
    compressor = zlib.compressobj(level=9, wbits=-15)
    token = '3.' + base64.urlsafe_b64encode(compressor.compress(raw) + compressor.flush()).decode().rstrip('=')
    if len(token) > CONTRACT['limits']['tokenCharacters']: fail('LINK_TOO_LONG')
    return token

# Keep discovery and request validation on the same supported-field definitions.
TUNING = {
    'grid_type': ('gridType', ['mi', 'tian', 'square'], 'INVALID_GRID'),
    'columns': ('columns', list(range(4, 17)), 'INVALID_COLUMNS'),
    'orientation': ('orientation', ['portrait', 'landscape'], 'INVALID_ORIENTATION'),
    'pinyin': ('pinyin', [False, True], 'INVALID_PINYIN'),
    'trace_style': ('traceStyle', ['solid', 'hollow'], 'INVALID_TRACE_STYLE'),
    'trace_density': ('traceDensity', ['light', 'normal', 'dark'], 'INVALID_TRACE_DENSITY'),
    'practice_gradient': ('practiceGradient', ['classic', 'half', 'all-trace'], 'INVALID_PRACTICE_GRADIENT'),
}

def effective_settings(document):
    return {
        'grid_type': document['grid']['type'], 'columns': document['layout']['columns'],
        'orientation': document['layout']['orientation'],
        'pinyin': document['annotations']['pinyin'] == 'tone',
        'trace_style': document['exercise']['traceStyle'],
        'trace_density': document['exercise']['traceDensity'],
        'practice_stages': deepcopy(document['exercise']['stages']),
    }

TRACE_COLORS = {'light': '#d1d5db', 'normal': '#b8b8b8', 'dark': '#9ca3af'}
FIELD_ERRORS = {'columns': 'UNSUPPORTED_COLUMNS', **{field: code for field, (_, _, code) in TUNING.items() if field != 'columns'}}

def normalize_host(value):
    """Attribution must never block a worksheet: new platforms keep appearing, so accept any
    platform name, reduced to a short slug that cannot carry names or worksheet text."""
    if not isinstance(value, str): return None
    slug = re.sub(r'[^a-z0-9-]', '', re.sub(r'[\s_.]+', '-', value.strip().lower())).strip('-')[:32].strip('-')
    return slug or None

def find_preset(template_id):
    return next((p for p in CONTRACT['presets'] if p['id'] == template_id), None)

def is_han(char):
    # Matches the website's HAN ranges plus supplementary ideographs, which it renders but may lack data for.
    code = ord(char)
    return (0x3400 <= code <= 0x4DBF or 0x4E00 <= code <= 0x9FFF or 0xF900 <= code <= 0xFAFF
            or 0x20000 <= code <= 0x323AF)

def content_warnings(text, kind):
    """The website turns every non-space character into practice cells, so flag what will not be Han."""
    chars = [char for char in text if not char.isspace()]
    if not any(is_han(char) for char in chars): fail('NO_CJK_CONTENT')
    others = [char for char in chars if not is_han(char)]
    punctuation = [char for char in others if unicodedata.category(char)[0] in 'PS']
    unexpected = list(dict.fromkeys(char for char in others if char not in punctuation))
    warnings = []
    if unexpected:
        warnings.append(f'text 含有非汉字字符（{"".join(unexpected[:10])}），它们也会被当作练习内容排进字帖；如非有意请删除。')
    if punctuation and kind != 'poetry':
        warnings.append(f'text 含有 {len(punctuation)} 个标点，逐字练习时每个标点会单独占一行；如非有意请删除。')
    return warnings

def describe_template(template_id):
    preset = find_preset(template_id)
    if preset is None:
        fail('UNKNOWN_TEMPLATE', 'template_id', [p['id'] for p in CONTRACT['presets']])
    kind = preset['document']['content']['kind']
    fields = {'template_id': {'allowed_values': [template_id]}, 'title': {'type': 'string'},
              'source': {'allowed_values': CONTRACT['sources']}, 'host': {'type': 'string', 'max_characters': 32, 'suggested_values': CONTRACT['hosts']}}
    required = ['template_id']
    example = {'template_id': template_id}
    if kind == 'name':
        required.append('student_name')
        fields.update({name: {'type': 'string'} for name in ['student_name', 'student_class', 'student_id']})
        fields['student_name']['max_characters'] = CONTRACT['limits']['nameCharacters']
        example['student_name'] = '林小禾'
    elif kind != 'foundations':
        required.append('text')
        fields['text'] = {'type': 'string', 'non_empty': True, 'requires_han': True}
        example['text'] = '春夏秋冬'
    for field, (control, values, _) in TUNING.items():
        if control in preset['capabilities']['controls']:
            fields[field] = {'allowed_values': ['portrait'] if field == 'orientation' and kind == 'name' else values}
    return {'id': template_id, 'name': preset['name'], 'required_fields': required,
            'fields': fields, 'defaults': effective_settings(preset['document']), 'example': example}

def list_templates():
    templates = []
    for preset in CONTRACT['presets']:
        description = describe_template(preset['id'])
        fields = {k: v for k, v in description['fields'].items() if k != 'template_id'}
        templates.append({'id': preset['id'], 'mode': preset['document']['content']['kind'], 'name': preset['name'],
            'description': preset['description'], 'required_fields': description['required_fields'],
            'fields': fields, 'defaults': description['defaults']})
    return templates

def validate(request):
    """Collect every problem in the request instead of stopping at the first one."""
    errors = []
    def check(condition, code, field=None, allowed_values=None):
        if not condition: errors.append(SkillInputError(code, field, allowed_values))
    preset = find_preset(request.get('template_id'))
    fields = describe_template(preset['id'])['fields'] if preset else {}
    for field in sorted(set(request) - set(CONTRACT['fields'])):
        errors.append(SkillInputError('UNKNOWN_FIELD', field, sorted(fields) if preset else CONTRACT['fields']))
    if preset is None:
        errors.insert(0, SkillInputError('UNKNOWN_TEMPLATE', 'template_id', [p['id'] for p in CONTRACT['presets']]))
        return errors, []
    kind = preset['document']['content']['kind']
    for field in sorted(set(request) & set(CONTRACT['fields'])):
        value = request[field]
        if field not in fields:
            errors.append(SkillInputError(FIELD_ERRORS.get(field, 'INCOMPATIBLE_CONTENT'), field, []))
        elif field in TUNING:
            allowed = fields[field]['allowed_values']
            check(any(type(value) is type(option) and value == option for option in allowed), TUNING[field][2], field, allowed)
    warnings = []
    if kind == 'name':
        name = request.get('student_name')
        if not isinstance(name, str) or not name.strip(): errors.append(SkillInputError('MISSING_NAME'))
        else: check(len(name.strip()) <= CONTRACT['limits']['nameCharacters'], 'NAME_TOO_LONG')
        check(isinstance(request.get('student_class', ''), str), 'INVALID_CLASS')
        check(isinstance(request.get('student_id', ''), str), 'INVALID_STUDENT_ID')
    elif kind != 'foundations':
        text = request.get('text')
        if not isinstance(text, str) or not text.strip(): errors.append(SkillInputError('MISSING_CONTENT'))
        else:
            try: warnings = content_warnings(text, kind)
            except SkillInputError as error: errors.append(error)
    check(isinstance(request.get('title', ''), str), 'INVALID_TITLE')
    check(request.get('source', 'skill') in CONTRACT['sources'], 'INVALID_SOURCE', 'source', CONTRACT['sources'])
    return errors, warnings

def create_link(request):
    if not isinstance(request, dict): fail('INVALID_INPUT')
    errors, warnings = validate(request)
    if errors: raise SkillInputErrors(errors)
    preset = find_preset(request['template_id'])
    document = deepcopy(preset['document'])
    content = document['content']; layout = document['layout']; exercise = document['exercise']
    kind = content['kind']
    if kind == 'name':
        content['studentName'] = request['student_name'].strip()
        content['studentClass'] = request.get('student_class', '')
        content['studentId'] = request.get('student_id', '')
    elif kind != 'foundations':
        content['text'] = request['text']
    if 'title' in request: content['title'] = request['title']
    if 'grid_type' in request: document['grid']['type'] = request['grid_type']
    if 'columns' in request: layout['columns'] = request['columns']
    if 'orientation' in request: layout['orientation'] = request['orientation']
    if 'pinyin' in request: document['annotations']['pinyin'] = 'tone' if request['pinyin'] else 'off'
    if 'trace_style' in request: exercise['traceStyle'] = request['trace_style']
    if 'trace_density' in request:
        exercise['traceDensity'] = request['trace_density']
        document['style']['traceColor'] = TRACE_COLORS[request['trace_density']]
    # Stages depend on the final column count, so build them after every layout field is applied.
    # Mirrors js/worksheet/legacy-adapter.js: "half" fills half the row with master + trace cells.
    gradient = request.get('practice_gradient')
    if gradient == 'classic':
        exercise['stages'] = [{'role':'master','count':1},{'role':'trace','count':2},{'role':'copy','count':'fill'}]
    elif gradient == 'half':
        exercise['stages'] = [{'role':'master','count':1},{'role':'trace','count':max(1, layout['columns']//2-1)},{'role':'copy','count':'fill'}]
    elif gradient == 'all-trace':
        exercise['stages'] = [{'role':'master','count':1},{'role':'trace','count':'fill'}]
    document['footer']['reprint'] = False
    # Attribution only: never put names or worksheet text in the query string.
    query = {'from': request.get('source', 'skill'), 'v': SCRIPT_VERSION}
    host = normalize_host(request.get('host'))
    if host: query['host'] = host
    token = encode_document(document)
    return {'status':'configuration_ready','schema_version':'3','template_id':preset['id'],'template_name':preset['name'],
        'url':f'https://zitieku.com/zitie-shengchengqi.html?{urlencode(query)}#reprint={token}',
        'content_length':len(content['studentName'] if kind=='name' else content['text']),'render_verified':False,
        'settings':effective_settings(document),
        'warnings':warnings + ['请在网站预览中检查页面容量、字形、拼音和笔顺数据，再下载或打印。']}

def error_response(errors):
    first = errors[0]
    if first.code in ('CONTENT_TOO_LONG', 'LINK_TOO_LONG', 'INPUT_TOO_LONG'): hint = '请减少内容或按用户需求拆分后重试。'
    elif first.allowed_values == []: hint = '请删除当前方案不支持的字段；可用 --describe-template 查询方案。'
    else: hint = '请按字段类型和允许值修正；可用 --describe-template 查询方案。'
    if len(errors) > 1: hint = f'共 {len(errors)} 处问题，见 errors，请一次修正后重试。' + hint
    return {'status':'error', **first.as_dict(), 'hint':hint, 'errors':[error.as_dict() for error in errors]}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', help='UTF-8 JSON 输入文件；省略时从标准输入读取')
    parser.add_argument('--describe-template', help='查询一个方案的支持字段、取值、默认设置和最小示例')
    parser.add_argument('--list-templates', action='store_true', help='列出全部可用字帖方案及各自支持的字段、取值和默认设置')
    args=parser.parse_args()
    try:
        if args.describe_template:
            result=describe_template(args.describe_template)
        elif args.list_templates:
            result=list_templates()
        else:
            raw=Path(args.input).read_text(encoding='utf-8') if args.input else sys.stdin.read(100001)
            if len(raw)>100000: fail('INPUT_TOO_LONG')
            result=create_link(json.loads(raw))
        print(json.dumps(result,ensure_ascii=False));return 0
    except SkillInputErrors as error:
        print(json.dumps(error_response(error.errors),ensure_ascii=False));return 1
    except SkillInputError as error:
        print(json.dumps(error_response([error]),ensure_ascii=False));return 1
    except json.JSONDecodeError:
        print(json.dumps(error_response([SkillInputError('INVALID_JSON')]),ensure_ascii=False));return 1
    except OSError:
        print(json.dumps(error_response([SkillInputError('INPUT_READ_FAILED')]),ensure_ascii=False));return 1
    except Exception as error:
        # Unexpected failures are bugs, not bad input; say so instead of blaming the request.
        response=error_response([SkillInputError('INTERNAL_ERROR')])
        response.update({'hint':f'{type(error).__name__}: {error}','script_version':SCRIPT_VERSION})
        print(json.dumps(response,ensure_ascii=False));return 2

if __name__=='__main__': sys.exit(main())
