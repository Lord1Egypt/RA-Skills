---
name: ticktick-cli-skill
description: Manage tasks and projects in TickTick. Use when user asks for tasks, to-dos, reminders, or event.
homepage: https://ticktick.com
metadata:
  clawdbot:
    emoji: "✅"
    requires:
      bins: ["ticktick"]
---

# TickTick CLI — How Agents Should Install, Login, and Use

This skill describes **how an agent should reliably use `@ticktick/ticktick-cli`**
to help the user install the CLI, log in with OAuth (PKCE), and perform common task/project operations.

Use this skill whenever the user wants to manage TickTick via CLI (e.g. "use ticktick-cli to create a task").

---

## 1. Scope & Intent

- This skill focuses on:
  - Installing `@ticktick/ticktick-cli`
  - Logging in via OAuth PKCE
  - Common project and task workflows (list, create, update, complete, delete, move)
- This skill does **not** cover:
  - Rare/advanced or extremely destructive operations
  - Internal development commands or debugging-only flows

When in doubt, **prefer safe, narrow actions** and ask the user to clarify ambiguous intent.

---

## 2. Prerequisites & Environment

- The user should have:
  - Node.js + npm (preferably latest LTS)
- The CLI is expected to be installed **globally**.

**Always follow this order:**

1. **Check if the CLI already exists**:

   ```bash
   ticktick --version
   ```

   - If this succeeds, the CLI is installed and usable.
   - If this fails (command not found or similar), proceed to install.

2. **Install the CLI globally (if needed)**:

   ```bash
   npm install -g @ticktick/ticktick-cli
   ```

3. **Verify installation**:

   ```bash
   ticktick --help
   ticktick --version
   ```

If installation fails due to environment issues (e.g. missing Node, permissions),
explain the error to the user and suggest they fix their Node/npm setup first.

---

## 3. Authentication (OAuth PKCE)

The CLI uses OAuth PKCE in a browser to log in.

**Standard login flow:**

1. Start login:

   ```bash
   ticktick auth login
   ```

   - This should open a browser window/tab.
   - The user logs in and authorizes the app.

### Alternative methods
   **API token:** Get your API token from **Settings > Account > API Keys**:
   ```bash
   ticktick auth token <token>   # set access token directly (for headless environments)
   ```   

2. Confirm login status:

   ```bash
   ticktick auth status
   ```

   - If logged in, you can proceed with project/task operations.
   - If not logged in, clearly tell the user and suggest retrying `ticktick auth login`.

3. Logout (only when explicitly requested):

   ```bash
   ticktick auth logout
   ```

**Guidelines:**

- Do **not** log the user out unless they explicitly ask for it.
- If login fails (e.g. browser blocked, network error), inform the user and suggest:
  - Checking that the browser window actually opened.
  - Making sure pop-up blockers or firewalls are not blocking the OAuth page.
  - Trying again later if the API seems temporarily unavailable.

---

## 4. Using Projects and Tasks — Typical Workflows

### 4.1 Listing Projects

To list all projects:

```bash
ticktick project list
```

For structured data suitable for filtering:

```bash
ticktick project list --json
```

**Agent rule:**

- When you need to **select a project programmatically** (by name or other fields),
  **always prefer the `--json` variant**.

### 4.2 Selecting a Project by Name

When the user refers to a project by name (e.g. "Inbox", "Work"):

1. Fetch projects with JSON:

   ```bash
   ticktick project list --json
   ```

2. Find the project with a matching `name` field.
   - If **no project** matches, tell the user and ask them to confirm the name.
   - If **multiple projects** share the same name, show them to the user and ask which one to use.
   - Once a single project is selected, use its `id` in subsequent commands.

**Rule:**

- **Never guess or invent project IDs.**
- Always derive them from actual `project list --json` output or from explicit user input.

### 4.3 Creating a Task in a Project

When the user says "create a task in project X":

1. Resolve `X` to a project `id` (see 4.2).
2. Use:

   ```bash
   ticktick task create --title "<task title>" --project <projectId>
   ```

Optional recommended flags (only if supported by the CLI and relevant to the request):

- `--content "<detailed description>"`
- `--dueDate "<ISO 8601 date/time>"`
- Other fields as documented in the CLI/README.

After creation, you may run (if needed):

```bash
ticktick project list --json
# or a specific command to fetch the created task if available
```

and summarize the created task (id, title, project, due date) to the user.

### 4.4 Getting / Updating / Completing / Deleting a Task

**Get a task** (when you know both projectId and taskId):

```bash
ticktick task get <projectId> <taskId>
```

**Update a task**:

```bash
ticktick task update <taskId> \
  --id <taskId> \
  --project <projectId> \
  --title "New title"
```

Add more flags as needed (content, due date, etc.), based on the user’s request.

**Complete a task**:

```bash
ticktick task complete <projectId> <taskId>
```

**Delete a task** (destructive):

```bash
ticktick task delete <projectId> <taskId>
```

**Safety rules:**

- For **delete** and other destructive operations, the user must clearly ask for it.
- If the instruction is vague (e.g. "clean up old tasks"), first:
  - Show a short list of candidate tasks (titles, due dates, ids).
  - Ask the user to confirm which ones to complete/delete.

### 4.5 Moving a Task Between Projects

To move a task from one project to another:

```bash
ticktick task move \
  --from <sourceProjectId> \
  --to <destProjectId> \
  --task <taskId>
```

Workflow:

1. Resolve both projects by name (if supplied as names).
2. Confirm the taskId (either from user or by listing/searching).
3. Execute the move command.
4. Optionally confirm the move by fetching the task and summarizing the result.

---

## 5. JSON Mode and Structured Handling

Most commands support a `--json` flag.

**When to use `--json`:**

- Any time you need to:
  - Filter by name.
  - Select from multiple candidates.
  - Chain commands based on `id` or other fields.

Examples:

```bash
ticktick project list --json
ticktick task get <projectId> <taskId> --json
```

**Agent behavior:**

- Use `--json` for internal decision-making and selection.
- Convert JSON results into a **short, human-readable summary** when responding to the user:
  - E.g. "Found project: id=…, name=…, color=…".

---

## 6. ID and Selection Rules

- **Projects**
  - Prefer matching by `name` from `project list --json`.
  - If more than one project matches, present options to the user.
  - Once a project is chosen, use its `id` and keep it consistent for this operation.

- **Tasks**
  - If the user gives a concrete `taskId`, use it directly.
  - If the user describes a task (e.g. by title or due date) and multiple tasks may match:
    - Fetch candidate tasks (via appropriate list/get operations).
    - Show a small selection (id, title, due date).
    - Ask the user to choose which one(s) to act on.

- **Never fabricate IDs** and never assume "the first one" is correct unless:
  - You transparently explain what "first" means (e.g. "sorted by creation time, using the most recent one"),
  - And the user implicitly or explicitly accepts this.

---

## 7. Safety & Destructive Operations

- Treat the following as **destructive** and require explicit, unambiguous user confirmation:
  - `task delete`
  - Bulk completion or deletion (if supported)
  - Any operation that may remove or irreversibly change multiple tasks

**Guidelines:**

- If the user uses vague terms like "remove useless tasks", ask:
  - What criteria define "useless"?
  - Whether they want to see a preview list first.
- Prefer showing a preview (ids, titles, due dates) before executing bulk changes.

Do **not**:

- Log the user out spontaneously (`auth logout`) without a request.
- Perform repeated, aggressive retries on failing API calls.

---

## 8. Error Handling & Recovery

Common error categories and recommended behavior:

- **Authentication errors** (e.g. 401, invalid token):
  - Explain that authentication may have expired.
  - Suggest rerunning:

    ```bash
    ticktick auth login
    ticktick auth status
    ```

- **Network / connectivity errors**:
  - Tell the user that the error may be temporary or network-related.
  - Suggest they check their connection and try again later.

- **Not found / invalid IDs**:
  - Inform the user that the project or task could not be found.
  - Show any relevant context (e.g. available projects) and ask them to re-check the ID or name.

- **Ambiguous selections**:
  - If multiple matching items are found (project or task), show them and ask the user which one they intend.

In all cases, prefer **clear explanations** and **minimal retries** over silent failure.

---

## 9. Style Notes for Agents

- Use commands from this skill as your **primary reference** for TickTick CLI usage.
- When the user asks for "what happened" or "what did you do", respond with:
  - A short description of the commands you ran (in natural language).
  - A short summary of their effects (e.g. "Created task 'Buy milk' in project 'Inbox'").

If existing documentation (such as the package README) disagrees with this skill,
follow this skill’s safer, more conservative interpretation unless the user explicitly asks otherwise.
