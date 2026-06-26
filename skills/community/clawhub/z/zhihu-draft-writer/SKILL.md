---
name: zhihu-draft-writer
description: "自动从知乎热榜选题、调用 AI 生成原创回答并保存为草稿，支持自定义话题关键词、写作风格和批量生成。\nDraft Zhihu answers automatically: picks hot questions, generates original answers via AI, and saves them as drafts — with custom topic filters, writing style, and batch support. Never publishes."
metadata:
  clawdbot:
    skillKey: zhihu-draft-writer
    emoji: "📝"
    os:
      - win32
      - darwin
      - linux
    primaryEnv: ZHIHUIAPI_KEY
    requires:
      env:
        - ZHIHUIAPI_KEY
      bins:
        - curl
---

# Zhihu Draft Writer

Use the host browser session that is already logged into Zhihu. Do not attempt automated login, do not ask for passwords, and do not use the publish action.

Before the first run, read `{baseDir}/references/setup.md`.
Before each run, resolve user options with `{baseDir}/references/runtime-options.md`.

## Operating Rules

- Use OpenClaw browser host control so the skill can work with the user's current Chrome session.
- Use `curl` to call the zhihuiapi inference endpoint directly for answer generation. Do not use llm-task, do not spawn a subagent for generation, and do not use the current session model to generate answer text.
- Save drafts only. Never click any control that publishes or submits the answer.
- Exclude political, sensitive, illegal, or legally risky topics from both topic selection and answer generation. See the **Legally Risky Content** section for specific examples.
- Stop immediately if Zhihu is not logged in, comments cannot be read, the answer editor cannot be found, the draft button is missing, or the model output fails validation.
- When `draft_count > 1` and a single draft fails (generation or save), skip that question, record the failure reason, and continue with the next eligible question. Report a summary of successes and failures at the end.

## Legally Risky Content

Skip or reject any content that falls into these categories:

- Political commentary targeting specific leaders, parties, or government policies
- Promotion of organizations or ideologies banned in China
- Medical misinformation or unlicensed treatment recommendations
- Financial fraud, unlicensed investment advice, or pyramid-scheme promotion
- Content that incites violence, ethnic hatred, or religious extremism
- Sexual content involving minors or non-consensual scenarios
- Illegal service solicitation (gambling, drugs, counterfeit goods)

When in doubt, treat the content as risky and skip.

## Runtime Options

Resolve these options from the user's request before opening Zhihu:

- `topic_mode`
- `custom_topic_keywords`
- `draft_count`
- `comment_count`
- `writing_style`

If the user does not specify them, use the defaults from `{baseDir}/references/runtime-options.md`.
Do not ask follow-up questions just to collect optional parameters.
When the user gives no parameter at all, use this default run mode:

- `topic_mode = general_hot`
- `draft_count = 1`
- `comment_count = 3`
- `writing_style.mode = default`

Process up to `draft_count` eligible questions in one run. Create one draft answer per selected question. Never exceed 5 drafts in a single run even if the user asks for more; cap at 5 and note the cap in the result.

## History File

The skill maintains a local deduplication log at `{baseDir}/data/history.json`.

**Format:**
```json
{
  "answered": [
    {
      "question_url": "https://www.zhihu.com/question/xxxxxxx",
      "question_title": "string",
      "saved_at": "2026-03-16T10:00:00Z"
    }
  ]
}
```

**Rules:**
- Before each run, read `{baseDir}/data/history.json`. If the file does not exist, treat `answered` as an empty array.
- During topic selection, skip any candidate whose `question_url` already appears in `answered`.
- After a draft is successfully saved (confirmed by Zhihu's save signal), append the entry to `answered` and write the file back immediately. Do not wait until the end of the run.
- If writing the history file fails, log a warning in the end-of-run report but do not stop the current run.
- Never delete or overwrite existing entries. Only append.
- The history file is append-only. It is the user's responsibility to prune old entries manually if desired.

## Topic Selection

1. Open `https://www.zhihu.com/hot` in the host browser.
2. Read the visible hot-question cards before clicking anything.
3. Load `{baseDir}/data/history.json` and extract the set of already-answered `question_url` values.
4. Determine the active topic filter based on `topic_mode`:

   **`general_hot` (default)**
   - Choose any eligible hot question that supports a substantive text answer.
   - Prefer questions with more visible heat (higher view/answer count displayed on the card) when multiple candidates exist.

   **`custom`**
   - Match questions whose title or summary contains at least one keyword from `custom_topic_keywords`.
   - Keywords use OR logic: a question matches if it contains any one keyword.
   - If the user's request contains negation (e.g., "法律问题但不是法律援助"), extract positive keywords only and note the exclusion as a skip-reason during evaluation.
   - If multiple matches exist, prefer the hotter one.
   - If no match exists on the current visible hot list, stop and report: "No eligible question matched the requested keywords: [keywords]. Try broadening your keywords or switching to general_hot mode."
   - Do not fall back to general_hot silently.

4. Tie-breaking rule (applies to all modes): when two candidates are equally eligible, prefer the one with a higher visible heat indicator (answer count, comment count, or heat score shown on the card). If still tied, prefer the one whose title suggests a more open-ended question that allows varied perspectives.

5. Skip any candidate question that:
   - Falls into a legally risky category (see **Legally Risky Content**)
   - Is primarily a factual lookup with a single correct answer (no room for personal perspective)
   - Is a news headline with no room for insight
   - Has a `question_url` that already exists in `answered` (already handled in a previous run)
   - Choose the next eligible candidate instead.

6. Continue selecting until `draft_count` eligible questions have been found or no more eligible visible hot questions remain. If the visible list is exhausted before reaching `draft_count`, report how many drafts were completed and why the run ended early.

## Evidence Collection

1. Open the selected Zhihu question page.
2. Capture these fields:
   - `question_title`
   - `question_url`
   - `question_excerpt`
   - `selected_reason` (why this question was chosen)
3. Find discussion material in this order:
   - Prefer a visible hot-sorted comment area on the question page.
   - If the question page does not expose a usable comment list, open the current top hot answer and use that answer's hot comments as the fallback discussion source.
4. Collect the hottest `comment_count` usable comments, clamped to the range 3–5. If fewer than 3 usable comments remain after one expand or load-more attempt, continue with however many are available (including 1 or 2).
5. For each comment, collect:
   - `rank`
   - `author_name` (use `"[已删除]"` if the author name is missing or shows a deletion marker)
   - `like_count`
   - `text`
6. Ignore a comment if any of these are true:
   - The comment text is absent or replaced by a deletion notice
   - The comment text is a duplicate of an already-collected comment
   - More than 60% of its characters are emoji or emoticon tokens
   - The comment text is fewer than 15 Chinese characters
   - The comment is in a language other than Chinese (skip entirely)
7. If the available question context or top comments are dominated by politically sensitive, extremist, illegal, or otherwise legally risky content, abandon that question and return to the hot list to choose another eligible question.

## Answer Generation via curl

1. Read `{baseDir}/references/answer-generation.md` to get the system prompt text.
2. Build the user message as a JSON string containing the collected question and comment data (see structure below).
3. Call the API with the following curl command. Replace `<user_message_json>` with the escaped JSON string, and read the API key from the `ZHIHUIAPI_KEY` environment variable:

```bash
curl https://cc.zhihuiapi.top/v1/chat/completions \
  -s \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${ZHIHUIAPI_KEY}" \
  -d '{
    "model": "claude-sonnet-4-6",
    "max_tokens": 2400,
    "response_format": {"type": "json_object"},
    "messages": [
      {
        "role": "system",
        "content": "<contents of {baseDir}/references/answer-generation.md>"
      },
      {
        "role": "user",
        "content": <user_message_json>
      }
    ]
  }'
```

4. The user message JSON object (fill runtime values before sending):

```json
{
  "topic_mode": "general_hot | custom",
  "custom_topic_keywords": ["string"],
  "draft_index": 1,
  "draft_count": 1,
  "question_title": "string",
  "question_excerpt": "string",
  "question_url": "string",
  "selected_reason": "string",
  "writing_style": {
    "mode": "default | user_defined",
    "summary": "string"
  },
  "top_comments": [
    {
      "rank": 1,
      "author_name": "string",
      "like_count": 123,
      "text": "string"
    }
  ],
  "writing_rules": [
    "模仿评论语气和论述节奏，但不要抄袭；连续18个及以上汉字不得与任何评论重合",
    "必须有自己的判断和补充，加入至少1个评论中没有出现的观点或角度",
    "中文自然表达，像真实知乎答主，不要出现元叙述",
    "禁止任何政治相关言论、敏感表达、违法内容或法律风险内容",
    "如果用户提供了写作风格，则优先遵循用户风格；风格冲突时以话题适配为准",
    "如果无法安全表达，返回 {\"status\": \"failed\", \"error\": \"unsafe_content\"} 而非空字符串"
  ]
}
```

5. Parse the curl response: extract `choices[0].message.content` and parse it as JSON.
6. If curl exits with a non-zero code, or the HTTP status is not 200, stop and report: "API call failed — HTTP [status], curl exit [code]. Do not fall back to generating with the current session model."

## Output Validation

Read the expected schema from `{baseDir}/references/answer-schema.json` before validating.

Validate the model output before writing to Zhihu:

- **Reject** if JSON parsing fails.
- **Reject** if the response contains `"status": "failed"` — record `error` field as the failure reason and do not retry.
- **Reject** if `answer_text` is absent or shorter than 200 characters.
- **Reject** if `answer_text` exceeds 800 characters.
- **Reject** if `answer_text` contains any of these meta-wording tokens: `AI`、`人工智能`、`模型`、`生成`、`ChatGPT`、`Claude`、`根据评论`、`根据以上`、`作为助手`、`作为AI`.
- **Reject** if `answer_text` contains political advocacy, political commentary, sensitive expression, illegal instructions, or other legally risky content.
- **Reject** if any 18 or more consecutive Chinese characters in `answer_text` are identical to the same span in any single source comment.
- **Reject** if any full sentence in `answer_text` is a near-verbatim rewrite of a comment sentence (same meaning, minimal word substitution).

On the first rejection (except `status: failed` responses), retry generation once with a strengthened anti-copy instruction appended to `writing_rules`. If the retry still fails validation, stop and report the specific rejection reason. Do not attempt a third generation.

## Draft Save Flow

1. Open the answer editor for the selected question.
2. Write only `answer_text` into the main answer field.
3. Re-check the visible controls before clicking. Use an interactive snapshot to highlight controls if the layout is ambiguous:
   - If there is a single button that combines Save and Publish in a dropdown, click only the dropdown option that says "保存草稿" or equivalent. Do not click the primary button if it defaults to publish.
   - If there are separate Save-Draft and Publish buttons, click only the Save-Draft button.
   - If an auto-save indicator is the only visible signal, do not treat it as a confirmed save; still look for an explicit save-draft action.
   - If the only available action appears to be Publish with no Save-Draft alternative visible, stop and report: "No save-draft control found; draft was not saved."
4. Wait for a visible success signal such as a draft toast, "草稿已保存" status text, or an updated draft count indicator.
5. After receiving the save confirmation, immediately append an entry to `{baseDir}/data/history.json`:
   - `question_url`: the URL of the answered question
   - `question_title`: the title of the answered question
   - `saved_at`: current UTC timestamp in ISO 8601 format
6. If no save confirmation appears within a reasonable wait, stop and report a draft-save failure. Do not assume the draft was saved and do not write to history.
7. If `draft_count` is greater than 1, return to the hot list and repeat the full flow for the next eligible question until the target count is reached or no eligible question remains.

## Failure Handling

- **Stale element refs**: Re-run a browser snapshot and continue with fresh refs. Allow up to 3 re-snapshot attempts per page before giving up and reporting the failure.
- **Ambiguous page layout**: Use interactive snapshots to highlight the intended control before clicking. Never click speculatively.
- **Zhihu blocks session or requests login**: Stop immediately and ask the user to re-open the logged-in Chrome page manually. Do not retry the blocked action.
- **Network timeout on page load**: If a question page fails to load within the configured timeout, skip that question, record the timeout, and try the next candidate.
- **Rate limiting (HTTP 429 or equivalent)**: Stop the run, report how many drafts were completed, and suggest the user wait before retrying.
- **Never perform destructive cleanup**. Leave the page in its current state when the flow stops.

## End-of-Run Report

After completing all drafts (or stopping early), output a brief summary:

```
完成草稿：X / Y
成功：[问题标题列表]
跳过/失败：[问题标题 + 原因]
已跳过（历史重复）：[问题标题列表]
历史记录：已写入 {baseDir}/data/history.json（当前共 N 条）
```

## Manual Validation

Use `{baseDir}/references/manual-test-checklist.md` after changes to the workflow or prompt contract.
