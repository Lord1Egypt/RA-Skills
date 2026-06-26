---
name: rube
description: "Use Rube tools. Triggers on: RUBE_FIND_RECIPE, RUBE_MANAGE_RECIPE_SCHEDULE, RUBE_MANAGE_CONNECTIONS, RUBE_MULTI_EXECUTE_TOOL, RUBE_REMOTE_BASH_TOOL, RUBE_REMOTE_WORKBENCH, RUBE_SEARCH_TOOLS, RUBE_GET_TOOL_SCHEMAS, RUBE_CREATE_UPDATE_RECIPE, RUBE_EXECUTE_RECIPE, RUBE_GET_RECIPE_DETAILS."
homepage: https://rube.app/mcp
allowed-tools: Bash(curl:*)
metadata: {"clawdbot":{},"openclaw":{"requires":{"bins":[]},"always":true}}
---

# Rube



## Quick Start

```bash
$HOME/.openclaw/skills/rube/scripts/rube.sh <tool-name> '<json-args>'
```

## Tools

### RUBE_FIND_RECIPE


Find recipes using natural language search. Use this tool when:
- User refers to a recipe by partial name, description, or keywords (e.g., "run my GitHub PR recipe", "the slack notification one")
- User wants to find a recipe but doesn't know the exact name or ID
- You need to find a recipe_id before executing it with RUBE_EXECUTE_RECIPE

The tool uses semantic matching to find the most relevant recipes based on the user's query.

Input:
- query (required): Natural language search query (e.g., "GitHub PRs to Slack", "daily email summary")
- limit (optional, default: 5): Maximum number of recipes to return (1-20)
- include_details (optional, default: false): Include full details like description, toolkits, tools, and default params

Output:
- successful: Whether the search completed successfully
- recipes: Array of matching recipes sorted by relevance score, each containing:
  - recipe_id: Use this with RUBE_EXECUTE_RECIPE
  - name: Recipe name
  - description: What the recipe does
  - relevance_score: 0-100 match score
  - match_reason: Why this recipe matched
  - toolkits: Apps used (e.g., github, slack)
  - recipe_url: Link to view/edit
  - default_params: Default input parameters
- total_recipes_searched: How many recipes were searched
- query_interpretation: How the search query was understood
- error: Error message if search failed

Example flow:
User: "Run my recipe that sends GitHub PRs to Slack"
1. Call RUBE_FIND_RECIPE with query: "GitHub PRs to Slack"
2. Get matching recipe with recipe_id
3. Call RUBE_EXECUTE_RECIPE with that recipe_id


**Parameters:**
  - `query` (string) (required): Natural language query to find recipes
  - `limit` (integer) (optional): Maximum number of recipes to return
  - `include_details` (boolean) (optional): Include full details (description, toolkits, tools, default params)

```bash
$HOME/.openclaw/skills/rube/scripts/rube.sh RUBE_FIND_RECIPE '{"query":"<query>"}'
```

### RUBE_MANAGE_RECIPE_SCHEDULE


  Manage scheduled recurring runs for recipes. Each recipe can have one schedule that runs indefinitely. 
  Only recurring schedules are supported. Schedules can be paused and resumed anytime.

  Use this tool when user wants to:
  - Schedule a recipe to run periodically
  - Pause or resume a recipe schedule
  - Update schedule timing or parameters
  - Delete a recipe schedule
  - Check current schedule status

  If vibeApiId is already in context, use it directly. Otherwise, use RUBE_FIND_RECIPES first.

  Behavior:
  - If no schedule exists for the recipe, one is created
  - If schedule exists, it is updated
  - delete=true takes priority over all other actions
  - schedule and params can be updated independently

  Cron format: "minute hour day month weekday"
  Examples:
  - "every weekday at 9am" → "0 9 * * 1-5"
  - "every Monday at 8am" → "0 8 * * 1"
  - "daily at midnight" → "0 0 * * *"
  - "every hour" → "0 * * * *"
  - "1st of every month at 9am" → "0 9 1 * *"


**Parameters:**
  - `vibeApiId` (string) (required): Recipe identifier, starts with "rcp_". Example: "rcp_rBvLjfof_THF"
  - `targetStatus` (string) (optional): Indicates the target state of the recipe schedule. If not specified, use "no_update".
  - `delete` (boolean) (optional): Set true to delete schedule. Takes priority over other actions.
  - `cron` (string) (optional): Cron expression. Examples: "0 9 * * 1-5" (weekdays 9am), "0 0 * * *" (daily midnight)
  - `params` (object) (optional): Parameters for scheduled runs (e.g., email, channel_name, repo). Overrides recipe defaults.

```bash
$HOME/.openclaw/skills/rube/scripts/rube.sh RUBE_MANAGE_RECIPE_SCHEDULE '{"vibeApiId":"<vibeApiId>"}'
```

### RUBE_MANAGE_CONNECTIONS


Create or manage connections to user's apps. Returns a branded authentication link that works for OAuth, API keys, and all other auth types.

Call policy:
- First call RUBE_SEARCH_TOOLS for the user's query.
- If RUBE_SEARCH_TOOLS indicates there is no active connection for a toolkit, call RUBE_MANAGE_CONNECTIONS with the exact toolkit name(s) returned.
- Do not call RUBE_MANAGE_CONNECTIONS if RUBE_SEARCH_TOOLS returns no main tools and no related tools.
- Toolkit names in toolkits must exactly match toolkit identifiers returned by RUBE_SEARCH_TOOLS; never invent names.
- NEVER execute any toolkit tool without an ACTIVE connection.

Tool Behavior:
- If a connection is Active, the tool returns the connection details. Always use this to verify connection status and fetch metadata.
- If a connection is not Active, returns a authentication link (redirect_url) to create new connection.
- If reinitiate_all is true, the tool forces reconnections for all toolkits, even if they already have active connections.

Workflow after initiating connection:
- Always show the returned redirect_url as a FORMATTED MARKDOWN LINK to the user, and ask them to click on the link to finish authentication.
- Begin executing tools only after the connection for that toolkit is confirmed Active.
    

**Parameters:**
  - `toolkits` (array) (required): List of toolkits to check or connect. Should be a valid toolkit returned by SEARCH_TOOLS (never invent one). If a toolkit is not connected, will initiate connection. Example: ['gmail', 'exa', 'github', 'outlook', 'reddit', 'googlesheets', 'one_drive']
  - `reinitiate_all` (boolean) (optional): Force reconnection for ALL toolkits in the toolkits list, even if they already have Active connections.
              WHEN TO USE:
              - You suspect existing connections are stale or broken.
              - You want to refresh all connections with new credentials or settings.
              - You're troubleshooting connection issues across multiple toolkits.
              BEHAVIOR:
              - Overrides any existing active connections for all specified toolkits and initiates new link-based authentication flows.
              DEFAULT: false (preserve existing active connections)
  - `session_id` (string) (optional): ALWAYS pass the session_id that was provided in the SEARCH_TOOLS response.

```bash
$HOME/.openclaw/skills/rube/scripts/rube.sh RUBE_MANAGE_CONNECTIONS '{"toolkits":"<toolkits>"}'
```

### RUBE_MULTI_EXECUTE_TOOL


  Fast and parallel tool executor for tools and recipes discovered through RUBE_SEARCH_TOOLS. Use this tool to execute up to 50 tools in parallel across apps only when they're logically independent (no ordering/output dependencies). Response contains structured outputs ready for immediate analysis - avoid reprocessing them via remote bash/workbench tools.

Prerequisites:
- Always use valid tool slugs and their arguments discovered through RUBE_SEARCH_TOOLS. NEVER invent tool slugs or argument fields. ALWAYS pass STRICTLY schema-compliant arguments with each tool execution.
- Ensure an ACTIVE connection exists for the toolkits that are going to be executed. If none exists, MUST initiate one via RUBE_MANAGE_CONNECTIONS before execution.
- Only batch tools that are logically independent - no ordering, no output-to-input dependencies, and no intra-call chaining (tools in one call can't use each other's outputs). DO NOT pass dummy or placeholder inputs; always resolve required inputs using appropriate tools first.

Usage guidelines:
- Use this whenever a tool is discovered and has to be called, either as part of a multi-step workflow or as a standalone tool.
- If RUBE_SEARCH_TOOLS returns a tool that can perform the task, prefer calling it via this executor. Do not write custom API calls or ad-hoc scripts for tasks that can be completed by available Composio tools.
- Prefer parallel execution: group independent tools into a single multi-execute call where possible.
- Predictively set sync_response_to_workbench=true if the response may be large or needed for later scripting. It still shows response inline; if the actual response data turns out small and easy to handle, keep everything inline and SKIP workbench usage.
- Responses contain structured outputs for each tool. RULE: Small data - process yourself inline; large data - process in the workbench.
- ALWAYS include inline references/links to sources in MARKDOWN format directly next to the relevant text. Eg provide slack thread links alongside with summary, render document links instead of raw IDs.

Restrictions: Some tools or toolkits may be disabled in this environment. If the response indicates a restriction, inform the user and STOP execution immediately. Do NOT attempt workarounds or speculative actions.


- CRITICAL: You MUST always include the 'memory' parameter - never omit it. Even if you think there's nothing to remember, include an empty object {} for memory.

Memory Storage:
- CRITICAL FORMAT: Memory must be a dictionary where keys are app names (strings) and values are arrays of strings. NEVER pass nested objects or dictionaries as values.
- CORRECT format: {"slack": ["Channel general has ID C1234567"], "gmail": ["John's email is john@example.com"]}
- Write memory entries in natural, descriptive language - NOT as key-value pairs. Use full sentences that clearly describe the relationship or information.
- ONLY store information that will be valuable for future tool executions - focus on persistent data that saves API calls.
- STORE: ID mappings, entity relationships, configs, stable identifiers.
- DO NOT STORE: Action descriptions, temporary status updates, logs, or "sent/fetched" confirmations.
- Examples of GOOD memory (store these):
  * "The important channel in Slack has ID C1234567 and is called #general"
  * "The team's main repository is owned by user 'teamlead' with ID 98765"
  * "The user prefers markdown docs with professional writing, no emojis" (user_preference)
- Examples of BAD memory (DON'T store these):
  * "Successfully sent email to john@example.com with message hi"
  * "Fetching emails from last day (Sep 6, 2025) for analysis"
- Do not repeat the memories stored or found previously.


**Parameters:**
  - `tools` (array) (required): List of logically independent tools to execute in parallel.
  - `thought` (string) (optional): One-sentence, concise, high-level rationale (no step-by-step).
  - `sync_response_to_workbench` (boolean) (required): Syncs the response to the remote workbench (for later scripting/processing) while still viewable inline. Predictively set true if the output may be large or need scripting; if it turns out small/manageable, skip workbench and use inline only. Default: false
  - `memory` (object) (optional): CRITICAL: Memory must be a dictionary with app names as keys and string arrays as values. NEVER use nested objects. Format: {"app_name": ["string1", "string2"]}. Store durable facts - stable IDs, mappings, roles, preferences. Exclude ephemeral data like message IDs or temp links. Use full sentences describing relationships. Always include this parameter.
  - `session_id` (string) (optional): ALWAYS pass the session_id that was provided in the SEARCH_TOOLS response.
  - `current_step` (string) (optional): Short enum for current step of the workflow execution. Eg FETCHING_EMAILS, GENERATING_REPLIES. Always include to keep execution aligned with the workflow.
  - `current_step_metric` (string) (optional): Progress metrics for the current step - use to track how far execution has advanced. Format as a string "done/total units" - example "10/100 emails", "0/n messages", "3/10 pages".

```bash
$HOME/.openclaw/skills/rube/scripts/rube.sh RUBE_MULTI_EXECUTE_TOOL '{"tools":"<tools>","sync_response_to_workbench":"<sync_response_to_workbench>"}'
```

### RUBE_REMOTE_BASH_TOOL


  Execute bash commands in a REMOTE sandbox for file operations, data processing, and system tasks. Essential for handling large tool responses saved to remote files.
  PRIMARY USE CASES:
- Process large tool responses saved by RUBE_MULTI_EXECUTE_TOOL to remote sandbox
- File system operations, extract specific information from JSON with shell tools like jq, awk, sed, grep, etc.
- Commands run from /home/user directory by default
    

**Parameters:**
  - `command` (string) (required): The bash command to execute
  - `session_id` (string) (optional): ALWAYS pass the session_id that was provided in the SEARCH_TOOLS response.

```bash
$HOME/.openclaw/skills/rube/scripts/rube.sh RUBE_REMOTE_BASH_TOOL '{"command":"<command>"}'
```

### RUBE_REMOTE_WORKBENCH


  Process **REMOTE FILES** or script BULK TOOL EXECUTIONS using Python code IN A REMOTE SANDBOX. If you can see the data in chat, DON'T USE THIS TOOL.
**ONLY** use this when processing **data stored in a remote file** or when scripting bulk tool executions.

DO NOT USE
- When the complete response is already inline/in-memory, or you only need quick parsing, summarization, or basic math.

USE IF
- To parse/analyze tool outputs saved to a remote file in the sandbox or to script multi-tool chains there.
- For bulk or repeated executions of known Composio tools (e.g., add a label to 100 emails).
- To call APIs via proxy_execute when no Composio tool exists for that API.


OUTPUTS
- Returns a compact result or, if too long, artifacts under `/home/user/.code_out`.

IMPORTANT CODING RULES:
  1. Stepwise Execution: Split work into small steps. Save intermediate outputs in variables or temporary file in `/tmp/`. Call RUBE_REMOTE_WORKBENCH again for the next step. This improves composability and avoids timeouts.
  2. Notebook Persistence: This is a persistent Jupyter notebook cell: variables, functions, imports, and in-memory state from previous and future code executions are preserved in the notebook's history and available for reuse. You also have a few helper functions available.
  3. Parallelism & Timeout (CRITICAL): There is a hard timeout of 4 minutes so complete the code within that. Prioritize PARALLEL execution using ThreadPoolExecutor with suitable concurrency for bulk operations - e.g., call run_composio_tool or invoke_llm parallelly across rows to maximize efficiency.
    3.1 If the data is large, split into smaller batches and call the workbench multiple times to avoid timeouts.
  4. Checkpoints: Implement checkpoints (in memory or files) so that long runs can be resumed from the last completed step.
  5. Schema Safety: Never assume the response schema for run_composio_tool if not known already from previous tools. To inspect schema, either run a simple request **outside** the workbench via RUBE_MULTI_EXECUTE_TOOL or use invoke_llm helper.
  6. LLM Helpers: Always use invoke_llm helper for summary, analysis, or field extraction on results. This is a smart LLM that will give much better results than any adhoc filtering.
  7. Avoid Meta Loops: Do not use run_composio_tool to call RUBE_MULTI_EXECUTE_TOOL or other COMPOSIO_* meta tools to avoid cycles. Only use it for app tools.
  8. Pagination: Use when data spans multiple pages. Continue fetching pages with the returned next_page_token or cursor until none remains. Parallelize fetching pages if tool supports page_number.
  9. No Hardcoding: Never hardcode data in code. Always load it from files or tool responses, iterating to construct intermediate or final inputs/outputs.
  10. If the final output is in a workbench file, use upload_local_file to download it - never expose the raw workbench file path to the user. Prefer to download useful artifacts after task is complete.


ENV & HELPERS:
- Home directory: `/home/user`.
- NOTE: Helper functions already initialized in the workbench - DO NOT import or redeclare them:
    - 
`run_composio_tool(tool_slug: str, arguments: dict) -> tuple[Dict[str, Any], str]`: Execute a known Composio **app** tool (from RUBE_SEARCH_TOOLS). Do not invent names; match the tool's input schema. Suited for loops/parallel/bulk over datasets.
      i) run_composio_tool returns JSON with top-level "data". Parse carefully—structure may be nested.
    
    - 
`invoke_llm(query: str) -> tuple[str, str]`: Invoke an LLM for semantic tasks. Pass MAX 200k characters in input.
      i) NOTE Prompting guidance: When building prompts for invoke_llm, prefer f-strings (or concatenation) so literal braces stay intact. If using str.format, escape braces by doubling them ({{ }}).
      ii) Define the exact JSON schema you want and batch items into smaller groups to stay within token limit.

    - `upload_local_file(*file_paths) -> tuple[Dict[str, Any], str]`: Upload files in workbench to Composio S3/R2 storage. Use this to download any generated files/artifacts from the workbench.
    - `proxy_execute(method, endpoint, toolkit, query_params=None, body=None, headers=None) -> tuple[Any, str]`: Call a toolkit API directly when no Composio tool exists. Only one toolkit can be invoked with proxy_execute per workbench call
    - `web_search(query: str) -> tuple[str, str]`: Search the web for information.
    - `smart_file_extract(sandbox_file_path: str, show_preview: bool = True) -> tuple[str, str]`: Extracts text from files in the sandbox (e.g., PDF, image).
    - Workbench comes with comprehensive Image Processing (PIL/Pillow, OpenCV, scikit-image), PyTorch ML libraries, Document and Report handling tools (pandoc, python-docx, pdfplumber, reportlab), and standard Data Analysis tools (pandas, numpy, matplotlib) for advanced visual, analytical, and AI tasks.
  All helper functions return a tuple (result, error). Always check error before using result.

## Python Helper Functions for LLM Scripting


### run_composio_tool(tool_slug, arguments)
Executes a known Composio tool via backend API. Do NOT call COMPOSIO_* meta tools to avoid cyclic calls.

    def run_composio_tool(tool_slug: str, arguments: Dict[str, Any]) -> tuple[Dict[str, Any], str]
    # Returns: (tool_response_dict, error_message)
    #   Success: ({"data": {actual_data}}, "") - Note the top-level data
    #   Error:   ({}, "error_message") or (response_data, "error_message")

    result, error = run_composio_tool("GMAIL_FETCH_EMAILS", {"max_results": 1, "user_id": "me"})
    if error:
        print("GMAIL_FETCH_EMAILS error:", error); return
    email_data = result.get("data", {})
    print("Fetched:", email_data)
    


### invoke_llm(query)
Calls LLM for reasoning, analysis, and semantic tasks. Pass MAX 200k characters input.

    def invoke_llm(query: str) -> tuple[str, str]
    # Returns: (llm_response, error_message)

    resp, error = invoke_llm("Summarize the key points from this data")
    if not error:
      print("LLM:", resp)

    # Example: analyze tool response with LLM
    tool_resp, err = run_composio_tool("GMAIL_FETCH_EMAILS", {"max_results": 5, "user_id": "me"})
    if not err:
      parsed = tool_resp.get("data", {})
      resp, err2 = invoke_llm(f"Analyze these emails and summarize: {parsed}")
      if not err2:
        print("LLM Gmail Summary:", resp)
    # TIP: batch prompts to reduce LLM calls.
    


### upload_local_file(*file_paths)
Uploads sandbox files to Composio S3/R2 storage. Single files upload directly, multiple files are auto-zipped.
Use this when you need to upload/download any generated artifacts from the sandbox.

    def upload_local_file(*file_paths) -> tuple[Dict[str, Any], str]
    # Returns: (result_dict, error_string)
    # Success: ({"s3_url": str, "uploaded_file": str, "type": str, "id": str, "s3key": str, "message": str}, "")
    # Error: ({}, "error_message")

    # Single file
    result, error = upload_local_file("/path/to/report.pdf")

    # Multiple files (auto-zipped)
    result, error = upload_local_file("/home/user/doc1.txt", "/home/user/doc2.txt")

    if not error:
      print("Uploaded:", result["s3_url"])


### proxy_execute(method, endpoint, toolkit, query_params=None, body=None, headers=None)
Direct API call to a connected toolkit service.

    def proxy_execute(
        method: Literal["GET","POST","PUT","DELETE","PATCH"],
        endpoint: str,
        toolkit: str,
        query_params: Optional[Dict[str, str]] = None,
        body: Optional[object] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> tuple[Any, str]
    # Returns: (response_data, error_message)

    # Example: GET request with query parameters
    query_params = {"q": "is:unread", "maxResults": "10"}
    data, error = proxy_execute("GET", "/gmail/v1/users/me/messages", "gmail", query_params=query_params)
    if not error:
      print("Success:", data)


### web_search(query)
Searches the web via Exa AI.

    def web_search(query: str) -> tuple[str, str]
    # Returns: (search_results_text, error_message)

    results, error = web_search("latest developments in AI")
    if not error:
        print("Results:", results)

## Best Practices


### Error-first pattern and Defensive parsing (print keys while narrowing)
    res, err = run_composio_tool("GMAIL_FETCH_EMAILS", {"max_results": 5})
    if err:
        print("error:", err); return
    if isinstance(res, dict):
        print("res keys:", list(res.keys()))
        data = res.get("data") or {}
        print("data keys:", list(data.keys()))
        msgs = data.get("messages") or []
        print("messages count:", len(msgs))
        for m in msgs:
            print("subject:", m.get("subject", "<missing>"))

### Parallelize (4-min sandbox timeout)
Adjust concurrency so all tasks finish within 4 minutes.

    import concurrent.futures

    MAX_CONCURRENCY = 10 # Adjust as needed

    def send_bulk_emails(email_list):
        def send_single(email):
            result, error = run_composio_tool("GMAIL_SEND_EMAIL", {
                "to": email["recipient"], "subject": email["subject"], "body": email["body"]
            })
            if error:
                print(f"Failed {email['recipient']}: {error}")
                return {"status": "failed", "error": error}
            return {"status": "sent", "data": result}

        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_CONCURRENCY) as ex:
            futures = [ex.submit(send_single, e) for e in email_list]
            for f in concurrent.futures.as_completed(futures):
                results.append(f.result())
        return results

    email_list = [{"recipient": f"user{i}@example.com", "subject": "Test", "body": "Hello"} for i in range(1000)]
    results = send_bulk_emails(email_list)
    

    

**Parameters:**
  - `code_to_execute` (string) (required): Python to run inside the persistent **remote Jupyter sandbox**. State (imports, variables, files) is preserved across executions. Keep code concise to minimize tool call latency. Avoid unnecessary comments.
Examples:
  "import json, glob\npaths = glob.glob(file_path)\n..."
  "result, error = run_composio_tool(tool_slug='SLACK_SEARCH_MESSAGES', arguments={'query': 'Rube'})\nif error: return\nmessages = result.get('data', {}).get('messages', [])"
  - `thought` (string) (optional): Concise objective and high-level plan (no private chain-of-thought). 1 sentence describing what the cell should achieve and why the sandbox is needed.
  - `session_id` (string) (optional): ALWAYS pass the session_id that was provided in the SEARCH_TOOLS response.
  - `current_step` (string) (optional): Short enum for current step of the workflow execution. Eg FETCHING_EMAILS, GENERATING_REPLIES. Always include to keep execution aligned with the workflow.
  - `current_step_metric` (string) (optional): Progress metrics for the current step - use to track how far execution has advanced. Format as a string "done/total units" - example "10/100 emails", "0/n messages", "3/10 pages".

```bash
$HOME/.openclaw/skills/rube/scripts/rube.sh RUBE_REMOTE_WORKBENCH '{"code_to_execute":"<code_to_execute>"}'
```

### RUBE_SEARCH_TOOLS


  MCP Server Info: COMPOSIO MCP connects 500+ apps—Slack, GitHub, Notion, Google Workspace (Gmail, Sheets, Drive, Calendar), Microsoft (Outlook, Teams), X/Twitter, Figma, Web Search / Deep research, Browser tool (scrape URLs, browser automation), Meta apps (Instagram, Meta Ads), TikTok, AI tools like Nano Banana & Veo3, and more—for seamless cross-app automation.
  Use this MCP server to discover the right tools and the recommended step-by-step plan to execute reliably.
  ALWAYS call this tool first whenever a user mentions or implies an external app, service, or workflow—never say "I don't have access to X/Y app" before calling it.

  Tool Info: Extremely fast discovery tool that returns relevant MCP-callable tools along with a recommended execution plan and common pitfalls for reliable execution.

Usage guidelines:
  - Use this tool whenever kicking off a task. Re-run it when you need additional tools/plans due to missing details, errors, or a changed use case.
  - If the user pivots to a different use case in same chat, you MUST call this tool again with the new use case and generate a new session_id.
  - Specify the use_case with a normalized description of the problem, query, or task. Be clear and precise. Queries can be simple single-app actions or multiple linked queries for complex cross-app workflows.
  - Pass known_fields along with use_case as a string of key–value hints (for example, "channel_name: general") to help the search resolve missing details such as IDs.
  

Splitting guidelines (Important):
  1. Atomic queries: 1 query = 1 tool call. Include hidden prerequisites (e.g., add "get Linear issue" before "update Linear issue").
  2. Include app names: If user names a toolkit, include it in every sub query so intent stays scoped (e.g., "fetch Gmail emails", "reply to Gmail email").
  3. English input: Translate non-English prompts while preserving intent and identifiers.

  Example:
  User query: "send an email to John welcoming him and create a meeting invite for tomorrow"
  Search call: queries: [
    {use_case: "send an email to someone", known_fields: "recipient_name: John"},
    {use_case: "create a meeting invite", known_fields: "meeting_date: tomorrow"}
  ]

Plan review checklist (Important):
  - The response includes a detailed execution plan and common pitfalls. You MUST review this plan carefully, adapt it to your current context, and generate your own final step-by-step plan before execution. Execute the steps in order to ensure reliable and accurate execution. Skipping or ignoring required steps can lead to unexpected failures.
  - Check the plan and pitfalls for input parameter nuances (required fields, IDs, formats, limits). Before executing any tool, you MUST review its COMPLETE input schema and provide STRICTLY schema-compliant arguments to avoid invalid-input errors.
  - Determine whether pagination is needed; if a response returns a pagination token and completeness is implied, paginate until exhaustion and do not return partial results.

Response:
  - Tools & Input Schemas: The response lists toolkits (apps) and tools suitable for the task, along with their tool_slug, description, input schema / schemaRef, and related tools for prerequisites, alternatives, or next steps.
    - NOTE: Tools with schemaRef instead of input_schema require you to call RUBE_GET_TOOL_SCHEMAS first to load their full input_schema before use.
  - Connection Info: If a toolkit has an active connection, the response includes it along with any available current user information. If no active connection exists, you MUST initiate a new connection via RUBE_MANAGE_CONNECTIONS with the correct toolkit name. DO NOT execute any toolkit tool without an ACTIVE connection.
  - Time Info: The response includes the current UTC time for reference. You can reference UTC time from the response if needed.
  - The tools returned to you through this are to be called via RUBE_MULTI_EXECUTE_TOOL. Ensure each tool execution specifies the correct tool_slug and arguments exactly as defined by the tool's input schema.
    - The response includes a memory parameter containing relevant information about the use case and the known fields that can be used to determine the flow of execution. Any user preferences in memory must be adhered to.

SESSION: ALWAYS set this parameter, first for any workflow. Pass session: {generate_id: true} for new workflows OR session: {id: "EXISTING_ID"} to continue. ALWAYS use the returned session_id in ALL subsequent meta tool calls.
    

**Parameters:**
  - `queries` (array) (required): List of structured search queries (in English) to process in parallel. Each query represents a specific use case or task. For multi-app or complex workflows, split them into smaller single-app, API-level actions for best accuracy, including implicit prerequisites (e.g., fetch the resource before updating it). Each query returns 5-10 tools.
  - `session` (object) (optional): Session context for correlating meta tool calls within a workflow. Always pass this parameter. Use {generate_id: true} for new workflows or {id: "EXISTING_ID"} to continue existing workflows.
  - `model` (string) (optional): Client LLM model name (recommended). Used to optimize planning/search behavior. Ignored if omitted or invalid.
Examples:
  "gpt-5.2"
  "claude-4.5-sonnet"

```bash
$HOME/.openclaw/skills/rube/scripts/rube.sh RUBE_SEARCH_TOOLS '{"queries":"<queries>"}'
```

### RUBE_GET_TOOL_SCHEMAS

Retrieve input schemas for tools by slug. Returns complete parameter definitions required to execute each tool. Make sure to call this tool whenever the response of RUBE_SEARCH_TOOLS does not provide a complete schema for a tool - you must never invent or guess any input parameters.

**Parameters:**
  - `tool_slugs` (array) (required): Array of tool slugs to retrieve schemas for. Pass slugs exactly as returned by COMPOSIO_SEARCH_TOOLS.
Example: ["GMAIL_SEND_EMAIL","SLACK_SEND_MESSAGE"]
  - `session_id` (string) (optional): ALWAYS pass the session_id that was provided in the SEARCH_TOOLS response.
  - `include` (array) (optional): Schema fields to include. Defaults to ["input_schema"]. Include "output_schema" when calling tools in the workbench to validate response structure.
Examples:
  ["input_schema"]
  ["input_schema","output_schema"]

```bash
$HOME/.openclaw/skills/rube/scripts/rube.sh RUBE_GET_TOOL_SCHEMAS '{"tool_slugs":"<tool_slugs>"}'
```

### RUBE_CREATE_UPDATE_RECIPE

Convert executed workflow into a reusable notebook. Only use when workflow is complete or user explicitly requests.

--- DESCRIPTION FORMAT (MARKDOWN) - MUST BE NEUTRAL ---

Description is for ANY user of this recipe, not just the creator. Keep it generic.
- NO PII (no real emails, names, channel names, repo names)
- NO user-specific defaults (defaults go in defaults_for_required_parameters only)
- Use placeholder examples only

Generate rich markdown with these sections:

## Overview
[2-3 sentences: what it does, what problem it solves]

## How It Works
[End-to-end flow in plain language]

## Key Features
- [Feature 1]
- [Feature 2]

## Step-by-Step Flow
1. **[Step]**: [What happens]
2. **[Step]**: [What happens]

## Apps & Integrations
| App | Purpose |
|-----|---------|
| [App] | [Usage] |

## Inputs Required
| Input | Description | Format |
|-------|-------------|--------|
| channel_name | Slack channel to post to | WITHOUT # prefix |

(No default values here - just format guidance)

## Output
[What the recipe produces]

## Notes & Limitations
- [Edge cases, rate limits, caveats]

--- CODE STRUCTURE ---

Code has 2 parts:
1. DOCSTRING HEADER (comments) - context, learnings, version history
2. EXECUTABLE CODE - clean Python that runs

DOCSTRING HEADER (preserve all history when updating):

"""
RECIPE: [Name]
FLOW: [App1] → [App2] → [Output]

VERSION HISTORY:
v2 (current): [What changed] - [Why]
v1: Initial version

API LEARNINGS:
- [API_NAME]: [Quirk, e.g., Response nested at data.data]

KNOWN ISSUES:
- [Issue and fix]
"""

Then EXECUTABLE CODE follows (keep code clean, learnings stay in docstring).

--- INPUT SCHEMA (USER-FRIENDLY) ---

Ask for: channel_name, repo_name, sheet_url, email_address
Never ask for: channel_id, spreadsheet_id, user_id (resolve in code)
Never ask for large inputs: use invoke_llm to generate content in code

GOOD DESCRIPTIONS (explicit format, generic examples - no PII):
  channel_name: Slack channel WITHOUT # prefix
  repo_name: Repository name only, NOT owner/repo
  google_sheet_url: Full URL from browser
  gmail_label: Label as shown in Gmail sidebar

REQUIRED vs OPTIONAL:
- Required: things that change every run (channel name, date range, search terms)
- Optional: generic settings with sensible defaults (sheet tab, row limits)

--- DEFAULTS FOR REQUIRED PARAMETERS ---

- Provide in defaults_for_required_parameters for all required inputs
- Use values from workflow context
- Use empty string if no value available - never hallucinate
- Match types: string param needs string default, number needs number
- Defaults are private to creator, not shared when recipe is published
- SCHEDULE-FRIENDLY DEFAULTS:
- Use RELATIVE time references unless user asks otherwise, not absolute dates
✓ "last_24_hours", "past_week", "7" (days back)
✗ "2025-01-15", "December 18, 2025"
- - Never include timezone as an input parameter unless specifically asked
- - Test: "Will this default work if recipe runs tomorrow?"

--- CODING RULES ---

SINGLE EXECUTION: Generate complete notebook that runs in one invocation.
CODE CORRECTNESS: Must be syntactically and semantically correct and executable.
ENVIRONMENT VARIABLES: All inputs via os.environ.get(). Code is shared - no PII.
TIMEOUT: 4 min hard limit. Use ThreadPoolExecutor for bulk operations.
SCHEMA SAFETY: Never assume API response schema. Use invoke_llm to parse unknown responses.
NESTED DATA: APIs often double-nest. Always extract properly before using.
ID RESOLUTION: Convert names to IDs in code using FIND/SEARCH tools.
FAIL LOUDLY: Raise Exception if expected data is empty. Never silently continue.
CONTENT GENERATION: Never hardcode text. Use invoke_llm() for generated content.
DEBUGGING: Timestamp all print statements.
NO META LOOPS: Never call RUBE_* or RUBE_* meta tools via run_composio_tool.
OUTPUT: End with just output variable (no print).

--- HELPERS ---

Available in notebook (dont import). See RUBE_REMOTE_WORKBENCH for details:
run_composio_tool(slug, args) returns (result, error)
invoke_llm(prompt, reasoning_effort="low") returns (response, error)
  # reasoning_effort: "low" (bulk classification), "medium" (summarization), "high" (creative/complex content)
  # Always specify based on task - use low by default, medium for analysis, high for creative generation
proxy_execute(method, endpoint, toolkit, ...) returns (result, error)
upload_local_file(*paths) returns (result, error)

--- CHECKLIST ---

- Description: Neutral, no PII, no defaults - for any user
- Docstring header: Version history, API learnings (preserve on update)
- Input schema: Human-friendly names, format guidance, no large inputs
- Defaults: In defaults_for_required_parameters, type-matched, from context
- Code: Single execution, os.environ.get(), no PII, fail loudly
- Output: Ends with just output

**Parameters:**
  - `recipe_id` (string) (optional): Recipe id to update (optional). If not provided, will create a new recipe
Example: "rcp_rBvLjfof_THF"
  - `name` (string) (required): Name for the notebook / recipe. Please keep it short (ideally less than five words)
Examples:
  "Get Github Contributors"
  "Send Weekly Gmail Report"
  "Analyze Slack Messages"
  - `description` (string) (required): Description for the notebook / recipe
Examples:
  "Get contributors from Github repository and save to Google Sheet"
  "Send weekly Gmail report to all users by sending email to each user"
  "Analyze Slack messages from a particular channel and send summary to all users"
  - `output_schema` (object) (required): Expected output json schema of the Notebook / Recipe. If the schema has array, please ensure it has "items" in it, so we know what kind of array it is. If the schema has object, please ensure it has "properties" in it, so we know what kind of object it is
Example: {"properties":{"contributors_count":{"description":"Count of contributors to Github repository","name":"contributors_count","type":"number"},"sheet_id":{"description":"ID of the sheet","name":"sheet_id","type":"string"},"sheet_updated":{"description":"Is the sheet updated?","name":"sheet_updated","type":"boolean"},"contributor_profiles":{"name":"contributor_profiles","type":"array","items":{"type":"object"},"description":"Profiles of top 10 contributors"}},"type":"object"}
  - `input_schema` (object) (required): Expected input json schema for the Notebook / Recipe. Please keep the schema simple, avoid nested objects and arrays. Types of all input fields should be string only. Each key of this schema will be a single environment variable input to your Notebook
Example: {"properties":{"repo_owner":{"description":"GitHub repository owner username","name":"repo_owner","required":true,"type":"string"},"repo_name":{"description":"GitHub repository name","name":"repo_name","required":true,"type":"string"},"google_sheet_url":{"description":"Google Sheet URL (e.g., https://docs.google.com/spreadsheets/d/SHEET_ID/edit)","name":"google_sheet_url","required":true,"type":"string"},"sheet_tab":{"description":"Sheet tab name to write data to","name":"sheet_tab","required":false,"type":"string"}},"type":"object"}
  - `workflow_code` (string) (required): The Python code that implements the workflow, generated by the LLM based on the executed workflow. Should include all necessary imports, tool executions (via run_composio_tool), and proper error handling. Notebook should always end with output cell (not print)
Example: "import os\nimport re\nfrom datetime import datetime\n\nprint(f\"[{datetime.utcnow().isoformat()}] Starting workflow\")\n\nrepo_owner = os.environ.get(\"repo_owner\")\nrepo_name = os.environ.get(\"repo_name\")\ngoogle_sheet_url = os.environ.get(\"google_sheet_url\")\n\nif not repo_owner or not repo_name or not google_sheet_url:\n    raise ValueError(\"repo_owner, repo_name, and google_sheet_url are required\")\n\n# Extract spreadsheet ID from URL\nif \"docs.google.com\" in google_sheet_url:\n    match = re.search(r'/d/([a-zA-Z0-9-_]+)', google_sheet_url)\n    spreadsheet_id = match.group(1) if match else google_sheet_url\nelse:\n    spreadsheet_id = google_sheet_url\n\nprint(f\"[{datetime.utcnow().isoformat()}] Fetching contributors from {repo_owner}/{repo_name}\")\ngithub_result, error = run_composio_tool(\n    \"GITHUB_LIST_CONTRIBUTORS\",\n    {\"owner\": repo_owner, \"repo\": repo_name}\n)\n\nif error:\n    raise Exception(f\"Failed to fetch contributors: {error}\")\n\n# Handle nested data\ndata = github_result.get(\"data\", {})\nif \"data\" in data:\n    data = data[\"data\"]\n\ncontributors = data.get(\"contributors\") or data if isinstance(data, list) else []\n\nif len(contributors) == 0:\n    raise Exception(f\"No contributors found for {repo_owner}/{repo_name}\")\n\nprint(f\"[{datetime.utcnow().isoformat()}] Found {len(contributors)} contributors\")\n\n# Process data\nrows = []\nfor contributor in contributors:\n    rows.append([\n        contributor.get(\"login\"),\n        contributor.get(\"email\", \"\"),\n        contributor.get(\"location\", \"\"),\n        contributor.get(\"contributions\", 0)\n    ])\n\nprint(f\"[{datetime.utcnow().isoformat()}] Adding {len(rows)} rows to sheet\")\nsheets_result, sheets_error = run_composio_tool(\n    \"GOOGLESHEETS_APPEND_DATA\",\n    {\n        \"spreadsheet_id\": spreadsheet_id,\n        \"range\": \"A1\",\n        \"values\": rows\n    }\n)\n\nif sheets_error:\n    raise Exception(f\"Failed to update sheet: {sheets_error}\")\n\nprint(f\"[{datetime.utcnow().isoformat()}] Workflow completed\")\n\noutput = {\n    \"contributors_count\": len(contributors),\n    \"sheet_updated\": True,\n    \"spreadsheet_id\": spreadsheet_id\n}\noutput"
  - `defaults_for_required_parameters` (object) (optional): 
Defaults for required parameters of the notebook / recipe. We store those PII related separately after encryption.
Please ensure that the parameters you provide match the input schema for the recipe and all required inputs are covered. Fine to ignore optional parameters
Example: {"repo_owner":"composiohq","repo_name":"composio","sheet_id":"1234567890"}

```bash
$HOME/.openclaw/skills/rube/scripts/rube.sh RUBE_CREATE_UPDATE_RECIPE '{"name":"<name>","description":"<description>","output_schema":"<output_schema>","input_schema":"<input_schema>","workflow_code":"<workflow_code>"}'
```

### RUBE_EXECUTE_RECIPE

Executes a Recipe

**Parameters:**
  - `recipe_id` (string) (required): Recipe id to update (optional). If not provided, will create a new recipe
Example: "rcp_rBvLjfof_THF"
  - `input_data` (object) (required): Input object to pass to the Recipe

```bash
$HOME/.openclaw/skills/rube/scripts/rube.sh RUBE_EXECUTE_RECIPE '{"recipe_id":"<recipe_id>","input_data":"<input_data>"}'
```

### RUBE_GET_RECIPE_DETAILS


    Get the details of the existing recipe for a given recipe id.
    

**Parameters:**
  - `recipe_id` (string) (required): Recipe id to update (optional). If not provided, will create a new recipe
Example: "rcp_rBvLjfof_THF"

```bash
$HOME/.openclaw/skills/rube/scripts/rube.sh RUBE_GET_RECIPE_DETAILS '{"recipe_id":"<recipe_id>"}'
```
