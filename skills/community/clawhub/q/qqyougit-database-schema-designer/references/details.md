# 数据库模式设计 - 详细参考

## 一、规范化详解

### 1.1 各范式速查
| 范式 | 要求 | 解决问题 | 实际应用 |
|------|------|---------|---------|
| 1NF | 字段不可再分（原子性） | 重复组/数组 | 几乎所有表 |
| 2NF | 消除部分函数依赖 | 非主属性依赖主键的一部分 | 消除复合主键表 |
| 3NF | 消除传递函数依赖 | 非主属性依赖其他非主属性 | 默认目标 |
| BCNF | 每个决定因素都是候选键 | 主属性间的依赖 | 特殊情况 |
| 4NF | 消除多值依赖 | 独立的多值事实 | 罕见 |

### 1.2 反范式场景（有意违反3NF）
```
适用场景：
1. 高频JOIN → 冗余存储常用字段（用空间换时间）
2. 统计汇总 → 预计算并存储聚合值（如订单数/总金额）
3. 历史快照 → 存储下单时的商品信息（不随商品表变化）
4. 树形结构 → 冗余存储path字段（加速查询）

注意事项：
- 必须通过应用层或触发器保证冗余一致性
- 标注哪些字段是冗余的（注释说明）
- 评估数据不一致的容忍度
```

## 二、主键策略对比

| 策略 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| AUTO_INCREMENT | 简单有序/索引友好 | 可预测/分布式不友好 | 单机小项目 |
| UUID v4 | 全局唯一/安全 | 无序/索引差/36字符 | 分布式系统 |
| UUID v7 | 时间有序+唯一 | 需库支持 | 新项目首选 |
| 雪花算法 | 有序/唯一/64位 | 需部署发生器 | 大规模分布式 |
| ULID | 有序/更短/Crockford Base32 | 较新 | 现代Web应用 |

## 三、索引设计原则

### 3.1 复合索引设计（最左前缀原则）
```
索引 idx_a_b_c (a, b, c)

可匹配的查询：
✅ WHERE a = 1
✅ WHERE a = 1 AND b = 2
✅ WHERE a = 1 AND b = 2 AND c = 3
✅ WHERE a = 1 AND c = 3 (只用a的索引)
❌ WHERE b = 2 (不匹配最左前缀)
❌ WHERE b = 2 AND c = 3 (不匹配最左前缀)

范围查询后的字段不走索引：
✅ WHERE a = 1 AND b > 5 AND c = 3 → a精确+b范围（c不走索引）
```

### 3.2 覆盖索引
```
目的：查询只需访问索引，不需回表

查询：SELECT name, age FROM users WHERE status = 'active'
覆盖索引：idx_status_name_age (status, name, age)

优势：
- 避免回表（随机IO → 顺序IO）
- 大数据量时性能提升10-100倍
```

### 3.3 索引设计检查清单
- [ ] 每个WHERE条件字段都有索引覆盖
- [ ] 复合索引字段顺序正确（等值在前，范围在后）
- [ ] 无冗余索引（索引A是索引B的前缀）
- [ ] 无过度索引（写多读少的表索引不宜过多）
- [ ] 长字符串字段考虑前缀索引
- [ ] EXPLAIN验证索引实际被使用

## 四、分库分表策略

### 4.1 何时需要分表
| 指标 | 阈值 | 建议 |
|------|------|------|
| 单表行数 | >1000万 | 考虑分表 |
| 单表大小 | >10GB | 考虑分表 |
| 查询延迟 | >200ms | 检查是否需要优化/分表 |
| 写入QPS | >5000 | 考虑分库 |

### 4.2 分表策略对比
| 策略 | 方法 | 优点 | 缺点 |
|------|------|------|------|
| 哈希分表 | id % N | 数据均匀 | 范围查询跨表 |
| 范围分表 | 按ID区间/时间 | 范围查询友好 | 数据可能不均匀 |
| 一致性哈希 | 虚拟节点环 | 扩缩容方便 | 实现复杂 |
| 按业务分 | 按租户/地区 | 业务隔离 | 跨业务查询复杂 |

### 4.3 分库分表中间件
| 中间件 | 语言 | 特点 |
|--------|------|------|
| ShardingSphere | Java | 功能全面/社区活跃 |
| MyCat | Java | 基于Cobar改进 |
| Vitess | Go | YouTube出品/云原生 |
| TiDB | Go | 分布式NewSQL/兼容MySQL |

## 五、常用数据模型模板

### 5.1 电商系统核心表
```sql
-- 用户表
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL COMMENT 'bcrypt哈希',
    phone VARCHAR(20) COMMENT '加密存储',
    status TINYINT DEFAULT 1 COMMENT '0禁用1正常',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_status_created (status, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 商品表
CREATE TABLE products (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    category_id BIGINT NOT NULL,
    price DECIMAL(10,2) NOT NULL COMMENT '当前售价',
    original_price DECIMAL(10,2) COMMENT '原价',
    stock INT NOT NULL DEFAULT 0 COMMENT '库存',
    status TINYINT DEFAULT 1 COMMENT '0下架1上架',
    sales_count INT DEFAULT 0 COMMENT '冗余：总销量',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_category_status (category_id, status),
    INDEX idx_sales (sales_count DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 订单表（需分表）
CREATE TABLE orders (
    id BIGINT PRIMARY KEY COMMENT '雪花算法ID',
    user_id BIGINT NOT NULL,
    order_no VARCHAR(32) NOT NULL UNIQUE COMMENT '订单编号',
    total_amount DECIMAL(10,2) NOT NULL,
    status TINYINT NOT NULL DEFAULT 0 COMMENT '0待付款1已付款2已发货3已完成4已取消',
    address_snapshot TEXT COMMENT '地址快照(下单时)',
    paid_at TIMESTAMP NULL,
    shipped_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_status (user_id, status),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 5.2 SaaS多租户模型
```
方案对比：
1. 独立数据库：数据隔离最强，成本最高
2. 共享数据库独立Schema：中等隔离，中等成本
3. 共享Schema+tenant_id：成本最低，隔离最弱

推荐：中小项目用方案3（tenant_id字段），大项目用方案1
```

### 5.3 评论/反馈系统
```sql
-- 评论表（支持嵌套回复）
CREATE TABLE comments (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    target_type VARCHAR(50) NOT NULL COMMENT '关联类型：post/product',
    target_id BIGINT NOT NULL COMMENT '关联ID',
    parent_id BIGINT DEFAULT 0 COMMENT '父评论ID，0为顶级',
    root_id BIGINT DEFAULT 0 COMMENT '根评论ID（加速查询整棵树）',
    user_id BIGINT NOT NULL,
    content TEXT NOT NULL,
    like_count INT DEFAULT 0 COMMENT '冗余：点赞数',
    reply_count INT DEFAULT 0 COMMENT '冗余：回复数',
    status TINYINT DEFAULT 1 COMMENT '0隐藏1正常2待审核',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_target (target_type, target_id, created_at),
    INDEX idx_parent (parent_id, created_at),
    INDEX idx_user (user_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

## 六、迁移脚本模板

### 6.1 标准迁移格式
```sql
-- Migration: 20260614_create_users_table
-- Description: 创建用户表
-- Author: agent
-- Date: 2026-06-14

-- UP
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    -- 字段定义...
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- DOWN (回滚)
DROP TABLE IF EXISTS users;
```

### 6.2 字段变更迁移
```sql
-- Migration: 20260614_add_phone_to_users
-- UP
ALTER TABLE users ADD COLUMN phone VARCHAR(20) COMMENT '加密存储' AFTER email;
CREATE INDEX idx_phone ON users(phone);

-- DOWN
DROP INDEX idx_phone ON users;
ALTER TABLE users DROP COLUMN phone;
```

## 七、设计评审检查清单

### 7.1 基础检查
- [ ] 所有表有主键
- [ ] 字段命名一致（snake_case）
- [ ] 时间字段统一用TIMESTAMP或DATETIME
- [ ] 金额用DECIMAL不用FLOAT
- [ ] 字符集统一utf8mb4
- [ ] 所有字段有注释

### 7.2 性能检查
- [ ] WHERE条件字段有索引
- [ ] 无不必要的索引（影响写入性能）
- [ ] 大表有分区/分表预案
- [ ] JOIN表数量≤3个
- [ ] 无SELECT *

### 7.3 安全检查
- [ ] 密码字段哈希存储
- [ ] 敏感信息字段标注加密
- [ ] 有软删除标记（deleted_at/is_deleted）
- [ ] 有审计字段（created_by/updated_by）

### 7.4 扩展性检查
- [ ] 预留扩展字段或采用EAV模式
- [ ] 分表策略已规划
- [ ] 读写分离兼容性
- [ ] 数据归档策略
