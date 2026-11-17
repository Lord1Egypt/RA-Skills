---
name: qwen-web-reviewer
description: GPT-only reviewer workflow for Qwen Web using the authenticated ChatGPT Work/Codex Cloud Browser. Requires GPT browser-control; not an OpenClaw-native integration.
---
> **Platform note:** This package depends on the GPT/ChatGPT Work Cloud Browser and its browser-control skill. It is not directly executable in a standard OpenClaw runtime unless equivalent browser capabilities are provided.


# Qwen Web Reviewer

Use Qwen Web at `chat.qwen.ai` through the authorized Cloud Browser session. This skill is a web-interface workflow, not an API integration. Do not use a Qwen API, API key, paid endpoint, hidden network request, or an unapproved local browser workaround.

## Operating contract

- Treat Qwen as an independent reviewer, not as an authority. Compare its answer with the primary agent's reasoning, supplied documents, and primary sources.
- Use Qwen proactively as an independent consultant whenever an important question remains unclear, multiple interpretations are plausible, or a second opinion could reveal an error. Ask it to challenge assumptions and identify counterarguments rather than merely confirm the current conclusion.
- Qwen's response is advisory evidence only. The primary agent retains responsibility for checking facts, weighing conflicting evidence, stating uncertainty, and making the final decision. Never transfer final authority to Qwen or present its answer as verified solely because it sounds confident.
- When this skill is invoked, use the newest suitable model currently exposed in the live Qwen UI and enable Thinking/Reasoning/Deep Thinking. Never hard-code a model name as permanently current.
- Keep user data minimal. Before transmitting sensitive personal, proprietary, medical, financial, credential, or confidential project information to Qwen, obtain the user's explicit authorization for that material and destination. Do not transmit passwords, OTPs, session tokens, cookies, or private browser data.
- Do not upload files unless the user explicitly asks for Qwen to inspect them or has clearly authorized that transfer. Prefer a short, redacted text excerpt when it is sufficient.
- Never accept Qwen output as verified merely because it is detailed or confident. Preserve uncertainty and provenance.

## Browser and session

1. Use the available browser-control skill before interacting with Qwen. Reuse the existing Qwen tab when it is live; do not create unnecessary tabs or reload an active conversation.
2. Verify that the visible page is Qwen Studio and that the account is signed in. A visible user profile, sidebar, model picker, and working composer are positive signs of authentication. Do not ask the user to log in or create a new tab when those signs are present; request manual login only when the current visible page actually shows `Войти`/`Sign in`, `Зарегистрироваться`/`Sign up`, a login form, CAPTCHA, bot check, or an equivalent blocking state.
3. Use the secure browser-auth capability for login or credential entry. Never request or enter a password, OTP, recovery code, or passkey through ordinary page automation. Passkeys are not supported in the Cloud Browser.
4. If Qwen requests CAPTCHA, 2FA, re-authentication, or a security decision, stop at the blocking step and offer the documented manual browser handoff. Do not solve or bypass a CAPTCHA without the required action-time confirmation, and do not claim that the session is persistent until a fresh Qwen page verifies it.

## Attachments through the Brave extension

Use this workflow only when the user asks Qwen to inspect an attachment or explicitly authorizes a file-transfer test.

- A local-file upload requires the Codex/ChatGPT browser extension's `Allow access to file URLs` permission. The Russian UI may call this `Разрешить открывать локальные файлы по ссылкам`; installing the extension alone is insufficient. If the user has just changed this setting, refresh the connected-browser inventory once because the extension may reconnect with a new browser ID. Then inspect the current user tabs and claim the existing Qwen tab; an empty agent-tab list does not mean the user tab or sign-in is missing.
- If browser policy blocks `brave://extensions` or another internal extension-settings URL, do not retry through another surface or raw browser commands. Ask the user to check the permission through Brave's normal UI.
- Read the browser's `file-uploads` documentation before attaching. Start `waitForEvent("filechooser")` before clicking the visible upload control or menu item, then pass an absolute local path to the chooser. In the observed Qwen UI, the plus control labelled `Выбрать режим` opened `Загрузить вложение` / `Файл, изображение, Видео, аудио`; inspect current labels because they can change.
- A page may have a hidden `input[type=file]`. Do not force-click it or use unsupported `setInputFiles`; inspect the live UI and click the visible control associated with that input. Keep the target unique so a broad selector cannot also match `Send`.
- Verify the expected filename is visible in the attachment preview before sending. For an explicitly requested smoke test, use a harmless, small text file with a unique expected token and count success only after the completed reply matches the token. Inspect the current chat/main response rather than dumping the whole sidebar or chat history.

## Select the model and Thinking mode

Inspect the live, rendered UI immediately before sending the first task. Use accessible labels, visible DOM, and a screenshot only when visual state is necessary; do not rely on guessed selectors or stale labels.

1. Open the model picker and collect the visible model names, version numbers, dates, and badges. Prefer an explicit `Latest`, `Newest`, `Новейшая`, or equivalent recency label on a model entry.
2. Otherwise rank candidates by the highest visible version/date, then by the strongest general-purpose or reasoning capability. Use a specialized Coder/VL/Omni model only when the task requires that modality; otherwise prefer the newest general reasoning model.
3. Treat an explicit recency label such as `Новейшая` in the model picker as live evidence of newness; generic claims such as `flagship` or `advanced` do not establish recency. If names remain ambiguous or no version/recency signal is visible, select the strongest suitable general model and report the ambiguity.
4. Enable the visible control labelled `Thinking`, `Reasoning`, `Deep Thinking`, `Extended thinking`, `思考`, or an equivalent. Verify the control's selected/on state after the click. If the selected model is explicitly thinking-only, record that fact rather than toggling a nonexistent switch.
5. If the current UI does not expose a Thinking control, do not simulate it with prompt wording and do not claim it is enabled. Report `Thinking: not visibly available`.
6. Record the exact visible model label and Thinking state for the final synthesis. Recheck after creating a new chat because Qwen may reset model settings per chat.

### Visible UI is authoritative

- Treat the live, rendered Qwen interface as the source of truth for the selected model and mode. If the model picker visibly shows a selected model, record that exact label; if the model entry or its description explicitly says `Latest`, `Newest`, or `Новейшая`, accept that as the newest available model.
- Treat a visible `Thinking`/`Мышление` label, selected switch, active mode indicator, or a completed response marked as reasoning/thinking as confirmation that the mode is enabled. Do not downgrade this conclusion merely because Qwen's text reply says it cannot identify its internal version or does not see a separate switch.
- If the UI and the model's self-description conflict, report both facts and resolve model/version status from the UI. Never claim that the mode is unavailable when the rendered UI visibly shows it active.

## Run a review

1. Create a new Qwen chat for an independent task unless the user asks to continue an existing Qwen conversation. Save the verified chat URL only if it is safe and does not contain session-bound secrets.
2. Formulate a focused prompt. Include the question, relevant facts, constraints, requested output, and the review role. For technical and engineering questions, ask Qwen to trace each conclusion to its source, then separate confirmed facts, contradictions, assumptions, and verification steps.
3. Prefer prompts that try to falsify the primary conclusion: ask for missed errors, counterexamples, alternative interpretations, unsafe assumptions, and the minimum evidence needed to resolve disputes.
4. Send the prompt through the visible composer. Sending a task to Qwen is an external transmission; ensure the user has authorized the included material before doing so.
5. Wait until generation has visibly completed. Read the complete answer, including code blocks, tables, citations, and any continuation. If Qwen offers `Continue`, use it only when the response is visibly incomplete and keep the same chat and settings.
6. For difficult or disputed results, ask one or more targeted follow-up questions in the same chat: first request a concise list of claims and evidence, then request a red-team critique of those claims. Stop when the answer becomes repetitive or no new evidence is produced.
7. If the DOM, selectors, chat URL, or page layout changes, stop and re-inspect the current visible state. Do not loop on stale selectors, blindly resend prompts, or use hidden page state.

## Chat isolation when the topic changes

Treat each Qwen chat as a separate consultant context. Do not carry a prior topic into a new subject merely because the same account or model is available.

### ChatGPT–Qwen chat pairing

- Pair each new ChatGPT task/chat with a new Qwen chat whenever Qwen is used for that task. Do not continue an older Qwen conversation just because the session, model, or settings are still available.
- When a new ChatGPT chat is created or the subject changes, open `Новый чат` in Qwen as well, verify that the Qwen conversation header/URL changed, and then re-select the newest visible model and verify `Thinking`/`Мышление` again.
- Keep the pair isolated: do not paste or reuse context from an older Qwen chat unless the user explicitly asks to continue that same subject. For a follow-up within the same ChatGPT task, reuse the paired Qwen chat only when the subject, source material, assumptions, and reviewer role are unchanged.

- Keep a compact topic label for the active chat, such as `project-review-2026-09`, `тренировки`, or `текущая политика`.
- Reuse the active chat only when the new request has the same subject, source material, assumptions, and desired role.
- Open a new chat through the visible `New chat`, `Новый чат`, plus, or equivalent control when any of these changes: subject domain, project/document, time period, person or account, confidential-data scope, or reviewer role.
- After opening a new chat, verify that the composer is empty and the conversation header/URL changed. Re-select the newest suitable model and re-enable or verify Thinking because Qwen may reset these settings per chat.
- Never continue a previous conversation merely to preserve model settings. Context separation has priority over convenience.
- For a follow-up on the same subject, keep the same chat and reference the earlier answer explicitly. For a new subject, start a new chat and do not paste the old answer unless it is intentionally part of the new task.
- Record the chat label, model label, Thinking state, and round count in the final synthesis; do not expose session-bound URLs.

## Synthesis and reporting

Compare Qwen's output against the primary analysis and available primary sources. Keep only conclusions supported by evidence or label them as inferences. Resolve disagreement explicitly:

- `CONFIRMED`: independently supported by the supplied material or a primary source.
- `QWEN_CANDIDATE`: useful lead from Qwen that still needs verification.
- `CONFLICT`: Qwen and the primary analysis disagree; show the exact issue and what would resolve it.
- `NOT_CHECKED`: the interface, source, or required artifact was unavailable.

When Qwen was used, state briefly: the exact visible model label, Thinking status, number of rounds, what role Qwen played, and which findings were accepted or rejected. Do not expose credentials, cookies, hidden reasoning, or session-bound URLs.

## Failure handling

Use the sequence `STOP → CAPTURE → MATCH → RUN → VERIFY`:

- **STOP**: stop after CAPTCHA, login failure, bot block, origin change, repeated timeout, or a changed UI.
- **CAPTURE**: capture the current visible URL origin, page title, visible DOM, and (when needed) screenshot; redact sensitive values.
- **MATCH**: match the state to a known condition: expired session, Qwen outage, rate limit, selector/layout change, incomplete generation, or browser transport error.
- **RUN**: make at most one low-risk recovery attempt allowed by the browser guidance, such as waiting briefly or reloading once. Do not evade site safeguards.
- **VERIFY**: require a positive visible signal—signed-in Qwen Studio, selected model, Thinking enabled, completed answer—before proceeding.

Never silently substitute a Qwen API, another account, another model, or a different service when the user requested Qwen Web. If the Cloud Browser cannot reach Qwen or its review quota is exhausted, report the exact blocking stage and continue the primary analysis without pretending that Qwen was consulted.
