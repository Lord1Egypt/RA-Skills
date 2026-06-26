# 快递单号输入格式规范

## 目录
1. [概览](#概览)
2. [CSV格式](#csv格式)
3. [JSON格式](#json格式)
4. [验证规则](#验证规则)
5. [完整示例](#完整示例)

## 概览
本规范定义快递批量查询时输入文件的格式要求。支持CSV和JSON两种格式，脚本会自动解析并提取快递单号。

## CSV格式

### 结构
- 文件编码：UTF-8
- 分隔符：逗号
- 第一行：表头（必须包含 `express_number` 字段）
- 数据行：每行一个快递单号

### 表头字段
| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| express_number | string | 是 | 快递单号 |
| remark | string | 否 | 备注（可选） |

### 示例
```csv
express_number,remark
JD0012345678,京东快递
SF0098765432,顺丰速运
YT0123456789,圆通快递
```

## JSON格式

### 结构
- 文件编码：UTF-8
- 根对象：对象或数组

### 字段定义
| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| express_numbers | array | 是 | 快递单号数组 |
| 或 items | array | 是 | 包含单号和备注的对象数组 |

### 示例格式1：简单数组
```json
{
  "express_numbers": [
    "JD0012345678",
    "SF0098765432",
    "YT0123456789"
  ]
}
```

### 示例格式2：对象数组
```json
{
  "items": [
    {
      "express_number": "JD0012345678",
      "remark": "京东快递"
    },
    {
      "express_number": "SF0098765432",
      "remark": "顺丰速运"
    }
  ]
}
```

## 验证规则

### 单号格式验证
- 单号长度：8-30位字符
- 允许字符：数字、字母（不区分大小写）
- 常见快递公司单号规则：
  - 顺丰：SF开头 + 10-15位数字
  - 京东：JD开头 + 10-15位数字
  - 圆通：YT开头 + 10-15位数字
  - 中通：ZT开头 + 10-15位数字
  - 申通：ST开头 + 10-15位数字
  - EMS：13位数字

### 文件验证
- CSV文件：
  - 必须包含 `express_number` 列
  - 单号列不能为空
  - 单号必须符合格式要求
- JSON文件：
  - 必须包含 `express_numbers` 或 `items` 字段
  - 数组不能为空
  - 单号必须符合格式要求

### 错误处理
- 单号格式错误：跳过该单号并记录警告
- 单号重复：自动去重
- 文件格式错误：抛出异常并提示具体位置

## 完整示例

### 示例1：CSV输入文件（express_list.csv）
```csv
express_number,remark
JD0012345678,手机订单
SF0098765432,书籍
YT0123456789,服装
ZT0987654321,电子产品
```

### 示例2：JSON输入文件（express_list.json）
```json
{
  "express_numbers": [
    "JD0012345678",
    "SF0098765432",
    "YT0123456789",
    "ZT0987654321"
  ]
}
```

### 示例3：复杂JSON（带备注）
```json
{
  "items": [
    {
      "express_number": "JD0012345678",
      "remark": "2024-01-15 手机订单"
    },
    {
      "express_number": "SF0098765432",
      "remark": "2024-01-16 书籍"
    },
    {
      "express_number": "YT0123456789",
      "remark": "2024-01-17 服装"
    }
  ],
  "batch_id": "batch_20240117",
  "description": "今日待查询快递"
}
```

### 使用方式
```bash
# 读取CSV文件
python scripts/express_query.py --numbers JD0012345678,SF0098765432

# 读取JSON文件（需先解析JSON提取单号）
# 示例代码（在智能体中执行）：
import json
with open('./express_list.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    numbers = data.get('express_numbers', [])
    python scripts/express_query.py --numbers ','.join(numbers)
```
