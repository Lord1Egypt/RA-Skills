---
name: wiro-models
description: "Search the Wiro AI catalog of 1,000+ models, compare them and read their inputs and prices, for free. Use when the user asks which Wiro AI model fits a job, what Wiro AI models cost, or how two models compare."
---

# Wiro AI: find models and prices

Request: the user's request in this conversation

This skill only reads. It never runs a model and costs nothing. If you cannot see the Wiro MCP tools, the `wiro` server may still be connecting: wait for it and look again. If they are still missing, tell the user to connect the Wiro MCP server: add the remote server `https://mcp.wiro.ai/v1` (Streamable HTTP) under the name `wiro` and sign in with a Wiro account when the client asks, or send a Wiro API key as a Bearer token. In Claude Code that is `claude mcp add --transport http wiro https://mcp.wiro.ai/v1`; setup for other clients is at https://wiro.ai/docs/wiro-mcp-server.

- A job or key words ("upscale", "video with sound", "cheapest text to speech"): call `recommend_model` with two or three key words and `search_models` with the matching category.
- A category (`text-to-image`, `image-to-image`, `image-editing`, `text-to-video`, `image-to-video`, `video-to-video`, `text-to-speech`, `speech-to-text`, `text-to-music`, `text-to-song`, `voice-clone`, `3d-generation`, `llm` and others): `search_models` with that category, `limit` up to 100, sorted by `ratedusercount` unless the user wants the newest (`time`).
- A model (`owner/slug` or a name): `get_model_schema`, then explain what it takes (inputs, options, limits, defaults) and its price at the default settings and at the settings the user cares about.
- `--cheapest`: list the category, compare the prices, and check the two or three cheapest with `get_model_schema` at the settings asked for before you name one. A price shown as a range depends on settings such as resolution or length.
- `--compare a b`: read each one with `get_model_schema` and compare inputs, limits and price at the same settings.
- Empty: `explore`, and show its curated groups.

Answer with a table: the model as `owner/slug` exactly as the tools return it, its name, what it is good for, and the price with its unit (per run, per image, per second, per 1M tokens). Say when a price is only known after the run, or when the run is charged for the time it takes. End with one line naming the skill that runs the model they pick, with `--model <owner/slug>`: the `wiro-image` skill or the `wiro-edit-image` skill for images, the `wiro-video` skill for video, the `wiro-speech` skill for speech, the `wiro-music` skill for music, the `wiro-transcribe` skill for speech to text and the `wiro-3d` skill for 3D.
