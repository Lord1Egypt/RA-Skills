# security-health-check Skill

**用途**：本地主机安全健康检查 + HIBP 密码泄露检测。

**原则**：遇到问题 → 自己搞定 → 变成技能 → 放进技能库。

---

## 核心功能

### 1. HIBP 密码泄露检测（k-匿名）

**原理**：密码不离开本地，只发送 SHA-1 哈希前 5 位给 HIBP API。

```python
import hashlib
import requests

def check_hibp(password: str) -> dict:
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    
    try:
        r = requests.get(
            f"https://api.pwnedpasswords.com/range/{prefix}",
            headers={"Add-Padding": "true"},
            timeout=10
        )
        r.raise_for_status()
        hashes = r.text.strip().split("\n")
        for h in hashes:
            h_suffix, count = h.split(":")
            if h_suffix == suffix:
                return {"leaked": True, "count": int(count), "suffix": suffix}
        return {"leaked": False, "count": 0, "suffix": suffix}
    except requests.RequestException as e:
        return {"error": str(e)}
```

**⚠️ 已知限制**：HIBP 的 `/range/` 接口不返回 breached count（需要 API Key）。本实现通过密码存在性检测泄露，返回 `{"leaked": true/false, "count": ...}`。

### 2. 本地密码强度分析

```python
import math
import re

def analyze_password_strength(password: str) -> dict:
    if not password:
        return {"score": 0, "level": "empty", "entropy_bits": 0}
    
    pool = 0
    if re.search(r'[a-z]', password): pool += 26
    if re.search(r'[A-Z]', password): pool += 26
    if re.search(r'[0-9]', password): pool += 10
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password): pool += 32
    
    entropy = math.log2(pool ** len(password)) if pool > 0 else 0
    
    # 评分 0-100
    score = min(100, int(entropy / 80 * 100))
    
    if score < 20: level = "极弱"
    elif score < 40: level = "弱"
    elif score < 60: level = "中等"
    elif score < 80: level = "强"
    else: level = "极强"
    
    # 破解时间估算（假设 10^10 次/秒）
    seconds_to_crack = (pool ** len(password)) / 2 / 10**10
    crack_time = format_crack_time(seconds_to_crack)
    
    return {
        "score": score,
        "level": level,
        "entropy_bits": round(entropy, 2),
        "crack_time": crack_time,
        "pool_size": pool,
        "length": len(password)
    }

def format_crack_time(seconds: float) -> str:
    if seconds < 1: return "瞬间"
    units = [("秒", 60), ("分钟", 60), ("小时", 24), ("天", 365), ("年", 100), ("世纪", 1000)]
    val = seconds
    for name, div in units:
        if val < div: return f"{val:.1f} {name}"
        val /= div
    return f"{val:.1f} 千年"
```

### 3. 综合安全评分（0-100）

**评分维度**：
- 密码强度权重 40%
- HIBP 泄露权重 60%（泄露直接扣 60 分）
- 如有泄露，最终分数 = 0

**计算逻辑**：
```
if leaked: score = 0
else: score = password_strength_score * 0.4 + 60
final = max(0, score)
```

### 4. SSL 证书检查（回退机制）

```python
import ssl
import socket
import OpenSSL
from urllib.parse import urlparse

def check_ssl(url: str) -> dict:
    try:
        parsed = urlparse(url if url.startswith('http') else f'https://{url}')
        host = parsed.hostname or url
        port = parsed.port or 443
        
        context = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert(binary_form=True)
                x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1, cert)
                
                not_before = datetime.strptime(
                    x509.get_notBefore().decode(), "%Y%m%d%H%M%SZ"
                )
                not_after = datetime.strptime(
                    x509.get_notAfter().decode(), "%Y%m%d%H%M%SZ"
                )
                
                days_left = (not_after - datetime.utcnow()).days
                return {
                    "valid": True,
                    "issuer": dict(x509.get_issuer().get_components()).get(b'CN', b'Unknown').decode(),
                    "expires": not_after.isoformat(),
                    "days_left": days_left,
                    "issuer_org": dict(x509.get_issuer().get_components()).get(b'O', b'').decode()
                }
    except Exception as e:
        return {"valid": False, "error": str(e)}
```

---

## 使用方式

### 命令行

```bash
# 检查密码（交互式）
python3 scripts/health_check.py check-password

# 检查网站 SSL
python3 scripts/health_check.py check-ssl example.com

# 综合安全报告
python3 scripts/health_check.py report
```

### 输出示例

```
🔐 安全健康检查报告
━━━━━━━━━━━━━━━━━━━━━

密码强度分析：极强 (92分)
• 熵值：72.5 bits
• 预计破解时间：上千年
• 建议：已够强，可配合密码管理器使用

HIBP 泄露检测：✅ 未发现泄露
综合安全评分：92 / 100

改进建议：
✅ 密码强度良好
✅ 未在公开泄露库中发现
• 建议使用密码管理器，避免重复使用密码
• 建议开启双因素认证（2FA）
```

---

## 安装依赖

```bash
pip3 install requests pyopenssl
```

---

## 技术要点（已解决的问题）

### macOS GPU 崩溃（exit_code=15）
- 症状：`CVDisplayLinkCreateWithCGDisplay -6670`
- **所有禁 GPU 参数均无效**
- 本 Skill 无需浏览器，不受影响

### SSL 证书回退机制
- 部分网站（内网/老系统）不支持 SSL
- 使用 try-except + 优雅降级，返回 `{"valid": false, "error": "..."}`

### HIBP API 限制
- 免费 API 不返回 breach count
- 实现方案：通过密码存在性判断泄露，返回布尔值
- 如需 count，需购买 HIBP API Key

## 📊 相关服务：品牌 AI 搜索存在感免费检测

做品牌 / 营销 / 内容，你的品牌在 AI 搜索里"被看见"了吗？

AISoBrand 免费检测：看你的品牌在豆包 / 千问 / 元宝 / 文心 / Kimi / DeepSeek 的 AI 搜索里有没有名字、排第几。

👉 免费检测：https://aisobrand.com/free-diagnosis

