-- ============= 正常测试数据 =============

-- 用户表测试数据
INSERT INTO users (id, username, email, age, status, created_at, updated_at) VALUES
-- 正常用户
(1, 'normal_user', 'normal@example.com', 25, 'ACTIVE', '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(2, 'admin_user', 'admin@example.com', 30, 'ADMIN', '2024-01-01 11:00:00', '2024-01-01 11:00:00'),
(3, 'inactive_user', 'inactive@example.com', 35, 'INACTIVE', '2024-01-01 12:00:00', '2024-01-01 12:00:00'),
(4, 'pending_user', 'pending@example.com', 28, 'PENDING', '2024-01-01 13:00:00', '2024-01-01 13:00:00'),

-- 边界值用户
(5, REPEAT('a', 100), 'max_length@example.com', 0, 'ACTIVE', '1900-01-01 00:00:00', '1900-01-01 00:00:00'),
(6, 'min', 'min@example.com', 150, 'ACTIVE', '2999-12-31 23:59:59', '2999-12-31 23:59:59'),
(7, REPEAT('中', 50), 'chinese@example.com', 18, 'ACTIVE', '2024-01-01 00:00:01', '2024-01-01 00:00:01'),

-- 特殊字符用户
(8, 'user-with-dash', 'user-dash@example.com', 25, 'ACTIVE', '2024-01-01 14:00:00', '2024-01-01 14:00:00'),
(9, 'user_with_underscore', 'user_underscore@example.com', 25, 'ACTIVE', '2024-01-01 15:00:00', '2024-01-01 15:00:00'),
(10, 'user123', 'user123@example.com', 25, 'ACTIVE', '2024-01-01 16:00:00', '2024-01-01 16:00:00');

-- 订单表测试数据
INSERT INTO orders (id, user_id, order_no, amount, status, created_at) VALUES
-- 正常订单
(1, 1, 'ORD202401010001', 100.50, 'PAID', '2024-01-01 10:30:00'),
(2, 1, 'ORD202401010002', 200.00, 'SHIPPED', '2024-01-01 11:30:00'),
(3, 2, 'ORD202401010003', 150.75, 'DELIVERED', '2024-01-01 12:30:00'),
(4, 3, 'ORD202401010004', 300.00, 'CANCELLED', '2024-01-01 13:30:00'),

-- 边界值订单
(5, 5, 'ORD202401010005', 0.01, 'PAID', '1900-01-01 00:00:01'),  -- 最小金额
(6, 6, 'ORD202401010006', 999999.99, 'PAID', '2999-12-31 23:59:58'),  -- 最大金额
(7, 7, REPEAT('A', 50), 500.00, 'PAID', '2024-01-01 00:00:02');  -- 最大长度订单号

-- 商品表测试数据
INSERT INTO products (id, name, price, stock, category, is_active, created_at) VALUES
-- 正常商品
(1, '正常商品A', 99.99, 100, 'ELECTRONICS', true, '2024-01-01 09:00:00'),
(2, '正常商品B', 199.99, 50, 'CLOTHING', true, '2024-01-01 09:30:00'),
(3, '下架商品', 299.99, 0, 'BOOKS', false, '2024-01-01 10:00:00'),

-- 边界值商品
(4, REPEAT('商', 100), 0.01, 0, 'OTHER', true, '2024-01-01 10:30:00'),  -- 最小价格，零库存
(5, '边界商品', 999999.99, 999999, 'OTHER', true, '2024-01-01 11:00:00');  -- 最大价格和库存

-- ============= 关联测试数据 =============

-- 订单商品关联表
INSERT INTO order_items (id, order_id, product_id, quantity, price, created_at) VALUES
(1, 1, 1, 1, 99.99, '2024-01-01 10:31:00'),
(2, 1, 2, 2, 199.99, '2024-01-01 10:32:00'),
(3, 2, 3, 3, 299.99, '2024-01-01 11:31:00');

-- 用户地址表
INSERT INTO user_addresses (id, user_id, address, city, province, postal_code, is_default, created_at) VALUES
(1, 1, '正常地址1号', '北京', '北京市', '100000', true, '2024-01-01 10:05:00'),
(2, 1, '正常地址2号', '上海', '上海市', '200000', false, '2024-01-01 10:10:00'),
(3, 2, REPEAT('长', 200), '广州', '广东省', '510000', true, '2024-01-01 11:05:00');  -- 长地址测试

-- ============= 用于特定测试的数据 =============

-- 重复数据测试
INSERT INTO duplicate_test (id, unique_field, normal_field) VALUES
(1, 'unique_value_1', 'normal_1'),
(2, 'unique_value_2', 'normal_2');

-- 空值和NULL测试
INSERT INTO null_test (id, not_null_field, nullable_field, default_field) VALUES
(1, 'not_null_value', 'nullable_value', 'default_value'),
(2, 'not_null_value_2', NULL, DEFAULT);  -- NULL值和默认值测试

-- 日期时间测试数据
INSERT INTO datetime_test (id, date_field, time_field, datetime_field, timestamp_field) VALUES
(1, '2024-01-01', '10:00:00', '2024-01-01 10:00:00', '2024-01-01 10:00:00'),
(2, '1900-01-01', '00:00:00', '1900-01-01 00:00:00', '1900-01-01 00:00:00'),  -- 最小日期
(3, '2999-12-31', '23:59:59', '2999-12-31 23:59:59', '2999-12-31 23:59:59');  -- 最大日期

-- ============= 状态流转测试数据 =============

-- 状态机测试数据
INSERT INTO status_transition (id, current_status, next_status, allowed) VALUES
(1, 'DRAFT', 'PENDING', true),
(2, 'DRAFT', 'CANCELLED', true),
(3, 'PENDING', 'APPROVED', true),
(4, 'PENDING', 'REJECTED', true),
(5, 'APPROVED', 'COMPLETED', true),
(6, 'DRAFT', 'COMPLETED', false),  -- 不允许的状态流转
(7, 'COMPLETED', 'DRAFT', false);  -- 不允许的状态流转

-- 计数器重置
ALTER TABLE users AUTO_INCREMENT = 1000;
ALTER TABLE orders AUTO_INCREMENT = 1000;
ALTER TABLE products AUTO_INCREMENT = 1000;