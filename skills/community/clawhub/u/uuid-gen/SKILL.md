---
name: uuid-gen
description: "生成 UUID（通用唯一标识符）。使用场景：(1) 需要为数据库记录、API、文件生成唯一 ID，(2) 批量生成多个 UUID，(3) 需要无连字符的紧凑格式，(4) 验证字符串是否为有效 UUID格式。"
version: 1.0.0
author: 肖总
metadata:
  {
    "openclaw":
      {
        "requires": { }
      },
  }
---

# UUID Generator

简单、安全的 UUID 生成工具。支持多种 UUID 版本和格式。

## 适用场景

| 场景 | 示例 |
|------|------|
| 数据库主键 | "给我生成一个 UUID 做 ID" |
| API 请求追踪 | "生成 request ID" |
| 文件名去重 | "生成唯一文件名" |
| 批量生成 | "给我 10 个 UUID" |
| 验证格式 | "检查这个字符串是不是 UUID" |

## 使用方法

### 1. 生成单个 UUID v4（最常用）

UUID v4 是随机生成的，最常用：

```bash
python -c "import uuid; print(uuid.uuid4())"
```

**输出示例：**
```
550e8400-e29b-41d4-a716-446655440000
```

### 2. 生成无连字符格式（32位）

用于数据库、URL 参数等紧凑场景：

```bash
python -c "import uuid; print(uuid.uuid4().hex)"
```

**输出示例：**
```
550e8400e29b41d4a716446655440000
```

### 3. 批量生成多个 UUID

```bash
python -c "
import uuid
count = 5  # 修改数量
for i in range(1, count + 1):
    print(f'{i}. {uuid.uuid4()}')
"
```

**输出示例：**
```
1. 550e8400-e29b-41d4-a716-446655440000
2. 6ba7b810-9dad-11d1-80b4-00c04fd430c8
3. 6ba7b811-9dad-11d1-80b4-00c04fd430c8
4. 6ba7b812-9dad-11d1-80b4-00c04fd430c8
5. 6ba7b813-9dad-11d1-80b4-00c04fd430c8
```

### 4. 生成带前缀的 UUID（用于命名空间）

```bash
python -c "
import uuid
prefix = 'user'  # 修改前缀
uid = str(uuid.uuid4())[:8]  # 取前8位
print(f'{prefix}_{uid}')
"
```

**输出示例：**
```
user_550e8400
```

### 5. 验证字符串是否为有效 UUID

```bash
python -c "
import uuid

def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False

# 测试
test_values = [
    '550e8400-e29b-41d4-a716-446655440000',
    '550e8400e29b41d4a716446655440000',
    'not-a-uuid',
    '12345'
]

for val in test_values:
    result = '✓ Valid' if is_valid_uuid(val) else '✗ Invalid'
    print(f'{val}: {result}')
"
```

### 6. 比较两个 UUID 是否相同

```bash
python -c "
import uuid

uuid1 = uuid.uuid4()
uuid2 = uuid.uuid4()

print(f'UUID 1: {uuid1}')
print(f'UUID 2: {uuid2}')
print(f'相同: {uuid1 == uuid2}')
"
```

### 7. 从字符串解析 UUID

```bash
python -c "
import uuid

uuid_string = '550e8400-e29b-41d4-a716-446655440000'
try:
    parsed = uuid.UUID(uuid_string)
    print(f'解析成功: {parsed}')
    print(f'版本: {parsed.version}')
    print(f'十六进制: {parsed.hex}')
    print(f'整数: {parsed.int}')
except ValueError as e:
    print(f'解析失败: {e}')
"
```

## UUID 版本对比

| 版本 | 特点 | 使用场景 |
|------|------|----------|
| **v4** | 完全随机 | 通用、推荐、最常用 |
| v1 | 基于时间+MAC地址 | 需要排序/追踪 |
| v3 | 基于 MD5 哈希 | 从名称生成确定性 ID |
| v5 | 基于 SHA1 哈希 | 从名称生成确定性 ID |

**推荐使用 v4**，除非有特殊需求。

## 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `count` | int | 1 | 生成数量 |
| `format` | str | "standard" | 格式："standard"（带连字符）或 "compact"（32位） |
| `prefix` | str | "" | 可选前缀 |
| `version` | int | 4 | UUID 版本：1, 3, 4, 5 |

## 常见使用场景代码

### 生成数据库主键

```bash
python -c "import uuid; print(f\"INSERT INTO users (id, name) VALUES ('{uuid.uuid4()}', '张三');\")"
```

### 生成 API 追踪 ID

```bash
python -c "
import uuid
import datetime

request_id = str(uuid.uuid4())[:8]
timestamp = datetime.datetime.now().isoformat()
print(f'[{timestamp}] Request-{request_id}: 开始处理')
"
```

### 生成唯一文件名

```bash
python -c "
import uuid
import os

original_name = 'document.pdf'
ext = os.path.splitext(original_name)[1]
unique_name = f'{uuid.uuid4().hex}{ext}'
print(f'原文件名: {original_name}')
print(f'唯一文件名: {unique_name}')
"
```

### 生成测试数据

```bash
python -c "
import uuid
import json

users = []
for i in range(3):
    users.append({
        'id': str(uuid.uuid4()),
        'name': f'User{i+1}',
        'email': f'user{i+1}@example.com'
    })

print(json.dumps(users, indent=2))
"
```

## 注意事项

1. **UUID 碰撞概率**：v4 的 122 位随机数，碰撞概率极低，可放心使用
2. **不要自己实现**：总是使用标准库 `uuid`，不要手写随机算法
3. **性能**：Python 的 `uuid.uuid4()` 每秒可生成数百万个，足够快
4. **存储**：数据库中通常存为 CHAR(36) 或 BINARY(16)

## 常见问题

| 问题 | 解决 |
|------|------|
| 需要纯数字 ID | UUID 不是纯数字，用雪花算法或自增 ID |
| 需要有序 ID | 用 UUID v1 或 ULID |
| 需要短 ID | 用 Base58 编码的 UUID 前 8 位 |
| 需要确定性 ID | 用 UUID v3/v5，基于名称生成 |

## 相关资源

- UUID 标准：[RFC 4122](https://tools.ietf.org/html/rfc4122)
- Python uuid 文档：https://docs.python.org/3/library/uuid.html

---

Created: 2026-03-14 by 肖总
