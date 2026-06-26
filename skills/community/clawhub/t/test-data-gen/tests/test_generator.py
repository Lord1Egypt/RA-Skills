"""
测试数据生成器 - 单元测试
"""

import pytest
import json
import csv
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from generator import (
    DataGenerator, random_name, random_email, random_phone,
    random_age, random_gender, random_amount, random_date,
    random_address, random_product_name, DEFAULT_TEMPLATES
)


class TestRandomFunctions:
    """测试随机数据生成函数"""

    def test_random_name(self):
        """测试姓名生成"""
        for _ in range(100):
            name = random_name()
            assert len(name) >= 2
            assert len(name) <= 4

    def test_random_email(self):
        """测试邮箱生成"""
        for _ in range(100):
            email = random_email()
            assert "@" in email
            assert "." in email.split("@")[1]

    def test_random_phone(self):
        """测试手机号生成"""
        for _ in range(100):
            phone = random_phone()
            assert len(phone) == 11
            assert phone.startswith("1")

    def test_random_age(self):
        """测试年龄生成"""
        for _ in range(100):
            age = random_age(18, 60)
            assert 18 <= age <= 60

    def test_random_gender(self):
        """测试性别生成"""
        genders = [random_gender() for _ in range(100)]
        assert all(g in ["男", "女"] for g in genders)

    def test_random_amount(self):
        """测试金额生成"""
        for _ in range(100):
            amount = random_amount(1.0, 100.0)
            assert 1.0 <= amount <= 100.0

    def test_random_date(self):
        """测试日期生成"""
        for _ in range(100):
            date_str = random_date(2020)
            assert len(date_str) == 10
            parts = date_str.split("-")
            assert len(parts) == 3
            assert 2020 <= int(parts[0]) <= 2030

    def test_random_address(self):
        """测试地址生成"""
        addr = random_address()
        assert "province" in addr
        assert "city" in addr
        assert "district" in addr
        assert "detail" in addr

    def test_random_product_name(self):
        """测试产品名称生成"""
        for _ in range(100):
            name = random_product_name()
            assert len(name) > 0


class TestDataGenerator:
    """测试数据生成器类"""

    def test_generator_init(self):
        """测试生成器初始化"""
        gen = DataGenerator("users")
        assert gen.template_name == "users"

    def test_generate_users(self):
        """测试生成用户数据"""
        gen = DataGenerator("users")
        data = gen.generate(10)
        assert len(data) == 10
        assert "name" in data[0]
        assert "email" in data[0]
        assert "phone" in data[0]

    def test_generate_orders(self):
        """测试生成订单数据"""
        gen = DataGenerator("orders")
        data = gen.generate(5)
        assert len(data) == 5
        assert "product" in data[0]
        assert "amount" in data[0]
        assert "status" in data[0]

    def test_generate_products(self):
        """测试生成产品数据"""
        gen = DataGenerator("products")
        data = gen.generate(20)
        assert len(data) == 20
        assert "name" in data[0]
        assert "price" in data[0]
        assert "stock" in data[0]

    def test_auto_increment(self):
        """测试自增ID"""
        gen = DataGenerator("users")
        data = gen.generate(10)
        ids = [r["id"] for r in data]
        assert ids == list(range(1, 11))

    def test_to_json(self):
        """测试JSON输出"""
        gen = DataGenerator("users")
        data = gen.generate(2)
        json_str = gen.to_json(data)
        parsed = json.loads(json_str)
        assert len(parsed) == 2

    def test_to_csv(self):
        """测试CSV输出"""
        gen = DataGenerator("users")
        data = gen.generate(2)
        csv_str = gen.to_csv(data)
        lines = csv_str.strip().split("\n")
        assert len(lines) == 3  # 1 header + 2 data

    def test_to_sql_mysql(self):
        """测试MySQL SQL输出"""
        gen = DataGenerator("users")
        data = gen.generate(1)
        sql = gen.to_sql(data, "mysql")
        assert "INSERT INTO users" in sql
        assert "VALUES" in sql

    def test_to_sql_pg(self):
        """测试PostgreSQL SQL输出"""
        gen = DataGenerator("users")
        data = gen.generate(1)
        sql = gen.to_sql(data, "pg")
        assert "INSERT INTO users" in sql

    def test_get_available_templates(self):
        """测试获取模板列表"""
        templates = DataGenerator.get_available_templates()
        assert "users" in templates
        assert "orders" in templates
        assert "products" in templates


class TestEdgeCases:
    """边界情况测试"""

    def test_generate_zero(self):
        """测试生成0条数据"""
        gen = DataGenerator("users")
        data = gen.generate(0)
        assert len(data) == 0

    def test_empty_to_csv(self):
        """测试空数据CSV"""
        gen = DataGenerator("users")
        csv_str = gen.to_csv([])
        assert csv_str == ""

    def test_empty_to_sql(self):
        """测试空数据SQL"""
        gen = DataGenerator("users")
        sql = gen.to_sql([])
        assert sql == ""

    def test_special_characters(self):
        """测试特殊字符转义"""
        gen = DataGenerator("users")
        data = [{"name": "O'Brien", "email": "test@test.com"}]
        sql = gen.to_sql(data)
        assert "O''Brien" in sql  # 单引号应该被转义


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
