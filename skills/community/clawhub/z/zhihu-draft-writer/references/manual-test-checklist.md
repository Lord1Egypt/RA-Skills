# Manual Test Checklist

Run these checks after changing the workflow, prompt, or Zhihu element strategy.

---

## 1. Core Path (General Hot)

1. Zhihu is already logged in through the host Chrome session.
2. Run the skill with no parameters (default: `general_hot`, `draft_count=1`).
3. Confirm the skill opens the hot page and selects a question without prompting the user for any input.
4. Confirm the skill reads 3–5 hot comments and extracts `rank`, `author_name`, `like_count`, `text`.
5. Confirm the skill generates a non-empty answer (180–700 characters) and saves it as a draft.
6. Confirm the skill does not click any publish control.
7. Confirm the end-of-run report shows "完成草稿：1 / 1".

---

## 2. Custom Topic Path

1. Request a custom topic such as `职场` or `健身`.
2. Confirm the skill selects a question matching at least one keyword, not just the hottest general question.
3. Request a topic where no hot question matches (e.g., an obscure niche keyword).
4. Confirm the skill stops and reports the "no eligible question" message with the requested keywords listed.
5. Confirm the skill does **not** silently fall back to general_hot.

---

## 3. Custom Topic with Multiple Matches

1. Set `custom_topic_keywords = ["职场"]` where multiple hot questions match.
2. Confirm the skill selects the hotter one (higher visible heat indicator), not just the first in DOM order.
3. Set `custom_topic_keywords = ["职场", "亲子"]` (OR logic).
4. Confirm the skill accepts questions matching either keyword.

---

## 4. Batch Draft Path

1. Request `draft_count = 3`.
2. Confirm the skill creates one draft per eligible question, up to 3.
3. Confirm the skill stops at 3 or earlier if no more eligible questions remain, and reports remaining count.
4. Request `draft_count = 7`. Confirm the skill caps at 5 and notes the cap in the result.
5. Confirm the end-of-run report lists all successes and any skipped/failed questions with reasons.

---

## 5. Batch Partial Failure Path

1. Set `draft_count = 3`. Arrange so the second candidate question triggers a safety skip.
2. Confirm the skill skips the second question, records the skip reason, and continues to the third.
3. Confirm the end-of-run report accurately reflects 2 successes and 1 skip.
4. Set `draft_count = 3`. Force the model to return a validation failure on the second draft (e.g., temporarily corrupt the API key for one call).
5. Confirm the skill reports the failure for draft #2 and still saves drafts #1 and #3.

---

## 6. Writing Style Path

1. Request a custom style such as `更口语化` or `像过来人分享经验，不要鸡汤`.
2. Confirm the generated answer tone reflects the custom style.
3. Run again without a custom style and confirm the default rational Zhihu style is used.
4. Request a style that conflicts with the topic (e.g., `激进风格` on a medical question).
5. Confirm the skill produces a safe, topic-appropriate answer rather than an aggressive one, without failing.

---

## 7. Thin Comment Path

1. Choose a question page that exposes only 1–2 usable comments after one expand attempt.
2. Confirm the skill continues with the reduced comment set instead of failing.
3. Confirm the generated answer does not fabricate facts that weren't in the available comments.

---

## 8. Model Failure Path

1. Force an invalid provider API key.
2. Confirm the skill stops before writing any text into the Zhihu editor.
3. Confirm the error message points to model generation failure, not a browser or page error.
4. Simulate a model timeout (set `timeoutMs` to a very low value, e.g., 100).
5. Confirm the skill stops cleanly, reports a timeout error, and does not leave partial text in the editor.
6. Force the model to return malformed JSON (non-JSON string).
7. Confirm the skill treats this as a validation failure and either retries or stops with a clear error.

---

## 9. Save Button Ambiguity Path

1. Verify on a real Zhihu answer editor that the skill correctly identifies the save-draft action.
2. If the editor shows a combined button with a dropdown (Save + Publish options), confirm the skill opens the dropdown and selects only "保存草稿".
3. Confirm the skill does not click the primary button if it defaults to "发布".
4. If an auto-save indicator is the only visible signal, confirm the skill still looks for an explicit save-draft action and does not treat auto-save as a confirmed save.
5. Confirm the skill waits for a visible toast or status indicator before proceeding to the next draft.

---

## 10. Page Drift Path

1. Make the expected draft-save control unavailable (e.g., hide it via DevTools).
2. Confirm the skill reports "No save-draft control found" and does not click any other button.
3. Simulate a stale element reference by navigating away mid-flow.
4. Confirm the skill re-snapshots (up to 3 attempts) and recovers, or stops after 3 failed attempts.

---

## 11. Anti-Copy Path

1. Use comments that contain distinctive long phrases (20+ characters).
2. Confirm the generated answer does not contain any 18+ consecutive character overlap with any source comment.
3. Force a scenario where the first generation contains an overlap (mock or prompt-inject).
4. Confirm the skill retries once with a stronger anti-copy instruction.
5. If the retry also fails, confirm the skill stops and does not write the answer into Zhihu.

---

## 12. Safety Filter Path

1. Select a hot question whose title or comments lean toward politically sensitive content.
2. Confirm the skill skips that candidate question during topic selection.
3. If the skill somehow generates text that contains politically sensitive language, confirm the output validation rejects it.
4. Confirm no draft is saved when the model returns `{"status": "failed", "error": "unsafe_content"}`.
5. Confirm the skill does **not** retry on a `status: failed` response.

---

## 13. Login Wall Path

1. Log out of Zhihu in the browser while the skill is running (or start with a logged-out session).
2. Confirm the skill detects the login wall immediately and stops with a message asking the user to log in manually.
3. Confirm the skill does not attempt to automate the login process.

---

## 15. History Deduplication Path

1. Run the skill once and confirm a draft is saved successfully.
2. Confirm `data/history.json` now contains exactly one entry with the correct `question_url`, `question_title`, and a valid `saved_at` timestamp.
3. Run the skill again without clearing the history. Confirm the previously answered question is skipped during topic selection and does not appear as a new draft.
4. Confirm the end-of-run report lists the skipped question under "已跳过（历史重复）".
5. Manually add a fake entry to `history.json` with a `question_url` that matches a current hot question. Run the skill and confirm that question is skipped.
6. Delete `data/history.json` entirely. Run the skill and confirm it starts fresh with an empty history (no error, no crash).
7. Simulate a file-write failure when appending to `history.json` (e.g., make the file read-only). Confirm the skill logs a warning in the report but still completes the draft save successfully.
8. Run the skill with `draft_count = 3` where 2 of the visible hot questions are already in history. Confirm the skill finds 3 new eligible questions (scrolling or using remaining hot list) rather than counting the skipped ones toward the target.

1. Simulate an HTTP 429 response from Zhihu (via network proxy or mock).
2. Confirm the skill stops the run, reports how many drafts were completed before the rate limit, and suggests waiting before retrying.
3. Confirm the skill does not loop-retry the blocked request.
