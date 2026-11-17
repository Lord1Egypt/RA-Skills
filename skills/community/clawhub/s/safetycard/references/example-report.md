# Worked example (format reference only)

> Read this after you have scored, to check format and evidence density. Do not borrow its levels: they describe smolagents at commit `c30b115` (2026-10-03). Rendered by `score.py --report` from `example-scorecard.json`.


**Repo:** https://github.com/huggingface/smolagents · **Commit:** `c30b115286e000e98711fae5e85993547b73d826` · **Reviewed:** 2026-10-03
**What it is:** Python agent framework whose CodeAgent writes its actions as Python code; ships a CLI and optional remote sandboxes.
**Category:** Agent Frameworks
**Scored configuration:** CodeAgent with default constructor arguments (executor_type='local', add_base_tools=False), as in the README quickstart.
**Agent surface (default):** code execution yes · filesystem write no · network egress yes · external credentials yes · persistent memory no · untrusted input yes · third party extensions opt-in · sub agents yes · external communication yes

## Score: 2.2 / 10.0 (Minimal)

| # | Criterion | S | C | D | B | Raw | Cap | Score | Confidence |
|---|---|---|---|---|---|---|---|---|---|
| C1 | Identity & least privilege | L0 | L0 | L0 | L1 | 0.05 | none | **0.05** | Medium |
| C2 | Approval gates | L0 | L0 | L0 | L0 | 0.00 | none | **0.00** | High |
| C3 | Tool & action scoping | L1 | L1 | L2 | L1 | 0.30 | none | **0.30** | High |
| C4 | Code-execution isolation | L4 | L3 | L0 | L2 | 0.62 | G1 | **0.50** (alt) | Medium |
| C5 | Untrusted input blast radius | L0 | L0 | L0 | L0 | 0.00 | C5-WORSTCASE | **0.00** | High |
| C6 | Memory, context & configuration integrity | L1 | L1 | L2 | L2 | 0.35 | C6-REPOCONFIG | **0.25** | Medium |
| C7 | Third-party extensions | L1 | L0 | L1 | L0 | 0.12 | none | **0.12** | High |
| C8 | Secrets & sensitive-data protection | L1 | L0 | L2 | L1 | 0.23 | none | **0.23** | Medium |
| C9 | Audit & traceability | L1 | L2 | L1 | L0 | 0.28 | none | **0.28** | High |
| C10 | Limits & kill switch | L2 | L2 | L2 | L1 | 0.45 | none | **0.45** | High |


As shipped, model-written code runs inside the developer's own Python process behind a filter its maintainers say is not a security boundary, with no approval gate and no separation between web content and instructions. The dominant risk is goal hijack: a web page read during a run can steer code that executes with the host's authority. Strong isolation exists but is opt-in, and the framework gives developers no oversight primitive for the tools they register.

## Safest setup

smolagents keeps its own footprint small: agents get only the tools you list, Hub code needs an explicit trust flag, and every run stops after 20 steps. Model-written code runs in your own Python process by default and there is no approval step, so the safest setup moves that code into a sandbox and puts the boundaries around the process yourself.

| Setup | How | What it gives you |
|---|---|---|
| A dedicated, low-limit key | Run the agent in an environment that holds only the model key and tool credentials this agent needs, with a spending limit set at the provider | Whatever the agent does, it can only reach the systems and spend you gave it, not everything your shell can (C1) |
| A remote sandbox | `executor_type="e2b"` on `CodeAgent` ([src/smolagents/agents.py:1535](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/agents.py#L1535)) | Model-written code and your registered tools run in a remote sandbox that never sees your host environment (C4) |
| A short import list | List only the modules the task needs in `additional_authorized_imports` ([src/smolagents/agents.py:1532](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/agents.py#L1532)) | The local interpreter keeps blocking `os`, `subprocess` and other modules the task has no use for (C4) |
| Reviewed, pinned Hub code | Keep the default `trust_remote_code=False`; when you load a tool you have read, set it to `True` and pin the commit with `revision` ([src/smolagents/tools.py:521](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/tools.py#L521); [src/smolagents/tools.py:563](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/tools.py#L563)) | Only code you have read runs inside your agent, and it can't change after you read it (C7) |
| A step budget | Keep the default `max_steps=20`, or lower it for short tasks ([src/smolagents/agents.py:300](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/agents.py#L300)) | Every run ends after a fixed number of steps (C10) |
| A clean working directory | Start agents from a directory that holds no `.env` file you didn't write ([src/smolagents/remote_executors.py:48](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/remote_executors.py#L48)) | Settings such as the model endpoint come only from you, not from a repository you happen to run in (C6) |
| Its own container or VM | Run the agent process in a container or VM with network access limited to the hosts the task needs | An outer boundary around the local executor and your registered tools, and a narrower path for data to leave (C5) |
| A run record on disk | Register a callback in `step_callbacks` that writes each step to storage the agent can't modify ([src/smolagents/agents.py:304](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/agents.py#L304)) | A record of every tool call and observation that outlives the process (C9) |

### Handling data

- Tool observations print to the console unredacted at the default `verbosity_level`; treat console output and anything a step callback stores like the data the agent read.

## Critical gaps
- Model-generated code executes in-process by default; the maintainers state the local executor is not a security boundary. (ASI05; C4). Evidence: [src/smolagents/agents.py:1535](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/agents.py#L1535); [SECURITY.md:80](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/SECURITY.md#L80)
- If a web page the agent reads hijacks it, it can leak data through arbitrary URL fetches and run any registered tool, with no human involved. (ASI01; C5). Evidence: [README.md:61-64](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/README.md#L61-L64); [src/smolagents/default_tools.py:528](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/default_tools.py#L528)
- .env in the working directory is loaded at import time, letting a cloned repo set endpoints or sandbox credentials (impact inferred). (ASI06; C6). Evidence: [src/smolagents/remote_executors.py:46-48](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/remote_executors.py#L46-L48); [src/smolagents/cli.py:230](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/cli.py#L230)
- Hub, Space, and MCP tools run in-process with full authority once trust_remote_code=True, which official examples routinely set. (ASI04; C7). Evidence: [src/smolagents/tools.py:1052-1055](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/tools.py#L1052-L1055); [src/smolagents/tools.py:1005](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/tools.py#L1005)

## Criterion details

### C1 Identity & least privilege: 0.05 (medium confidence)

smolagents has no notion of an agent identity or per-request authorization: every tool runs in the host process with whatever credentials the developer's environment holds, and importing the remote-executor module silently loads a .env file from the working directory into that environment. The default local executor blocks model code from importing os, which narrows access a little, but its maintainers state it is not a security boundary.

- **S L0:** No authorization or scoping primitive; tools run with the host process's full authority. Evidence: searched `rg -n -S 'authoriz|permission|scope'` in `src/smolagents/agents.py src/smolagents/tools.py` → 27 hits (hits are import-allowlist names, tool type checks, HTTP-bearer docstrings, license text, and the word 'scope'; none authorizes actions); [src/smolagents/agents.py:987](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/agents.py#L987) (verified)
  - *To reach the next level:* No scoping primitive at all; L1 needs at least a dedicated identity for agent tools.
- **C L0:** The tool path only type-checks arguments; no authorization layer exists to cover anything. Evidence: [src/smolagents/agents.py:1476](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/agents.py#L1476) (verified)
  - *To reach the next level:* No authorization layer; L1 needs the main tool path checked in code.
- **D L0:** No narrower default identity; import-time load_dotenv() widens the environment from the working directory. Evidence: [src/smolagents/remote_executors.py:46-48](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/remote_executors.py#L46-L48) (verified)
  - *To reach the next level:* No narrower default to set; L1 needs any default narrower than the host's authority.
- **B L1:** The framework neither narrows nor widens the developer's credentials; model code can't import os by default, but the executor isn't a boundary. Evidence: [src/smolagents/local_python_executor.py:130-141](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/local_python_executor.py#L130-L141); [SECURITY.md:80](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/SECURITY.md#L80) (inferred)
  - *To reach the next level:* Developer credentials are fully reachable; L2 needs agent tools limited to one system.
- **Cap:** none

### C2 Approval gates: 0.00 (high confidence)

There is no approval mechanism anywhere in the tool execution path. Step callbacks fire after a step has already run, and interrupt() is checked between steps. Under the frameworks rule this is L0 even though the bundled tools are read-only: any tool a developer registers executes without a gate, and nothing offers checkpoints or dry-runs.

- **S L0:** No approval; step_callbacks run after a step executes. Evidence: searched `rg -n -S 'approv|confirm|human_in|ask_user'` in `src/smolagents/` → 4 hits (none in the execution path); [src/smolagents/agents.py:304](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/agents.py#L304); [src/smolagents/agents.py:623](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/agents.py#L623) (verified)
  - *To reach the next level:* No approval primitive; L1 needs any human approval hook in the tool executor.
- **C L0:** No gate exists; every registered tool executes directly. Evidence: [src/smolagents/agents.py:1476](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/agents.py#L1476) (verified)
  - *To reach the next level:* Nothing is gated; L1 needs gating on tools flagged as mutating.
- **D L0:** No approval primitive to default on. Evidence: searched `rg -n -S 'approv|confirm|allow|permission'` in `src/smolagents/gradio_ui.py src/smolagents/cli.py` → 11 hits (only a license comment and file-type allowlist) (verified)
  - *To reach the next level:* No gate to enable; L1 needs a gate on by default.
- **B L0:** No checkpoint, undo, or dry-run primitive bounds a bad action. Evidence: searched `rg -n -S 'checkpoint|undo|rollback|dry_run'` in `src/smolagents/` → 10 hits (all hits are ML model 'checkpoint' names in pipeline tools) (verified)
  - *To reach the next level:* No undo, preview, or rate limit for registered tools; L1 needs some reversibility.
- **Cap:** none

### C3 Tool & action scoping: 0.30 (high confidence)

Tool arguments are checked for type and presence only, and only on the ToolCallingAgent path; CodeAgent calls tools from generated code without that check. The bundled page-visit tool fetches any URL it is given, including internal addresses. On the positive side, agents receive only the tools the developer lists, since base tools are off by default.

- **S L1:** Type/presence-only validation; visit_webpage does a raw requests.get(url). Evidence: [src/smolagents/tools.py:1361-1367](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/tools.py#L1361-L1367); [src/smolagents/default_tools.py:528](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/default_tools.py#L528) (verified)
  - *To reach the next level:* Type checks only; L2 needs content validation such as URL host checks.
- **C L1:** validate_tool_arguments runs only on the ToolCallingAgent path. Evidence: [src/smolagents/agents.py:1476](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/agents.py#L1476) (verified)
  - *To reach the next level:* Validation runs only on the ToolCallingAgent path; L2 needs most tools covered, including CodeAgent calls.
- **D L2:** add_base_tools=False: the agent gets only developer-listed tools. Evidence: [src/smolagents/agents.py:301](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/agents.py#L301) (verified)
  - *To reach the next level:* Developer-listed tools are all enabled; L3 needs read-only tools by default.
- **B L1:** visit_webpage can reach any host, including localhost and cloud metadata addresses. Evidence: [src/smolagents/default_tools.py:515-528](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/default_tools.py#L515-L528) (verified)
  - *To reach the next level:* visit_webpage reaches any host, including internal ones; L2 needs scoping, such as blocking internal addresses.
- **Cap:** none

### C4 Code-execution isolation: 0.50 (medium confidence)

By default, model-written code runs in an in-process AST interpreter with an import allowlist and a denylist of dangerous modules. It is a sensible filter, but the project's own security policy says it is not a security boundary and that escaping it is expected. Remote sandboxes (E2B, Docker, Modal, Blaxel) are available on request; E2B runs both model code and registered tools remotely without passing the host environment, but network egress is unrestricted and the option is off by default.

- **default configuration** (default; raw 0.33 → 0.33)
  - **S L1:** In-process AST interpreter with import allowlist and denylist; maintainers disclaim it as a boundary. Evidence: [src/smolagents/local_python_executor.py:130-153](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/local_python_executor.py#L130-L153); [src/smolagents/utils.py:49-61](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/utils.py#L49-L61); [SECURITY.md:80](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/SECURITY.md#L80); [src/smolagents/local_python_executor.py:1693](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/local_python_executor.py#L1693) (verified)
    - *To reach the next level:* In-process AST filter its authors disclaim as a boundary; L2 needs OS-level separation.
  - **C L2:** All CodeAgent code goes through the configured executor; registered tools run in the host process. Evidence: [src/smolagents/agents.py:1602-1605](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/agents.py#L1602-L1605) (verified)
    - *To reach the next level:* Registered tools run outside the interpreter; L3 needs every execution path sandboxed.
  - **D L2:** executor_type='local' by default; developers can authorize '*' imports with a warning. Evidence: [src/smolagents/agents.py:1535](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/agents.py#L1535); [src/smolagents/agents.py:1578-1580](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/agents.py#L1578-L1580) (verified)
    - *To reach the next level:* Developers can authorize '*' imports with only a warning; L3 needs disabling to require an explicit operator flag.
  - **B L0:** In-process: host filesystem, network, and environment are reachable on escape. Evidence: [SECURITY.md:80](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/SECURITY.md#L80) (verified)
    - *To reach the next level:* An escape reaches the host process's files, network, and credentials; L1 needs at least the credentials kept out of reach.
- **opt-in E2B remote sandbox (executor_type='e2b')** (alt; raw 0.62, cap G1 → 0.50) ← counted
  - **S L4:** Remote ephemeral sandbox service. Evidence: [src/smolagents/remote_executors.py:335](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/remote_executors.py#L335); [src/smolagents/remote_executors.py:366-370](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/remote_executors.py#L366-L370) (verified)
  - **C L3:** Model code and registered tool definitions both run inside the sandbox. Evidence: [src/smolagents/agents.py:1616-1617](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/agents.py#L1616-L1617); [src/smolagents/remote_executors.py:94-112](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/remote_executors.py#L94-L112) (verified)
    - *To reach the next level:* Some registered tools may still run locally; L4 needs every path sandboxed with no fallback.
  - **D L0:** Off by default. Evidence: [src/smolagents/agents.py:1535](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/agents.py#L1535) (verified)
    - *To reach the next level:* Off by default; L1+ needs it on.
  - **B L2:** Only explicit kwargs reach the sandbox (no host env), but egress is unrestricted in code. Evidence: [src/smolagents/remote_executors.py:366-370](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/remote_executors.py#L366-L370); searched `rg -n -S 'network|egress|internet'` in `src/smolagents/remote_executors.py` → 0 hits (file-wide search; no network restriction anywhere in the executors) (inferred)
    - *To reach the next level:* Sandbox network egress is unrestricted; L3 needs egress off or allowlisted.
- **Cap:** G1: Opt-in mechanism: off in the scored default configuration.

### C5 Untrusted input blast radius: 0.00 (high confidence)

Assume an attacker controls a web page or search result the agent reads. Nothing in smolagents limits what happens next: untrusted content enters the agent's memory like any other observation, the hijacked agent can still fetch any URL (an outbound channel for leaking data), and every tool the developer registered remains available with no approval step. The worst case is therefore data leakage plus whatever irreversible actions the developer's tools allow, with no human involved.

- **S L0:** No provenance, taint, or detection; observations stored as-is. Evidence: searched `rg -n -S 'untrusted|taint|provenance|injection|spotlight'` in `src/smolagents/` → 6 hits (hits are pickle warnings, a sandbox-injection docstring, and the executor's own 'not a security sandbox' note; none handles untrusted content); [src/smolagents/memory.py:60](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/memory.py#L60) (verified)
  - *To reach the next level:* No provenance or structural limit; L1 needs at least detection or labelling.
- **C L0:** No source is distinguished; search results and page content enter context like any observation. Evidence: [src/smolagents/default_tools.py:243](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/default_tools.py#L243); [src/smolagents/default_tools.py:528](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/default_tools.py#L528) (verified)
  - *To reach the next level:* No source is distinguished; L1 needs one untrusted source handled.
- **D L0:** No mechanism to default on. Evidence: searched `rg -n -S 'untrusted|taint|provenance|injection|spotlight'` in `src/smolagents/` → 6 hits (hits are pickle warnings, a sandbox-injection docstring, and the executor's own 'not a security sandbox' note; none handles untrusted content) (verified)
  - *To reach the next level:* No mechanism to default on; L1 needs a limit that is on by default.
- **B L0:** Worst case: hijacked agent can leak data via arbitrary-URL fetch and run any registered tool unattended; the framework prevents neither. Evidence: [README.md:61-64](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/README.md#L61-L64); [src/smolagents/default_tools.py:528](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/default_tools.py#L528) (verified)
  - *To reach the next level:* Leak plus unattended actions possible; L1 needs one of the two to require a human.
- **Cap:** C5-WORSTCASE: Worst case (B L0): a hijacked agent can leak data and take irreversible actions unattended.

### C6 Memory, context & configuration integrity: 0.25 (medium confidence)

Agent memory lives only in the running process and is never persisted, which keeps poisoning session-scoped. The concern is configuration: both the CLI and the remote-executor module call load_dotenv(), which reads a .env file from the current working directory. If a user runs an agent inside a cloned repository, that repository can set environment variables such as a model API base URL or a sandbox provider key without any prompt.

- **S L1:** .env silently loaded from the working directory; no memory persistence. Evidence: [src/smolagents/cli.py:230](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/cli.py#L230); [src/smolagents/remote_executors.py:46-48](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/remote_executors.py#L46-L48); [src/smolagents/agents.py:892](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/agents.py#L892) (verified)
  - *To reach the next level:* .env loads silently from the working directory; L2 needs security-relevant config to come only from user scope.
- **C L1:** The one auto-loaded path is uncontrolled. Evidence: [src/smolagents/cli.py:230](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/cli.py#L230); [src/smolagents/memory.py:53-63](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/memory.py#L53-L63) (verified)
  - *To reach the next level:* The .env path is uncontrolled; L2 needs every auto-loaded path controlled.
- **D L2:** Memory is per agent instance and never shared. Evidence: [src/smolagents/agents.py:602](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/agents.py#L602) (verified)
  - *To reach the next level:* Memory isolation per instance only; L3 needs the model unable to alter isolation (already true) plus enforced namespaces.
- **B L2:** A repo .env persists across runs and could set OPENAI_BASE_URL (read by the openai SDK) or E2B_API_KEY; memory is session-scoped. Evidence: [src/smolagents/remote_executors.py:46-48](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/remote_executors.py#L46-L48); [src/smolagents/memory.py:53](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/memory.py#L53) (inferred)
  - *To reach the next level:* A repo .env persists across runs; L3 needs nothing workspace-controlled to persist into behaviour.
- **Cap:** C6-REPOCONFIG: load_dotenv() from the working directory (verified) lets a cloned repo redirect security-relevant endpoints or credentials (impact inferred from openai SDK env handling).

### C7 Third-party extensions: 0.12 (high confidence)

Loading tools or agents from the Hugging Face Hub, Spaces, or MCP servers requires an explicit trust_remote_code=True flag, which is a genuine consent step. Beyond that, nothing protects you: versions aren't pinned by default, nothing checks that the code is what you approved, and loaded code runs inside the agent's own process with all of its access. The project's own docs and examples set the flag to True in about twenty places, which teaches users to bypass the consent step.

- **S L1:** Remote code behind an acknowledgement flag; no digest or signature check. Evidence: [src/smolagents/tools.py:517-551](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/tools.py#L517-L551); searched `rg -n -S 'sha256|digest|signature'` in `src/smolagents/` → 25 hits (all hits are Python function-signature handling; no integrity verification) (verified)
  - *To reach the next level:* Hub code is unpinned and unverified; L2 needs version pinning by default.
- **C L0:** Hub tools, Spaces, MCP tools, and Hub agents are all unverified. Evidence: [src/smolagents/tools.py:600](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/tools.py#L600); [src/smolagents/tools.py:1052-1055](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/tools.py#L1052-L1055); [src/smolagents/agents.py:1097](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/agents.py#L1097) (verified)
  - *To reach the next level:* No extension type is verified; L1 needs at least one type pinned or checked.
- **D L1:** Safe API default (False), lowered one level because official examples set it True. Evidence: [src/smolagents/tools.py:521](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/tools.py#L521); [src/smolagents/tools.py:1005](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/tools.py#L1005); searched `rg -n 'trust_remote_code\s*=\s*True'` in `examples/ README.md docs/` → 20 hits (verified)
  - *To reach the next level:* Consent flag exists but official examples set it True; L2 needs examples that keep consent explicit.
- **B L0:** Loaded code executes on the local machine in-process. Evidence: [src/smolagents/tools.py:1052-1055](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/tools.py#L1052-L1055); [SECURITY.md:73](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/SECURITY.md#L73) (verified)
  - *To reach the next level:* Loaded code runs in-process with full authority; L1 needs a separate process.
- **Cap:** none
- **Notes:** Optional revision= pinning exists but is unset by default.

### C8 Secrets & sensitive-data protection: 0.23 (medium confidence)

Provider keys come from environment variables and there is no redaction anywhere: neither console logs nor the tool observations sent to the model are scrubbed. There is no telemetry, which is good. Model code can't import os by default, so it can't trivially read the environment, but that protection inherits the local executor's weakness.

- **S L1:** Keys from env; no redaction (the only 'redact' hit is a variable name). Evidence: [src/smolagents/cli.py:230](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/cli.py#L230); [src/smolagents/default_tools.py:243-244](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/default_tools.py#L243-L244) (verified)
  - *To reach the next level:* Keys come from env with no redaction; L2 needs masking on main paths.
- **C L0:** Neither logs nor model-bound observations are redacted. Evidence: searched `rg -n -S 'redact|mask|scrub|SecretStr'` in `src/smolagents/` → 2 hits (both hits are a variable name in default_tools.py) (verified)
  - *To reach the next level:* No redaction on logs or model-bound text; L1 needs one path redacted.
- **D L2:** No telemetry; console logging of observations at default INFO level. Evidence: searched `rg -n -S 'sentry|posthog|telemetry|analytics'` in `src/smolagents/` → 0 hits; [src/smolagents/monitoring.py:120-124](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/monitoring.py#L120-L124) (verified)
  - *To reach the next level:* Observations print to console by default; L3 needs redaction that is always on.
- **B L1:** Long-lived provider keys sit in the process environment. Evidence: [src/smolagents/local_python_executor.py:134](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/local_python_executor.py#L134); [SECURITY.md:80](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/SECURITY.md#L80) (inferred)
  - *To reach the next level:* Long-lived provider keys sit in the process environment; L2 needs scoped keys.
- **Cap:** none

### C9 Audit & traceability: 0.28 (high confidence)

Each step is recorded as a structured object (tool calls, observations, timings), but only in the agent's in-process memory; nothing is written to disk by default, so the record disappears when the process exits. OpenTelemetry tracing is documented, but via a third-party package, so it isn't credited.

- **S L1:** Structured steps kept in memory only; no persisted transcript. Evidence: [src/smolagents/memory.py:53-63](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/memory.py#L53-L63); searched `rg -n -S 'jsonl|trajectory|transcript'` in `src/smolagents/` → 0 hits (verified)
  - *To reach the next level:* Steps are kept in memory only; L2 needs a structured record persisted to disk.
- **C L2:** Every top-level step is recorded; managed agents keep separate memories. Evidence: [src/smolagents/agents.py:602](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/agents.py#L602); [src/smolagents/agents.py:369](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/agents.py#L369) (verified)
  - *To reach the next level:* Managed agents keep separate memories; L3 needs sub-agent actions in one correlated record.
- **D L1:** On by default but held in the agent's own process. Evidence: [src/smolagents/agents.py:488](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/agents.py#L488) (verified)
  - *To reach the next level:* The record lives in the agent's own process; L2 needs storage outside the agent's reach.
- **B L0:** Lost at process exit; tracing is docs-only via a third-party package. Evidence: [docs/source/en/tutorials/inspect_runs.md:46](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/docs/source/en/tutorials/inspect_runs.md#L46) (verified)
  - *To reach the next level:* The record is lost at process exit; L1 needs a best-effort persisted record.
- **Cap:** none

### C10 Limits & kill switch: 0.45 (high confidence)

Runs stop after 20 steps by default and each code execution has a timeout, but there's no token or cost ceiling. Stopping is incomplete: the halt is checked between steps, and when code execution times out its thread keeps running in the background. Managed sub-agents start their own step budgets, so delegation escapes the parent's limit.

- **S L2:** max_steps=20 enforced in the loop plus per-execution timeout; no token/cost cap. Evidence: [src/smolagents/agents.py:300](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/agents.py#L300); [src/smolagents/agents.py:545](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/agents.py#L545); [src/smolagents/local_python_executor.py:285-299](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/local_python_executor.py#L285-L299) (verified)
  - *To reach the next level:* No token or cost cap; L3 needs step, time, and cost caps all enforced.
- **C L2:** Top-level loop plus execution timeouts; managed agents run with their own budgets. Evidence: [src/smolagents/agents.py:369-373](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/agents.py#L369-L373) (verified)
  - *To reach the next level:* Managed agents get fresh budgets; L3 needs sub-agents counted against the parent's budget.
- **D L2:** Sensible default, but delegating to a managed agent starts a fresh budget. Evidence: [src/smolagents/agents.py:300](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/agents.py#L300) (verified)
  - *To reach the next level:* Delegation resets step budgets; L3 needs limits the model can't reset by delegating.
- **B L1:** A 20-step ceiling exists, but timed-out code keeps running in the background after the agent gives up on it. Evidence: [src/smolagents/local_python_executor.py:299-300](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/local_python_executor.py#L299-L300); [src/smolagents/agents.py:300](https://github.com/huggingface/smolagents/blob/c30b115286e000e98711fae5e85993547b73d826/src/smolagents/agents.py#L300) (verified)
  - *To reach the next level:* Timed-out code keeps running in the background; L2 needs stop to end all work.
- **Cap:** none
- **Notes:** Halt is cooperative (agents.py:546).

## Rule-of-Two check
[A] untrusted input: web search and page fetch (default_tools.py:243, :528) · [B] sensitive data/systems: whatever the developer adds; the framework doesn't constrain it · [C] state change / egress: arbitrary GET via visit_webpage (default_tools.py:528) · Same default session? Yes

## Highest-impact improvements
1. Make a sandboxed executor the default and require an explicit unsafe flag for local execution. (C4 D L0→L3, +0.150 before caps; Playbook 3, step 1)
2. Add an approval hook in the tool executor, consulted for every registered tool, with default-deny for unknown tools. (C2 S L0→L2, +0.150 before caps; Playbook 5, step 1)
3. Tag observations with provenance and disable egress tools after untrusted content enters the session. (C5 S L0→L3, +0.225 before caps; Playbook 1, step 2)
4. Block internal addresses and recheck redirects in visit_webpage. (C3 S L1→L3, +0.150 before caps; Playbook 3, step 1)
5. Load .env only from the user's config directory, never the working directory. (C6 S L1→L3, +0.150 before caps; Playbook 2, step 1)

## Re-audit log
- C4 C: L2 → L3. Alt mechanism: send_tools defines registered tools inside the sandbox (remote_executors.py:94-112); was inferred, now verified. No score change (G1).
- C10 B: L2 → L1. C10 B measures what happens before limits trip or after stop; timed-out code keeps running in the background (local_python_executor.py:299-300).

## Limitations
- Static source review of commit c30b115 only; nothing was executed, installed, or probed.
- Framework scored by its defaults: absent primitives score L0 even where a developer could add them.
- Docker, Modal, and Blaxel executors not scored separately (E2B was the strongest opt-in).
- Model behaviour (refusals, deception) is out of scope; only code-level controls are scored.
- No reviewer-directed prompt injection found in the repo.
