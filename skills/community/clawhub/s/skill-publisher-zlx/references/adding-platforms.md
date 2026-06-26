# 添加新平台适配器

本指南介绍如何为 skill-publisher 添加新的发布平台。

## 快速开始

### 1. 创建适配器文件

在 `scripts/` 目录下创建 `platform_<name>.sh`：

```bash
#!/usr/bin/env bash
set -euo pipefail

# @platform_name: myplatform
# @platform_label: My Platform
# @auth_method: api_key
# @auth_check: echo $MYPLATFORM_TOKEN
# @auth_hint: "export MYPLATFORM_TOKEN=your_token"
# @upload_type: http_api
# @upload_command: curl POST
# @requires_bin: curl
# @install_hint: "apt install curl"
# @supports_changelog: false
# @supports_version: true
```

### 2. 实现标准函数

```bash
# 必选函数
platform_myplatform_manifest() {
  # 返回 JSON 格式的平台元数据
  echo '{"name":"myplatform","label":"My Platform",...}'
}

platform_myplatform_check_auth() {
  # 检查认证状态
  # 成功: 输出 JSON + return 0
  # 失败: 输出 JSON + return 1
}

platform_myplatform_publish() {
  local tarball_path="$1"
  local skill_path="$2"
  # 执行发布逻辑
  # 成功: 输出 JSON + return 0
  # 失败: 输出 JSON + return 1
}

# 可选函数
platform_myplatform_status() {
  local skill_name="$1"
  # 查询远程版本/状态
}

platform_myplatform_post_publish() {
  local skill_name="$1"
  local version="$2"
  # 发布后钩子
}

platform_myplatform_validate() {
  local skill_path="$1"
  # 平台特定验证
}

platform_myplatform_help() {
  # 平台帮助信息
}
```

### 3. 测试适配器

```bash
# 直接运行适配器
bash scripts/platform_myplatform.sh manifest
bash scripts/platform_myplatform.sh check_auth

# 通过主入口测试
bash scripts/publish.sh platforms list
bash scripts/publish.sh platforms info myplatform
```

## @manifest 注解规范

每个适配器文件头部必须包含以下注解：

| 注解 | 必选 | 说明 |
|------|------|------|
| `@platform_name` | ✅ | 平台标识符（小写字母、数字、下划线） |
| `@platform_label` | ✅ | 平台显示名称 |
| `@auth_method` | ✅ | 认证方式 |
| `@auth_check` | ✅ | 认证检查命令 |
| `@auth_hint` | ✅ | 认证失败提示 |
| `@upload_type` | ✅ | 上传方式 |
| `@upload_command` | ✅ | 上传命令 |
| `@requires_bin` | ❌ | 依赖的二进制文件 |
| `@install_hint` | ❌ | 安装提示 |
| `@supports_changelog` | ❌ | 是否支持 changelog |
| `@supports_version` | ❌ | 是否支持版本管理 |

## 认证方式详解

### `cli` — CLI 工具自带登录

```bash
# @auth_method: cli
# @auth_check: mytool whoami
# @auth_hint: "请先运行: mytool login"

platform_myplatform_check_auth() {
  if ! command -v mytool &>/dev/null; then
    echo '{"status":"fail","error":"mytool not found"}'
    return 1
  fi
  if mytool whoami &>/dev/null; then
    echo '{"status":"ok"}'
  else
    echo '{"status":"fail","error":"Not logged in"}'
    return 1
  fi
}
```

### `api_key` — 环境变量

```bash
# @auth_method: api_key
# @auth_check: echo $MY_TOKEN
# @auth_hint: "export MY_TOKEN=your_token"

platform_myplatform_check_auth() {
  if [[ -z "${MY_TOKEN:-}" ]]; then
    echo '{"status":"fail","error":"MY_TOKEN not set"}'
    return 1
  fi
  echo '{"status":"ok","token_set":true}'
}
```

### `oauth` — OAuth 授权

```bash
platform_myplatform_check_auth() {
  if [[ -f ~/.myplatform/token ]]; then
    echo '{"status":"ok"}'
  else
    echo '{"status":"fail","auth_url":"https://myplatform.com/oauth/authorize"}'
    return 1
  fi
}
```

## 上传方式详解

### `tarball` — 主流程打包

适配器接收已打包的 tarball 路径，负责上传。

### `files` — 逐文件上传

```bash
platform_myplatform_publish() {
  local tarball_path="$1"
  local skill_path="$2"
  local tmp_dir=$(mktemp -d)
  tar -xzf "$tarball_path" -C "$tmp_dir"
  
  find "$tmp_dir" -type f | while read -r file; do
    curl -X POST -F "file=@$file" "https://api.myplatform.com/upload"
  done
  
  rm -rf "$tmp_dir"
}
```

### `http_api` — HTTP REST API

```bash
platform_myplatform_publish() {
  local tarball_path="$1"
  curl -X POST \
    -H "Authorization: Bearer $MY_TOKEN" \
    -F "file=@$tarball_path" \
    "https://api.myplatform.com/skills"
}
```

### `cli_tool` — 委托第三方 CLI

```bash
platform_myplatform_publish() {
  local tarball_path="$1"
  local skill_path="$2"
  mytool publish "$skill_path"
}
```

## 输出格式规范

所有函数输出必须是合法 JSON，包含 `module` 和 `status` 字段：

```json
{
  "module": "platform_myplatform",
  "function": "check_auth",
  "status": "ok",
  "data": "..."
}
```

状态值：
- `ok` — 成功
- `fail` — 失败
- `skipped` — 跳过
- `not_found` — 未找到
- `unknown` — 未知

## 安全要求

1. **不输出凭证**：token、secret、password 等不写入 JSON 输出
2. **不写入日志**：敏感信息不记录到 history.jsonl
3. **错误信息脱敏**：API 响应中可能包含凭证的部分要过滤

## 提交到社区

完成适配器后：

1. 在 `scripts/platform_<name>.sh` 中实现所有函数
2. 在 `references/platform-interface.md` 中添加平台文档
3. 测试所有函数的正常和异常路径
4. 提交 PR 到 skill-publisher 仓库
