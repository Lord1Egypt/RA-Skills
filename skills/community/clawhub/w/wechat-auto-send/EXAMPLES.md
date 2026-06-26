# 使用示例

## 基本示例

### 示例1：发送测试消息
```bash
python wechat-send.py "文件传输助手" "这是一条自动发送的测试消息"
```

### 示例2：发送工作消息
```bash
python wechat-send.py "项目经理" "周报已提交，请查收"
```

### 示例3：发送提醒消息
```bash
python wechat-send.py "团队成员" "下午3点会议室开会，请准时参加"
```

## 高级示例

### 示例4：长消息发送
```bash
python wechat-send.py "客户" "尊敬的客户，您好！您的问题我们已经收到，技术团队正在处理中，预计今天下午给您回复。感谢您的耐心等待！" --wait 2
```

### 示例5：紧急消息（快速发送）
```bash
python wechat-send.py "紧急联系人" "服务器宕机，请立即处理！" --wait 1 --countdown 2
```

### 示例6：调试模式
```bash
python wechat-send.py "测试账号" "调试消息" --verbose --wait 2 --countdown 3
```

## 实际应用场景

### 场景1：每日报告自动发送
```bash
# 每天早上9点发送日报
python wechat-send.py "领导" "早安！昨日工作已完成，今日计划如下：1.完成项目A测试 2.参加部门会议 3.编写技术文档"
```

### 场景2：会议提醒
```bash
# 会议前15分钟提醒
python wechat-send.py "全体成员" "提醒：15分钟后在201会议室开会，请带好相关资料"
```

### 场景3：系统状态通知
```bash
# 系统监控报警
python wechat-send.py "运维人员" "【系统报警】数据库连接数超过阈值，当前连接数：85/100"
```

### 场景4：批量消息（配合脚本）
```bash
# 批量发送消息脚本
#!/bin/bash
contacts=("张三" "李四" "王五")
message="本周五下午团队建设活动，请准时参加"

for contact in "${contacts[@]}"; do
    python wechat-send.py "$contact" "$message" --wait 2 --countdown 1
    echo "已发送给: $contact"
    sleep 3  # 避免发送过快
done
```

## 集成示例

### 集成到任务计划（Windows）
1. 创建批处理文件 `send-reminder.bat`:
```batch
@echo off
cd /d "C:\path\to\skill"
python wechat-send.py "团队成员" "每日站会10点开始"
```

2. 使用 Windows 任务计划程序设置每天9:55自动执行。

### 集成到 Python 项目
```python
import subprocess
import datetime

def send_wechat_reminder(contact, message):
    """发送微信提醒"""
    try:
        result = subprocess.run(
            ['python', 'wechat-send.py', contact, message, '--wait', '1.5'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"[{datetime.datetime.now()}] 消息发送成功: {contact}")
            return True
        else:
            print(f"[{datetime.datetime.now()}] 消息发送失败: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"[{datetime.datetime.now()}] 发送超时: {contact}")
        return False

# 使用示例
send_wechat_reminder("值班人员", "系统巡检时间到了")
```

## 故障排除示例

### 问题：消息发送到搜索框
**现象**：消息被粘贴到了搜索框而不是聊天输入框。

**解决方案**：
```bash
# 增加等待时间，确保正确进入聊天界面
python wechat-send.py "联系人" "消息" --wait 2.5
```

### 问题：联系人搜索不到
**现象**：脚本提示找不到联系人。

**解决方案**：
1. 确认联系人名称完全正确
2. 检查微信中该联系人的备注名
3. 如果名称包含特殊字符，用引号包裹：
```bash
python wechat-send.py "张三(技术部)" "消息内容"
```

### 问题：脚本执行太快
**现象**：操作太快导致微信反应不过来。

**解决方案**：
```bash
# 增加所有操作的等待时间
python wechat-send.py "联系人" "消息" --wait 3
```

## 最佳实践

1. **测试环境**：先在"文件传输助手"上测试脚本
2. **逐步调试**：使用 `--verbose` 参数查看详细执行过程
3. **适当等待**：根据网络和电脑性能调整 `--wait` 参数
4. **备份联系人**：重要联系人先测试确认名称正确
5. **安全第一**：不要用于发送敏感信息