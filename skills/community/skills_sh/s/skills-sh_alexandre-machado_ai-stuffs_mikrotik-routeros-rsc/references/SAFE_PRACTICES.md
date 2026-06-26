# Best Practices: Security and Idempotency

Primary sources:
- Scripting Manual (Jan 2026): https://help.mikrotik.com/docs/spaces/ROS/pages/47579229/Scripting
- Scripting Tips & Tricks: https://help.mikrotik.com/docs/spaces/ROS/pages/283574370/Scripting+Tips+and+Tricks

## Idempotency
- Before `add`/`set`, verify with `find where ...` and conditional `:if`.
- Use `print as-value` and arrays to compare states.
- Avoid depending on `numbers`; select by `name`, `address`, `comment`, etc.

## Permissions
- Scripts inherit permissions from user/scheduler depending on execution.
- `use-script-permissions` only works when script permissions are sufficient.
- Don't grant unnecessary policies in `/system script add policy=...`.
  The linter flags anything beyond `read,write,test`.
- **Scheduler and Netwatch** only accept `read,write,test,reboot` as policies.
  Assigning other policies (e.g. `ftp`, `policy`) to a scheduler `on-event` script
  has no effect — the scheduler cannot escalate beyond its own set.
- **`/system scheduler` valid properties** (RouterOS v7): `name`, `on-event`,
  `interval`, `start-date`, `start-time` (accepts `startup` for boot-time
  execution), `policy`, `comment`, `disabled`. There is **no** `start-delay`,
  `delay`, `boot-delay`, or `run-after` — importing a scheduler entry with one
  of those fails with `expected end of command`. To delay the first run after
  boot, either set `start-time` to an absolute clock time, or make the
  scheduled script itself resilient to "not yet ready" state (e.g. exit early
  if DHCP isn't bound) instead of trying to delay the scheduler.
- **`dont-require-permissions=yes`** lets a script bypass the caller's policy
  restrictions entirely. The official Tips & Tricks page documents this as a
  security risk. Avoid it unless you have an explicit, audited reason.

## Robustness
- `:onerror` to capture failures; combine with `:retry` for controlled retries.
- Limit multiple instances with `:jobname`.
- Avoid `:delay` in loops without limits; use `Scheduler` for periodic tasks.

## Security
- Don't automate destructive commands (`system reset-configuration`, formatting, wipe).
- Avoid accidental exfiltration (`/export hide-sensitive=no` in sensitive environments).
- Handle secrets carefully; don't log passwords in `:log`.
- Validate inputs before `fetch` and similar operations.
- **Built-in variable name collisions**: RouterOS pre-defines variables like
  `$nothing`, `$true`, `$false`. Re-declaring them with `:local` or `:global`
  shadows the built-in silently and causes hard-to-debug behaviour.
- **`:global` re-declaration inside functions**: calling `:global myVar value`
  inside a function body resets the global every time the function runs. If the
  intent is to *read* an existing global, declare with `:global myVar` (no
  value) to bind without overwriting.
- **`:set` inside nested `do={...}` blocks does NOT modify outer globals by
  default.** In RouterOS v7, every `do={...}` (including the body of `:if/else`,
  `:foreach`, `/system script source={...}`) is a closure with its own scope.
  Even if you declared `:global myVar` at the top of the script, a
  `:set myVar $x` inside a nested `else={...}` creates a fresh local in that
  inner scope and the global is never updated — so the next run reads the
  still-empty global and the comparison fails silently. Re-declare
  `:global myVar` (no value, just to bind) at the top of every inner
  `do={...}` block that needs to mutate it.

## Type coercion
- RouterOS is weakly typed. Comparing a `str` to a `num` may succeed silently
  with unexpected results (e.g. `"5" > 3` is `true` but `"abc" > 3` is also
  `true` because the string sorts lexically higher).
- Use `:tonum`, `:tostr`, `:toip`, etc. explicitly before comparisons to avoid
  silent type coercion bugs. The `:typeof` command can verify a value's type at
  runtime.

## Style
- Parameterize with `:local` at top; add `:global` only when needed.
- Short and objective comments; no large blocks.
- Use `where` and clear expressions; consistent alignment.
