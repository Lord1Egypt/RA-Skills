#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TestCase Generator - 数据读取脚本

用于从MySQL数据库和Redis缓存中读取测试数据。

版本: 1.0.0
"""

import sys
import yaml
import json
import argparse
from typing import List, Dict, Any, Optional
from datetime import datetime

try:
    import pymysql
except ImportError:
    pymysql = None

try:
    import redis
except ImportError:
    redis = None


import os
import re
from typing import Dict, Any


class ConfigLoader:
    """配置文件加载器"""

    @staticmethod
    def resolve_env_var(value: Any) -> Any:
        """
        解析配置值中的环境变量引用 ${VAR:default_value}

        Args:
            value: 配置值，可能是字符串或任意类型

        Returns:
            解析后的值
        """
        if not isinstance(value, str):
            return value

        pattern = r'\$\{([^}:]+):([^}]*)\}'
        matches = re.findall(pattern, value)

        if not matches:
            return value

        for env_var, default_value in matches:
            env_value = os.environ.get(env_var, default_value)
            value = value.replace(f'${{{env_var}:{default_value}}}', env_value)

        return value

    @staticmethod
    def resolve_config(config: Dict[str, Any], parent_key: str = '') -> Dict[str, Any]:
        """
        递归解析配置字典中的所有环境变量引用

        Args:
            config: 配置字典
            parent_key: 父级键名（用于日志）

        Returns:
            解析后的配置字典
        """
        resolved = {}
        for key, value in config.items():
            if isinstance(value, dict):
                resolved[key] = ConfigLoader.resolve_config(value, f"{parent_key}.{key}")
            else:
                resolved[key] = ConfigLoader.resolve_env_var(value)
        return resolved

    @staticmethod
    def load_from_yaml(config_path: str) -> Dict[str, Any]:
        """
        从YAML配置文件加载配置

        Args:
            config_path: 配置文件路径

        Returns:
            配置字典
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                if config:
                    config = ConfigLoader.resolve_config(config)
                return config or {}
        except FileNotFoundError:
            print(f"警告: 配置文件 {config_path} 不存在")
            return {}
        except yaml.YAMLError as e:
            print(f"警告: YAML解析错误: {e}")
            return {}

    @staticmethod
    def extract_mysql_config(config: Dict[str, Any]) -> Dict[str, Any]:
        """
        从Spring Boot配置中提取MySQL连接参数

        Args:
            config: 完整配置字典

        Returns:
            MySQL连接配置
        """
        datasource = config.get('spring', {}).get('datasource', {})

        url = datasource.get('url', '')
        if not url:
            return {}

        url_parts = url.replace('jdbc:mysql://', '').split('/')
        host_port = url_parts[0].split(':')
        db_name = url_parts[1].split('?')[0] if len(url_parts) > 1 else ''

        return {
            'host': host_port[0] if len(host_port) > 0 else 'localhost',
            'port': int(host_port[1]) if len(host_port) > 1 else 3306,
            'user': datasource.get('username', 'root'),
            'password': datasource.get('password', ''),
            'database': db_name,
            'charset': 'utf8mb4'
        }

    @staticmethod
    def extract_redis_config(config: Dict[str, Any]) -> Dict[str, Any]:
        """
        从Spring Boot配置中提取Redis连接参数

        Args:
            config: 完整配置字典

        Returns:
            Redis连接配置
        """
        redis_config = config.get('spring', {}).get('data', {}).get('redis', {})

        password = redis_config.get('password')
        if password and password.lower() == 'null':
            password = None

        return {
            'host': redis_config.get('host', 'localhost'),
            'port': int(redis_config.get('port', 6379)),
            'password': password,
            'db': int(redis_config.get('database', 0)),
            'decode_responses': True
        }


class MySQLDataReader:
    """MySQL数据读取器"""

    def __init__(self, config: Dict[str, Any]):
        """
        初始化MySQL连接

        Args:
            config: MySQL连接配置
        """
        self.config = config
        self.connection = None

        if pymysql is None:
            print("警告: pymysql未安装，MySQL功能将不可用")
            print("  安装命令: pip install pymysql")

    def connect(self) -> bool:
        """
        建立MySQL连接

        Returns:
            连接是否成功
        """
        if pymysql is None:
            return False

        try:
            self.connection = pymysql.connect(
                host=self.config['host'],
                port=self.config['port'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database'],
                charset=self.config.get('charset', 'utf8mb4'),
                cursorclass=pymysql.cursors.DictCursor
            )
            print(f"MySQL连接成功: {self.config['host']}:{self.config['port']}/{self.config['database']}")
            return True
        except Exception as e:
            print(f"MySQL连接失败: {e}")
            return False

    def read_table_data(self, table_name: str, where: str = None, limit: int = 100) -> List[Dict]:
        """
        读取表数据

        Args:
            table_name: 表名
            where: WHERE条件
            limit: 返回记录数限制

        Returns:
            表数据列表
        """
        if not self.connection:
            if not self.connect():
                return []

        try:
            with self.connection.cursor() as cursor:
                sql = f"SELECT * FROM {table_name}"
                if where:
                    sql += f" WHERE {where}"
                sql += f" LIMIT {limit}"

                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            print(f"读取表 {table_name} 失败: {e}")
            return []

    def read_table_schema(self, table_name: str) -> List[Dict]:
        """
        读取表结构

        Args:
            table_name: 表名

        Returns:
            字段信息列表
        """
        if not self.connection:
            if not self.connect():
                return []

        try:
            with self.connection.cursor() as cursor:
                sql = f"DESCRIBE {table_name}"
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            print(f"读取表结构 {table_name} 失败: {e}")
            return []

    def execute_query(self, sql: str) -> List[Dict]:
        """
        执行自定义SQL查询

        Args:
            sql: SQL语句

        Returns:
            查询结果列表
        """
        if not self.connection:
            if not self.connect():
                return []

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            print(f"执行SQL失败: {e}")
            return []

    def close(self):
        """关闭连接"""
        if self.connection:
            self.connection.close()
            self.connection = None


class RedisDataReader:
    """Redis数据读取器"""

    def __init__(self, config: Dict[str, Any]):
        """
        初始化Redis连接

        Args:
            config: Redis连接配置
        """
        self.config = config
        self.client = None

        if redis is None:
            print("警告: redis未安装，Redis功能将不可用")
            print("  安装命令: pip install redis")

    def connect(self) -> bool:
        """
        建立Redis连接

        Returns:
            连接是否成功
        """
        if redis is None:
            return False

        try:
            self.client = redis.Redis(
                host=self.config['host'],
                port=self.config['port'],
                password=self.config.get('password'),
                db=self.config.get('db', 0),
                decode_responses=self.config.get('decode_responses', True)
            )
            self.client.ping()
            print(f"Redis连接成功: {self.config['host']}:{self.config['port']}")
            return True
        except Exception as e:
            print(f"Redis连接失败: {e}")
            return False

    def _safe_get(self, key: str) -> Optional[str]:
        """
        安全读取键值，自动处理二进制数据

        Args:
            key: 键名

        Returns:
            值字符串，失败返回None
        """
        try:
            value = self.client.get(key)
            if value is None:
                return None
            if isinstance(value, bytes):
                try:
                    return value.decode('utf-8')
                except UnicodeDecodeError:
                    return f"<binary data: {len(value)} bytes>"
            return str(value)
        except Exception as e:
            return None

    def read_key(self, key: str) -> Optional[str]:
        """
        读取单个键的值

        Args:
            key: 键名

        Returns:
            值字符串，不存在返回None
        """
        if not self.client:
            if not self.connect():
                return None

        return self._safe_get(key)

    def _safe_decode(self, value):
        """安全解码字节串"""
        if value is None:
            return None
        if isinstance(value, bytes):
            try:
                return value.decode('utf-8')
            except UnicodeDecodeError:
                return f"<binary: {len(value)}bytes>"
        return str(value)

    def _safe_key_decode(self, key):
        """安全解码键名"""
        if isinstance(key, bytes):
            try:
                return key.decode('utf-8')
            except UnicodeDecodeError:
                return f"<binary_key: {key.hex()}>"
        return key

    def read_keys(self, pattern: str, limit: int = 1000) -> Dict[str, Optional[str]]:
        """
        读取匹配模式的所有键值对（使用SCAN避免阻塞）

        Args:
            pattern: 键模式，如 "user:*" 或 "alpha:*"
            limit: 最大返回键数量

        Returns:
            键值对字典
        """
        if not self.client:
            if not self.connect():
                return {}

        result = {}
        cursor = 0
        try:
            while len(result) < limit:
                cursor, raw_keys = self.client.scan(cursor, match=pattern, count=100)
                for raw_key in raw_keys:
                    key = self._safe_key_decode(raw_key)
                    value = self._safe_get(key)
                    result[key] = value
                    if len(result) >= limit:
                        break
                if cursor == 0:
                    break
            return result
        except Exception as e:
            print(f"读取Redis键模式 {pattern} 失败: {e}")
            return {}

    def read_hash(self, key: str) -> Dict[str, str]:
        """
        读取Hash类型数据

        Args:
            key: Hash键名

        Returns:
            Hash字段值字典
        """
        if not self.client:
            if not self.connect():
                return {}

        try:
            return self.client.hgetall(key)
        except Exception as e:
            print(f"读取Redis Hash {key} 失败: {e}")
            return {}

    def close(self):
        """关闭连接"""
        if self.client:
            self.client.close()
            self.client = None


class DataReader:
    """数据读取器主类"""

    def __init__(self, config_path: str = "config/config.yaml"):
        """
        初始化数据读取器

        Args:
            config_path: 配置文件路径
        """
        self.config = ConfigLoader.load_from_yaml(config_path)
        self.mysql = MySQLDataReader(ConfigLoader.extract_mysql_config(self.config))
        self.redis = RedisDataReader(ConfigLoader.extract_redis_config(self.config))

    def read_mysql_table(self, table_name: str, limit: int = 100) -> Dict[str, Any]:
        """
        读取MySQL表数据

        Args:
            table_name: 表名
            limit: 记录数限制

        Returns:
            包含表结构和数据的字典
        """
        schema = self.mysql.read_table_schema(table_name)
        data = self.mysql.read_table_data(table_name, limit=limit)

        return {
            'table_name': table_name,
            'schema': schema,
            'data': data,
            'count': len(data)
        }

    def read_redis_pattern(self, pattern: str) -> Dict[str, Any]:
        """
        读取Redis匹配模式的数据

        Args:
            pattern: 键模式

        Returns:
            键值对字典
        """
        return self.redis.read_keys(pattern)

    def close(self):
        """关闭所有连接"""
        self.mysql.close()
        self.redis.close()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='TestCase Generator - MySQL和Redis数据读取工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 读取单个表的数据
  python data_reader.py --config application.yaml --tables home_scene

  # 读取多个表的数据
  python data_reader.py --config application.yaml --tables home_scene scene_ma --limit 50

  # 读取Redis数据
  python data_reader.py --config application.yaml --redis-patterns "alpha:*"

  # 读取表结构
  python data_reader.py --config application.yaml --tables home_scene --schema-only

  # 输出到JSON文件
  python data_reader.py --config application.yaml --tables home_scene --output mysql_data.json
        """
    )

    parser.add_argument('--config', required=True, help='配置文件路径 (application.yaml)')
    parser.add_argument('--tables', nargs='+', help='要读取的MySQL表名列表')
    parser.add_argument('--redis-patterns', nargs='+', help='Redis键模式列表 (如 alpha:*)')
    parser.add_argument('--limit', type=int, default=100, help='每表读取的记录数限制 (默认100)')
    parser.add_argument('--schema-only', action='store_true', help='仅读取表结构，不读取数据')
    parser.add_argument('--output', help='输出JSON文件路径')

    args = parser.parse_args()

    reader = DataReader(args.config)

    result = {
        'timestamp': datetime.now().isoformat(),
        'config': args.config,
        'mysql_data': {},
        'redis_data': {}
    }

    if args.tables:
        for table in args.tables:
            print(f"\n读取MySQL表: {table}")
            table_data = reader.read_mysql_table(table, limit=args.limit)

            if args.schema_only:
                print(f"  - 字段数: {len(table_data['schema'])}")
                for field in table_data['schema']:
                    print(f"    - {field['Field']}: {field['Type']}")
            else:
                print(f"  - 记录数: {table_data['count']}")

            result['mysql_data'][table] = table_data

    if args.redis_patterns:
        for pattern in args.redis_patterns:
            print(f"\n读取Redis模式: {pattern}")
            redis_data = reader.read_redis_pattern(pattern)
            print(f"  - 键数量: {len(redis_data)}")
            result['redis_data'][pattern] = redis_data

    reader.close()

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n数据已保存到: {args.output}")
    else:
        print("\n" + json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()