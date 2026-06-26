---
name: suning-bangke
description: 苏宁帮客预约服务
---

# 苏宁帮客预约服务 Skill

## Description
苏宁帮客预约服务，支持用户输入手机号和故障描述进行服务预约下单。

## When to Activate (何时激活)

当用户说以下内容时激活：
- "苏宁帮客" 或 "苏宁预约"
- "预约服务" 或 "预约维修"
- "空调坏了"、"电器坏了" 等故障相关描述
- 提到苏宁帮客服务、苏宁维修服务

## Instructions (指令)

当激活此技能时，帮助用户完成苏宁帮客预约服务。按以下步骤进行：

### 步骤1：收集用户信息
向用户询问以下信息（如果未提供）：
1. **手机号** - 获取用户的联系电话
2. **故障描述** - 获取具体的故障或服务需求（如："空调不制冷"、"冰箱不工作"等）

### 步骤2：确认信息
向用户确认收集到的信息，例如：
```
请确认预约信息：
- 手机号：138XXXX1234
- 故障描述：空调坏了
```

### 步骤3：提交预约（如果用户确认）
使用 POST 请求提交数据到苏宁帮客预约接口：

**接口地址：**
```
https://asapps.suning.com/asapps/mcp/serviceReserveNew
```

**请求方式：** POST
**Content-Type：** application/x-www-form-urlencoded

**请求体参数：**
```
phone=<手机号>
serviceDescription=<故障描述>
```

**执行命令示例：**
```bash
curl -X POST "https://asapps.suning.com/asapps/mcp/serviceReserveNew" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "phone=13812345678" \
  --data-urlencode "serviceDescription=空调坏了"
```

**重要：** 使用 `--data-urlencode` 参数对包含中文的 `serviceDescription` 进行 URL 编码，避免中文乱码问题。

如果用户没有提供联系方式或描述，可以引导用户提供，或者告知用户直接访问苏宁帮客网站进行预约。

### 示例对话

用户："苏宁帮客预约，手机 13812345678，空调坏了"
响应：
```
收到您的预约请求：
- 手机号：13812345678
- 故障描述：空调坏了

正在为您提交苏宁帮客预约服务...
```

然后使用 POST 请求、配合 `--data-urlencode` 向服务器提交预约数据。

## Notes (注意事项)

- ✅ 使用 POST 请求，数据在请求体中，不在 URL 中（更安全）
- ✅ 使用 `--data-urlencode` 对中文参数进行 URL 编码，避免乱码
- 确保手机号格式正确（11位数字）
- 故障描述尽量简洁明确
- 实际提交预约时可能需要额外的验证或登录
- 接口使用生产环境地址

## Security Notes (安全注意事项)

⚠️ **安全改进：**
- ✅ 使用 POST 请求，手机号等 PII 信息不在 URL 查询参数中
- ✅ 避免敏感数据被记录在服务器日志、浏览器历史、HTTP Referrer 头中
- ✅ 提升用户隐私保护级别
- ✅ 使用 `--data-urlencode` 正确处理中文，避免乱码

**理由：** POST 请求将敏感数据放在请求体中，比 GET 请求（URL 参数）更安全。使用 `--data-urlencode` 确保中文等特殊字符正确传输。
