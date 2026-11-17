# Self-media Title Rewriter

![Chinese social media title rewriting](assets/promo-1600x900.png)

Turn one Chinese content brief into three differentiated titles each for Douyin, Xiaohongshu, and Bilibili, plus one recommendation. Provide the core benefit, body, and target platforms to get copy-ready options based on your facts. No browser or additional API key is required.

## Use it now

Provide a core benefit, body text, and one or more platforms. The Skill returns copy-ready titles plus a concise recommendation. If a required field is absent, it identifies the missing material instead of inventing facts. See [the successful fixture](fixtures/success-output.md).

## Scope

- Built for Chinese independent creators and small-shop operators.
- Uses only supplied, verifiable facts; optional audience, tone, and restricted words are welcome.
- Produces titles and a recommendation reason only.
- No browser, account, or external service is required, so it never accesses login state or publishing platforms.

## Validate

```bash
node scripts/self-test.mjs
```

Original title-writing instructions and examples, licensed under [MIT-0](LICENSE).

## Install

```bash
npx skills add xxjrq/selfmedia-title-lab-cn
```

Alternatively, copy this repository folder into your Agent’s skill directory, then invoke `$selfmedia-title-lab-cn` with your input.
