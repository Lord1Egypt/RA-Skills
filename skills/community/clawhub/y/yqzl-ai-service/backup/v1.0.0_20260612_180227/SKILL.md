---
name: yqzl-ai-service
description: 封装云启智联AI计费接口服务，支持银行回单解析、银行对账单解析、发票解析、文件解析及异步结果查询。当用户提到回单解析、银行回单、对账单解析、银行对账单、发票解析、发票识别、文件解析、查询任务结果、任务状态、ping等关键词时，自动调用对应接口并返回结果。
---

# 云启智联AI服务（yqzl-ai-service）

## 触发条件

当用户对话中出现以下关键词时，自动识别并调用对应接口：

- **回单解析、银行回单、回单识别** -> 调用 `bank_receipt_parsing`
- **对账单解析、银行对账单、对账单识别** -> 调用 `bank_statement_parsing`
- **发票解析、发票识别** -> 调用 `invoice_parsing`
- **文件解析** -> 调用 `file_parsing`
- **查询结果、任务结果、获取结果、任务状态** -> 调用 `async_result`
- **ping、连通性测试、服务状态** -> 调用 `ping`
- **升级、更新技能、检查版本** -> 调用 `updater.py check` 或 `updater.py update`

## 使用说明

### 1. 获取 API KEY

访问官网注册账号并获取 API KEY：
http://8.135.62.13:5000/

### 2. 配置 API KEY

运行以下命令配置（会自动加密保存到本地）：

```bash
python scripts/config_manager.py set "你的API_KEY"
```

已配置的机器可直接使用，无需重复配置。API KEY 采用基于机器特征的加密存储，避免直接暴露导致泄露。

### 3. 调用接口

**银行回单解析：**
```bash
python scripts/api_client.py bank_receipt_parsing --file /path/to/receipt.pdf
```

**银行对账单解析：**
```bash
python scripts/api_client.py bank_statement_parsing --file-url http://example.com/statement.pdf
```

**发票解析：**
```bash
python scripts/api_client.py invoice_parsing --file /path/to/invoice.jpg
```

**文件解析：**
```bash
python scripts/api_client.py file_parsing --file /path/to/document.pdf
```

**查询异步任务结果：**
```bash
python scripts/api_client.py async_result --task-id xxxxxxxx
```

**服务连通性测试：**
```bash
python scripts/api_client.py ping
```

### 4. 技能自动升级

**检查是否有新版本：**
```bash
python scripts/updater.py check
```

**执行升级：**
```bash
python scripts/updater.py update
```

**查看已备份版本：**
```bash
python scripts/updater.py backups
```

**查看当前版本：**
```bash
python scripts/api_client.py --version
# 或
python scripts/updater.py version
```

升级前会自动备份当前版本到 `backup/` 目录，如遇问题可手动回滚。API KEY 配置文件 `.api_key.enc` 在升级过程中会被保留。

## Agent 调用规范

当识别到用户意图后，按以下步骤执行：

1. **检查 API KEY 是否已配置**：运行 `python scripts/config_manager.py check`
2. **若未配置**：向用户返回友好提示，引导访问 http://8.135.62.13:5000/ 获取 API KEY，并告知配置命令
3. **若已配置**：根据用户提供的文件路径或 URL，构建对应接口调用命令
4. **执行调用**：运行 `python scripts/api_client.py <接口名> [参数]`
5. **返回结果**：将脚本输出整理后返回给用户。若返回了 task_id，提醒用户可通过 async_result 查询结果
6. **错误处理**：若接口调用失败（如超时、网络错误、余额不足等），向用户返回清晰友好的中文错误提示，不要暴露底层异常堆栈
7. **版本检查/升级**：当用户提到升级、更新技能、检查版本等意图时，运行 `python scripts/updater.py check` 检查新版本。若有新版本，询问用户是否执行升级；若用户同意，运行 `python scripts/updater.py update` 执行升级。升级完成后告知用户当前版本号和备份位置。

## 接口参数说明

| 接口 | 必需参数 | 可选参数 |
|------|----------|----------|
| bank_receipt_parsing | --file 或 --file-url | --callback-url |
| bank_statement_parsing | --file 或 --file-url | --callback-url |
| invoice_parsing | --file 或 --file-url | --callback-url |
| file_parsing | --file 或 --file-url | --callback-url |
| async_result | --task-id | 无 |
| ping | 无 | 无 |

## 注意事项

- 计费接口包含：bank_receipt_parsing、bank_statement_parsing、invoice_parsing、file_parsing
- 文件参数支持本地文件路径（--file）或文件URL（--file-url），二者选其一
- 异步解析接口返回 task_id，需通过 async_result 接口查询最终结果
- API KEY 加密存储于本地，绑定当前机器，更换机器需重新配置
- 若接口调用返回 code 非 1000，视为调用失败，需向用户说明原因
