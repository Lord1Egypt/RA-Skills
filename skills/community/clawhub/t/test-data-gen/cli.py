#!/usr/bin/env python3
"""
Test Data Generator CLI
命令行测试数据生成工具
"""

import argparse
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generator import DataGenerator, DEFAULT_TEMPLATES, generate_from_template


def main():
    parser = argparse.ArgumentParser(
        description="测试数据生成器 - 生成高质量测试数据",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s users 100 json           # 生成100条用户JSON
  %(prog)s orders 50 csv            # 生成50条订单CSV
  %(prog)s products 20 sql mysql     # 生成20条产品SQL(MySQL)
  %(prog)s products 20 sql pg        # 生成20条产品SQL(PostgreSQL)
  %(prog)s --list                    # 列出所有模板
  %(prog)s --template custom.json 100 json  # 使用自定义模板

可用模板: users, orders, products, reviews, addresses
"""
    )

    parser.add_argument("template", nargs="?", default="users",
                        help="模板名称 (默认: users)")
    parser.add_argument("count", nargs="?", type=int, default=10,
                        help="生成数量 (默认: 10)")
    parser.add_argument("format", nargs="?", choices=["json", "csv", "sql"],
                        default="json", help="输出格式 (默认: json)")

    parser.add_argument("--db", dest="db_type", choices=["mysql", "pg"],
                        default="mysql", help="SQL数据库类型 (默认: mysql)")
    parser.add_argument("--template-file", dest="template_file",
                        help="自定义模板文件路径")
    parser.add_argument("--list", action="store_true",
                        help="列出所有可用模板")
    parser.add_argument("--output", "-o", dest="output_file",
                        help="输出到文件而非stdout")

    args = parser.parse_args()

    # 列出模板
    if args.list:
        print("可用模板:")
        for name in DataGenerator.get_available_templates():
            print(f"  - {name}")
        print("\n字段说明:")
        print("  users: id, name, email, phone, age, gender, created_at")
        print("  orders: id, user_id, product, amount, quantity, status, payment_method, created_at")
        print("  products: id, name, category, price, stock, created_at")
        print("  reviews: id, user_id, product_id, rating, comment, created_at")
        print("  addresses: id, user_id, province, city, district, detail, phone, is_default")
        return 0

    # 验证模板
    if args.template not in DEFAULT_TEMPLATES and not os.path.exists(args.template):
        print(f"错误: 未知模板 '{args.template}'", file=sys.stderr)
        print("使用 --list 查看可用模板", file=sys.stderr)
        return 1

    # 验证数量
    if args.count <= 0 or args.count > 100000:
        print("错误: 数量必须在 1-100000 之间", file=sys.stderr)
        return 1

    # 生成数据
    try:
        result = generate_from_template(
            template_name=args.template,
            count=args.count,
            output_format=args.format,
            db_type=args.db_type,
            custom_template=args.template_file
        )

        # 输出
        if args.output_file:
            with open(args.output_file, "w", encoding="utf-8") as f:
                f.write(result)
            print(f"已生成 {args.count} 条数据，保存到: {args.output_file}")
        else:
            print(result)

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
