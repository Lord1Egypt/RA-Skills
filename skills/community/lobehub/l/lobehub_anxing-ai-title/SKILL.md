---
name: anxing-ai-title
description: "利用本地 LLMs 已训练拆封商品标题信息。"
source: LobeHub
tags: [电商, 文字处理]
compatible: [claude-code, openai-agents, hermes-agent, any-llm]
---

# 商品标题拆分

请分析以下客户发送的消息，提取出型号、规格和品类信息，并以 CSV 格式输出，不要添加任何额外信息。确保以下信息按列排列：

消息内容为："{客户发送的动态消息}"。

请输出格式如下：
大类，品类，品牌，型号
办公生活，轮椅，鱼跃，H062
