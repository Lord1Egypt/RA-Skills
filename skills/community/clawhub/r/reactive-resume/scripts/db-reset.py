#!/usr/bin/env python3
"""
Reactive Resume 开发数据库重置工具

快速重置开发数据库（删除所有数据并重新迁移）。

警告：此操作不可逆，仅用于开发环境！

用法:
    python db-reset.py [--confirm]

示例:
    python db-reset.py           # 需要确认
    python db-reset.py --confirm # 直接执行
"""

import os
import sys
import argparse
import subprocess
from datetime import datetime

# 颜色输出
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_colored(text, color):
    print(f"{color}{text}{Colors.END}")

def run_command(command, capture=False):
    """运行 shell 命令"""
    try:
        if capture:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.returncode, result.stdout, result.stderr
        else:
            subprocess.run(command, shell=True)
            return 0, "", ""
    except Exception as e:
        print_colored(f"Error: {e}", Colors.RED)
        return 1, "", str(e)

def check_env():
    """检查环境变量"""
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        # 尝试从 .env 读取
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('DATABASE_URL='):
                        db_url = line.split('=', 1)[1].strip()
                        break
    
    if not db_url:
        print_colored("❌ DATABASE_URL not found. Please set it in .env or environment.", Colors.RED)
        return None
    
    # 检查是否是开发环境（localhost 或 postgres）
    if 'localhost' not in db_url and 'postgres' not in db_url:
        print_colored("⚠️  Warning: DATABASE_URL does not look like a development database.", Colors.YELLOW)
        print(f"   URL: {db_url}")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            return None
    
    return db_url

def drop_all_tables(db_url):
    """删除所有表"""
    print_colored("\n🗑️  Dropping all tables...", Colors.YELLOW)
    
    # 使用 psql 删除所有表
    drop_sql = """
    DO $$ DECLARE
        r RECORD;
    BEGIN
        FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
            EXECUTE 'DROP TABLE IF EXISTS public.' || quote_ident(r.tablename) || ' CASCADE';
        END LOOP;
    END $$;
    """
    
    # 写入临时文件
    with open('/tmp/drop_tables.sql', 'w') as f:
        f.write(drop_sql)
    
    # 执行
    cmd = f"psql {db_url} -f /tmp/drop_tables.sql"
    returncode, stdout, stderr = run_command(cmd, capture=True)
    
    if returncode != 0:
        print_colored(f"❌ Failed to drop tables: {stderr}", Colors.RED)
        return False
    
    print_colored("✓ All tables dropped", Colors.GREEN)
    return True

def run_migrations():
    """运行数据库迁移"""
    print_colored("\n🔄 Running migrations...", Colors.YELLOW)
    
    returncode, stdout, stderr = run_command("pnpm db:migrate", capture=True)
    
    if returncode != 0:
        print_colored(f"❌ Failed to run migrations: {stderr}", Colors.RED)
        return False
    
    print_colored("✓ Migrations completed", Colors.GREEN)
    return True

def create_test_data():
    """创建测试数据（可选）"""
    print_colored("\n📝 Create test data? (y/N): ", Colors.BLUE, end='')
    response = input().strip().lower()
    
    if response != 'y':
        return True
    
    print_colored("Creating test data...", Colors.YELLOW)
    
    # 这里可以添加创建测试数据的逻辑
    # 目前仅作为占位符
    
    print_colored("✓ Test data created (placeholder)", Colors.GREEN)
    return True

def reset_database(confirm):
    """重置数据库主流程"""
    print_colored("=" * 60, Colors.BLUE)
    print_colored("⚠️  DATABASE RESET WARNING", Colors.RED)
    print_colored("=" * 60, Colors.BLUE)
    print_colored("This will DELETE ALL DATA from the database.", Colors.RED)
    print_colored("This action is IRREVERSIBLE!", Colors.RED)
    print_colored("=" * 60, Colors.BLUE)
    
    # 检查环境
    db_url = check_env()
    if not db_url:
        print_colored("\n❌ Aborted.", Colors.RED)
        return False
    
    print(f"\nDatabase: {db_url}")
    
    # 确认
    if not confirm:
        print_colored("\nType 'DELETE' to confirm: ", Colors.RED, end='')
        confirmation = input().strip()
        if confirmation != 'DELETE':
            print_colored("\n❌ Aborted.", Colors.RED)
            return False
    
    # 执行重置
    start_time = datetime.now()
    
    if not drop_all_tables(db_url):
        return False
    
    if not run_migrations():
        return False
    
    if not create_test_data():
        return False
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print_colored("\n" + "=" * 60, Colors.GREEN)
    print_colored("✅ DATABASE RESET COMPLETED", Colors.GREEN)
    print_colored("=" * 60, Colors.GREEN)
    print(f"Duration: {duration:.2f}s")
    print_colored("=" * 60, Colors.GREEN)
    
    print("\nNext steps:")
    print("1. Start the dev server: pnpm dev")
    print("2. Create a test account at http://localhost:3000")
    print("3. Test the application")
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Reset Reactive Resume development database')
    parser.add_argument('--confirm', action='store_true', help='Skip confirmation prompt')
    parser.add_argument('--create-data', action='store_true', help='Create test data after reset')
    
    args = parser.parse_args()
    
    # 检查是否在正确的目录
    if not os.path.exists('package.json'):
        print_colored("❌ Please run this script from the project root directory.", Colors.RED)
        sys.exit(1)
    
    # 检查 pnpm
    returncode, _, _ = run_command("pnpm --version", capture=True)
    if returncode != 0:
        print_colored("❌ pnpm not found. Please install pnpm first.", Colors.RED)
        sys.exit(1)
    
    # 执行重置
    success = reset_database(args.confirm)
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
