# QA Reviewer 工作流程

## 1. 项目启动阶段

### 1.1 需求评审
```bash
# 复制评审模板
cp ~/.openclaw/extensions/qa-reviewer/templates/code_review.md ./REVIEW.md

# 进行需求评审
vim ./REVIEW.md

# 提交评审报告
git add REVIEW.md
git commit -m "review: 需求评审报告"
```

### 1.2 任务清单检查
- [ ] P0 任务完整
- [ ] 验收标准明确
- [ ] 时间估算合理

## 2. 开发阶段

### 2.1 代码审查
```bash
# 运行代码审查
~/.openclaw/extensions/qa-reviewer/scripts/code_review.sh

# 查看报告
cat CODE_REVIEW_*.md
```

### 2.2 问题跟踪
```bash
# 更新 TODO.md
vim TODO.md

# 提交更新
git add TODO.md
git commit -m "docs: 更新 TODO 清单"
```

## 3. 测试阶段

### 3.1 单元测试
```bash
# 运行测试
~/.openclaw/extensions/qa-reviewer/scripts/run_tests.sh

# 查看结果
cat TEST_RESULT_*.md
```

### 3.2 生成报告
```bash
# 复制测试报告模板
cp ~/.openclaw/extensions/qa-reviewer/templates/test_report.md ./

# 填写报告
vim TEST_REPORT.md

# 提交报告
git add TEST_REPORT.md
git commit -m "test: 测试报告"
```

## 4. 验收阶段

### 4.1 验收检查
- [ ] 所有 P0 任务完成
- [ ] 测试全部通过
- [ ] 问题全部修复
- [ ] 文档齐全

### 4.2 验收报告
```markdown
# 验收报告

**验收时间**: YYYY-MM-DD  
**验收人**: [名字]

## 结果
- P0 完成度：100%
- 测试通过：✅
- 问题修复：✅

## 结论
✅ 验收通过
```

---

*最后更新：2026-03-04*
