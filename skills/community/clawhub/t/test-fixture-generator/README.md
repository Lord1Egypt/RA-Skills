# test-fixture-generator

自动生成pytest fixtures的工具，支持常见测试场景（数据库、API mock、文件处理等）。

## 功能特性

- 🚀 **一键生成** - 快速生成各种类型的pytest fixtures
- 📦 **多种类型** - 支持数据库、API mock、文件处理、随机数据
- 🎨 **可定制** - 支持自定义配置和输出
- 📝 **规范代码** - 生成的代码符合pytest最佳实践
- 🔧 **零依赖** - 核心代码仅使用Python标准库

## 安装

```bash
# 克隆项目
git clone <repository-url>
cd test-fixture-generator

# 安装为可编辑包
pip install -e .

# 或直接使用
python -m test_fixture_generator --help
```

## 快速开始

### 生成fixture

```bash
# 生成数据库fixture (MySQL)
python -m test_fixture_generator generate --type db --db-type mysql

# 生成API mock fixture (requests)
python -m test_fixture_generator generate --type api --framework requests

# 生成文件处理fixture (JSON)
python -m test_fixture_generator generate --type file --format json

# 生成随机数据fixture
python -m test_fixture_generator generate --type random
```

### 初始化conftest.py

```bash
# 创建包含数据库和API mock的conftest.py
python -m test_fixture_generator init --db --api --random

# 指定输出文件
python -m test_fixture_generator init --db --output tests/conftest.py
```

### 交互式生成

```bash
python -m test_fixture_generator interactive
```

### 列出所有模板

```bash
python -m test_fixture_generator list
```

### 预览模板

```bash
python -m test_fixture_generator preview db_mysql
```

## 命令详解

### generate

生成指定类型的fixture代码。

| 参数 | 说明 | 可选值 |
|------|------|--------|
| `--type`, `-t` | fixture类型 | `db`, `api`, `file`, `random` |
| `--db-type` | 数据库类型 | `mysql`, `postgres`, `sqlite` |
| `--framework`, `-f` | API框架 | `requests`, `httpx`, `boto3` |
| `--format` | 文件格式 | `json`, `yaml`, `csv`, `toml` |
| `--output`, `-o` | 输出文件路径 | - |

### init

初始化conftest.py文件。

| 参数 | 说明 |
|------|------|
| `--db` | 包含数据库fixtures |
| `--api` | 包含API mock fixtures |
| `--file` | 包含文件处理fixtures |
| `--random` | 包含随机数据fixtures |
| `--output`, `-o` | 输出文件路径 (默认: conftest.py) |

## 支持的类型

### 数据库 (db)

| 类型 | 说明 |
|------|------|
| mysql | MySQL数据库连接和游标fixture |
| postgres | PostgreSQL数据库连接和游标fixture |
| sqlite | SQLite内存数据库fixture |

### API Mock (api)

| 框架 | 说明 |
|------|------|
| requests | requests库mock，使用requests-mock |
| httpx | httpx异步HTTP客户端mock |
| boto3 | AWS S3/DynamoDB mock，使用moto |

### 文件处理 (file)

| 格式 | 说明 |
|------|------|
| json | JSON文件读写fixture |
| yaml | YAML文件读写fixture |
| csv | CSV文件读写fixture |
| toml | TOML文件读写fixture |

### 随机数据 (random)

- `random_string` - 生成随机字符串
- `random_email` - 生成随机邮箱
- `random_phone` - 生成随机手机号
- `random_date` - 生成随机日期
- `random_user` - 生成随机用户数据

## 示例

### 示例1: MySQL测试

```python
# 运行生成命令
python -m test_fixture_generator generate --type db --db-type mysql -o mysql_fixtures.py

# 在conftest.py中使用
import pytest
from mysql_fixtures import mysql_connection, mysql_cursor, mysql_table

def test_insert(mysql_cursor, mysql_table):
    mysql_cursor.execute(f"INSERT INTO {mysql_table} (name) VALUES ('test')")
    mysql_cursor.execute(f"SELECT * FROM {mysql_table}")
    assert mysql_cursor.fetchone()["name"] == "test"
```

### 示例2: API Mock测试

```python
# 生成requests mock fixtures
python -m test_fixture_generator generate --type api --framework requests -o api_mock.py

# 在测试中使用
import pytest
from api_mock import mock_user_api

def test_get_user(mock_api):
    response = requests.get(f"{mock_api.base_url}/users/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Test User"
```

### 示例3: 随机数据测试

```python
# 生成随机数据fixtures
python -m test_fixture_generator generate --type random -o random_fixtures.py

# 在测试中使用
import pytest
from random_fixtures import random_user

def test_create_user(random_email):
    user = {
        "email": random_email(),
        "name": "Test User"
    }
    assert "@" in user["email"]
```

## 开发

### 运行测试

```bash
# 安装pytest
pip install pytest

# 运行测试
pytest tests/ -v
```

### 项目结构

```
test-fixture-generator/
├── SKILL.md              # 技能定义
├── README.md             # 项目文档
├── generator.py          # 核心生成器
├── cli.py                 # CLI入口
└── tests/
    └── test_generator.py  # 测试用例
```

## 许可证

MIT License

## 作者

kay
