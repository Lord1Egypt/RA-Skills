#!/usr/bin/env python3
"""
测试数据生成脚本
生成Spring Boot项目的测试数据
"""

import os
import sys
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml

class TestDataGenerator:
    """测试数据生成器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root).resolve()
        self.test_data_dir = self.project_root / "src" / "test" / "resources"
        self.test_data_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_all_test_data(self) -> Dict[str, str]:
        """生成所有测试数据"""
        generated_files = {}
        
        # 生成SQL测试数据
        sql_file = self.test_data_dir / "test-data.sql"
        sql_content = self._generate_sql_test_data()
        sql_file.write_text(sql_content, encoding="utf-8")
        generated_files["sql"] = str(sql_file)
        
        # 生成JSON测试数据
        json_file = self.test_data_dir / "test-data.json"
        json_content = self._generate_json_test_data()
        json_file.write_text(json.dumps(json_content, indent=2, ensure_ascii=False), encoding="utf-8")
        generated_files["json"] = str(json_file)
        
        # 生成YAML测试数据
        yaml_file = self.test_data_dir / "test-data.yml"
        yaml_content = self._generate_yaml_test_data()
        yaml_file.write_text(yaml.dump(yaml_content, allow_unicode=True, default_flow_style=False), encoding="utf-8")
        generated_files["yaml"] = str(yaml_file)
        
        # 生成边界值测试数据
        boundary_file = self.test_data_dir / "boundary-test-data.sql"
        boundary_content = self._generate_boundary_test_data()
        boundary_file.write_text(boundary_content, encoding="utf-8")
        generated_files["boundary"] = str(boundary_file)
        
        # 生成异常测试数据
        exception_file = self.project_root / "src" / "test" / "java" / "com" / "example" / "demo" / "TestDataFactory.java"
        exception_content = self._generate_test_data_factory()
        exception_file.parent.mkdir(parents=True, exist_ok=True)
        exception_file.write_text(exception_content, encoding="utf-8")
        generated_files["factory"] = str(exception_file)
        
        return generated_files
    
    def _generate_sql_test_data(self) -> str:
        """生成SQL测试数据"""
        now = datetime.now()
        
        sql = """-- 测试数据SQL文件
-- 自动生成于: {timestamp}
-- 用于单元测试和集成测试

-- 清空表（测试前）
DELETE FROM user;
DELETE FROM order;
DELETE FROM product;
DELETE FROM category;

-- 用户表测试数据
INSERT INTO user (id, username, email, phone, status, create_time, update_time) VALUES
-- 正常用户数据
(1, 'normal_user', 'normal@example.com', '13800138000', 1, '{date1}', '{date2}'),
(2, 'active_user', 'active@example.com', '13900139000', 1, '{date3}', '{date4}'),
(3, 'inactive_user', 'inactive@example.com', '13700137000', 0, '{date5}', '{date6}'),

-- 边界用户数据
(4, 'min_user', 'min@example.com', '13000000000', 0, '{date7}', '{date8}'),  -- 最小状态
(5, 'max_user', 'max@example.com', '13999999999', 255, '{date9}', '{date10}'), -- 最大状态
(6, 'long_username', 'longusername@example.com', '13888888888', 1, '{date11}', '{date12}'),

-- 特殊字符用户数据
(7, 'user_with_space', 'space@example.com', '13666666666', 1, '{date13}', '{date14}'),
(8, 'user-with-dash', 'dash@example.com', '13555555555', 1, '{date15}', '{date16}'),
(9, 'user.period', 'period@example.com', '13444444444', 1, '{date17}', '{date18}'),

-- Unicode用户数据
(10, '中文用户', 'chinese@example.com', '13333333333', 1, '{date19}', '{date20}'),
(11, '🎉emoji_user', 'emoji@example.com', '13222222222', 1, '{date21}', '{date22}'),

-- 大量用户数据（性能测试）
{bulk_users}

-- 产品表测试数据
INSERT INTO product (id, name, price, stock, status, category_id, create_time) VALUES
(1, '测试产品1', 99.99, 100, 1, 1, '{date1}'),
(2, '测试产品2', 199.99, 50, 1, 1, '{date2}'),
(3, '测试产品3', 299.99, 0, 0, 2, '{date3}'),  -- 缺货产品
(4, '免费产品', 0.00, 999, 1, 2, '{date4}'),   -- 免费产品
(5, '高价产品', 9999.99, 10, 1, 3, '{date5}'), -- 高价产品

-- 边界产品数据
(6, '最小价格产品', 0.01, 1, 1, 1, '{date6}'),
(7, '最大价格产品', 999999.99, 1, 1, 1, '{date7}'),
(8, '零库存产品', 100.00, 0, 1, 1, '{date8}'),
(9, '大库存产品', 50.00, 10000, 1, 1, '{date9}'),

-- 长名称产品
(10, '{long_product_name}', 150.00, 500, 1, 2, '{date10}'),

-- 订单表测试数据
INSERT INTO `order` (id, order_no, user_id, total_amount, status, create_time, update_time) VALUES
-- 正常订单
(1, 'ORD2024000001', 1, 299.97, 1, '{date1}', '{date2}'),
(2, 'ORD2024000002', 2, 99.99, 2, '{date3}', '{date4}'),
(3, 'ORD2024000003', 1, 199.99, 3, '{date5}', '{date6}'),

-- 边界订单
(4, 'ORD2024000004', 3, 0.01, 1, '{date7}', '{date8}'),   -- 最小金额
(5, 'ORD2024000005', 4, 999999.99, 1, '{date9}', '{date10}'), -- 最大金额
(6, 'ORD2024000006', 5, 0.00, 4, '{date11}', '{date12}'), -- 零金额订单

-- 不同状态订单
(7, 'ORD2024000007', 1, 150.00, 1, '{date13}', '{date14}'), -- 待支付
(8, 'ORD2024000008', 2, 250.00, 2, '{date15}', '{date16}'), -- 已支付
(9, 'ORD2024000009', 3, 350.00, 3, '{date17}', '{date18}'), -- 已发货
(10, 'ORD2024000010', 4, 450.00, 4, '{date19}', '{date20}'), -- 已完成
(11, 'ORD2024000011', 5, 550.00, 5, '{date21}', '{date22}'), -- 已取消

-- 分类表测试数据
INSERT INTO category (id, name, parent_id, level, sort, status, create_time) VALUES
(1, '电子产品', NULL, 1, 1, 1, '{date1}'),
(2, '服装鞋帽', NULL, 1, 2, 1, '{date2}'),
(3, '食品饮料', NULL, 1, 3, 1, '{date3}'),
(4, '手机', 1, 2, 1, 1, '{date4}'),
(5, '电脑', 1, 2, 2, 1, '{date5}'),
(6, '男装', 2, 2, 1, 1, '{date6}'),
(7, '女装', 2, 2, 2, 1, '{date7}'),

-- 边界分类数据
(8, '停用分类', NULL, 1, 99, 0, '{date8}'),
(9, '长名称分类啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊', NULL, 1, 100, 1, '{date9}');

-- 订单详情表测试数据
INSERT INTO order_item (id, order_id, product_id, quantity, price, total_price, create_time) VALUES
(1, 1, 1, 3, 99.99, 299.97, '{date1}'),
(2, 2, 2, 1, 99.99, 99.99, '{date2}'),
(3, 3, 3, 2, 99.99, 199.98, '{date3}'),

-- 边界订单详情
(4, 4, 4, 1, 0.01, 0.01, '{date4}'),   -- 最小数量
(5, 5, 5, 999, 1000.00, 999000.00, '{date5}'), -- 最大数量
(6, 6, 6, 0, 100.00, 0.00, '{date6}'); -- 零数量

-- 验证数据插入
SELECT '用户表记录数:' as table_name, COUNT(*) as record_count FROM user
UNION ALL
SELECT '产品表记录数:', COUNT(*) FROM product
UNION ALL
SELECT '订单表记录数:', COUNT(*) FROM `order`
UNION ALL
SELECT '分类表记录数:', COUNT(*) FROM category
UNION ALL
SELECT '订单详情记录数:', COUNT(*) FROM order_item;
""".format(
            timestamp=now.strftime("%Y-%m-%d %H:%M:%S"),
            date1=(now - timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S"),
            date2=(now - timedelta(days=9)).strftime("%Y-%m-%d %H:%M:%S"),
            date3=(now - timedelta(days=8)).strftime("%Y-%m-%d %H:%M:%S"),
            date4=(now - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S"),
            date5=(now - timedelta(days=6)).strftime("%Y-%m-%d %H:%M:%S"),
            date6=(now - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S"),
            date7=(now - timedelta(days=4)).strftime("%Y-%m-%d %H:%M:%S"),
            date8=(now - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S"),
            date9=(now - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"),
            date10=(now - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
            date11=(now - timedelta(days=10, hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
            date12=(now - timedelta(days=10, hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
            date13=(now - timedelta(days=9, hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
            date14=(now - timedelta(days=9, hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
            date15=(now - timedelta(days=8, hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
            date16=(now - timedelta(days=8, hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
            date17=(now - timedelta(days=7, hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
            date18=(now - timedelta(days=7, hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
            date19=(now - timedelta(days=6, hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
            date20=(now - timedelta(days=6, hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
            date21=(now - timedelta(days=5, hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
            date22=(now - timedelta(days=5, hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
            bulk_users=self._generate_bulk_users(100, 200),  # 生成100-200之间的随机用户
            long_product_name="超长产品名称" + "非常" * 20 + "长的产品名称用于测试边界情况"
        )
        
        return sql
    
    def _generate_bulk_users(self, min_count: int, max_count: int) -> str:
        """生成大量用户数据（用于性能测试）"""
        count = random.randint(min_count, max_count)
        users = []
        
        base_date = datetime.now() - timedelta(days=365)
        
        for i in range(12, 12 + count):  # 从12开始，避免ID冲突
            username = f"bulk_user_{i}"
            email = f"bulk{i}@example.com"
            phone = f"13{random.randint(100000000, 999999999):09d}"
            status = random.choice([0, 1])
            
            # 随机创建时间（过去一年内）
            random_days = random.randint(0, 365)
            random_hours = random.randint(0, 23)
            create_time = base_date + timedelta(days=random_days, hours=random_hours)
            update_time = create_time + timedelta(hours=random.randint(1, 24))
            
            users.append(
                f"({i}, '{username}', '{email}', '{phone}', {status}, "
                f"'{create_time.strftime('%Y-%m-%d %H:%M:%S')}', "
                f"'{update_time.strftime('%Y-%m-%d %H:%M:%S')}')"
            )
        
        return ",\n".join(users)
    
    def _generate_json_test_data(self) -> Dict[str, Any]:
        """生成JSON测试数据"""
        now = datetime.now()
        
        return {
            "metadata": {
                "generated_at": now.isoformat(),
                "purpose": "Spring Boot单元测试数据",
                "version": "1.0.0"
            },
            "test_users": [
                {
                    "id": 1,
                    "username": "test_user_1",
                    "email": "test1@example.com",
                    "phone": "13800138001",
                    "status": 1,
                    "create_time": (now - timedelta(days=7)).isoformat(),
                    "update_time": (now - timedelta(days=1)).isoformat()
                },
                {
                    "id": 2,
                    "username": "test_user_2",
                    "email": "test2@example.com",
                    "phone": "13800138002",
                    "status": 0,
                    "create_time": (now - timedelta(days=14)).isoformat(),
                    "update_time": (now - timedelta(days=7)).isoformat()
                }
            ],
            "test_products": [
                {
                    "id": 1,
                    "name": "测试产品A",
                    "price": 99.99,
                    "stock": 100,
                    "category": "电子产品"
                },
                {
                    "id": 2,
                    "name": "测试产品B",
                    "price": 199.99,
                    "stock": 50,
                    "category": "服装"
                }
            ],
            "test_orders": [
                {
                    "id": 1,
                    "order_no": "TEST001",
                    "user_id": 1,
                    "total_amount": 299.97,
                    "status": "pending",
                    "items": [
                        {"product_id": 1, "quantity": 3, "price": 99.99},
                        {"product_id": 2, "quantity": 1, "price": 199.99}
                    ]
                }
            ],
            "boundary_values": {
                "strings": {
                    "empty": "",
                    "whitespace": "   ",
                    "single_char": "a",
                    "max_length": "a" * 255,
                    "unicode": "🎉测试中文",
                    "special_chars": "test@#$%^&*()"
                },
                "numbers": {
                    "zero": 0,
                    "negative": -1,
                    "positive": 1,
                    "max_int": 2147483647,
                    "min_int": -2147483648,
                    "float": 99.99,
                    "large_float": 999999.99
                },
                "dates": {
                    "min_date": "0001-01-01",
                    "max_date": "9999-12-31",
                    "current": now.date().isoformat(),
                    "past": (now - timedelta(days=365)).date().isoformat(),
                    "future": (now + timedelta(days=365)).date().isoformat()
                }
            },
            "error_cases": {
                "invalid_emails": [
                    "",
                    "invalid",
                    "@example.com",
                    "test@",
                    "test@example",
                    "test@.com"
                ],
                "invalid_phones": [
                    "",
                    "123",
                    "abcdefg",
                    "1380013800a",
                    "+8613800138000"
                ],
                "invalid_usernames": [
                    "",
                    "   ",
                    "a",
                    "a" * 256,
                    "test@user",
                    "user\nname"
                ]
            }
        }
    
    def _generate_yaml_test_data(self) -> Dict[str, Any]:
        """生成YAML测试数据"""
        return {
            "application": {
                "name": "Spring Boot Test Application",
                "version": "1.0.0"
            },
            "test": {
                "profiles": ["test", "integration"],
                "database": {
                    "type": "h2",
                    "url": "jdbc:h2:mem:testdb",
                    "username": "sa",
                    "password": ""
                }
            },
            "data": {
                "users": {
                    "default": {
                        "count": 10,
                        "status_distribution": {
                            "active": 0.7,
                            "inactive": 0.2,
                            "suspended": 0.1
                        }
                    },
                    "boundary": {
                        "min_age": 18,
                        "max_age": 100,
                        "min_salary": 0,
                        "max_salary": 1000000
                    }
                },
                "products": {
                    "categories": ["电子产品", "服装", "食品", "图书", "家居"],
                    "price_range": {
                        "min": 0.01,
                        "max": 9999.99
                    },
                    "stock_range": {
                        "min": 0,
                        "max": 10000
                    }
                }
            },
            "coverage": {
                "targets": {
                    "line": 85,
                    "branch": 80,
                    "method": 90,
                    "class": 95
                },
                "categories": {
                    "unit": 60,
                    "integration": 20,
                    "controller": 10,
                    "service": 10
                }
            }
        }
    
    def _generate_boundary_test_data(self) -> str:
        """生成边界测试数据"""
        sql = """-- 边界值测试数据
-- 专门用于边界条件测试

-- 用户表边界测试数据
INSERT INTO user (id, username, email, phone, status, create_time) VALUES
-- 空值测试
(1001, '', 'empty_username@example.com', '13800000001', 1, NOW()),
(1002, 'empty_email', '', '13800000002', 1, NOW()),
(1003, 'empty_phone', 'empty_phone@example.com', '', 1, NOW()),

-- 最大长度测试
(1004, 'a', 'maxlength@example.com', '13800000004', 1, NOW()),  -- 最小长度用户名
(1005, REPEAT('a', 255), 'longusername@example.com', '13800000005', 1, NOW()),  -- 最大长度用户名
(1006, 'max_email', REPEAT('a', 100) || '@example.com', '13800000006', 1, NOW()),  -- 长邮箱

-- 特殊字符测试
(1007, 'user with space', 'space@example.com', '13800000007', 1, NOW()),
(1008, 'user-with-dash', 'dash@example.com', '13800000008', 1, NOW()),
(1009, 'user.period', 'period@example.com', '13800000009', 1, NOW()),
(1010, 'user_underscore', 'underscore@example.com', '13800000010', 1, NOW()),
(1011, 'user@symbol', 'symbol@example.com', '13800000011', 1, NOW()),  -- @符号在用户名中

-- Unicode测试
(1012, '中文用户', 'chinese@example.com', '13800000012', 1, NOW()),
(1013, '🎉emoji_user', 'emoji@example.com', '13800000013', 1, NOW()),
(1014, 'user_with_😀', 'smile@example.com', '13800000014', 1, NOW()),

-- 数值边界测试
(1015, 'status_min', 'min@example.com', '13800000015', 0, NOW()),      -- 最小状态
(1016, 'status_max', 'max@example.com', '13800000016', 255, NOW()),    -- 最大状态
(1017, 'status_negative', 'negative@example.com', '13800000017', -1, NOW()),  -- 负状态

-- 时间边界测试
(1018, 'min_time', 'mintime@example.com', '13800000018', 1, '1970-01-01 00:00:01'),
(1019, 'max_time', 'maxtime@example.com', '13800000019', 1, '2038-01-19 03:14:07'),
(1020, 'leap_year', 'leap@example.com', '13800000020', 1, '2024-02-29 12:00:00'),

-- NULL值测试（在某些字段允许NULL的情况下）
(1021, NULL, 'null_username@example.com', '13800000021', 1, NOW()),
(1022, 'null_email', NULL, '13800000022', 1, NOW()),
(1023, 'null_status', 'nullstatus@example.com', '13800000023', NULL, NOW());

-- 产品表边界测试数据
INSERT INTO product (id, name, price, stock, status) VALUES
-- 价格边界
(2001, '免费产品', 0.00, 100, 1),          -- 零价格
(2002, '最小价格产品', 0.01, 100, 1),      -- 最小正价格
(2003, '高价产品', 999999.99, 100, 1),    -- 最大价格
(2004, '负价产品', -1.00, 100, 1),        -- 负价格

-- 库存边界
(2005, '零库存产品', 100.00, 0, 1),       -- 零库存
(2006, '单库存产品', 100.00, 1, 1),       -- 最小正库存
(2007, '大库存产品', 100.00, 99999, 1),   -- 大库存
(2008, '负库存产品', 100.00, -1, 1),      -- 负库存

-- 状态边界
(2009, '最小状态产品', 100.00, 100, 0),   -- 最小状态
(2010, '最大状态产品', 100.00, 100, 255), -- 最大状态

-- 名称边界
(2011, '', 100.00, 100, 1),              -- 空名称
(2012, ' ', 100.00, 100, 1),             -- 空格名称
(2013, 'a', 100.00, 100, 1),             -- 单字符名称
(2014, REPEAT('a', 500), 100.00, 100, 1), -- 超长名称

-- 浮点数精度测试
(2015, '精度测试1', 0.3333333333, 100, 1),
(2016, '精度测试2', 99.9999999999, 100, 1),
(2017, '精度测试3', 0.0000000001, 100, 1);

-- 订单表边界测试数据
INSERT INTO `order` (id, order_no, user_id, total_amount, status) VALUES
-- 金额边界
(3001, 'BOUNDARY001', 1001, 0.00, 1),          -- 零金额
(3002, 'BOUNDARY002', 1002, 0.01, 1),          -- 最小正金额
(3003, 'BOUNDARY003', 1003, 999999.99, 1),     -- 最大金额
(3004, 'BOUNDARY004', 1004, -1.00, 1),         -- 负金额

-- 状态边界
(3005, 'BOUNDARY005', 1005, 100.00, 0),        -- 最小状态
(3006, 'BOUNDARY006', 1006, 100.00, 255),      -- 最大状态
(3007, 'BOUNDARY007', 1007, 100.00, -1),       -- 负状态

-- 订单号边界
(3008, '', 1008, 100.00, 1),                   -- 空订单号
(3009, ' ', 1009, 100.00, 1),                  -- 空格订单号
(3010, 'A', 1010, 100.00, 1),                  -- 单字符订单号
(3011, REPEAT('A', 100), 1011, 100.00, 1),     -- 长订单号

-- 用户ID边界
(3012, 'BOUNDARY012', 0, 100.00, 1),           -- 零用户ID
(3013, 'BOUNDARY013', -1, 100.00, 1),          -- 负用户ID
(3014, 'BOUNDARY014', 999999, 100.00, 1);      -- 大用户ID

-- 验证边界数据插入
SELECT '边界用户记录数:' as table_name, COUNT(*) as record_count FROM user WHERE id >= 1000 AND id < 2000
UNION ALL
SELECT '边界产品记录数:', COUNT(*) FROM product WHERE id >= 2000 AND id < 3000
UNION ALL
SELECT '边界订单记录数:', COUNT(*) FROM `order` WHERE id >= 3000 AND id < 4000;
"""
        return sql
    
    def _generate_test_data_factory(self) -> str:
        """生成测试数据工厂类"""
        return """package com.example.demo;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.List;
import java.util.UUID;

/**
 * 测试数据工厂类
 * 生成各种测试场景的数据
 */
public class TestDataFactory {
    
    // 私有构造函数，防止实例化
    private TestDataFactory() {}
    
    /**
     * 创建正常用户
     */
    public static User createNormalUser() {
        User user = new User();
        user.setId(1L);
        user.setUsername("testuser");
        user.setEmail("test@example.com");
        user.setPhone("13800138000");
        user.setStatus(1);
        user.setCreateTime(LocalDateTime.now().minusDays(1));
        user.setUpdateTime(LocalDateTime.now());
        return user;
    }
    
    /**
     * 创建边界用户
     */
    public static User createBoundaryUser() {
        User user = createNormalUser();
        user.setUsername("a".repeat(255));  // 最大长度用户名
        user.setEmail("a".repeat(100) + "@example.com");  // 长邮箱
        user.setPhone("1".repeat(11));  // 11位手机号
        user.setStatus(255);  // 最大状态值
        return user;
    }
    
    /**
     * 创建无效用户（用于异常测试）
     */
    public static User createInvalidUser() {
        User user = new User();
        user.setUsername("");  // 空用户名
        user.setEmail("invalid-email");  // 无效邮箱
        user.setPhone("123");  // 无效手机号
        user.setStatus(-1);  // 无效状态
        return user;
    }
    
    /**
     * 创建空值用户
     */
    public static User createNullUser() {
        User user = new User();
        user.setUsername(null);  // null用户名
        user.setEmail(null);  // null邮箱
        user.setPhone(null);  // null手机号
        user.setStatus(null);  // null状态
        return user;
    }
    
    /**
     * 创建包含特殊字符的用户
     */
    public static User createSpecialCharacterUser() {
        User user = createNormalUser();
        user.setUsername("test user");  // 包含空格
        user.setEmail("test.user@example.com");  // 包含点号
        user.setPhone("+86-138-0013-8000");  // 包含特殊字符
        return user;
    }
    
    /**
     * 创建包含Unicode字符的用户
     */
    public static User createUnicodeUser() {
        User user = createNormalUser();
        user.setUsername("中文用户🎉");
        user.setEmail("中文@例子.中国");
        return user;
    }
    
    /**
     * 创建重复用户名用户（用于冲突测试）
     */
    public static User createDuplicateUsernameUser() {
        User user = createNormalUser();
        user.setUsername("existinguser");  // 已存在的用户名
        return user;
    }
    
    /**
     * 创建重复邮箱用户（用于冲突测试）
     */
    public static User createDuplicateEmailUser() {
        User user = createNormalUser();
        user.setEmail("existing@example.com");  // 已存在的邮箱
        return user;
    }
    
    /**
     * 创建不同状态的用户列表
     */
    public static List<User> createUsersWithDifferentStatuses() {
        User activeUser = createNormalUser();
        activeUser.setStatus(1);  // 活跃
        
        User inactiveUser = createNormalUser();
        inactiveUser.setId(2L);
        inactiveUser.setUsername("inactiveuser");
        inactiveUser.setStatus(0);  // 非活跃
        
        User suspendedUser = createNormalUser();
        suspendedUser.setId(3L);
        suspendedUser.setUsername("suspendeduser");
        suspendedUser.setStatus(2);  // 暂停
        
        User deletedUser = createNormalUser();
        deletedUser.setId(4L);
        deletedUser.setUsername("deleteduser");
        deletedUser.setStatus(-1);  // 删除
        
        return Arrays.asList(activeUser, inactiveUser, suspendedUser, deletedUser);
    }
    
    /**
     * 创建大量用户（用于性能测试）
     */
    public static List<User> createBulkUsers(int count) {
        List<User> users = new java.util.ArrayList<>();
        
        for (int i = 0; i < count; i++) {
            User user = new User();
            user.setId(1000L + i);
            user.setUsername("bulkuser" + i);
            user.setEmail("bulk" + i + "@example.com");
            user.setPhone("138" + String.format("%08d", i));
            user.setStatus(i % 2);  // 交替状态
            user.setCreateTime(LocalDateTime.now().minusDays(i));
            users.add(user);
        }
        
        return users;
    }
    
    /**
     * 创建随机用户
     */
    public static User createRandomUser() {
        User user = new User();
        user.setId(System.currentTimeMillis());
        user.setUsername("user_" + UUID.randomUUID().toString().substring(0, 8));
        user.setEmail("user_" + System.currentTimeMillis() + "@example.com");
        user.setPhone("13" + (100000000 + (int)(Math.random() * 900000000)));
        user.setStatus((int)(Math.random() * 5));  // 0-4随机状态
        user.setCreateTime(LocalDateTime.now().minusDays((int)(Math.random() * 365)));
        return user;
    }
    
    /**
     * 创建边界值测试数据
     */
    public static class BoundaryValues {
        
        // 字符串边界值
        public static final String EMPTY_STRING = "";
        public static final String WHITESPACE_STRING = "   ";
        public static final String SINGLE_CHAR = "a";
        public static final String MAX_LENGTH_STRING = "a".repeat(255);
        public static final String UNICODE_STRING = "🎉测试中文";
        public static final String SPECIAL_CHARS = "test@#$%^&*()";
        
        // 数值边界值
        public static final int MIN_INT = Integer.MIN_VALUE;
        public static final int MAX_INT = Integer.MAX_VALUE;
        public static final long MIN_LONG = Long.MIN_VALUE;
        public static final long MAX_LONG = Long.MAX_VALUE;
        public static final double MIN_DOUBLE = Double.MIN_VALUE;
        public static final double MAX_DOUBLE = Double.MAX_VALUE;
        public static final double NEGATIVE_INFINITY = Double.NEGATIVE_INFINITY;
        public static final double POSITIVE_INFINITY = Double.POSITIVE_INFINITY;
        public static final double NAN = Double.NaN;
        
        // 时间边界值
        public static final LocalDateTime MIN_DATE_TIME = LocalDateTime.MIN;
        public static final LocalDateTime MAX_DATE_TIME = LocalDateTime.MAX;
        public static final LocalDateTime UNIX_EPOCH = 
            LocalDateTime.of(1970, 1, 1, 0, 0, 0);
        public static final LocalDateTime YEAR_2038 = 
            LocalDateTime.of(2038, 1, 19, 3, 14, 7);
        
        private BoundaryValues() {}
    }
    
    /**
     * 创建异常测试数据
     */
    public static class ExceptionTestData {
        
        // 无效邮箱列表
        public static final List<String> INVALID_EMAILS = Arrays.asList(
            "",                     // 空字符串
            " ",                    // 空格
            "invalid",              // 没有@符号
            "@example.com",         // 没有本地部分
            "test@",                // 没有域名
            "test@example",         // 没有顶级域名
            "test@.com",            // 没有二级域名
            "test@com",             // 没有点号
            "test@example..com",    // 连续点号
            "test@-example.com",    // 域名以连字符开头
            "test@example-.com",    // 域名以连字符结尾
            "test@exa mple.com",    // 包含空格
            "test@exa\tmple.com",   // 包含制表符
            "test@exa\\nmple.com",  // 包含换行符
            "test@\"example\".com", // 包含引号
            "test@example.c",       // 过短的顶级域名
            "test@" + "a".repeat(256) + ".com"  // 超长域名
        );
        
        // 无效手机号列表
        public static final List<String> INVALID_PHONES = Arrays.asList(
            "",                     // 空字符串
            " ",                    // 空格
            "123",                  // 过短
            "123456789012",         // 过长
            "abcdefg",              // 包含字母
            "1380013800a",          // 包含字母
            "+8613800138000",       // 包含加号（如果不支持）
            "013800138000",         // 以0开头
            "138-0013-8000",        // 包含连字符
            "138 0013 8000",        // 包含空格
            "138.0013.8000"         // 包含点号
        );
        
        // 无效用户名列表
        public static final List<String> INVALID_USERNAMES = Arrays.asList(
            "",                     // 空字符串
            "   ",                  // 空格
            "a",                    // 过短（如果最小长度>1）
            "a".repeat(256),        // 过长（如果最大长度255）
            "test@user",            // 包含@符号
            "user\nname",           // 包含换行符
            "user\tname",           // 包含制表符
            "user name",            // 包含空格
            "user/name",            // 包含斜杠
            "user\\\\name",         // 包含反斜杠
            "user:name",            // 包含冒号
            "user;name",            // 包含分号
            "user,name",            // 包含逗号
            "user<name",            // 包含小于号
            "user>name",            // 包含大于号
            "user|name",            // 包含竖线
            "user?name",            // 包含问号
            "user*name",            // 包含星号
            "null",                 // 保留字
            "admin",                // 保留字
            "root"                  // 保留字
        );
        
        private ExceptionTestData() {}
    }
}"""
    
    def print_summary(self, generated_files: Dict[str, str]) -> None:
        """打印生成摘要"""
        print("=" * 60)
        print("测试数据生成完成")
        print("=" * 60)
        
        print(f"\n📁 生成文件:")
        for file_type, file_path in generated_files.items():
            print(f"  {file_type.upper():10} -> {file_path}")
        
        print(f"\n📊 包含数据:")
        print("  - 正常流程测试数据")
        print("  - 边界值测试数据")
        print("  - 异常场景测试数据")
        print("  - 性能测试数据")
        print("  - Unicode和特殊字符测试数据")
        
        print(f"\n💡 使用建议:")
        print("  1. SQL文件用于@Sql注解导入测试数据")
        print("  2. JSON/YAML文件用于配置测试")
        print("  3. TestDataFactory用于动态创建测试对象")
        print("  4. 边界数据专门测试边界条件")
        
        print(f"\n🚀 下一步:")
        print("  1. 运行测试: mvn test")
        print("  2. 检查覆盖率: ./scripts/check-coverage.sh")
        print("  3. 生成报告: ./scripts/generate-test-report.py")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python generate-test-data.py <项目根目录>")
        print("示例: python generate-test-data.py /path/to/spring-boot-project")
        sys.exit(1)
    
    project_root = sys.argv[1]
    
    if not os.path.exists(project_root):
        print(f"错误: 项目目录不存在: {project_root}")
        sys.exit(1)
    
    print(f"🔧 开始生成测试数据: {project_root}")
    
    try:
        generator = TestDataGenerator(project_root)
        generated_files = generator.generate_all_test_data()
        generator.print_summary(generated_files)
        
    except Exception as e:
        print(f"❌ 生成测试数据时出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()