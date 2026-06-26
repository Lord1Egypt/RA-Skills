# 📘 微信公众号自动发布工具 - 用户使用手册

**版本**：v1.0.0
**作者**: 豌豆侠 - 基于openclaw的agent
**公司**: 豌豆信息（www.wandoutech.com）  
**最后更新**：2026-03-10  
**适用对象**：公众号运营者、内容创作者

---

## 📑 目录

1. [产品简介](#1-产品简介)
2. [快速开始](#2-快速开始)
3. [配置指南](#3-配置指南)
4. [使用教程](#4-使用教程)
5. [高级功能](#5-高级功能)
6. [常见问题](#6-常见问题)
7. [最佳实践](#7-最佳实践)

---

## 1. 产品简介

### 1.1 产品功能

微信公众号自动发布工具是一款帮助公众号运营者自动化发布内容的工具。

**核心功能**：
- ✅ 自动发布文章到微信公众号
- ✅ Markdown 格式转 HTML 渲染
- ✅ 智能配图生成
- ✅ 定时任务支持
- ✅ 多图片源选择

### 1.2 适用场景

- **公众号日常运营**：自动发布文章
- **内容批量处理**：批量发布多篇文章
- **定时发布**：按计划自动发布
- **多账号管理**：支持多个公众号

### 1.3 技术优势

- **安全可靠**：日志脱敏、权限保护
- **灵活配置**：支持多个 AI 绘图服务
- **成本优化**：免费额度优先使用
- **易于维护**：统一配置管理

---

## 2. 快速开始

### 2.1 环境要求

- Python 3.8+
- macOS / Linux
- 微信公众号（已认证）

### 2.2 安装步骤

**步骤 1：进入目录**
```bash
cd /Users/brucesong/.openclaw/workspace/skills/wechat-mp-publish
```

**步骤 2：安装依赖**
```bash
venv/bin/pip install -r requirements.txt
```

**步骤 3：验证安装**
```bash
venv/bin/python -c "from publish import WechatPublisher; print('✅ 安装成功')"
```

### 2.3 基础配置

**编辑配置文件**：
```bash
vim config.yaml
```

**最小配置**：
```yaml
wechat:
  appid: "你的公众号 AppID"
  appsecret: "你的公众号 AppSecret"
  name: "你的公众号名称"

image:
  providers:
    placeholder:
      enabled: true  # 使用占位图（无需 API Key）
```

### 2.4 发布第一篇文章

**创建文章文件** `article.md`：
```markdown
# 我的第一篇文章

这是文章内容...
```

**发布命令**：
```bash
venv/bin/python publish_article.py article.md
```

**查看结果**：
1. 登录微信公众号后台
2. 内容与互动 → 草稿箱
3. 找到文章

---

## 3. 配置指南

### 3.1 微信公众号配置

**获取 AppID 和 AppSecret**：
1. 登录 [微信公众平台](https://mp.weixin.qq.com/)
2. 开发 → 基本配置
3. 复制 AppID 和 AppSecret

**配置示例**：
```yaml
wechat:
  appid: "your-wechat-appid"
  appsecret: "your-wechat-appsecret"
  name: "你的公众号名称"
```

### 3.2 图片源配置

#### 方案 A：使用占位图（免费）

```yaml
image:
  providers:
    placeholder:
      enabled: true
```

**优点**：无需 API Key，完全免费  
**缺点**：图片简单（渐变色）

#### 方案 B：使用 Unsplash（推荐）

**获取 Access Key**：
1. 访问 https://unsplash.com/developers
2. 注册并创建应用
3. 复制 Access Key

**配置**：
```yaml
image:
  provider_priority:
    - "unsplash"
  
  providers:
    unsplash:
      enabled: true
      access_key: "你的 Access Key"
```

**优点**：真实照片，质量高，免费  
**缺点**：需要国际网络

#### 方案 C：使用通义万相（国内推荐）

**获取 API Key**：
1. 访问 https://dashscope.console.aliyun.com/
2. 开通 DashScope 服务
3. 创建 API Key

**配置**：
```yaml
image:
  provider_priority:
    - "tongyi-wanxiang"
  
  providers:
    tongyi-wanxiang:
      enabled: true
      api_key: "sk-你的 API Key"
      monthly_limit: 100  # 每月免费 100 张
```

**优点**：国内访问快，支持中文  
**缺点**：有免费额度限制

### 3.3 环境变量配置（可选）

**使用环境变量**：
```yaml
wechat:
  appid: "${WECHAT_APPID}"
  appsecret: "${WECHAT_APPSECRET}"

image:
  providers:
    unsplash:
      access_key: "${UNSPLASH_ACCESS_KEY}"
```

**设置环境变量**：
```bash
export WECHAT_APPID="your-wechat-appid"
export WECHAT_APPSECRET="your-wechat-appsecret"
export UNSPLASH_ACCESS_KEY="your-unsplash-access-key"
```

### 3.4 IP 白名单配置

**步骤**：
1. 查询服务器 IP：
   ```bash
   curl https://api.ipify.org
   ```

2. 登录微信公众号后台

3. 开发 → 基本配置 → IP 白名单

4. 添加 IP 地址

5. 保存（等待 5-10 分钟生效）

---

## 4. 使用教程

### 4.1 发布单篇文章

**方法 1：使用 Python 脚本**

创建 `publish_article.py`：
```python
#!/usr/bin/env python3
from publish import WechatPublisher
import sys

if len(sys.argv) < 2:
    print("用法：python publish_article.py <文章文件.md>")
    sys.exit(1)

publisher = WechatPublisher()

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    content = f.read()

article = publisher.create_article(
    title='文章标题',
    content=content,
    template='business',
    author='作者名',
    multi_images=True
)

media_id = publisher.publish_to_draft([article])
print(f'✅ 发布成功！草稿 ID: {media_id}')
```

**运行**：
```bash
venv/bin/python publish_article.py article.md
```

**方法 2：使用命令行**

```bash
venv/bin/python -c "
from publish import WechatPublisher

publisher = WechatPublisher()

with open('article.md', 'r', encoding='utf-8') as f:
    content = f.read()

article = publisher.create_article(
    title='文章标题',
    content=content,
    template='business',
    author='作者名'
)

media_id = publisher.publish_to_draft([article])
print(f'发布成功：{media_id}')
"
```

### 4.2 发布多篇文章

**批量发布脚本** `batch_publish.py`：
```python
#!/usr/bin/env python3
from publish import WechatPublisher
from pathlib import Path

publisher = WechatPublisher()

# 获取所有文章
articles_dir = Path('articles')
article_files = sorted(articles_dir.glob('*.md'))

print(f'找到 {len(article_files)} 篇文章')

for article_file in article_files:
    print(f'\n发布：{article_file.name}')
    
    with open(article_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    article = publisher.create_article(
        title=article_file.stem,
        content=content,
        template='business',
        multi_images=True
    )
    
    media_id = publisher.publish_to_draft([article])
    print(f'✅ 发布成功：{media_id[:30]}...')

print('\n🎉 全部发布完成！')
```

**运行**：
```bash
venv/bin/python batch_publish.py
```

### 4.3 定时发布

**创建定时任务**（macOS）：
```bash
# 编辑 launchd 配置文件
vim ~/Library/LaunchAgents/com.wechat.publish.plist
```

**配置示例**：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.wechat.publish</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/brucesong/.openclaw/workspace/skills/wechat-mp-publish/venv/bin/python</string>
        <string>/Users/brucesong/.openclaw/workspace/skills/wechat-mp-publish/scheduled_publish.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
</dict>
</plist>
```

**加载任务**：
```bash
launchctl load ~/Library/LaunchAgents/com.wechat.publish.plist
```

---

## 5. 高级功能

### 5.1 自定义模板

**创建模板文件** `templates/custom.html`：
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{title}}</title>
</head>
<body style="font-family: Arial; line-height: 1.8;">
    <h1 style="color: #333;">{{title}}</h1>
    <p style="color: #666;">作者：{{author}}</p>
    <div>{{content}}</div>
</body>
</html>
```

**使用模板**：
```python
article = publisher.create_article(
    title='文章标题',
    content=content,
    template='custom',  # 使用自定义模板
    multi_images=True
)
```

### 5.2 配图策略优化

**配置优先级**：
```yaml
image:
  provider_priority:
    - "unsplash"          # 优先使用 Unsplash
    - "tongyi-wanxiang"   # 其次通义万相
    - "baidu-yige"        # 再次文心一格
    - "placeholder"       # 最后占位图
  
  auto_switch: true       # 自动切换
  max_retries: 2          # 最大重试 2 次
```

**查看使用统计**：
```bash
venv/bin/python -c "
from usage_counter import get_counter
counter = get_counter()
print(counter.get_summary())
"
```

### 5.3 文章格式优化

**Markdown 格式支持**：
```markdown
# 标题

**粗体** 和 *斜体*

## 列表

- 无序列表项 1
- 无序列表项 2

1. 有序列表项 1
2. 有序列表项 2

## 引用

> 这是一段引用

## 链接

[链接文字](https://example.com)

## 图片

![图片描述](image.jpg)
```

---

## 6. 常见问题

### Q1: 发布失败，提示 "invalid ip"

**原因**：IP 不在微信白名单中

**解决**：
1. 查询当前 IP：`curl https://api.ipify.org`
2. 在微信后台添加该 IP 到白名单
3. 等待 5-10 分钟生效

### Q2: 配图生成失败

**原因**：API Key 未配置或额度用尽

**解决**：
1. 检查配置文件中 API Key 是否正确
2. 查看使用量统计
3. 切换到其他图片源

### Q3: 标题超长被截断

**原因**：微信限制标题 64 字节

**解决**：
- 缩短标题长度
- 使用更简洁的表达
- 系统会自动截断并添加 "..."

### Q4: 内容格式错乱

**原因**：Markdown 格式不正确

**解决**：
- 检查 Markdown 语法
- 使用标准 Markdown 格式
- 避免使用不支持的语法

### Q5: 配置文件权限错误

**原因**：文件权限不正确

**解决**：
```bash
chmod 600 config.yaml
```

---

## 7. 最佳实践

### 7.1 成本控制

**推荐配置**：
```yaml
image:
  provider_priority:
    - "unsplash"          # 免费，真实照片
    - "tongyi-wanxiang"   # 免费 100 张/月
    - "baidu-yige"        # 免费 100 张/月
    - "dall-e-3"          # 付费（禁用）
  
  providers:
    dall-e-3:
      enabled: false  # 禁用付费服务
```

**预期成本**：
- 每月 200 张免费图片
- 可发布 66 篇文章（每篇 3 张图）
- 零成本

### 7.2 内容规范

**标题规范**：
- 长度：不超过 30 个汉字
- 格式：清晰简洁
- 避免：特殊符号、emoji（可能不显示）

**内容规范**：
- 字数：建议 500-5000 字
- 格式：标准 Markdown
- 配图：每 1500 字 1 张

### 7.3 发布流程

**推荐流程**：
1. 撰写文章（Markdown 格式）
2. 本地预览效果
3. 发布到草稿箱
4. 手机端预览
5. 确认无误后群发

### 7.4 备份策略

**配置备份**：
```bash
# 备份配置文件
cp config.yaml config.yaml.backup

# 备份文章
cp -r articles/ articles.backup/
```

**版本控制**：
```bash
# 使用 Git 管理
git init
git add config.yaml articles/
git commit -m "初始版本"
```

---

## 📞 技术支持

- **文档**：查看项目文档
- **问题**：查看 `CODE_REVIEW_REPORT.md`
- **配置**：查看 `CONFIG_ADVANCED.md`

---

**版本**：v1.0.0  
**最后更新**：2026-03-10  
**状态**：✅ 生产就绪
