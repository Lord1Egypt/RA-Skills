#!/usr/bin/env python3
"""
Workout Tracker 数据库初始化脚本
创建数据库表结构
"""

import os
import sys
import mysql.connector
from mysql.connector import Error

def get_db_config():
    """获取数据库配置"""
    return {
        'unix_socket': os.getenv('MYSQL_SOCKET', '/tmp/mysql.sock'),
        'user': os.getenv('MYSQL_USER'),
        'password': os.getenv('MYSQL_PASSWORD'),
        'database': os.getenv('MYSQL_DATABASE', 'workout_tracker')
    }

def create_tables(conn):
    """创建数据库表"""
    cursor = conn.cursor()
    
    tables_sql = [
        """
        CREATE TABLE IF NOT EXISTS exercise_types (
          id INT PRIMARY KEY AUTO_INCREMENT,
          name VARCHAR(50) NOT NULL UNIQUE,
          muscle_group VARCHAR(50),
          equipment VARCHAR(50),
          unit VARCHAR(10) DEFAULT '次',
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS gym_equipment (
          id INT PRIMARY KEY AUTO_INCREMENT,
          name VARCHAR(50) NOT NULL UNIQUE,
          category VARCHAR(30),
          muscle_main VARCHAR(50),
          muscle_sec VARCHAR(100),
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS workout_sessions (
          id INT PRIMARY KEY AUTO_INCREMENT,
          user_id INT NOT NULL DEFAULT 1,
          workout_date DATE NOT NULL,
          start_time TIME,
          end_time TIME,
          duration_min INT,
          workout_type VARCHAR(30),
          sport_name VARCHAR(50),
          notes TEXT,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          INDEX idx_user_date (user_id, workout_date)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS workout_items (
          id INT PRIMARY KEY AUTO_INCREMENT,
          session_id INT NOT NULL,
          exercise_type_id INT NOT NULL,
          set_order INT DEFAULT 1,
          reps INT,
          weight_kg DECIMAL(6,2),
          distance_km DECIMAL(6,2),
          rpe INT,
          notes VARCHAR(100),
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY (session_id) REFERENCES workout_sessions(id) ON DELETE CASCADE,
          FOREIGN KEY (exercise_type_id) REFERENCES exercise_types(id),
          INDEX idx_session (session_id)
        )
        """
    ]
    
    # 创建表
    for i, sql in enumerate(tables_sql, 1):
        try:
            cursor.execute(sql)
            print(f"✅ 表 {i}/4 创建成功")
        except Error as e:
            print(f"❌ 创建表 {i} 失败: {e}")
            return False
    
    cursor.close()
    return True

def insert_default_data(conn):
    """插入默认数据"""
    cursor = conn.cursor()
    
    # 插入常见动作类型
    exercises = [
        ('杠铃深蹲', '腿', '杠铃', '次'),
        ('杠铃卧推', '胸', '杠铃', '次'),
        ('杠铃硬拉', '下背', '杠铃', '次'),
        ('引体向上', '背', '自重', '次'),
        ('哑铃弯举', '臂', '哑铃', '次'),
        ('哑铃划船', '背', '哑铃', '次'),
        ('腿举机', '腿', '器械', '次'),
        ('高位下拉', '背', '器械', '次'),
        ('罗马凳', '下背', '器械', '次'),
        ('跑步', '全身', '有氧', '分钟'),
        ('游泳', '全身', '有氧', '分钟'),
        ('网球', '全身', '球类', '分钟'),
        ('羽毛球', '全身', '球类', '分钟'),
        ('网球发球机', '全身', '球类', '分钟'),
        ('篮球', '全身', '球类', '分钟')
    ]
    
    inserted = 0
    for exercise in exercises:
        try:
            cursor.execute(
                "INSERT IGNORE INTO exercise_types (name, muscle_group, equipment, unit) VALUES (%s, %s, %s, %s)",
                exercise
            )
            inserted += cursor.rowcount
        except Error:
            pass
    
    print(f"✅ 插入 {inserted} 个默认动作类型")
    
    cursor.close()
    return True

def load_env_file(env_file='.workout-tracker.env'):
    """尝试从 .env 文件加载环境变量"""
    if os.path.exists(env_file):
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip()
                            if key and not os.getenv(key):
                                os.environ[key] = value
            return True
        except Exception:
            pass
    return False

def main():
    """主函数"""
    print("🏋️ Workout Tracker 数据库初始化")
    print("=" * 50)
    
    # 首先尝试加载 .env 文件
    load_env_file()
    
    # 检查环境变量
    if not os.getenv('MYSQL_USER') or not os.getenv('MYSQL_PASSWORD'):
        print("❌ 请先设置 MYSQL_USER 和 MYSQL_PASSWORD 环境变量")
        print("\n💡 配置方法:")
        print("1. 创建 .env 文件:")
        print("   echo 'MYSQL_USER=workout_user' > .workout-tracker.env")
        print("   echo 'MYSQL_PASSWORD=your_password' >> .workout-tracker.env")
        print("   source .workout-tracker.env")
        print("\n2. 或直接设置环境变量:")
        print("   export MYSQL_USER=workout_user")
        print("   export MYSQL_PASSWORD=your_password")
        sys.exit(1)
    
    config = get_db_config()
    
    try:
        # 连接数据库
        print("🔗 连接数据库...")
        conn = mysql.connector.connect(**config)
        print("✅ 数据库连接成功")
        
        # 创建表
        print("\n📊 创建数据表...")
        if not create_tables(conn):
            print("❌ 创建表失败")
            conn.close()
            sys.exit(1)
        
        # 插入默认数据
        print("\n📝 插入默认数据...")
        insert_default_data(conn)
        
        # 提交更改
        conn.commit()
        conn.close()
        
        print("\n" + "=" * 50)
        print("🎉 数据库初始化完成！")
        print("💪 现在可以开始使用 Workout Tracker 了")
        
    except Error as e:
        print(f"❌ 数据库操作失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()