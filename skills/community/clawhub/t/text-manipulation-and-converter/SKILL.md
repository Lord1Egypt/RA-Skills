---
name: text-manipulation-and-converter
description: "Text Manipulation and Converter: Manipulate text: case conversion (11 formats), whitespace handling, line operations, sorting, deduplication, wrapping, character counts. Use when an agent needs text manipulation and converter, converting variable names between programming language conventions, cleaning and normalizing imported data, meeting word or character count requirements, formatting text to specific column widths, add quotes, text, quote type through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/text-manipulation-and-converter
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/text-manipulation-and-converter"}}
---
# Text Manipulation and Converter

## Freshness
Last updated: `2026-06-23`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Text Tools is a comprehensive text manipulation utility providing 23 operations across four categories: text manipulation, case conversion, special transformations, and counting.

Text manipulation operations handle whitespace and line-level transformations. These include removing line breaks, collapsing extra spaces, sorting lines alphabetically (ascending or descending), removing duplicate lines while preserving order, adding quotes (single, double, or backtick) to each line, converting between tabs and spaces with configurable width (1–16), trimming whitespace from lines, removing empty lines, normalizing whitespace comprehensively, indenting and dedenting text, wrapping text at a specified column width (10–200), unwrapping text, and reversing line order.

Case conversion supports 11 formats through a single action: camelCase, snake_case, PascalCase, kebab-case, SCREAMING_SNAKE_CASE, UPPERCASE, lowercase, Title Case, Sentence case, dot.case, and path/case.

Special transformations include reversing text character-by-character, removing accents and diacritical marks (é becomes e), alternating case (aLtErNaTiNg), and detecting the case style of input text.

Counting operations return line count, word count, and detailed character statistics including totals with and without spaces, letter count, digit count, and space count.

## Product Instructions
### Text Manipulation and Converter - Instructions

#### Overview

A comprehensive text processing tool for manipulating, converting, and analyzing text. Supports whitespace management, case conversion across 11 formats, line operations, and character/word/line counting.

---

#### Actions

##### Text Manipulation

###### remove-line-breaks
Converts multi-line text into a single line by replacing line breaks with spaces.

- **Required:** `text` (string) - The input text
- **Optional:** None

**Example:**
```json
{ "action": "remove-line-breaks", "text": "Hello\nWorld\nFoo" }
```
Returns: `"Hello World Foo"`

---

###### remove-extra-spaces
Collapses multiple consecutive spaces into a single space.

- **Required:** `text` (string)
- **Optional:** None

**Example:**
```json
{ "action": "remove-extra-spaces", "text": "Hello    world   foo" }
```
Returns: `"Hello world foo"`

---

###### sort-lines
Sorts lines alphabetically in ascending or descending order.

- **Required:** `text` (string)
- **Optional:** `order` (string) - `"asc"` (default) or `"desc"`

**Example:**
```json
{ "action": "sort-lines", "text": "banana\napple\ncherry", "order": "asc" }
```
Returns: `"apple\nbanana\ncherry"`

---

###### remove-duplicate-lines
Removes duplicate lines while preserving the original order of first occurrences.

- **Required:** `text` (string)
- **Optional:** None

**Example:**
```json
{ "action": "remove-duplicate-lines", "text": "apple\nbanana\napple\ncherry\nbanana" }
```
Returns: `"apple\nbanana\ncherry"`

---

###### add-quotes
Wraps each line in quotes of the specified type.

- **Required:** `text` (string)
- **Optional:** `quote_type` (string) - `"single"`, `"double"` (default), or `"backtick"`

**Example:**
```json
{ "action": "add-quotes", "text": "apple\nbanana", "quote_type": "single" }
```
Returns: `"'apple'\n'banana'"`

---

###### tabs-to-spaces
Converts tab characters to spaces.

- **Required:** `text` (string)
- **Optional:** `tab_width` (integer, 1-16, default: 4) - Number of spaces per tab

**Example:**
```json
{ "action": "tabs-to-spaces", "text": "\tHello\n\t\tWorld", "tab_width": 2 }
```

---

###### spaces-to-tabs
Converts leading spaces to tab characters.

- **Required:** `text` (string)
- **Optional:** `tab_width` (integer, 1-16, default: 4) - Number of spaces per tab

**Example:**
```json
{ "action": "spaces-to-tabs", "text": "    Hello\n        World", "tab_width": 4 }
```

---

###### trim-whitespace
Removes leading and trailing whitespace from each line and the overall text.

- **Required:** `text` (string)
- **Optional:** None

**Example:**
```json
{ "action": "trim-whitespace", "text": "  Hello  \n  World  " }
```
Returns: `"Hello\nWorld"`

---

###### remove-empty-lines
Removes all blank/empty lines from the text.

- **Required:** `text` (string)
- **Optional:** None

**Example:**
```json
{ "action": "remove-empty-lines", "text": "Hello\n\n\nWorld\n\nFoo" }
```
Returns: `"Hello\nWorld\nFoo"`

---

###### normalize-whitespace
Comprehensive cleanup: trims each line, removes empty lines, and collapses multiple spaces within lines.

- **Required:** `text` (string)
- **Optional:** None

**Example:**
```json
{ "action": "normalize-whitespace", "text": "  Hello   world  \n\n  Foo   bar  " }
```
Returns: `"Hello world\nFoo bar"`

---

###### indent-text
Adds consistent indentation to every line of text.

- **Required:** `text` (string)
- **Optional:**
  - `indent_char` (string) - `"space"` (default) or `"tab"`
  - `indent_count` (integer, 1-16, default: 4) - Number of indent characters per level

**Example:**
```json
{ "action": "indent-text", "text": "Hello\nWorld", "indent_char": "space", "indent_count": 2 }
```
Returns: `"  Hello\n  World"`

---

###### dedent-text
Removes common leading whitespace from all lines (the minimum shared indentation).

- **Required:** `text` (string)
- **Optional:** None

**Example:**
```json
{ "action": "dedent-text", "text": "    Hello\n    World\n        Nested" }
```
Returns: `"Hello\nWorld\n    Nested"`

---

###### wrap-text
Wraps text to fit within a specified column width.

- **Required:** `text` (string)
- **Optional:** `width` (integer, 10-200, default: 80) - Maximum line width

**Example:**
```json
{ "action": "wrap-text", "text": "This is a long sentence that should be wrapped at a shorter width.", "width": 30 }
```

---

###### unwrap-text
Joins all lines into a single line, removing line breaks.

- **Required:** `text` (string)
- **Optional:** None

**Example:**
```json
{ "action": "unwrap-text", "text": "This is\na wrapped\nparagraph." }
```
Returns: `"This is a wrapped paragraph."`

---

###### reverse-lines
Reverses the order of lines (last line becomes first).

- **Required:** `text` (string)
- **Optional:** None

**Example:**
```json
{ "action": "reverse-lines", "text": "first\nsecond\nthird" }
```
Returns: `"third\nsecond\nfirst"`

---

##### Case Conversion

###### change-case
Converts text to a target case format. Supports 11 case types.

- **Required:**
  - `text` (string)
  - `case_type` (string) - One of: `camel`, `snake`, `pascal`, `kebab`, `screaming-snake`, `upper`, `lower`, `title`, `sentence`, `dot`, `path`

**Case type reference:**
| case_type | Output |
|---|---|
| `camel` | `helloWorld` |
| `snake` | `hello_world` |
| `pascal` | `HelloWorld` |
| `kebab` | `hello-world` |
| `screaming-snake` | `HELLO_WORLD` |
| `upper` | `HELLO WORLD` |
| `lower` | `hello world` |
| `title` | `Hello World` |
| `sentence` | `Hello world` |
| `dot` | `hello.world` |
| `path` | `hello/world` |

**Example:**
```json
{ "action": "change-case", "text": "hello world example", "case_type": "camel" }
```
Returns: `"helloWorldExample"`

---

##### Special Text Operations

###### reverse-text
Reverses the entire text character by character.

- **Required:** `text` (string)
- **Optional:** None

**Example:**
```json
{ "action": "reverse-text", "text": "Hello" }
```
Returns: `"olleH"`

---

###### remove-accents
Strips accents and diacritical marks from characters.

- **Required:** `text` (string)
- **Optional:** None

**Example:**
```json
{ "action": "remove-accents", "text": "café résumé naïve" }
```
Returns: `"cafe resume naive"`

---

###### alternate-case
Alternates between uppercase and lowercase for each character position.

- **Required:** `text` (string)
- **Optional:** None

**Example:**
```json
{ "action": "alternate-case", "text": "hello world" }
```
Returns: `"HeLlO wOrLd"`

---

###### smart-case-detect
Detects the case style of the input text. Returns one of: `upper`, `lower`, `title`, `snake`, `kebab`, `dot`, `path`, `camel`, `pascal`, `mixed`, or `empty`.

- **Required:** `text` (string)
- **Optional:** None

**Example:**
```json
{ "action": "smart-case-detect", "text": "helloWorld" }
```
Returns: `"camel"`

---

##### Counting

###### count-lines
Counts the number of lines in the text.

- **Required:** `text` (string)
- **Optional:** None

**Example:**
```json
{ "action": "count-lines", "text": "Line 1\nLine 2\nLine 3" }
```
Returns: `3`

---

###### count-words
Counts the number of words in the text.

- **Required:** `text` (string)
- **Optional:** None

**Example:**
```json
{ "action": "count-words", "text": "Hello world this is a test" }
```
Returns: `6`

---

###### count-characters
Returns detailed character statistics including total characters, characters without spaces, letters, digits, spaces, and line count.

- **Required:** `text` (string)
- **Optional:** None

**Example:**
```json
{ "action": "count-characters", "text": "Hello World 123" }
```
Returns:
```json
{ "total": 15, "without_spaces": 13, "letters": 10, "digits": 3, "spaces": 2, "lines": 1 }
```

---

#### Common Workflows

1. **Clean messy text:** Use `normalize-whitespace` for a one-step cleanup of irregular spacing and blank lines.
2. **Prepare CSV values:** Use `add-quotes` with `quote_type: "double"` to wrap each line in quotes.
3. **Convert variable names:** Use `change-case` to convert between naming conventions (e.g., camelCase to snake_case).
4. **Analyze text:** Combine `count-words`, `count-characters`, and `count-lines` for a full text analysis.
5. **Deduplicate lists:** Use `sort-lines` followed by `remove-duplicate-lines` to get a clean sorted unique list.

#### Important Notes

- The `text` parameter is required for all actions.
- The `change-case` action requires the `case_type` parameter.
- All responses include metadata with original text length and (for string results) result length.
- `spaces-to-tabs` only converts leading spaces on each line, not spaces within text.
- `smart-case-detect` returns `"mixed"` when text does not match any recognized case pattern.

## When To Use
- Use this skill for `Text Manipulation and Converter` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: text manipulation and converter, converting variable names between programming language conventions, cleaning and normalizing imported data, meeting word or character count requirements, formatting text to specific column widths, add quotes, text, quote type.
- Supported action names: `add-quotes`, `alternate-case`, `change-case`, `count-characters`, `count-lines`, `count-words`, `dedent-text`, `indent-text`, `normalize-whitespace`, `remove-accents`, `remove-duplicate-lines`, `remove-empty-lines`, `remove-extra-spaces`, `remove-line-breaks`, `reverse-lines`, `reverse-text`, `smart-case-detect`, `sort-lines`, `spaces-to-tabs`, `tabs-to-spaces`, `trim-whitespace`, `unwrap-text`, `wrap-text`.

## Use Cases
- Converting variable names between programming language conventions
- cleaning and normalizing imported data
- meeting word or character count requirements
- formatting text to specific column widths
- sorting and deduplicating configuration lists
- standardizing tabs versus spaces
- generating quoted values for CSV or config files
- creating URL slugs from Unicode text
- detecting inconsistent naming conventions in codebases
- preparing text for systems requiring ASCII-only input
- batch formatting log files or text exports
- removing accents for search indexing.

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `23`.
x402 availability: not enabled for this product.

- `add-quotes` (action slug: `add-quotes`): Wrap each line in quotes of the specified type. Price: `5` credits. Parameters: `quote_type`, `text`.
- `alternate-case` (action slug: `alternate-case`): Alternate between uppercase and lowercase for each character position. Price: `5` credits. Parameters: `text`.
- `change-case` (action slug: `change-case`): Convert text to a target case format. Supports 11 case types: camel (camelCase), snake (snake_case), pascal (PascalCase), kebab (kebab-case), screaming-snake (SCREAMING_SNAKE_CASE), upper (UPPERCASE), lower (lowercase), title (Title Case), sentence (Sentence case), dot (dot.case), path (path/case). Price: `5` credits. Parameters: `case_type`, `text`.
- `count-characters` (action slug: `count-characters`): Return detailed character statistics: total characters, characters without spaces, letters, digits, spaces, and line count. Price: `5` credits. Parameters: `text`.
- `count-lines` (action slug: `count-lines`): Count the number of lines in the text. Price: `5` credits. Parameters: `text`.
- `count-words` (action slug: `count-words`): Count the number of words in the text. Price: `5` credits. Parameters: `text`.
- `dedent-text` (action slug: `dedent-text`): Remove common leading whitespace from all lines. Price: `5` credits. Parameters: `text`.
- `indent-text` (action slug: `indent-text`): Add consistent indentation to every line of text. Price: `5` credits. Parameters: `indent_char`, `indent_count`, `text`.
- `normalize-whitespace` (action slug: `normalize-whitespace`): Comprehensive cleanup: trim each line, remove empty lines, collapse multiple spaces. Price: `5` credits. Parameters: `text`.
- `remove-accents` (action slug: `remove-accents`): Strip accents and diacritical marks from characters. Price: `5` credits. Parameters: `text`.
- `remove-duplicate-lines` (action slug: `remove-duplicate-lines`): Remove duplicate lines while preserving the order of first occurrences. Price: `5` credits. Parameters: `text`.
- `remove-empty-lines` (action slug: `remove-empty-lines`): Remove all blank/empty lines from the text. Price: `5` credits. Parameters: `text`.
- `remove-extra-spaces` (action slug: `remove-extra-spaces`): Collapse multiple consecutive spaces into a single space. Price: `5` credits. Parameters: `text`.
- `remove-line-breaks` (action slug: `remove-line-breaks`): Convert multi-line text to a single line by replacing line breaks with spaces. Price: `5` credits. Parameters: `text`.
- `reverse-lines` (action slug: `reverse-lines`): Reverse the order of lines (last line becomes first). Price: `5` credits. Parameters: `text`.
- `reverse-text` (action slug: `reverse-text`): Reverse the entire text character by character. Price: `5` credits. Parameters: `text`.
- `smart-case-detect` (action slug: `smart-case-detect`): Detect the case style of input text. Returns: upper, lower, title, snake, kebab, dot, path, camel, pascal, mixed, or empty. Price: `5` credits. Parameters: `text`.
- `sort-lines` (action slug: `sort-lines`): Sort lines alphabetically in ascending or descending order. Price: `5` credits. Parameters: `order`, `text`.
- `spaces-to-tabs` (action slug: `spaces-to-tabs`): Convert leading spaces to tab characters. Price: `5` credits. Parameters: `tab_width`, `text`.
- `tabs-to-spaces` (action slug: `tabs-to-spaces`): Convert tab characters to spaces with configurable tab width. Price: `5` credits. Parameters: `tab_width`, `text`.
- `trim-whitespace` (action slug: `trim-whitespace`): Remove leading and trailing whitespace from each line and the overall text. Price: `5` credits. Parameters: `text`.
- `unwrap-text` (action slug: `unwrap-text`): Join all lines into a single line, removing line breaks. Price: `5` credits. Parameters: `text`.
- `wrap-text` (action slug: `wrap-text`): Wrap text to fit within a specified column width. Price: `5` credits. Parameters: `text`, `width`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "text-manipulation-and-converter"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "text-manipulation-and-converter"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "text-manipulation-and-converter"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "text-manipulation-and-converter"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "text-manipulation-and-converter"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "text-manipulation-and-converter"
  }
}
```

## Call This Tool
Product slug: `text-manipulation-and-converter`

Marketplace page: https://www.agentpmt.com/marketplace/text-manipulation-and-converter

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Text-Manipulation-and-Converter",
    "arguments": {
      "action": "add-quotes",
      "quote_type": "double",
      "text": "example text"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "text-manipulation-and-converter",
  "parameters": {
    "action": "add-quotes",
    "quote_type": "double",
    "text": "example text"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `add-quotes` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/text-manipulation-and-converter
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
