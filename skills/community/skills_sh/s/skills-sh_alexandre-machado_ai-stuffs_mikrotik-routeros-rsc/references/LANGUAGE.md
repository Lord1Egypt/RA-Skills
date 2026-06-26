# RouterOS Scripting – Language and Syntax

Concise reference based on the official manual (updated Jan 2026):
https://help.mikrotik.com/docs/spaces/ROS/pages/47579229/Scripting

## Concepts
- Logical line ends with `;` or `NEWLINE`; inside `()`, `[]`, `{}` `;` is not needed.
- Comment: starts with `#` until end of line; no multi-line comments.
- Line joining with `\` following rules (does not continue comment/token except string).
- Scopes: global (root) and local `{}`; avoid `:global` inside local scopes without external re-reference.
- Keywords: `and`, `or`, `in`. Delimiters: `() [] {} : ; $ /`.

## Types
- `num`, `bool`, `str`, `ip`, `ip-prefix`, `ip6`, `ip6-prefix`, `id`, `time`, `array`, `nil`.
- Conversions: `:tonum`, `:tostr`, `:toarray`, `:toip`, `:toid`, `:totime`, etc.

## Operators
- Arithmetic: `+ - * / %`. Use parentheses to avoid ambiguity with IP.
- Relational: `< > = <= >= !=`. Negation by `expr=false` or logical `!`.
- Logical: `! && || and or in`.
- Bitwise (IP/IPv6): `~ | ^ & << >>`. Docs state these work on both IP and IPv6 data types.
- Concatenation: `.` for strings, `,` for arrays. Interpolation with `$var`, `$()`, `$[]`.
- Others: `[]` command substitution, `()` grouping, `$` substitution, `~` POSIX regex.

## Variables
- `:global` and `:local` require declaration before use.
- Avoid reserved names (built-in menu properties). Prefer custom names.
- Case-sensitive; invalid names must be in quotes.

## Useful global commands
- `:onerror e in={ ... } do={ ... }` captures errors; `:retry` for retry logic.
- `:jobname` to limit execution to single instance.
- `:serialize`/`:deserialize` for JSON/DSV; `file-name` to generate file.
- `:time`, `:timestamp`, `:rndnum`, `:rndstr` utilities.

## Menu commands
- `add`, `remove`, `enable`, `disable`, `set`, `get`, `print`, `find`, `export`, `edit`.
- `print` parameters: `as-value`, `where`, `count-only`, `file`, `follow`, `interval`, etc.
- `import` (root): since 7.16.x supports `on-error=` parameter and `verbose=yes dry-run`. Wrap with `:onerror` for general error handling (see EXAMPLES.md).

## Control structures
- Loops: `:for`, `:foreach`, `:do { ... } while=()` and `:while do={}`.
- Conditional: `:if (cond) do={...} else={...}`.

## Functions
- No native functions; use `:global myFunc do={...}` or `:parse` to define and invoke; `:return` for return value.

## Arrays
- Non-alphanumeric keys must be in quotes; `:foreach k,v in={...}` to iterate.

