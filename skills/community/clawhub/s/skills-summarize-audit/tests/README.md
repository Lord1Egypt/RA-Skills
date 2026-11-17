# skills-summarize-audit 测试套件

> 自动化验证覆盖版本、YAML、评分、发布契约和平台配置；Markdown 用例补充流程验收。
> 每次修改后，先运行 `python tests/validate.py` 做自动化检查，再按 Markdown 套件逐项验证。

## 运行方式

```bash
# 自动化验证（推荐每次修改后执行）
python tests/validate.py

# 遍历所有 Markdown 测试
for f in tests/test-*.md; do echo "=== $f ==="; cat "$f"; done
```

## 测试列表

| 文件 | 验证目标 | 优先级 |
|:----|:---------|:------:|
| test-tier-classification.md | T1/T2/T3 分层 + T3 活性验证逻辑 | P0 |
| test-capacity-calculation.md | 多因子有效容量计算公式 | P0 |
| test-rollback-flow.md | ⑦-a 快照备份 + ⑦-d 回滚流程 | P0 |
| test-weight-sum.md | 8 维评分权重和 = 100% | P0 |
| test-yaml-parse.md | 所有 YAML 文件可解析 | P0 |
| test-version-sync.md | 版本号多源一致性 | P0 |
| test-platform-yaml.md | 平台配置不重复定义 scan_paths / trigger_words | P1 |
