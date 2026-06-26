# IV 功能规划 /iv-plan

## 命令设计

```
/pvp iv <宝可梦> <联盟>
/pvp iv <宝可梦> <联盟> <攻击>/<防御>/<生命>
```

### 联盟支持

| 联盟 | 全称 | IV 策略 |
|------|------|---------|
| 1500 | 超级联盟 | 4096 枚举 + 互联网 API 兜底 |
| 2500 | 高级联盟 | 4096 枚举 + 互联网 API 兜底 |
| master | 大师联盟 | 不计算，默认 15/15/15 |

大师联盟不计算 IV，输出时直接显示 15/15/15。

### 输出格式（表格）

```
宝可梦    弃世猴
联盟    超级联盟
排名    #28
评分    90.1
属性    格斗 / 幽灵
CP    1499
等级    17
招式    踢倒 / 憤怒之拳* / 近身戰
---
最佳IV    1/15/13
最佳CP    1499
最佳等级    17
我的IV    1/15/10
我的排名    #50
差别    防御相同，生命 -3
---
来源    PvPokeTW
更新时间    2026-05-19 05:57
```

禁止输出：
- 百分比（如 99.6%）
- 乘积 / stat product
- 接近度 / 接近值
- 随机 IV
- 模拟数据

### IV 差别显示规则

只标用户 IV 与最佳 IV 的差值：

```
差别    防御相同，生命 -3
差别    攻击 -1，防御相同，生命相同
差别    全部相同（即最佳IV）
```

空 IV 不标差别。

---

## IV 数据来源（优先级降序）

### 来源 1：PvPokeTW 个体值计算器接口

PvPokeTW 有个体值排名计算逻辑。PvPoke 开源项目中有 `src/engine/iv.ts` 或类似文件，提供基于 CP 上限的 IV 排名计算。

具体方案：
- npm 包 `@pvpoke/engine` 或直接复制其 IV 算法
- 或通过脚本定期从 PvPoke GitHub 同步 IV 排名数据到本地缓存

地址参考：
- https://github.com/pvpoke/pvpoke
- `src/engine/iv.js`

### 来源 2：BattleFlow IV Checker

BattleFlow 是一个社区开发的 PvP IV 检测工具。提供 API 接口，可通过 HTTP 获取指定宝可梦在指定联盟下的最佳 IV。

- 优点：离线备选，API 简单
- 缺点：需要网络，有速率限制

### 来源 3：本地枚举 4096 IV 组合（推荐首选）

使用自定义算法，遍历所有可能的 IV 组合（0-15 攻击 × 0-15 防御 × 0-15 生命 = 4096 种），计算 CP 和等级：

```
CP = Math.floor((攻击种族 + 攻击IV) * (防御种族 + 防御IV) ^ 0.5 * (生命种族 + 生命IV) ^ 0.5 * (等级乘数) ^ 2 / 10)
```

过滤条件：
- CP <= 1500（超级联盟）
- CP <= 2500（高级联盟）
- 等级 <= 50

排序规则：
- 按 stat product（攻击 × 防御 × 生命）降序
- 取排名前 50

#### 等级乘数表

CPM（CP Multiplier）表使用 PvPoke 标准的 0.5 级步进值，从等级 1 到 50。需要从 PvPoke 源数据或 gamemaster.json 中提取。

#### 需要的宝可梦基础数据

每个宝可梦需要：
- `speciesId` — PvPoke ID（如 "annihilape"）
- `atk` — 种族攻击值
- `def` — 种族防御值
- `sta` — 种族生命值

这些数据目前来自：
- `cache/gamemaster.json`（已存在）
- 或通过 mapper.id → PvPoke speciesId 查询

#### 关键问题：中文 speciesId 映射

当前缓存使用中文 speciesId（如"棄世猴"），而 PvPoke IV 引擎需要英文 speciesId（如"annihilape"）。

解决方案：
- 用 `data/pokemon_alias.json` 反向映射：中文 → 英文 speciesId
- 或扩展 mapper.ts 增加 `getPvPokeId(cnAlias)` 函数
- 或修改缓存存储双 ID

---

## 分级实现方案

### Phase 1：本地 4096 枚举（最小可行）

1. 从 gamemaster.json 提取宝可梦基础数据（atk/def/sta）
2. 生成 CPM 表
3. 遍历 4096 种 IV 组合，计算 CP → 筛选符合联盟 CP 上限的 → 按 stat product 排序
4. 输出前 50 名（含 CP、等级、IV）

依赖：
- alias 反向映射（中文 speciesId → PvPoke 英文 speciesId）
- gamemaster.json（已有）
- 新增 `iv.ts` 或 `iv_calculator.ts`

### Phase 2：添加用户 IV 对比

1. 用户输入 `a/d/h`（如 `1/15/10`）
2. 在枚举结果中搜索该 IV 组合
3. 计算与最佳 IV 的差值
4. 输出匹配结果或最接近的（精确匹配，不模拟）

### Phase 3：互联网 API 补强（可选）

1. 监测 PvPokeTW 网站或 API 是否有 IV 查询接口
2. 实现优雅降级：API 不可用时回退到本地枚举

---

## 文件变更清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `src/iv.ts` | 新增 | IV 计算核心：枚举 + 排序 |
| `src/query.ts` | 修改 | 增加 `queryIV()` 函数 |
| `src/index.ts` | 修改 | 处理 `/pvp iv` 命令，格式化 IV 输出 |
| `tsconfig.json` | 可能修改 | 如需要额外 lib |

不修改：
- `scripts/` 下的 Python 导入脚本
- `data/pokemon_alias.json`
- `cache/` 内容结构

---

## 禁止事项（红线）

- ❌ 不输出百分制 IV 评分（如 "99.6%"）
- ❌ 不输出 stat product、乘积
- ❌ 不输出接近度、接近值
- ❌ 不使用随机或模拟 IV
- ❌ 大师联盟不做 IV 计算
- ❌ 不允许未经确认的 API 数据
