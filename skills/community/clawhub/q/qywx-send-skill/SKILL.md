---
name: qywx-send-skill
description: 严格按照企业微信文档规范，支持文本、markdown、markdown_v2、图片、图文等多种消息类型的发送技能。
---

# qywx-send-skill

## 功能概述

这个技能严格按照企业微信文档规范，支持以下消息类型：
- ✅ **文本类型** (text) - 支持超长内容自动分片
- ✅ **markdown类型** (markdown) - 支持超长内容自动分片
- ✅ **markdown_v2类型** (markdown_v2) - 支持超长内容自动分片
- ✅ **图片类型** (image)
- ✅ **图文类型** (news)

**注意**: 本技能专注于消息发送功能，不包含告警消息和每日报告的发送功能。

### 新增功能：超长内容分片发送
- ✅ **自动分片**: 当text、markdown、markdown_v2类型的消息内容超过企业微信限制时，自动拆分成多个消息发送
- ✅ **分片标记**: 每个分片消息都包含分片编号信息，便于接收方识别
- ✅ **完整性保证**: 确保长消息的完整传递，避免内容截断

## 使用方法

### 1. 发送文本消息
```
使用qywx-send-skill发送文本消息 [消息内容]
```
**超长内容处理**: 当内容超过2048字节时，会自动分片发送

### 2. 发送markdown消息
```
使用qywx-send-skill发送markdown消息 [消息内容]
```
**超长内容处理**: 当内容超过4096字节时，会自动分片发送

### 3. 发送markdown_v2消息
```
使用qywx-send-skill发送markdown_v2消息 [消息内容]
```
**超长内容处理**: 当内容超过4096字节时，会自动分片发送

### 4. 发送图片消息
```
使用qywx-send-skill发送图片消息 [图片路径或URL]
```

### 5. 发送图文消息
```
使用qywx-send-skill发送图文消息 [标题] [描述] [图片URL] [跳转URL]
```

### 6. 指定自定义Webhook
```
使用qywx-send-skill发送[消息类型] [消息内容]，Webhook地址: [your-webhook-url]
```

## 配置参数

### Webhook地址
- **默认Webhook**: `https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=you-key`
- **自定义Webhook**: 支持用户指定自定义的企业微信Webhook地址

## 消息格式规范

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

## 使用示例

### 示例1: 发送简单文本消息
```
使用qywx-send-skill发送文本消息 服务器监控：CPU使用率正常
```

### 示例2: 发送Markdown消息
```
使用qywx-send-skill发送markdown消息 **📊 系统状态**\n\n- CPU使用率：65%\n- 内存使用率：72%\n- 磁盘使用率：45%
```

### 示例3: 发送长文本消息（自动分片）
```
使用qywx-send-skill发送文本消息 [超过2048字节的长文本内容]
```
**处理**: 自动拆分成多个消息发送，每个分片包含分片编号

### 示例4: 发送长Markdown消息（自动分片）
```
使用qywx-send-skill发送markdown消息 **📊 长报告**\n\n[超过4096字节的详细内容]
```
**处理**: 自动拆分成多个消息发送，每个分片包含分片编号

### 示例5: 发送图片消息
```
使用qywx-send-skill发送图片消息 /path/to/image.png
```

### 示例6: 发送图文消息
```
使用qywx-send-skill发送图文消息 "系统更新通知" "系统将于今晚进行更新维护" "https://example.com/image.png" "https://example.com/detail"
```

### 示例7: 使用自定义Webhook
```
使用qywx-send-skill发送文本消息 测试消息，Webhook地址: https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-key
```

## Python脚本调用

```python
from skills.qywx_send_skill.scripts.send_message import send_wechat_message

# 发送文本消息
result = send_wechat_message("服务器监控：CPU使用率正常", msg_type="text")
print(result)

# 发送markdown消息
markdown_content = "**📊 系统状态**\n\n- CPU使用率：65%\n- 内存使用率：72%"
result = send_wechat_message(markdown_content, msg_type="markdown")
print(result)

# 发送长文本消息（自动分片）
long_text = "长文本内容..." * 1000  # 超过2048字节
result = send_wechat_message(long_text, msg_type="text")
print(f"分片发送结果: {result.get('chunk_count', 1)}片")

# 发送长Markdown消息（自动分片）
long_markdown = "**📊 长报告**\n\n" + "详细内容..." * 1000  # 超过4096字节
result = send_wechat_message(long_markdown, msg_type="markdown")
print(f"分片发送结果: {result.get('chunk_count', 1)}片")

# 发送图片消息
result = send_wechat_message("/path/to/image.png", msg_type="image")
print(result)

# 发送图文消息
articles = [
    {
        "title": "系统更新通知",
        "description": "系统将于今晚进行更新维护",
        "url": "https://example.com/detail",
        "picurl": "https://example.com/image.png"
    }
]
result = send_wechat_message(articles, msg_type="news")
print(result)

# 使用自定义Webhook
result = send_wechat_message("测试消息", msg_type="text", webhook_url="https://your-webhook-url")
print(result)

# 禁用分片发送（强制单条发送，可能失败）
result = send_wechat_message(long_text, msg_type="text", enable_chunking=False)
print(result)
```

## 返回结果

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

## 错误处理

### 常见错误码
- **40014**: Webhook地址无效
- **40015**: 消息内容格式错误
- **40016**: 消息长度超过限制
- **40017**: 接口调用频率限制
- **40018**: 接口频率限制
- **40019**: 机器人不存在
- **40020**: 机器人已禁用

### 错误处理建议
1. 检查Webhook地址是否正确
2. 验证消息格式是否符合要求
3. 控制消息发送频率
4. 检查企业微信应用配置

## 技术实现

### 依赖库
- `urllib.request`: HTTP请求发送
- `json`: 数据格式处理
- `ssl`: HTTPS连接支持
- `base64`: 图片编码处理
- `hashlib`: MD5计算

### 发送流程
1. 构造消息数据
2. 设置HTTP请求头
3. 发送POST请求
4. 处理响应结果

## 最佳实践

### 消息内容优化
1. **简洁明了**: 控制消息长度，突出重点
2. **格式规范**: 使用Markdown增强可读性
3. **定期发送**: 避免频繁发送相同内容
4. **分类发送**: 按重要性分级发送

### Webhook管理
1. **统一管理**: 集中管理Webhook地址
2. **权限控制**: 限制Webhook使用权限
3. **监控告警**: 监控Webhook调用状态
4. **备份机制**: 准备备用Webhook地址

## 注意事项

### 消息限制
- **文本消息**: 最长2048字节
- **Markdown消息**: 最长4096字节
- **Markdown V2消息**: 最长4096字节
- **图片消息**: 支持JPG、PNG格式，最大10MB
- **图文消息**: 最多8条图文
- **发送频率**: 每分钟不超过20条

### 安全性
- **Webhook保密**: 不要泄露Webhook地址
- **内容验证**: 验证发送的消息内容
- **权限控制**: 限制消息发送权限
- **日志审计**: 记录所有发送记录

## 参考文档

- [企业微信开发文档](https://developer.work.weixin.qq.com/document/path/99110)
- [Webhook发送消息API](https://developer.work.weixin.qq.com/document/path/90236)
- [消息类型说明](https://developer.work.weixin.qq.com/document/path/90237)