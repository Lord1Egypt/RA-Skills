## REA2-追踪与取证域范本

### 范本概述

覆盖 REA2-01~REA2-04 的产物样式：静态分析执行记录、追踪记录、证据台账、运行时观察记录。核心是「证据引用」的写法，以「Electron 应用离线搜索」为目标贯穿示例。

### 范本正文

**【REA2-01 静态分析执行】执行记录样例**：

```markdown
## 执行记录
- 工具 ／ 命令：analyze_javascript_application（detail: summary） ／ analyze-javascript-application {{应用路径}} --format json
- 输出：已保存至 {{evidence/app-summary.json}}；MCP 通道以父证据 {{parent_evidence_id}} 复用同一份证据，CLI 通道以该文件作输入、用 inspect-analysis-view 分页复读
- 初步读解：模块 {{N}} 个；与搜索相关的候选：{{search/index.js、main.js 的 search:run 通道}}
- 限制：{{动态加载模块未覆盖，标注为未知}}
```

**【REA2-02 线索追踪】追踪记录样例（单问题闭环）**：

```markdown
## 追踪记录：查询路径
- 种子：IPC 通道 "search:run"（来源：preload 暴露的桥接）
- 追踪（出向）：renderer 调用点 → preload 桥接 → 主进程 handler
- 结论（观察）：handler 调用查询解析后访问本地索引；索引由 {{index 模块}} 构建
- 证据引用：{{ev_xxx（模块详情）}}；{{文件偏移/行号}}
- 推断（标注）：索引疑似 SQLite 格式（依据：{{依赖与文件特征}}），未经运行验证
- 新增未决项：{{索引重建的触发时机}}
```

**【REA2-03 证据登记与未决项管理】证据台账样例**：

```markdown
## 证据台账
| # | 结论 | 证据引用 | 置信度 | 类型 |
|---|---|---|---|---|
| 1 | 搜索经 IPC 通道 search:run | ev_xxx / node_id=xxx | observed | 静态 |
| 2 | 索引疑似 SQLite | ev_xxx（依赖特征） | derived | 推断 |

## 未决项
- U1：索引重建的触发时机 → 需要 {{运行时观察或初始化路径证据}}
- 维护方式：record_unknown / update_unknown 逐条登记 ／ 无对应命令，本台账由文件承载（建议 evidence/ledger.md）
```

**【REA2-04 运行时观察（按需）】观察记录样例**：

```markdown
## 运行时观察记录
- 高风险确认：已向用户复述「将启动目标应用并以用户权限捕获初始化调用」并获确认（{{时间}}）
- 观察结果：{{启动时调用索引重建；无网络请求}}
- 副作用说明：{{仅读取本地文件，未修改任何文件}}
- 结论更新：U1 关闭（证据 ev_yyy，运行时）；结论 2 升级为 observed
```

### 结构要点标注

1. 每条追踪结论必须带证据引用与「观察/推断」标注；推断必须给出依据。
2. 台账粒度是「一条结论一行」；未决项写清所需证据类型。台账优先落盘而非留在会话记忆里——CLI 通道无 `record_unknown` / `update_unknown`，未决项必须以文件形式存在（建议 `evidence/ledger.md`），否则收尾时无处归档。
3. REA2-04 必须先有确认记录（复述动作与权限），再执行；结果同样登记进台账。
4. 同证据引用复用，不重复执行同一分析。
5. CLI 通道的 `analyze-javascript-application` 无 `detail` 参数：概要须由 `inspect-analysis-view` 分页取得（按 `coverage.next_offset` 推进），不得假定 CLI 直接返回已裁剪结果；`parent_evidence_id` 亦为 MCP 专有，CLI 以证据文件路径充当引用。

### 替换清单

目标名/通道名/模块名/证据 ID 替换为真实值；限制说明按实际 limitations 改写；调用链按实际追踪结果重写。
