---
slug: tenderaudit-full-compliance-free
displayName: 招投标全案合规审计（免费版）
version: 1.1.43
summary: 把一个项目的投标材料先做一轮免费的AI体检，报价算术 + 模板占位符，不需要付款，也不需要注册。 免费、无需注册、无需 API Key。
tags: [招投标, 免费, 逐家报价算术校验, 标书检查, 投标自查]
license: Proprietary
name: tenderaudit-full-compliance-free
display_name: 招投标全案合规审计（免费版）
display_name_en: TenderAudit Full Compliance (Free)
description: 把一个项目的投标材料先做一轮免费的AI体检，报价算术 + 模板占位符，不需要付款，也不需要注册。 本免费版执行 逐家报价算术校验、模板占位符扫描。触发词包括 招投标全案合规审计、逐家报价算术校验、模板占位符扫描。触发词还包括投标文件检查、标书审查、投标文件审查、标书合规检查。
description_zh: 把一个项目的投标材料先做一轮免费的AI体检，报价算术 + 模板占位符，不需要付款，也不需要注册。 本免费版执行 逐家报价算术校验、模板占位符扫描。
description_en: A free mechanical pre-check for bidding documents. No payment, no registration, no API key.
category: office
author: WorkBuddy 开放平台开发者
allowed-tools: Read, Bash
---

# 招投标全案合规审计（免费）

> 一句话：把一个项目的投标材料先做一轮免费的AI体检：报价算术 + 模板占位符，不需要付款，也不需要注册。

**完全免费**：不需要付款、不需要注册、不需要配置任何 API Key，直接调用即可。

## 什么时候用

- 标书刚拼完，想先扫一遍有没有没替换掉的模板痕迹
- 想先核一遍各家报价的算术，再决定要不要做更完整的审查
- 递交前想先做一轮零成本的自检

## 这个免费版查什么

| # | 检查项 |
|---|---|
| 1 | 逐家报价算术校验 |
| 2 | 模板占位符扫描 |

- 逐家报价算术校验：每行核对「合价 = 数量 × 单价」，按投标人归集
- 模板占位符扫描：搜出残留的 `【…】`、`XXX`、`＿＿`、`（此处填写）` 这类没替换干净的地方

## 这个免费版不包含

以下检查项**不在本版本范围内**，调用时也不会执行：

- 招标文件要素体检
- 合同草案必备条款与陷阱条款扫描
- 跨家串通线索
- 统一整改清单与阻断判定

## 怎么调用

### 方式一：命令行脚本（最省事）

```bash
node scripts/run.mjs --sample
node scripts/run.mjs --input my-input.json
node scripts/run.mjs --input my-input.json --json
```

### 方式二：直接引用引擎（接进自己的流程）

脚本本身不做计算，真正的检查在同目录的 `scripts/engine/tender-compliance-audit.js`（纯 Node 标准库，CommonJS），可以直接引用：

```js
const engine = require('./scripts/engine/tender-compliance-audit.js');
const outcome = engine.run(payload);
// outcome.status === 'success'            → outcome.result 就是结果
// outcome.status === 'insufficient_input' → outcome.missing 列出缺什么（此时不出结论）
```

所有检查都在**本机**完成：核对过程不外发材料、不需要任何凭证。

## 入参

给一个 bidders 数组。每家可带报价明细 items 与投标材料正文 text（占位符扫描读的是 text）。本版本不做分项加总校验，所以投标总价 price 字段不使用。

```json
{
  "bidders": [
    {
      "name": "河南甲建设有限公司",
      "price": 1000000,
      "items": [
        {
          "name": "钢筋制安",
          "qty": 10,
          "price": 100,
          "amount": 900
        }
      ],
      "text": "投标报价壹佰万元整 法定代表人：王五 盖章 承诺【填写：项目名称】"
    }
  ]
}
```

## 返回

返回 `ok: true` 与 `result`：`checks_given` **原样列出本次实际执行了哪些检查项**，
`checks_withheld` 列出本版本不包含的检查项。**不会用默认值编造结论。**

材料不足时（入参为空、只有空白、只有一个字符、解析不出任何明细行）**不出结论**：
会说明缺什么，并以退出码 `3` 结束；正常执行退出码为 `0`。

## 使用限制

- 在本机执行：核对过程不外发材料、没有调用次数上限，也不需要任何凭证。
- 输出的是**AI核对结果**，不是认定、不是评分。

## 反模式

- ❌ 把它的输出当作评标结论 —— 它只做AI核对，认定权在评标委员会。
- ❌ 拿它替代对招标文件的实质响应检查 —— 本版本不含该类检查。
- ❌ 输入残缺时怪结果不对 —— 检查项依赖你提供的字段，缺字段的检查项不会被伪造出来。

## 需要完整档时（可选）

本免费版是**完整可用的核心产出**，本版本**不包含**下面这些项：

- 招标文件要素体检
- 合同草案必备条款与陷阱条款扫描
- 跨家串通线索
- 统一整改清单与阻断判定

同名工具的**完整档**是另一个独立商品（条款与条件以它自己的商品页为准）；两档的差别**就是上面这些，没有别的**。

## 边界与免责

只做文本层面的缺陷扫描，不构成法律意见，也不替代评标委员会的专业判断。

本技能的所有结论都可由第三方用同一份输入复算出来。
