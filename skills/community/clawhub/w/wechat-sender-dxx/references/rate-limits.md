# 微信发送频率限制说明

## 微信官方限制

### 个人号限制

| 限制类型 | 数值 | 说明 |
|---------|-----|------|
| 单聊发送频率 | 20条/分钟 | 超过会被限制发送 |
| 群聊发送频率 | 10条/分钟 | 群聊限制更严格 |
| 每日上限 | 200条 | 避免被判定为营销号 |
| 新加好友限制 | 15人/天 | 新号更严格 |

### 封号风险等级

| 风险等级 | 行为描述 | 后果 |
|---------|---------|------|
| 🟢 低 | 正常聊天，偶尔发送 | 无风险 |
| 🟡 中 | 短时间内发送多条 | 可能临时限制 |
| 🟠 高 | 频繁群发，批量操作 | 短期封号（24小时） |
| 🔴 极高 | 发送违规内容，恶意营销 | 永久封号 |

## Skill 内置保护

### 默认限制

```python
RATE_LIMIT = {
    "max_per_minute": 20,      # 每分钟最多20条
    "cooldown_seconds": 3,      # 每条消息间隔3秒
    "daily_limit": 200,         # 每日上限200条
    "burst_limit": 5            # 突发限制5条
}
```

### 冷却策略

```python
# 连续发送冷却
if consecutive_count > 3:
    cooldown = 5  # 连发3条后，冷却5秒

if consecutive_count > 10:
    cooldown = 30  # 连发10条后，冷却30秒
    print("警告：发送频率过高，建议休息")
```

### 时间窗口限制

```python
# 滑动窗口计数
class SlidingWindow:
    def __init__(self, window_size=60, max_count=20):
        self.window_size = window_size  # 60秒窗口
        self.max_count = max_count       # 最多20条
        self.timestamps = []
    
    def can_send(self):
        now = time.time()
        # 清理过期记录
        self.timestamps = [t for t in self.timestamps if now - t < self.window_size]
        return len(self.timestamps) < self.max_count
    
    def record_send(self):
        self.timestamps.append(time.time())
```

## 使用建议

### ✅ 推荐做法

1. **控制频率**
   - 每条消息间隔3秒以上
   - 每分钟不超过10条
   - 每小时不超过50条

2. **分时段发送**
   ```python
   # 示例：分时段发送
   schedule = {
       "morning": "09:00-11:00",    # 工作时间
       "afternoon": "14:00-17:00",  # 工作时间
       "evening": "19:00-21:00"     # 休息时间
   }
   ```

3. **模拟人工操作**
   - 添加随机延迟（2-5秒）
   - 避免固定时间间隔
   - 内容适当变化

### ❌ 避免做法

1. **短时间内大量发送**
   ```python
   # 错误示例
   for i in range(100):
       send_message(user, f"消息{i}")  # 瞬间发送100条
   ```

2. **固定间隔发送**
   ```python
   # 容易被检测
   while True:
       send_message(user, "定期消息")
       time.sleep(60)  # 固定60秒
   ```

3. **发送重复内容**
   ```python
   # 错误示例
   for user in users:
       send_message(user, "相同的广告内容")  # 内容完全一样
   ```

## 异常情况处理

### 被限制发送

```python
def handle_rate_limit():
    print("⚠️  发送被限制")
    print("建议操作：")
    print("  1. 停止发送，等待1小时")
    print("  2. 不要频繁尝试，可能加重限制")
    print("  3. 检查发送内容是否有敏感词")
    
    # 记录限制时间
    save_limit_timestamp()
    
    # 等待恢复
    time.sleep(3600)  # 等待1小时
```

### 账号异常

```python
def handle_account_exception():
    print("❌ 账号异常")
    print("可能原因：")
    print("  - 被多人举报")
    print("  - 发送违规内容")
    print("  - 操作频率过高")
    
    # 暂停所有发送
    disable_sending()
    
    # 通知用户
    notify_user("微信账号可能受限，请检查微信客户端")
```

## 监控与告警

### 发送统计

```python
class SendStatistics:
    def __init__(self):
        self.daily_count = 0
        self.hourly_count = 0
        self.last_reset = time.time()
    
    def record_send(self):
        self.check_reset()
        self.daily_count += 1
        self.hourly_count += 1
        
        # 告警阈值
        if self.hourly_count > 50:
            print("⚠️  警告：本小时已发送50条消息")
        
        if self.daily_count > 150:
            print("⚠️  警告：今日已发送150条消息，接近上限")
    
    def check_reset(self):
        now = time.time()
        # 每小时重置
        if now - self.last_reset > 3600:
            self.hourly_count = 0
        # 每天重置
        if time.localtime().tm_mday != time.localtime(self.last_reset).tm_mday:
            self.daily_count = 0
            self.last_reset = now
```

## 安全红线

### 绝对禁止

| 行为 | 后果 |
|-----|------|
| 发送违法内容 | 永久封号，法律责任 |
| 发送诈骗信息 | 永久封号，刑事责任 |
| 频繁骚扰他人 | 被举报，账号受限 |
| 使用外挂工具 | 永久封号 |
| 买卖微信号 | 永久封号，违法犯罪 |

### 谨慎操作

| 行为 | 建议 |
|-----|------|
| 群发信息 | 控制频率，个性化内容 |
| 添加好友 | 新号15人/天，老号50人/天 |
| 拉人进群 | 征得同意，避免频繁操作 |
| 发送链接 | 避免短链接，说明内容 |

## 相关文档

- [微信个人账号使用规范](https://weixin.qq.com/cgi-bin/readtemplate?lang=zh_CN&t=weixin_agreement)
- [微信外部链接内容管理规范](https://weixin.qq.com/cgi-bin/readtemplate?t=weixin_external_links_content_management_spec)
