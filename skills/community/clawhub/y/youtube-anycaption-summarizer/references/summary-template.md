# Summary Template

Use the requested summary language.
- If `summary-language=source`, keep the same language as the source transcript when it is clear.
- If the apparent source language is unclear, first infer the main transcript language from the transcript itself, backfill that language into both markdown files, and then write the summary in that language unless the user requested another one.
- If the user explicitly requests another language, write the summary in that language.

## Required sections
- 视频标题 / Video Title
- 来源 / Source
- Video ID
- Source Transcript
- Summary Language
- Transcript Source Method
- Executive Summary
- Key Takeaways
- Step-by-Step Execution / Deployment Details
- Tools / Platforms Mentioned
- Caveats / Notes
- Bottom Line

## Writing rules
- Fully replace any placeholder content. Do not leave `## Status`, filler text, draft notes, or unused template text in the final output.
- Use the transcript and available metadata to produce a summary that serves two purposes at the same time:
  1. Help the reader quickly understand the video’s main message, structure, and conclusions.
  2. Capture enough operational and technical detail so the reader can reproduce, deploy, test, or adapt the use case, workflow, or technology explained in the video.
- Correct obvious grammar, punctuation, and transcription errors only when the intended meaning is clear from context.
- Preserve product names, company names, model names, APIs, frameworks, datasets, metrics, and technical terminology with high precision.
- If a technical term is unclear or the transcript is ambiguous, mark it as approximate or uncertain instead of guessing.
- Prioritize both strategic meaning and implementation detail:
  - explain what the speaker is trying to achieve,
  - why it matters,
  - how the workflow or system works,
  - what tools, steps, inputs, and decisions are required,
  - and what constraints or risks affect success.
- In videos about business development, AI/BI workflows, automation, product strategy, or technology explanation, extract practical details as concretely as possible, such as:
  - business problem being solved,
  - target users or customers,
  - workflow steps,
  - system architecture,
  - model choices,
  - data inputs and outputs,
  - evaluation methods,
  - deployment process,
  - costs, tradeoffs, limitations, and operational dependencies.
- Prefer concise, structured writing. Use short paragraphs and bullet lists instead of long transcript-like blocks.
- Organize the content so a reader can scan it quickly, but still recover the important technical and operational details without rewatching the video.
- **The section `Step-by-Step Execution / Deployment Details` is mandatory and must be highly informative.** Treat it like a beginner-friendly runbook, not a vague recap.
- In `Step-by-Step Execution / Deployment Details`, capture as many of the following as the transcript supports:
  - prerequisites, environment, hardware/software assumptions
  - accounts, permissions, API keys, auth steps, and integrations
  - installation/setup steps in actual execution order
  - configuration parameters, model choices, flags, commands, files, and settings
  - workflow stages, inputs, outputs, intermediate artifacts, and cleanup steps
  - deployment/launch process, operational checks, validation steps, and monitoring
  - failure points, caveats, human-in-the-loop steps, and decision criteria
- When the video explains a strategy, architecture, or automation system, make the section detailed enough that a beginner could reproduce the same setup or adapt the same strategy using only the summary plus the original assets they already have access to.
- Do not collapse many concrete steps into one generic sentence when the transcript provides specifics.
- If a key implementation detail is implied but not explicitly stated, label it clearly as an inference. If a needed detail is missing, write `Not clearly stated in the transcript` rather than inventing it.
- Do not omit important setup requirements, permissions, assumptions, dependencies, routing logic, integrations, model/tool choices, human-in-the-loop steps, or caveats that materially affect execution.
- If the transcript is noisy, incomplete, repetitive, low-quality, or low-information, state that clearly in Caveats / Notes and keep the summary appropriately conservative.
- If the transcript source is subtitles, OCR, auto-captions, or Whisper, preserve any source-related limitations that affect confidence, terminology accuracy, speaker attribution, or completeness.
- Do not turn the summary into a generic overview. Keep it grounded in what the video actually says.

## Minimum honesty standard
- Do not add facts, claims, steps, tools, or conclusions that are not supported by the transcript or obvious metadata.
- Do not infer implementation details unless the transcript gives a reasonable basis. When inference is helpful, label it clearly as an interpretation rather than a confirmed fact.
- If the transcript is too short, too noisy, or too incomplete to support a detailed summary, say so explicitly.
- When confidence is low, make the uncertainty visible in the relevant section instead of writing with false precision.
- If a section cannot be filled reliably from the available input, say `Not clearly stated in the transcript` rather than fabricating content.
