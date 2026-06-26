# 示例代码片段

## PowerShell转义语法示例

对于参数中的单引号，使用转义语法：
```powershell
# 错误：I'm Groot
# 正确：'I'\''m Groot'

# 或者如果可能，使用双引号：
"I'm Groot"
```

## 检查清单项目结构示例

### 正确的项目格式：
```markdown
- [ ] CHK001 - Are the exact number and layout of featured episodes specified? [Completeness, Spec §FR-001]
- [ ] CHK002 - Are hover state requirements consistently defined for all interactive elements? [Consistency, Spec §FR-003]
- [ ] CHK003 - Is the selection criteria for related episodes documented? [Gap, Spec §FR-005]
```

### 项目组成要素：
1. **复选框**：`- [ ]`
2. **ID**：`CHK###`（从001开始顺序编号）
3. **问题格式**：询问需求质量的问题
4. **质量维度标签**：`[Completeness/Clarity/Consistency/etc.]`
5. **规范引用**：`[Spec §X.Y]`（当检查现有需求时）
6. **缺失标记**：`[Gap]`（当检查缺失需求时）

## 问题格式化规则

### 选项表格格式：
```markdown
| 选项 | 候选项 | 重要性 |
|------|--------|---------|
| A | 轻量级预提交检查 | 快速反馈，低摩擦 |
| B | 正式发布门控 | 高质量保证，正式流程 |
| C | PR审查辅助 | 协作改进，知识共享 |
```

### 限制：
- 最多A-E选项
- 如果自由形式答案更清晰，则省略表格
- 绝不要要求用户重述他们已经说过的内容
- 避免推测类别（无幻觉）

## 默认值设置

当交互不可能时：
- **深度**：标准
- **受众**：如果与代码相关则为审查者（PR）；否则为作者
- **焦点**：前2个相关聚类