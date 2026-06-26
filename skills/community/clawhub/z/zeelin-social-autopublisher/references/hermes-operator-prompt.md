# Hermes Operator Prompt

下面这两段提示词是给 Hermes 直接调用 `zeelin-social-autopublisher` 时使用的。

## 审核模式

目标：先生成内容与结构化工件，不直接发布。

```text
Use the zeelin-social-autopublisher skill.

Before choosing the topic, gather at least 2 current AI news signals from the web or browser results.
Then compress them into one operator topic for all platforms: "{TOPIC}".

Run the Hermes wrapper in review mode for topic: "{TOPIC}".

Requirements:
- Use all requested platforms: {PLATFORMS}
- Generate content artifacts and a structured summary
- Do not publish anything
- Return the run directory path
- Summarize next_action from summary.json
- Summarize the chosen hot-topic angle in one sentence
- Apply self-media viral-content standards, not generic brand copy
- Every platform copy must include: a hook in the first 1-2 lines, a clear judgment, 2+ concrete signals, and at least one line with screenshot-worthy传播感
- For X/Twitter, avoid overly short copy; prefer a dense single-post structure with a clear hook, 2-3 concrete signals, and a forward-looking judgment
- For Weibo, use short-paragraph rhythm plus interaction bait at the end
- For Xiaohongshu, title must be click-oriented and body must feel collectible/searchable
- For WeChat, article must have a strong opening scene, clear section rhythm, and 2+ quotable lines
- If content generation falls back to template copy, clearly say that human editing is required before publish
```

## 发布模式

目标：复用已经审核过的内容 JSON，直接按顺序发布。

```text
Use the zeelin-social-autopublisher skill.

Run the Hermes wrapper in publish mode for topic: "{TOPIC}".

Requirements:
- Use only these platforms: {PLATFORMS}
- Reuse approved content from: {CONTENT_JSON}
- Do not regenerate content
- If approved content already exists, topic may be omitted and the wrapper should still run
- Return the run directory path
- Summarize platform-level success or failure from report.json
- If any platform fails, identify which platform needs manual follow-up
```

## 推荐原则

- Hermes 优先运行 skill 自带包装脚本 `scripts/run_hermes_agent_ops.sh`
- 审核阶段与发布阶段分开，避免未审稿件直接发出
- 自动化流程优先读取 `summary.json` 和 `report.json`，不要依赖终端日志解析
