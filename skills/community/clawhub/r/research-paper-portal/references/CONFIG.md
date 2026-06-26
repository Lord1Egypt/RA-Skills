# 配置说明

## 目录结构

```
your-site/
├── index.html              # 主页面
├── paper-index.json        # 今日论文（5篇）
├── pending-papers.json     # 待发布队列
├── version.txt             # 版本号
├── assets/
│   └── images/
│       ├── preview-{id}.webp   # 预览图 (640px, ~30KB)
│       └── full-{id}.webp      # 高清图 (1280px, ~100KB)
└── scripts/
    ├── update-papers.py    # 论文收集
    ├── generate-bg.py      # 图片生成
    └── daily-publish.py    # 每日发布
```

## 环境变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `OPENALEX_EMAIL` | OpenAlex API 邮箱 | `your@email.com` |
| `COMFYUI_URL` | ComfyUI 服务器地址 | `http://192.168.1.100:8188` |

## 配置文件

### config.json（可选）

```json
{
  "siteName": "YourResearch.Tech",
  "keywords": ["thermoelectric", "heat pipe"],
  "paperSources": {
    "openalex": true,
    "arxiv": true,
    "rss": [
      "https://rss.sciencedirect.com/..."
    ]
  },
  "llm": {
    "provider": "gemini",
    "command": "gemini -p"
  },
  "imageGeneration": {
    "comfyui_url": "http://YOUR_SERVER:8188",
    "width": 1280,
    "height": 720
  },
  "publishSchedule": {
    "updatePapers": "05:00",
    "publishSite": "08:00"
  }
}
```

## 定时任务配置

### OpenClaw Cron

```bash
# 论文更新（每日凌晨 5:00）
openclaw cron add \
  --name "论文更新" \
  --schedule "0 5 * * *" \
  --script "/path/to/update-papers.py"

# 网站发布（每日早晨 8:00）
openclaw cron add \
  --name "网站发布" \
  --schedule "0 8 * * *" \
  --script "/path/to/daily-publish.py"
```

### 系统 Crontab

```bash
# 编辑 crontab
crontab -e

# 添加任务
0 5 * * * /usr/bin/python3 /path/to/update-papers.py
0 8 * * * /usr/bin/python3 /path/to/daily-publish.py
```

### Windows 任务计划

```powershell
# 创建计划任务
$trigger = New-ScheduledTaskTrigger -Daily -At 5am
$action = New-ScheduledTaskAction -Execute "python" -Argument "C:\path\to\update-papers.py"
Register-ScheduledTask -TaskName "论文更新" -Trigger $trigger -Action $action
```

## Web 服务器配置

### Caddy（推荐）

```caddyfile
yourdomain.com {
    root * /var/www/your-site
    file_server
    encode gzip
    
    # 缓存静态资源
    @static {
        path /assets/*
    }
    header @static Cache-Control "public, max-age=31536000"
    
    # 不缓存 JSON 数据
    @data {
        path *.json
    }
    header @data Cache-Control "no-cache"
}
```

### Nginx

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    root /var/www/your-site;
    
    # 静态资源缓存
    location /assets/ {
        expires 1y;
        add_header Cache-Control "public";
    }
    
    # JSON 不缓存
    location ~ \.json$ {
        add_header Cache-Control "no-cache";
    }
}
```

## 图片优化建议

| 参数 | 建议值 | 说明 |
|------|--------|------|
| 预览图宽度 | 640px | 首屏加载 |
| 高清图宽度 | 1280px | 完整显示 |
| WebP 质量 | 85 | 平衡质量和体积 |
| 单张图片大小 | <200KB | 优化加载速度 |

## API 使用限制

| API | 限制 | 建议 |
|-----|------|------|
| OpenAlex | 免费，无限制 | 提供 email 提高限额 |
| arXiv | 每 3 秒 1 次 | 避免频繁请求 |
| CrossRef | 免费 | 用于 DOI 查询 |

## 故障排除

### 常见问题

1. **论文数据为空**
   - 检查关键词拼写
   - 确认 API 可访问
   - 检查日期范围

2. **图片生成失败**
   - 检查 ComfyUI 服务状态
   - 确认模型文件已加载
   - 检查磁盘空间

3. **中文显示乱码**
   - 确认文件 UTF-8 编码
   - 检查 Content-Type 头
   - 使用 `write` 工具写入文件

4. **定时任务未执行**
   - 检查 cron 服务状态
   - 确认脚本执行权限
   - 检查环境变量配置
