---
name: vision-understanding
description: >
  Turn images, video, audio, or documents into text. Use when the user says
  "what's in this image", "describe / caption this", "tag these photos", "read
  this document / receipt / screenshot", "summarize this video", "transcribe
  this audio", "answer questions about this picture", or wants OCR, alt-text, or
  structured extraction from media. Any "media in, text out" task.
---

# Vision and media understanding

Take a media input (an image, a video, an audio clip, a document) and produce text about it: a direct answer, a caption, tags, extracted fields, a transcript, a summary. The lever is matching the input modality to a model that accepts it, then asking for exactly the text shape you want.

## Inputs to collect

- **The media** to understand, as a URL or base64 (image, video, audio, or a document rendered to image/PDF).
- **The input modality** - image, video, or audio. This is the primary routing decision.
- **What text you want back:** a free-form answer, a one-line caption, a tag list, structured fields (JSON), a transcript, or a summary.
- Optional: the question or instruction (visual Q&A), and whether output must be machine-parseable (then ask for JSON explicitly).

## Models

Route by input modality. Confirm the live model + its schema via the `runware-models` + `runware-run` skills before calling - never hardcode a stale choice.

- **Image → text (default): Qwen2.5-VL-7B-Instruct** (`runware:152@2`) - hosted, instruction-tuned for captioning, visual Q&A, and structured extraction. Good price/quality default.
- **Image → text (premium / reasoning): Gemini 3.1 Pro** (`google:gemini@3.1-pro`) - flagship multimodal, strong on documents, charts, dense OCR, and multi-step reasoning over an image.
- **Image → text (cheap / fast alts):** Qwen2.5-VL-3B-Instruct (`runware:152@1`), LLaVA-1.6-Mistral-7B (`runware:150@2`), or Gemini 3.1 Flash Lite (`google:gemini@3.1-flash-lite`) for high-volume tagging.
- **Video → text: Gemini 3.1 Pro** (`google:gemini@3.1-pro`) for summarization and Q&A over a clip; **Memories Video Captioning** (`memories:1@1`) for structured captions with speaker labels and optional chapter summaries.
- **Audio → text: Gemini 3.1 Pro** (`google:gemini@3.1-pro`). Audio-to-text is single-vendor today - only the Gemini family carries `io:audio-to-text`, so there is no non-Google fallback for pure audio.
- **Documents:** render to image or PDF and route as image → text. Gemini 3.1 Pro handles multi-page and dense layouts best.

## Workflow

1. **Decide the path by modality and by model type.** Chat-style models (Gemini, Qwen-VL, LLaVA) carry `io:image-to-text` / `io:video-to-text` / `io:audio-to-text` and run as a chat call against the OpenAI-compatible endpoint (`api.runware.ai/v1`). Dedicated caption models carry `op:caption` and run as a generation task (its own `taskType`), not a chat completion.
2. **Resolve the schema** (`runware-run`) and confirm the exact input field and the message/content shape before calling. Mirror its field names exactly.
3. **Attach the media** as a URL or base64 under the documented input field. Local files upload first.
4. **Ask for the text shape you want** in the instruction: a caption, tags, an answer, or "return JSON with keys X, Y". For `op:caption` models, set the caption options the schema exposes rather than free-prompting.
5. **Run with the right delivery mode.** Image and short-audio understanding return quickly and can run synchronously. Long video or long audio is a time-based job - run async and poll `getResponse` until terminal (see `runware-run`).
6. **Read the result as text** and validate it against what you asked for (correct fields present, transcript complete, no hallucinated detail).

## Technique

- **Pick by what goes in, not by brand.** The whole decision is the input modality. Image and document → a vision-language model. Video → a video-capable model. Audio → Gemini. Sending a video to an image-only model fails the schema gate.
- **Ask for the output shape explicitly.** "Describe this" yields prose. For tags, say "list 10 keywords". For extraction, say "return JSON with fields date, total, vendor" and the chat models comply. Underspecifying the shape is the main cause of unusable output.
- **Two surfaces, two contracts.** Chat-style VLMs (Gemini, Qwen-VL, LLaVA) take an image alongside a text instruction in a chat message and answer conversationally - use the OpenAI-compatible endpoint. `op:caption` models (Qwen-VL and Memories also expose this) are a single-shot generation task driven by caption options, not by a free instruction.
- **For documents and dense OCR, prefer the reasoning tier.** Gemini 3.1 Pro reads small text, tables, and multi-column layouts more reliably than the small hosted VLMs. Render each page to an image or pass the PDF.
- **For video, separate "summarize" from "caption".** Gemini answers open questions and summarizes a clip. Memories produces structured captions with speaker labels and chapter-style markers - use it when you need navigable, labeled output rather than a free answer.
- **Stay grounded.** Ask the model to report only what is visible or audible and to say so when something is not present. Do not let it invent text it cannot read or details off-frame.

## Parameters that matter

- **Input field** - the media goes under the model's documented input field (an image/video/audio reference in the chat message content, or the caption task's input field). Confirm the exact name against the live schema; never guess.
- **Instruction / question** - the text prompt that sets the task (caption vs Q&A vs extraction). For `op:caption` models, use the schema's caption options instead.
- **`op:caption` is text-output only.** Media output params (output type/format/quality, upload endpoint) do not apply and are removed from caption base types. Only `memories:1@1` enforces this gate; other caption models accept-and-ignore them, but do not rely on that.
- **Delivery mode** - sync for images and short clips, async + poll for long video/audio.
- For chat-style calls, the OpenAI-compatible endpoint takes the usual completion controls (e.g. token limit, temperature); keep temperature low for factual extraction.

## Quality bar

- The model used actually supports the input modality (verified against its capabilities, not assumed) - no image-only model fed a video.
- The output is in the requested shape (a caption is one line, tags are a list, JSON parses, a transcript is complete).
- Every claim is grounded in the media: no invented text, objects, or speakers. Unreadable or absent detail is reported as such, not fabricated.
- For long media, the job ran async and was polled to completion rather than blocking a sync call.

## Related skills

`runware-run`, `runware-models`, `runware-prompting`; `llm-agent` (text-only reasoning and tool use once the media is described, the sibling outcome on the OpenAI-compatible endpoint).
