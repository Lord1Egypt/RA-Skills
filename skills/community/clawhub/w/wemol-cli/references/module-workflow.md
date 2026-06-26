# Module Workflow

Use the module workflow to discover what can be run before submitting jobs.

## Start With Command Guidance

```bash
wemol-cli module --help
wemol-cli module --doc
```

## Search

Search by keywords:

```bash
wemol-cli module search antibody design
```

This is the normal entry point when the user describes a capability instead of giving a module ID.

Current behavior:
- search results contain enabled modules only
- query is positional (`module search <query...>`), not `--query`

## List

Browse and filter:

```bash
wemol-cli module list
wemol-cli module list --name antibody --limit 20
wemol-cli module list --all
```

Current behavior:
- list returns enabled modules only
- legacy `--status` filtering is not supported on `module list`

## Inspect One Module

```bash
wemol-cli module get 451
```

This prints:
- module documentation
- a method summary at the end

The document body follows the current CLI language.
`module get` uses positional ID (`module get <id>`), not legacy `--id/--code` flags.

## Inspect Parameters

Fetch structured parameter schemas:

```bash
wemol-cli module get 451 --params-json
```

For one method only:

```bash
wemol-cli module get 451 --params-json --method run
```

Use this instead of guessing input fields.

## Agent Guidance

- Read the method list before choosing a method.
- Use `module_id` from prior outputs when available.
- Prefer `--params-json` whenever the next step is job submission or parameter analysis.
- Build `job submit --params` keys from exact `field` values in `--params-json`.
