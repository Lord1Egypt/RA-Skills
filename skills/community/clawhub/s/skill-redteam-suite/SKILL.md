---
name: redteam-suite
description: "Use when you must test whether a skill reviewer, gate or scoring script can be fooled — 'my reviewer keeps passing junk', 'can this gate be gamed', 'test the anti-cheat', 'reviewer 能不能被假包骗过'. Ships two adversarial probe packages and a runner that judges the verdict on the reproducible dimension, not on the total score. Also use it before trusting any quality gate you did not build yourself."
license: MIT
metadata:
  version: 1.1.0
  author: zhaoxinghua09-cell
  tags:
    - red-team
    - 反作弊
    - skill-review
    - quality-gate
    - benchmark
---

# Skill Redteam Suite

An adversarial benchmark for skill reviewers, gates and scoring scripts. It answers one question:

> Can your reviewer be fooled by a package that looks complete but verifies nothing?

## 什么时候调用（触发词）

用户说出下面任一句时，就应该用本套件，而不是凭感觉评价一个评审器：

- 「我这个 reviewer 靠不靠谱」「它是不是见谁都给分」
- 「测一下反作弊」「能不能绕过这个门禁」
- 「这个评分脚本会被假包骗过吗」「来个人红队一下」
- "can this gate be gamed", "does my reviewer reject junk", "red-team the reviewer"

**不适用**：评审一个业务技能本身的质量（那是 `lgd-skill-review` 的事）、检查代码安全漏洞、给人做能力背书。

## 决策树：先问要回答什么

```
要回答什么？
├─ 只想确认评审器不会被假包骗
│    → 跑全量：python run_suite.py --reviewer <review.py>      出口码 0 = 两个探针都被拦下
├─ 想知道具体哪个探针漏了
│    → 看输出里的 "GOT THROUGH <- hole" 行，它会在那一行给出 total 与 repro 的实际值
├─ 改过评审器、要做回归
│    → 跑全量 + 与本页基线表对比：shape 应 <80、vacuity 的 repro 应 <20/20
└─ 手上没有评审器
     → 别跑。本套件不产出评分，只产出判定；没有被测对象时它返回 2，不会给一个空的 PASS
```

## 五个有序步骤

1. 确认被测对象是一个**能接受目录参数、输出 `总分 x/100` 与 `reproducible n/20`** 的评审器。
2. 跑 `python run_suite.py --reviewer <path>`，默认门线 80（`--threshold` 可调）。
3. 读两行探针结果：`shape` 与 `vacuity`，每行给出 total、repro、BLOCKED/GOT THROUGH。
4. 出现 `GOT THROUGH` 时，先看 repro 是否拿满 20/20 —— 那是「验不了任何东西还拿满分」的硬洞。
5. 把这一轮的 total/repro 记进你的基线表；下一版评审器用同一张表对比，才叫回归。

## 探针清单（2 个）

| 探针 | 它伪装成什么 | 为什么必须存在 | 期望结果（我们的基线） |
|---|---|---|---|
| `shape` | 形状完整、runner 打印 PASS 但零断言，demo 只打印一行 | 骗「有没有测试入口」这类结构检查 | total < 80 且 repro < 20（实测 78 / 11） |
| `vacuity` | 形式完整、内容为空的包 | 骗「字段齐不齐」这类形式检查：总分可能过，但复现维度必须掉分 | repro < 20（实测 88 / 16） |

两个探针都不是为了好看：`shape` 打的是「有 runner 就算能复现」，`vacuity` 打的是「字段齐全就算有内容」。

## 反模式（每条都带理由）

1. **只看总分，不看复现维度。** 理由：总分本质是形状分，一个形状漂亮的假包在本尺子上能到 88 以上；真正暴露「什么都没验」的是 `reproducible` 这一维。
2. **把「ALL PROBES BLOCKED」读成「评审器很强」。** 理由：这只证明它没被这两个探针骗过，不证明它能识别细微错误；结论要写成「未被这两个探针骗过」。
3. **拿产品尺子给本套件打分然后判它不合格。** 理由：这是范畴错误——仪器问的是「你能不能被骗」，产品尺子问的是「你能不能干活」；两者不冲突，但也不能互相替代。
4. **把 `probes/` 当可安装技能目录发出去。** 理由：里面是故意坏掉的包，进了公共索引就会被人真的装走。所以分发态只带 `probes.zip`，由 runner 解到临时目录，用完删。

## 硬规则清单（MUST / NEVER）

- **禁止**用总分下结论：因为总分是形状分，形状漂亮的假包在本尺子上也能到 88 以上。
- **必须**在结论里写明「未被这两个探针骗过」，否则读者会把它读成能力背书。
- **禁止**把 `probes/` 目录原样发布：因为里面是故意坏掉的包，进了公共索引就会被真的装走。
- **必须**把探针解到临时目录并在结束后删除，否则用户机器上会残留假包。
- **禁止**在没有被测评审器时假装通过：因为空转的绿灯比红灯更危险。
- **必须**同时记录 `total` 与 `repro` 两个数，否则下一版回归时无法比较。
- **不得**把本套件的结果写进对外认证口径：因为它只覆盖两种造假形态。
- **禁止**为了让它过而修改被测评审器：那等于自己给自己出题。
- **必须**在改动评审器后重跑基线表，否则新补的检查可能只是让探针更容易通过。
- **不得**忽略 repro 的 warn：读不懂输出，就等于这一维没有验过。

## 安全边界与降级

- **只读**：不修改被测评审器、不改被测包、不发网络请求、不安装依赖；探针只解到系统临时目录，结束即删（`--keep` 才保留）。
- **不判内容质量**：本套件不评价技能写得好不好，只判定「明显造假能不能蒙过去」。
- **找不到评审器** → 返回 2 并打印原因，**不伪造 PASS**；找不到 `probes/` 或 `probes.zip` → 同样返回 2。
- **评审器输出不可解析**（没有 `总分`）→ 判为「拦住了」，同时打印 warn：读不懂的东西骗不了它，但这一维等于没验。
- **超时 300 秒** → 视为未验证，不计入通过。
- **自检入口**：`python tests/run_tests.py`，需要同级 `lgd-skill-review` 或用 `REDTEAM_REVIEWER` 指定；成功输出 `---- 2/2 PASS ----`，找不到就返回 3，不冒充通过。

## 自检与本机实测

```bash
# 自证：两个探针都应被拦下
python tests/run_tests.py

# 直接跑（门线可调）
python run_suite.py --reviewer ../lgd-skill-review/scripts/review.py --threshold 80
```

本机基线：2/2 PASS（shape 78、repro 11；vacuity 88、repro 16，门线 80）。这个数字由 `tests/run_tests.py` 跑出来，不是写上去的。

## 对照实验：证明这套件会失败

| 评审器 | shape | vacuity | 结论 |
|---|---|---|---|
| lgd-skill-review 1.1.21 | 78，repro 11/20 | 88，repro 16/20 | 全部拦下 |
| 同一份代码，关掉三项检查 | 87，repro 20/20 | 92，repro 20/20 | 2 个探针全部穿过去 |

第二行是这套件的负控：不做这一行，「全拦」只能说明探针太弱。

## 同系列技能（LGD 生态）

- **lgd-skill-review** — 双尺评审（结构 100 + 语义 120），本套件是被它调用来做反作弊关的
- **claim-audit** — 把文档里的数字拉去重跑，判「说得对不对」
- **evidence-anchor** — 把 `file:line` 引证解析回真实文件，判「证据在不在」

三者组合才是一条完整链：**看形状 → 核数字 → 验证据 → 拦造假**。任何一环单独用，都别声称「全面审计过了」。

## 局限

- 只覆盖两种典型造假形态；第三种（半真半假的包）本套件不判。
- 通过不代表评审器优秀，只代表它没被这两个探针骗过。
- 探针基于我们自己的评审器调过参数；换评审器后门线 80 需要重新校准。
- 本套件不做判断，只做判定：它**不编造分数、不编造通过**，只 faithful 地把被测评审器自己的输出摆出来。

## Distribution note

`probes/` 是开发态目录；发布态只带 `probes.zip`（20 个成员），安装本包不会往任何技能索引里塞可安装的假包。这是 1.1.0 相对 1.0.0 的结构修正。

## License

MIT. Copyright (c) 2026 SynomosAI.
