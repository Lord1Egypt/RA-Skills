# 🦐 Skill Publisher

**一键多平台发布 OpenClaw Agent 技能**

把你的 AI Skills 同时发布到 ClawHub、GitHub Releases、SkillHub CN 等平台，一条命令搞定。

## 为什么需要它？

手动发布技能到多个平台：登录 A 平台 → 上传 → 登录 B 平台 → 上传 → 登录 C 平台... 重复每次版本更新。

用 Skill Publisher：

```bash
skill-publisher publish ./my-skill --to clawhub,github,skillhub --yes
```

一条命令，三个平台，全搞定。

## ✨ 特点

- **🔌 插件式平台架构** — 每个平台是独立适配器，社区可自由扩展
- **📦 一键多平台** — `--to clawhub,github,skillhub` 或 `--to all`
- **🔒 安全第一** — 发布前自动验证，敏感信息不入日志，需确认才执行
- **📋 版本管理** — 自动从 SKILL.md 读取版本，支持 `--bump patch|minor|major`
- **📝 发布历史** — 每次发布记录到 `~/.openclaw/skill-publisher/history.jsonl`

## 🚀 快速开始

### 安装

```bash
npm i -g clawhub   # ClawHub CLI
gh auth login      # GitHub CLI 登录
```

### 发布到单个平台

```bash
# ClawHub
skill-publisher publish ./my-skill --to clawhub

# GitHub Releases
skill-publisher publish ./my-skill --to github

# SkillHub CN（ClawHub 镜像，自动同步）
skill-publisher publish ./my-skill --to skillhub
```

### 一键多平台

```bash
# 指定平台
skill-publisher publish ./my-skill --to clawhub,github,skillhub

# 全部平台
skill-publisher publish ./my-skill --to all

# 跳过确认
skill-publisher publish ./my-skill --to all --yes
```

### 版本管理

```bash
# 查看当前版本
skill-publisher version ./my-skill

# 自动递增版本号
skill-publisher version ./my-skill --bump patch   # 1.0.0 → 1.0.1
skill-publisher version ./my-skill --bump minor   # 1.0.0 → 1.1.0
skill-publisher version ./my-skill --bump major   # 1.0.0 → 2.0.0

# 指定版本号
skill-publisher version ./my-skill --set 2.0.0
```

## 📦 内置平台

| 平台 | 认证方式 | 说明 |
|------|---------|------|
| 🟢 **ClawHub** | `clawhub login` | OpenClaw 官方技能注册中心 |
| 🟣 **GitHub Releases** | `gh auth login` | 自动创建 tag + release + 附件 |
| 🟠 **SkillHub CN** | 无需认证 | 腾讯云 ClawHub 镜像，国内高速下载 |

## 🔧 添加新平台

平台适配器只需要实现 3 个函数：

```bash
platform_<name>_manifest    # 返回平台元数据
platform_<name>_check_auth  # 检查认证状态
platform_<name>_publish     # 执行发布
```

详见 `references/adding-platforms.md`。

## 📁 项目结构

```
skill-publisher/
├── SKILL.md                   # OpenClaw 技能定义
├── README.md                  # 本文件
├── scripts/
│   ├── publish.sh             # 主入口
│   ├── platform_registry.sh   # 平台注册表
│   ├── platform_clawhub.sh    # ClawHub 适配器
│   ├── platform_github.sh     # GitHub Releases 适配器
│   ├── platform_skillhub.sh   # SkillHub CN 适配器
│   ├── validate.sh            # 技能验证
│   ├── version.sh             # 版本管理
│   └── status.sh              # 状态查询
└── references/
    ├── adding-platforms.md    # 添加平台指南
    └── platform-interface.md  # 平台接口规范
```

## 🛡️ 安全

- 发布前自动验证 SKILL.md 完整性
- 敏感关键词检测，防止意外泄露
- 所有发布操作需用户确认（`--yes` 跳过）
- 认证凭证不写入日志或输出

## License

MIT
