# 文件夹组织（阶段 0 详细）

> 适用于：知识库结构混乱、文件散落在根目录、需要多层结构整理。

## 0.1 三种"文件夹"操作

| 操作 | API | 效果 | 何时使用 |
|------|-----|------|---------|
| **创建文件夹** | `create_folder` | 在知识库根目录建一个新文件夹 | 建立分类骨架 |
| **虚拟归类** | `add_knowledge` | 让文件"看起来"在文件夹中（**parent_folder_id 不变**）| 临时展示 |
| **物理归类** | `move_knowledge` | 真正修改 `parent_folder_id` 为目标文件夹 | 真正整理 |

**关键警告**：
- `add_knowledge` 创建的是"虚拟关联"，**不改变 `parent_folder_id`**
- 仅用 `add_knowledge` 而不调用 `move_knowledge`，文件永远挂在根目录
- 根目录调用 `get_knowledge_list` 会返回所有文件（包括已"虚拟关联"的），但这不代表它们真正归属于文件夹

## 0.2 诊断流程

### 步骤 1：拉取知识库根目录

```bash
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/get_knowledge_list" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"knowledge_base_id": "<kb_id>", "limit": 50}'
```

### 步骤 2：识别散落文件

```python
ROOT_FOLDER_ID = "<知识库根目录 ID>"  # 通常通过 get_knowledge_base 获取

orphans = [f for f in root_items
           if f.get("media_type") != 99
           and f.get("parent_folder_id") == ROOT_FOLDER_ID]
```

### 步骤 3：递归扫描文件夹层级

对每个文件夹调用 `get_knowledge_list(folder_id=...)`，记录：
- 子文件夹（`media_type == 99`）
- 文件数
- 每个文件的 `parent_folder_id` 是否等于当前 `folder_id`

### 步骤 4：分类汇总

| 状态 | 含义 | 处理方式 |
|------|------|---------|
| 文件 `parent_folder_id` 是根目录 | 真正散落 | 用 `move_knowledge` 归类 |
| 文件 `parent_folder_id` 是文件夹 ID | 已归类 | 仅检查是否需要打标签 |
| 文件仅在根目录返回但 parent 是文件夹 | 虚拟关联 | 已正确处理 |

## 0.3 诊断输出模板

```markdown
## 知识库结构诊断报告

### 顶层文件夹
| 文件夹 | 文件数 | 含子文件夹 |
|--------|:------:|:----------:|
| ... | ... | ... |

### 散落文件
- 共 X 个文件 `parent_folder_id` 是根目录
- 列出每个文件的标题和推荐目标文件夹

### 多层结构
- AI 量化与深度学习/
  - 机器学习理论方法/（Y 个文件）
  - 大模型与智能体/（Y 个文件）
  - ...

### 处理建议
- 散落文件：调用 `move_knowledge` 归类
- 多层结构：导览放父级，子文件夹不需要各自导览
```

## 0.4 归类流程

### 步骤 1：列出待归类文件

```python
# 从诊断报告中获取散落文件
orphans = [(f["media_id"], f["title"]) for f in orphan_files]
```

### 步骤 2：推荐目标文件夹

关键词匹配模式（参考实战案例）：

| 关键词模式 | 推荐目标文件夹 |
|-----------|---------------|
| AkShare、BaoStock、OpenClaw、JQData、MooTdx、聚宽、a-stock-data、数据源、入门 | 数据工具与入门 |
| HFT、harris、Athena、净订单、信息差、微观结构、高频 | 高频交易与微观结构 |
| 情绪、a-share-sentiment | 金融情绪分析 |
| Fama-French、因子、融资融券、IF基差、基差、散户、定价、动量、反转、隔夜、华尔街 | 因子与资产定价 |
| Qlib、AI、Claude、智能体、遗传算法、深度学习、神经网络、图神经网络、LLM | AI 量化与深度学习（顶层）|
| 多层 AI 量化子文件夹 | 机器学习理论方法 / 大模型与智能体 / 深度学习与预测模型 |
| 其他（兜底） | 交易策略与系统 |

> 关键词表针对量化投资领域；其他领域需重新设计。

### 步骤 3：批量调用 `move_knowledge`

```bash
# 移动到目标文件夹（src_kb_id == dst_kb_id 表示知识库内移动）
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/move_knowledge" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{
    "src_knowledge_base_id": "<kb_id>",
    "dst_knowledge_base_id": "<kb_id>",
    "dst_folder_id": "<target_folder_id>",
    "dst_folder_name": "<target_folder_name>",
    "infos": [{"media_id": "<file1_media_id>"}, {"media_id": "<file2_media_id>"}]
  }'
```

**注意**：每次最多 10 个文件，分批调用。

### ⚠️ `move_knowledge` 的副作用

| 副作用 | 说明 |
|--------|------|
| `parent_folder_id` 改变 | ✅ 这是目标行为 |
| **文件标签可能丢失** | ⚠️ 移动前若有标签，先备份！|

**标签备份与恢复模式**：

```python
# 1. 移动前：备份标签
backup = {f["media_id"]: f.get("tags", []) for f in to_move_files}

# 2. 执行 move_knowledge
api_call("openapi/wiki/v1/move_knowledge", {...})

# 3. 移动后：恢复标签
for media_id, tags in backup.items():
    for tag in tags:
        tag_add(kb_id, media_id, real_title, tag)
```

### 步骤 4：验证归类效果

```python
# 验证根目录为空
root_items = get_knowledge_list(kb_id, limit=50)  # 不带 folder_id
remaining = [f for f in root_items if f.get("media_type") != 99]
assert len(remaining) == 0, f"根目录仍有 {len(remaining)} 个散落文件"

# 验证每个文件夹的文件数符合预期
```

## 0.5 多层结构设计原则

- **导览放父级**：父文件夹放主题导览，子文件夹**不需要**各自的导览
- **MECE 划分**：子文件夹之间互斥、覆盖完整
- **层级不超过 3 层**：超过 3 层说明分类需要重新设计
- **避免"其他"类子文件夹**：用语义命名而非兜底类

## 0.6 文件夹层级模式

**模式 A：扁平**（推荐用于中等规模）

```
知识库根
├── 文件夹 1
├── 文件夹 2
└── 文件夹 3
```

**模式 B：2 层嵌套**（推荐用于复杂领域）

```
知识库根
├── 文件夹 1
├── 文件夹 2（复杂主题）
│   ├── 子文件夹 A
│   ├── 子文件夹 B
│   └── 子文件夹 C
└── 文件夹 3
```

## 0.7 与标签的协同

| 维度 | 文件夹 | 标签 |
|------|:---:|:---:|
| 主导维度 | 主题分类 | 多维关联 |
| 结构 | 树状（一文件一父） | 网状（一文件多标签）|
| 人类友好 | 高（导览） | 低（API）|
| 机器友好 | 低 | 高 |
| 一致性要求 | 文件归属唯一 | 一文件多标签 |
| 创建方式 | 必须事先规划 | 可渐进添加 |

**核心原则**：文件夹负责"内容组织"，标签负责"维度标记"，二者互为补充。

## 0.8 实战案例

详见 [cases/quantitative-investing.md](cases/quantitative-investing.md)

## 0.9 与 `add_knowledge` 的对比使用场景

| 场景 | 用什么 API |
|------|----------|
| 临时把笔记"展示"在文件夹中 | `add_knowledge` |
| 把已有文件真正归类 | `move_knowledge` |
| 新建文件时指定归属 | `add_knowledge`（创建时即关联）|
| 把根目录散落文件归位 | `move_knowledge` |
| 调整多层结构 | `move_knowledge` |
