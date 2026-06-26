#!/usr/bin/env python3
"""
Workout Tracker 安装验证脚本
验证 MySQL 连接和环境变量配置
"""

import os
import sys
import mysql.connector
from mysql.connector import Error

def load_env_file(env_file='.workout-tracker.env'):
    """尝试从 .env 文件加载环境变量"""
    if os.path.exists(env_file):
        print(f"📁 发现配置文件: {env_file}")
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip()
                            # 只设置未设置的环境变量
                            if key and not os.getenv(key):
                                os.environ[key] = value
                                print(f"  已加载: {key}")
            return True
        except Exception as e:
            print(f"⚠️  加载配置文件失败: {e}")
    return False

def check_environment():
    """检查必需的环境变量"""
    print("🔍 检查环境变量...")
    
    required_vars = ['MYSQL_USER', 'MYSQL_PASSWORD']
    optional_vars = ['MYSQL_SOCKET', 'MYSQL_DATABASE']
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print(f"❌ 缺少必需的环境变量: {', '.join(missing)}")
        print("\n💡 配置方法（选择一种）:")
        print("1. 使用 .env 文件:")
        print("   echo 'MYSQL_USER=workout_user' > .workout-tracker.env")
        print("   echo 'MYSQL_PASSWORD=your_password' >> .workout-tracker.env")
        print("   source .workout-tracker.env")
        print("\n2. 设置环境变量:")
        for var in missing:
            print(f"   export {var}=your_value")
        print("\n3. 交互式输入（推荐）:")
        print("   python3 -c \"import getpass; import os; os.environ['MYSQL_PASSWORD'] = getpass.getpass('密码: ')\"")
        print("\n⚠️  安全提示: 不要将密码存储在版本控制或 ~/.bashrc 中")
        return False
    
    print("✅ 环境变量检查通过")
    
    # 显示配置信息（不显示密码）
    print(f"  用户: {os.getenv('MYSQL_USER')}")
    print(f"  Socket: {os.getenv('MYSQL_SOCKET', '/tmp/mysql.sock (默认)')}")
    print(f"  数据库: {os.getenv('MYSQL_DATABASE', 'workout_tracker (默认)')}")
    print(f"  密码: {'*' * 8} (已设置)")
    
    return True

def check_mysql_connection():
    """测试 MySQL 连接"""
    print("\n🔍 测试 MySQL 连接...")
    
    try:
        # 从环境变量获取配置
        config = {
            'unix_socket': os.getenv('MYSQL_SOCKET', '/tmp/mysql.sock'),
            'user': os.getenv('MYSQL_USER'),
            'password': os.getenv('MYSQL_PASSWORD'),
            'database': os.getenv('MYSQL_DATABASE', 'workout_tracker'),
            'raise_on_warnings': True
        }
        
        # 尝试连接
        conn = mysql.connector.connect(**config)
        
        # 获取服务器信息
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        
        print(f"✅ MySQL 连接成功")
        print(f"  服务器版本: {version}")
        
        # 检查数据库是否存在
        cursor.execute("SHOW DATABASES LIKE %s", (config['database'],))
        if cursor.fetchone():
            print(f"  数据库 '{config['database']}' 存在")
        else:
            print(f"⚠️  数据库 '{config['database']}' 不存在，请运行初始化脚本")
        
        cursor.close()
        conn.close()
        return True
        
    except Error as e:
        print(f"❌ MySQL 连接失败: {e}")
        print("\n💡 故障排除:")
        print("1. 确保 MySQL 服务正在运行")
        print("2. 检查 socket 路径是否正确")
        print("3. 验证用户名和密码")
        print("4. 确保用户有访问权限")
        return False

def check_python_dependencies():
    """检查 Python 依赖"""
    print("\n🔍 检查 Python 依赖...")
    
    try:
        import mysql.connector
        print("✅ mysql-connector-python 已安装")
        return True
    except ImportError:
        print("❌ mysql-connector-python 未安装")
        print("💡 安装命令: pip install mysql-connector-python")
        return False

def main():
    """主函数"""
    print("🏋️ Workout Tracker 安装验证")
    print("=" * 50)
    
    all_passed = True
    
    # 首先尝试加载 .env 文件
    load_env_file()
    
    # 检查依赖
    if not check_python_dependencies():
        all_passed = False
    
    # 检查环境变量
    if not check_environment():
        all_passed = False
    else:
        # 只有环境变量正确才测试连接
        if not check_mysql_connection():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有检查通过！Workout Tracker 可以正常运行")
        print("💪 现在可以使用技能了: 说'深蹲 60公斤 4组×8次'开始训练")
    else:
        print("⚠️  发现一些问题，请根据上面的提示修复")
        sys.exit(1)

if __name__ == "__main__":
    main()