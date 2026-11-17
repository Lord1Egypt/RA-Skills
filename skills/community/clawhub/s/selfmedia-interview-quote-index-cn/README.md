# 采访原话摘引清单

从已获授权的采访逐字稿中快速找出能安全使用的原话：每条都附原说话人、时间或段落位置、必要上下文与公开范围，避免把摘要、润色或断章句误作采访引语。

![采访原话摘引清单推广图](assets/promo-1600x900.png)

## 输入与结果

输入一份最多 6,000 字的逐字稿、说话人/时间锚点（缺失时可用段落编号）、选题和允许公开的范围。输出不超过 15 条可用短引语，以及禁用或待确认项；每条可用项都可回到原文定位，并保留否定与关键限定。

没有逐字稿、身份或授权范围不清时，Skill 会停止把内容称作原话，改为清楚列出需要补充的材料。

## 安装

```bash
npx skills add xxjrq/selfmedia-interview-quote-index-cn
```

## 使用

提供材料后，说明主题和公开边界，例如：

```text
请从以下已授权逐字稿中找出“产品验证”主题的可用原话。可署名用于公众号；保留说话人、时间锚点和必要上下文。没有把握的项请放入待确认。
```

完整规则与交付模板见 [SKILL.md](SKILL.md)。可复制的成功材料与结果见 [fixtures/success-input.md](fixtures/success-input.md) 和 [fixtures/success-output.md](fixtures/success-output.md)；缺料分支见 [fixtures/failure-input.md](fixtures/failure-input.md) 和 [fixtures/failure-output.md](fixtures/failure-output.md)。

## 边界

只筛选忠实、可追溯的已有原话。不会采访、拟问题或发布；不会删掉否定或关键限定来改变原意，也不会把改写句标成原话。

## 自检

```bash
bash scripts/self-test.sh
```

本自检核验发布文件、图像尺寸和两份可执行参考分支；它不把结构检查伪称为模型质量验证。

## 来源与许可证

业务用途参考了 [marketingskills 的 content-strategy 目录](https://github.com/coreyhaines31/marketingskills/tree/main/skills/content-strategy)，本仓库的说明、步骤和示例均为原创，未复制其文本或代码。以 [MIT-0](LICENSE) 发布。
