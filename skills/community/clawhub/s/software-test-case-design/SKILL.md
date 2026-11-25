---
name: test-case-design
description: Use this skill to generate, write, or design test cases for a specific scenario or feature, add negative scenarios and boundary values, design test cases for complex interactions, or output standardized test cases — e.g., functional testing, compatibility testing, adaptability testing, API testing, UI visual testing, mobile / app / mini program / H5 / desktop / PC web testing, AI agent testing, linkage testing, or routing testing. Focuses only on writing test cases; does not cover test plans, test strategies, or automation scripts.
---

## Workflow

1. **Identify the mode**:
   - The request contains "supplement" / "complete" / "improve" / "fill the gaps" / "add negative cases" / "add boundary cases", or the user provides existing test cases → Supplement mode (see "Supplement Mode Rules"; steps 2–5 and 7–8 run as usual, and step 6 generates cases according to the Supplement Mode Rules)
   - Otherwise → New mode
2. **Identify the test case type** (see "Type Identification Rules"):
   - API signals only → API test cases
   - Agent signals only → Agent test cases
   - Both API and Agent signals → confirm the test scope with the user first
   - Neither signal → Functional test cases (default)
3. **Identify the platform** (skip for API testing): match keywords in the "Platform Files" table; resolve ambiguity according to the "Platform Identification Rules"
4. **Requirement analysis and clarification**:
   - Extract the object under test, feature points, input constraints (type / length / range / required), business rules, state transitions, roles and permissions, and platform
   - **Handling input materials**: when the user provides requirement materials, extract constraints from them first, then decide whether questions are needed
     - PRD / requirement documents: extract feature points, field constraints, business rules, and exception descriptions item by item; put the requirement ID or section into "Related Requirement"
     - Prototypes / UI screenshots: identify page elements (input boxes, buttons, drop-downs, lists, etc.), copy text, navigation relationships, and interaction states; treat constraints that cannot be determined from the image (e.g., length, range) as missing constraints
     - Swagger / OpenAPI / API documents: extract the URL, request method, parameters (type / required / enum / range), request and response examples, error codes, and authentication method
     - Existing test cases: parse them according to the "Supplement Mode Rules"
     - When materials contradict each other, list the conflicts and confirm with the user; if the user asks to generate directly, follow the latest version of the materials and record the conflicts in "Assumptions to Confirm"
   - When key constraints are missing and concrete test data cannot be given, ask the user all questions at once, no more than 3
   - When the user asks to generate directly, write reasonable assumptions into the preconditions marked "(assumption)", e.g., "Username length is 6–18 characters (assumption)", and list "Assumptions to Confirm" at the end of the output
5. **Load files**:
   - Rules file: always load `references/templates/common-rules.md`
   - Capability files: load according to the "Capability Files" table
   - Platform files: load `references/platform/{platform}.md` for each identified platform; multiple files can be stacked
6. **Generate test cases**: generate test cases according to the loaded rules, capability, and platform files
7. **Self-check**: check item by item against the checklists in the table below; add test cases directly for any gaps found; do not list the checklist in the output

   | Test case type | Checklist |
   |---------|---------|
   | API testing | `references/checklists/api-checklist.md` |
   | Agent testing | `references/checklists/agent-checklist.md` + `references/checklists/common-checklist.md` (only "1. Functional Testing Checklist") |
   | Agent testing + platform | Agent testing checklists + `references/checklists/{platform}-checklist.md` |
   | Agent + API | API part follows "API testing"; Agent part follows "Agent testing" or "Agent testing + platform" |
   | Functional testing + platform | `references/checklists/common-checklist.md` + `references/checklists/{platform}-checklist.md` |
   | Functional testing (no platform) | `references/checklists/common-checklist.md` |

8. **Output**: output Markdown tables in the format defined in `references/examples/format-spec.md`

## Capability Boundaries
✅ Can generate: functional testing, API testing, AI agent testing (including agent safety and boundaries), platform-specific testing
❌ Cannot generate: test plans, test strategies, test schedules, penetration test execution, vulnerability scanning, performance stress testing (concurrency / stress / load), automation scripts

> Performance cases are limited to performance-experience cases that can be observed manually or with tools (e.g., startup time, first-screen load, scrolling frame rate, whether memory keeps growing). Do not generate concurrency, stress, load, stability, or capacity cases.

## Type Identification Rules

- **API signals**: "API testing", "interface testing", or the requirement provides a URL, request method, request / response body, or Swagger / OpenAPI document
- **Agent signals**: "Agent testing", "AI agent testing", "intelligent agent", "AI assistant", "chatbot", "LLM application"
  - When the word "Agent" appears alone, judge from context: it is an Agent signal when it refers to an AI agent; "sales agent", "User-Agent", etc. are not; ask the user when unsure

| Situation | Handling |
|-----|---------|
| Agent signals only | Treat as Agent testing |
| API signals only | Treat as API testing |
| Both signals, and the user has not stated the scope | Ask the user first (template below) |
| The user has explicitly asked for both | Do not ask; treat as "Agent + API" |
| Already asked, but the user asks to generate directly | Treat as "Agent + API" by default |

**Question template**:

> Your requirement involves both an Agent and APIs. Please confirm the test scope:
> 1. Agent testing only (dialogue understanding, behavior, tool calls, safety boundaries, etc.)
> 2. API testing only (the APIs exposed by the Agent service)
> 3. Agent + API (generate both)

**"Agent + API" rules**:
- Load: `references/core-capabilities/api-testing.md` + `references/core-capabilities/agent-testing.md` + `references/core-capabilities/functional-testing.md` (only Part 1 "Test Case Design Methods" and Part 2 "Test Case Quality Standards")
- Output: split into "1. API Test Cases" and "2. Agent Test Cases", with IDs prefixed `TC_API_` and `TC_AGENT_` respectively; each part numbers from 001
- Platform: platform files apply only to the Agent part, not the API part
- Self-check: follow the "Agent + API" row of the table in step 7
- De-duplication: for the same scenario, each part tests one side. For example, for "tool call failure", the API part only verifies the error code and payload returned by the API, and the Agent part only verifies how the Agent handles it and informs the user

## Platform Identification Rules

- **No platform matched**: generate general functional tests; if the requirement mentions "compatibility testing" / "adaptability testing" / "adaptation" without a platform, ask for the platform first and then load the matching platform file (compatibility and adaptability test points are in each platform file)
- **Overlapping keywords (longest match first)**: match the longest keyword first; shorter keywords contained in it are not counted separately. For example: "mobile web" only matches mobile-web and does not also match pc-web via "web"; "desktop app" only matches desktop and does not also match mobile-app via "app"; "mobile webpage", "in-WeChat webpage", and "WeChat Official Account page" only match mobile-web and do not trigger the "webpage" question
- **Multiple platforms matched** (still more than one after longest-match de-duplication): load all of them; write general functional cases only once and group platform-specific cases by platform
- **"Mobile"**: context contains "download" / "install" / "app store" → mobile-app; contains "browser" / "link" / "H5" → mobile-web; ask the user if unclear
- **"Client"**: contains "PC" / "computer" → desktop; contains "phone" → mobile-app; ask the user if unclear
- **"Webpage"**: contains "phone" / "mobile" → mobile-web; otherwise ask the user whether it is PC Web or mobile web (H5) (if another platform keyword such as "PC Web" or "Web client" is already matched, follow that platform)

## Supplement Mode Rules

1. Parse the IDs, feature modules, and covered test points of the user's existing test cases, and identify the test case type and platform according to workflow steps 2 and 3
2. Choose the basis for supplementing by test case type, and combine equivalence partitioning, boundary value analysis, and error guessing to find uncovered test points:
   - Functional testing: "1.9 Negative and Boundary Supplement Points" in `references/core-capabilities/functional-testing.md`
   - API testing: each dimension of `references/core-capabilities/api-testing.md`, focusing on parameter validation (required / type / length / range / format), authentication and authorization, security testing, error handling, and pagination out-of-range
   - Agent testing: each dimension of `references/core-capabilities/agent-testing.md`, focusing on ambiguous instructions, out-of-scope instructions, tool call failures, safety and boundaries, and extreme inputs; also refer to the text input points in "1.9" of functional-testing.md
   - Agent + API: supplement each part according to its basis above
   - When a platform is involved: add the platform-specific points from the corresponding platform file (e.g., interruption recovery, network switching, permission denial)
3. Output only new test cases; do not repeat existing ones
4. Numbering: if the existing cases have IDs, follow their numbering style and continue from the largest sequence number; otherwise number them according to the numbering rules in `references/templates/common-rules.md`
5. Append a "Supplementary Coverage Notes" table at the end of the output (format in `references/examples/format-spec.md`)
6. If the user provides no existing cases and only asks to "add negative and boundary cases", generate only negative-scenario and boundary-value cases

## Instruction Mapping

> Always load the rules file `references/templates/common-rules.md`. Capability files are chosen by test case type; platform files are stacked as needed.

### Capability Files

| Keyword trigger | Load | Notes |
|-----------|------|------|
| API signals ("API testing", "interface testing", etc.) | `references/core-capabilities/api-testing.md` | Used alone; no platform stacking |
| Agent signals ("Agent testing", "intelligent agent", etc.) | `references/core-capabilities/agent-testing.md` + `references/core-capabilities/functional-testing.md` (only Part 1 "Test Case Design Methods" and Part 2 "Test Case Quality Standards") | Can be stacked with any platform |
| Agent + API | Load the files of both rows above | Platform applies only to the Agent part |
| Default | `references/core-capabilities/functional-testing.md` | Functional testing |

### Platform Files (stacked on capability files, except for API testing)

| Keyword trigger | Load | Notes |
|-----------|------|------|
| "mobile app testing", "App testing", "App", "iOS", "Android", "mobile application", "HarmonyOS" | `references/platform/mobile-app.md` | Gestures / screen adaptation / interruption / network / permissions / push / device compatibility / system interaction / storage / updates / performance / accessibility |
| "mini program testing", "mini program", "WeChat Mini Program", "Alipay Mini Program", "Douyin Mini Program" | `references/platform/mini-program.md` | Lifecycle / authorization / sharing / payment / navigation / subscription messages / storage / maps and location / platform differences |
| "mobile web testing", "H5 testing", "H5", "mobile web", "mobile webpage", "WAP", "WeChat Official Account page", "in-WeChat webpage" | `references/platform/mobile-web.md` | Browsers / touch / responsive / viewport / keyboard input / H5-specific / third-party login and payment / WebView / network and cache / performance / SEO and sharing |
| "desktop testing", "desktop app testing", "desktop", "desktop app", "PC client", "Windows app", "macOS app" | `references/platform/desktop.md` | Windows / shortcuts / files / system integration / multiple monitors / install and update / system compatibility |
| "PC Web testing", "Web client testing", "PC Web", "Web client", "webpage" (confirm per "Platform Identification Rules") | `references/platform/pc-web.md` | Browsers / layout / keyboard / forms / sessions / multiple windows / routing / linkage / drag and drop / rich text / files / i18n / dark mode / printing / network and cache / performance |
