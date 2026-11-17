# 测试：YAML 可解析性

> 验证所有 `.yaml` 配置文件语法正确，无未闭合引号、缩进错误等。

## 输入

扫描以下 YAML 文件：

- `config.yaml`
- `platforms/*.yaml`
- `references/project-types.yaml`

## 预期输出

所有文件被 `yaml.safe_load()` 成功解析，无异常。

## 验证标准

| 检查项 | 通过标准 |
|:-------|:---------|
| config.yaml | 可解析，`scan_paths` 为包含 4 个元素的列表 |
| platforms/zcode.yaml | 可解析，无未闭合 `"` |
| platforms/claude.yaml | 可解析，无未闭合 `"` |
| platforms/codex.yaml | 可解析，无未闭合 `"` |
| platforms/cursor.yaml | 可解析，无未闭合 `"` |
| platforms/default.yaml | 可解析，无 `scan_paths` 键 |
| platforms/workbuddy.yaml | 可解析，描述为 7 维 |
| references/project-types.yaml | 可解析，`requirements.txt` 模式结构正确 |

## 执行方式

```bash
python tests/validate.py
```
