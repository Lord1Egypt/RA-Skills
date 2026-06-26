# OpenClaw 中使用微信自动发送消息技能

## 技能集成

### 1. 技能位置
```
~/.openclaw/workspace/skills/wechat-auto-send/
```

### 2. 技能调用方式
当用户发送以下类型的消息时，OpenClaw 应该使用此技能：

```
用户: 给张三发微信说"晚上7点开会"
OpenClaw: 好的，我将通过微信给张三发送消息："晚上7点开会"

用户: 给文件传输助手发送测试消息
OpenClaw: 正在给文件传输助手发送测试消息...

用户: 告诉李四资料已准备好
OpenClaw: 正在通过微信通知李四资料已准备好
```

### 3. 执行流程
1. **解析指令**：提取联系人和消息内容
2. **检查准备**：确认微信已打开，依赖已安装
3. **执行脚本**：调用 `wechat-send.py` 脚本
4. **返回结果**：向用户报告发送结果

## 示例对话

### 示例1：简单发送
```
用户: 给文件传输助手发微信说"这是一条测试消息"
OpenClaw: 好的，我将给文件传输助手发送微信消息："这是一条测试消息"
       正在执行发送脚本...
       [脚本输出：倒计时5秒...开始执行...消息发送完成！]
       消息已成功发送！
```

### 示例2：工作通知
```
用户: 给项目经理发消息说"周报已提交，请查收"
OpenClaw: 正在给项目经理发送微信消息："周报已提交，请查收"
       请确保微信已打开并可见...
       消息发送成功！
```

### 示例3：错误处理
```
用户: 给不存在的联系人发消息说"测试"
OpenClaw: 正在尝试发送消息...
       [脚本输出：错误：未找到微信窗口]
       发送失败：请先打开微信并确保窗口可见。
```

## 技能配置

### 1. 依赖检查
在执行技能前，OpenClaw 应该检查：
```python
# 伪代码示例
def check_wechat_skill_dependencies():
    try:
        import pyautogui
        import pygetwindow
        import pyperclip
        return True
    except ImportError:
        return False
```

### 2. 微信状态检查
```python
def check_wechat_running():
    try:
        import pygetwindow
        windows = pygetwindow.getWindowsWithTitle('微信')
        return len(windows) > 0
    except:
        return False
```

### 3. 指令解析
```python
def parse_wechat_command(user_message):
    """
    解析用户指令，提取联系人和消息
    
    示例：
    输入: "给张三发微信说晚上7点开会"
    输出: ("张三", "晚上7点开会")
    
    输入: "告诉李四资料已准备好"
    输出: ("李四", "资料已准备好")
    """
    # 解析逻辑...
    pass
```

## 高级功能

### 1. 定时发送
可以结合 OpenClaw 的 cron 功能实现定时发送：
```python
# 创建定时任务，每天9点发送日报
cron_job = {
    "name": "微信日报发送",
    "schedule": {"kind": "cron", "expr": "0 9 * * *", "tz": "Asia/Shanghai"},
    "payload": {
        "kind": "agentTurn",
        "message": "给领导发微信说'早安！今日工作计划已准备好。'"
    },
    "sessionTarget": "isolated"
}
```

### 2. 批量发送
```python
# 批量发送给多个联系人
contacts = ["张三", "李四", "王五"]
message = "本周五下午团队建设，请准时参加"

for contact in contacts:
    # 调用微信发送技能
    send_wechat_message(contact, message)
```

### 3. 消息模板
```python
# 预定义消息模板
templates = {
    "meeting_reminder": "提醒：{time}在{location}开会，请准时参加。",
    "task_complete": "{task}已完成，请查收。",
    "urgent": "【紧急】{content}，请立即处理！"
}

# 使用模板
template = templates["meeting_reminder"]
message = template.format(time="下午3点", location="201会议室")
send_wechat_message("团队成员", message)
```

## 安全注意事项

### 1. 用户确认
对于重要消息，应该要求用户确认：
```
用户: 给客户发微信说"价格可以再优惠10%"
OpenClaw: 这是一条重要消息，请确认是否发送：
         联系人：客户
         消息："价格可以再优惠10%"
         确认发送？(是/否)
```

### 2. 敏感信息过滤
避免发送包含密码、密钥等敏感信息。

### 3. 发送频率限制
避免短时间内发送大量消息，防止被微信限制。

## 故障排除

### 常见问题
1. **微信未打开**：提示用户先打开微信
2. **依赖未安装**：提供安装命令
3. **发送失败**：建议调大等待时间或检查联系人名称
4. **权限问题**：确保有控制鼠标键盘的权限

### 调试模式
可以添加 `--verbose` 参数查看详细执行过程：
```bash
python wechat-send.py "联系人" "消息" --verbose
```

## 技能改进建议

### 短期改进
1. 添加发送结果验证
2. 支持发送图片/文件链接
3. 添加发送历史记录

### 长期改进
1. 支持微信多开
2. 支持企业微信
3. 集成消息模板库
4. 添加消息队列和重试机制