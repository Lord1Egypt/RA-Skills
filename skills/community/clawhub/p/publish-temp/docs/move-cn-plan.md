# 配招中文覆盖 — move-cn 设计文档

## 问题

当前 mapper.ts 中还有大量招式缺少中文翻译，例如：

- NATURES_MADNESS → 已修
- RAGE_FIST → 缺
- MUD_BOMB → 已修
- BEHEMOTH_BLADE → 已修
- BEHEMOTH_BASH → 缺
- 各种极巨化招式 → 缺
- 新世代招式 → 缺

进入 `/pvp 配队` 输出时，缺少中文的招显示为英文，破坏体验。

## 目标

禁止输出纯英文招式名。所有输出必须：

1. 有中文 → 用中文
2. 无中文 → 自动回退翻译
3. 自动回退仍失败 → 显示英文（极少情况）

## 策略

### 方案 A：人工补齐（首选）

在 mapper.ts 的 MOVE_CN 中补充缺失招式。

目标：覆盖至少 200 个常用招式。

### 方案 B：自动回退翻译（兜底）

`getMoveCn()` 函数的改进：

1. 查 MOVE_CN 表 → 有则返回
2. 尝试自动翻译：
   - `SNAKE_TO_SNAKE` → 下划线替换空格
   - `WEATHER_BALL_ICE` → 截取 WEATHER_BALL 基础名 + 子类型
   - `TECHNO_BLAST_BURN` → 科技光炮（火）
3. 兜底：首字母大写 + 下划线替换空格

### 方案 C：社区贡献

- 从 PvPokeTW 网页抓取中文招式名
- 或者从中文社区获取对照表

## 自动翻译规则

### 带前缀/后缀的招式

```
WEATHER_BALL_{TYPE} → 气象球（{type_cn}）
TECHNO_BLAST_{TYPE} → 高科技光炮（{type_cn}）
G_MAX_{NAME} → 极巨{name_cn}
```

### 常见英文→中文转换

```
BEHEMOTH → 巨兽
BASH → 弹
BLADE → 斩
FIST → 拳
CLAW → 爪
KICK → 踢
PUNCH → 拳
SLASH → 切
SWIPE → 爪
```

### 兜底规则

```
下划线 → 空格
首字母大写 → 保持
全大写词 → 首字母大写其余小写
```

## 验证

所有输出通路调 `getMoveCn()` 确保：

- `src/query.ts` — 培养查询
- `src/team.ts` — 配队推荐
- `src/evaluate.ts` — 评估我的
- `src/iv.ts` — IV查询（不涉及招式）
- `src/train.ts` — 值得练（新）

## 实现步骤

1. 在 mapper.ts 中添加缺失招式（主流招式全补齐）
2. 增强 `getMoveCn()` 自动回退逻辑
3. 验证所有输出通路无英文招式名
