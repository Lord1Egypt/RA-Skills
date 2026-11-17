# Documentation

Use when a change alters setup, configuration, commands, an API, user-visible behavior or an operational procedure, or when asked to write a README, guide or changelog.

## Keep docs matching behavior

Update the affected documentation in the same change as the behavior. Correct or delete text that is no longer true; wrong documentation is worse than none because readers trust it. Run the documented commands the change affects in a safe place, such as a sandbox, a test project or a dry run, and ask before running any that delete data, change production or have external effects, unless the request already covers them. Keep real secrets out of examples, and date statements that will go stale.

| Change | Update |
|---|---|
| Configuration option | Its default, an example and where it is set |
| Endpoint, event or CLI flag | The contract file or generated reference, and the changelog |
| Dependency or setup step | Prerequisites and quick start in the README |
| User-visible change in a release | Changelog and release notes |
| New alert or operational procedure | The runbook or the alert's own note |

Generate reference material from its source of truth, such as an OpenAPI file, the CLI's help or a configuration schema, where the tooling allows, so that it cannot drift. Give each page one purpose: a tutorial teaches, a how-to guide completes a task, a reference states facts and an explanation gives reasons.

## What a README needs

What the project does and for whom, prerequisites with versions, copyable commands to install, configure, run and test it, where configuration lives, how to get help or contribute, and the license.

## What a changelog needs

Entries grouped by version and date, newest first, under headings such as Added, Changed, Deprecated, Removed, Fixed and Security. Write them for users rather than copying commit messages, call out breaking changes, and follow the project's versioning rule, such as Semantic Versioning.

## Sources

- [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
- [Semantic Versioning](https://semver.org/)
- [Diátaxis documentation framework](https://diataxis.fr/)
- [Write the Docs: docs as code](https://www.writethedocs.org/guide/docs-as-code/)
