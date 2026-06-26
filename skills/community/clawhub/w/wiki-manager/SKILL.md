# wiki-manager / Wiki 索引管理

> 版本：v1.0
> 创建：2026-04-08
> 更新：2026-04-08（空空建议，改为单 JSON 索引方案）
> 依据：空空方案 + 小蜂自想（两者高度一致）
> 铁三角：彧哥 + 空空 + 小蜂

---

## 核心理念

**用工具化索引文件代替散 .md**：
- 1 个 wiki.json = 所有关键词索引
- 500 条封顶
- 三池循环（core / buffer / new）
- 不存大段正文，内容交给向量库/memory

---

## 文件结构

```
wiki/
├── wiki.json       ← 索引文件（三池合一，全部词条在这里）
├── wiki.json.bak   ← 上一次备份（每次写入前自动更新）
└── SKILL.md       ← 本文件，管理脚本
```

---

## wiki.json 结构

```json
{
  "version": "1.0",
  "name": "小蜂Wiki索引",
  "pools": {
    "core":   { "name": "核心热词池", "limit": 200 },
    "buffer": { "name": "次热缓冲池", "limit": 200 },
    "new":    { "name": "新晋新词池", "limit": 100 }
  },
  "entries": [
    {
      "id": "001",
      "keyword": "四部曲",
      "pool": "core",
      "definition": "想→说→做→看，沟通决策流程",
      "source": "skills/4steps-to-wisdom/SKILL.md",
      "score": 5,
      "lastUsed": "2026-04-08",
      "created": "2026-04-08",
      "sourceType": "skill"
    }
  ]
}
```

**字段说明**：

| 字段 | 必填 | 说明 |
|------|------|------|
| id | ✅ | 唯一ID，格式"001"～"500" |
| keyword | ✅ | 关键词（去重校验） |
| pool | ✅ | 所在池：core / buffer / new |
| definition | ✅ | 一句话定义 |
| source | ✅ | 引用路径（memory/xxx 或 skills/xxx） |
| score | ✅ | 使用频率评分（1-5） |
| lastUsed | ✅ | 最后使用日期 YYYY-MM-DD |
| created | ✅ | 创建日期 YYYY-MM-DD |
| sourceType | ❌ | 来源类型：skill / memory / discuss |

---

## 三池容量

| 池 | 上限 | 说明 |
|---|------|------|
| core | 200 | 最高频，核心专属 |
| buffer | 200 | 次高频，缓冲梯队 |
| new | 100 | 新增词，观察期 |
| **合计** | **500** | **永不膨胀** |

---

## 循环规则

```
new 高频用 → 升 buffer
buffer 高频用 → 升 core
core 长期不用 → 降 buffer
buffer 长期不用 → 降 new → 淘汰
```

**降级/淘汰触发**：最后使用距今 > 30 天

---

## 管理脚本（无工具版，用 exec）

### 查词（按池）
```bash
# 查 core 池
cat wiki/wiki.json | jq '.entries | map(select(.pool == "core"))'

# 模糊搜索
cat wiki/wiki.json | jq '.entries | map(select(.keyword | contains("四部")))'
```

### 查所有（高效加载）
```bash
cat wiki/wiki.json    # 一次读完所有词条，毫秒级
```

### 新增词条
```bash
# 编辑 wiki/wiki.json，手动追加 entries[]
# 注意：先检查是否已存在（keyword 去重）
```

### 升降级
```bash
# 将某词从 new 升到 buffer（score >= 3 时触发）
# 修改 wiki.json 中对应 entry 的 pool 字段
```

### 淘汰检查（每次心跳或定期）
```bash
# 检查 buffer/new 池中最后使用 > 30 天的词
cat wiki/wiki.json | jq '.entries | map(select(.lastUsed < "2026-03-09" and .pool != "core"))'
```

### 备份（写入前自动）
```bash
cp wiki/wiki.json wiki/wiki.json.bak
```

---

## compact 恢复流程

compact 后认知丢失 → 执行以下步骤恢复：

```
1. cat wiki/wiki.json         # 加载所有词条（毫秒级）
2. 读取 definition 字段       # 恢复一句话认知
3. 如需详细内容 → 从 source 字段路径读取 memory/ 向量库
```

---

## 维护节奏

| 动作 | 频率 |
|------|------|
| 新词入 new 池 | 按需，随时 |
| 升降级检查 | 每天开机 |
| 淘汰检查 | 每周 |
| 备份 | 每次 wiki.json 写入前 |

---

## 注意事项

- 每次写入前先 `cp wiki/wiki.json wiki/wiki.json.bak`
- wiki.json 损坏时用 `cp wiki/wiki.json.bak wiki/wiki.json` 恢复
- compact 后 reload 一次 wiki.json 即可恢复全部词条认知
- 不要存大段正文，只存引用路径，详细内容在 memory 向量库

---

*Wiki 索引管理 v1.0 - 轻量高效，铁三角共识*
