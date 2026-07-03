#完整 Prompt模板（变量化版本）

可用 `envsubst` 直接渲染：`envsubst < references/prompt.md > /tmp/prompt-rendered.md`

```text
【每日资讯任务】按 cron计划推送 ${ARTICLE_COUNT} 篇文字（不发图）。

【硬性白名单】话题必须来源于以下企业之一，其他公司一律不发：
${WHITELIST}

【操作步骤】
1. 用 web_search工具搜索上述白名单企业过去24小时内的最新动态（中英文各搜一次）。${SEARCH_PROVIDER} 默认每条结果带 content摘要（200-500字），这就是正文基础。
2.筛选出最有爆点的 ${ARTICLE_COUNT} 条热点（最好来自不同公司）。
3. **不要再调用 web_fetch** —— 这台机器抓 Bloomberg/Reuters/Yahoo全部超时或403。每条只用 ${SEARCH_PROVIDER} 返回的 content字段即可。
4. **不要发图片**，也不要 image_generate（SEND_IMAGE=false 时强制不生成）。
5.写一篇 ${WORDS_PER_ARTICLE} 字左右中文短文，基于 ${SEARCH_PROVIDER} content摘要提炼关键事实，每篇文末标注"来源：[媒体名] [URL]"。
6.发送：${ARTICLE_COUNT} 条文字消息，依次发到 ${RECIPIENT}。

【硬约束 —违反任何一条则中止任务不发】
- 只准用 ${SEARCH_PROVIDER} content摘要里写明的事实，禁止脑补数字、人名、日期
- **不发图、不调用 image_generate**（除非 SEND_IMAGE=true 且明确指示）
- **避免触发内容过滤**：不写"${SENSITIVE_WORDS}"等敏感词；如选中的话题包含敏感词，换个白名单企业的话题
-话题必须来源于白名单（${WHITELIST}），其他公司一律不发
- 每篇必须有可验证的来源 URL（${SEARCH_PROVIDER} 返回的 source URL字段）
- 如果凑不到 ${ARTICLE_COUNT} 条真实热点，宁可少发也不要凑数或编造

【报告】
任务结束后简短报告：发了X条、每条的企业归属、每条的来源URL、字数。
```

## 默认值（变量未设时的 fallback）

如果用户没设这些环境变量，下面是默认值：

|变量 | 默认值 |
|---|---|
| `${ARTICLE_COUNT}` | `3` |
| `${WHITELIST}` | `OpenAI·Google·NVIDIA·Anthropic·DeepSeek·阿里巴巴·字节跳动·Tesla·SpaceX` |
| `${SEARCH_PROVIDER}` | `tavily` |
| `${WORDS_PER_ARTICLE}` | `400` |
| `${SENSITIVE_WORDS}` | `武器/生物/政治/中国政策` |
| `${RECIPIENT}` | `o9cq808Uh5iap7dzqHDbRTzQ1JS4@im.wechat` |

##渲染示例

```bash
#默认配置（M2.7 +400字 + Tavily +微信）
envsubst < references/prompt.md > /tmp/prompt-default.md

#换成500 字 + M3 + brave
export MODEL=minimax/MiniMax-M3
export SEARCH_PROVIDER=brave
export WORDS_PER_ARTICLE=500
envsubst < references/prompt.md > /tmp/prompt-m3-500.md

#换白名单（加上 Meta）
export WHITELIST="OpenAI·Google·NVIDIA·Anthropic·DeepSeek·阿里巴巴·字节跳动·Tesla·SpaceX·Meta"
envsubst < references/prompt.md > /tmp/prompt-meta.md
```

##注意事项

1. **白名单分隔符**：`·`（中文中点）— 别换成英文逗号，避免被 cron / shell解释错
2. **敏感词分隔符**：`/`（斜杠）—方便 prompt 里当作一串列出
3. **变量未定义时**：`envsubst` 会保留 `${VAR}` 字面值传给 agent；agent看到 `${VAR}` 时会按 prompt字面意思处理，可能出错。**务必先用 `env -u`或显式 export**
4. **SEND_IMAGE=true 时**：prompt 中需要额外补充图片获取逻辑（不在本默认模板里）