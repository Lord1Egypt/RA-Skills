---
name: seap-shopping
version: 1.0.0
trigger: "用户触发购买、帮我买、预约购买等厂家"
description: 用户在场/不在场购买skill
---

# SEAP Shopping Skill

这是一个用于处理购物需求的 skill，支持用户在场购买和不在场预约购买两种场景。

## 触发条件

当用户对话中包含"买"字时，自动触发此 skill。

## 配置文件

配置文件位于 `seap.config.json`，包含以下配置项：

```json
{
  "authCode": "your_auth_code_here",
  "secretToken": "your_secret_token_here",
  "address": "your_delivery_address_here"
}
```

- **authCode**: 用于调用云侧接口传输的凭证
- **secretToken**: 当用户为不在场购买时，需要将支付token存储，用于后续支付时传入
- **address**: 用户购买后的收货地址

## 依赖工具

依赖 `scripts/seap-cli.js` 执行相关命令。

## 工作流程

### 场景一：用户在场购买

1. 用户发送对话，例如"我想买一瓶红酒"
2. 提取用户意图关键词原文为"queryGoodsIntention"
3. 执行命令：
   ```bash
   node scripts seap-cli search --sessionId=${openclaw当前sessionId} --intent=${queryGoodsIntention} --format md
   ```
4. 将查询后的 markdown 通过对话信息返回商品数据并按顺序标号，供用户进行选择
5. 用户对话确认指定序号商品后，读取 `${openclaw当前sessionId}.json` 文件对应序号的商品，获取商品 "skuId"
6. 若获取到 skuId 则执行以下命令进行购买，否则返回商品不存在提示用户重新选择：
   ```bash
   node scripts seap-cli aipay --sessionId=${openclaw当前sessionId} --skuId=${skuId}
   ```
7. 将购买后的结果信息返回给用户进行提示，根据 success 区分"购买成功"或"购买失败"

### 场景二：用户不在场购买

1. 用户发送对话，例如"三十分钟后帮我买一瓶红酒"
2. 提取用户意图关键词原文为"queryGoodsIntention"，以及定时任务 cron
3. 执行命令：
   ```bash
   node scripts seap-cli search --sessionId=${openclaw当前sessionId} --intent=${queryGoodsIntention} --format md
   ```
4. 将查询后的 markdown 通过对话信息返回商品数据并按顺序标号，供用户进行选择
5. 用户对话确认指定序号商品后，读取 `${openclaw当前sessionId}.json` 文件对应序号的商品，获取商品 "skuId"
6. 若获取到 skuId 后根据 cron 创建定时任务并提醒用户"已创建预约购买任务"，否则返回商品不存在提示用户重新选择
7. 待定时任务启动完成后，则执行以下命令进行购买：
   ```bash
   node scripts seap-cli aipay --sessionId=${openclaw当前sessionId} --skuId=${skuId}
   ```
8. 将购买后的结果信息返回给用户进行提示"预约购买任务已完成"，根据 success 区分"购买成功"或"购买失败"

## 实现说明

### 意图识别

当检测到"买"字时，skill 需要分析用户意图：

- **在场购买**：用户直接表达购买意图，如"我想买..."
- **不在场购买**：用户表达定时购买意图，如"三十分钟后帮我买..."、"明天上午买..."

### 商品选择流程

1. 调用 search 接口获取商品列表
2. 将商品列表格式化为带序号的 markdown
3. 等待用户选择序号
4. 从 json 文件中读取对应的商品信息

### 定时任务创建

对于不在场购买，需要：

1. 解析时间表达式（如"三十分钟后"、"明天上午"）
2. 转换为 cron 表达式
3. 使用 OpenClaw 的 cron 工具创建定时任务
4. 在定时任务中执行购买操作

### 购买执行

1. 调用 aipay 接口执行购买
2. 解析返回结果
3. 根据 success 字段判断购买是否成功
4. 向用户反馈购买结果

## 状态管理

Skill 需要维护以下状态：

- 当前会话的 sessionId
- 用户选择的商品序号
- 购买模式（在场/不在场）
- 定时任务 ID（如果是预约购买）

状态可以存储在临时文件中，文件名为 `${sessionId}_state.json`。