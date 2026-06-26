# 多平台内容自动分发

在小红书发布内容后，自动同步到抖音、视频号、快手等多个平台。

## 功能亮点

- 🤖 **自动同步** - 一键将小红书内容同步到多个平台
- 🖼️ **图片适配** - 自动处理不同平台的图片尺寸要求
- 📝 **智能填写** - 自动填写标题、描述和标签
- 🔐 **验证码处理** - 自动识别并处理发布后的验证码
- ⚙️ **灵活配置** - 支持自定义各平台发布策略

## 快速开始

### 安装依赖

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install chromium

# 安装图片处理库（可选）
pip install Pillow
```

### 配置账号

```bash
# 复制配置模板
cp config/accounts.yaml.example config/accounts.yaml

# 编辑配置
nano config/accounts.yaml
```

### 运行分发

```bash
# 同步最新发布的小红书内容
python3 scripts/distribute.py

# 指定笔记ID
python3 scripts/distribute.py --note-id 123456789

# 同步到指定平台
python3 scripts/distribute.py --targets douyin,kuaishou

# 调试模式
python3 scripts/distribute.py --debug
```

## 目录结构

```
skill-distribute/
├── SKILL.md              # Skill 主文档
├── README.md             # 本文件
├── requirements.txt      # Python 依赖
├── scripts/
│   ├── distribute.py     # 主分发脚本
│   ├── batch_distribute.py  # 批量分发
│   ├── schedule.py       # 定时任务
│   └── review_skill.py   # 审查脚本
├── config/
│   ├── accounts.yaml     # 账号配置
│   ├── image.yaml        # 图片处理配置
│   ├── content.yaml      # 内容适配配置
│   ├── captcha.yaml      # 验证码配置
│   └── strategy.yaml     # 发布策略配置
└── references/
    ├── PLATFORM_GUIDE.md # 平台适配指南
    ├── SELECTORS.md      # 选择器配置
    ├── API.md            # API 文档
    └── CHANGELOG.md      # 更新日志
```

## 平台支持

| 平台 | 登录方式 | 图片 | 视频 | 状态 |
|------|----------|------|------|------|
| 小红书 | 扫码 | ✅ | ✅ | 源平台 |
| 抖音 | 手机/扫码 | ✅ | ✅ | 支持 |
| 视频号 | 微信扫码 | ✅ | ✅ | 支持 |
| 快手 | 手机/扫码 | ✅ | ✅ | 支持 |

## 图片尺寸适配

| 源尺寸 | 目标平台 | 处理方式 |
|--------|----------|----------|
| 3:4 | 9:16 | 模糊填充 |
| 1:1 | 9:16 | 纯色填充 |
| 4:3 | 9:16 | 智能裁剪 |

## 高级用法

### 批量分发

```bash
# 同步最近 10 篇笔记
python3 scripts/batch_distribute.py --recent 10

# 从文件读取笔记列表
python3 scripts/batch_distribute.py --file notes.txt
```

### 定时发布

```bash
# 每天 9:00 自动同步
python3 scripts/schedule.py --time "09:00" --daily

# 每周一、三、五 20:00 同步
python3 scripts/schedule.py --time "20:00" --days mon,wed,fri
```

### 错峰发布

```bash
# 平台间间隔 30 分钟
python3 scripts/distribute.py --stagger
```

## 配置说明

### 账号配置 (config/accounts.yaml)

```yaml
platforms:
  douyin:
    enabled: true
    login_type: phone
    phone: "13800138000"
```

### 图片处理 (config/image.yaml)

```yaml
image_processing:
  fill_mode: blur  # blur | solid | crop
  quality: 95
```

### 验证码处理 (config/captcha.yaml)

```yaml
captcha:
  timeout: 30
  max_retries: 3
```

## 安全提示

⚠️ **重要提醒**：

1. 不要在公共环境保存密码
2. 使用扫码登录更安全
3. 遵守各平台社区规范
4. 避免频繁操作触发风控
5. 配置文件设置权限 600

## 故障排除

### 无法打开浏览器

```bash
# 重新安装 Playwright
playwright install --force chromium
```

### 登录失败

```bash
# 清除登录缓存
rm -rf data/cookies/*

# 强制重新登录
python3 scripts/distribute.py --relogin
```

### 验证码处理失败

- 增加重试次数
- 切换到手动模式
- 使用第三方验证码服务

## 参考文档

- [平台适配指南](references/PLATFORM_GUIDE.md)
- [选择器配置](references/SELECTORS.md)
- [API 文档](references/API.md)
- [更新日志](references/CHANGELOG.md)

## 许可证

MIT
