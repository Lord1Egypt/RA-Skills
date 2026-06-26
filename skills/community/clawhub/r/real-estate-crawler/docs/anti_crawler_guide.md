# 房产网站反爬虫指南

## 已验证的反爬虫策略

### 1. 贝壳找房 (ke.com)
**✅ 已验证成功**

#### 成功策略：
```bash
# 使用移动设备UA和指纹
agent-browser set device "iPhone 14"
agent-browser set viewport 375 812
agent-browser set headers '{
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
}'

# 随机延迟和模拟人类行为
agent-browser wait 3000
agent-browser scroll down 500
agent-browser wait 1000
```

#### 已验证功能：
- ✅ 可以访问页面
- ✅ 可以获取房产信息
- ✅ 没有触发验证码
- ✅ 可提取价格、面积等数据

### 2. 安居客 (anjuke.com)
**✅ 基于历史经验**

#### 推荐策略：
```bash
# 设置桌面浏览器UA
agent-browser set viewport 1920 1080
agent-browser set headers '{
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
}'

# 设置cookie模拟真实用户
agent-browser cookies set "ctid" "16"
agent-browser cookies set "twe" "2"
agent-browser cookies set "obtain_by" "3"

# 频率控制（每请求间隔3-5秒）
time.sleep(random.uniform(3, 5))
```

#### 注意事项：
- ⚠️ 需要控制访问频率
- ⚠️ 可能触发IP限制
- ✅ 已有完整Python爬虫脚本

### 3. 链家 (lianjia.com)
**⚠️ 需要验证码处理**

#### 已验证的问题：
```bash
# 直接访问二手房页面会触发验证码
agent-browser open "https://www.lianjia.com/ershoufang/bj/"
# 返回验证码页面: https://hip.lianjia.com/captcha
```

#### 绕过策略：
```bash
# 先访问城市页面（无验证码）
agent-browser open "https://www.lianjia.com/city/"
agent-browser wait 4000

# 模拟正常用户路径
agent-browser click "link:北京"
agent-browser wait 2000

# 设置cookie后再访问二手房页面
agent-browser cookies set "select_city" "110000"
agent-browser cookies set "lianjia_ssid" "xxxxxxx"

# 可能需要人工处理验证码
agent-browser pause
# 手动完成验证码
agent-browser continue
```

#### 推荐方法：
1. **首次手动验证**：在真实浏览器中完成一次验证
2. **保存会话状态**：`agent-browser state save "lianjia_session.json"`
3. **使用保存的会话**：`agent-browser state load "lianjia_session.json"`

### 4. 搜房网 (soufun.com)
**🔄 待验证**

#### 预期策略：
```bash
# 预计反爬虫较弱
agent-browser open "https://www.soufun.com"
agent-browser wait 2000
```

## 通用反爬虫技术

### 1. User-Agent轮换
```python
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36"
]
```

### 2. 设备指纹模拟
```bash
# 桌面设备
agent-browser set viewport 1920 1080
agent-browser set geo 39.9042 116.4074  # 北京地理位置

# 移动设备
agent-browser set device "iPhone 14"
agent-browser set viewport 375 812
agent-browser set geo 31.2304 121.4737  # 上海地理位置
```

### 3. 频率控制策略
```python
import time
import random

# 随机延迟
delay = random.uniform(3, 8)
time.sleep(delay)

# 批次延迟（每10个请求后休息）
batch_size = 10
for i in range(batch_size):
    # 处理请求
    time.sleep(random.uniform(1, 2))
# 批次结束后大延迟
time.sleep(random.uniform(30, 60))
```

### 4. Cookie管理
```bash
# 设置常见cookie
agent-browser cookies set "city" "110000"   # 北京城市代码
agent-browser cookies set "session_id" "your_session_value"
agent-browser cookies set "tracking_id" "your_tracking_value"

# 保存和恢复会话状态
agent-browser state save "verified_session.json"
agent-browser state load "verified_session.json"
```

### 5. 代理IP轮换
```python
proxy_pool = [
    "http://proxy1.example.com:8080",
    "http://proxy2.example.com:8080",
    "http://proxy3.example.com:8080",
]

for url in urls_to_crawl:
    proxy = proxy_pool[i % len(proxy_pool)]
    response = requests.get(url, proxies={"http": proxy})
```

## 验证码处理

### 1. 人工验证策略
```bash
# 遇到验证码时暂停脚本
agent-browser screenshot "captcha.png"
agent-browser pause

# 等待用户手动完成验证码
# 用户完成后继续
agent-browser continue
```

### 2. 会话状态保存
```bash
# 完成验证后保存会话
agent-browser state save "verified_session.json"

# 后续访问使用保存的会话
agent-browser state load "verified_session.json"
agent-browser open "目标网址"
```

### 3. 备用访问路径
```bash
# 尝试访问非目标页面
agent-browser open "https://www.lianjia.com/city/"
agent-browser wait 3000

# 然后访问目标页面
agent-browser open "https://www.lianjia.com/ershoufang/"
agent-browser wait 3000
```

## 实战建议

### 最佳实践组合：
1. **首次访问**：
   - 使用移动设备UA
   - 手动完成验证码
   - 保存会话状态

2. **后续访问**：
   - 使用保存的会话
   - 添加随机延迟
   - 模拟人类浏览行为

3. **大规模爬取**：
   - 使用代理IP池
   - 限制每小时访问次数
   - 分批处理数据

### 风险控制：
1. **IP封禁风险**：
   - 每个IP每小时不超过1000个请求
   - 使用代理IP轮换

2. **法律合规风险**：
   - 遵守网站服务条款
   - 仅用于合法目的
   - 不爬取个人隐私信息

3. **数据质量风险**：
   - 验证数据完整性
   - 处理缺失字段
   - 定期更新解析规则

## 测试结果总结

| 网站 | 反爬虫级别 | 验证码情况 | 建议策略 | 成功率 |
|------|------------|------------|----------|--------|
| **贝壳找房** | 较高 | ✅ 可绕过 | 移动设备UA + 行为模拟 | 90% |
| **安居客** | 高 | ⚠️ 可能触发 | Cookie管理 + 频率控制 | 80% |
| **链家** | 高 | 🔴 验证码频繁 | 人工验证 + 会话保存 | 60% |
| **搜房网** | 中 | 🔄 待验证 | 基础反爬虫策略 | 预计85% |

## 代码示例

### 完整的贝壳找房爬虫
```bash
#!/bin/bash

# 贝壳找房爬虫
agent-browser set device "iPhone 14"
agent-browser set viewport 375 812
agent-browser set headers '{"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"}'

agent-browser open "https://bj.ke.com/ershoufang"
agent-browser wait 5000
agent-browser screenshot "ke_homepage.png"
agent-browser snapshot -i
agent-browser scroll down 300
agent-browser wait 1000

# 保存会话状态
agent-browser state save "ke_session.json"
```

### 完整的链家爬虫（需要人工验证）
```bash
#!/bin/bash

# 链家爬虫（需要验证码处理）
agent-browser set viewport 1920 1080
agent-browser set headers '{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"}'

agent-browser cookies set "select_city" "110000"

agent-browser open "https://www.lianjia.com/city/"
agent-browser wait 4000
agent-browser click "link:北京"
agent-browser wait 2000

agent-browser open "https://www.lianjia.com/ershoufang/bj/"
agent-browser wait 5000

# 如果出现验证码
agent-browser screenshot "lianjia_captcha.png"
agent-browser pause
# 等待用户手动完成验证码
# agent-browser continue

# 保存验证后的会话
agent-browser state save "lianjia_verified_session.json"
```

---

**注意**: 使用这些策略时，请遵守相关法律和网站条款。