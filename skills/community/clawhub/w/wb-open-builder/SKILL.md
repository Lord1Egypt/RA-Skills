---
name: wb-open-builder
display_name: 开放平台资产构建器
display_name_en: Open Platform Asset Builder
description: 生成符合 WorkBuddy 开放平台规范的技能、连接器、专家、专家团与 Buddy 应用资产包，内置字段级规范、校验脚本与打包提交指引。触发词：开放平台、生成技能、生成连接器、生成专家、生成专家团、Buddy应用、上架、资产包、wb-open-builder、meta-skill-system
description_zh: 生成符合 WorkBuddy 开放平台规范的技能、连接器、专家、专家团与 Buddy 应用，内置字段级规范校验与打包提交指引
description_en: Generate WorkBuddy open-platform compliant skills, connectors, experts, expert teams and Buddy apps with field-level spec validation and submission guidance
category: development       # 对应技能市场分类「开发工具」；英文枚举官方未公开，此为推断值，创建技能时以平台分类下拉为准
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.0.0
disable-model-invocation: false
user-invocable: true
author: 王教成 Wang Jiaocheng (波动几何)
---

# 开放平台资产构建器

## 定位

本技能是「WorkBuddy 开放平台资产生成」领域的领域负载物，负责把"将能力发布到开放平台"的需求，端到端转化为符合平台规范的资产包——技能（Skill）、连接器（Connector）、专家（Expert）、专家团（Expert Team）、Buddy 应用——并完成字段级校验、打包与提交指引。

依赖声明：本技能仅依赖自身 references/ 下的三层结构文件与通用任务执行能力（三轴正交框架），不依赖任何其他领域技能。规范来源为 WorkBuddy 开放平台官方文档 https://open.workbuddy.cn/docs（2026-09 抓取）；平台规范更新时，以官方文档为准，按「负载物深化」流程更新 references/ 后重新校验。

## 核心能力

1. **需求与路由**：收集资产需求，按能力形态判定资产类型，规划生成方案（D0）
2. **技能生成**：生成符合开放平台技能规范的 SKILL.md + references/scripts/templates 资产包（D1）
3. **连接器生成**：在 MCP+Skill 与 CLI+Skill 两种接入方式中判定并生成 connector-meta.json、mcp.json/cli.json、图标与配套 Skill（D2）
4. **专家生成**：生成含 plugin.json、Agent 定义、头像与依赖声明的单专家包（D3）
5. **专家团生成**：设计主理人+成员分工与 SOP，生成团队 plugin.json、主理人与成员 Agent 定义（D4）
6. **Buddy 应用生成**：按 5 个配置模块产出应用配置内容与预览调试清单（D5）
7. **校验与交付**：执行 scripts/validate_asset.py 字段级校验，输出打包与提交审核指引（D6）

## 三层结构

```
wb-open-builder/
├── SKILL.md                                   # 本文件：路由 + 执行框架接口 + 域概览
├── references/                                # 参考文档（加载到上下文）
│   ├── wb-open-builder-catalog.md             #   任务清单 + 依赖拓扑
│   ├── wb-open-builder-requirements.md        #   任务要求清单（含全类型字段级规范）
│   ├── wb-open-builder-exemplars.md           #   范本索引 + 范本标准格式
│   ├── WB00~WB06-*.md                         #   各域具体范本（一域一本，编号对齐域号，与索引同级存放）
├── scripts/                                   # 可执行脚本（直接执行，不加载）
│   └── validate_asset.py                      #   资产包字段级规范校验
└── templates/                                 # 输出资源（按需引用，不加载全文）
    ├── README.md                              #   资源清单与使用方式
    ├── skill-SKILL-template.md                #   技能 SKILL.md 模板
    ├── expert-plugin.json-template.json       #   专家 plugin.json 模板
    ├── team-plugin.json-template.json         #   专家团 plugin.json 模板
    ├── connector-meta.json-template.json      #   连接器元信息模板
    ├── mcp.json-template.json                 #   MCP 接入配置模板
    ├── cli.json-template.json                 #   CLI 接入配置模板
    └── buddy-app-config-checklist.md          #   Buddy 应用五模块配置清单
```

**目录硬约束（平台实测）**：Skill 包仅支持两级目录结构（根目录/二级目录/文件），references/、scripts/、templates/ 内不得再建子目录；本技能自身结构即按此约束组织（范本与索引文件同级存放，原 references/exemplars/ 子目录已取消）。

信息优先放在 references/ 中；scripts/ 由 Bash/命令行直接执行；templates/ 模板含占位符，按需复制填充。

## 使用规则

### 执行流程
1. **首次加载**：读取 `references/wb-open-builder-catalog.md`，获取域分类、依赖拓扑与元操作映射提示
2. **按需深入**：确认资产类型后，读取 `references/wb-open-builder-requirements.md` 对应域的字段级规范；需要模仿产出时读取 `references/wb-open-builder-exemplars.md` 及对应范本子文件
3. **生成执行**：按 catalog 依赖拓扑编排管线逐任务执行；结构类文件优先从 templates/ 模板填充
4. **交付前校验**：运行 `python scripts/validate_asset.py <资产包目录> --type <skill|connector|expert|team>`，FAIL 项修正后复检，全部通过再进入打包提交

### 内容权限
5. **修改权限**：本技能 references/ 内容按领域负载物规范维护；平台规范变更时先更新 references/ 对应域的规范表，再同步更新范本与校验脚本，保持三者一致
6. **用户补充**：用户可提供已上架成功的真实资产包作为补充范本（脱敏后与范本索引文件同级放入 references/，保持两级目录约束）

### 降级模式

| 模式 | 权限 |
|------|------|
| 标准模式 | 读写目标目录、执行 scripts/、生成全部资产文件、运行校验 |
| 只读模式 | 仅读取与校验（D6-01）、输出校验报告与修改建议，不写入任何文件 |
| 禁写模式 | 无法落盘时，将全部生成内容以代码块形式输出，由用户手动保存为对应文件 |

### 提示词导出
7. 可将本技能合并为单一提示词文件用于不支持 skill 目录格式的工具。合并顺序：SKILL.md → wb-open-builder-catalog.md → wb-open-builder-requirements.md → wb-open-builder-exemplars.md → references/ 下各范本文件（按编号 WB00→WB06）。命令示例：`cat SKILL.md references/wb-open-builder-catalog.md references/wb-open-builder-requirements.md references/wb-open-builder-exemplars.md references/WB0*.md > wb-open-builder-prompt.md`

## 与执行框架的接口

本技能通过以下五步接入通用任务执行框架（三轴正交），任何生成/校验请求都从 Step 0 进入：

- **Step 0 三轴判定**：复杂度（单类型生成=中等；多类型或含专家团=复杂）、内容类型（结构化资产包）、创新需求（默认无需创新，按规范执行；命名/文案可少量创造）
- **Step 1 领域校准**：按本领域 R1-R5 参数校准执行（见下）
- **Step 2 三轴分解**：执行轴按 catalog 依赖拓扑分解为 D0→Dx→D6 管线；内容轴对文案类组件（描述、示例、SOP）启用清单法；创新轴默认关闭
- **Step 3 管线编排与执行**：五类资产生成域内部任务可并行的标记并行（如 D4-03/D4-04）；每个生成任务完成后立即做基元内分步校准（对照 requirements 字段表逐项核对）
- **Step 4 整合交付**：运行校验脚本 → 输出校验报告 → 打包 → 给出提交审核指引

**Step 1 领域校准的领域特定推导**：

| 参数 | 本领域取值 | 执行影响 |
|------|-----------|---------|
| R1 信息密度 | 高（字段表、JSON 结构、路径约定密集） | S/C 权重高：生成前必须先核对 requirements 字段表，禁止凭记忆写结构 |
| R2 创造性 | 中（提示词正文、描述文案、SOP 可创造；结构零创造） | A 权重中：结构类组件走模板填充，文案类组件走清单法 |
| R3 交互性 | 中（需求收集、类型确认需用户输入；生成过程可自治） | I 权重中：D0 域必须向用户确认类型与关键信息后才进入生成 |
| R4 规范性 | 极高（平台审核硬约束，字段错即解析失败） | G 权重最高：D6-01 校验为强制门禁，FAIL 不交付；安全红线（禁止硬编码凭证）零容忍 |
| R5 迭代性 | 中高（生成→校验→修正循环） | 校验 FAIL 项回到对应生成任务修正后复检，循环直至全 PASS |

**自治度**：结构生成⬛全自动、文案生成🟨半自动（关键文案向用户确认）、提交审核⬜人工（需用户操作开放平台）。

## 通用任务执行能力

**三轴正交**：执行轴（How，必选）+ 内容轴（What，按需）+ 创新轴（Why Different，按需）。

**执行轴**：6 大元操作 S 感知（采集需求、读取规范）/ C 认知（类型判定、方案规划、校准）/ A 行动（生成文件、打包）/ O 组织（目录结构、归档）/ I 交互（需求确认、提交指引）/ G 守护（规范校验、安全审计）；6 种编排模式：顺序→、并行‖、条件?、循环↻、扇出⇉、扇入⇇；7 种通用管线模式 P1 基础闭环 / P2 迭代精炼 / P3 并行汇聚 / P4 条件分支 / P5 交互驱动 / P6 全守护 / P7 发散收敛。本领域默认管线：P4 条件分支（类型判定后进入对应生成域）嵌套 P2 迭代精炼（校验循环）。

**内容轴**：清单法（结构类文件 = 字段清单逐项填充）+ 样本法（文案类组件模仿 references/ 下 WB00~WB06 范本的结构与风格，不复制内容）。

**创新轴**：默认关闭；仅在用户对命名、人设、SOP 提出差异化要求时启用，创新后仍须通过 D6-01 规范校验。

**三轴协同**：顺序协同（判定→分解→生成→校验）为默认；多成员 Agent 生成时启用并行协同；校验 FAIL 时启用迭代协同（G 发现问题 → 回到对应 A 任务修正）。

**核心公式**：产出 = 元操作（S/C/A/O/I/G 管线）× 本负载物（references/ 字段级规范 + templates/ 模板 + WB 系列范本）。

## 域概览

按生成流程组织，共 7 域 24 种资产构建任务：

| 域 | 任务数 | 典型任务 |
|----|--------|---------|
| D0 需求与路由域 | 3 | 需求信息收集、资产类型判定、生成方案规划 |
| D1 技能生成域 | 4 | 目录结构生成、SKILL.md 生成、子资源生成、技能打包 |
| D2 连接器生成域 | 4 | 接入方式判定、元信息与图标生成、连接配置生成、配套 Skill 生成 |
| D3 专家生成域 | 4 | 专家包结构生成、plugin.json 生成、Agent 定义生成、依赖声明生成 |
| D4 专家团生成域 | 4 | 团队角色设计、团队 plugin.json 生成、主理人 Agent 生成、成员 Agent 生成 |
| D5 Buddy应用生成域 | 3 | 应用基础配置、首页与市场配置、其他配置与预览 |
| D6 校验与交付域 | 2 | 规范校验、打包与提交指引 |

**域间逻辑流**：D0 → D1/D2/D3/D4/D5（按类型条件分支）→ D6（扇入）。

完整任务清单与依赖拓扑见 `references/wb-open-builder-catalog.md`；全类型字段级规范见 `references/wb-open-builder-requirements.md`；可模仿范本见 `references/wb-open-builder-exemplars.md`。

**扩展类型说明**：开放平台另支持「外部应用接入」（OAuth 2.1 + Open API，涉及 access_token 24h / refresh_token 60d / Scope 最小权限申请）。该类型为平台网页配置 + 服务端开发，不走资产包上传；用户提出时按 requirements D0-02 的要点级指引处理，并引导查阅官方文档 /docs/third-party-app。

## 事实纪律

1. 仅使用本技能 references/ 中确知的规范字段与取值，不得编造字段名、枚举值或目录约定；规范未覆盖处标注"以开放平台官方文档为准"
2. 字段级生成必须对照 requirements 对应域的字段表逐项核对，不得凭记忆输出结构
3. 任何文件中不得写入真实 Token、密钥、内部地址；占位符统一使用 `${VAR_NAME}` 形式
4. 中英文字段（displayName、description 等）必须成对提供；中文展示描述遵守平台字数要求
5. 校验未全部通过不得进入打包提交；平台解析失败时按 requirements 各域"解析失败排查"节定位
6. 样本法模仿范本时仅借鉴结构与风格，不复制范本的业务内容
