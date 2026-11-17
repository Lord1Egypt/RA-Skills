# wechat-article-ai-check

> 微信公众号文章 AI 检查 skill —— 检查创作度、原创增量、同质化、搬运拼凑、信息量与低价值 AIGC 风险，并给出可执行的改写建议。

## 它解决什么

当用户丢来一篇微信公众号文章，要求"检查是不是 AI 写的 / 有没有同质化 / 会不会被平台误判 / 帮我改得更有原创感"时，这个 skill 给出**可验证、不臆测**的检查流程。

## Features

- **两阶段执行**：先检查给建议，用户确认后再改写，不在未确认时附送完整稿。
- **创作度优先**：把"可验证的原创增量"作为最高优先级，不根据同义词替换或第一人称猜测作者是不是 AI。
- **六维风险表**：原创增量 / 同质化 / 搬运拼凑 / 信息量 / 低价值 AIGC / 排版与编辑投入，每项都引原文证据。
- **明确边界**：平台风险无可靠安全分数，不承诺过审、不虚构平台规则、不教授对抗检测。
- **绝对红线**：内容空洞与虚构论据零容忍，缺失关键材料用 `[请补充：……]` 占位而非编造。

## Quick Start

```bash
git clone https://github.com/Songhonglei/better-article-writing.git
# 把 skills/wechat-article-ai-check 复制到你的 Agent skills 目录
cp -r better-article-writing/skills/wechat-article-ai-check ~/.workbuddy/skills/
```

## 使用示例

> 用户："检查这篇文章，先给意见。"
> 正确行为：给总体结论、创作度盘点、六维风险表、提升方案和待补材料，然后询问是否改写并停止。

> 用户："按这些建议改吧。"
> 正确行为：给完整修改稿、修改原因、仍缺的原创材料和发布前核实项。

## License

MIT (see [./LICENSE](./LICENSE))
