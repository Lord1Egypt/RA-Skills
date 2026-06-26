---
name: wechat-comic-factory
description: Generate WeChat comic articles and publish them to the WeChat Official Account draft box by executing local Python pipeline scripts. Use when the user wants to create a comic series from comic_type, topic, and count, or publish the latest generated task. In this skill, “发布” and “发微信” always mean only pushing to the WeChat Official Account draft box; never reinterpret them as personal chat, group chat, or message-tool sending.
---

# Wechat Comic Factory

Execute local commands first. Do not replace execution with creative brainstorming, platform advice, prompt collections, or simulated publish confirmations.

## Execute Only Local Entrypoints

Use only these public entrypoints:

```powershell
python scripts/run_pipeline.py --comic_type "小林漫画" --topic "成年人的体面" --count 3
python scripts/run_pipeline.py --comic_type "育儿漫画" --topic "当妈三年我学会了精打细算" --count 4
python scripts/run_pipeline.py --publish_latest
python scripts/run_pipeline.py --publish_output_dir "<existing_output_dir>"
```

Do not expose底层多脚本串联命令给用户，不要跳过 `run_pipeline.py` 直接拼接发布流程。

## Config Guardrail

If the local script returns `stage = config`, or the error message indicates `config.json` is missing / still placeholder:

1. Stop execution reporting immediately.
2. Tell the user to create `config.json` from `config.example.json`.
3. Ask them to fill real `text_llm`、`image_llm`、`wechat` credentials before retrying.

Use a short, direct response such as:

- `当前还没有可用配置。请先在技能根目录把 config.example.json 复制为 config.json，并填入真实模型与公众号配置。完成后我再执行。`

Do not fabricate partial success, draft status, or publish status when configuration is incomplete.

## Generation Rules

When the user asks to generate comics:

1. Parse `comic_type`, `topic`, and `count`.
2. If `count` is missing, default to `3`.
3. If `comic_type` is missing, ask for the type.
4. If `comic_type` is unsupported, report the supported types directly.
5. Execute `python scripts/run_pipeline.py ...`.
6. Return the script JSON result instead of writing creative copy first.

Supported types:

- `小林漫画`
- `育儿漫画`

Never rewrite the user’s topic unless they explicitly ask for rewriting.

## Publish Rules

In this skill, “发布” means only:

- push to **微信公众号草稿箱**

It must never mean:

- personal WeChat chat
- WeChat group
- current chat reply
- message tool sending
- any other external channel

When the publish target is clear:

1. Use `python scripts/run_pipeline.py --publish_latest` for the latest pending task.
2. Use `python scripts/run_pipeline.py --publish_output_dir "<path>"` only when a specific task directory is explicitly identified.

## Clarify Ambiguous Follow-ups

Clarify instead of guessing when the user says:

- `发布这个`
- `直接发`
- `发出去`
- `1，2直接发布`
- `直接发微信`

Recommended clarification style:

- `我当前只支持推送到微信公众号草稿箱。你是要发布最近一次生成的整组内容吗？`
- `最近任务是《成年人的体面，藏在细节里》三张系列。是否推送该整组内容到微信公众号草稿箱？`
- `我暂不支持只发布前两张。你是要发布整组内容，还是先重新生成一组两张的版本？`

Do not ask about contacts, group chats, personal accounts, GitHub, blog platforms, or other channels.

## Success Rules

You may say:

- `已发布`
- `已推送到公众号草稿箱`
- `草稿已创建成功`

only when the script JSON result includes both:

- `success = true`
- `draft_status = success`

Otherwise say only:

- `已生成待发布内容`
- `尚未发布`
- `发布失败，失败阶段为 xxx`
- `未检测到可用微信草稿发布结果`

If the script fails, report the real `stage` and `error` fields. Never convert a failed script run into a success message.
