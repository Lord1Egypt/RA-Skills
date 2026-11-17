import json, sys

f = sys.argv[1]
try:
    with open(f, 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    print(f'OK: {len(data.get("测试用例", []))} test cases')
except json.JSONDecodeError as e:
    print(f'ERROR: {e}')
    # Show problematic area
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    pos = e.pos
    start = max(0, pos - 50)
    end = min(len(content), pos + 50)
    print(f'  Context: ...{repr(content[start:end])}...')
