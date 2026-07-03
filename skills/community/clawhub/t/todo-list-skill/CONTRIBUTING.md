# CONTRIBUTING — todo-list Skill

> 版本：v1.5 | 日期：2026-06-11

---

## 开发规范

### 代码规范

| 规范 | 要求 |
|------|------|
| 风格 | PEP 8（用 `black` 格式化） |
| 类型提示 | 函数参数 + 返回值必须有 type hint |
| 文档字符串 | 所有公共方法必须有 docstring |
| 异常处理 | 捕获具体异常，不 bare except |
| SQL | 参数化查询，禁止字符串拼接 |

### Git 提交规范

```bash
# 格式：<type>(<scope>): <subject>
# 示例：
feat(store): add restore method
fix(nl_parser): handle empty string
docs(readme): add FAQ section
test(store): add test for ambiguous done

# type：
# feat / fix / docs / style / refactor / test / chore
```

### 测试规范

```bash
# 所有代码变更必须附带测试
# 运行全部测试
python -m pytest tests/ -v

# 带覆盖率
python -m pytest tests/ --cov=src --cov-report=term-missing

# 单个模块
python -m pytest tests/test_store.py -v
```

### 审查清单（PR 前必须）

- [ ] 所有新增方法有 docstring
- [ ] 所有新增方法有单元测试
- [ ] 边界用例测试通过
- [ ] `python -m pytest tests/ -v` 全通过
- [ ] `black src/ tests/` 格式化通过
- [ ] CHANGELOG.md 已更新
- [ ] 文档（SKILL.md/README.md/DESIGN.md）已更新（如需）
- [ ] SECURITY.md 已更新（如有安全相关变更）

---

## 文档更新规范

| 文档 | 更新时机 |
|------|----------|
| CHANGELOG.md | 每次发布新版本 |
| SKILL.md | 功能变更、错误处理变更 |
| README.md | 用户-facing 功能变更 |
| DESIGN.md | 架构、接口、算法变更 |
| SECURITY.md | 依赖变更、权限变更 |
| manifest.yaml | 版本号更新 |

---

## 问题反馈

### 使用 Issue Template

发现 bug 或有功能建议，请使用以下格式提交：

#### Bug 报告模板

```markdown
## 🐛 Bug 报告

**Skill 版本**：v1.5.0
**环境**：Python 3.8+ / QwenPaw latest
**优先级**：P1/P2/P3

### 问题描述
（简要描述 bug）

### 复现步骤
1. ...
2. ...
3. ...

### 预期行为
（应该是什么样）

### 实际行为
（实际是什么样）

### 错误日志
```
（粘贴相关日志）
```

### 截图（如有）
```

#### 功能建议模板

```markdown
## 💡 功能建议

**使用场景**：
（什么时候需要这个功能）

**期望行为**：
（希望怎么工作）

**当前 workaround**：
（现在怎么做的）

**优先级**：P1/P2/P3
```

---

## 代码审查清单（PR 前必填）

```markdown
- [ ] 新方法有 docstring
- [ ] 新方法有单元测试
- [ ] 边界用例测试通过
- [ ] pytest 全通过
- [ ] black 格式化通过
- [ ] CHANGELOG.md 已更新
- [ ] 相关文档已更新
- [ ] SECURITY.md 已更新（如有安全变更）
```

---

*本项目遵循 MIT 协议*