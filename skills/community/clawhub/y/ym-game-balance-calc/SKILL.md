---
name: ym-game-balance-calc
slug: ym-game-balance-calc
display_name: 游戏数值平衡校验
display_name_en: Game Balance Calculator
displayName: 游戏数值平衡校验
description: "校验游戏伤害公式与经济系统数值，输出可复算的平衡报告。 当用户提到「数值平衡」「伤害公式」「游戏数值」「经济系统校验」时使用。"
description_zh: "校验游戏伤害公式与经济系统数值，输出可复算的平衡报告。"
description_en: "Verify damage and economy numbers with a reproducible balance report."
summary: "校验游戏伤害公式与经济系统数值，输出可复算的平衡报告。"
category: data-analysis
version: 0.1.0
author: 刘玉明
tags: [数值平衡, 伤害公式, 游戏数值, 经济系统校验]
trigger:
  - 数值平衡
  - 伤害公式
  - 游戏数值
  - 经济系统校验
agent_created: true
---

# 游戏数值平衡校验 (ym-game-balance-calc)

只做数值计算与判定，不接引擎、不调游戏。核心交付是 `scripts/balance_calc.py`：三个子命令分别校验伤害公式、经验曲线、经济收支，每份报告都附「复算命令」，用户改参数重跑即得同样口径结果。公式只开放内置名（减伤式/乘算式/差值式），不解析任意表达式，规避注入与歧义。

## 何时使用

- 用户说「校验一下伤害公式」「DPS 算一下」「数值平衡」时
- 用户给了一套攻击/防御/等级参数，想知道各等级实际输出时
- 用户要设计等级曲线，问「30 小时到 30 级怎么定经验」时
- 用户有产出点和消耗点价格表，想找收支断档点和回本周期时

## 运行前提

- 依赖：Python 3.8+ 标准库，无第三方包
- 脚本路径：`scripts/balance_calc.py`（Windows 下 `python scripts/balance_calc.py ...`）
- 不联网、不读写技能目录以外的文件
- 公式名只认内置三种，传任意表达式会被拒绝并提示可用名

## 输入契约

三种场景，选一种跑对应子命令：

| 场景 | 子命令 | 必需输入 | 可选输入 |
|---|---|---|---|
| (a) 伤害/减伤公式 | `dps` | --atk --def --lvl --formula | --grow --defgrow --aps --coef --floor |
| (b) 等级成长曲线 | `curve` | --target-hours --max-lvl | --base --curve-type --power --rate-exp |
| (c) 经济系统 | `economy` | --income --cost | 无 |

- dps：--atk/--def 为 1 级基础值；--lvl 为逗号分隔等级列表；--formula 取「减伤式/乘算式/差值式」。
- curve：--target-hours 为到满级目标总时长；--max-lvl 为满级；--base 为 1 级经验。
- economy：--income/--cost 为「等级:数值」逗号串，脚本在整数等级上线性插值。

**缺失处理：**

- 缺必需参数 → argparse 报错退出，提示缺哪个，不臆造默认值
- --formula 给非内置名 → 报错列出可用名，不执行
- economy 节点为空或格式错 → 报错说明格式，不跑

## 执行步骤

1. **确定场景** — 分辨用户给的是伤害参数、等级目标还是经济表，选 `dps` / `curve` / `economy`。拿不准就问清是哪一种，不要混跑。

2. **选子命令并跑** — 按输入契约组装命令，例如：
   `python scripts/balance_calc.py dps --atk 100 --def 50 --lvl 1,10,50,100 --formula 减伤式`
   `python scripts/balance_calc.py curve --target-hours 30 --max-lvl 30 --base 100`
   `python scripts/balance_calc.py economy --income "1:100,10:250,30:900" --cost "5:120,15:400,30:2000"`

3. **读报告判定** — 看脚本输出的「判定」行：超调/平坦/断档/健康。dps 看 DPS 是否随等级平滑；curve 看本级时长是否平滑；economy 看有无断档点（产出低于消耗）。

4. **对照公式库定方案** — 按 `references/formulas.md` 判断当前公式类型是否合适：减伤式后期是否爆炸、乘算式 K 是否过小、差值式是否触底。拿不准就查该文件的「典型病与症状」。

5. **调参重跑对比** — 改参数（如把 --grow 从 0.08 调到 0.05、curve 的 --power 从 1.5 调到 1.3）重跑，把两次报告的判定行并列，给出「改前/改后」对比，让用户看到曲线变平滑。报告末尾的「复算命令」原样可用。

## 输出格式

脚本输出为表格 + 判定结论 + 复算命令。交给用户的报告取其中「判定」与关键几行，结构如下：

```
=== DPS 校验报告 ===
公式类型：减伤式
等级    攻击      防御      单次伤害  DPS
1       100.0     50.0      66.7      66.7
10      ...
判定：健康：DPS 随等级平滑增长（xx.x），未见突跳或爆炸
复算命令：python scripts/balance_calc.py dps --atk 100 --def 50 --lvl 1,10,50,100 --formula 减伤式
```

## 能力边界

- 只做数值计算与判定，不接入任何游戏引擎
- 不调游戏、不读运行时日志、不爬线上数据
- 不支持任意自定义公式解析（防注入与歧义），新公式需登记为内置名
- 不预测玩家行为、不替代策划最终拍板

## 常见坑

1. **面板攻击不等于实际输出** — 现象：只拿 atk 算 DPS，忽略防御和穿透，结果虚高。原因：面板值未过减伤公式。规避：dps 子命令强制带入 --def 与公式，报告看「单次伤害」而非裸攻击。

2. **指数成长后期爆炸** — 现象：经验曲线用 exp 且 r>1.05，满级一级要刷几小时。原因：等比增长后期必爆。规避：curve 默认用 power（p=1.5）；用 exp 时看脚本「超调/爆炸」判定，把 r 压到 1.05 以内或改用幂函数。

3. **只测毕业装备不看过程装备** — 现象：只验满级 DPS，中间等级断档没发现。原因：只给首尾等级。规避：--lvl 给完整梯度（1,10,50,100），脚本会抓相邻级突增并标「断档」。

4. **经济产出算总量忘算回收** — 现象：总产大于总消，但某等级产出断崖低于消耗，玩家卡死。原因：只看汇总。规避：economy 按等级插值逐节点出净收支，脚本直接标出「断档点（产出<消耗）」。

5. **公式让用户随便输入表达式有注入风险** — 现象：解析 `atk*atk/(atk+def)` 这类字符串，可能夹带系统调用或写法歧义。原因：任意表达式解析 = 执行用户输入。规避：--formula 只认内置名，传表达式直接报错列可用名。

6. **攻防同速成长导致伤害不涨** — 现象：减伤式下 DPS 随等级几乎不动，玩家觉得没变强。原因：atk 与 def 等比涨，减伤除法式趋向恒定。规避：dps 默认 --grow(0.08) > --defgrow(0.04)，并看「平坦」判定，必要时拉开攻防成长差。

## 验收用例

- dps：输入 `--atk 100 --def 50 --lvl 1,10,50,100 --formula 减伤式` → 输出 4 行 DPS 表 + 判定结论；改成非内置名（如 `--formula "atk*def"`）应报错列可用名
- curve：输入 `--target-hours 30 --max-lvl 30 --base 100` → 输出每级经验、累计时长，判定曲线平滑度；改 `--power 2.5` 应判「超调/爆炸」
- economy：输入 `--income "1:100,10:250,30:900" --cost "5:120,15:400,30:2000"` → 输出各节点净收支，标出断档等级与回本等级
- 通用：三个子命令 `--help` 均可运行，列出参数说明

## 目录说明

- `scripts/balance_calc.py` — 主脚本，dps / curve / economy 三个子命令
- `references/formulas.md` — 公式库与适用场景、典型病与症状
- `templates/` — 预留（本报告由脚本直接生成，无需模板）
