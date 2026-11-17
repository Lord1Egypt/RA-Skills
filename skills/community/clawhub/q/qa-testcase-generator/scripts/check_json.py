import json, sys

f = sys.argv[1]
try:
    with open(f, 'r', encoding='utf-8-sig') as fh:
        data = json.load(fh)
    print(f'VALID: {len(data.get("测试用例", []))} 条用例')
except json.JSONDecodeError as e:
    print(f'ERROR at line {e.lineno}, col {e.colno}, pos {e.pos}')
    with open(f, 'r', encoding='utf-8-sig') as fh:
        content = fh.read()
    pos = e.pos
    start = max(0, pos - 30)
    end = min(len(content), pos + 30)
    before = repr(content[start:pos])
    after = repr(content[pos:end])
    print(f'BEFORE: ...{before}')
    print(f'AFTER:  {after}...')
    # Suggest fix
    print(f'SUGGESTION: Check for unescaped chars around pos {pos}')
