# 企业微信Webhook API 文档

## 📋 API概览

### 基础信息
- **API文档**: https://developer.work.weixin.qq.com/document/path/99110
- **API类型**: Webhook机器人消息发送
- **请求方式**: POST
- **数据格式**: JSON

## 🔌 API接口

### 发送消息接口
```
POST https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-key
```

### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| key | string | 是 | Webhook机器人密钥 |

## 📝 消息类型

### 1. 文本消息 (text)
```json
{
    "msgtype": "text",
    "text": {
        "content": "消息内容",
        "mentioned_list": ["@all"],
        "mentioned_mobile_list": ["@all"]
    }
}
```

**字段说明**:
- `content`: 消息内容，最长2048字节
- `mentioned_list`: 需要@的成员，`["@all"]`表示@所有人
- `mentioned_mobile_list`: 需要@的成员手机号

### 2. markdown消息 (markdown)
```json
{
    "msgtype": "markdown",
    "markdown": {
        "content": "**标题**\n\n内容"
    }
}
```

**字段说明**:
- `content`: Markdown格式内容，最长4096字节

**支持的Markdown语法**:
- 标题: `# 标题`
- 加粗: `**加粗**`
- 斜体: `*斜体*`
- 链接: `[链接](url)`
- 列表: `- 列表项`
- 引用: `> 引用内容`

### 3. markdown_v2消息 (markdown_v2)
```json
{
    "msgtype": "markdown_v2",
    "markdown_v2": {
        "content": "**标题**\n\n内容",
        "template_id": "template_id",
        "template_data": {
            "key1": "value1",
            "key2": "value2"
        }
    }
}
```

**字段说明**:
- `content`: Markdown V2格式内容
- `template_id`: 模板ID（可选）
- `template_data`: 模板数据（可选）

### 4. 图片消息 (image)
```json
{
    "msgtype": "image",
    "image": {
        "base64": "base64编码的图片内容",
        "md5": "图片的MD5值"
    }
}
```

**字段说明**:
- `base64`: 图片的base64编码
- `md5`: 图片的MD5值

### 5. 图文消息 (news)
```json
{
    "msgtype": "news",
    "news": {
        "articles": [
            {
                "title": "标题",
                "description": "描述",
                "url": "跳转链接",
                "picurl": "图片链接"
            }
        ]
    }
}
```

**字段说明**:
- `articles`: 图文消息列表
- `title`: 标题，最长128字节
- `description`: 描述，最长512字节
- `url`: 跳转链接
- `picurl`: 图片链接

## 📊 响应格式

### 成功响应
```json
{
    "errcode": 0,
    "errmsg": "ok"
}
```

### 错误响应
```json
{
    "errcode": 40014,
    "errmsg": "invalid webhook"
}
```

## 🚨 错误码列表

| 错误码 | 错误说明 | 处理建议 |
|--------|----------|----------|
| 0 | 成功 | - |
| 40014 | Webhook地址无效 | 检查Webhook地址 |
| 40015 | 消息格式错误 | 检查JSON格式 |
| 40016 | 消息长度超限 | 缩短消息内容 |
| 40017 | 调用频率限制 | 降低发送频率 |
| 40018 | 接口频率限制 | 稍后重试 |
| 40019 | 机器人不存在 | 检查机器人配置 |
| 40020 | 机器人已禁用 | 启用机器人 |

## 📈 调用限制

### 频率限制
- **调用频率**: 每分钟不超过20次
- **消息长度**: 文本2048字节，Markdown 4096字节
- **图片大小**: 最大10MB
- **图文消息**: 最多8条图文
- **并发限制**: 建议单线程调用

### 建议策略
1. **消息聚合**: 多条消息合并发送
2. **异步发送**: 非阻塞方式发送
3. **错误重试**: 失败后延迟重试
4. **队列管理**: 消息队列控制发送频率

## 🔧 配置说明

### Webhook地址获取
1. 进入企业微信群聊
2. 点击右上角"群设置"
3. 选择"群机器人"
4. 点击"添加机器人"
5. 复制Webhook地址

### 安全配置
1. **IP白名单**: 配置允许的IP地址
2. **关键词过滤**: 设置敏感词过滤
3. **权限控制**: 限制机器人使用权限
4. **日志审计**: 记录所有发送记录

## 📝 使用示例

### Python调用示例
```python
import requests
import json

def send_wechat_message(content, msg_type="text"):
    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-key"
    
    if msg_type == "text":
        message = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
    elif msg_type == "markdown":
        message = {
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        }
    elif msg_type == "image":
        message = {
            "msgtype": "image",
            "image": {
                "base64": "base64编码",
                "md5": "md5值"
            }
        }
    elif msg_type == "news":
        message = {
            "msgtype": "news",
            "news": {
                "articles": content
            }
        }
    
    response = requests.post(
        webhook_url,
        json=message,
        headers={'Content-Type': 'application/json'}
    )
    
    return response.json()

# 发送文本消息
message = "服务器监控：CPU使用率正常"
result = send_wechat_message(message, "text")
print(result)

# 发送markdown消息
markdown_content = "**📊 系统状态**\n\n- CPU使用率：65%\n- 内存使用率：72%"
result = send_wechat_message(markdown_content, "markdown")
print(result)
```

### cURL调用示例
```bash
# 发送文本消息
curl -X POST \
  https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-key \
  -H 'Content-Type: application/json' \
  -d '{
    "msgtype": "text",
    "text": {
        "content": "服务器告警：CPU使用率超过80%"
    }
  }'

# 发送markdown消息
curl -X POST \
  https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-key \
  -H 'Content-Type: application/json' \
  -d '{
    "msgtype": "markdown",
    "markdown": {
        "content": "**📊 系统监控报告**\n\n- CPU使用率：85%\n- 内存使用率：78%"
    }
  }'
```

## 💡 最佳实践

### 消息设计
1. **简洁明了**: 控制消息长度，突出重点
2. **格式规范**: 统一消息格式标准
3. **分类清晰**: 按重要性分级发送
4. **时间标注**: 包含时间信息便于追踪

### 错误处理
1. **重试机制**: 失败后自动重试
2. **降级策略**: 失败后降级处理
3. **日志记录**: 记录所有发送和错误信息

### 性能优化
1. **批量发送**: 多条消息合并发送
2. **异步处理**: 非阻塞方式提高性能
3. **连接池**: 复用HTTP连接
4. **缓存机制**: 缓存常用消息模板

## 🔒 安全建议

### Webhook安全
1. **保密存储**: 不要硬编码在代码中
2. **权限最小化**: 只授予必要权限
3. **定期更新**: 定期更换Webhook密钥
4. **访问控制**: 限制IP白名单

### 内容安全
1. **输入验证**: 验证消息内容
2. **敏感词过滤**: 过滤敏感信息
3. **内容审计**: 记录发送内容
4. **权限验证**: 验证发送权限

## 📞 故障排查

### 常见问题
1. **Webhook地址错误**: 检查地址是否正确
2. **网络连接问题**: 检查网络连通性
3. **JSON格式错误**: 验证JSON格式
4. **频率限制**: 降低发送频率

### 调试方法
1. **日志分析**: 查看发送日志
2. **返回值检查**: 检查API返回结果
3. **网络测试**: 测试网络连通性
4. **格式验证**: 验证消息格式

---

**参考链接**: 
- [官方文档](https://developer.work.weixin.qq.com/document/path/99110)
- [API详细说明](https://developer.work.weixin.qq.com/document/path/90236)
- [消息类型说明](https://developer.work.weixin.qq.com/document/path/90237)