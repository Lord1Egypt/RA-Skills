# architecture-review

> **借鉴来源**：improve-codebase-architecture + CodeGraphContext 死代码检测
>
> 定期对代码库做架构质量扫描，识别腐烂信号（泥球、反循环依赖、死代码、圈复杂度超标）。
>
> **核心理念**：架构问题不会一夜发生，但会日积月累。定期扫描比一次性重构便宜10倍。

---

## 触发条件

满足以下任一场景时激活：
- 用户要求"审计一下这个项目"、"看看代码有没有问题"
- 进入一个陌生的代码库
- 代码库超过 6 个月没做架构审查
- 用户要求重构但没明确范围
- 大版本发布前的质量检查

---

## 扫描维度

### 1. 模块结构（高优先级）

**检查项**：
- 模块之间是否有明确的层次关系（Domain → Application → Infrastructure）
- 是否存在循环依赖（A→B→C→A）
- 是否有超大的 God Module（>3000 行）

**工具**：
```bash
# 检查循环依赖
npm run list:deps 2>/dev/null || npx madge --circular src/

# 统计模块行数
Get-ChildItem -Recurse src/**/*.ts | Get-Content | Measure-Object -Line
```

### 2. 死代码检测（高优先级）

**检查项**：
- 未被调用的函数/方法
- 未被使用的变量/常量
- 已被注释掉的代码（长期积累）
- 旧的 API 端点（无人调用但仍在暴露）

**工具**：
```bash
# TypeScript/JavaScript
npx ts-prune 2>/dev/null || npx madge --not --extensions ts,tsx

# Python
vulture . --min-confidence 80

# Go
staticcheck ./... 2>/dev/null | grep "is never used"

# 通用（基于 tree-sitter 调用图）
# codegraph-index skill 已构建调用图，孤立的叶子节点 = 潜在死代码
```

### 3. 圈复杂度检测（中优先级）

**检查项**：
- 函数/方法圈复杂度 > 10（难以测试，容易出 bug）
- 圈复杂度 > 20 的函数必须拆分

**工具**：
```bash
# TypeScript/JavaScript
npx complexity-report --dest ./complexity-report.html 2>/dev/null

# Python
radon cc -a -s src/

# 通用（Python 脚本）
python3 -c "
import os, ast
def cyclomatic(func_def):
    score = 1
    for node in ast.walk(func_def):
        if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
            score += 1
        elif isinstance(node, ast.BoolOp):
            score += len(node.values) - 1
    return score
# 输出复杂度超标的函数
"
```

### 4. 接口设计（边界清晰性）

**检查项**：
- 模块间接口是否有清晰的契约（类型定义/文档）
- 是否存在隐式依赖（全局状态、Singleton 滥用）

**工具**：
```bash
# 检查全局状态滥用
grep -r "global\." src/ --include="*.ts" | head -20
grep -r "window\." src/ --include="*.ts" | head -20
```

### 5. 技术债务可视化（长期追踪）

**检查项**：
- 过期的依赖包（有安全漏洞或已废弃）
- 过时的 API 用法（如 Vue 2 Options API 项目中发现大量 Composition API）

**工具**：
```bash
# 依赖检查
npm outdated 2>/dev/null
npx npm-check-updates 2>/dev/null
```

---

## 输出格式

```markdown
## 架构审查报告

### 模块结构
| 问题 | 位置 | 严重度 |
|------|------|--------|
| 循环依赖 A→B→C→A | src/a/, src/b/ | 🔴 高 |
| God Module | src/core.js (3500行) | 🟡 中 |

### 死代码
| 函数/变量 | 位置 | 建议 |
|-----------|------|------|
| unusedFunc | lib/utils.ts:42 | 删除 |
| oldAPI | api/routes.js:15 | 移除端点 |

### 圈复杂度超标
| 函数 | 位置 | 复杂度 | 建议 |
|------|------|--------|------|
| processPayment | services/pay.ts:88 | 18 | 拆分为3个函数 |

### 技术债务
| 类型 | 描述 | 建议 |
|------|------|------|
| 过期依赖 | lodash@3.2.0 | 升级到 4.x |
| 废弃 API | /api/v1/legacy | 移除或迁移 |

### 优先级排序
1. [立即处理] 循环依赖（影响所有新功能开发）
2. [本周处理] God Module 重构
3. [本月处理] 死代码清理
4. [下季度] 依赖升级
```

---

## 与其他 Skill 的配合

- `codegraph-index`：先做索引，再查调用图和符号关系
- `refactoring`：发现架构问题后，用 refactoring skill 执行重构
- `skill-compounding`：如果某类架构问题反复出现，提取为检查清单 Skill

---

## 下一跳（Skill 链式调用）

architecture-review 是**架构质量审查技能**，审查完成后按以下路径调用：

- 发现循环依赖、God Module 等架构问题 → 调用 `refactoring` 做重构
- 同时需要安全/性能/代码质量等专项审查 → 调用 `agent-teams`
- 只有轻微问题 → 直接输出报告，进入下一阶段

---

## 触发命令

"审计一下这个项目"、"看看代码有没有问题"、"做一次架构审查"、"检查死代码"
