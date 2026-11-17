# 测试：平台 YAML 合规性

> 验证平台配置文件只保留平台特征，不定义扫描路径和触发词。

## 输入

读取 `platforms/*.yaml`：

- `zcode.yaml`
- `claude.yaml`
- `codex.yaml`
- `cursor.yaml`
- `workbuddy.yaml`
- `default.yaml`

## 预期输出

- 所有文件可解析。
- 无 `scan_paths:` YAML 键。
- 无 `trigger_words:` YAML 键。
- 触发词权威来源注释完整。

## 验证标准

| 文件 | scan_paths | trigger_words | 未闭合引号 |
|:-----|:----------:|:-------------:|:----------:|
| zcode.yaml | ❌ | ❌ | ❌ |
| claude.yaml | ❌ | ❌ | ❌ |
| codex.yaml | ❌ | ❌ | ❌ |
| cursor.yaml | ❌ | ❌ | ❌ |
| workbuddy.yaml | ❌ | ❌ | ❌ |
| default.yaml | ❌ | ❌ | ❌ |

> `scan_paths` 和 `trigger_words` 的唯一来源为 `config.yaml` 和 `SKILL.md`。

## 执行方式

```bash
python tests/validate.py
```
