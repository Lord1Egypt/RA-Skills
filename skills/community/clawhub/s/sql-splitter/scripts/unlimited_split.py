#!/usr/bin/env python3
"""
绕过社区版限制的SQL拆分脚本
- 解除对象数≤20和文件≤1MB的限制
- 修复dialect字符串→枚举转换
- 支持按对象类型过滤（--type proc/view/table等）

用法:
  python3 unlimited_split.py input.sql output_dir [--dialect sqlserver] [--type proc]
  
示例:
  # 全部拆分
  python3 unlimited_split.py /tmp/HRBI_Stage.sql /output/dir --dialect sqlserver
  
  # 只提取存储过程
  python3 unlimited_split.py /tmp/HRBI_Stage.sql /output/dir --dialect sqlserver --type proc
"""
import sys, os, types, argparse, shutil

sys.path.insert(0, '/Users/a1234/.hermes/skills/sql-splitter/scripts')

# Patch v21 source to bypass limits
with open('/Users/a1234/.hermes/skills/sql-splitter/scripts/split_sql_v21.py', 'r') as f:
    source = f.read()

source = source.replace('MAX_OBJECTS = 20', 'MAX_OBJECTS = 99999')
source = source.replace('MAX_FILE_SIZE_MB = 1', 'MAX_FILE_SIZE_MB = 9999')

# Fix dialect string→enum
old = '    if verbose:\n        print(f"[detect] 方言: {dialect.value.upper()}")'
new = '''    # 兼容字符串和枚举
    if isinstance(dialect, str):
        from common import SQLDialect
        dialect_map = {'mysql': SQLDialect.MYSQL, 'postgresql': SQLDialect.POSTGRESQL,
                       'oracle': SQLDialect.ORACLE, 'sqlserver': SQLDialect.SQLSERVER,
                       'dm': SQLDialect.DM, 'generic': SQLDialect.GENERIC}
        dialect = dialect_map.get(dialect, SQLDialect.SQLSERVER)
    if verbose:
        print(f"[detect] 方言: {dialect.value.upper()}")'''
source = source.replace(old, new)

mod = types.ModuleType('v21_patched')
mod.__file__ = '<patched>'
exec(compile(source, '<patched>', 'exec'), mod.__dict__)
split_fn = mod.split_sql_file

# CLI
parser = argparse.ArgumentParser(description='绕过社区版限制的SQL拆分')
parser.add_argument('input', help='输入SQL文件')
parser.add_argument('output', help='输出目录')
parser.add_argument('--dialect', default='sqlserver', help='SQL方言(sqlserver/oracle/dm等)')
parser.add_argument('--type', default=None, help='只提取指定类型前缀(proc/view/table/func/trig/idx等)')
args = parser.parse_args()

result = split_fn(args.input, args.output, dialect=args.dialect, verbose=True)

if result.success:
    print(f"\n✅ 拆分完成! 共 {len(result.files_created)} 个文件")
    
    if args.type:
        # 过滤：只保留指定前缀的文件
        prefix = args.type if args.type.endswith('_') else args.type + '_'
        filter_dir = args.output.rstrip('/') + f'_{args.type}'
        os.makedirs(filter_dir, exist_ok=True)
        
        kept = 0
        for fn in result.files_created:
            if fn.startswith(prefix):
                src = os.path.join(result.output_dir, fn)
                dst = os.path.join(filter_dir, fn)
                shutil.copy2(src, dst)
                kept += 1
        
        print(f"   过滤 {prefix}*: {kept} 个文件 -> {filter_dir}")
    else:
        from collections import Counter
        counters = Counter()
        for fn in result.files_created:
            for p in ['proc_','func_','view_','table_','trig_','idx_','uidx_','con_','seq_']:
                if fn.startswith(p):
                    counters[p] += 1
                    break
            else:
                counters['other'] += 1
        name_map = {'proc_':'存储过程','func_':'函数','view_':'视图','table_':'表',
                     'trig_':'触发器','idx_':'索引','uidx_':'唯一索引','con_':'约束','seq_':'序列'}
        for k, v in sorted(counters.items(), key=lambda x: -x[1]):
            print(f"   {name_map.get(k, k)}: {v}")
else:
    print(f"\n❌ 失败")
    for e in result.errors:
        print(f"   {e}")
