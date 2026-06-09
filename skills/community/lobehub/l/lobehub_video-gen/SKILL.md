---
name: video-gen
description: "POST https://api.minimaxi.chat/v1/video_generation"
source: LobeHub
tags: [ai-assistant, tech-support]
compatible: [claude-code, openai-agents, hermes-agent, any-llm]
---

# task_id

curl --location 'https://api.minimaxi.chat/v1/video\_generation' \
\--header 'content-type: application/json' \
\--header 'authorization: Bearer ${api_key}' \
\--data '{
"model":"video-01",
"prompt":"On a distant planet, there is a MiniMax."
}'
