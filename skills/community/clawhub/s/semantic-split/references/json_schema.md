# JSON 结构规范

> **加载时机**：生成或更新能力级/规则级 json 时加载

---

## 一、层级关系

```
              ┌─────────────────────────────┐
              │        规则级 json           │  ← 上层抽象
              │  • 粒度粗，覆盖一类任务      │
              │  • 由能力级凝练/统合生成      │
              │  • 内嵌 capability_refs[]    │
              └──────────┬──────────────────┘
                         │ 引用 / 渐进加载
            ┌────────────┼────────────┐
            ▼            ▼            ▼
    ┌──────────┐  ┌──────────┐  ┌──────────┐
    │能力级json│  │能力级json│  │能力级json│  ← 原子单元
    └──────────┘  └──────────┘  └──────────┘
```

**规则级 > 能力级**：规则级是上层抽象，能力级是原子单元。

---

## 二、能力级 json（原子单元）

### 生成时机

仅当规则级和能力级均不命中时，经模型思考生成步骤并**执行完成后**，才生成新能力级 json。

### 通用化规则

**通用化 ≠ 抽象提炼**，而是**字段替换**——用占位符替换具体信息，保留步骤结构和粒度。

| 原始具体内容 | 通用化后 |
|---|---|
| `"介绍钛合金马扎产品"` | `"介绍[产品名称]"` |
| `"收集钛合金材料参数"` | `"收集[产品核心参数]"` |
| `"明天下午3点前交付"` | `"在[截止时间]前交付"` |
| `"导出为微信公众号格式"` | `"导出为[目标格式/平台]"` |

**原则**：
- 保留步骤粒度（细节步骤**不**合并）
- 只替换「值」，不改变「结构」
- 步骤数量、并行关系、milestone 标记全部保留
- 文件名格式：`{动词}_{对象类型}_v{n}.json`

### 数据结构

```json
{
  "id": "make_product_ppt_v1",
  "type": "capability",
  "name": "制作产品介绍PPT",
  "version": "1.0.0",
  "created_at": "2026-05-22",
  "description": "从零制作一份产品介绍PPT的完整步骤，通用化版本",
  "generic_params": ["[产品名称]", "[核心参数]", "[截止时间]", "[目标格式]", "[目标受众]"],
  "steps": [
    {
      "id": "s1",
      "name": "收集资料",
      "action": "搜索/整理[产品名称]相关资料和[核心参数]",
      "parallel_group": null,
      "milestone": true,
      "dependency_heat": 0,
      "depends_on": [],
      "constraint_level": "none",
      "source": "focus"
    },
    {
      "id": "s2",
      "name": "设计大纲",
      "action": "根据资料设计PPT结构与章节",
      "parallel_group": null,
      "milestone": true,
      "dependency_heat": 9,
      "depends_on": ["s1"],
      "constraint_level": "none",
      "source": "focus"
    },
    {
      "id": "s3a",
      "name": "制作内容页",
      "action": "填充正文幻灯片内容",
      "parallel_group": "pg1",
      "milestone": false,
      "dependency_heat": 8,
      "depends_on": ["s2"],
      "constraint_level": "none",
      "source": "focus"
    },
    {
      "id": "s3b",
      "name": "设计视觉风格",
      "action": "确定配色/字体/模板风格",
      "parallel_group": "pg1",
      "milestone": false,
      "dependency_heat": 5,
      "depends_on": ["s2"],
      "constraint_level": "soft",
      "source": "focus"
    },
    {
      "id": "s3c",
      "name": "AI生成备选视觉方案",
      "action": "用AI工具生成3个不同风格的视觉草稿供选择",
      "parallel_group": "pg1",
      "milestone": false,
      "dependency_heat": 4,
      "depends_on": ["s2"],
      "constraint_level": "none",
      "source": "divergent_enhanced"
    },
    {
      "id": "s4",
      "name": "审核修改",
      "action": "检查内容准确性与视觉一致性",
      "parallel_group": null,
      "milestone": true,
      "dependency_heat": 7,
      "depends_on": ["s3a", "s3b"]
    },
    {
      "id": "s5",
      "name": "导出PPT",
      "action": "导出为[目标格式]",
      "parallel_group": null,
      "milestone": false,
      "dependency_heat": 3,
      "depends_on": ["s4"]
    }
  ],
  "tags": ["ppt", "内容制作", "产品介绍"]
}
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|:----:|------|
| `id` | ✅ | 唯一标识，格式 `{动词}_{对象}_v{版本}` |
| `type` | ✅ | 固定为 `"capability"` |
| `name` | ✅ | 人类可读名称 |
| `version` | ✅ | 语义化版本号 |
| `created_at` | ✅ | 创建日期 |
| `description` | ✅ | 能力描述 |
| `generic_params` | ✅ | 通用化参数占位符列表 |
| `steps` | ✅ | 步骤数组（见下方） |
| `tags` | ✅ | 标签，用于归类 |

**steps 子字段**：

| 字段 | 必填 | 说明 |
|------|:----:|------|
| `id` | ✅ | 步骤唯一标识（如 `s1`, `s3a`） |
| `name` | ✅ | 步骤名称 |
| `action` | ✅ | 具体操作描述（含通用化占位符） |
| `parallel_group` | ✅ | 并行组标识，`null` 表示串行 |
| `milestone` | ✅ | 是否为里程碑步骤 |
| `dependency_heat` | ✅ | 关联热度 0-10 |
| `depends_on` | ✅ | 依赖的前置步骤 id 数组 |
| `constraint_level` | ❌ | 约束强度：`critical` / `soft` / `none`，对应🔴🟡⚪ |
| `source` | ❌ | 步骤来源：`focus` / `divergent_enhanced`，聚焦步骤可不填（默认 focus） |

---

## 三、规则级 json（统合上层）

### 生成时机

同类能力级 json **≥ 5 份** 后，通过定时任务/自动化/用户主动要求凝练生成。

### 数据结构

```json
{
  "id": "rule_ppt_v1",
  "type": "rule",
  "name": "PPT类任务规则",
  "version": "1.0.0",
  "created_at": "2026-05-22",
  "description": "统合所有PPT相关能力级json，提炼核心思考链",
  "source_capability_count": 5,
  "capability_refs": [
    { "id": "make_product_ppt_v1", "name": "制作产品介绍PPT" },
    { "id": "make_tech_ppt_v1",    "name": "制作技术方案PPT" },
    { "id": "design_slide_v1",     "name": "设计幻灯片" },
    { "id": "export_ppt_v1",       "name": "导出PPT" },
    { "id": "review_ppt_v1",       "name": "审核PPT" }
  ],
  "condensed_steps": [
    {
      "id": "r1",
      "name": "资料与大纲",
      "milestone": true,
      "parallel_group": null,
      "maps_to": ["make_product_ppt_v1.s1", "make_product_ppt_v1.s2"],
      "load_capability_if_detail_needed": "make_product_ppt_v1"
    },
    {
      "id": "r2",
      "name": "制作与设计（可并行）",
      "milestone": false,
      "parallel_group": "rp1",
      "maps_to": ["make_product_ppt_v1.s3a", "make_product_ppt_v1.s3b"],
      "load_capability_if_detail_needed": "design_slide_v1"
    },
    {
      "id": "r3",
      "name": "审核与导出",
      "milestone": true,
      "parallel_group": null,
      "maps_to": ["make_product_ppt_v1.s4", "make_product_ppt_v1.s5"],
      "load_capability_if_detail_needed": "export_ppt_v1"
    }
  ],
  "tags": ["ppt", "规则汇总"]
}
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|:----:|------|
| `id` | ✅ | 唯一标识，格式 `rule_{类别}_v{版本}` |
| `type` | ✅ | 固定为 `"rule"` |
| `name` | ✅ | 人类可读名称 |
| `version` | ✅ | 语义化版本号 |
| `created_at` | ✅ | 创建日期 |
| `description` | ✅ | 规则描述 |
| `source_capability_count` | ✅ | 来源能力级 json 数量 |
| `capability_refs` | ✅ | 来源能力级引用数组（id + name） |
| `condensed_steps` | ✅ | 压缩步骤数组（见下方） |
| `tags` | ✅ | 标签 |

**condensed_steps 子字段**：

| 字段 | 必填 | 说明 |
|------|:----:|------|
| `id` | ✅ | 步骤唯一标识 |
| `name` | ✅ | 步骤名称 |
| `milestone` | ✅ | 是否为里程碑 |
| `parallel_group` | ✅ | 并行组标识，`null` 表示串行 |
| `maps_to` | ✅ | 映射到哪些能力级的具体步骤（格式：`{能力级id}.{步骤id}`） |
| `load_capability_if_detail_needed` | ✅ | 需要细节时加载的能力级 json id |

---

## 五、脚本辅助操作

> 以下操作可通过 `scripts/json_manager.py` 自动化完成，AI 调用时优先使用脚本而非手动 Read/Write。

### 5.1 扫描匹配

```bash
# 按关键词搜索 json 库（规则级 + 能力级）
python scripts/json_manager.py scan --keywords ppt 制作 --top 5
# 输出: 匹配的 json 列表，含分数、类型、文件路径
```

### 5.2 归类统计

```bash
# 统计所有能力级 json 的 tag 分布，判断是否达到规则级阈值
python scripts/json_manager.py categorize --threshold 5
# 输出: 各 tag 分组及数量，ready_for_rule 标识
```

### 5.3 通用化（字段替换）

```bash
# params 模式：AI 决定替换映射，脚本执行替换
python scripts/json_manager.py generalize \
  --input ~/.workbuddy/skills/.standardization/semantic-split/data/capabilities/xxx_concrete.json \
  --params "钛合金马扎=[产品名称]" "材料参数=[核心参数]" "明天=[截止时间]" \
  --output ~/.workbuddy/skills/.standardization/semantic-split/data/capabilities/xxx_v1.json

# auto 模式：仅收集已有的中括号占位符（不替换）
python scripts/json_manager.py generalize --input xxx.json --auto
```

### 5.4 规则级生成

```bash
# 按标签自动选取同类能力级 json 生成规则级
python scripts/json_manager.py rule-gen --tag ppt --output rule_ppt_v1.json

# 指定多个文件生成
python scripts/json_manager.py rule-gen --files a.json b.json c.json
```

### 5.5 创建与验证

```bash
# 创建骨架文件
python scripts/json_manager.py create --type capability --name make_report_v1

# 验证格式
python scripts/json_manager.py validate --file ~/.workbuddy/skills/.standardization/semantic-split/data/capabilities/make_report_v1.json
```

---

## 四、JSON 存储结构

```
skills/.standardization/semantic-split/data/    ← 铁律4：产出物不嵌入技能目录
├── capabilities/                     # 能力级 json 存储目录
│   ├── make_product_ppt_v1.json
│   └── ...
└── rules/                            # 规则级 json 存储目录
    ├── rule_ppt_v1.json
    ├── rule_report_v1.json
    └── ...
```
