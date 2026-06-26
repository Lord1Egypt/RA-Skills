# 反爬虫策略

## User-Agent 轮换

```bash
# 常用 UA 列表
UA_LIST=(
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
  "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
)

# 随机选择 UA
UA=${UA_LIST[$RANDOM % ${#UA_LIST[@]}]}
curl -s -H "User-Agent: $UA" "$URL"
```

## 请求频率控制

```bash
# 每次请求后随机等待 2-8 秒
sleep $((RANDOM % 6 + 2))

# 每 10 次请求后等待更长时间（模拟人工浏览）
if [ $((REQUEST_COUNT % 10)) -eq 0 ]; then
  sleep $((RANDOM % 30 + 10))
fi
```

## 请求头模拟

```bash
# 完整的浏览器请求头
curl -s \
  -H "User-Agent: Mozilla/5.0 ..." \
  -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
  -H "Accept-Language: zh-CN,zh;q=0.9,en;q=0.8" \
  -H "Accept-Encoding: gzip, deflate, br" \
  -H "Connection: keep-alive" \
  -H "Upgrade-Insecure-Requests: 1" \
  -H "Sec-Fetch-Dest: document" \
  -H "Sec-Fetch-Mode: navigate" \
  -H "Sec-Fetch-Site: none" \
  "$URL"
```

## 代理 IP 使用

```bash
# 使用代理（需配置代理池）
PROXY="http://proxy-host:port"
curl -s --proxy "$PROXY" "$URL"

# 轮换代理
PROXIES=("proxy1:port" "proxy2:port" "proxy3:port")
PROXY=${PROXIES[$RANDOM % ${#PROXIES[@]}]}
curl -s --proxy "http://$PROXY" "$URL"
```

## 验证码识别

常见验证码类型及处理策略：
- **图形验证码**：使用 OCR 工具（tesseract）识别简单验证码
- **滑块验证码**：需要浏览器自动化（Playwright/Selenium）
- **行为验证码（reCAPTCHA）**：使用第三方打码服务或降低请求频率避免触发

## 被封禁后的处理

```bash
# 检测是否被封禁（HTTP 状态码或内容特征）
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$URL")
if [ "$HTTP_CODE" = "403" ] || [ "$HTTP_CODE" = "429" ]; then
  echo "可能被封禁，等待后重试"
  sleep 3600  # 等待 1 小时
fi

# 检测内容是否为验证页面
if grep -q "captcha\|robot\|blocked" page.html; then
  echo "触发反爬虫，切换策略"
fi
```

## 合规提示

- 遵守目标网站的 `robots.txt` 规则
- 控制请求频率，避免对目标网站造成压力
- 敏感数据需加密存储
- 仅用于合法的商业情报收集，不用于恶意竞争
