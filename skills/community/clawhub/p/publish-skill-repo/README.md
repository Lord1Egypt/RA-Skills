# Publish Skill

一个 Claude Code Skill，用于将 Skill 项目发布到 GitHub 并同步到 ClawHub。

在 Claude Code 中说「发布skill」或「publish skill」即可启动交互式发布流程，无需记忆脚本命令。

## 功能

- 自动识别新项目 / 已有项目，走不同发布流程
- 新项目一键完成：Git 初始化、LICENSE、GitHub 仓库、ClawHub 同步、v1.0.0 发布
- 已有项目交互式引导：总结变更 → 确认提交信息 → 建议版本号 → 执行发布
- 缺少 LICENSE / workflow / Secrets 时自动补齐
- 底层脚本支持幂等操作，可安全重复运行

## 使用方式

### 作为 Skill 使用（推荐）

在包含 `SKILL.md` 的项目目录中，对 Claude Code 说：

```
发布skill
```

Skill 会自动：

1. 检查前置条件（SKILL.md、gh CLI、ClawHub Token）
2. 判断是新项目还是已有项目
3. **新项目** — 自动走完整个流程
4. **已有项目** — 交互式确认变更、提交信息和版本号后发布

### 直接运行脚本

```bash
./scripts/publish-skill-repo.sh <skill目录> [github-owner] [public|private]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| skill目录 | Skill 项目路径（需包含 SKILL.md） | 必填 |
| github-owner | GitHub 用户名或组织名 | 当前用户 |
| public\|private | 仓库可见性 | public |

```bash
# 默认：当前用户、公开仓库
./scripts/publish-skill-repo.sh ~/skills/my-skill

# 指定组织和私有仓库
./scripts/publish-skill-repo.sh ~/skills/my-skill myorg private
```

## 准备工作

### 1. ClawHub Token

1. 打开 https://clawhub.ai/
2. 点击 **"Login with GitHub"** 登录
3. 进入 **Settings** → **API tokens** → **"Create token"**
4. 复制生成的 Token（格式：`clh_iVnxxxxxxxx...`）

Token 仅显示一次，请立即保存：

```bash
mkdir -p ~/.clawhub
echo "your-clawhub-token" > ~/.clawhub/secret_token
chmod 600 ~/.clawhub/secret_token
```

### 2. GitHub CLI

```bash
# macOS
brew install gh

# 登录 GitHub
gh auth login
```

## 发布流程

### 新项目

自动完成所有步骤：

1. 初始化 Git → 创建 LICENSE → 创建 workflow
2. 创建 GitHub 仓库 → 配置 ClawHub Token
3. 推送代码 → 创建 v1.0.0 tag
4. GitHub Actions 自动发布到 ClawHub

### 已有项目

交互式引导发布新版本：

1. 总结自上次 tag 以来的变更
2. 确认 commit message
3. 建议版本号（feat → minor，fix → patch，breaking → major）
4. 提交、推送、打 tag、发布

## 项目结构

```
publish-skill-repo/
├── SKILL.md                          # Skill 定义（触发词、流程逻辑）
├── scripts/
│   └── publish-skill-repo.sh         # 底层自动化脚本
└── .github/workflows/
    └── publish-to-clawhub.yml        # 新项目自动生成的 workflow
```

## 配置说明

| 配置项 | 路径/格式 |
|--------|----------|
| Token 文件 | `~/.clawhub/secret_token` |
| Tag 格式 | `v*.*.*`（如 v1.0.0） |
| Workflow | `.github/workflows/publish-to-clawhub.yml` |
