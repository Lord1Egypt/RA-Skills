"""se-semantic-graph schema: 软件工程语义图谱的节点/边类型定义。

四域划分（经典软件工程）：
- 问题域：客户画像 / 需求 / 成本约束 / 业务规则
- 方案域：架构层 / 模块 / 接口契约 / 技术栈
- 实现域：模块运行逻辑 / 数据流 / 数据模型 / 函数锚点
- 决策域：历史决策 ADR / 被否方案

核心：跨域语义边（traceability），图库价值=边定向遍历+字段级提取+只输出差异。
"""

# ── 节点类型（type 字段）───────────────────────────────

# 问题域
TYPE_PERSONA = "persona"              # 客户画像
TYPE_REQUIREMENT = "requirement"      # 需求（功能/非功能）
TYPE_COST = "cost"                    # 成本约束（预算/时间线/ROI）
TYPE_BUSINESS_RULE = "business_rule"  # 业务规则

# 方案域
TYPE_ARCHITECTURE = "architecture"    # 架构层（分层架构中的一层）
TYPE_MODULE = "module"                # 模块
TYPE_INTERFACE = "interface"          # 接口契约
TYPE_TECH_STACK = "tech_stack"        # 技术栈选择

# 实现域
TYPE_RUNTIME_LOGIC = "runtime_logic"  # 模块运行逻辑（状态机/关键路径）
TYPE_DATA_FLOW = "data_flow"          # 数据流
TYPE_DATA_MODEL = "data_model"        # 数据模型
TYPE_FUNCTION = "function"            # 函数锚点（挂到运行逻辑/模块）

# 决策域
TYPE_DECISION = "decision"            # 历史决策 ADR
TYPE_REJECTED = "rejected"            # 被否方案

NODE_TYPES = {
    TYPE_PERSONA: "客户画像",
    TYPE_REQUIREMENT: "需求",
    TYPE_COST: "成本约束",
    TYPE_BUSINESS_RULE: "业务规则",
    TYPE_ARCHITECTURE: "架构层",
    TYPE_MODULE: "模块",
    TYPE_INTERFACE: "接口契约",
    TYPE_TECH_STACK: "技术栈",
    TYPE_RUNTIME_LOGIC: "运行逻辑",
    TYPE_DATA_FLOW: "数据流",
    TYPE_DATA_MODEL: "数据模型",
    TYPE_FUNCTION: "函数",
    TYPE_DECISION: "历史决策",
    TYPE_REJECTED: "被否方案",
}

# 域归属（用于按域过滤/统计）
DOMAIN_OF_TYPE = {
    TYPE_PERSONA: "problem",
    TYPE_REQUIREMENT: "problem",
    TYPE_COST: "problem",
    TYPE_BUSINESS_RULE: "problem",
    TYPE_ARCHITECTURE: "solution",
    TYPE_MODULE: "solution",
    TYPE_INTERFACE: "solution",
    TYPE_TECH_STACK: "solution",
    TYPE_RUNTIME_LOGIC: "implementation",
    TYPE_DATA_FLOW: "implementation",
    TYPE_DATA_MODEL: "implementation",
    TYPE_FUNCTION: "implementation",
    TYPE_DECISION: "decision",
    TYPE_REJECTED: "decision",
}

# ── 边类型（kind 字段）─────────────────────────────────
#
# ⚠️ 方向约定（核心，勿反）：
#   所有语义边统一方向 = 问题域 → 实现域（from 在上游，to 在下游）：
#     画像 → 需求 → 架构层 → 模块 → 运行逻辑 → 函数
#   这样「修 bug 反向追溯（为什么做）」= 沿边反向 = 原生 in_neighbors；
#    「加功能正向展开（影响什么）」= 沿边正向 = 原生 out_neighbors。
#   反了方向的边（如 serves 写成 模块→需求）会导致追溯断链。

# 问题域内部 / 问题→方案
KIND_DRIVES = "drives"                # 客户画像 → 需求（画像驱动需求）
KIND_CONSTRAINS = "constrains"        # 成本/业务规则 → 需求（约束）
# 方案域
KIND_MAPPED_TO = "mapped_to"          # 需求 → 架构层（需求落在哪层）
KIND_PART_OF = "part_of"              # 架构层 → 模块（模块归属层）
KIND_DEPENDS_ON = "depends_on"        # 模块 → 模块（依赖）
# 方案→实现
KIND_SERVES = "serves"                # 需求 → 模块（需求由哪些模块服务）
KIND_IMPLEMENTS = "implements"        # 模块 → 运行逻辑（模块承载逻辑）
# 实现内部
KIND_TRACED_TO = "traced_to"          # 运行逻辑 → 函数（函数对应逻辑）
KIND_FLOWS = "flows"                  # 数据流相关
# 决策贯穿（决策属上游，指向被影响的下游）
KIND_AFFECTS = "affects"              # 决策 → 任意（决策影响）
KIND_REJECTS = "rejects"              # 决策 → 被否方案（被否）

EDGE_KINDS = {
    KIND_DRIVES: "画像驱动需求",
    KIND_CONSTRAINS: "约束",
    KIND_MAPPED_TO: "映射到",
    KIND_PART_OF: "归属",
    KIND_DEPENDS_ON: "依赖",
    KIND_SERVES: "服务",
    KIND_IMPLEMENTS: "实现",
    KIND_TRACED_TO: "追溯到",
    KIND_FLOWS: "流转",
    KIND_AFFECTS: "影响",
    KIND_REJECTS: "否决",
}

# 查询语义：反向追溯时这些 kind 表示"向问题域走"（读 why）
# 统一方向（问题域→实现域）后，up=in_neighbors 天然覆盖全部语义边，
# 无需逐 kind 判断；此集合仅用于文档说明。
WHY_EDGES_UP = {
    KIND_TRACED_TO,   # 逻辑 → 函数（反向=逻辑由哪些函数实现）
    KIND_IMPLEMENTS,  # 模块 → 逻辑
    KIND_SERVES,      # 需求 → 模块
    KIND_MAPPED_TO,   # 需求 → 层
    KIND_PART_OF,     # 层 → 模块
    KIND_DRIVES,      # 画像 → 需求
    KIND_AFFECTS,     # 决策 → 任意
}

# 默认 field 规范：每个节点只存摘要级字段，不 dump 源码/全文
NODE_FIELDS = {
    "id": "稳定标识符（英文/拼音，无空格）",
    "label": "可读名称",
    "type": "节点类型（见上）",
    "summary": "一句话摘要（≤200字，字段级提取的关键）",
    "detail_ref": "详细文档/源码位置引用（不存全文）",
    "source": "来源（需求文档/issue/PR/会议/对话）",
}

# 写入时必填的最小字段
REQUIRED_FIELDS = ["id", "label", "type", "summary"]
