---
name: test-data-gen
description: >
  Generate realistic test data for software testing. Create structured data sets
  with Chinese locale support (names, ID cards, phone numbers, addresses, bank cards).
  Generate SQL inserts, JSON fixtures, CSV files, and API-ready payloads.
  Supports Faker (Python), custom generators, and data masking/desensitization.
  Use when: (1) generating test data for databases or APIs, (2) creating data fixtures,
  (3) building test user accounts, (4) generating Chinese locale data (身份证/手机号/姓名/地址),
  (5) data masking/desensitization for test environments,
  (6) "造数据", "测试数据", "生成数据", "假数据", "mock数据", "数据脱敏",
  "身份证号", "手机号生成", "Faker".
  NOT for: production data management, data analysis, or database administration.
---

# Test Data Generator

Generate realistic, structured test data for testing.

## Quick Generation with Python Faker

Reference: https://faker.readthedocs.io/en/master/

### Install

```bash
pip install faker
```

### Chinese Locale Data

```python
from faker import Faker

fake = Faker('zh_CN')

# Basic personal info
print(fake.name())           # 张三
print(fake.phone_number())   # 13800138000
print(fake.address())        # 北京市朝阳区...
print(fake.company())        # XX科技有限公司
print(fake.email())          # zhangsan@example.com
print(fake.ssn())            # 身份证号 (18位)
print(fake.credit_card_number())  # 银行卡号

# Date/time
print(fake.date_of_birth(minimum_age=18, maximum_age=65))
print(fake.date_between(start_date='-1y', end_date='today'))
```

### Batch Generation Script

Use `scripts/gen_data.py` for batch data generation:

```bash
# Generate 100 users as JSON
python3 scripts/gen_data.py --type users --count 100 --format json --output users.json

# Generate 500 orders as CSV
python3 scripts/gen_data.py --type orders --count 500 --format csv --output orders.csv

# Generate SQL INSERT statements
python3 scripts/gen_data.py --type users --count 50 --format sql --table users --output seed.sql
```

## Data Generation Patterns

### User Data

```python
from faker import Faker
import json, random

fake = Faker('zh_CN')

def gen_user(uid):
    return {
        "id": uid,
        "name": fake.name(),
        "email": fake.ascii_free_email(),
        "phone": fake.phone_number(),
        "id_card": fake.ssn(),
        "gender": random.choice(["male", "female"]),
        "birth_date": str(fake.date_of_birth(minimum_age=18, maximum_age=60)),
        "address": fake.address(),
        "created_at": str(fake.date_time_between(start_date='-2y')),
        "status": random.choices(["active", "inactive", "banned"],
                                weights=[85, 10, 5])[0],
    }

users = [gen_user(i) for i in range(1, 101)]
print(json.dumps(users, ensure_ascii=False, indent=2))
```

### Order Data (with foreign keys)

```python
def gen_order(oid, user_ids, product_ids):
    qty = random.randint(1, 10)
    price = round(random.uniform(9.9, 999.9), 2)
    return {
        "id": oid,
        "user_id": random.choice(user_ids),
        "product_id": random.choice(product_ids),
        "quantity": qty,
        "unit_price": price,
        "total": round(qty * price, 2),
        "status": random.choices(
            ["pending", "paid", "shipped", "delivered", "cancelled"],
            weights=[10, 20, 25, 40, 5])[0],
        "created_at": str(fake.date_time_between(start_date='-6m')),
        "address": fake.address(),
    }
```

### Boundary & Edge Case Data

Always include these special values in test datasets:

```python
EDGE_CASES = {
    "string": [
        "",                          # empty
        " ",                         # whitespace only
        "a" * 256,                   # max length
        "a" * 257,                   # over max length
        "<script>alert(1)</script>", # XSS
        "' OR 1=1 --",              # SQLi
        "张三\x00李四",              # null byte
        "🔍 emoji test 🎉",         # emoji
        "Ñoño café résumé",         # unicode accents
    ],
    "number": [0, -1, 1, 2147483647, -2147483648, 0.001, 99999999.99],
    "date": ["1970-01-01", "2099-12-31", "2000-02-29", "2001-02-29"],  # leap year
    "phone": ["13800138000", "19900001111", "12345678901", "1380013800"],  # boundary
}
```

## Output Formats

### SQL INSERT

```python
def to_sql(users, table="users"):
    cols = users[0].keys()
    lines = [f"INSERT INTO {table} ({','.join(cols)}) VALUES"]
    for i, u in enumerate(users):
        vals = []
        for v in u.values():
            if v is None:
                vals.append("NULL")
            elif isinstance(v, (int, float)):
                vals.append(str(v))
            else:
                vals.append(f"'{str(v).replace(chr(39), chr(39)*2)}'")
        sep = "," if i < len(users) - 1 else ";"
        lines.append(f"  ({','.join(vals)}){sep}")
    return "\n".join(lines)
```

### CSV

```python
import csv

def to_csv(data, filepath):
    with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
```

### JSON Fixture

```python
def to_json(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
```

## Chinese ID Card Validation

Reference: GB 11643-1999 (公民身份号码标准)

```python
def validate_id_card(id_number: str) -> bool:
    """Validate Chinese 18-digit ID card number per GB 11643-1999."""
    if len(id_number) != 18:
        return False
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_codes = '10X98765432'
    try:
        total = sum(int(id_number[i]) * weights[i] for i in range(17))
        return check_codes[total % 11] == id_number[17].upper()
    except (ValueError, IndexError):
        return False

def gen_valid_id_card():
    """Generate a valid Chinese ID card number with correct checksum."""
    import random
    # Area codes (sample: Beijing, Shanghai, Guangdong)
    areas = ['110101', '310101', '440106', '330102', '510104']
    area = random.choice(areas)
    birth = fake.date_of_birth(minimum_age=18, maximum_age=60).strftime('%Y%m%d')
    seq = f"{random.randint(0, 999):03d}"
    base = area + birth + seq
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_codes = '10X98765432'
    total = sum(int(base[i]) * weights[i] for i in range(17))
    return base + check_codes[total % 11]
```

## Data Masking / Desensitization

For copying production data to test environments:

```python
def mask_phone(phone: str) -> str:
    """138****8000"""
    if len(phone) >= 11:
        return phone[:3] + "****" + phone[7:]
    return "***"

def mask_id_card(id_card: str) -> str:
    """110101****0001"""
    if len(id_card) >= 18:
        return id_card[:6] + "********" + id_card[14:]
    return "***"

def mask_name(name: str) -> str:
    """张*"""
    if len(name) >= 2:
        return name[0] + "*" * (len(name) - 1)
    return "*"

def mask_email(email: str) -> str:
    """z***@example.com"""
    local, domain = email.split("@")
    return local[0] + "***@" + domain

def mask_bank_card(card: str) -> str:
    """6222 **** **** 1234"""
    if len(card) >= 16:
        return card[:4] + " **** **** " + card[-4:]
    return "****"
```

## Tips

- Always use `ensure_ascii=False` for Chinese JSON output
- Use `utf-8-sig` encoding for CSV files opened in Excel
- Set `Faker.seed(42)` for reproducible test data
- Mix normal data (90%) with edge cases (10%) for realistic coverage
- Include data relationships (FK references) when generating related tables
- For large datasets (>10k rows), use batch inserts and transactions
