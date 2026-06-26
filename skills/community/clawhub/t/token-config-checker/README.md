# token-config-checker

[简体中文](#简体中文) | [English](#english)

---

## 简体中文

用于检测这类 token / auth JSON 配置文件（如 Codex / OpenAI / OpenAI-compatible 导出的会话配置）是否仍然可用。

### 功能
- 检查 JSON 结构是否正常
- 解码 JWT payload（不校验签名）
- 检查 `exp` / `expired` 是否过期
- 支持在线探测接口有效性
- 支持脱敏输出，方便安全分享报告
- 支持三分类：
  - `valid`
  - `no_quota`
  - `invalid`
- 支持把三类配置分别保存到不同目录
- 自动生成 `index.json`

### 推荐用法
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

### 输出结果
运行后通常会得到：

```text
valid_configs/
no_quota_configs/
invalid_configs/
report.txt
index.json
```

### 适用场景
- 检查 Codex 导出的 JSON 配置是否有效
- 批量扫描一整个目录下的 auth/token 文件
- 自动分离有效配置、无额度配置、失效配置
- 生成可分享的脱敏排查报告

### 注意事项
- 这些配置文件非常敏感，请勿随意分享原始文件。
- 调试时建议优先使用增强版，并开启脱敏输出。
- 默认探测地址使用 OpenAI 官方接口；如果你使用私有中转或自定义面板，请手动传入你自己的 `--probe-url`。

---

## English

A utility skill for validating token/auth JSON files such as Codex/OpenAI/OpenAI-compatible exported session configs.

### Features
- Validate JSON structure
- Decode JWT payloads without signature verification
- Check expiry fields such as `exp` and `expired`
- Support online probing against a validation endpoint
- Generate redacted output for safer sharing
- Classify configs into:
  - `valid`
  - `no_quota`
  - `invalid`
- Save each class into separate directories
- Generate `index.json`

### Recommended usage
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

### Typical output
```text
valid_configs/
no_quota_configs/
invalid_configs/
report.txt
index.json
```

### Good fit for
- Verifying exported Codex/OpenAI-style session JSON files
- Batch scanning a directory of auth/token files
- Separating usable configs from revoked ones
- Producing safe redacted reports for debugging

### Notes
- These files are highly sensitive. Do not share raw configs.
- Prefer the enhanced script with redacted reporting when debugging.
- Default probe target uses the OpenAI official endpoint; if you use a private relay or custom panel, pass your own `--probe-url` explicitly.
