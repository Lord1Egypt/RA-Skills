# UTOS接口校验清单

生成的领域负载物技能必须通过以下21项逐条检查，确保与UTOS零冲突。每项标注 **PASS** / **FAIL** / **N/A**。

---

## A类：结构一致性（6项，全部必须PASS）

| # | 检查项 | 检查方法 | 通过标准 |
|---|--------|---------|---------|
| A1 | 三层结构存在 | 检查references/目录下是否有3个文件 + exemplars/子目录 | 必须有：catalog + requirements + exemplars主文件 + exemplars/子目录 |
| A2 | SKILL.md含依赖声明 | 检查SKILL.md是否含"依赖声明"章节 | 必须声明强依赖task-ops |
| A3 | 加载检查流程完整 | 检查是否有4步流程(检测→安装→加载→降级) | 4步缺一不可 |
| A4 | 降级模式定义 | 检查是否有只读模式的✅❌权限表 | 必须区分有Task Ops和无Task Ops两种模式 |
| A5 | 域间逻辑流声明 | catalog文件头部是否有域间逻辑流描述 | 必须→连接各域 |
| A6 | 依赖拓扑摘要 | catalog文件末尾是否有"依赖拓扑摘要"章节 | 必须有至少3条跨域管线链路 |

## B类：任务Schema完整性（5项，全部必须PASS）

| # | 检查项 | 检查方法 | 通过标准 |
|---|--------|---------|---------|
| B1 | 每个任务含5字段 | 随机抽查3-5个任务 | ID/名称/说明/依赖/UTOS映射提示 全部存在 |
| B2 | 依赖格式正确 | 检查所有任务的"依赖"列 | 格式为："无（入口）" 或 "X-XX"(有效ID) 或 "X-XX, Y-YY"(多依赖) |
| B3 | UTOS映射提示有效 | 检查映射提示值 | 仅允许：S/C/A/O/I/G 及其组合(→/‖) + 可选的A/G后缀 |
| B4 | 无孤立任务 | 检查每个非入口任务的前置依赖是否在catalog中存在 | 依赖ID必须指向已定义的任务 |
| B5 | 入口任务标识正确 | 标注"无（入口）"的任务确实是起始点 | 入口任务数应≥1且≤总任务数的30% |

## C类：结构要求槽位规范（4项，至少3项PASS）

| # | 检查项 | 检查方法 | 通过标准 |
|---|--------|---------|---------|
| C1 | 必选组件存在 | 每个任务必须有"必选组件"字段 | 100%覆盖率 |
| C2 | 组装顺序存在 | 每个任务必须有"组装顺序"字段 | ≥90%覆盖率（极简任务可省略） |
| C3 | 约束字段存在 | 每个任务必须有约束相关字段 | 命名为"合规约束"/"风格约束"/"质量约束"/"平台约束"等均可 |
| C4 | 格式字段存在 | 每个任务必须指定输出格式 | Markdown/Word/Excel/HTML/PDF/代码等 |

## D类：UTOS接口章节（3项，全部必须PASS）

| # | 检查项 | 检查方法 | 通过标准 |
|---|--------|---------|---------|
| D1 | "与Task Ops的接口"章节 | SKILL.md中是否存在此章节 | 必须存在 |
| D2 | Step 0-4覆盖 | 该章节是否覆盖Step 0到Step 4 | Step 0/1/2/3/4 全部有内容 |
| D3 | Step 1领域校准具体化 | Step 1是否包含R1-R5规则的领域特定推导 | 不能照抄通用模板，必须有该领域的具体参数 |

## E类：范本库规范（3项，至少2项PASS）

| # | 检查项 | 检查方法 | 通过标准 |
|---|--------|---------|---------|
| E1 | 范本清单表存在 | exemplars.md中是否有按域分组的范本清单表格 | 必须有按任务ID索引的范本表 |
| E2 | 范本子文件存在 | references/exemplars/目录下是否有.md文件 | 状态为"可用"的条目必须有对应子文件 |
| E3 | 范本模板格式存在 | 是否提供了子文件的标准化模板格式 | 供后续填充的结构模板 |

---

## 校验执行流程

```
生成技能文件
    ↓
┌─────────────┐
│ A类检查(6项)│ ← 结构一致性
│ 全部PASS?   │
└──────┬──────┘
       │ FAIL → 修正后重新检查
       │ PASS ↓
┌─────────────┐
│ B类检查(5项)│ ← 任务Schema
│ 全部PASS?   │
└──────┬──────┘
       │ FAIL → 补充缺失字段
       │ PASS ↓
┌─────────────┐
│ C类检查(4项)│ ← 槽位规范
│ ≥3 PASS?   │
└──────┬──────┘
       │ 不足 → 补充关键槽位
       │ OK   ↓
┌─────────────┐
│ D类检查(3项)│ ← UTOS接口
│ 全部PASS?   │
└──────┬──────┘
       │ FAIL → 重写接口章节
       │ PASS ↓
┌─────────────┐
│ E类检查(3项)│ ← 范本库
│ ≥2 PASS?   │
└──────┬──────┘
       │ 不足 → 创建空范本框架
       │ OK   ↓
    ✅ 校验通过，技能可用
```

## 常见FAIL原因与修正

| FAIL项 | 常见原因 | 修正方法 |
|--------|---------|---------|
| A2/A3 | SKILL.md直接复制了其他技能但忘了改领域名 | 全局搜索替换旧领域名为新域名 |
| B3 | UTOS映射写了中文而非S/C/A代码 | 统一为字母代号 |
| B4 | 引用了不存在的依赖任务ID | 检查catalog中是否有该ID，或删除无效引用 |
| D3 | Step 1照抄通用模板无领域特定内容 | 根据分析框架A-2的结果填充具体的R1-R5推导 |
| C1/C2 | requirements文件是空的或只有标题 | 至少为每个域的代表性任务填写一个完整槽位 |
| E2 | exemplars.md索引指向的子文件不存在 | 在references/exemplars/下创建对应文件，或在主文件中将状态改为"空" |

## 自动化校验提示

此校验清单可以转化为简单的脚本自动化：

```python
# 伪代码 - 校验逻辑示意
def validate_skill(skill_path):
    results = []
    # A类: 文件存在性 + 关键章节检测（含exemplars/子目录）
    results.append(check_A_files_exist(skill_path))
    results.append(check_A_dependency_section(skill_path))
    results.append(check_A_domain_flow(skill_path))
    # B类: Catalog表格解析 + Schema验证
    results.append(check_B_task_schema(skill_path))
    results.append(check_B_dependency_validity(skill_path))
    # C-E类: Requirements和Exemplars抽查
    results.append(check_C_requirements_coverage(skill_path))
    results.append(check_D_utos_interface(skill_path))
    results.append(check_E_exemplar_subfiles(skill_path))
    return generate_report(results)
```
