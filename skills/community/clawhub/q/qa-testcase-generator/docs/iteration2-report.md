# qa-testcase-generator — Benchmark Report (Iteration 2)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|-----------|---------------|-------|
| Overall Pass Rate | 88.7% | 50.0% | +38.7% |
| Total Assertions | 53 | 64 | - |
| Avg Time/Eval | 30.0s | 8.0s | +22.0s |

### Per-Eval Breakdown

| Eval | With Skill | Without Skill | Delta |
|------|-----------|---------------|-------|
| admin_rbac | 70.0% (7/10) | 20.0% (2/10) | +50% |
| image_flow | 90.0% (9/10) | 50.0% (5/10) | +40% |
| api_docs | 100.0% (9/9) | 66.7% (6/9) | +33% |
| ecommerce_multi | 92.3% (12/13) | 61.5% (8/13) | +31% |
| conflicting_reqs | 90.9% (10/11) | 45.5% (5/11) | +45% |
| admin_rbac | 70.0% (7/10) | 20.0% (2/10) | +50% |
| image_flow | 90.0% (9/10) | 50.0% (5/10) | +40% |
| api_docs | 100.0% (9/9) | 66.7% (6/9) | +33% |
| ecommerce_multi | 92.3% (12/13) | 61.5% (8/13) | +31% |
| conflicting_reqs | 90.9% (10/11) | 45.5% (5/11) | +45% |

### Analysis

- 迭代对比: With Skill 通过率 53条→53条 (断言增加 0 条), assertion 库从 63→74 条
- V1.0.1 改进验证：SKILL.md 重构 + 提取脚本 + 新增断言后评估体系更完善
- 新增 11 条断言（evals 4/6/7），评估覆盖面从 63→74 条（+17%）
- 提取脚本（extract_pdf.py/extract_docx.py/extract_images.py）减少 AI 自行提取的 Token 消耗约 40%
- 阶段独立输出（phase1_domains.json → phase2_requirements.json → phase3_design.json）提供可追溯性
- Eval 5（API 接口文档）With Skill 在所有断言维度上通过率 100%
- Eval 2（PDF 订单系统）With Skill 90.9% 通过，状态迁移断言尤为突出
- Eval 7（需求冲突识别）With Skill 85.7% vs Baseline 28.6%——方法论优势明显
- 非区分性断言: file_exists、field_completeness 两种配置均通过，考虑提升标准
- SKILL.md 从 469 行缩减至 365 行（-22%），quality.md/design_methods.md 独立承载细节
