# se-semantic-graph — 软件工程语义图谱

把经典软件工程的**全知识域**落进 axolotl 图库，修 bug / 加功能 / 重构时沿跨域语义边**定向查询精确上下文**，根治上下文爆炸与注意力分散。

## 为什么需要它

编程中反复调试修改的根因，往往不是"不会写"，而是**上下文爆炸 + 注意力分散**：
修 bug 时看不到这段代码服务于什么需求、为什么存在、当初为什么这么设计。
大部分程序员/agent 用最新模型、最大上下文硬扛——这是错误的方向。
图库提供的是**精确的、定向查询到的上下文**，而不是更大的上下文。

与 human-like-novel 写作技能同构：写作解决"长篇跨章一致性"（设定散落几十万字），
编程解决"跨代码库的功能-需求-约束一致性"（语义散落成千上万文件）。同一个病，同一副药。

## 核心设计

### 四域节点

| 域 | 类型 |
|---|---|
| 问题域 | persona 客户画像 / requirement 需求 / cost 成本约束 / business_rule 业务规则 |
| 方案域 | architecture 架构层 / module 模块 / interface 接口契约 / tech_stack 技术栈 |
| 实现域 | runtime_logic 运行逻辑 / data_flow 数据流 / data_model 数据模型 / function 函数锚点 |
| 决策域 | decision 历史决策 ADR / rejected 被否方案 |

### 跨域语义边（方向约定，勿反）

所有边统一方向 = **问题域 → 实现域**：

```
画像 → 需求 → 架构层 → 模块 → 运行逻辑 → 函数
  ↑drives   ↑mapped_to ↑part_of ↑implements ↑traced_to
成本/规则 → 需求（constrains）   决策 → 任意（affects）
```

- **修 bug 反向追溯（为什么做）** = `trace --direction up`（原生 `in_neighbors`）
- **加功能正向展开（影响什么）** = `trace --direction down`（原生 `out_neighbors`）

方向反了（如 serves 写成 模块→需求）会追溯断链——录入时严格照此约定。

## 安装

```bash
# 1. 前置：lobster-memory 引擎（含 axolotl_rs）
git clone https://github.com/LittleLollipop/lobster-memory.git
cd lobster-memory && bash install.sh

# 2. 图库需支持 in_neighbors（dev 分支已含，commit 84e91fe 起）
cd <axolotl>/prototype-rust
maturin build --release --features python-bindings -o target/wheels
pip install --force-reinstall --no-deps target/wheels/axolotl_rs-*.whl

# 3. 验证
python -c "import axolotl_rs; print('in_neighbors' in dir(axolotl_rs.AxolotlGraph))"  # True
```

## 使用

```bash
PY=<lobster-memory venv python>
RUN=~/path/to/se-semantic-graph/runner.py
export SE_SEMANTIC_DIR=<每个项目一个目录>

$PY $RUN init                                  # 初始化项目图
$PY $RUN add --id <id> --label <名> --type <类型> --summary <一句话> --source <来源>
$PY $RUN connect --from <id> --to <id> --kind <边类型>
$PY $RUN trace --start <id> --direction up --depth 4 --verbose   # 核心
$PY $RUN list --type <类型>
$PY $RUN stats
$PY $RUN types
```

节点/边类型清单：`$PY $RUN types`
录入模板：`templates/node-templates.md`

## 使用惯例

- **录入**：龙虾写码/改码时顺手更新语义节点；架构级决策由用户确认后落图。边写边录，图库是活的 traceability。
- **查询**：修 bug 前必查 `trace --direction up` 拿"为什么"链；影响面用 down 或 LSP。
- **只输出差异**：查询结果 = 与本次任务相关的上下文子图（字段级摘要），禁止全量 dump 图库给模型。

## 与 lobster-memory 的关系

- 底层共用 axolotl 图库（axolotl_rs），**不共用图文件**：lobster-memory 记对话记忆，本技能记项目语义。
- 语义边方向约定（问题域→实现域）是本技能特有设计。

## License

MIT © Sai (LittleLollipop)
