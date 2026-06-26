# Test Data Generator - 测试数据生成器

专为测试工程师设计的测试数据生成工具，支持 JSON/CSV/SQL 多种格式输出。

## 安装

```bash
pip install -r requirements.txt
```

或者直接使用：
```bash
python cli.py users 100 json
```

## 快速开始

### 基本用法

```bash
# 生成用户数据（默认）
python cli.py users 100 json

# 生成订单数据 CSV
python cli.py orders 50 csv

# 生成产品数据 SQL (MySQL)
python cli.py products 20 sql mysql

# 生成产品数据 SQL (PostgreSQL)
python cli.py products 20 sql pg
```

### 列出所有模板

```bash
python cli.py --list
```

### 输出到文件

```bash
python cli.py users 1000 json -o users.json
python cli.py orders 100 csv -o orders.csv
```

## 内置模板

| 模板 | 说明 |
|------|------|
| users | 用户数据：id, name, email, phone, age, gender, created_at |
| orders | 订单数据：id, user_id, product, amount, quantity, status, payment_method, created_at |
| products | 产品数据：id, name, category, price, stock, created_at |
| reviews | 评论数据：id, user_id, product_id, rating, comment, created_at |
| addresses | 地址数据：id, user_id, province, city, district, detail, phone, is_default |

## 输出格式

### JSON
```json
[
  {
    "id": 1,
    "name": "张伟",
    "email": "zhangwei123@163.com",
    "phone": "13812345678",
    "age": 28,
    "gender": "男"
  }
]
```

### CSV
```csv
id,name,email,phone,age,gender
1,张伟,zhangwei123@163.com,13812345678,28,男
```

### SQL (MySQL)
```sql
INSERT INTO users (id, name, email, phone, age, gender) VALUES (1, '张伟', 'zhangwei123@163.com', '13812345678', 28, '男');
```

## 作为模块使用

```python
from generator import DataGenerator, generate_from_template

# 使用内置模板
gen = DataGenerator("users")
data = gen.generate(100)
json_data = gen.to_json(data)

# 直接生成
result = generate_from_template("orders", 50, "csv")
```

## 自定义模板

创建模板文件 `my_template.json`:

```json
{
  "fields": {
    "id": {"type": "auto_increment", "start": 1},
    "name": {"type": "name"},
    "custom_field": {"type": "enum", "values": ["A", "B", "C"]}
  }
}
```

使用自定义模板:
```bash
python cli.py custom 100 json --template-file my_template.json
```

## 字段类型

| 类型 | 说明 |
|------|------|
| name | 中文姓名 |
| email | 随机邮箱 |
| phone | 中国手机号 |
| age | 年龄 (默认18-80) |
| gender | 性别 (男/女) |
| amount | 金额 |
| date | 日期 |
| datetime | 日期时间 |
| enum | 自定义枚举 |
| uuid | 唯一ID |
| auto_increment | 自增ID |
| product_name | 产品名称 |
| province | 省份 |
| city | 城市 |
| bool | 布尔值 |
| int | 整数 |
| text | 文本 |

## 运行测试

```bash
pytest tests/ -v
```

## 项目结构

```
test-data-gen/
├── SKILL.md          # 技能描述
├── generator.py      # 核心生成器
├── cli.py            # 命令行入口
├── README.md         # 使用说明
├── requirements.txt  # 依赖
└── tests/
    └── test_generator.py
```

## License

MIT
