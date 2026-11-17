---
name: xiaohongshu-prohibited-words
description: 小红书违禁词离线检测（单一真相源）。纯本地词库 + 扫描脚本，不依赖付费 API，覆盖免费课程/证书等场景实测限流词 + 通用违禁词。发布前必跑，退出码 0 才可发布。词库带入库/出库维护机制，持续养护不过时。
version: 1.0.6
metadata:
  short-description: 小红书违禁词离线检测与词库维护
---

# 小红书违禁词离线检测

小红书内容发布前的违禁词闸门。**这是违禁词库的单一真相源**——其他 skill（free-course-share、xiaohongshu-content-workflow 等）需要违禁词检查时，都引用本 skill，不要各自维护一份。

## Trigger

- 任何小红书笔记发布前，需要做违禁词/敏感词检查
- 需要判断某文案是否会触发限流、下架或驳回
- 需要维护违禁词库（新增实测雷、降级误杀词、过期删除）

## 为什么用离线库而不是付费 API

- `multi-wordcheck` 依赖 REDFOX API（付费，积分耗尽时无法运行）
- 本 skill 纯本地、零依赖、随时可跑，作为发布前**强制兜底**
- REDFOX 充值后可补跑 API 做双保险，但离线扫描是底线

## 使用

### 1. 发布前扫描（强制）

```bash
# 从物料 md 扫描（只提取「## 标题」+「## 正文」+「## 标签」三段，跳过审查记录避免误报）
python3 scripts/check_prohibited.py --file 笔记终稿.md

# 或直接传纯发布文案
python3 scripts/check_prohibited.py "标题" "正文" "标签"
```

退出码：`0` = 无 P0 硬词（PASS）；`1` = 有 P0 硬词需改；`2` = 运行错误；`3` = **依赖缺失（fail-closed）**。

**规则：P0 硬词未清空 = 禁止发布。** P1/P2 命中建议顺手改，但不阻塞发布。

> 词库路径默认自动查找。要用别的词库，设环境变量 `XHS_WORDLIST=<路径>` ——
> **指定了却找不到就是退出码 3，不会静默回落到默认词库**（否则「我换了词库」会变成一句谎话）。

> ⚠️ **这是单项检查（只查词）**，不覆盖标题字数、AI 声明、导流风险。
> 要一次过完发布前所有关，用 **`xiaohongshu-preflight-check`** —— 那是发布前闸门的**唯一出口**：
> ```bash
> python3 ~/.workbuddy/skills/xiaohongshu-preflight-check/scripts/preflight.py --file 笔记终稿.md
> ```
> 两者**共用同一份词库与同一套解析**，结论必然一致，不会一个放行一个拦截。

### 2. 词库维护（入库 / 出库）

词库在 `references/prohibited-words.md`，**不是静态清单，必须持续养护**，否则会越滚越臃肿、把能发的词误杀。

**入库**（满足任一才加，禁止"感觉像敏感词"就加）：
1. 实测触发限流/下架（要有日期+场景+可复现）
2. 官方公告明文列出
3. 可核验的第三方词库（标注来源）

入库写全 5 字段：`词 | 级别 | 触发场景 | 替代 | 入库日期`

**出库 / 降级**（定期做，建议每月一次）：
1. P0→P1：确认不再触发硬限流（平台更新或连续 3 次使用未限流）
2. P1→删除：确认是误杀（正常使用无影响）
3. 合并去重：同一词的不同变体合并
4. 过期删除：规则变化后不再适用的词

**校准信号**：
- 限流了但词库没扫出 = 漏词 → 补进库
- 用了"违禁词"却没限流 = 误杀词 → 降级/删除
- 平台更新审核规则 → 主动重审

> 原则：**宁可禁得准，不要滥禁。** 误杀损失正常表达空间，漏词才损失一篇笔记。两害相权，优先保证禁得准。

## 资源

- `references/prohibited-words.md` — 违禁词库（7 大类：实测硬词/外部平台名/极限词/价格诱导/导流话术/账号禁区词/强制标注项）
- `references/sections.json` — **段落配置**：哪一段归哪一组、默认什么级别、逐词覆写（改级别只改这里）
- `scripts/wordlist.py` — **解析与匹配的单一实现**（被本 skill 与 `xiaohongshu-preflight-check` 共用）
- `scripts/check_prohibited.py` — 离线扫描脚本（纯 stdlib，零依赖）
  ```bash
  python3 scripts/check_prohibited.py --file 笔记终稿.md
  ```
- `scripts/selftest.sh` — 退出码回归自测（含两条漂移回归用例，改词库后跑一遍）
  ```bash
  bash scripts/selftest.sh
  ```

## 设计约束：词条只有一个来源

`check_prohibited.py` **不内嵌任何词条副本**，运行时从 `references/prohibited-words.md`
解析；解析逻辑在 `scripts/wordlist.py`，消费方（含 `xiaohongshu-preflight-check`）按同级
skill 目录载入，不各自复制一份。

**为什么定这条（有事故）**：脚本原先内嵌一份「精简可运行版词库」，靠人工与 md 同步。
2026-09-19 实测发现两边已经漂移 —— md 里标为 P0 的
「免费（全文≥2次）」与「答案+PDF+主页群」，脚本**一个都没拦住**，
而脚本自造的「免费领取」规则又拦了 md 只说 P1 的词。**内嵌副本 = 漂移的来源。**

所以：
- 加词 / 改级别 → **只改 `prohibited-words.md` 与（必要时）`sections.json`**，脚本不动
- 词库读不到、`sections.json` 缺失、解析出 0 条规则 → **退出码 3，绝不放行**

## 引用关系

- 被 `free-course-share` 引用（免费课程/证书笔记发布前）
- 被 `xiaohongshu-content-workflow` 引用（内容生产流程第 7 步）
- 被 `xiaohongshu-preflight-check` 引用（发布前闸门：词库 + 解析都从这里载入）

## 相关 skill / Related skills

- 表情包出图文案、课程卡文案定稿后，直接丢进来跑一遍（`emoji-sticker-cn` / `free-course-share` 的产出都适用）。发布前过一遍本 skill，是把「被限流/被拒」的成本前移的最便宜动作。
