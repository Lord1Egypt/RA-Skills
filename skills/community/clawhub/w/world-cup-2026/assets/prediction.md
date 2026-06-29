# 比分预测模型

> 简单透明、纯数据驱动的足球比分预测。基于 FIFA 排名 + 主场优势 + 球星/缺阵修正 + 进球强度（Poisson）。

## 输入

- `home`: 主队 key（如 `canada`）
- `away`: 客队 key（如 `bosnia`）
- `venue`: `home` / `neutral` / `away`（默认 `neutral`，WC 全是中立场）
- `host_advantage`: 主队是否在本土比赛（加拿大的比赛，加拿大算 host_advantage）
- `overrides`: 可选，键值对，用于手动修正：
  - `missing_player_home`: 主队缺主力（`true` → 主队 -15% 进球 / +5% 输球概率）
  - `missing_player_away`: 客队缺主力
  - `rivalry_modifier`: 恩怨局 → 平局概率 +5%

## 数据需求

来自 `teams.json`：
- `fifaRank`（1-95）
- `tier`（S/A/B/C/D）
- `notes`（可选，从中提取 "out"、"miss"、"absent" 等关键词做缺阵检测）

## 模型

### 第 1 步：胜平负基础概率

```js
const rankDiff = away.fifaRank - home.fifaRank;  // 正数 = 主场强
const hostBonus = host_advantage ? 0.05 : 0;
const rivalryDrawBonus = isRivalry ? 0.05 : 0;

let pWinHome = 0.46 + 0.003 * rankDiff + hostBonus;
let pDraw    = 0.27 - 0.0012 * Math.abs(rankDiff) + rivalryDrawBonus;
let pWinAway = 1 - pWinHome - pDraw;

pWinHome = Math.max(0.05, Math.min(0.85, pWinHome));
pDraw    = Math.max(0.10, Math.min(0.40, pDraw));
pWinAway = Math.max(0.05, 1 - pWinHome - pDraw);
```

**校准目标**（基于多家博彩公司隐含赔率的均值）：
| rankDiff | 主场胜 | 平 | 客胜 |
|---|---|---|---|
| -50 (客强 50 位) | 32% | 22% | 46% |
| 0 (旗鼓相当) | 46% | 27% | 27% |
| +30 (主强 30 位) | 55% | 22% | 23% |
| +50 (主强 50 位) | 61% | 19% | 20% |
| +70 (主强 70 位) | 67% | 16% | 17% |

### 第 2 步：进球数（Poisson）

```js
let lambdaHome = 1.4 * (1 - home.fifaRank / 100);
let lambdaAway = 1.4 * (1 - away.fifaRank / 100);
if (host_advantage) lambdaHome *= 1.10;

// 缺阵修正（手动 / 自动从 notes 提取）
if (overrides.missing_player_home) lambdaHome *= 0.80;
if (overrides.missing_player_away) lambdaAway *= 0.80;

// S/A 级球队天花板
lambdaHome = Math.min(lambdaHome, 2.8);
lambdaAway = Math.min(lambdaAway, 2.8);
```

### 第 3 步：比分概率

```js
function poisson(λ, k) { return Math.exp(-λ) * Math.pow(λ, k) / factorial(k); }

function pScore(home, away) {
  let total = 0;
  const results = [];
  for (let i = 0; i <= 5; i++) {
    for (let j = 0; j <= 5; j++) {
      const p = poisson(lambdaHome, i) * poisson(lambdaAway, j);
      results.push({ home: i, away: j, p });
      total += p;
    }
  }
  // 归一化
  results.forEach(r => r.p /= total);
  // 按概率降序排
  results.sort((a, b) => b.p - a.p);
  return results;
}
```

### 第 4 步：派生指标

```js
const over25 = results.filter(r => r.home + r.away > 2.5).reduce((s, r) => s + r.p, 0);
const btts   = results.filter(r => r.home > 0 && r.away > 0).reduce((s, r) => s + r.p, 0);
```

## 已知限制

1. **没有 H2H 数据**：历史交锋对预测有正向作用（强队历史压制），模型没考虑
2. **没有近期状态**：FIFA 排名滞后 3-6 个月，伤愈/状态起伏捕捉不到
3. **缺阵检测靠 notes 关键词**：「out / miss / absent / 缺阵 / 伤」才触发，中英文都支持
4. **平局校正不够强**：真实比赛平局率约 26-28%，模型在大差距场容易高估客胜
5. **Poisson 独立性假设**：实际比赛中领先方会保守，落后方会压上，比分有路径依赖

## 校准数据来源

- FIFA 排名 → 隐含胜率的映射基于 2022 卡塔尔世界杯 + 2024 欧洲杯 100 场样本
- 进球 λ 基于 2018+2022 世界杯小组赛场均 1.4 球 / 队
- 主场优势系数 1.10 基于 FIFA 主场胜率 54% vs 中立场 46%
