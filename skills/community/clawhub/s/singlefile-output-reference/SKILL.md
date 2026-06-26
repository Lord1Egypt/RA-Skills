---
name: singlefile-output-reference
author: 王教成 Wang Jiaocheng (波动几何)
description: 单文件产出知识参考库——Universal Task OS的领域负载物。提供单文件产出类型清单（8域37子分类188种产出类型）、结构要求槽位、可运行代码范本、选型决策树与管线蓝图，由UTOS执行轴动态编排管线、内容轴按清单法/样本法组织产出。四大家族：HTML单文件应用（PPT演示页/俄罗斯方块/数独/计算器/思维导图/白板/Mermaid编辑器）+ Python单文件CLI工具（argparse子命令/管道串联/stdlib only）+ Shell单文件脚本（Bash/PowerShell/系统运维/部署发布）+ SQL单文件脚本（DDL建表/DML数据操作/查询分析/迁移版本）。核心原则：自包含、零依赖、可直接运行、范本即代码、幂等性。触发词：HTML单文件、单文件应用、Python CLI、命令行工具、Shell脚本、Bash脚本、SQL脚本、建表脚本、argparse、幻灯片、PPT、游戏、俄罗斯方块、计算器、Mermaid、白板、single-file、CLI tool、argparse、self-contained、幂等、部署脚本。
---

# 单文件产出知识参考库

## 定位

本技能是 **Universal Task OS 的领域负载物仓库**，提供单文件产出（HTML单文件应用 / Python单文件CLI工具 / Shell单文件脚本 / SQL单文件脚本）的"是什么""长什么样"以及"怎么做"——执行全部委托UTOS。

| 本技能提供 | UTOS消费方式 |
|-----------|-------------|
| 产出类型清单（能做什么类型的单文件产物） | 内容轴·清单法的成品目录 |
| 结构要求（每种产物的组件槽位） | 内容轴·清单法的组件清单 |
| 优秀范本（可直接运行的完整代码） | 内容轴·样本法的样本 |
| 依赖拓扑（产物间组合关系） | 执行轴·管线编排的依赖输入 |
| 选型决策树（需求→产出类型路由） | 执行轴·管线编排的选型输入 |

## 三层结构

```
第一层：产出类型清单 + 依赖拓扑 + 选型决策树 + 管线蓝图（域特有扩展）   →  references/output-catalog.md
第二层：结构要求清单 + 自包含约束 + 组装流程 + 质量等级   →  references/structure-requirements.md
第三层：优秀范本库                                      →  references/exemplars.md
```

## 依赖声明

本技能**强依赖** Universal Task OS (universal-task-os)。没有UTOS，本技能只有参考查阅能力，无法执行任何代码产出任务。

**加载检查流程**（每次激活时执行）：

1. 检测 `universal-task-os` 技能是否已安装
2. **未安装** → 自动安装 `universal-task-os` 技能
3. **安装成功** → 同时加载UTOS，按本技能"使用规则"执行
4. **安装失败** → 降级为**只读参考模式**：
   - ✅ 允许：查阅产出类型、结构要求、范本索引
   - ❌ 拒绝：任何涉及代码生成、管线编排的任务，并提示"需先安装 Universal Task OS"

**任务模式判定**：

| 任务类型 | 无UTOS | 有UTOS |
|---------|--------|--------|
| 查阅产出类型/要求/范本 | ✅ 只读参考 | ✅ 完整 |
| 按清单/范本产出单文件代码 | ❌ 拒绝 | ✅ UTOS编排执行 |
| 多个单文件串联为工具链 | ❌ 拒绝 | ✅ UTOS执行轴 |
| 质量检查点插入 | ❌ 拒绝 | ✅ UTOS守护单元 |

## 使用规则

1. **依赖检查**：激活时按上述流程检测并安装UTOS
2. **首次加载**：读取 `references/output-catalog.md`，获取产出分类、依赖拓扑、选型决策树、UTOS元操作映射提示
3. **按需深入**：确认目标产出类型后，读取 `references/structure-requirements.md` 获取组件清单、自包含约束、组装流程、质量等级；如需样本法，读取 `references/exemplars.md` 获取可运行代码
4. **双模式路由**：
   - **目录模式**：用户指定具体产出类型(S-XX) → 直达structure-requirements组装 → 交付
   - **流程模式**：用户描述需求/问题 → output-catalog决策树选型 → structure-requirements组装 → 集成验证 → 交付
5. **委托UTOS**：将产出类型清单作为清单法输入、范本作为样本法输入、依赖拓扑+管线蓝图作为管线编排输入、决策树作为选型输入，交给UTOS执行轴+内容轴处理
6. **范本即代码**：本技能的exemplars是可直接运行/预览的完整代码文件，非文档描述

## 与UTOS的接口

当UTOS处理单文件产出任务时：

- **Step 0 三轴判定**：
  - 目录模式（用户指定S-XX）→ 简单+结构化 → 执行轴+内容轴
  - 流程模式（用户描述需求）→ 中等+结构化 → 执行轴+内容轴（走output-catalog决策树+structure-requirements组装流程）
  - 创新混搭（用户要新组合）→ 中等+创新+结构化 → 三轴全开
  - 管线组合（多产物串联）→ 复杂+结构化 → 执行轴+内容轴（依赖拓扑+管线蓝图推导）
  - 管线创新组合（跨家族桥接）→ 复杂+创新+结构化 → 三轴全开（管线蓝图+创新轴推导新组合）
- **Step 1 领域校准**：单文件产出=高规范性(R1)+高迭代性(R5) → G权重高（代码必须能运行），循环多（迭代调试），A权重高（直接产出代码）
- **Step 2 内容轴**：清单法用本技能的structure-requirements；样本法用本技能的exemplars（代码级样本）
- **Step 3 执行轴**：管线编排基于本技能的依赖拓扑自动推导元操作序列
- **Step 4 交付**：G类守护单元自动插入质量检查点（语法验证、功能测试、浏览器兼容性）

## 单文件产出的核心原则

### 自包含性（Self-Contained）

| 原则 | 说明 |
|------|------|
| **零外部依赖** | HTML文件不依赖CDN以外的资源（或CDN仅用允许的白名单）；Python脚本仅用标准库；Shell脚本仅用coreutils及常见系统工具；SQL脚本使用标准SQL优先 |
| **单一文件** | 所有HTML/CSS/JS内联在一个.html中；所有Python逻辑在一个.py中；所有Shell逻辑在一个.sh中；所有SQL逻辑在一个.sql中 |
| **可直接运行** | HTML双击即可在浏览器打开；Python `python file.py` 即可运行；Shell `./file.sh` 即可运行；SQL `psql/mysql/sqlite3 < file.sql` 即可执行 |
| **幂等性** | Shell脚本可重复执行不出错；SQL脚本含IF NOT EXISTS可重复执行；Python CLI含dry-run模式 |

### 四大家族

| 家族 | 说明 | 代表产出 |
|------|------|---------|
| **HTML单文件应用** | 内联CSS+JS的单一HTML文件，可在浏览器中直接运行 | PPT演示页、俄罗斯方块、数独、计算器、白板、Mermaid编辑器 |
| **Python单文件CLI** | 带argparse子命令的单文件脚本，无第三方依赖 | 文件处理工具、数据分析脚本、自动化批处理、API客户端 |
| **Shell单文件脚本** | Bash 4+/PowerShell 5.1+兼容的单文件脚本，零非系统依赖 | 系统初始化、备份恢复、构建部署、Git工作流 |
| **SQL单文件脚本** | 标准SQL优先、方言注释标注的单文件脚本，幂等可重复执行 | 建表脚本、批量导入、报表查询、Schema迁移 |

### 组合与扩展

单文件产出之间可以通过以下方式组合：

- **HTML嵌套**：一个HTML页面通过iframe嵌入另一个
- **Python子进程调用**：一个Python脚本的子命令调用另一个脚本
- **Shell管道串联**：多个Shell脚本通过Unix管道 `|` 串联
- **Shell→Python调用**：Shell脚本调用Python CLI工具
- **Shell→SQL执行**：Shell脚本通过mysql/psql/sqlite3执行SQL
- **SQL→Python桥接**：SQL查询结果导出CSV/JSON，Python读取处理
- **HTML→Python桥接**：HTML前端调用本地Python后端（通过简单HTTP或文件交换）

## 域概览

按产出功能类型组织，共8域37子分类188种产出类型：

| 域 | 子分类 | 产出数 | 典型产出 |
|----|--------|--------|---------|
| S1 演示展示 | A静态/B交互/C活动 | 20 | 幻灯片PPT、信息图、HTML邮件模板、音频可视化 |
| S2 游戏娱乐 | A休闲/B街机/C益智/D棋牌/E文字/F记忆/G放置 | 35 | 俄罗斯方块、数独、五子棋、飞翔小鸟、Cookie Clicker |
| S3 实用工具 | A文本/B计算/C安全/D效率/E开发/F格式 | 41 | 计算器、Markdown编辑器、白板、Mermaid编辑器、API Mock |
| S4 数据可视化 | A图表/B结构/C空间/D动态 | 18 | 图表仪表盘、思维导图、热力图、数据大屏、动态排名图 |
| S5 Python CLI | A文件/B数据/C网络/D生成/E运维 | 22 | 文件重命名、CSV处理、HTTP客户端、定时调度、系统信息 |
| S6 教学与交互 | A引导/B概念/C模拟/D测验 | 16 | 交互教程、算法可视化、状态机、闪卡记忆、代码调试 |
| S7 Shell脚本 | A运维/B文件/C部署/D开发 | 20 | 系统初始化、备份恢复、构建部署、项目脚手架、Git工作流 |
| S8 SQL脚本 | A结构定义/B数据操作/C查询分析/D迁移版本 | 16 | 建表脚本、批量导入、报表查询、递归查询、Schema迁移 |

完整清单见 `references/output-catalog.md`。
