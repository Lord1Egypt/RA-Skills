# RSS 源状态参考

## ✅ 可用源

| 源 | RSS URL | 说明 |
|---|---|---|
| 嘶吼 | `https://www.4hou.com/feed` | 每次约 8 条新增 |
| 先知社区 | `https://xz.aliyun.com/feed` | 每次约 2 条新增 |
| Seebug Paper | `https://paper.seebug.org/rss/` | 漏洞档案，有更新才推 |

## ❌ 失效源

| 源 | 原因 | 尝试过的 URL |
|---|---|---|
| FreeBuf | 阿里云 WAF 拦截所有请求 | `feed.freebuf.com/feed`, `/rss`, `/articles/feed` |
| 安全客 | RSS 已下线，仅首页可访问 | `anquanke.com/feed`, `/feed.xml` |
| T00ls | RSS 已下线 | `t00ls.com/articles.atom`, `t00ls.net/feed` |
| 安全脉搏 | 服务器无响应/超时 | `secpulse.com/feed` |
| 补天 | 返回 HTML 而非 XML | `butian.net/feed`, `/rss` |
| SecWiki | SSL 证书错误 | `secwiki.org/rss`, `/?feed=rss2` |
| 极速安全 | DNS 解析失败 | `biersec.com/feed` |

## 🔍 探测方法

当某 RSS 源失效时，可尝试以下方法找替代：

```bash
# 1. 检查 HTTP 状态码
curl -s -o /dev/null -w "%{http_code}" --max-time 8 "URL"

# 2. 检查首页 HTML 是否含 RSS link
curl -s --max-time 8 "https://官网首页" | \
  grep -i 'type="application/rss+xml"'

# 3. 常见 RSS 路径穷举
for path in /feed /rss /atom.xml /feed.xml /articles/feed; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 6 "https://网站.com$path")
  echo "$path -> $code"
done
```

## 🌐 可考虑添加的新源

- 奇安信威胁情报中心：`ti.qianxin.com`（如有 RSS）
- 国家信息安全漏洞库 CNVD：`cnvd.org.cn`（需确认 RSS）
- 知道创宇 ZoomEye：`zoomeye.org`（可能有 RSS）
- 嘶吼（已接入）、先知（已接入）、Seebug（已接入）
