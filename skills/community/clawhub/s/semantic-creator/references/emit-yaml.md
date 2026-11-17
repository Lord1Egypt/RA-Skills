# Phase 3 · Emit — repo-YAML（可选目标）+ 共享字段语义

输入：Phase 2 批准的建模决策集。产出：Kimball 星型/星座 YAML，三类文件：**catalog（薄路由）** → **shared-dimensions（一致性维度）** → **model（事实）**。本文件同时是两个目标共享的**字段语义定义**（OKF frontmatter 扩展键同源此处）。生成后跑 `verify.md`。

铁律：形态/路由/粒度 → 语义层；可键入或读取的取值（枚举、code、字段路径、命令）→ 契约层，语义层只指向。

## §1 `semantic_catalog`（路由，每 bundle 1 个）

```yaml
name: <PascalCaseName>
type: semantic_catalog
version: <semver>
domain: <snake_case_domain>
description: <一句话；薄路由，触发词/对话流不放这里>
entry_points:
  <entry_key>:                 # 按场景
    <axis>: <value>            # 可选路由轴（如 time）
    primary_facts: [<Fact>, ...]
    ontology_files: [<file>, ...]
command_contracts_file: <相对路径或 null>   # 指向契约层
```

约束：`name/type/domain/entry_points` 必填；每个 entry_point 至少 1 个 `ontology_files`；catalog 不得内联事实/维度定义，也不重复 model 已有的 operations/doc 出处（推导即可，避免第二真源）。

**多 bundle**：≥2 个 bundle 时在共同父目录生成薄 `index.yml`——每 bundle 一行（`domain / 一句 scope / catalog 路径`）；单 bundle 不生成。

## §2 `semantic_ontology` — shared dimensions（一致性维度，按需 1 个）

```yaml
name: <Name>
type: semantic_ontology
description: <共享维度集；被各 model 引用>
source_evidence: { <key>: <url> }     # 可选，证据出处
dimensions:
  - name: Dim_<Name>                  # PascalCase，以 Dim_ 前缀
    kind: <见 §4>
    business_key: <field>
    parent_dimension: <Dim_*>         # 仅 snowflake
    source_operations: [<Service/Operation>, ...]
    source_documents: [<url>, ...]    # 无 List API 时
    attributes: [<field>, ...]
    notes: <可选>
evidence_boundary: [<句>, ...]
```

## §3 `semantic_ontology` — model（事实，每个业务过程/计费模式 1 个）

```yaml
name: <Name>
type: semantic_ontology
description: <对齐哪个 operation 的哪段结构>
<axis>: <value>                       # 可选路由轴，与 catalog 对应
shared_dimensions_file: <相对路径>
facts:
  - name: <Fact>                      # PascalCase
    role: primary | child
    grain: <一句可证伪的粒度>
    parent_fact: <Fact>               # 仅 child
    child_facts: [<Fact>, ...]        # 仅 primary
    cardinality_max: <int>            # 可选
    degenerate_dimensions: [<field>, ...]
    dimensions: [Dim_<Name>, ...]     # 引用 §2/§4 的维度名
    attributes:
      - name: <field>
        type: string|integer|number|boolean|date|datetime
        dimension: Dim_<Name>         # 该列是某维度的外键时
        required: true | false | conditional
        condition: <when conditional>
        max_length: <int>             # 可选
        min: <n>; max: <n>            # 可选
        notes: <取值/枚举指向契约层>
    measures:
      - { name: <field>, additivity: additive|semi_additive|non_additive, unit: <或指向契约层>, notes: <basis> }
evidence_boundary: [<句>, ...]
```

约束：每个 fact 必有 `name/role/grain`；`child` 必有 `parent_fact`；`dimensions` 中每名必须在 shared-dimensions 或本文件可解析；可被键入/读取的枚举值不得写进 `attributes`（只在 `notes` 指向契约层）。

## §4 Dimension `kind` 取值

| kind | 用途 | 必填 |
| --- | --- | --- |
| `conformed_dimension` | 跨事实复用的一致性维度 | business_key, source_operations |
| `snowflake_dimension` | 规范化子维（挂在父维下） | business_key, parent_dimension |
| `degenerate`（不单列） | 事实里的裸键 | 记于 fact.degenerate_dimensions |
