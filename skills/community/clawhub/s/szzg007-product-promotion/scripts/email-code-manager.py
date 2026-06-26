#!/usr/bin/env python3
"""
邮件模版代号管理器 - szzg007-product-promotion

管理邮件素材代号系统 (如 QY1, QB1, QA1 等)

代号规则:
- Q = Promotion (推广)
- Y = 童装 (Childrenswear)
- B = 收纳 (Box/Storage)
- A = 通用/其他 (General)
- 数字 = 序号 (1, 2, 3...)

使用方式:
    python3 email-code-manager.py list              # 列出所有代号
    python3 email-code-manager.py generate <type>   # 生成新代号
    python3 email-code-manager.py info <code>       # 查看代号详情
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# 配置
ASSETS_DIR = Path("/Users/zhuzhenguo/.openclaw/workspace/product-promotion-assets")
EMAILS_DIR = ASSETS_DIR / "emails"

# 代号类型映射
CODE_TYPES = {
    'y': {'prefix': 'QY', 'name': '童装 (Childrenswear)'},
    'b': {'prefix': 'QB', 'name': '收纳 (Box/Storage)'},
    'a': {'prefix': 'QA', 'name': '通用 (General)'},
    'h': {'prefix': 'QH', 'name': '家居 (Home)'},
    'f': {'prefix': 'QF', 'name': '时尚 (Fashion)'},
}


def get_existing_codes() -> list:
    """获取所有已存在的代号"""
    codes = []
    
    if EMAILS_DIR.exists():
        for f in EMAILS_DIR.glob("*.meta.json"):
            try:
                with open(f, 'r', encoding='utf-8') as file:
                    meta = json.load(file)
                    codes.append({
                        'code': meta.get('code', 'UNKNOWN'),
                        'name': meta.get('name', 'Unnamed'),
                        'created': meta.get('created', 'Unknown'),
                        'category': meta.get('category', 'uncategorized')
                    })
            except Exception as e:
                print(f"⚠️ 读取失败 {f}: {e}")
    
    # 按代号排序
    codes.sort(key=lambda x: x['code'])
    return codes


def generate_next_code(code_type: str) -> str:
    """生成下一个可用代号"""
    code_type = code_type.lower()
    
    if code_type not in CODE_TYPES:
        print(f"❌ 未知类型：{code_type}")
        print(f"可用类型：{', '.join(CODE_TYPES.keys())}")
        return None
    
    prefix = CODE_TYPES[code_type]['prefix']
    
    # 获取已存在的该类型代号
    existing = get_existing_codes()
    same_type = [c for c in existing if c['code'].startswith(prefix)]
    
    # 找出最大序号
    max_num = 0
    for c in same_type:
        try:
            num = int(c['code'].replace(prefix, ''))
            max_num = max(max_num, num)
        except ValueError:
            pass
    
    # 生成新代号
    new_code = f"{prefix}{max_num + 1}"
    return new_code


def list_codes():
    """列出所有代号"""
    codes = get_existing_codes()
    
    print("\n" + "=" * 60)
    print("📧 邮件素材代号列表")
    print("=" * 60)
    
    if not codes:
        print("\n暂无邮件素材")
        return
    
    print(f"\n总计：{len(codes)} 个素材\n")
    
    # 按类型分组
    grouped = {}
    for code in codes:
        prefix = code['code'][:2]
        if prefix not in grouped:
            grouped[prefix] = []
        grouped[prefix].append(code)
    
    for prefix, items in grouped.items():
        type_name = CODE_TYPES.get(prefix.lower(), {}).get('name', prefix)
        print(f"\n{type_name}:")
        print("-" * 40)
        for item in items:
            print(f"  {item['code']:6} | {item['name']}")
            print(f"         | 创建：{item['created'][:10]}")
    
    print("\n" + "=" * 60)


def generate_code(code_type: str):
    """生成新代号"""
    new_code = generate_next_code(code_type)
    
    if new_code:
        type_name = CODE_TYPES.get(code_type.lower(), {}).get('name', code_type)
        
        print("\n" + "=" * 60)
        print("✅ 新代号生成")
        print("=" * 60)
        print(f"\n类型：{type_name}")
        print(f"新代号：{new_code}")
        print(f"\n使用方式:")
        print(f"  python3 product-promotion.py <url> --code {new_code}")
        print("=" * 60 + "\n")


def get_code_info(code: str):
    """查看代号详情"""
    meta_file = EMAILS_DIR / f"{code}.meta.json"
    
    if not meta_file.exists():
        print(f"❌ 未找到代号：{code}")
        return
    
    with open(meta_file, 'r', encoding='utf-8') as f:
        meta = json.load(f)
    
    print("\n" + "=" * 60)
    print(f"📧 代号详情：{code}")
    print("=" * 60)
    
    print(f"\n名称：{meta.get('name', 'N/A')}")
    print(f"描述：{meta.get('description', 'N/A')}")
    print(f"版本：{meta.get('version', '1.0.0')}")
    print(f"创建：{meta.get('created', 'N/A')}")
    print(f"分类：{meta.get('category', 'N/A')}")
    
    if 'product' in meta:
        print(f"\n产品信息:")
        product = meta['product']
        print(f"  名称：{product.get('name', 'N/A')}")
        print(f"  价格：{product.get('price', {}).get('sale', 'N/A')}")
        if 'url' in product:
            print(f"  网址：{product['url'][:60]}...")
    
    if 'design' in meta:
        print(f"\n设计信息:")
        design = meta['design']
        print(f"  主题：{design.get('theme', 'N/A')}")
        print(f"  风格：{design.get('style', 'N/A')}")
    
    if 'usage' in meta:
        print(f"\n使用统计:")
        usage = meta['usage']
        print(f"  发送次数：{usage.get('sentCount', 0)}")
        if usage.get('lastSent'):
            print(f"  最后发送：{usage['lastSent']}")
            if usage.get('lastSentTo'):
                print(f"  发送到：{usage['lastSentTo']}")
    
    if 'tags' in meta:
        print(f"\n标签：{', '.join(meta['tags'])}")
    
    print("\n" + "=" * 60 + "\n")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python3 email-code-manager.py <command> [args]")
        print("\n命令:")
        print("  list              - 列出所有代号")
        print("  generate <type>   - 生成新代号 (y/b/a/h/f)")
        print("  info <code>       - 查看代号详情")
        print("\n代号类型:")
        for k, v in CODE_TYPES.items():
            print(f"  {k:5} - {v['name']}")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "list":
        list_codes()
    elif command == "generate":
        if len(sys.argv) < 3:
            print("❌ 请指定代号类型")
            sys.exit(1)
        generate_code(sys.argv[2])
    elif command == "info":
        if len(sys.argv) < 3:
            print("❌ 请指定代号")
            sys.exit(1)
        get_code_info(sys.argv[2])
    else:
        print(f"❌ 未知命令：{command}")
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
