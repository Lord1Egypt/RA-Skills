---
name: skill-distribute
description: 多平台内容自动分发工具。在小红书发布后，自动将内容同步到抖音、视频号、快手。支持自动处理图片尺寸、填写标题标签、处理验证码。
license: MIT
compatibility: 需要 Python 3.8+、Chrome 浏览器、Playwright 或 Selenium
metadata:
  author: content-distributor
  version: "1.0"
  platforms: xiaohongshu,douyin,shipinhao,kuaishou
---

# 多平台内容自动分发

在小红书发布内容后，自动同步到抖音、视频号、快手等多个平台。

## 核心功能

- 🤖 **自动同步**: 从小红书获取内容，自动发布到其他平台
- 🖼️ **图片适配**: 自动处理不同平台的图片尺寸要求
- 📝 **智能填写**: 自动填写标题、描述和标签
- 🔐 **验证码处理**: 自动识别并处理发布后的验证码
- ⚙️ **灵活配置**: 支持自定义各平台发布策略

## 支持平台

| 平台 | 状态 | 图片尺寸 | 特殊要求 |
|------|------|----------|----------|
| 小红书 | 源平台 | 3:4 / 1:1 / 4:3 | - |
| 抖音 | ✅ 支持 | 9:16 (1080x1920) | 视频优先 |
| 视频号 | ✅ 支持 | 9:16 (1080x1920) | 需微信扫码 |
| 快手 | ✅ 支持 | 9:16 (1080x1920) | - |

## 快速开始

### 1. 配置账号信息

```bash
# 编辑配置文件
nano config/accounts.yaml
```

```yaml
# config/accounts.yaml
platforms:
  xiaohongshu:
    enabled: true
    username: your_username
    # 使用扫码登录，无需密码
    
  douyin:
    enabled: true
    username: your_phone
    # 使用验证码登录
    
  shipinhao:
    enabled: true
    # 使用微信扫码登录
    
  kuaishou:
    enabled: true
    username: your_phone
    # 使用验证码登录
```

### 2. 运行分发

```bash
# 基本用法 - 同步最新发布的小红书内容
python3 scripts/distribute.py --source xiaohongshu

# 指定具体笔记
python3 scripts/distribute.py --note-id 123456789

# 同步到指定平台
python3 scripts/distribute.py --targets douyin,kuaishou

# 使用桌面端 App（更稳定）
python3 scripts/distribute.py --use-app

# 调试模式（查看浏览器操作）
python3 scripts/distribute.py --debug
```

### 3. 批量分发

```bash
# 批量同步最近 10 篇笔记
python3 scripts/batch_distribute.py --recent 10

# 从文件读取笔记列表
python3 scripts/batch_distribute.py --file notes.txt
```

## 图片尺寸自动适配

### 适配规则

| 源尺寸 | 目标平台 | 处理方式 |
|--------|----------|----------|
| 3:4 | 抖音 9:16 | 上下加黑边 / 智能填充 |
| 1:1 | 抖音 9:16 | 上下加黑边 |
| 4:3 | 视频号 9:16 | 智能裁剪 |
| 9:16 | 小红书 3:4 | 左右加白边 |

### 智能填充选项

```yaml
# config/image.yaml
image_processing:
  fill_mode: blur  # blur | solid | extend
  background_color: "#000000"
  blur_radius: 50
  quality: 95
```

## 标题标签智能处理

### 平台差异适配

```yaml
# config/content.yaml
content_adaptation:
  xiaohongshu:
    max_title_length: 20
    max_desc_length: 1000
    max_tags: 10
    tag_prefix: "#"
    
  douyin:
    max_title_length: 55
    max_desc_length: 500
    max_tags: 5
    tag_prefix: "#"
    # 自动添加热门标签
    auto_tags: ["热门", "推荐"]
    
  shipinhao:
    max_title_length: 30
    max_desc_length: 300
    max_tags: 3
    tag_prefix: "#"
    
  kuaishou:
    max_title_length: 40
    max_desc_length: 400
    max_tags: 5
    tag_prefix: "#"
```

### 标签转换示例

小红书标签 → 各平台标签：
- `#穿搭分享` → 抖音: `#穿搭分享 #ootd #时尚`
- `#美食探店` → 快手: `#美食探店 #吃货 #探店`

## 验证码处理

### 支持的验证码类型

| 类型 | 处理方式 | 成功率 |
|------|----------|--------|
| 滑块验证码 | 自动识别滑动距离 | 85% |
| 点选验证码 | 图像识别 + 点击 | 75% |
| 文字验证码 | OCR 识别 | 90% |
| 短信验证码 | 等待用户输入 | 100% |

### 验证码配置

```yaml
# config/captcha.yaml
captcha:
  # 自动处理超时时间（秒）
  timeout: 30
  
  # 失败重试次数
  max_retries: 3
  
  # 第三方验证码服务（可选）
  service:
    enabled: false
    provider: "2captcha"  # 2captcha | anti-captcha
    api_key: "your_api_key"
```

## 高级用法

### 定时分发

```bash
# 每天 9:00 自动同步
python3 scripts/schedule.py --time "09:00" --daily

# 每周一、三、五 20:00 同步
python3 scripts/schedule.py --time "20:00" --days mon,wed,fri
```

### 内容过滤

```bash
# 只同步特定标签的内容
python3 scripts/distribute.py --filter-tag "穿搭"

# 排除特定关键词
python3 scripts/distribute.py --exclude "广告|推广"
```

### 发布策略

```yaml
# config/strategy.yaml
publish_strategy:
  # 错峰发布
  stagger:
    enabled: true
    interval: 30  # 平台间隔 30 分钟
    
  # 随机延迟
  random_delay:
    enabled: true
    min: 5
    max: 15
    
  # 失败重试
  retry:
    enabled: true
    max_attempts: 3
    delay: 60
```

## 浏览器自动化

### 使用 Playwright（推荐）

```bash
# 安装依赖
pip install playwright
playwright install chromium

# 运行
python3 scripts/distribute.py --driver playwright
```

### 使用 Selenium

```bash
# 安装依赖
pip install selenium webdriver-manager

# 运行
python3 scripts/distribute.py --driver selenium
```

### 使用桌面端 App

```bash
# 需要安装各平台桌面客户端
python3 scripts/distribute.py --use-app
```

## 日志与监控

### 查看日志

```bash
# 实时查看日志
tail -f logs/distribute.log

# 查看最近 100 条
cat logs/distribute.log | tail -100
```

### 发布统计

```bash
# 生成发布报告
python3 scripts/report.py --period week

# 导出 CSV
python3 scripts/report.py --export csv --output report.csv
```

## 常见问题

### Q: 登录状态会过期吗？

A: 会。建议：
- 定期重新登录（每周一次）
- 使用 `--relogin` 参数强制重新登录
- 配置自动登录检测

### Q: 图片处理速度慢怎么办？

A: 优化建议：
- 使用本地图片缓存
- 降低图片质量参数
- 使用多线程处理

### Q: 验证码处理失败怎么办？

A: 解决方案：
- 增加重试次数
- 使用第三方验证码服务
- 切换到手动模式（等待用户输入）

### Q: 如何避免被封号？

A: 安全措施：
- 设置合理的发布间隔
- 使用随机延迟
- 避免短时间内大量发布
- 模拟人工操作（鼠标移动、点击间隔）

## 安全提示

⚠️ **重要提醒**：

1. **账号安全**
   - 不要在公共环境保存密码
   - 使用扫码登录更安全
   - 定期更换密码

2. **平台规则**
   - 遵守各平台社区规范
   - 避免频繁操作触发风控
   - 注意内容版权

3. **隐私保护**
   - 配置文件设置权限 600
   - 不要在日志中记录敏感信息
   - 定期清理临时文件

## 故障排除

### 无法打开浏览器

```bash
# 检查 Chrome 安装
which google-chrome

# 重新安装 Playwright
playwright install --force chromium
```

### 元素定位失败

```bash
# 更新选择器配置
python3 scripts/update_selectors.py

# 使用调试模式查看页面结构
python3 scripts/distribute.py --debug --screenshot
```

### 登录失败

```bash
# 清除登录缓存
rm -rf data/cookies/*

# 强制重新登录
python3 scripts/distribute.py --relogin
```

## 参考文档

- [平台适配指南](references/PLATFORM_GUIDE.md)
- [选择器配置](references/SELECTORS.md)
- [API 文档](references/API.md)
- [更新日志](references/CHANGELOG.md)

## 更新与支持

- GitHub: https://github.com/your-repo/skill-distribute
- 问题反馈: https://github.com/your-repo/skill-distribute/issues
- 文档: https://skill-distribute.readthedocs.io
