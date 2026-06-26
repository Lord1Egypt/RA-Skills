# qywx-send-skill 使用示例

## 🚀 快速开始

### 1. 发送文本消息
发送简单文本消息到企业微信

```
使用qywx-send-skill发送文本消息 服务器监控：CPU使用率正常
```

**预期输出**:
```
✅ 消息发送成功！
📤 发送内容: 服务器监控：CPU使用率正常...
```

### 2. 发送markdown消息
发送格式化的Markdown消息

```
使用qywx-send-skill发送markdown消息 **📊 系统状态**\n\n- CPU使用率：65%\n- 内存使用率：72%\n- 磁盘使用率：45%
```

**预期输出**:
```
✅ 消息发送成功！
📤 发送内容: **📊 系统状态**\n\n- CPU使用率：65%...
```

### 3. 发送markdown_v2消息
发送Markdown V2格式消息

```
使用qywx-send-skill发送markdown_v2消息 **📊 系统状态**\n\n- CPU使用率：65%\n- 内存使用率：72%
```

**预期输出**:
```
✅ 消息发送成功！
📤 发送内容: **📊 系统状态**\n\n- CPU使用率：65%...
```

### 4. 发送图片消息
发送图片消息

```
使用qywx-send-skill发送图片消息 /path/to/image.png
```

**预期输出**:
```
✅ 消息发送成功！
📤 发送类型: image
```

### 5. 发送图文消息
发送图文消息

```
使用qywx-send-skill发送图文消息 "系统更新通知" "系统将于今晚进行更新维护" "https://example.com/image.png" "https://example.com/detail"
```

**预期输出**:
```
✅ 消息发送成功！
📤 发送类型: news
```

### 6. 指定自定义Webhook
使用自定义的企业微信Webhook地址

```
使用qywx-send-skill发送文本消息 测试消息，Webhook地址: https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-key
```

**预期输出**:
```
✅ 消息发送成功！
📤 发送内容: 测试消息...
```

---

## 📊 实际应用场景

### 场景1: 系统状态通知
**需求**: 定时发送系统运行状态

**命令**:
```
使用qywx-send-skill发送markdown消息 **📊 系统状态报告**\n\n**⏰ 时间**：2026-03-19 13:30\n**📈 CPU使用率**：65%\n**💾 内存使用率**：72%\n**🗄️ 磁盘使用率**：45%\n**🌐 网络状态**：正常
```

### 场景2: 部署完成通知
**需求**: 代码部署完成后发送通知

**命令**:
```
使用qywx-send-skill发送markdown消息 **🚀 部署完成通知**\n\n**项目名称**：chezhuyun-daijia-aggregation\n**版本号**：v2.1.0\n**部署时间**：2026-03-19 14:30\n**部署状态**：✅ 成功\n**负责人**：王兴华
```

### 场景3: 会议提醒
**需求**: 发送会议提醒通知

**命令**:
```
使用qywx-send-skill发送markdown消息 **📅 会议提醒**\n\n**会议主题**：周例会\n**会议时间**：今天下午2:00\n**会议地点**：会议室A\n**参会人员**：技术部全体成员\n**注意事项**：请准备本周工作总结
```

### 场景4: 图片通知
**需求**: 发送系统监控截图

**命令**:
```
使用qywx-send-skill发送图片消息 /path/to/monitoring-screenshot.png
```

### 场景5: 图文通知
**需求**: 发送系统更新通知

**命令**:
```
使用qywx-send-skill发送图文消息 "系统更新通知" "系统将于今晚22:00-24:00进行更新维护，请提前做好准备。" "https://example.com/update-image.png" "https://example.com/update-detail"
```

---

## 🔧 Python脚本调用示例

### 基本调用
```python
from skills.qywx_send_skill.scripts.send_message import send_wechat_message

# 发送文本消息
result = send_wechat_message("服务器监控：CPU使用率正常", msg_type="text")
if result["success"]:
    print("✅ 消息发送成功")
else:
    print(f"❌ 发送失败: {result['error']}")
```

### Markdown消息
```python
# 发送Markdown格式消息
markdown_content = """
**📊 系统监控报告**

- **CPU使用率**：65%
- **内存使用率**：72%
- **磁盘使用率**：45%
- **网络状态**：正常

**报告时间**：2026-03-19 13:30
"""

result = send_wechat_message(markdown_content, msg_type="markdown")
```

### Markdown V2消息
```python
# 发送Markdown V2格式消息
markdown_v2_content = {
    "content": "**📊 系统监控报告**\n\n- CPU使用率：65%\n- 内存使用率：72%",
    "template_id": "your-template-id",
    "template_data": {
        "cpu": "65%",
        "memory": "72%"
    }
}

result = send_wechat_message(markdown_v2_content, msg_type="markdown_v2")
```

### 图片消息
```python
# 发送图片消息
result = send_wechat_message("/path/to/monitoring-screenshot.png", msg_type="image")
```

### 图文消息
```python
# 发送图文消息
from skills.qywx_send_skill.scripts.send_message import create_news_article

article = create_news_article(
    title="系统更新通知",
    description="系统将于今晚22:00-24:00进行更新维护",
    url="https://example.com/update-detail",
    picurl="https://example.com/update-image.png"
)

result = send_wechat_message(article, msg_type="news")
```

### 自定义Webhook
```python
# 使用自定义Webhook地址
custom_webhook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-key"
result = send_wechat_message("测试消息", msg_type="text", webhook_url=custom_webhook)
```

---

## 📱 消息格式示例

### 文本消息格式
```
服务器监控：CPU使用率正常
```

### Markdown消息格式
```
**📊 系统状态报告**

**⏰ 时间**：2026-03-19 13:30
**📈 CPU使用率**：65%
**💾 内存使用率**：72%
**🗄️ 磁盘使用率**：45%
**🌐 网络状态**：正常
```

### Markdown V2消息格式
```
**📊 系统状态报告**

- CPU使用率：{{cpu}}
- 内存使用率：{{memory}}
- 磁盘使用率：{{disk}}
```

### 图片消息格式
```
图片文件路径或URL
```

### 图文消息格式
```
标题：系统更新通知
描述：系统将于今晚进行更新维护
图片：https://example.com/image.png
链接：https://example.com/detail
```

---

## 🎯 高级功能

### 1. 批量消息发送
```python
# 批量发送不同类型的消息
messages = [
    ("text", "服务器监控：CPU使用率正常"),
    ("markdown", "**📊 系统状态**\n\n- CPU使用率：65%"),
    ("image", "/path/to/image.png"),
]

for msg_type, content in messages:
    result = send_wechat_message(content, msg_type=msg_type)
    print(f"发送结果: {result['success']}")
```

### 2. 定时消息发送
```python
import schedule
import time

def send_status_report():
    """发送状态报告"""
    content = "**📊 定时状态报告**\n\n- CPU使用率：65%\n- 内存使用率：72%"
    result = send_wechat_message(content, msg_type="markdown")
    print(f"定时报告发送结果: {result['success']}")

# 设置定时任务
schedule.every().hour.do(send_status_report)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### 3. 错误重试机制
```python
import time

def send_with_retry(message, msg_type, max_retries=3):
    """带重试的消息发送"""
    for attempt in range(max_retries):
        result = send_wechat_message(message, msg_type=msg_type)
        if result["success"]:
            return result
        else:
            print(f"发送失败，第{attempt + 1}次重试...")
            time.sleep(5 * (attempt + 1))  # 递增等待时间
    
    print("发送失败，达到最大重试次数")
    return result
```

---

## 💡 使用技巧

### 1. 消息模板
```python
# 系统状态消息模板
STATUS_TEMPLATE = """
**📊 系统状态报告**

- **CPU使用率**：{cpu}
- **内存使用率**：{memory}
- **磁盘使用率**：{disk}
- **网络状态**：{network}

**报告时间**：{timestamp}
"""

def format_status_message(cpu, memory, disk, network):
    """格式化状态消息"""
    return STATUS_TEMPLATE.format(
        cpu=cpu,
        memory=memory,
        disk=disk,
        network=network,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M")
    )
```

### 2. 消息分级
```python
# 根据重要性选择消息类型
def send_by_priority(message, priority):
    """根据优先级选择消息类型"""
    if priority == "high":
        # 重要消息使用markdown格式
        return send_wechat_message(message, msg_type="markdown")
    else:
        # 一般消息使用文本格式
        return send_wechat_message(message, msg_type="text")
```

### 3. 消息队列
```python
import queue
import threading

# 消息队列
message_queue = queue.Queue()

def message_sender():
    """消息发送线程"""
    while True:
        try:
            message_data = message_queue.get(timeout=1)
            result = send_wechat_message(**message_data)
            print(f"发送结果: {result['success']}")
            message_queue.task_done()
        except queue.Empty:
            continue

# 启动发送线程
sender_thread = threading.Thread(target=message_sender, daemon=True)
sender_thread.start()

# 添加消息到队列
message_queue.put({
    "content": "服务器监控：CPU使用率正常",
    "msg_type": "text"
})
```

---

## 🚨 故障排查

### 1. Webhook地址错误
**现象**: `消息发送失败: invalid webhook`

**解决**:
- 检查Webhook地址是否正确
- 确认机器人是否已启用
- 验证Webhook地址是否包含`key`参数

### 2. 消息格式错误
**现象**: `消息发送失败: invalid message`

**解决**:
- 检查JSON格式是否正确
- 验证消息长度是否超限
- 确认消息类型是否支持

### 3. 网络连接问题
**现象**: `消息发送失败: connection timeout`

**解决**:
- 检查网络连通性
- 验证防火墙设置
- 尝试使用HTTP代理

### 4. 图片处理问题
**现象**: `消息发送失败: image process error`

**解决**:
- 检查图片路径是否正确
- 确认图片格式是否支持
- 验证图片大小是否超限

---

## 📈 最佳实践

### 1. 消息内容优化
- **简洁明了**: 控制消息长度，突出重点
- **格式规范**: 统一消息格式标准
- **分类清晰**: 按重要性分级发送
- **时间标注**: 包含时间信息便于追踪

### 2. 发送策略优化
- **批量发送**: 多条消息合并发送
- **异步处理**: 非阻塞方式提高性能
- **错误重试**: 失败后自动重试
- **频率控制**: 控制发送频率避免限制

### 3. 安全性和可靠性
- **Webhook保密**: 不要硬编码在代码中
- **内容验证**: 验证发送的消息内容
- **权限控制**: 限制消息发送权限
- **日志记录**: 记录所有发送操作

---

## 📞 使用帮助

### 获取Webhook地址
1. 进入企业微信群聊
2. 点击右上角"群设置"
3. 选择"群机器人"
4. 点击"添加机器人"
5. 复制Webhook地址

### 测试消息发送
```python
# 测试所有消息类型
test_messages = [
    ("text", "测试文本消息"),
    ("markdown", "**测试Markdown消息**"),
    ("markdown_v2", "**测试Markdown V2消息**"),
    ("image", "/path/to/test-image.png"),
    ("news", create_news_article("测试标题", "测试描述", "https://example.com", "https://example.com/image.png")),
]

for msg_type, content in test_messages:
    result = send_wechat_message(content, msg_type=msg_type)
    print(f"{msg_type}消息测试结果: {result['success']}")
```

**技能使用完成！** 现在您可以使用qywx-send-skill发送各种类型的消息到企业微信了。