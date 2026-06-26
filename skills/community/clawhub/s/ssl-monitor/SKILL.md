---
name: ssl-monitor
description: "查询域名 SSL 证书过期时间。用法：说「查 xxx.cn 证书」或「SSL 证书 xxx.com」即可。"
metadata: { "openclaw": { "emoji": "", "requires": { "bins": ["openssl"] } } }
---

# SSL 证书查询

一句话查询域名 SSL 证书状态。

## 用法

直接说：
- 「查 baidu.com 证书」
- 「SSL 证书 example.com」
- 「xxx.cn 还有多久过期」

## 核心命令

```bash
domain="xxx.cn"
expiry=$(echo | openssl s_client -servername $domain -connect $domain:443 2>/dev/null | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
expiry_epoch=$(date -d "$expiry" +%s 2>/dev/null)
now_epoch=$(date +%s)
days_left=$(( ($expiry_epoch - $now_epoch) / 86400 ))
echo "域名：$domain"
echo "   过期时间：$expiry"
echo "   剩余天数：$days_left 天"
[ $days_left -lt 7 ] && echo "   状态：紧急" || ([ $days_left -lt 30 ] && echo "   状态：注意" || echo "   状态：正常")
```

## 响应示例

**查 baidu.com 证书**
```
域名：baidu.com
   过期时间：Dec 15 23:59:59 2026 GMT
   剩余天数：259 天
   状态：正常
```

**快过期的域名**
```
域名：expiring.com
   过期时间：Apr 5 23:59:59 2026 GMT
   剩余天数：5 天
   状态：紧急
```
