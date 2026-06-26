# Stable Internal API

Primary docs:

- WP-CLI Internal API reference: <https://make.wordpress.org/cli/handbook/references/internal-api/>

Use this file as the grouped map of the stable methods that WP-CLI documents publicly.

## Registration And Hooks

Common stable entrypoints:

- `WP_CLI::add_command()`
- `WP_CLI::add_hook()`
- `WP_CLI::do_hook()`

Use these for:

- registering command namespaces and subcommands
- inserting lifecycle hooks
- responding to WP-CLI events without patching core internals

## Output And Logging

Common stable helpers:

- `WP_CLI::log()`
- `WP_CLI::line()`
- `WP_CLI::success()`
- `WP_CLI::warning()`
- `WP_CLI::error()`
- `WP_CLI::halt()`
- `WP_CLI::debug()`

Use these instead of ad hoc `echo` plus manual exit handling.

## Command Execution

Common stable helpers:

- `WP_CLI::runcommand()`
- `WP_CLI::launch()`
- `WP_CLI::launch_self()`

Use these when command code needs to trigger other WP-CLI behavior or external processes.

## Input And Runtime Helpers

Common stable helpers:

- `WP_CLI::confirm()`
- `WP_CLI::get_config()`
- `WP_CLI::get_runner()`

Use `confirm()` before destructive actions and use runtime config helpers instead of guessing bootstrap state.

## Utility Namespace

Common helpers under `WP_CLI\Utils`:

- `format_items()`
- `get_flag_value()`
- `assoc_args_to_str()`
- `parse_str_to_argv()`
- `make_progress_bar()`

For tabular or machine-readable output, `format_items()` is the default workhorse.

## Practical Rule

If you can solve the command with the stable methods above, do that first. Avoid coupling a ClawHub-facing skill to undocumented WP-CLI internals that can drift across releases.
