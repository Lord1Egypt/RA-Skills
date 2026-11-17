# 因子收集 · WorldQuant 公式化 Alpha（扩展族）

> 收集时间：2026-08-13
> 重要澄清：**WorldQuant 没有官方 "Alpha 201 / 212"**。经典出处是《101 Formulaic Alphas》(2015, Tulchinsky et al.)，该全集 **已完整转写收录于 `task/factor-Alpha101.json`（#1–#101）**，用 `row_rank`/`rolling_imax`/`.rolling().corr()` 等 QuantAll 原语。
> 用户提到的 "201/212" 是社区对**公式化 alpha 扩展家族（量价算子型，200+ 个）**的统称。本技能交付：① 算子语义映射表（可复用）；② 公式目录样本；③ 手写一批代表性扩展样本（`factor-WorldQuant_formulaic.json`），与已有 101 互补、不重复。

## 一、WorldQuant 算子 → QuantAll 映射

| WQ 算子 | 含义 | QuantAll 转写 |
|---|---|---|
| `delay(x, d)` | d 天前值 | `x.shift(d)` |
| `delta(x, d)` | 差分 x−x.shift(d) | `x - x.shift(d)` 或 `x.diff(d)` |
| `ts_min/ts_max(x, d)` | 滚动最小/最大 | `x.rolling(d).min()/.max()` |
| `ts_argmax/ts_argmin(x, d)` | 窗口内最值位置 | `rolling_imax(x, d)` / `rolling_imin(x, d)`（返回位置，需 ×d 近似天数） |
| `ts_rank(x, d)` | 时序滚动排名(0-1) | `x.rolling(d).rank(pct=True)` |
| `rank(x)` | 截面排名(0-1) | `row_rank(x)` |
| `correlation(x, y, d)` | 滚动相关 | `x.rolling(d).corr(y)` |
| `covariance(x, y, d)` | 滚动协方差 | `x.rolling(d).cov(y)` |
| `scale(x)` | 截面绝对值和为1 | `x / x.abs().sum()` |
| `decay_linear(x, d)` | 线性衰减加权 | `rolling_decay_linear(x, d)`（=rolling_wma） |
| `signedpower(x, a)` | sign(x)*|x|^a | `np.sign(x) * (np.abs(x)**a)` |
| `indneutralize(x, g)` | 行业中性化 | QuantAll 暂无原生；用 `row_rank` 近似或跳过 |

## 二、公式目录样本（节选，带中文标签）

| # | 公式（原表达式） | 类型 |
|---|---|---|
| 1 | `rank(ts_argmax(signedpower(if(ret<0,std(ret,20),close),2),5))-0.5` | 趋势/反转 |
| 2 | `-corr(rank(delta(log(vol),2)), rank((close-open)/open), 6)` | 量价背离 |
| 9 | `if(0<ts_min(delta(close,1),5), delta(close,1), if(ts_max(delta(close,1),5)<0, delta(close,1), -delta(close,1)))` | 反转 |
| 12 | `sign(delta(vol,1)) * (-delta(close,1))` | 量价背离 |
| 33 | `rank(-(1-open/close))` | 日内 |
| 41 | `sqrt(high*low) - vwap` | 反转 |
| 42 | `(vwap-close)/(vwap+close)` | 反转 |
| 54 | `(close-low)*open^5/((low-high)*close^5)` | 反转 |
| 56 | `rank(sum(ret,10)/sum(sum(ret,2),3)) * rank(ret*cap)` | 量价 |
| 84 | `power(rank(vwap-max(vwap,15),21), delta(close,5))` | 量价 |
| 101 | `(open-close)/(high-low+0.001)` | 日内反转 |

> 完整 101 见 `task/factor-Alpha101.json`。本目录为扩展族参考，标注类型便于后续按需扩充。

## 三、交付文件

- `factor-WorldQuant_formulaic.json` — 10 个手写公式化 alpha 样本（WQ_ 前缀），结构同 task/*.json，待确认后入库。
- 实跑验证见 `output/factor-WorldQuant_formulaic.xlsx`。
- ⚠️ 与 `task/factor-Alpha101.json`(基础 101) 互补；如需真正 200+ 全集，需另行获取社区扩展公式源（当前公开无可靠独立的 #102–212 官方公式）。
