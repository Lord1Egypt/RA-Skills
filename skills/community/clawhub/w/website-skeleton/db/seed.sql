-- ============================================================
-- 示例种子数据 — 可重复执行 (使用 INSERT IGNORE)
-- 生成时间: 2026-05-26
-- ============================================================
-- 说明：
--   - 所有 INSERT 使用 IGNORE，防止重复执行报错
--   - 密码字段使用注释标注，需用户自行生成哈希值
--   - 可使用 `node scripts/sample-data.js --hash-passwords > db/seed.sql` 自动生成
--   - 图片使用 picsum.photos 占位 URL
-- ============================================================

-- 清空已有数据（按外键约束顺序）
-- TRUNCATE order_items;
-- TRUNCATE orders;
-- TRUNCATE products;
-- TRUNCATE product_categories;
-- TRUNCATE users;

-- ---------------------------
-- 1. 商品分类
-- ---------------------------
INSERT IGNORE INTO product_categories (id, name, description, sort_order) VALUES (1, '电子产品', '手机、电脑、数码配件等电子产品', 1);
INSERT IGNORE INTO product_categories (id, name, description, sort_order) VALUES (2, '服装', '男装、女装、童装等服饰', 2);
INSERT IGNORE INTO product_categories (id, name, description, sort_order) VALUES (3, '食品', '零食、饮料、生鲜等食品', 3);
INSERT IGNORE INTO product_categories (id, name, description, sort_order) VALUES (4, '书籍', '文学、科技、教育等图书', 4);
INSERT IGNORE INTO product_categories (id, name, description, sort_order) VALUES (5, '家居', '家具、家纺、日用品等家居产品', 5);

-- ---------------------------
-- 2. 商品 (25 个)
-- ---------------------------

-- 电子产品 (category_id = 1)
INSERT IGNORE INTO products (id, name, price, stock, category_id, status, description, image_url) VALUES (1, 'iPhone 15 Pro Max 256GB', 8999.00, 150, 1, 'active', '苹果旗舰手机，A17 Pro 芯片，钛金属设计', 'https://picsum.photos/seed/prod01/400/400');
INSERT IGNORE INTO products (id, name, price, stock, category_id, status, description, image_url) VALUES (2, 'MacBook Air M3 13.6"', 9999.00, 80, 1, 'active', '轻薄笔记本，M3 芯片，18 小时续航', 'https://picsum.photos/seed/prod02/400/400');
INSERT IGNORE INTO products (id, name, price, stock, category_id, status, description, image_url) VALUES (3, 'Sony WH-1000XM5 降噪耳机', 2499.00, 200, 1, 'active', '旗舰级降噪耳机，30 小时续航', 'https://picsum.photos/seed/prod03/400/400');
INSERT IGNORE INTO products (id, name, price, stock, category_id, status, description, image_url) VALUES (4, 'Anker 65W GaN 充电器', 299.00, 500, 1, 'active', '氮化镓快充，支持笔记本/手机多设备', 'https://picsum.photos/seed/prod04/400/400');
INSERT IGNORE INTO products (id, name, price, stock, category_id, status, description, image_url) VALUES (5, 'Samsung 1TB 移动固态硬盘 T7', 899.00, 120, 1, 'active', 'USB 3.2 Gen2，1050MB/s 读写', 'https://picsum.photos/seed/prod05/400/400');
INSERT IGNORE INTO products (id, name, price, stock, category_id, status, description, image_url) VALUES (6, '罗技 MX Master 3S 鼠标', 699.00, 180, 1, 'active', '人体工学设计，8K DPI，无线充电', 'https://picsum.photos/seed/prod06/400/400');
INSERT IGNORE INTO products (id, name, price, stock, category_id, status, description, image_url) VALUES (7, '戴尔 U2723QE 4K 显示器', 4599.00, 40, 1, 'active', '27 英寸 4K IPS Black，USB-C 90W 供电', 'https://picsum.photos/seed/prod07/400/400');
INSERT IGNORE INTO products (id, name, price, stock, category_id, status, description, image_url) VALUES (8, 'Raspberry Pi 5 8GB', 599.00, 300, 1, 'active', '单板电脑，ARM Cortex-A76 四核', 'https://picsum.photos/seed/prod08/400/400');

-- 服装 (category_id = 2)
INSERT IGNORE INTO products (id, name, price, stock, category_id, status, description, image_url) VALUES (9, '经典纯棉白 T 恤', 129.00, 1000, 2, 'active', '100% 新疆棉，宽松版型', 'https://picsum.photos/seed/prod09/400/400');
INSERT IGNORE INTO products (id, name, price, stock, category_id, status, description, image_url) VALUES (10, '轻量羽绒服', 599.00, 300, 2, 'active', '90% 白鹅绒，防风防泼水', 'https://picsum.photos/seed/prod10/400/400');
INSERT IGNORE INTO products (id, name, price, stock, category_id, status, description, image_url) VALUES (11, '修身牛仔裤', 299.00, 500, 2, 'active', '弹力牛仔，百搭款', 'https://picsum.photos/seed/prod11/400/400');
INSERT IGNORE INTO products (id, name, price, stock, category_id, status, description, image_url) VALUES (12, '运动跑步鞋', 459.00, 400, 2, 'active', '缓震回弹，透气网面', 'https://picsum.photos/seed/prod12/400/400');

-- 食品 (category_id = 3)
INSERT IGNORE INTO products (id, name, price, stock, category_id, status, description, image_url) VALUES (13, '有机混合坚果 500g', 89.00, 600, 3, 'active', '腰果、杏仁、核桃混合装', 'https://picsum.photos/seed/prod13/400/400');
INSERT IGNORE INTO products (id, name, price, stock, category_id, status, description, image_url) VALUES (14, '日式抹茶粉 100g', 68.00, 400, 3, 'active', '宇治抹茶，烘焙冲饮皆可', 'https://picsum.photos/seed/prod14/400/400');
INSERT IGNORE INTO products (id, name, price, stock, category_id, status, description, image_url) VALUES (15, '精品咖啡豆 哥伦比亚 250g', 128.00, 250, 3, 'active', '中浅烘焙，柑橘风味', 'https://picsum.photos/seed/prod15/400/400');
INSERT IGNORE INTO products (id, name, price, stock, category_id, status, description, image_url) VALUES (16, '手工黑巧克力 72% 可可 80g', 45.00, 800, 3, 'active', '比利时工艺，低糖健康', 'https://picsum.photos/seed/prod16/400/400');

-- 书籍 (category_id = 4)
INSERT IGNORE INTO products (id, name, price, stock, category_id, status, description, image_url) VALUES (17, '深入理解计算机系统 (CS:APP)', 139.00, 200, 4, 'active', '计算机科学经典教材，第3版', 'https://picsum.photos/seed/prod17/400/400');
INSERT IGNORE INTO products (id, name, price, stock, category_id, status, description, image_url) VALUES (18, '设计模式：可复用面向对象软件的基础', 79.00, 180, 4, 'active', 'GoF 经典设计模式，程序员必读', 'https://picsum.photos/seed/prod18/400/400');
INSERT IGNORE INTO products (id, name, price, stock, category_id, status, description, image_url) VALUES (19, '人类群星闪耀时', 49.00, 350, 4, 'active', '斯蒂芬·茨威格历史特写集', 'https://picsum.photos/seed/prod19/400/400');
INSERT IGNORE INTO products (id, name, price, stock, category_id, status, description, image_url) VALUES (20, '算法导论 (CLRS)', 128.00, 150, 4, 'active', 'MIT 经典算法教材，第4版', 'https://picsum.photos/seed/prod20/400/400');

-- 家居 (category_id = 5)
INSERT IGNORE INTO products (id, name, price, stock, category_id, status, description, image_url) VALUES (21, '人体工学办公椅', 1599.00, 60, 5, 'active', '腰部支撑，可调节扶手，网面透气', 'https://picsum.photos/seed/prod21/400/400');
INSERT IGNORE INTO products (id, name, price, stock, category_id, status, description, image_url) VALUES (22, '北欧风落地灯', 399.00, 120, 5, 'active', '三色温调节，实木底座', 'https://picsum.photos/seed/prod22/400/400');
INSERT IGNORE INTO products (id, name, price, stock, category_id, status, description, image_url) VALUES (23, '纯棉四件套 1.8m 床', 499.00, 200, 5, 'active', '60 支长绒棉，简约印花', 'https://picsum.photos/seed/prod23/400/400');
INSERT IGNORE INTO products (id, name, price, stock, category_id, status, description, image_url) VALUES (24, '智能扫地机器人', 2499.00, 90, 5, 'active', '激光导航，5000Pa 吸力，自动集尘', 'https://picsum.photos/seed/prod24/400/400');
INSERT IGNORE INTO products (id, name, price, stock, category_id, status, description, image_url) VALUES (25, '日式简约陶瓷餐具套装 16件', 299.00, 150, 5, 'active', '哑光釉面，适合 2-4 人使用', 'https://picsum.photos/seed/prod25/400/400');

-- ---------------------------
-- 3. 示例用户
-- 注意: password_hash 需要使用 bcrypt 等工具实际生成
-- 生成方式: node -e "require('bcryptjs').hash('your-password',10).then(console.log)"
-- ---------------------------
INSERT IGNORE INTO users (id, email, password_hash, name, role) VALUES (1, 'admin@example.com', '$2a$10$placeholder_admin_hash_change_me', '管理员', 'admin');
INSERT IGNORE INTO users (id, email, password_hash, name, role) VALUES (2, 'user@example.com', '$2a$10$placeholder_user_hash_change_me', '测试用户', 'user');

-- 密码说明：
--   管理员: email=admin@example.com, password=admin123
--   普通用户: email=user@example.com, password=user123
--   请在导入前替换 password_hash 为实际 bcrypt 哈希值

-- ---------------------------
-- 4. 测试订单
-- ---------------------------
INSERT IGNORE INTO orders (id, order_no, user_id, product_id, qty, amount, total, status, paid_at) VALUES (1, 'ORD-TEST-20240101-0001', 2, 1, 1, 8999.00, 8999.00, 'completed', '2026-01-15 10:30:00');

-- ---------------------------
-- 5. 订单项
-- ---------------------------
INSERT IGNORE INTO order_items (id, order_id, product_id, product_name, qty, price, subtotal) VALUES (1, 1, 1, 'iPhone 15 Pro Max 256GB', 1, 8999.00, 8999.00);

-- ============================================================
-- End of seed data
-- ============================================================
