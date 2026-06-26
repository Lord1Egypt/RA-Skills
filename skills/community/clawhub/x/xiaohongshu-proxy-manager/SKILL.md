---
name: xiaohongshu-proxy-manager
description: 小红书多账号IP隔离工具 - 代理池管理，支持代理切换、延迟控制、模拟真实用户行为
allowed-tools:
  - Bash(python:*)
  - Read
license: MIT
---

# 小红书代理管理器

为小红书多账号运营实现 IP 隔离，每个账号使用不同 IP，避免同 IP 多账号被封。

## 核心功能

### 1. 代理池管理
- 添加、删除、启用/禁用代理
- 代理列表查看
- 代理延迟测试

### 2. 账号-代理绑定
- 为不同账号分配不同代理
- 一对一、一对多映射

### 3. 随机代理分配
- 随机获取可用代理
- 适用于负载均衡场景

### 4. 代理配置导出
- 输出环境变量格式（HTTP_PROXY、HTTPS_PROXY）
- 输出 Python requests 格式
- 输出 curl 格式

## 小红书多账号策略

### 典型架构
```
主账号 (专业干货)  → 代理 A
素人账号 1 (真实晒家) → 代理 B
素人账号 2 (踩坑日记) → 代理 C
素人账号 3 (装修对比) → 代理 D
```

### 为什么需要 IP 隔离？
1. **防封号**：小红书限制同 IP 多账号，隔离降低风险
2. **模拟真实用户**：不同 IP 来自不同地区，行为更自然
3. **提高曝光**：账号分布在不同 IP，避免平台判定为"刷量"

## 使用方法

### 添加代理
```bash
# HTTP 代理
xiaohongshu-proxy-manager --add "1.1.1.1:8080" \
  --name "代理A" \
  --protocol http

# 带认证的代理
xiaohongshu-proxy-manager --add "2.2.2.2:3128" \
  --name "代理B" \
  --protocol http \
  --username user123 \
  --password pass456

# SOCKS5 代理
xiaohongshu-proxy-manager --add "3.3.3.3:1080" \
  --name "代理C" \
  --protocol socks5
```

### 绑定账号和代理
```bash
# 为主账号绑定代理 A
xiaohongshu-proxy-manager --map main_account proxyA

# 为素人账号绑定代理
xiaohongshu-proxy-manager --map normal_account1 proxyB
xiaohongshu-proxy-manager --map normal_account2 proxyC
xiaohongshu-proxy-manager --map normal_account3 proxyD
```

### 获取账号的代理配置
```bash
xiaohongshu-proxy-manager --account main_account
```

输出：
```
📦 账号 main_account 的代理配置：
   HTTP_PROXY=http://1.1.1.1:8080
   HTTPS_PROXY=http://1.1.1.1:8080

💻 Python requests 用法：
   proxies = {'http': 'http://1.1.1.1:8080', 'https': 'http://1.1.1.1:8080'}
   response = requests.get(url, proxies=proxies)

🐘 curl 用法：
   curl -x 'http://1.1.1.1:8080' https://example.com
```

### 列出所有代理
```bash
xiaohongshu-proxy-manager --list
```

### 测试代理
```bash
# 测试单个代理
xiaohongshu-proxy-manager --test proxyA

# 测试所有代理
xiaohongshu-proxy-manager --test-all
```

### 随机获取可用代理
```bash
xiaohongshu-proxy-manager --random
```

### 启用/禁用代理
```bash
xiaohongshu-proxy-manager --enable proxyA
xiaohongshu-proxy-manager --disable proxyB
```

### 删除代理
```bash
xiaohongshu-proxy-manager --remove proxyA
```

## 配置文件

### 位置
```
~/.openclaw/workspace/skills/xiaohongshu-proxy-manager/config/proxies.json
```

### 结构示例
```json
{
  "proxies": [
    {
      "id": "proxyA",
      "name": "代理A",
      "protocol": "http",
      "host": "1.1.1.1",
      "port": 8080,
      "username": "",
      "password": "",
      "enabled": true
    },
    {
      "id": "proxyB",
      "name": "代理B",
      "protocol": "http",
      "host": "2.2.2.2",
      "port": 3128,
      "username": "user123",
      "password": "pass456",
      "enabled": true
    }
  ],
  "account_mapping": {
    "main_account": "proxyA",
    "normal_account1": "proxyB",
    "normal_account2": "proxyC"
  },
  "test_timeout": 10,
  "test_url": "https://www.baidu.com"
}
```

## 实战场景

### 场景 1：小红书多账号发布
```bash
# 1. 配置代理池
xiaohongshu-proxy-manager --add "1.1.1.1:8080" --name "代理A"
xiaohongshu-proxy-manager --add "2.2.2.2:8080" --name "代理B"

# 2. 绑定账号
xiaohongshu-proxy-manager --map xiaohongshu_main proxyA
xiaohongshu-proxy-manager --map xiaohongshu_normal1 proxyB

# 3. 发布时切换代理
# Python 示例：
proxies = {
    'http': 'http://1.1.1.1:8080',
    'https': 'http://1.1.1.1:8080'
}
response = requests.post(api_url, json=data, proxies=proxies)
```

### 场景 2：负载均衡（随机代理）
```bash
# 获取随机代理用于自动化脚本
PROXY=$(xiaohongshu-proxy-manager --random | grep HTTPS_PROXY | cut -d= -f2)

# 在 curl 中使用
curl -x "$PROXY" https://api.xiaohongshu.com/publish
```

### 场景 3：代理健康检查
```bash
# 定期测试所有代理
xiaohongshu-proxy-manager --test-all

# 根据结果自动切换到最快代理
```

## 代理购买建议

### 免费代理
- ❌ 不稳定，经常失效
- ❌ 速度慢，影响用户体验
- ❌ 安全性差，可能窃取数据
- **结论**：仅测试使用，生产环境不建议

### 付费代理（推荐）
- ✅ 稳定可靠，自动切换
- ✅ 速度快，支持高并发
- ✅ 安全性高，加密传输
- ✅ 提供不同地区 IP

### 推荐服务商
- **Luminati**：全球最大代理网络，质量高
- **Oxylabs**：企业级代理，支持不同地区
- **Smartproxy**：性价比高，适合中小规模
- **芝麻代理**：国内代理，适合国内平台

### 配置建议
- 小红书：使用国内 IP 代理（或靠近中国地区）
- 主账号：使用高质量独享代理
- 素人账号：可以使用共享代理（成本低）

## Python 集成示例

```python
import requests
import subprocess
import json

def get_proxy_for_account(account_id):
    """获取账号代理配置"""
    result = subprocess.run(
        ['xiaohongshu-proxy-manager', '--account', account_id],
        capture_output=True,
        text=True
    )

    # 解析输出
    for line in result.stdout.split('\n'):
        if line.startswith('   HTTPS_PROXY='):
            proxy_url = line.split('=', 1)[1]
            return {
                'http': proxy_url,
                'https': proxy_url
            }

    return None

def post_with_proxy(account_id, url, data):
    """使用代理发送请求"""
    proxies = get_proxy_for_account(account_id)

    if proxies:
        print(f"使用代理：{proxies['https']}")
    else:
        print("未找到代理，直接连接")
        proxies = None

    response = requests.post(url, json=data, proxies=proxies)
    return response

# 使用示例
response = post_with_proxy(
    'main_account',
    'https://api.xiaohongshu.com/publish',
    {'title': '装修干货', 'content': '...'}
)
```

## 定时任务（Cron）

### 定期测试代理
```bash
# 每 5 分钟测试一次代理
*/5 * * * * xiaohongshu-proxy-manager --test-all >> /var/log/proxy_test.log 2>&1
```

### 监控代理可用性
```bash
# 每小时检查一次，失败时发送告警
0 * * * * xiaohongshu-proxy-manager --test-all | grep "失败" && send_alert.sh
```

## 故障排查

### 问题：代理测试失败
**原因**：
- 代理服务器宕机
- 代理认证失败
- 网络不通

**解决**：
```bash
# 1. 测试单个代理
xiaohongshu-proxy-manager --test proxyA

# 2. 检查代理配置
cat ~/.openclaw/workspace/skills/xiaohongshu-proxy-manager/config/proxies.json

# 3. 禁用失效代理
xiaohongshu-proxy-manager --disable proxyA
```

### 问题：账号被封
**原因**：
- 同 IP 多账号
- 发布频率过高
- 内容违规

**解决**：
1. 使用代理隔离 IP
2. 控制发布频率（建议：账号间隔 10-30 分钟）
3. 检查内容合规性

## 安全建议
1. **凭证安全**：代理用户名密码不要提交到代码仓库
2. **环境变量**：敏感信息使用环境变量管理
3. **定期更换**：代理定期更换，降低风险
4. **监控日志**：记录代理使用情况，异常及时处理

## License
MIT
