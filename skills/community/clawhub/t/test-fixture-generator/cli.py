#!/usr/bin/env python3
"""test-fixture-generator CLI入口"""

import argparse
import sys
from pathlib import Path

from generator import (
    FixtureGenerator, 
    FixtureType, 
    DatabaseType, 
    ApiFramework, 
    FileFormat
)


def cmd_generate(args):
    """生成fixture命令"""
    generator = FixtureGenerator()
    
    try:
        if args.type == "db":
            db_type = DatabaseType(args.db_type.lower())
            output = generator.generate(FixtureType.DB, db_type=db_type)
        elif args.type == "api":
            framework = ApiFramework(args.framework.lower())
            output = generator.generate(FixtureType.API, framework=framework)
        elif args.type == "file":
            file_format = FileFormat(args.format.lower())
            output = generator.generate(FixtureType.FILE, file_format=file_format)
        elif args.type == "random":
            output = generator.generate(FixtureType.RANDOM)
        else:
            print(f"Error: Unknown type '{args.type}'")
            return 1
        
        if args.output:
            Path(args.output).write_text(output)
            print(f"✓ Fixture已生成: {args.output}")
        else:
            print(output)
        
        return 0
    
    except ValueError as e:
        print(f"Error: {e}")
        return 1


def cmd_init(args):
    """初始化conftest.py命令"""
    generator = FixtureGenerator()
    
    fixtures = []
    
    # 根据选择的类型添加fixtures
    if args.db:
        try:
            db_type = DatabaseType(args.db.lower())
            fixtures.append(generator.generate(FixtureType.DB, db_type=db_type))
        except ValueError:
            db_type = DatabaseType.SQLITE
            fixtures.append(generator.generate(FixtureType.DB, db_type=db_type))
    
    if args.api:
        try:
            framework = ApiFramework(args.api.lower())
            fixtures.append(generator.generate(FixtureType.API, framework=framework))
        except ValueError:
            framework = ApiFramework.REQUESTS
            fixtures.append(generator.generate(FixtureType.API, framework=framework))
    
    if args.file:
        try:
            file_format = FileFormat(args.file.lower())
            fixtures.append(generator.generate(FixtureType.FILE, file_format=file_format))
        except ValueError:
            file_format = FileFormat.JSON
            fixtures.append(generator.generate(FixtureType.FILE, file_format=file_format))
    
    if args.random:
        fixtures.append(generator.generate(FixtureType.RANDOM))
    
    # 如果没有指定任何类型，添加基本fixtures
    if not fixtures:
        fixtures = [
            generator.generate(FixtureType.RANDOM),
        ]
    
    output = generator.generate_conftest(fixtures)
    
    output_path = Path(args.output)
    output_path.write_text(output)
    print(f"✓ conftest.py已生成: {output_path}")
    
    return 0


def cmd_list(args):
    """列出所有模板"""
    generator = FixtureGenerator()
    templates = generator.list_templates()
    
    print("可用模板:")
    print("-" * 40)
    for name in sorted(templates):
        print(f"  • {name}")
    
    return 0


def cmd_preview(args):
    """预览指定模板"""
    generator = FixtureGenerator()
    template = generator.get_template(args.name)
    
    if template is None:
        print(f"Error: 模板 '{args.name}' 不存在")
        return 1
    
    print(f"=== 模板: {args.name} ===")
    print(template)
    
    return 0


def cmd_interactive(args):
    """交互式生成"""
    print("=== test-fixture-generator 交互式生成 ===\n")
    
    # 选择fixture类型
    print("选择fixture类型:")
    print("  1. 数据库 (db)")
    print("  2. API Mock (api)")
    print("  3. 文件处理 (file)")
    print("  4. 随机数据 (random)")
    
    type_map = {"1": "db", "2": "api", "3": "file", "4": "random"}
    
    while True:
        choice = input("\n请选择 (1-4): ").strip()
        if choice in type_map:
            fixture_type = type_map[choice]
            break
        print("无效选择，请重新输入")
    
    generator = FixtureGenerator()
    output = ""
    
    if fixture_type == "db":
        print("\n选择数据库类型:")
        print("  1. MySQL")
        print("  2. PostgreSQL")
        print("  3. SQLite (默认)")
        
        db_choice = input("请选择 (1-3) [默认3]: ").strip() or "3"
        db_map = {"1": "mysql", "2": "postgres", "3": "sqlite"}
        db_type = DatabaseType(db_map.get(db_choice, "sqlite"))
        output = generator.generate(FixtureType.DB, db_type=db_type)
    
    elif fixture_type == "api":
        print("\n选择API框架:")
        print("  1. requests (默认)")
        print("  2. httpx")
        print("  3. boto3")
        
        api_choice = input("请选择 (1-3) [默认1]: ").strip() or "1"
        api_map = {"1": "requests", "2": "httpx", "3": "boto3"}
        framework = ApiFramework(api_map.get(api_choice, "requests"))
        output = generator.generate(FixtureType.API, framework=framework)
    
    elif fixture_type == "file":
        print("\n选择文件格式:")
        print("  1. JSON (默认)")
        print("  2. YAML")
        print("  3. CSV")
        print("  4. TOML")
        
        file_choice = input("请选择 (1-4) [默认1]: ").strip() or "1"
        file_map = {"1": "json", "2": "yaml", "3": "csv", "4": "toml"}
        file_format = FileFormat(file_map.get(file_choice, "json"))
        output = generator.generate(FixtureType.FILE, file_format=file_format)
    
    else:  # random
        output = generator.generate(FixtureType.RANDOM)
    
    print("\n生成的fixture:\n")
    print(output)
    
    # 询问是否保存
    save = input("\n是否保存到文件? (y/n) [n]: ").strip().lower()
    if save == "y":
        filename = input("文件名 [conftest.py]: ").strip() or "conftest.py"
        Path(filename).write_text(output)
        print(f"✓ 已保存到: {filename}")
    
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="test-fixture-generator - 自动生成pytest fixtures的工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 生成数据库fixture
  %(prog)s generate --type db --db-type mysql

  # 生成API mock fixture
  %(prog)s generate --type api --framework requests

  # 生成文件处理fixture
  %(prog)s generate --type file --format json

  # 初始化conftest.py
  %(prog)s init --db --api --random

  # 列出所有模板
  %(prog)s list

  # 预览模板
  %(prog)s preview db_mysql

  # 交互式生成
  %(prog)s interactive
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # generate命令
    gen_parser = subparsers.add_parser("generate", help="生成fixture代码")
    gen_parser.add_argument(
        "--type", "-t",
        choices=["db", "api", "file", "random"],
        required=True,
        help="fixture类型"
    )
    gen_parser.add_argument(
        "--db-type",
        default="sqlite",
        help="数据库类型 (mysql|postgres|sqlite)"
    )
    gen_parser.add_argument(
        "--framework", "-f",
        default="requests",
        help="API框架 (requests|httpx|boto3)"
    )
    gen_parser.add_argument(
        "--format",
        default="json",
        help="文件格式 (json|yaml|csv|toml)"
    )
    gen_parser.add_argument(
        "--output", "-o",
        help="输出文件路径"
    )
    gen_parser.set_defaults(func=cmd_generate)
    
    # init命令
    init_parser = subparsers.add_parser("init", help="初始化conftest.py")
    init_parser.add_argument(
        "--db",
        help="包含数据库fixtures"
    )
    init_parser.add_argument(
        "--api",
        help="包含API mock fixtures"
    )
    init_parser.add_argument(
        "--file",
        help="包含文件处理fixtures"
    )
    init_parser.add_argument(
        "--random",
        action="store_true",
        help="包含随机数据fixtures"
    )
    init_parser.add_argument(
        "--output", "-o",
        default="conftest.py",
        help="输出文件路径"
    )
    init_parser.set_defaults(func=cmd_init)
    
    # list命令
    list_parser = subparsers.add_parser("list", help="列出所有可用模板")
    list_parser.set_defaults(func=cmd_list)
    
    # preview命令
    preview_parser = subparsers.add_parser("preview", help="预览模板内容")
    preview_parser.add_argument("name", help="模板名称")
    preview_parser.set_defaults(func=cmd_preview)
    
    # interactive命令
    interactive_parser = subparsers.add_parser("interactive", help="交互式生成")
    interactive_parser.set_defaults(func=cmd_interactive)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return 0
    
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
