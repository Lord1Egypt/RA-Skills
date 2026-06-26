"""核心生成器模块 - 生成各种pytest fixtures"""

import os
from enum import Enum
from typing import Dict, Optional


class FixtureType(Enum):
    DB = "db"
    API = "api"
    FILE = "file"
    RANDOM = "random"


class DatabaseType(Enum):
    MYSQL = "mysql"
    POSTGRES = "postgres"
    SQLITE = "sqlite"


class ApiFramework(Enum):
    REQUESTS = "requests"
    HTTPX = "httpx"
    BOTO3 = "boto3"


class FileFormat(Enum):
    JSON = "json"
    YAML = "yaml"
    CSV = "csv"
    TOML = "toml"


class FixtureGenerator:
    """Pytest Fixture生成器"""
    
    def __init__(self):
        self._templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, str]:
        """加载内置模板"""
        return {
            # Database fixtures
            'db_mysql': self._mysql_template(),
            'db_postgres': self._postgres_template(),
            'db_sqlite': self._sqlite_template(),
            
            # API fixtures
            'api_requests': self._requests_mock_template(),
            'api_httpx': self._httpx_mock_template(),
            'api_boto3': self._boto3_mock_template(),
            
            # File fixtures
            'file_json': self._json_file_template(),
            'file_yaml': self._yaml_file_template(),
            'file_csv': self._csv_file_template(),
            'file_toml': self._toml_file_template(),
            
            # Random data fixtures
            'random_basic': self._random_basic_template(),
        }
    
    def generate(self, fixture_type: FixtureType, **kwargs) -> str:
        """生成指定类型的fixture代码"""
        if fixture_type == FixtureType.DB:
            db_type = kwargs.get('db_type', DatabaseType.SQLITE)
            return self._generate_db_fixture(db_type)
        
        elif fixture_type == FixtureType.API:
            framework = kwargs.get('framework', ApiFramework.REQUESTS)
            return self._generate_api_fixture(framework)
        
        elif fixture_type == FixtureType.FILE:
            file_format = kwargs.get('file_format', FileFormat.JSON)
            return self._generate_file_fixture(file_format)
        
        elif fixture_type == FixtureType.RANDOM:
            return self._templates['random_basic']
        
        raise ValueError(f"Unknown fixture type: {fixture_type}")
    
    def _generate_db_fixture(self, db_type: DatabaseType) -> str:
        """生成数据库fixture"""
        templates = {
            DatabaseType.MYSQL: 'db_mysql',
            DatabaseType.POSTGRES: 'db_postgres',
            DatabaseType.SQLITE: 'db_sqlite',
        }
        key = templates.get(db_type, 'db_sqlite')
        return self._templates[key]
    
    def _generate_api_fixture(self, framework: ApiFramework) -> str:
        """生成API mock fixture"""
        templates = {
            ApiFramework.REQUESTS: 'api_requests',
            ApiFramework.HTTPX: 'api_httpx',
            ApiFramework.BOTO3: 'api_boto3',
        }
        key = templates.get(framework, 'api_requests')
        return self._templates[key]
    
    def _generate_file_fixture(self, file_format: FileFormat) -> str:
        """生成文件处理fixture"""
        templates = {
            FileFormat.JSON: 'file_json',
            FileFormat.YAML: 'file_yaml',
            FileFormat.CSV: 'file_csv',
            FileFormat.TOML: 'file_toml',
        }
        key = templates.get(file_format, 'file_json')
        return self._templates[key]
    
    def generate_conftest(self, fixtures: list) -> str:
        """生成完整的conftest.py文件"""
        imports = [
            "import pytest",
            "from pathlib import Path",
            "import tempfile",
            "import shutil",
            "",
        ]
        
        conftest_parts = imports + fixtures + [
            "",
            "",
            "# ===== Custom hooks =====",
            "",
            "@pytest.fixture(autouse=True)",
            "def setup_test_env():",
            "    \"\"\"设置测试环境\"\"\"",
            "    import os",
            "    os.environ['TESTING'] = 'true'",
            "    yield",
            "    os.environ.pop('TESTING', None)",
        ]
        
        return "\n".join(conftest_parts)
    
    def list_templates(self) -> list:
        """列出所有可用模板"""
        return list(self._templates.keys())
    
    def get_template(self, name: str) -> Optional[str]:
        """获取指定模板"""
        return self._templates.get(name)
    
    # ========== 模板定义 ==========
    
    def _mysql_template(self) -> str:
        return '''import pytest
import mysql.connector
from mysql.connector import Error

@pytest.fixture(scope="session")
def mysql_connection():
    """MySQL数据库连接fixture"""
    config = {
        "host": "localhost",
        "port": 3306,
        "user": "test_user",
        "password": "test_password",
        "database": "test_db",
    }
    connection = None
    try:
        connection = mysql.connector.connect(**config)
        yield connection
    except Error as e:
        pytest.fail(f"MySQL连接失败: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()


@pytest.fixture(scope="function")
def mysql_cursor(mysql_connection):
    """MySQL游标fixture，每次测试后回滚"""
    cursor = mysql_connection.cursor(dictionary=True)
    yield cursor
    mysql_connection.rollback()
    cursor.close()


@pytest.fixture(scope="function")
def mysql_table(mysql_cursor):
    """自动清理的测试表fixture"""
    table_name = "test_table"
    
    # 创建测试表
    mysql_cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    yield table_name
    
    # 清理
    mysql_cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
'''

    def _postgres_template(self) -> str:
        return '''import pytest
import psycopg2
from psycopg2 import sql

@pytest.fixture(scope="session")
def pg_connection():
    """PostgreSQL数据库连接fixture"""
    config = {
        "host": "localhost",
        "port": 5432,
        "user": "test_user",
        "password": "test_password",
        "database": "test_db",
    }
    connection = None
    try:
        connection = psycopg2.connect(**config)
        yield connection
    except psycopg2.Error as e:
        pytest.fail(f"PostgreSQL连接失败: {e}")
    finally:
        if connection:
            connection.close()


@pytest.fixture(scope="function")
def pg_cursor(pg_connection):
    """PostgreSQL游标fixture"""
    cursor = pg_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    yield cursor
    pg_connection.rollback()
    cursor.close()


@pytest.fixture(scope="function")
def pg_table(pg_cursor):
    """PostgreSQL测试表fixture"""
    table_name = "test_table"
    
    pg_cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    yield table_name
    
    pg_cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
'''

    def _sqlite_template(self) -> str:
        return '''import pytest
import sqlite3
from pathlib import Path

@pytest.fixture(scope="session")
def sqlite_db():
    """SQLite内存数据库fixture"""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


@pytest.fixture(scope="function")
def sqlite_cursor(sqlite_db):
    """SQLite游标fixture"""
    cursor = sqlite_db.cursor()
    yield cursor
    sqlite_db.rollback()
    cursor.close()


@pytest.fixture(scope="function")
def sqlite_table(sqlite_cursor):
    """SQLite测试表fixture"""
    table_name = "test_table"
    
    sqlite_cursor.execute(f"""
        CREATE TABLE {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    yield table_name
    
    sqlite_cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
'''

    def _requests_mock_template(self) -> str:
        return '''import pytest
import requests
import requests_mock
from requests_mock import Mocker

@pytest.fixture
def requests_mock_client():
    """requests库的mock fixture"""
    with Mocker() as m:
        yield m


@pytest.fixture
def mock_api(requests_mock_client):
    """通用API mock fixture"""
    base_url = "https://api.example.com"
    
    def register_response(method, path, json_data=None, status_code=200):
        """注册API响应"""
        url = f"{base_url}{path}"
        requests_mock_client.register_uri(
            method,
            url,
            json=json_data,
            status_code=status_code
        )
        return url
    
    mock_api.register = register_response
    mock_api.base_url = base_url
    return mock_api


@pytest.fixture
def mock_user_api(mock_api):
    """用户API mock"""
    mock_api.register("GET", "/users/1", {
        "id": 1,
        "name": "Test User",
        "email": "test@example.com"
    })
    mock_api.register("POST", "/users", {
        "id": 2,
        "name": "New User",
        "email": "new@example.com"
    }, status_code=201)
    return mock_api
'''

    def _httpx_mock_template(self) -> str:
        return '''import pytest
from httpx import AsyncClient, Mock

@pytest.fixture
def httpx_mock():
    """httpx mock fixture"""
    with Mock() as m:
        yield m


@pytest.fixture
def async_client(httpx_mock):
    """异步HTTP客户端fixture"""
    from httpx import ASGITransport, AsyncClient
    
    async def app(scope, receive, send):
        pass
    
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="https://api.example.com")


@pytest.fixture
def mock_httpx_response(httpx_mock):
    """httpx响应mock"""
    def register(url, json_data, method="GET"):
        httpx_mock.register(method, url, json=json_data)
    return register
'''

    def _boto3_mock_template(self) -> str:
        return '''import pytest
import boto3
from moto import mock_aws

@pytest.fixture
def aws_credentials():
    """AWS凭证fixture"""
    import os
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture
def s3_mock(aws_credentials):
    """S3 mock fixture"""
    with mock_aws():
        yield boto3.client("s3", region_name="us-east-1")


@pytest.fixture
def dynamodb_mock(aws_credentials):
    """DynamoDB mock fixture"""
    with mock_aws():
        yield boto3.client("dynamodb", region_name="us-east-1")


@pytest.fixture
def s3_bucket(s3_mock):
    """带测试bucket的S3 fixture"""
    bucket_name = "test-bucket-12345"
    s3_mock.create_bucket(Bucket=bucket_name)
    
    yield bucket_name
    
    # 清理bucket内容
    try:
        s3_mock.delete_bucket(Bucket=bucket_name)
    except Exception:
        pass
'''

    def _json_file_template(self) -> str:
        return '''import pytest
import json
import tempfile
from pathlib import Path

@pytest.fixture
def temp_json_file():
    """临时JSON文件fixture"""
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        delete=False
    ) as f:
        yield Path(f.name)
    Path(f.name).unlink(missing_ok=True)


@pytest.fixture
def sample_json(temp_json_file):
    """示例JSON数据fixture"""
    data = {
        "users": [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"}
        ],
        "count": 2
    }
    
    with open(temp_json_file, "w") as f:
        json.dump(data, f, indent=2)
    
    return temp_json_file


@pytest.fixture
def json_loader(temp_json_file):
    """JSON加载器fixture"""
    def load(path=None):
        with open(path or temp_json_file) as f:
            return json.load(f)
    return load
'''

    def _yaml_file_template(self) -> str:
        return '''import pytest
import tempfile
import yaml
from pathlib import Path

@pytest.fixture
def temp_yaml_file():
    """临时YAML文件fixture"""
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".yaml",
        delete=False
    ) as f:
        yield Path(f.name)
    Path(f.name).unlink(missing_ok=True)


@pytest.fixture
def sample_yaml(temp_yaml_file):
    """示例YAML数据fixture"""
    data = {
        "database": {
            "host": "localhost",
            "port": 3306,
            "name": "test_db"
        },
        "debug": True
    }
    
    with open(temp_yaml_file, "w") as f:
        yaml.dump(data, f)
    
    return temp_yaml_file


@pytest.fixture
def yaml_loader(temp_yaml_file):
    """YAML加载器fixture"""
    def load(path=None):
        with open(path or temp_yaml_file) as f:
            return yaml.safe_load(f)
    return load
'''

    def _csv_file_template(self) -> str:
        return '''import pytest
import csv
import tempfile
from pathlib import Path

@pytest.fixture
def temp_csv_file():
    """临时CSV文件fixture"""
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".csv",
        delete=False,
        newline=""
    ) as f:
        yield Path(f.name)
    Path(f.name).unlink(missing_ok=True)


@pytest.fixture
def sample_csv(temp_csv_file):
    """示例CSV数据fixture"""
    data = [
        ["id", "name", "email"],
        ["1", "Alice", "alice@example.com"],
        ["2", "Bob", "bob@example.com"]
    ]
    
    with open(temp_csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)
    
    return temp_csv_file


@pytest.fixture
def csv_reader(temp_csv_file):
    """CSV读取器fixture"""
    def read(path=None):
        with open(path or temp_csv_file) as f:
            return list(csv.DictReader(f))
    return read
'''

    def _toml_file_template(self) -> str:
        return '''import pytest
import tempfile
import toml
from pathlib import Path

@pytest.fixture
def temp_toml_file():
    """临时TOML文件fixture"""
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".toml",
        delete=False
    ) as f:
        yield Path(f.name)
    Path(f.name).unlink(missing_ok=True)


@pytest.fixture
def sample_toml(temp_toml_file):
    """示例TOML数据fixture"""
    data = {
        "title": "Test Config",
        "database": {
            "host": "localhost",
            "port": 5432
        }
    }
    
    with open(temp_toml_file, "w") as f:
        toml.dump(data, f)
    
    return temp_toml_file


@pytest.fixture
def toml_loader(temp_toml_file):
    """TOML加载器fixture"""
    def load(path=None):
        with open(path or temp_toml_file) as f:
            return toml.load(f)
    return load
'''

    def _random_basic_template(self) -> str:
        return '''import pytest
import random
import string
from datetime import datetime, timedelta


@pytest.fixture
def random_string():
    """随机字符串fixture"""
    def generate(length=10, chars=None):
        chars = chars or string.ascii_letters + string.digits
        return "".join(random.choices(chars, k=length))
    return generate


@pytest.fixture
def random_email():
    """随机邮箱fixture"""
    def generate():
        username = "".join(random.choices(string.ascii_lowercase, k=8))
        domain = random.choice(["example.com", "test.com", "demo.com"])
        return f"{username}@{domain}"
    return generate


@pytest.fixture
def random_phone():
    """随机手机号fixture"""
    def generate(country="CN"):
        if country == "CN":
            prefix = random.choice(["130", "131", "132", "133", 
                                    "150", "151", "152", "180"])
            suffix = "".join(random.choices(string.digits, k=8))
            return f"{prefix}{suffix}"
        return "".join(random.choices(string.digits, k=10))
    return generate


@pytest.fixture
def random_date():
    """随机日期fixture"""
    def generate(start_days_ago=365, end_days=0):
        start = datetime.now() - timedelta(days=start_days_ago)
        end = datetime.now() - timedelta(days=end_days)
        return start + (end - start) * random.random()
    return generate


@pytest.fixture
def random_user():
    """随机用户数据fixture"""
    def generate(id_start=1):
        return {
            "id": id_start + random.randint(0, 1000),
            "name": "".join(random.choices(string.ascii_uppercase, k=2)) + 
                    "".join(random.choices(string.ascii_lowercase, k=5)),
            "email": f"user{random.randint(1000,9999)}@test.com",
            "age": random.randint(18, 80),
            "active": random.choice([True, False])
        }
    return generate
'''
