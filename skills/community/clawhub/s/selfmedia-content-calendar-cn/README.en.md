# Two-Week Content Calendar

![Two-Week Content Calendar promo](assets/promo-1600x900.png)

Turn existing materials and available production time into an actionable 14-day content calendar. Built for Chinese small-shop owners, fiction writers, and independent creators.

Provide account positioning, a materials inventory, capacity, and fixed topics. The Skill returns a day-by-day topic sequence, format, material needs, and production-time guidance. Missing critical fields are called out rather than invented.

This is a pure Markdown Skill: no login, browser, or third-party API is required. It plans production only; trend discovery, publishing, and post-publishing analytics are out of scope.

## Use

Send the four input fields described in [SKILL.md](SKILL.md). Run the package check with:

```bash
bash scripts/self-test.sh
```

The Chinese guide is available in [README.zh-CN.md](README.zh-CN.md).

## Source and license

The implementation and fixtures are original. Scope only was checked against [social-media-skills/skills](https://github.com/social-media-skills/skills) and its [batch-content-plan Skill](https://github.com/social-media-skills/skills/blob/main/skills/batch-content-plan/SKILL.md); no source code or copy was reused. Released under the [MIT-0](LICENSE).

## Install / 安装

```bash
npx skills add xxjrq/selfmedia-content-calendar-cn
```

[成功输入](fixtures/success-input.json) · [实际参考交付](fixtures/forward-success.md) · [缺料分支](fixtures/forward-failure.md)。样例为离线材料上的 Markdown 执行参考，自检仅检查包结构和样例约束。
