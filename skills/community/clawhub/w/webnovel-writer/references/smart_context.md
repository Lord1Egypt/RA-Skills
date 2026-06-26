# 上下文智能路由机制

> 在 `context_loader.md` 的分层加载基础上，增加**标签索引 + 上下文路由器**，让 agent 在写作每章时精准定位需要加载的设定条目，而不是靠 grep 模糊搜索。

## 一、问题定义

### 1.1 实际信息量（两部小说实测）

| 小说 | 设定集 | 设定词典 | 大纲 | 追踪表 | 合计 |
|------|--------|----------|------|--------|------|
| 我的死亡日期消失了 | ~17KB | ~5KB | ~20KB | ~8KB | ~50KB |
| 观众都是我的前世 | ~15KB | ~3KB | ~67KB | ~10KB | ~95KB |

即使按 context_loader.md 的压缩策略降到 12KB，仍有优化空间：很多章节不需要加载全部 L0 内容，而 grep 搜索容易遗漏。

### 1.2 核心矛盾

- **设定条目之间有隐性关联**：提到"永盛"就会涉及"孙磊""陈永生""八楼""三月周期"，但 grep "永盛" 不会自动带出这些关联
- **不同章节需要不同的设定组合**：第 14 章需要出差记录相关设定，第 35 章需要异常员工相关设定
- **角色在不同卷的设定侧重不同**：赵恒在第 1 卷只是搭档，第 10 卷揭示系统身份

## 二、设定标签索引

### 2.1 索引文件规范

每部小说维护一个 `设定索引.json`，放在项目根目录。结构：

```json
{
  "meta": {
    "novel": "我的死亡日期消失了",
    "last_updated": "2026-04-10",
    "total_entries": 42
  },
  "entries": [
    {
      "id": "E001",
      "name": "永盛集团",
      "type": "location",
      "tags": ["永盛", "公司", "江城", "孙磊", "陈永生", "十二楼", "八楼", "三月"],
      "file": "设定集.md",
      "section": "### 永盛集团",
      "line_start": 85,
      "line_end": 110,
      "volume_range": [1, 20],
      "priority": "always"
    },
    {
      "id": "C001",
      "name": "陆远",
      "type": "character",
      "tags": ["陆远", "主角", "余额", "观察者", "投行", "迈凯轮"],
      "file": "设定集.md",
      "section": "### 陆远",
      "line_start": 20,
      "line_end": 60,
      "volume_range": [1, 20],
      "priority": "always"
    },
    {
      "id": "S001",
      "name": "寿命交易系统",
      "type": "worldbuilding",
      "tags": ["系统", "余额", "交易", "归零", "暂停", "清算", "观察者", "陆承平"],
      "file": "设定集.md",
      "section": "### 寿命余额系统",
      "line_start": 200,
      "line_end": 260,
      "volume_range": [1, 20],
      "priority": "on-demand"
    },
    {
      "id": "P001",
      "name": "三月周期规律",
      "type": "plot_mechanism",
      "tags": ["三月", "周期", "入职", "陈永生", "忌日", "孙磊", "张维", "周志远"],
      "file": "写作追踪表.md",
      "section": "三个异常员工共同特征",
      "line_start": 180,
      "line_end": 190,
      "volume_range": [1, 5],
      "priority": "on-demand"
    }
  ],
  "tag_groups": {
    "永盛线": ["永盛", "孙磊", "张维", "周志远", "八楼", "十二楼", "三月", "陈永生"],
    "系统线": ["系统", "余额", "交易", "归零", "观察者", "陆承平", "赵恒"],
    "情感线": ["沈清", "告白", "决裂", "信任", "老钱", "张敏"],
    "职场线": ["投行", "尽调", "合伙人", "周雅", "王建国"]
  }
}
```

### 2.2 条目类型（type）

| type | 说明 | 压缩策略 |
|------|------|----------|
| `character` | 角色档案 | 按出场压缩为摘要 |
| `location` | 场景设定 | 按涉及场景加载描写 |
| `worldbuilding` | 世界观规则 | 按关键词触发加载 |
| `plot_mechanism` | 剧情机制/规律 | 按剧情阶段触发 |
| `relationship` | 角色关系 | 按出场角色组合加载 |
| `item` | 道具/物品 | 按提及加载 |
| `timeline` | 时间线事件 | 按章节范围加载 |

### 2.3 优先级（priority）

| priority | 含义 | 写入上下文包规则 |
|----------|------|------------------|
| `always` | 每章必带 | 全量或压缩后加载 |
| `high` | 经常需要 | 写作卡匹配到标签时加载 |
| `on-demand` | 特定场景才需要 | 写作卡精确匹配时加载 |
| `rare` | 极少需要 | 仅全量检查时加载 |

### 2.4 关联标签组（tag_groups）

`tag_groups` 定义标签之间的关联关系。当写作卡命中某标签时，同组的其他标签也会被激活。

**路由规则**：命中 tag_groups 中任一标签 → 该组所有标签对应的条目进入候选加载列表。

## 三、上下文路由器

### 3.1 路由流程

```
写作卡 → 关键词提取 → 标签匹配 → tag_groups 扩展 → 优先级过滤 → 去重 → 生成加载清单 → 按行号读取
```

### 3.2 关键词提取规则

从写作卡中提取以下维度并映射到标签：

| 提取维度 | 正则模式示例 | 映射到 tags |
|----------|-------------|-------------|
| 角色名 | `陆远\|沈清\|赵恒\|老钱\|孙磊\|方哲` | 直接匹配 |
| 场地名 | `永盛\|投行\|金库\|别墅\|面馆` | 直接匹配 |
| 机制词 | `余额\|交易\|归零\|暂停\|观察\|清算` | 直接匹配 |
| 情节词 | `调查\|发现\|见面\|决裂\|告白\|死亡` | 映射到 tag_groups |
| 物品词 | `迈凯轮\|签名\|死亡证明\|笔记本` | 直接匹配 |

### 3.3 路由算法（伪代码）

```python
def route_context(writing_card, index):
    # 1. 提取关键词
    keywords = extract_keywords(writing_card)
    
    # 2. 直接标签匹配
    matched_entries = set()
    for entry in index.entries:
        if any(kw in entry.tags for kw in keywords):
            matched_entries.add(entry.id)
    
    # 3. tag_groups 扩展
    expanded_tags = set()
    for group_name, group_tags in index.tag_groups.items():
        if any(kw in group_tags for kw in keywords):
            expanded_tags.update(group_tags)
    
    for entry in index.entries:
        if any(tag in entry.tags for tag in expanded_tags):
            matched_entries.add(entry.id)
    
    # 4. 加入 always 优先级条目
    for entry in index.entries:
        if entry.priority == "always":
            matched_entries.add(entry.id)
    
    # 5. 按 priority 排序 + 容量控制
    entries = sorted(
        [e for e in index.entries if e.id in matched_entries],
        key=lambda e: {"always": 0, "high": 1, "on-demand": 2, "rare": 3}[e.priority]
    )
    
    # 6. 容量限制（总加载量 ≤ 15KB）
    total_size = 0
    load_list = []
    for entry in entries:
        size = (entry.line_end - entry.line_start) * 30  # 估算：每行约30字节
        if total_size + size <= 15360:
            load_list.append(entry)
            total_size += size
        elif entry.priority == "always":
            # always 条目超限也要压缩加载
            load_list.append(entry)
    
    return load_list
```

### 3.4 路由结果示例

**输入**：第 35 章写作卡「分析三个异常员工共同特征→全部三月入职→3月15日关联→永盛是系统性问题」

**路由结果**：

| 条目ID | 名称 | 优先级 | 加载方式 |
|--------|------|--------|----------|
| C001 | 陆远 | always | 摘要 |
| C003 | 赵恒 | always | 摘要 |
| E001 | 永盛集团 | always | 场景描写 |
| P001 | 三月周期规律 | on-demand→命中 | 全量 |
| C010 | 孙磊 | high→命中 | 摘要 |
| C011 | 张维 | high→命中 | 摘要 |
| C012 | 周志远 | high→命中 | 摘要 |
| S001 | 寿命交易系统 | on-demand→命中 | 相关规则 |

**不加载**：方哲档案（第 4 卷才出场）、沈清档案（本章不出场）、地下金库场景（本章不去）。

## 四、索引维护规范

### 4.1 初始化

新小说项目创建时，agent 执行：

1. 读取设定集、设定词典、大纲
2. 为每个角色、场景、世界观条目创建索引条目
3. 基于大纲为每个条目分配 volume_range
4. 根据出场频率分配 priority
5. 构建 tag_groups

### 4.2 增量更新

每章写完后检查：

- **新增角色** → 添加 character 条目
- **新增场景** → 添加 location 条目
- **新揭示设定** → 添加 worldbuilding 条目 + 更新相关 tags
- **角色状态变化** → 更新 priority（如从 on-demand 升为 high）
- **新剧情线开启** → 添加 plot_mechanism 条目 + 新 tag_group

### 4.3 维护命令

```bash
# 查看索引统计
cat 设定索引.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'条目数: {len(d[\"entries\"])}')"

# 搜索某标签关联的所有条目
cat 设定索引.json | python3 -c "
import json,sys
d=json.load(sys.stdin)
tag=sys.argv[1]
for e in d['entries']:
    if tag in e['tags']:
        print(f'{e[\"id\"]} {e[\"name\"]} ({e[\"priority\"]})')
" '永盛'
```

## 五、与 context_loader.md 的关系

| 方面 | context_loader.md | 本文档（smart_context.md） |
|------|-------------------|---------------------------|
| 分层策略 | L0-L3 四层加载 | 继承分层，增加标签索引 |
| 角色加载 | grep 角色名 → read | 标签匹配 → 精确行号读取 |
| 大纲加载 | 按卷 grep | 同（大纲不适合标签化，按卷读取即可） |
| 关联发现 | 无 | tag_groups 自动扩展关联条目 |
| 容量控制 | 估算 12KB | 精确到条目级别的容量控制 |
| 维护成本 | 低（纯策略文档） | 中（需要维护设定索引文件） |

**建议**：简单项目（< 200 章）用 context_loader.md 的 grep 策略即可；复杂项目（200+ 章、多线并进）启用本文档的标签索引路由。

## 六、实战操作步骤

写作第 N 章时的完整操作序列：

```
1. 读取写作卡（从大纲提取本章要点）
2. 如果存在 设定索引.json → 执行路由算法
   如果不存在 → 回退到 context_loader.md 的 grep 策略
3. 加载 L0 必带项（硬性规则 + 设定词典 + 近5章摘要 + 上章尾部）
4. 根据路由结果加载 L1-L3 条目（按行号精确读取）
5. 组装上下文包
6. 开始写作
```

**不需要每次都运行路由算法**：如果连续几章出场角色和场景相似（常见），可以复用上一章的路由结果，只做增量调整。
