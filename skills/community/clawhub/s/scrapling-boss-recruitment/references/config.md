# Boss直聘爬虫配置指南

## Cookie获取

### 步骤

1. 在Chrome浏览器登录 [Boss直聘](https://www.zhipin.com)
2. 按 `F12` 打开开发者工具
3. 切换到 `Application` 标签
4. 左侧选择 `Cookies` → `https://www.zhipin.com`
5. 复制以下关键Cookie的值：

### 必需Cookie

| Cookie名称 | 说明 | 重要性 |
|-----------|------|--------|
| `__zp_stoken__` | 认证Token，核心参数 | ⭐⭐⭐ 必需 |
| `__zp_phoenix_id` | 浏览器会话ID | ⭐⭐⭐ 必需 |
| `Hm_lvt_xxx` | Session标记 | ⭐⭐ 重要 |
| `Hm_lpvt_xxx` | 最后活跃时间 | ⭐⭐ 重要 |
| `wt` | 访问令牌 | ⭐ 辅助 |
| `l` | 用户ID标记 | ⭐ 辅助 |
| `wmda_uuid` | 设备指纹 | ⭐ 辅助 |

### 注意事项

- Cookie有效期通常为 **几个小时到几天**
- 过期后需要用户重新登录获取
- 建议同时提供所有可见的Cookie以提高成功率

### Python Cookie格式

```python
COOKIES = {
    '__zp_stoken__': 'your_stoken_here',
    '__zp_phoenix_id': 'your_phoenix_id_here',
    'Hm_lvt_194a310...': 'timestamp',
    'Hm_lpvt_194a310...': 'timestamp',
    'wt': 'your_wt_here',
    'l': 'your_l_here',
    'wmda_uuid': 'your_uuid_here',
    'wmda_new_uuid': 'your_new_uuid_here',
}
```

## 请求频率配置

### 限制参数

```python
# 每日限制
DAILY_SEARCH_LIMIT = 200   # 搜索次数
DAILY_GREET_LIMIT = 500    # 打招呼次数

# 请求间隔
MIN_DELAY = 3   # 最小延迟（秒）
MAX_DELAY = 10  # 最大延迟（秒）

# 失败重试
MAX_RETRIES = 3           # 最大重试次数
RETRY_DELAY = 5           # 重试间隔（秒）
```

### 安全建议

| 建议 | 说明 |
|------|------|
| 限制日操作量 | 搜索≤200/天，打招呼≤500/天 |
| 随机延迟 | 每次请求间隔3-10秒随机 |
| 分散操作时间 | 避免集中在短时间大量请求 |
| 监控成功率 | 成功率低于80%时应降低频率 |

## 代理配置（可选）

如需使用代理：

```python
PROXY = {
    'http': 'http://username:password@proxy.com:8080',
    'https': 'http://username:password@proxy.com:8080',
}

# 使用代理
with DynamicSession(proxy=PROXY) as session:
    page = session.fetch(url)
```

## 错误处理

### 常见错误

| 错误类型 | 原因 | 处理方式 |
|---------|------|----------|
| `403 Forbidden` | Cookie无效或被禁止 | 提示用户更新Cookie |
| `429 Too Many Requests` | 请求过于频繁 | 降低频率，等待后重试 |
| `Captcha Required` | 触发验证码 | 暂停操作，提示用户 |
| `Network Error` | 网络问题 | 自动重试3次 |

### 重试装饰器

```python
from functools import wraps
import time

def retry_on_failure(max_retries=3, delay=5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    logger.warning(f"尝试 {attempt+1} 失败: {e}")
                    time.sleep(delay * (attempt + 1))
        return wrapper
    return decorator

@retry_on_failure(max_retries=3, delay=5)
def fetch_page(url):
    # 获取页面的逻辑
    pass
```

## 环境变量配置

```bash
# .env 文件
BOSSBOT_COOKIE_STOKEN=your_stoken
BOSSBOT_COOKIE_PHOENIX=your_phoenix
BOSSBOT_DAILY_SEARCH_LIMIT=200
BOSSBOT_DAILY_GREET_LIMIT=500
BOSSBOT_MIN_DELAY=3
BOSSBOT_MAX_DELAY=10
```

```python
import os
from dotenv import load_dotenv

load_dotenv()

COOKIES = {
    '__zp_stoken__': os.getenv('BOSSBOT_COOKIE_STOKEN'),
    '__zp_phoenix_id': os.getenv('BOSSBOT_COOKIE_PHOENIX'),
}
```
