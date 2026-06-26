# 配队推荐 · MVP 设计

## 命令入口

```
/pvp 配队 <联盟>
/pvp 配队 <联盟> <核心宝可梦>
```

示例：

```
/pvp 配队 1500
/pvp 配队 1500 胖嘟嘟
```

## MVP 输出格式

```
📦 大师联盟 配队推荐

推荐队伍：
  核心：宝可梦名（PvPokeTW #排名）
  小招 + 充能1 / 充能2
  安全换：宝可梦名（PvPokeTW #排名）
  小招 + 充能1 / 充能2
  收割：宝可梦名（PvPokeTW #排名）
  小招 + 充能1 / 充能2

我已有：✅ 胖嘟嘟、✅ 土龙弟弟
我缺少：❌ 勾魂眼
下一步培养：优先练 勾魂眼 → 土龙弟弟
```

## 数据来源（只读）

| 数据 | 来源 | 用途 |
|------|------|------|
| 物种排名 | `rankings-{1500,2500,master}.json` 数组索引+1 | PvPokeTW 排名 |
| 属性 | `rankings[].moves` → gamemaster 查询 | 克制/抗性基础 |
| 推荐配招 | `rankings[].moveset`（PvPoke 官方组合） | 显示在每只宝可梦旁 |
| 精英招式 | `data/elite_moves.json` | `*` 标记 |
| 我的宝可梦 | `data/my_pokemon.json` | 标记已有/缺少 |

## 角色定义（卡片简化版）

三个角色，基于 PvPokeTW 特定维度的评分排名选取：

**核心（Lead / Safe Switch）**— 开局面或安全换入
- 从高排名中选取
- 有核心命令时：以指定宝可梦为核心
- 无核心命令时：从排名前 20 或用户已有中选择一个

**安全换（Safe Switch）**— 逆风时换入
- 从属性抗性较好的宝可梦中选
- 优先选排名高 + 属性互补的

**收割（Closer）**— 收尾
- 从高速/高输出宝可梦中选
- 已有宝可梦优先

### MVP 阶段简化规则

```
无核心命令（/pvp 配队 1500）：
  1. 从已有宝可梦中，选排名最高的 → 核心
  2. 从已有宝可梦中，选属性与核心不同且排名次高 → 安全换
  3. 从已有宝可梦中，选第三个 → 收割
  4. 如果已有不足 3 只，从 rankings 补齐
  
有核心命令（/pvp 配队 1500 胖嘟嘟）：
  1. 核心 = 指定宝可梦
  2. 从 rankings 找属性最不弱的（抗性最多的）→ 安全换
  3. 从已有或 rankings 补第三个 → 收割
```

## "我已有 / 我缺少" 判断

| 列 | 规则 |
|----|------|
| 我已有 | 推荐队伍中在 `my_pokemon.json` 能找到的 |
| 我缺少 | 推荐队伍中不在 `my_pokemon.json` 的（含未培养） |
| 下一步培养 | 我缺少中排名最高的，建议优先补齐 |

## 精英招式标记规则

沿用已有逻辑：

```
isEliteMove(speciesId, moveId) → boolean
```

影响范围：
- 推荐配招中精英招式加 `*`
- "下一步培养" 若有精英招式需要精英 TM，加备注 ⚠️

## 与现有模块的关系

```
team.ts (新)
  └─ 调用 fetcher.getRankings(league)   → rankings 数据
  └─ 调用 mapper.getSpeciesCn(speciesId) → 中文名
  └─ 调用 mapper.getMoveCn(moveId)       → 中文招式名
  └─ 调用 evaluate.isEliteMove(speciesId, moveId) → * 标记
  └─ 读取 data/my_pokemon.json            → 已有宝可梦判断
  └─ 读取 data/elite_moves.json           → 精英招式查询

index.ts
  └─ handlePvp
       └─ args[0] === '配队' → team.ts handleTeam(args.slice(1))
```

## 限制（设计边界）

- 不做克制链计算（MVP）
- 不做真实胜率模拟（MVP）
- 不做 IV 判断（不管大师还是其他联盟）
- 不做多轮换位模拟
- 建议不做假——全部从 PvPokeTW 数据源读
- **输出中所有宝可梦名均使用中文**（通过 getSpeciesCn 转换）

## 后续方向

- 第二阶段：基于 type chart 做属性覆盖检查
- 第三阶段：open 组队（核心 + 辅助 + 收尾）
- 第四阶段：核心变动式推荐（如"不要胖嘟嘟"）
