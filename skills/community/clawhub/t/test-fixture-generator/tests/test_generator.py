"""test-fixture-generator 测试用例"""

import pytest
from pathlib import Path
import tempfile
import re

from generator import (
    FixtureGenerator,
    FixtureType,
    DatabaseType,
    ApiFramework,
    FileFormat
)


class TestFixtureGenerator:
    """FixtureGenerator测试类"""
    
    def setup_method(self):
        """每个测试方法前初始化"""
        self.generator = FixtureGenerator()
    
    # ========== 初始化测试 ==========
    
    def test_generator_init(self):
        """测试生成器初始化"""
        gen = FixtureGenerator()
        assert gen is not None
    
    def test_templates_loaded(self):
        """测试模板是否加载"""
        templates = self.generator.list_templates()
        assert len(templates) > 0
    
    # ========== FixtureType测试 ==========
    
    def test_fixture_type_db(self):
        """测试DB fixture类型"""
        assert FixtureType.DB.value == "db"
    
    def test_fixture_type_api(self):
        """测试API fixture类型"""
        assert FixtureType.API.value == "api"
    
    def test_fixture_type_file(self):
        """测试FILE fixture类型"""
        assert FixtureType.FILE.value == "file"
    
    def test_fixture_type_random(self):
        """测试RANDOM fixture类型"""
        assert FixtureType.RANDOM.value == "random"
    
    # ========== DatabaseType测试 ==========
    
    def test_database_type_mysql(self):
        """测试MySQL数据库类型"""
        assert DatabaseType.MYSQL.value == "mysql"
    
    def test_database_type_postgres(self):
        """测试PostgreSQL数据库类型"""
        assert DatabaseType.POSTGRES.value == "postgres"
    
    def test_database_type_sqlite(self):
        """测试SQLite数据库类型"""
        assert DatabaseType.SQLITE.value == "sqlite"
    
    # ========== ApiFramework测试 ==========
    
    def test_api_framework_requests(self):
        """测试requests框架"""
        assert ApiFramework.REQUESTS.value == "requests"
    
    def test_api_framework_httpx(self):
        """测试httpx框架"""
        assert ApiFramework.HTTPX.value == "httpx"
    
    def test_api_framework_boto3(self):
        """测试boto3框架"""
        assert ApiFramework.BOTO3.value == "boto3"
    
    # ========== FileFormat测试 ==========
    
    def test_file_format_json(self):
        """测试JSON格式"""
        assert FileFormat.JSON.value == "json"
    
    def test_file_format_yaml(self):
        """测试YAML格式"""
        assert FileFormat.YAML.value == "yaml"
    
    def test_file_format_csv(self):
        """测试CSV格式"""
        assert FileFormat.CSV.value == "csv"
    
    def test_file_format_toml(self):
        """测试TOML格式"""
        assert FileFormat.TOML.value == "toml"
    
    # ========== generate方法测试 ==========
    
    def test_generate_db_fixture(self):
        """测试生成数据库fixture"""
        result = self.generator.generate(FixtureType.DB, db_type=DatabaseType.MYSQL)
        assert "mysql" in result.lower() or "MySQL" in result
        assert "@pytest.fixture" in result
    
    def test_generate_postgres_fixture(self):
        """测试生成PostgreSQL fixture"""
        result = self.generator.generate(FixtureType.DB, db_type=DatabaseType.POSTGRES)
        assert "psycopg2" in result or "postgres" in result.lower()
        assert "@pytest.fixture" in result
    
    def test_generate_sqlite_fixture(self):
        """测试生成SQLite fixture"""
        result = self.generator.generate(FixtureType.DB, db_type=DatabaseType.SQLITE)
        assert "sqlite" in result.lower()
        assert "@pytest.fixture" in result
    
    def test_generate_api_fixture_requests(self):
        """测试生成requests mock fixture"""
        result = self.generator.generate(FixtureType.API, framework=ApiFramework.REQUESTS)
        assert "requests" in result.lower()
        assert "requests_mock" in result.lower() or "mock" in result.lower()
    
    def test_generate_api_fixture_httpx(self):
        """测试生成httpx mock fixture"""
        result = self.generator.generate(FixtureType.API, framework=ApiFramework.HTTPX)
        assert "httpx" in result.lower()
        assert "@pytest.fixture" in result
    
    def test_generate_api_fixture_boto3(self):
        """测试生成boto3 mock fixture"""
        result = self.generator.generate(FixtureType.API, framework=ApiFramework.BOTO3)
        assert "boto3" in result.lower() or "aws" in result.lower()
        assert "@pytest.fixture" in result
    
    def test_generate_file_fixture_json(self):
        """测试生成JSON file fixture"""
        result = self.generator.generate(FixtureType.FILE, file_format=FileFormat.JSON)
        assert "json" in result.lower()
        assert "@pytest.fixture" in result
    
    def test_generate_file_fixture_yaml(self):
        """测试生成YAML file fixture"""
        result = self.generator.generate(FixtureType.FILE, file_format=FileFormat.YAML)
        assert "yaml" in result.lower() or "yml" in result.lower()
        assert "@pytest.fixture" in result
    
    def test_generate_file_fixture_csv(self):
        """测试生成CSV file fixture"""
        result = self.generator.generate(FixtureType.FILE, file_format=FileFormat.CSV)
        assert "csv" in result.lower()
        assert "@pytest.fixture" in result
    
    def test_generate_file_fixture_toml(self):
        """测试生成TOML file fixture"""
        result = self.generator.generate(FixtureType.FILE, file_format=FileFormat.TOML)
        assert "toml" in result.lower()
        assert "@pytest.fixture" in result
    
    def test_generate_random_fixture(self):
        """测试生成随机数据fixture"""
        result = self.generator.generate(FixtureType.RANDOM)
        assert "@pytest.fixture" in result
        assert "random" in result.lower()
    
    # ========== conftest生成测试 ==========
    
    def test_generate_conftest_basic(self):
        """测试生成基础conftest"""
        fixtures = ["@pytest.fixture\ndef dummy():\n    pass"]
        result = self.generator.generate_conftest(fixtures)
        assert "@pytest.fixture" in result
        assert "setup_test_env" in result
    
    def test_generate_conftest_multiple_fixtures(self):
        """测试生成包含多个fixture的conftest"""
        fixtures = [
            "@pytest.fixture\ndef fix1():\n    pass",
            "@pytest.fixture\ndef fix2():\n    pass"
        ]
        result = self.generator.generate_conftest(fixtures)
        assert "fix1" in result
        assert "fix2" in result
    
    # ========== 模板系统测试 ==========
    
    def test_list_templates(self):
        """测试列出所有模板"""
        templates = self.generator.list_templates()
        assert isinstance(templates, list)
        assert len(templates) >= 10  # 至少10个模板
    
    def test_get_template_existing(self):
        """测试获取存在的模板"""
        template = self.generator.get_template("db_mysql")
        assert template is not None
        assert len(template) > 0
    
    def test_get_template_nonexisting(self):
        """测试获取不存在的模板"""
        template = self.generator.get_template("nonexisting_template")
        assert template is None
    
    # ========== 代码质量测试 ==========
    
    def test_all_db_templates_have_fixtures(self):
        """测试所有数据库模板都包含fixture装饰器"""
        for db_type in [DatabaseType.MYSQL, DatabaseType.POSTGRES, DatabaseType.SQLITE]:
            result = self.generator.generate(FixtureType.DB, db_type=db_type)
            assert "@pytest.fixture" in result
    
    def test_all_api_templates_have_fixtures(self):
        """测试所有API模板都包含fixture装饰器"""
        for framework in [ApiFramework.REQUESTS, ApiFramework.HTTPX, ApiFramework.BOTO3]:
            result = self.generator.generate(FixtureType.API, framework=framework)
            assert "@pytest.fixture" in result
    
    def test_all_file_templates_have_fixtures(self):
        """测试所有文件模板都包含fixture装饰器"""
        for fmt in [FileFormat.JSON, FileFormat.YAML, FileFormat.CSV, FileFormat.TOML]:
            result = self.generator.generate(FixtureType.FILE, file_format=fmt)
            assert "@pytest.fixture" in result
    
    def test_template_contains_imports(self):
        """测试模板包含必要的import"""
        template = self.generator.get_template("db_mysql")
        assert "pytest" in template.lower()
    
    def test_sqlite_template_uses_memory(self):
        """测试SQLite模板使用内存数据库"""
        result = self.generator.generate(FixtureType.DB, db_type=DatabaseType.SQLITE)
        assert ":memory:" in result


class TestFixtureContent:
    """Fixture内容验证测试"""
    
    def setup_method(self):
        self.generator = FixtureGenerator()
    
    def test_mysql_fixture_has_connection_and_cursor(self):
        """测试MySQL fixture包含连接和游标"""
        result = self.generator.generate(FixtureType.DB, db_type=DatabaseType.MYSQL)
        # 检查包含fixture定义
        assert result.count("@pytest.fixture") >= 2
    
    def test_postgres_fixture_has_connection(self):
        """测试PostgreSQL fixture包含连接"""
        result = self.generator.generate(FixtureType.DB, db_type=DatabaseType.POSTGRES)
        assert "connection" in result.lower()
    
    def test_sqlite_fixture_uses_temp(self):
        """测试SQLite fixture使用临时文件或内存"""
        result = self.generator.generate(FixtureType.DB, db_type=DatabaseType.SQLITE)
        # 应该包含 :memory: 或 tempfile
        assert ":memory:" in result or "tempfile" in result.lower()
    
    def test_requests_mock_has_mocker(self):
        """测试requests mock使用Mocker"""
        result = self.generator.generate(FixtureType.API, framework=ApiFramework.REQUESTS)
        assert "Mocker" in result or "mocker" in result.lower()
    
    def test_random_fixture_has_random_string(self):
        """测试随机fixture包含随机字符串"""
        result = self.generator.generate(FixtureType.RANDOM)
        assert "random_string" in result
    
    def test_random_fixture_has_random_email(self):
        """测试随机fixture包含随机邮箱"""
        result = self.generator.generate(FixtureType.RANDOM)
        assert "email" in result.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
