# test-data-gen — 测试数据生成器

## 痛点
- 手动造数据费时费力，格式不规范
- 不同项目需要不同数据格式（JSON/CSV/SQL）
- 需要特定数据库的SQL语法（MySQL/PostgreSQL）
- 难以生成符合业务规则的测试数据（如手机号、邮箱格式）

## 场景
- 快速生成100条用户订单数据进行接口测试
- 导出CSV格式给业务人员核对
- 生成MySQL/PostgreSQL INSERT语句导入测试库
- 批量造数据填充空库进行性能测试

## 定价
- **免费**：基础数据生成（姓名、邮箱、手机号）
- **Pro 19元**：自定义模板 + SQL导出 + 所有数据格式
- **Team 49元**：批量生成（10万条）+ API调用

## 指令格式

### 基本用法
```
test-data-gen [字段名] [数量] [格式]
```

### 生成示例
```
test-data-gen users 100 json          # 生成100条用户JSON
test-data-gen orders 50 csv           # 生成50条订单CSV
test-data-gen products 20 sql mysql   # 生成20条产品SQL（MySQL）
test-data-gen products 20 sql pg      # 生成20条产品SQL（PostgreSQL）
```

### 内置数据模板
| 模板 | 字段 |
|------|------|
| users | id, name, email, phone, age, gender |
| orders | id, user_id, product, amount, status, created_at |
| products | id, name, price, stock, category |
| reviews | id, user_id, product_id, rating, comment |
| addresses | id, user_id, province, city, district, detail |

### 自定义模板（Pro）
```
test-data-gen --template my_template.json 100 json
```

## 字段类型
- `name` — 中文姓名
- `email` — 随机邮箱
- `phone` — 中国手机号（以1开头）
- `age` — 18-80岁
- `gender` — 男/女
- `amount` — 金额（0.01-9999.99）
- `date` — 日期（2020-01-01 ~ 今天）
- `enum` — 自定义枚举值

## 输出格式
- `--format json` — JSON数组
- `--format csv` — CSV（带表头）
- `--format sql --db mysql|pg` — SQL INSERT语句
