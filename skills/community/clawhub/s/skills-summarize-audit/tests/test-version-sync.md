# 测试：版本号同步

> 验证所有版本源统一为同一版本号，避免安装/运行时显示不一致。

## 输入

读取以下文件的首个版本号：

- `VERSION`
- `SKILL.md` 正文 Version 行
- `README.md` 标题/徽章/changelog
- `CHANGELOG.md` 首个条目
- `references/skill-registry.yaml` 中 `skills-summarize-audit` 条目

## 预期输出

所有来源版本号一致，例如 `6.4.0`。

## 验证标准

| 来源 | 当前版本 |
|:-----|:---------|
| VERSION | 6.4.0 |
| SKILL.md | 6.4.0 |
| README.md | 6.4.0 |
| CHANGELOG.md | 6.4.0 |
| skill-registry.yaml | 6.4.0 |

若任一来源不一致，验证失败。

## 执行方式

```bash
python tests/validate.py
```
