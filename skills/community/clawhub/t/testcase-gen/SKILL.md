---
name: "testcase-generator"
description: "Generates comprehensive test cases from MySQL/Redis data. Invoke when user wants to create test cases for an API endpoint."
---

# Test Case Generator

LLM驱动的测试用例生成系统。根据服务配置自动连接MySQL和Redis，读取真实数据，生成覆盖多种测试维度的测试用例。

**核心理念**：深度分析业务逻辑，生成"多而全"的测试用例

## 核心功能

1. **连接配置** - 自动从服务配置读取MySQL和Redis连接信息
2. **深度代码分析** - 分析Controller、Service、实体类、Mapper完整链路
3. **数据读取** - 根据待测接口需求读取MySQL表数据及表结构和Redis缓存数据
4. **用例生成** - 基于数据库表结构、真实数据和业务逻辑生成不少于20条详细测试用例
5. **质量保证** - 覆盖正常场景、边界条件、异常情况、枚举值、业务规则

## 工作流程

┌─────────────────────────────────────────────────────────────┐
│                      LLM 智能层                             │
│  ┌─────────────────┐    ┌─────────────────────────────┐ │
│  │ 分析待测接口代码  │ -> │ 分析入参结构                 │ │
│  └─────────────────┘    └─────────────────────────────┘ │
│  ┌─────────────────┐    ┌─────────────────────────────┐ │
│  │ 分析业务逻辑     │ -> │ 分析参数校验和边界条件         │ │
│  └─────────────────┘    └─────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ 生成测试用例JSON (不少于10条)                         │ │
│  └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       Python 执行层                          │
│  ┌──────────────────────┐                                  │
│  │ run_generator.py     │                                  │
│  │ 入口脚本(一键执行)     │                                  │
│  └──────────────────────┘                                  │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ data_reader.py                                        │ │
│  │ - 连接MySQL/Redis                                     │ │
│  │ - 读取表结构和数据                                    │ │
│  │ - 支持 ${VAR:default} 环境变量解析                    │ │
│  │ - LLM分析                                            │ │
│  └──────────────────────────────────────────────────────┘ │
│  ┌──────────────────────────────────────────────────────┐ │
│  │                   LLM生成                             │ │
│  │ - 输出测试用例JSON文件                                 │ │
│  └──────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                 生成 test_cases_{timestamp}.json
                              │
                              ▼
          调用junit-test-generator skill生成JUnit 5测试类
```

## 测试用例格式

```json
{
  "test_suite": "接口所属模块",
  "test_cases": [
    {
      "id": "TC_XXX_001",
      "name": "测试场景描述",
      "endpoint": "/api/path",
      "method": "POST",
      "headers": {
        "Content-Type": "application/json"
      },
      "body": {},
      "setup": {
        "mysql": [],
        "redis": {}
      },
      "expected": {
        "status": 200,
        "message": "success"
      },
      "teardown": {
        "mysql": [],
        "redis": []
      }
    }
  ]
}
```

## 测试用例要素

每条测试用例必须包含:

| 要素 | 说明 | 示例 |
|------|------|------|
| id | 唯一标识符 | TC_MA_001 |
| name | 测试场景描述 | 测试查询智控模式配置-正常场景 |
| endpoint | API路径 | /ma/querySmartControlModeConfig |
| method | HTTP方法 | POST/GET/PUT/DELETE |
| headers | 请求头 | Content-Type等 |
| body | 请求体参数 | {homeId: 1, mac: "xxx"} |
| setup | 前置条件-MySQL/Redis数据准备 | INSERT/UPDATE/SET |
| expected | 预期输出 | status: 200, message: "success" |
| teardown | 后置条件-数据清理 | DELETE/DEL |

## 测试维度覆盖

| 维度 | 说明 | 用例数量 |
|------|------|---------|
| 正常场景 | 有效输入，正常业务流程 | 4-6条 |
| 边界条件 | 空值、零值、最大值、特殊字符 | 6-8条 |
| 异常情况 | 无效输入、权限问题、资源不存在 | 6-8条 |
| 极端场景 | 并发、大数据量、长时间运行 | 2-4条 |
| 业务规则 | 特定业务逻辑验证 | 3-5条 |
| 参数校验 | 每个必填参数的null/空/负数/超长 | 8-10条 |

## 使用方法

### 1. 分析待测接口

用户提供待测试的接口代码路径和行号范围。Agent必须：
1. 阅读Controller层接口定义
2. 阅读对应的实体类定义
3. 阅读Service层实现
4. 分析涉及的Mapper/Entity

### 2. 执行数据读取

```bash
python scripts/data_reader.py --config <配置文件路径> --tables <表名列表> --redis-keys <Redis键列表>
```

### 3. 生成测试用例

LLM基于以下信息生成测试用例：
- 接口源代码
- 实体类完整定义
- Service业务逻辑
- 数据库表结构
- 真实测试数据

### 4. 输出测试用例

生成的测试用例保存到 `test_cases_{timestamp}.json` 文件中。

### 5. 调用junit-test-generator这个skill去执行测试用例

测试用例生成后，需要等待用户查看并确认测试用例后，才会调用junit-test-generator这个skill去执行测试用例。



## 数据读取脚本

### data_reader.py

```python
#!/usr/bin/env python3
"""
MySQL和Redis数据读取脚本
"""
import sys
import yaml
import pymysql
import redis
import argparse
from typing import List, Dict, Any

class DataReader:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.mysql_conn = None
        self.redis_client = None

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """从application.yaml加载配置"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def connect_mysql(self):
        """建立MySQL连接"""
        db_config = self.config['spring']['datasource']
        self.mysql_conn = pymysql.connect(
            host=db_config.get('url', '').split(':')[0].split('//')[1],
            port=int(str(db_config.get('url', '').split(':')[2]).split('/')[0]),
            user=db_config['username'],
            password=db_config['password'],
            database=db_config['url'].split('/')[-1].split('?')[0],
            charset='utf8mb4'
        )

    def connect_redis(self):
        """建立Redis连接"""
        redis_config = self.config['spring']['data']['redis']
        self.redis_client = redis.Redis(
            host=redis_config['host'],
            port=redis_config['port'],
            password=redis_config.get('password'),
            db=redis_config.get('database', 0),
            decode_responses=True
        )

    def read_mysql_data(self, table_name: str, limit: int = 100) -> List[Dict]:
        """读取MySQL表数据"""
        if not self.mysql_conn:
            self.connect_mysql()
        with self.mysql_conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
            return cursor.fetchall()

    def read_redis_data(self, key_pattern: str) -> Dict[str, Any]:
        """读取Redis数据"""
        if not self.redis_client:
            self.connect_redis()
        keys = self.redis_client.keys(key_pattern)
        result = {}
        for key in keys:
            result[key] = self.redis_client.get(key)
        return result

    def close(self):
        """关闭连接"""
        if self.mysql_conn:
            self.mysql_conn.close()
        if self.redis_client:
            self.redis_client.close()

def main():
    parser = argparse.ArgumentParser(description='读取MySQL和Redis数据')
    parser.add_argument('--config', required=True, help='配置文件路径')
    parser.add_argument('--tables', nargs='+', help='要读取的表名')
    parser.add_argument('--redis-keys', nargs='+', help='Redis键模式')
    args = parser.parse_args()

    reader = DataReader(args.config)

    # 读取MySQL数据
    if args.tables:
        for table in args.tables:
            print(f"读取表: {table}")
            data = reader.read_mysql_data(table)
            print(f"  - 获取 {len(data)} 条记录")

    # 读取Redis数据
    if args.redis_keys:
        for pattern in args.redis_keys:
            print(f"读取Redis键: {pattern}")
            data = reader.read_redis_data(pattern)
            print(f"  - 获取 {len(data)} 条记录")

    reader.close()

if __name__ == "__main__":
    main()
```

## 配置说明

### MySQL配置

从 `application.yaml` 的 `spring.datasource` 节点读取:
- host: 数据库主机地址
- port: 端口号
- username: 用户名
- password: 密码
- database: 数据库名

### Redis配置

从 `application.yaml` 的 `spring.data.redis` 节点读取:
- host: Redis主机地址
- port: 端口号
- password: 密码（可选）
- database: 数据库索引

## LLM提示词模板

```
你是一个资深测试工程师。请分析以下源代码和数据库数据，为指定的API端点生成全面的测试用例。

## 待测接口信息
- 接口路径: {endpoint}
- HTTP方法: {method}
- 功能描述: {description}

## 源代码
{source_code}

## 实体类完整定义
{bean_definition}

## Service业务逻辑
{service_logic}

## MySQL表结构
{mysql_schema}

## MySQL数据
{mysql_data}

## Redis数据
{redis_data}

请生成符合以下格式的测试用例JSON，测试用例数量不少于20条:

{
  "test_suite": "模块名称",
  "test_cases": [
    {
      "id": "TC_XXX_001",
      "name": "测试场景描述",
      "endpoint": "/api/path",
      "method": "POST",
      "headers": {"Content-Type": "application/json"},
      "body": {},
      "setup": {"mysql": [], "redis": {}},
      "expected": {"status": 200, "message": "success"},
      "teardown": {"mysql": [], "redis": []}
    }
  ]
}

测试用例应覆盖:
1. 正常场景 - 有效的输入数据，业务流程正常
2. 边界条件 - 空值、零值、最大值、null、特殊字符
3. 异常情况 - 无效输入、权限问题、资源不存在
4. 极端场景 - 并发、大数据量
### 关键要求
1. 每条测试用例必须有明确的id和name
2. expected.status和expected.message必须与RespData结构一致
3. setup和teardown的SQL必须是有效的SQL语句
4. 测试用例之间不能重复
5. 所有枚举值的每个取值都要有对应测试
```

## 质量标准

- ✅ 测试用例数量不少于20条（复杂接口30+条）
- ✅ 覆盖所有指定测试维度
- ✅ 每条用例包含完整的前置条件和后置条件
- ✅ 测试数据基于真实数据库/缓存数据
- ✅ 预期输出明确且可验证
- ✅ 每个枚举值的所有可能取值都有对应测试
- ✅ 每个必填参数的null/空/无效值都有对应测试

## 版本信息

- 版本: 2.0.0
- 创建日期: 2026-03-20
- 更新日期: 2026-03-20
- 设计理念: 深度分析业务逻辑，生成全面覆盖的测试用例
