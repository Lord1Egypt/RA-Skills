#!/usr/bin/env python3
"""批量达梦转换脚本 - 遍历拆分目录，逐文件调用dm_converter

用法: python3 batch_convert.py [src_dir] [dm_dir] [schema_prefix]
  src_dir:        拆分输出目录 (默认: 当前目录下的 *_split)
  dm_dir:         达梦转换输出目录 (默认: src_dir + '_dm')
  schema_prefix:  schema前缀 (默认: 从src_dir目录名提取)

示例:
  python3 batch_convert.py /path/to/HRBI_Stage_split /path/to/HRBI_Stage_split_dm HRBI_Stage
"""
import os, sys

# 自动定位dm_converter所在目录
_skill_scripts = os.path.join(os.path.expanduser('~'), '.hermes', 'skills', 'sql-splitter', 'scripts')
if os.path.isdir(_skill_scripts):
    sys.path.insert(0, _skill_scripts)
else:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dm_converter import convert_sqlserver_to_dm

src_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
dm_dir = sys.argv[2] if len(sys.argv) > 2 else src_dir.rstrip('/') + '_dm'
schema_prefix = sys.argv[3] if len(sys.argv) > 3 else os.path.basename(src_dir.rstrip('/')).replace('_split', '')

os.makedirs(dm_dir, exist_ok=True)

ok = err = 0
err_list = []

for f in sorted(os.listdir(src_dir)):
    if not f.endswith('.sql') or f == 'merge_all.sql':
        continue
    obj_type = f.split('_')[0]
    type_map = {
        'proc': 'procedure', 'func': 'function', 'trig': 'trigger',
        'view': 'view', 'table': 'table', 'idx': 'index', 'uidx': 'index',
        'con': 'constraint', 'seq': 'sequence'
    }
    mapped_type = type_map.get(obj_type, 'generic')

    with open(os.path.join(src_dir, f)) as fh:
        c = fh.read()
    try:
        converted = convert_sqlserver_to_dm(c, mapped_type, schema_prefix=schema_prefix)
        with open(os.path.join(dm_dir, f), 'w') as fh:
            fh.write(converted)
        ok += 1
    except Exception as e:
        err += 1
        err_list.append(f'{f}: {str(e)[:120]}')

print(f'转换完成: {ok} 成功, {err} 失败')
if err_list:
    print('失败列表:')
    for e in err_list[:15]:
        print(f'  - {e}')
    if len(err_list) > 15:
        print(f'  ... 还有 {len(err_list)-15} 个失败')
