# 房产网站验证码绕过策略

## 贝壳找房 (ke.com)

### 验证码类型：
- 人机验证页面 (CAPTCHA)
- JavaScript 检测
- IP 限制
- Cookie 验证

### 成功绕过策略：
1. **使用移动设备UA**：
   ```
   User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1
   ```

2. **设置设备指纹**：
   ```
   agent-browser set device "iPhone 14"
   agent-browser set viewport 375 812
   ```

3. **模拟人类行为**：
   ```
   agent-browser scroll down 300
   agent-browser wait 1000
   ```

## 链家 (lianjia.com)

### 验证码类型：
- 验证码页面 (CAPTCHA)
- JavaScript 检测
- IP 限制
- Cookie 验证

### 发现的问题：
1. **直接的HTTP请求**会被拦截
2. **agent-browser**也会触发验证码
3. **验证码页面**显示在 `https://hip.lianjia.com/captcha`

### 可能的解决方案：
1. **手动完成一次验证**，保存会话状态
   ```
   agent-browser state save "lianjia_session.json"
   ```

2. **使用代理IP**轮换
3. **降低访问频率**（每次请求间隔至少5秒）
4. **设置Referer**模拟正常用户访问

## 通用验证码绕过策略

### 1. 会话管理
```bash
# 手动完成一次验证后保存会话
agent-browser open "https://www.lianjia.com"
# ... 手动完成验证码
agent-browser state save "verified_session.json"

# 后续访问使用保存的会话
agent-browser state load "verified_session.json"
agent-browser open "https://www.lianjia.com/ershoufang"
```

### 2. Cookie 管理
```bash
# 设置常见cookie
agent-browser cookies set "city" "110000"   # 北京城市代码
agent-browser cookies set "lianjia_ssid" "session_value"
agent-browser cookies set "lianjia_uuid" "uuid_value"
```

### 3. 代理IP轮换
```python
# Python脚本示例
import requests

proxy_pool = [
    "http://proxy1.example.com:8080",
    "http://proxy2.example.com:8080",
    "http://proxy3.example.com:8080",
]

for i, url in enumerate(urls_to_crawl):
    proxy = proxy_pool[i % len(proxy_pool)]
    response = requests.get(url, proxies={"http": proxy})
```

### 4. 请求频率控制
```python
import time
import random

# 随机延迟
delay = random.uniform(3, 8)
time.sleep(delay)

# 批次延迟
batch_size = 10
for i in range(batch_size):
    # 处理请求
    time.sleep(random.uniform(1, 2))
# 批次结束后大延迟
time.sleep(random.uniform(30, 60))
```

### 5. 验证码识别服务
```python
# 使用第三方验证码识别API
import requests

def solve_captcha(image_path):
    response = requests.post(
        "https://captcha.service.com/api/solve",
        files={"image": open(image_path, "rb")},
        headers={"Authorization": "Bearer YOUR_API_KEY"}
    )
    return response.json()["solution"]
```

## 针对链家的特殊策略

### 1. 使用已验证的cookie
```bash
# 先手动访问一次链家网站，完成验证码
# 获取cookie后
agent-browser cookies set "select_city" "110000"
agent-browser cookies set "lianjia_ssid" "xxxxxxx"
agent-browser cookies set "lianjia_uuid" "yyyyyyy"
agent-browser cookies set "ctid" "16"
```

### 2. 访问备用页面
```bash
# 尝试访问非列表页面
agent-browser open "https://www.lianjia.com/city/"
agent-browser wait 3000
agent-browser open "https://www.lianjia.com/about/"
agent-browser wait 2000
agent-browser open "https://www.lianjia.com/ershoufang/"
```

### 3. 页面验证码截图处理
```bash
# 截图验证码页面
agent-browser screenshot "lianjia_captcha.png"

# 暂停脚本，等待人工处理
echo "请手动完成验证码，然后继续脚本..."
agent-browser pause

# 手动完成后
agent-browser continue
```

## 实践建议

### 最佳实践：
1. **首次访问手动完成验证码**
2. **保存会话状态供后续使用**
3. **使用代理IP轮换降低风险**
4. **限制访问频率，避免高频访问**

### 备用方案：
1. **使用房产网站API**（如果有公开API）
2. **使用第三方房产数据平台**
3. **使用移动端APP接口**（通常反爬虫较弱）

### 风险评估：
1. **法律风险**：遵守网站条款
2. **技术风险**：可能被永久封禁
3. **数据质量**：验证码绕过可能影响数据完整性