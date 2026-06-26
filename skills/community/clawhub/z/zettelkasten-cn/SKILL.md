---
name: zettelkasten
description: 卢曼卡片学习法（Zettelkasten）全生命周期管理系统，支持九大人生领域分类、撤销操作、交互式创建流程。处理闪念笔记、文献笔记、永久笔记、项目笔记的增删改查，以及与Agent记忆系统的双向关联。
---

# 卢曼卡片学习法 (Zettelkasten)

基于卢曼卡片盒笔记法的个人知识管理系统，四级笔记流与九大人生领域分类深度整合，支持撤销操作和流程化卡片创建。

## 存储位置

卡片数据存储在：`~/Desktop/cardsdata/`

```
cardsdata/
├── inbox/              # 闪念笔记（临时，需定期清理）
├── lit/                # 文献笔记（阅读笔记）
├── zettel/             # 永久笔记（核心知识资产）
│   ├── 身心/            # 健康、心理、运动
│   ├── 学习/            # 学习方法、技能提升
│   ├── 投资/            # 理财、资产配置
│   ├── 家庭/            # 亲密关系、育儿
│   ├── 事业/            # 职业发展、工作
│   ├── 社交/            # 人际关系、沟通
│   ├── 物品/            # 物品管理、消费
│   ├── 爱好/            # 兴趣爱好
│   └── 体验/            # 旅行、美食、文化活动
├── project/            # 项目笔记
├── map/                # 索引/地图（MOC）
│   └── index.md        # 主索引（按九大领域组织）
├── attach/             # 附件
├── template/           # 本地模板
└── .system/            # 系统文件
    ├── trash/          # 回收站
    └── operation_history.json  # 操作历史（用于撤销）
```

## 四级笔记 + 九大领域

| 类型 | 目录 | 生命周期 | 用途 |
|------|------|---------|------|
| **闪念笔记** | `inbox/` | 1-2天 | 快速捕获想法 |
| **文献笔记** | `lit/` | 长期 | 读书笔记 |
| **永久笔记** | `zettel/分类/` | 永久 | 按九大领域组织的核心知识 |
| **项目笔记** | `project/` | 项目周期 | 特定项目相关 |

### 九大人生领域

1. **身心** - 健康、心理、运动、睡眠
2. **学习** - 学习方法、技能提升、知识管理
3. **投资** - 理财、资产配置、风险管理
4. **家庭** - 亲密关系、育儿、家务
5. **事业** - 职业发展、工作技能、创业
6. **社交** - 人际关系、沟通技巧、人脉
7. **物品** - 物品管理、消费决策、极简主义
8. **爱好** - 兴趣爱好、休闲活动
9. **体验** - 旅行、美食、文化活动

## 核心脚本

### 1. 基础管理脚本

**card_manager.py** - 卡片增删改查

```bash
cd /path/to/zettelkasten

# 创建笔记
python3 scripts/card_manager.py create fleeting "闪念标题" --content "内容"
python3 scripts/card_manager.py create permanent "笔记标题" --category 学习

# 查询
python3 scripts/card_manager.py list --type permanent
python3 scripts/card_manager.py search "关键词"
python3 scripts/card_manager.py read 20260301-0001

# 更新与删除
python3 scripts/card_manager.py update 20260301-0001 --content "新内容"
python3 scripts/card_manager.py delete 20260301-0001

# 链接笔记
python3 scripts/card_manager.py link 20260301-0001 20260301-0002 --type related

# 记忆关联
python3 scripts/card_manager.py memory add 20260301-0001 2026-03-01
python3 scripts/card_manager.py memory find 2026-03-01

# 转化闪念为永久
python3 scripts/card_manager.py convert 20260301-0001 --category 学习
```

### 2. 撤销管理脚本

**undo_manager.py** - 操作撤销

```bash
# 撤销最后一次操作
python3 scripts/undo_manager.py undo

# 列出最近的操作
python3 scripts/undo_manager.py list --limit 10

# 清空操作历史
python3 scripts/undo_manager.py clear
```

**支持的撤销操作**：
- ✅ 撤销创建（删除刚创建的卡片）
- ✅ 撤销删除（从回收站恢复）
- ✅ 撤销批量删除（批量恢复）
- ✅ 撤销更新（恢复更新前的内容）

**操作历史存储**：`~/.zettelkasten/memory/history.json`

### 3. 交互式创建脚本

**card_creator.py** - 流程化卡片创建

```bash
# 交互式创建（向导模式）
python3 scripts/card_creator.py

# 快速创建（非交互）
python3 scripts/card_creator.py --quick \
  --title "笔记标题" \
  --content "笔记内容" \
  --type permanent \
  --category 学习 \
  --memory 2026-03-01
```

**交互式流程**：
1. **输入阶段** - 选择类型、输入标题和内容、选择分类、添加标签、关联记忆
2. **处理阶段** - 验证输入、生成ID、渲染模板、写入文件、记录历史
3. **输出阶段** - 显示创建结果、提供后续操作建议

## 与记忆系统整合

### 卡片 → 记忆
```bash
# 创建时关联记忆
python3 scripts/card_manager.py create permanent "笔记标题" --category 学习 --memory 2026-03-01

# 事后添加记忆引用
python3 scripts/card_manager.py memory add 20260301-0001 2026-03-01 --context "讨论时产生"
```

### 记忆 → 卡片
```bash
# 查找某天关联的所有卡片
python3 scripts/card_manager.py memory find 2026-03-01
```

## 工作流程

### 日常捕获
```bash
# 方法1：使用基础脚本
python3 scripts/card_manager.py create fleeting "灵感" --content "详细内容"

# 方法2：使用交互式脚本（推荐）
python3 scripts/card_creator.py
```

### 定期整理
```bash
# 查看未处理的闪念
python3 scripts/card_manager.py list --type fleeting

# 有价值的转化为永久笔记
python3 scripts/card_manager.py convert 20260301-0001 --category 学习

# 如果转化错了，撤销
python3 scripts/undo_manager.py undo
```

### 分类浏览
打开 `~/Desktop/cardsdata/map/index.md`，按九大领域浏览知识结构。

## 笔记ID格式

```
YYYYMMDD-NNNN
```

示例：`20260301-0001`

- 自动生成，无需手动指定
- 全局唯一，永不改变
- 按时间排序，便于追溯

## 高级功能

详见 [references/advanced.md](references/advanced.md)：
- 批量导入导出
- 知识图谱生成
- 标签云统计
- 自动归档策略

## 脚本架构

```
scripts/
├── card_manager.py     # 基础增删改查（自动记录操作历史）
├── undo_manager.py     # 撤销管理（独立历史记录）
├── card_creator.py     # 交互式创建流程
└── search_index.py     # 搜索索引（可选）
```

### 操作历史机制

1. **自动记录**：`card_manager.py` 的 create/delete/update 操作自动记录
2. **独立存储**：历史存储在 JSON 文件，不污染卡片数据
3. **有限保留**：只保留最近100条操作记录
4. **撤销标记**：已撤销的操作会标记，避免重复撤销

## 最佳实践

1. **使用交互式创建**：`card_creator.py` 提供更友好的体验
2. **定期撤销检查**：误操作后立即 `undo_manager.py undo`
3. **关联记忆**：创建卡片时尽量关联记忆日期，便于追溯
4. **分类清晰**：永久笔记必须选择九大领域之一

---

*Skill 版本：2.0 | 更新：2026-03-02*
