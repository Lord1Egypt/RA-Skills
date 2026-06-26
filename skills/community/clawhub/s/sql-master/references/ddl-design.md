# DDL 设计规范

## 表设计原则

### 命名规范
```
表名：小写 + 下划线，加业务前缀
  ods_orders          原始订单表
  dwd_order_detail    订单明细事实表
  dim_user            用户维度表
  dws_user_daily      用户日汇总表
  ads_funnel_report   漏斗报表

列名：小写 + 下划线，语义清晰
  user_id（不用 uid）
  create_time（不用 ctime）
  is_deleted（布尔用 is_ 前缀）
  order_status（不用 status，加业务前缀）
```

### 字段类型选择

```sql
-- 整数：按范围选最小类型（节省存储，提升缓存命中）
TINYINT     -- 1字节，-128~127，适合状态码、等级
SMALLINT    -- 2字节，适合年份、小范围数值
INT         -- 4字节，适合普通 ID（<21亿）
BIGINT      -- 8字节，适合雪花ID、大流水号

-- 字符串
CHAR(n)     -- 定长，适合固定长度（手机号、身份证）
VARCHAR(n)  -- 变长，适合普通文本，n 不要设太大（影响内存分配）
TEXT        -- 大文本，不能建普通索引，不能作为主键

-- 金额：绝对不用 FLOAT/DOUBLE（精度丢失）
DECIMAL(10,2)   -- 精确小数，10位总长，2位小数
-- 或者存分（整数），避免小数运算
BIGINT          -- 单位：分，1元 = 100

-- 时间
DATETIME        -- MySQL，不含时区，'2024-01-15 10:30:00'
TIMESTAMP       -- MySQL，含时区转换，范围到2038年（慎用）
TIMESTAMPTZ     -- PostgreSQL，推荐，含时区

-- 布尔
TINYINT(1)      -- MySQL（没有原生 BOOLEAN）
BOOLEAN         -- PostgreSQL
```

---

## 生产级建表模板

### 业务表（MySQL）
```sql
CREATE TABLE `orders` (
    `id`            BIGINT          NOT NULL AUTO_INCREMENT  COMMENT '主键ID',
    `order_no`      VARCHAR(32)     NOT NULL                 COMMENT '订单号（业务唯一标识）',
    `user_id`       BIGINT          NOT NULL                 COMMENT '用户ID',
    `product_id`    BIGINT          NOT NULL                 COMMENT '商品ID',
    `quantity`      INT             NOT NULL DEFAULT 1       COMMENT '购买数量',
    `unit_price`    DECIMAL(10,2)   NOT NULL                 COMMENT '单价（元）',
    `discount`      DECIMAL(10,2)   NOT NULL DEFAULT 0.00    COMMENT '优惠金额（元）',
    `actual_amount` DECIMAL(10,2)   NOT NULL                 COMMENT '实付金额（元）',
    `status`        TINYINT         NOT NULL DEFAULT 0       COMMENT '订单状态：0待支付 1已支付 2已发货 3已完成 4已取消',
    `remark`        VARCHAR(500)    DEFAULT NULL             COMMENT '备注',
    `is_deleted`    TINYINT(1)      NOT NULL DEFAULT 0       COMMENT '软删除：0正常 1已删除',
    `create_time`   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP  COMMENT '创建时间',
    `update_time`   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_order_no` (`order_no`),
    KEY `idx_user_id_status` (`user_id`, `status`),
    KEY `idx_create_time` (`create_time`)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='订单表';
```

### 日志/流水表（大数据量）
```sql
-- 大流水表：分区 + 不建过多索引
CREATE TABLE `user_behavior_logs` (
    `id`            BIGINT          NOT NULL AUTO_INCREMENT  COMMENT '主键',
    `user_id`       BIGINT          NOT NULL                 COMMENT '用户ID',
    `event_type`    VARCHAR(50)     NOT NULL                 COMMENT '事件类型',
    `event_data`    JSON            DEFAULT NULL             COMMENT '事件数据',
    `ip`            VARCHAR(45)     DEFAULT NULL             COMMENT 'IP地址（支持IPv6）',
    `user_agent`    VARCHAR(500)    DEFAULT NULL             COMMENT 'UA',
    `create_time`   DATETIME(3)     NOT NULL DEFAULT CURRENT_TIMESTAMP(3) COMMENT '创建时间（毫秒精度）',
    PRIMARY KEY (`id`, `create_time`),   -- 分区键必须在主键中
    KEY `idx_user_event` (`user_id`, `event_type`, `create_time`)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COMMENT='用户行为日志'
  PARTITION BY RANGE (TO_DAYS(create_time)) (
    PARTITION p202401 VALUES LESS THAN (TO_DAYS('2024-02-01')),
    PARTITION p202402 VALUES LESS THAN (TO_DAYS('2024-03-01')),
    PARTITION p_future VALUES LESS THAN MAXVALUE
  );
```

### 配置/字典表
```sql
CREATE TABLE `sys_config` (
    `id`            INT             NOT NULL AUTO_INCREMENT  COMMENT '主键',
    `config_key`    VARCHAR(100)    NOT NULL                 COMMENT '配置键',
    `config_value`  TEXT            NOT NULL                 COMMENT '配置值',
    `config_type`   VARCHAR(20)     NOT NULL DEFAULT 'string' COMMENT '值类型：string/int/json/boolean',
    `description`   VARCHAR(500)    DEFAULT NULL             COMMENT '说明',
    `is_enabled`    TINYINT(1)      NOT NULL DEFAULT 1       COMMENT '是否启用',
    `create_time`   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `update_time`   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_config_key` (`config_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统配置表';
```

---

## 在线 DDL 变更（生产安全）

### MySQL 在线 DDL
```sql
-- 查看 DDL 是否支持 INPLACE（不锁表）
-- Algorithm=INPLACE：不重建表，不锁表（最好）
-- Algorithm=COPY：重建表，锁表（最差）

-- 加列（MySQL 8.0 支持 INSTANT，瞬间完成）
ALTER TABLE orders
    ADD COLUMN source VARCHAR(20) DEFAULT NULL COMMENT '来源渠道'
    AFTER status,
    ALGORITHM=INSTANT;  -- MySQL 8.0+

-- 加索引（INPLACE，不锁表）
ALTER TABLE orders
    ADD INDEX idx_product_id (product_id),
    ALGORITHM=INPLACE,
    LOCK=NONE;

-- 修改列类型（通常需要 COPY，会锁表，用 pt-osc 代替）
-- 生产环境用 pt-online-schema-change 或 gh-ost
-- pt-osc: pt-online-schema-change --alter "MODIFY COLUMN amount DECIMAL(12,2)" D=db,t=orders

-- 删除列（INPLACE）
ALTER TABLE orders
    DROP COLUMN old_column,
    ALGORITHM=INPLACE,
    LOCK=NONE;
```

### 字符集迁移（utf8 → utf8mb4）
```sql
-- MySQL 的 utf8 实际上是 utf8mb3（不支持 emoji）
-- 生产迁移步骤：

-- 1. 修改数据库默认字符集
ALTER DATABASE mydb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 2. 修改表（在线 DDL）
ALTER TABLE orders
    CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    ALGORITHM=INPLACE,
    LOCK=NONE;

-- 3. 修改连接字符集
SET NAMES utf8mb4;
-- 或在连接字符串中：charset=utf8mb4
```

---

## 常见设计反模式

```sql
-- ❌ 反模式 1：用字符串存枚举值（无约束，难查询）
status VARCHAR(20)  -- 'active', 'inactive', 'pending'...
-- ✅ 用 TINYINT + 注释说明，或 ENUM（但 ENUM 修改成本高）
status TINYINT COMMENT '1=active 2=inactive 3=pending'

-- ❌ 反模式 2：用逗号分隔存多值
tags VARCHAR(500)  -- '1,2,3,4'
-- ✅ 单独建关联表
CREATE TABLE user_tags (user_id BIGINT, tag_id INT, PRIMARY KEY(user_id, tag_id));

-- ❌ 反模式 3：用 NULL 表示业务含义
discount DECIMAL(10,2)  -- NULL 表示"无折扣"
-- ✅ 用默认值 0，NULL 只表示"未知/未填写"
discount DECIMAL(10,2) NOT NULL DEFAULT 0.00

-- ❌ 反模式 4：主键用 UUID 字符串
id VARCHAR(36) PRIMARY KEY  -- 'a1b2c3d4-...'
-- ✅ 用 BIGINT 自增，或 BIGINT 雪花ID
id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY

-- ❌ 反模式 5：没有 create_time / update_time
-- ✅ 所有业务表必须有这两个字段，便于排查问题和增量同步
```
