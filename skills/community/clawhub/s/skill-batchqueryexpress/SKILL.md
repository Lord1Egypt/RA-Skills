---
name: express-batch-query
description: 批量查询快递物流信息；当用户需要查询多个快递单号、获取物流状态或追踪包裹位置时使用
dependency:
  python:
    - openpyxl>=3.1.0
  system: []
---

# 快递批量查询

## 任务目标
- 本 Skill 用于：批量查询多个快递单号的物流轨迹信息
- 能力包含：支持多快递公司、单号批量查询、物流轨迹解析
- 触发条件：用户需要查询物流状态、追踪包裹位置、批量获取快递信息

## 前置准备
- 依赖说明：需要安装 openpyxl 库用于生成Excel文件
  ```bash
  pip install openpyxl>=3.1.0
  ```
- 凭证参数：需提供以下三个凭证参数
  - PlatformID：平台ID
  - MemberID：会员ID
  - APIKey：API密钥
- **获取凭证参数**：请访问小递查查官网 https://xdccy.com 注册账号并获取凭证参数
  1. 打开 https://xdccy.com
  2. 注册/登录账号
  3. 进入用户中心或API管理页面
  4. 获取 PlatformID、MemberID 和 APIKey

## 操作步骤

### 标准流程

1. **获取快递单号**
   - 从用户输入中提取快递单号列表
   - 或读取用户提供的单号文件（CSV/JSON格式）

2. **执行批量查询**
   - 调用 `scripts/express_query.py` 脚本进行查询
   - 必需参数：
     - `--numbers`：快递单号列表，逗号分隔（格式：单号:手机尾号，如 SF123456:6553）
     - `--platform-id`：平台ID (PlatformID)
     - `--member-id`：会员ID (MemberID)
     - `--api-key`：API密钥 (APIKey)
   - 可选参数：
     - `--output`：输出文件路径（支持xlsx/csv/txt/json格式，根据扩展名自动识别）
   - 示例：
     - 不需要手机尾号：`python scripts/express_query.py --numbers 123456,789012 --platform-id xxx --member-id xxx --api-key xxx`
     - 需要手机尾号（如顺丰）：`python scripts/express_query.py --numbers SF5139226181410:6553,SF7890123456789:1234 --platform-id xxx --member-id xxx --api-key xxx`
     - 导出Excel文件：`python scripts/express_query.py --numbers SF5139226181410:6553 --platform-id xxx --member-id xxx --api-key xxx --output results.xlsx`
   - 注意：部分快递（如顺丰）需要提供手机尾号，格式为 `单号:手机尾号`

3. **解析并展示结果**
   - 智能体解析脚本返回的结果
   - 批量查询（单号>1）：显示列表格式（控制台），支持导出Excel/CSV/TXT文件
   - 单个查询：显示完整JSON格式（控制台），支持导出JSON文件
   - Excel格式包含：完整的物流信息字段（运单号、快递公司、物流状态、各时间节点、快递员信息、物流轨迹详情等）
   - CSV格式包含：序号、运单号、快递公司、物流状态、状态码、最后更新时间、最新轨迹、查询状态
   - 列表格式包含：运单号、快递公司、物流状态、最后更新时间、最新轨迹
   - 标注关键节点（已揽收、运输中、派送中、已签收等）
   - **异常处理**：
     - 对异常情况（如单号错误、无物流信息）给出提示
     - 如果查询失败或无轨迹信息，提示："请登录小递查查官网（www.xdccy.com）配置查询渠道"

### 可选分支

- **当单号较少（1-3个）**：直接展示详细物流轨迹
- **当单号较多（超过10个）**：先展示摘要，按需展开详情
- **当查询失败**：分析失败原因，提示用户检查单号或重试
- **当缺少凭证参数**：提示用户访问 https://xdccy.com 获取 PlatformID、MemberID 和 APIKey

## 资源索引

- 必要脚本：见 [scripts/express_query.py](scripts/express_query.py)（用途：调用快递API批量查询物流信息）
- 格式参考：见 [references/input-format.md](references/input-format.md)（何时读取：需要批量处理单号文件时）

## 注意事项

- 脚本会自动识别快递公司类型（通过单号规则）
- 查询结果包含完整物流轨迹和时间戳
- 建议每次查询不超过50个单号以保证性能
- 异常单号会单独标注错误原因
- **手机尾号**：
  - 顺丰快递（SF开头）必须提供手机尾号才能查询
  - 格式为 `运单号:尾号`（如 SF5139226181410:6553）
  - 如果顺丰快递未提供手机尾号，会提示："查询顺丰快递需要手机尾号，请按格式提供：运单号:尾号"
- **渠道配置**：如果查询失败或无物流轨迹，请登录小递查查官网（www.xdccy.com）配置相应的查询渠道

## 使用示例

### 示例1：直接查询单号（控制台显示）
```
用户：查询快递单号 JD0012345678 和 SF0098765432 的物流
执行：
1. 调用脚本：python scripts/express_query.py --numbers JD0012345678,SF0098765432 --platform-id YOUR_PLATFORM_ID --member-id YOUR_MEMBER_ID --api-key YOUR_API_KEY
2. 解析结果并展示列表格式
```

### 示例2：批量查询导出Excel（推荐给客户）
```
用户：批量查询快递单号并导出Excel文件给客户
执行：
1. 读取用户上传的CSV文件（格式见 references/input-format.md）
2. 提取所有单号
3. 调用脚本批量查询：python scripts/express_query.py --numbers 123456,789012,345678 --platform-id YOUR_PLATFORM_ID --member-id YOUR_MEMBER_ID --api-key YOUR_API_KEY --output results.xlsx
4. Excel文件已生成，包含完整的物流信息，可直接发送给客户
```

### 示例3：批量查询导出CSV
```
用户：批量查询快递单号并导出为CSV文件
执行：
1. 调用脚本：python scripts/express_query.py --numbers 123456,789012,345678 --platform-id YOUR_PLATFORM_ID --member-id YOUR_MEMBER_ID --api-key YOUR_API_KEY --output results.csv
2. CSV格式的查询结果已保存至 results.csv
```

### 示例4：批量查询导出TXT
```
用户：批量查询快递单号并导出为TXT文件
执行：
1. 调用脚本：python scripts/express_query.py --numbers 123456,789012,345678 --platform-id YOUR_PLATFORM_ID --member-id YOUR_MEMBER_ID --api-key YOUR_API_KEY --output results.txt
2. TXT列表格式结果已保存至 results.txt
```

### 示例5：单个查询保存JSON
```
用户：查询单个快递单号并保存完整信息
执行：
1. 调用脚本：python scripts/express_query.py --numbers JD0012345678 --platform-id YOUR_PLATFORM_ID --member-id YOUR_MEMBER_ID --api-key YOUR_API_KEY --output result.json
2. JSON格式的完整查询结果已保存至 result.json
```
