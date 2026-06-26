# 平台接口规范

本文档定义 skill-publisher 平台适配器的完整接口规范。

## 架构概览

```text
publish.sh (主入口)
  │
  ├─ validate.sh        ← 全局验证
  ├─ version.sh         ← 版本管理
  ├─ platform_registry.sh ← 平台注册表
  │     ├─ platform_clawhub.sh
  │     ├─ platform_github.sh
  │     └─ platform_skillhub.sh
  └─ status.sh          ← 状态检查
```

## 平台发现机制

### 扫描规则

`platform_registry.sh` 扫描 `scripts/platform_*.sh` 文件：

1. 文件名匹配 `platform_*.sh`
2. 文件头部包含 `@platform_name` 注解
3. 解析所有 `@manifest` 注解为元数据

### 注册表函数

```bash
# 列出所有平台
platform_list
# 返回: {"module":"platform_registry","platforms":[{"name":"clawhub","label":"ClawHub"},...]}

# 获取平台详情
platform_info <name>
# 返回: {"module":"platform_registry","status":"ok","platform":{...}}

# 加载平台适配器
platform_load <name>
# 效果: source platform_<name>.sh，使函数可用
```

## 标准函数接口

### 必选函数

#### `platform_<name>_manifest`

返回平台元数据 JSON。

```bash
platform_<name>_manifest() {
  cat <<'EOF'
{
  "name": "myplatform",
  "label": "My Platform",
  "auth_method": "api_key",
  "upload_type": "http_api",
  ...
}
EOF
}
```

#### `platform_<name>_check_auth`

检查认证状态。

**输入**: 无（从环境变量或配置读取凭证）

**输出**: JSON

```json
{
  "module": "platform_<name>",
  "function": "check_auth",
  "status": "ok",
  "user": "username"
}
```

**返回值**:
- `0` — 认证成功
- `1` — 认证失败

#### `platform_<name>_publish`

执行发布操作。

**输入**:
- `$1` — tarball 路径
- `$2` — 技能目录路径

**输出**: JSON

```json
{
  "module": "platform_<name>",
  "function": "publish",
  "status": "ok",
  "url": "https://..."
}
```

**返回值**:
- `0` — 发布成功
- `1` — 发布失败

### 可选函数

#### `platform_<name>_status`

查询远程版本/状态。

**输入**: `$1` — 技能名称

**输出**: JSON

```json
{
  "module": "platform_<name>",
  "function": "status",
  "status": "ok",
  "skill_name": "my-skill",
  "remote_info": "..."
}
```

#### `platform_<name>_validate`

平台特定验证。

**输入**: `$1` — 技能目录路径

**输出**: JSON

#### `platform_<name>_post_publish`

发布后钩子。

**输入**:
- `$1` — 技能名称
- `$2` — 版本号

**输出**: JSON

#### `platform_<name>_help`

平台帮助信息。

**输入**: 无

**输出**: 纯文本

## 输出格式规范

### JSON 结构

所有函数输出必须是合法 JSON，包含以下必选字段：

```json
{
  "module": "platform_<name>",
  "function": "<function_name>",
  "status": "<status_code>"
}
```

### 状态码

| 状态 | 说明 |
|------|------|
| `ok` | 操作成功 |
| `fail` | 操作失败 |
| `skipped` | 操作被跳过 |
| `not_found` | 目标未找到 |
| `unknown` | 状态未知 |
| `partial` | 部分成功 |

### 错误输出

错误信息通过 `error` 字段返回，同时通过 stderr 输出详细信息：

```json
{
  "module": "platform_<name>",
  "function": "check_auth",
  "status": "fail",
  "error": "Authentication failed",
  "hint": "请先运行: mytool login"
}
```

## 认证方式

### `cli` — CLI 工具自带登录

- 适配器调用 CLI 命令检查登录态
- 认证失败时在 `hint` 中给出登录命令
- 示例: `clawhub whoami`, `gh auth status`

### `api_key` — 环境变量

- 适配器检查环境变量是否设置
- 可选: 调用 API 验证 token 有效性
- 示例: `SKILLHUB_TOKEN`, `NPM_TOKEN`

### `oauth` — OAuth 授权

- 适配器返回授权 URL
- 用户在浏览器中完成授权
- 适配器接收并存储 token

### `web_login` — 浏览器登录

- 适配器打开浏览器
- 用户在浏览器中登录
- 适配器通过回调或轮询获取确认

### `ssh_key` — SSH 密钥

- 适配器检查 `~/.ssh/` 下的密钥
- 提示用户将公钥添加到平台

### `none` — 无需认证

- 直接跳过认证检查
- 用于公开只读平台

## 上传方式

### `tarball` — 打包后上传

主流程负责打包，适配器接收 tarball 路径：

```bash
# 主流程:
tar -czf /tmp/skill.tar.gz -C /path/to skill/

# 适配器:
platform_<name>_publish() {
  local tarball_path="$1"
  upload "$tarball_path"
}
```

### `files` — 逐文件上传

适配器负责遍历目录并逐文件上传：

```bash
platform_<name>_publish() {
  local tarball_path="$1"
  local skill_path="$2"
  local tmp_dir=$(mktemp -d)
  tar -xzf "$tarball_path" -C "$tmp_dir"
  
  find "$tmp_dir" -type f | while read -r file; do
    upload_file "$file"
  done
  
  rm -rf "$tmp_dir"
}
```

### `http_api` — HTTP REST API

适配器构造 HTTP 请求上传：

```bash
platform_<name>_publish() {
  local tarball_path="$1"
  curl -X POST \
    -H "Authorization: Bearer $TOKEN" \
    -F "file=@$tarball_path" \
    "https://api.platform.com/skills"
}
```

### `cli_tool` — 委托第三方 CLI

适配器调用第三方 CLI 工具：

```bash
platform_<name>_publish() {
  local tarball_path="$1"
  local skill_path="$2"
  mytool publish "$skill_path"
}
```

## 主流程集成

### 发布流程

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

### 状态查询流程

```text
status <skill-path>
  │
  ├─ 1. 读取 SKILL.md 元数据
  ├─ 2. for each platform:
  │     ├─ load adapter
  │     ├─ status <skill-name>
  │     └─ 收集结果
  └─ 3. 汇总输出
```

## 安全要求

### 凭证保护

- 不将凭证写入 JSON 输出
- 不将凭证记录到 history.jsonl
- 错误信息中过滤凭证相关内容

### 输入验证

- 验证 tarball 路径存在
- 验证技能目录结构
- 验证版本号格式

### 错误处理

- 所有外部命令调用检查返回值
- 使用 `set -euo pipefail` 防止静默失败
- 错误信息清晰，包含修复建议

## 扩展点

### 自定义验证

实现 `platform_<name>_validate` 函数：

```bash
platform_myplatform_validate() {
  local skill_path="$1"
  
  # 检查平台特定要求
  if [[ ! -f "$skill_path/README.md" ]]; then
    echo '{"status":"fail","error":"README.md required"}'
    return 1
  fi
  
  echo '{"status":"ok"}'
}
```

### 发布后钩子

实现 `platform_<name>_post_publish` 函数：

```bash
platform_myplatform_post_publish() {
  local skill_name="$1"
  local version="$2"
  
  # 发送通知
  curl -X POST "https://hooks.slack.com/..." \
    -d "{\"text\":\"Published $skill_name@$version\"}"
  
  echo '{"status":"ok"}'
}
```

## 内置平台参考

| 平台 | auth | upload | 说明 |
|------|------|--------|------|
| ClawHub | cli | cli_tool | OpenClaw 官方 |
| GitHub | cli | cli_tool | GitHub Releases |
| SkillHub CN | api_key | http_api | 国内社区 |

## 参考

- [添加新平台指南](adding-platforms.md)
- [SKILL.md 规范](../SKILL.md)
