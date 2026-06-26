---
name: token-config-checker
description: 批量检测 token / auth JSON 配置文件有效性，并可对 access token 做在线轻量探测，自动输出脱敏报告。适用于排查 Codex/OpenAI/OpenAI 兼容客户端导出的登录配置、会话凭据文件、token 缓存文件。支持把配置分为 valid / no_quota / invalid 三类并分别保存。 Also validates token/auth JSON files such as Codex/OpenAI/OpenAI-compatible exported session configs, supports online probing, redacted reports, and saving valid / no_quota / invalid configs into separate directories.
---

# token-config-checker

[简体中文](#简体中文) | [English](#english)

---

## 简体中文

用于检测包含 `access_token` / `refresh_token` / `id_token` 的 JSON 配置文件是否还有效。

### 提供内容
- `scripts/check_token_configs.py`：基础版，支持离线检测和可选在线探测
- `scripts/check_token_configs_plus.py`：增强版，支持脱敏输出、失败原因分类、三分类保存、写入报告文件

### 快速用法

#### 检测单个文件
```bash
python3 scripts/check_token_configs.py /path/to/file.json
```

#### 批量检测目录
```bash
python3 scripts/check_token_configs.py /path/to/dir
```

#### 在线探测 access_token
```bash
python3 scripts/check_token_configs.py /path/to/file.json --probe
```

#### 增强版：按 valid / no_quota / invalid 三分类保存
```bash
python3 scripts/check_token_configs_plus.py ./tokens \
  --probe \
  --probe-url https://api.openai.com/v1/models \
  --save-valid-dir ./valid_configs \
  --save-no-quota-dir ./no_quota_configs \
  --save-invalid-dir ./invalid_configs \
  --group-by-type \
  --out report.txt
```

### 输出重点
- `valid_offline`：离线结构和过期时间是否正常
- `online_valid`：在线探测是否通过
- `failure_class`：失败分类，例如 `token_expired` / `online_invalid_or_revoked`
- `bucket`：最终分类（`valid` / `no_quota` / `invalid`）

### 注意事项
- 这类配置文件非常敏感，不要分享原始文件。
- 对 Codex 配置，在线结果通常比离线判断更重要。
- 默认探测地址使用 OpenAI 官方接口；如果你使用私有中转或自定义面板，请手动传入 `--probe-url`。
- 建议开启 `--out` 输出报告，便于复查。

---

## English

Use this skill to validate JSON config files containing `access_token` / `refresh_token` / `id_token`.

### Included scripts
- `scripts/check_token_configs.py`: basic version with offline checks and optional online probing
- `scripts/check_token_configs_plus.py`: enhanced version with redacted output, failure classification, three-bucket saving, and report generation

### Quick usage

#### Check one file
```bash
python3 scripts/check_token_configs.py /path/to/file.json
```

#### Batch scan a directory
```bash
python3 scripts/check_token_configs.py /path/to/dir
```

#### Online probe access_token
```bash
python3 scripts/check_token_configs.py /path/to/file.json --probe
```

#### Enhanced: save configs into valid / no_quota / invalid buckets
```bash
python3 scripts/check_token_configs_plus.py ./tokens \
  --probe \
  --probe-url https://api.openai.com/v1/models \
  --save-valid-dir ./valid_configs \
  --save-no-quota-dir ./no_quota_configs \
  --save-invalid-dir ./invalid_configs \
  --group-by-type \
  --out report.txt
```

### Key outputs
- `valid_offline`: whether the file looks structurally valid offline
- `online_valid`: whether online probing succeeded
- `failure_class`: failure reason classification
- `bucket`: final bucket (`valid` / `no_quota` / `invalid`)

### Notes
- These files are highly sensitive. Do not share raw configs.
- For Codex-style configs, online probe results are usually more important than offline checks.
- Default probe target uses the OpenAI official endpoint; if you use a private relay or custom panel, pass your own `--probe-url` explicitly.
- Prefer `--out` to generate a reusable report.
