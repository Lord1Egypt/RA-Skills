# OpenClaw 技能兼容格式与安装指南

## 技能结构

本技能兼容 **Hermes Agent** 和 **OpenClaw** 两个平台。打包内容：

```
roadshow-capture/
├── SKILL.md                              # 双平台 frontmatter（hermes + openclaw）
├── scripts/
│   └── netroadshow-capture.py            # Playwright 自动化脚本
└── references/
    ├── netroadshow-practice.md           # 实操记录
    └── openclaw-setup.md                 # 本文件
```

## OpenClaw 安装

### 方法 A：手动部署（推荐给朋友分享）

```bash
# 1. 解压到 skills 目录
tar -xzf roadshow-capture.tar.gz -C ~/.config/openclaw/skills/

# 2. 设置邮箱（或等 agent 首次运行时提问）
export NRS_EMAIL=your@email.com

# 3. 装 Chromium 浏览器（pip 包 OpenClaw 会自动装）
playwright install chromium

# 4. 确认加载
openclaw skills check
```

### 方法 B：ClawHub 发布

1. 登录 ClawHub：`clawhub login`（WSL 需要 fake xdg-open 绕开浏览器问题）
2. 发布：`clawhub publish ./roadshow-capture --slug roadshow-capture --version <ver>`（无需 --owner，从登录信息推断）
3. 朋友安装：`openclaw skills install roadshow-capture`

## 双平台 frontmatter 要点

```yaml
metadata:
  hermes:          # Hermes Agent 原生格式
    tags: [...]
    related_skills: [...]
  openclaw:        # OpenClaw 兼容格式（自动忽略不识别的 key）
    requires:
      bins: [python3]
      env: [NRS_EMAIL]      # 声明的环境变量，安装时会通知用户
    install:
      - kind: pip
        packages: [playwright, pillow]   # OpenClaw 自动安装 pip 包
```

**关键限制**：
- `playwright install chromium` 仍需手动执行（OpenClaw 无 postinstall hook）
- OpenClaw 前端的 install 只跑 pip，不能跑任意 shell 命令
- 两个平台的 metadata 不会冲突，OpenClaw 忽略 `hermes` 字段，Hermes 忽略 `openclaw` 字段

## 脚本中的凭证解析优先级

```python
# Resolve email: CLI arg → env var → agent 提问后写入 .env
email = args.email or os.environ.get("NRS_EMAIL")
assert email, "NRS_EMAIL 未设置。请通过 --email 参数或 export NRS_EMAIL=your-email@company.com 设置邮箱。"
```

优先级：`--email 参数` > `NRS_EMAIL 环境变量` > `skills/roadshow-capture/scripts/.env`

**没有 hardcoded 默认值**。首次使用时 agent 会主动问用户邮箱并写入 `.env`。

## ClawHub 发布陷阱（WSL 环境）

- `clawhub login` 会自动尝试 `xdg-open` 打开浏览器，WSL 无显示会报 `EACCES`
- 解决方案：创建假 `xdg-open` 脚本写入 URL，手动在 Windows 浏览器打开
- 首次发布需在 ClawHub 网页上接受 MIT-0 许可证（Publish 页面勾选），CLI 无 `--accept-mit0` 参数
- CLI 的 `--owner` 参数在 v0.7.0 中不存在，owner 从登录信息自动推断
