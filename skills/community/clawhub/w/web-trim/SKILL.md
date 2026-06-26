# Skill: Web-Trim-Summarize
**Goal**: Fetch a URL, clean the data in a sub-session, and return only the essence.

**Protocol**:
1. When asked to "Research" or "Summarize" a site:
2. Use `sessions_spawn` to create a worker.
3. Pass the following instructions to the worker:
   - Use `web_fetch` on [URL] with `extractMode: "markdown"`.
   - Strip all headers, footers, and cookie notices.
   - If the content is > 10,000 chars, truncate to the most relevant sections.
   - Produce a concise summary (max 500 words).
4. Retrieve the summary via `sessions_yield`.
5. Paste the final summary into the main chat.
