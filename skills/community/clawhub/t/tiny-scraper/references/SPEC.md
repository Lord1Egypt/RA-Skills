# TinyScraper 格式标准文档

本文档汇总 TinyScraper 开发过程中确认的所有格式要求和内容标准。

---

## 1. 下载目录

```
tmp/mirrors/{domain}/
```

- 绝对路径
- 按域名分目录


---

## 2. 文件路径规范

### URL → 本地路径映射规则

| 输入 URL | 本地路径 | 说明 |
|---------|---------|------|
| `/` | `index.html` | 根目录 |
| `/about` | `about/index.html` | 无扩展名加 `/index.html` |
| `/about.html` | `about.html` | 保持原扩展名 |
| `/page?id=1` | `page/index.html` | 查询参数忽略 |
| `/page#section` | `#` 去除，与 `/page` 同文件 | 锚点去除 |
| `/style.css?v=1.2` | `style.css` | 去重后缀忽略 |

---

## 3. 资源本地化重写

### HTML 重写
- 同域 `href` / `src` → 相对路径
- 外部链接 → 保持原值不处理
- `mailto:` / `tel:` / `javascript:` → 保持原值不处理

### CSS 重写
- `url(...)` → 相对路径
- `@import "..."` → 相对路径
- `data:` URI → 保持原值不处理

### JS 重写（只下载，不重写）
- `import ... from '...'`
- `import('...')`
- `require('...')`
- `src = '...'`

---

## 4. 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `OPENCLAW_WORKSPACE` | OpenClaw 工作区根目录 | `~/.openclaw/workspace` |

`MIRRORS_DIR` 相对于 `OPENCLAW_WORKSPACE` 解析。

---

## 5. 配置文件格式

文件：`conf/.tinyscraper.conf`

```bash
# 请求延迟（秒）
DELAY=0.5

# 递归深度，-1 表示不限深度
MAX_DEPTH=-1

# HTTP 请求超时（秒）
TIMEOUT=30

# 下载目录
MIRRORS_DIR="tmp/mirrors"

# User-Agent
USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36..."
```

---

## 6. 爬虫策略

- **遍历顺序：** 广度优先（BFS）
- **去重依据：** 规范化后的 URL（去除 fragment，`?v=` 等查询参数）
- **深度控制：** MAX_DEPTH 配置，-1 不限
- **延迟控制：** 每个请求间隔 DELAY 秒

---

## 7. CLI 接口

```bash
tinyscraper "https://example.com"           # 开始镜像
tinyscraper "https://example.com" --dry-run # 预览
tinyscraper -d example.com                  # 清理镜像
tinyscraper -h                               # 帮助
```

---

## 8. 进度日志格式

```
[STEP] 🌐 开始镜像: {url}
[STEP] 📁 保存目录: {path}
[STEP] 爬取 ({depth}): {url}
[INFO] 保存页面: {url} -> {local_path}
[INFO] 保存资源: {url} -> {local_path}
[INFO] 进度: 已爬 {pages} 页面, {resources} 资源, {pending} 待爬
[INFO] ==================================================
[INFO] 镜像完成!
[INFO]   页面: {pages}
[INFO]   资源: {resources}
[INFO]   失败: {failed}
[INFO]   目录: {path}
```

---

## 9. 已知局限性

1. 不支持 SPA（React/Vue 等 JS 驱动页面）
2. 不下载外部域名资源（如 CDN 上的 JS）
3. 有 `X-Frame-Options` 的网站 iframe 无法显示
4. robots.txt 被忽略（镜像工具通用行为）
5. 不支持需要登录认证的网站
