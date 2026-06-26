---
name: "skill-publisher"
description: "将 Agent 技能发布到多个平台：ClawHub、GitHub Releases、SkillHub CN。支持验证、打包、版本管理和一键多平台发布。"
version: "1.3.0"
---

# Skill Publisher

将本地 Agent 技能发布到多个平台。支持单平台发布、一键多平台发布，平台可扩展。

## 平台架构

采用**插件式平台注册**，每个平台是独立适配器，通过统一元数据声明自己的能力。

```text
skill-publisher/
  SKILL.md
  scripts/
    publish.sh              # 主入口
    platform_registry.sh    # 平台注册表 & 能力发现
    platform_clawhub.sh     # ClawHub 适配器
    platform_github.sh      # GitHub Releases 适配器
    platform_skillhub.sh    # SkillHub CN 适配器
    validate.sh
    version.sh
    status.sh
  references/
    adding-platforms.md     # 如何添加新平台
    platform-interface.md   # 完整接口规范
```

### 平台适配器声明（manifest）

每个平台适配器在文件头部以注释形式声明元数据：

```bash
# @platform_name: clawhub
# @platform_label: ClawHub (OpenClaw Registry)
# @auth_method: cli          # cli | api_key | oauth | web_login | ssh_key | none
# @auth_check: clawhub whoami
# @auth_hint: "请先运行: clawhub login"
# @upload_type: tarball      # tarball | files | http_api | cli_tool
# @upload_command: clawhub publish
# @requires_bin: clawhub
# @install_hint: "npm i -g clawhub"
# @supports_changelog: true
# @supports_version: true
```

### 认证方式（@auth_method）

| auth_method | 说明 | 适配器职责 |
|-------------|------|-----------|
| `cli` | CLI 工具自带登录 | 调用 CLI 检查登录态，给出登录提示 |
| `api_key` | 环境变量或配置文件 | 检查环境变量，提示设置方式 |
| `oauth` | OAuth 浏览器授权 | 返回授权 URL，等待 token 输入 |
| `web_login` | 浏览器登录（无 CLI） | 打开浏览器，提示粘贴确认码 |
| `ssh_key` | SSH 密钥认证 | 检查密钥，提示添加到平台 |
| `none` | 无需认证 | 直接跳过 |

### 上传方式（@upload_type）

| upload_type | 说明 | 适配器职责 |
|-------------|------|-----------|
| `tarball` | 打包 tar.gz 后上传 | 主流程打包，适配器接收路径并上传 |
| `files` | 逐文件上传 | 遍历目录，逐文件调用上传接口 |
| `http_api` | HTTP REST API | 构造 HTTP 请求上传 |
| `cli_tool` | 委托第三方 CLI | 组装命令行并执行 |

### 标准函数接口

```bash
# 必选
platform_<name>_manifest       # 返回元数据 JSON
platform_<name>_check_auth     # 检查认证
platform_<name>_publish        # 执行发布

# 可选
platform_<name>_validate       # 平台特定验证
platform_<name>_status         # 查询远程版本/状态
platform_<name>_post_publish   # 发布后钩子
platform_<name>_help           # 平台帮助信息
```

### 主流程

```text
publish <path> --to <platforms>
  │
  ├─ 1. validate       ← 全局验证
  ├─ 2. version check  ← 版本号管理
  ├─ 3. for each platform:
  │     ├─ manifest    ← 读取平台能力
  │     ├─ check_auth  ← 检查认证
  │     ├─ validate    ← 平台验证（可选）
  │     ├─ package     ← 按 upload_type 打包
  │     ├─ publish     ← 上传
  │     └─ post_publish ← 后钩子（可选）
  └─ 4. summary        ← 汇总结果
```

## 内置平台

### 🟢 ClawHub（OpenClaw 官方）

- **auth:** `cli`（`clawhub login`）
- **upload:** `tarball` → `clawhub publish`
- 支持 slug、changelog、版本管理

### 🟣 GitHub Releases

- **auth:** `cli`（`gh auth login`）
- **upload:** `cli_tool` → `gh release create`
- 自动创建 tag，附带 tarball

### 🟠 SkillHub CN（腾讯云 ClawHub 镜像）

- **地址:** `skillhub.cloud.tencent.com`
- **模式:** `mirror`（ClawHub 镜像，发布到 ClawHub 后自动同步）
- **auth:** 无需单独认证，通过 ClawHub 发布即可
- 专为中国用户优化，国内高速下载

## 第三方扩展

参考 `references/adding-platforms.md`，社区可添加：

| 平台 | auth | upload | 说明 |
|------|------|--------|------|
| GitLab Packages | api_key | http_api | REST API |
| Gitee | ssh_key | cli_tool | git push |
| 自建 Registry | api_key | http_api | POST tarball |
| 飞书云盘 | oauth | files | lark-cli 逐文件上传 |
| ClawHub Mirror | none | mirror | 自动同步，无需单独发布 |

## 命令

```bash
# 验证
skill-publisher validate <skill-path>

# 打包
skill-publisher package <skill-path> [--output <dir>] [--version <ver>]

# 发布
skill-publisher publish <path> --to <platform> [平台参数...]
skill-publisher publish <path> --to clawhub,github
skill-publisher publish <path> --to all
skill-publisher publish <path> --to <platform> --yes

# 版本管理
skill-publisher version <skill-path>
skill-publisher version <skill-path> --bump patch|minor|major
skill-publisher version <skill-path> --set <ver>

# 状态检查
skill-publisher status <skill-path>

# 平台管理
skill-publisher platforms list
skill-publisher platforms info <name>
```

## 安全规则

- 发布前自动 validate，失败则中止
- 不发布含敏感关键词的文件
- 认证凭证不写入日志或输出
- 所有发布操作需用户确认（`--yes` 跳过）
- 每次发布记录到 `~/.openclaw/skill-publisher/history.jsonl`（不含凭证）

## 参考

- ClawHub CLI: `clawhub --help`
- GitHub CLI: `gh release create --help`
- SkillHub CN: https://skillhub.cn/
- OpenClaw 技能规范: `skill-creator` skill
