# Command Patterns

Use this file when writing or reviewing custom command classes.

## Minimal Pattern

Recommended structure:

1. register the command with `WP_CLI::add_command()`
2. accept `$args` and `$assoc_args`
3. validate inputs early
4. call business logic
5. format output with `WP_CLI\Utils\format_items()` or explicit success or error helpers

## Output Rules

Default mapping:

- `log()` for progress
- `line()` for plain output lines
- `success()` for completion
- `warning()` for recoverable issues
- `error()` for fatal stops

Avoid mixing raw `echo` with these helpers unless you have a specific reason.

## Formatting Rules

For lists:

- accept a `--format=<format>` assoc arg
- default to `table`
- support `json` when the output may be consumed by automation

This is the common place to use `WP_CLI\Utils\get_flag_value()` and `WP_CLI\Utils\format_items()`.

## Destructive Actions

For deletes, resets, or bulk updates:

- call `WP_CLI::confirm()` unless the command explicitly supports a `--yes` bypass pattern
- print the scope of the action before running it

## Composing Commands

If a command needs another WP-CLI command:

- prefer `WP_CLI::runcommand()` when you want WP-CLI semantics
- prefer `WP_CLI::launch_self()` when you want a new WP-CLI process with inherited config
- avoid shelling out to `wp` manually unless there is no better supported option
