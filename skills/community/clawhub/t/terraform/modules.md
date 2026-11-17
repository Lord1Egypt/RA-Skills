# Modules — Design, Interfaces, and Versioning

A module is a contract with a version number. Every one you create is a thing to pin, upgrade, document, and eventually migrate away from — so the bar for creating one is higher than "these resources appear together".

## When A Module Earns Its Cost

Write one when it **encodes policy**: mandatory tags, encryption defaults, naming rules, a network topology your organization has decided on. Or when the same composition appears in three places and has already drifted between two of them.

Do not write one that renames another resource's arguments. That thin wrapper adds a version to pin, an indirection to trace, and an output to re-export by hand — in exchange for nothing.

## Interface Design

- Inputs typed, with `optional()` defaults (terraform >=1.3) instead of a `null` sentinel the module has to interpret.
- One object input per concern beats twenty flat variables — but an untyped `any` blob is worse than either; declare the object's shape.
- Outputs are the only thing callers can use. Every level of nesting re-exports by hand, which is why **two levels of nesting is the maximum** — level three means every new output is three PRs.
- `enable_*` booleans multiply: each one adds a `count = var.enabled ? 1 : 0` and a branch nobody tests. Past two or three, you have two modules pretending to be one.
- Mark outputs `sensitive` where the value is; a non-sensitive output derived from a sensitive input errors at plan.

## Providers Inside Modules

- A module used with `count`, `for_each`, or `depends_on` **cannot contain `provider` blocks**. Design modules provider-agnostic from the start; retrofitting this is a rewrite.
- The default (unaliased) provider is inherited automatically. Aliased providers must be passed explicitly:

```hcl
module "replica" {
  source    = "./modules/db"
  providers = { aws = aws.us_east_1 }
}
```

- A module that configures its own provider from its own variables looks convenient and makes the caller unable to control credentials, region, or retries.

## `depends_on` On A Module Call

`depends_on` at the module level makes every data source inside the module wait until apply. Their results become "known after apply", which cascades into permanently churning plans and unusable `for_each` keys. Pass the value you actually needed as an input — the dependency then exists in the graph for the right reason.

## Sources and Versioning

| Source | Form | Pin |
|---|---|---|
| Registry | `source = "org/name/aws"` | `version = "5.1.2"` — exact for third-party |
| Registry, internal | same | `version = "~> 1.2"` acceptable when your CI gates the module |
| Git | `source = "git::https://host/repo.git//modules/net?ref=v1.2.3"` | Tag only; `?ref=main` is an unpinned build |
| Local path | `source = "./modules/net"` | Unversioned by design — same-repo only |

- `//subdir` selects a directory inside a repo; the `?ref=` goes after it.
- The registry publishes from **tags**: the repo must be named `terraform-<provider>-<name>` and a release is a `vX.Y.Z` tag. Documentation is generated from your variable and output descriptions, so write them.
- Changing a module version is a code change with an infrastructure diff. Bump one module per PR and plan every environment.

## Upgrading A Module Safely

1. Read the module's CHANGELOG for renamed or removed inputs, and for **internal resource address changes**.
2. If the module renamed a resource internally and did not ship `moved` blocks, the upgrade is a destroy. Diff the module source before believing the version number.
3. Plan in the lowest environment; a well-behaved module upgrade is either zero-diff or a diff you can explain per line.
4. A module you author should ship its own `moved` blocks when addresses change — that is what makes it a library rather than a copy-paste.

## Composition Rules

- The **root** composes; modules take values, not other people's modules. A module that calls a third-party registry module drags that dependency into every consumer.
- A module must never read its own remote state, and should not read the caller's: pass values in.
- Modules used with `for_each` (terraform >=0.13) are the clean way to express "one of these per environment/region"; a module with an internal list of environments is not.
- Keep the module's blast radius aligned with the state's: a module that spans two blast radii forces them into one state.

## Testing And Documenting

- `.tftest.hcl` files live in the module repo and test the contract — given these inputs, these outputs and these resource attributes. Details in `testing.md` (routed from SKILL.md Quick Reference).
- Every variable and output gets a `description`. It is the module's only documentation on the registry page, and it is what the next reader diffs against behavior.
- An `examples/` directory that actually applies in a sandbox is the difference between a module people adopt and one they copy.

## Anti-Patterns Worth Naming

- **Mega-module**: one module, forty booleans, every consumer using a different subset. Split by resource lifecycle, not by cloud service.
- **Wrapper chain**: root → company module → team module → resource. Three versions to bump for one attribute.
- **Output tunnel**: a module that outputs its entire internal state so callers can reach inside. If callers need the internals, the boundary is wrong.
- **Provider-in-module with for_each**: fails at plan with a message about provider configurations, usually after the module is already adopted by four teams.
