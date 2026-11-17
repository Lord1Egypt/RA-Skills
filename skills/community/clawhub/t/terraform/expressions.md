# HCL Expressions — Loops, Types, and the Functions That Matter

Most "Terraform is weird" moments are HCL evaluation rules, not infrastructure. This is the subset that decides whether a plan works.

- Building a list, map, or a `for_each` set → `for` Expressions · Nested Loops · Collection Gotchas
- Repeating a nested block (ingress rules, tags) → `dynamic` Blocks
- Typing inputs and failing bad values early → Types and Validation
- "Which function do I want here?" → Functions Worth Knowing
- A diff that never goes away, or a value unknown at plan → Values That Change Every Run · Locals and Known-ness
- A masked value spreading through outputs → Sensitivity Propagation
- "Why is my variable not being applied?" → Variable Value Precedence

## `for` Expressions

```hcl
[for s in var.subnets : s.cidr]                       # list
{for k, v in var.envs : k => upper(v)}                # map
[for s in var.subnets : s.cidr if s.public]           # filter
{for u in var.users : u.team => u.name...}            # grouping mode: values collected per key
```

- Brackets choose the output type: `[...]` list, `{...}` map. A map comprehension with duplicate keys errors unless you use grouping mode (`...`).
- Iterating a map yields `k, v`; iterating a list yields the element, and `for i, v in list` yields index and value.

## Nested Loops

`setproduct` + a keyed map is the canonical cross-product for `for_each` — nested `for` alone cannot produce a flat map:

```hcl
locals {
  rules = {
    for pair in setproduct(keys(var.subnets), var.ports) :
    "${pair[0]}-${pair[1]}" => { subnet = pair[0], port = pair[1] }
  }
}
resource "aws_security_group_rule" "this" {
  for_each = local.rules
  # ...
}
```

`flatten()` does the same job when the shape is a list of lists produced by nested `for`. The composite key must be stable and human-readable — it is the resource's identity forever (SKILL.md Core Rules 5).

## `dynamic` Blocks

```hcl
dynamic "ingress" {
  for_each = var.ports
  content {
    from_port = ingress.value
    to_port   = ingress.value
  }
}
```

- Only for repeated **nested blocks** whose number is dynamic. Cannot generate meta-arguments (`lifecycle`, `provider`, `depends_on`) or top-level blocks.
- `iterator = port` renames the iterator when nesting two dynamics would otherwise shadow.
- A `dynamic` over a hardcoded list is strictly harder to read than writing the blocks out. Use it when the count comes from a variable, not to look clever.

## Types and Validation

- Always declare `type`. An undeclared variable is `type = any`, and type errors then surface deep inside an expression instead of at the input.
- Object types with defaults (terraform >=1.3):

```hcl
variable "cluster" {
  type = object({
    name     = string
    replicas = optional(number, 3)
    tags     = optional(map(string), {})
  })
  nullable = false
}
```

- `validation` blocks fail at plan with your message — the cheapest gate in the whole toolchain. Since terraform >=1.9 a validation condition may reference other variables; before that it could only reference itself.
- `precondition` / `postcondition` inside `lifecycle` (terraform >=1.2) assert facts across resources. A `postcondition` on a data source catches a wrong lookup at the source instead of ten resources downstream.
- `check` blocks (terraform >=1.5) report a failure as a warning without blocking the apply — the right tool for "this should be true but must not stop a deploy".

```hcl
variable "env" {
  type = string
  validation {
    condition     = contains(["dev", "stage", "prod"], var.env)
    error_message = "env must be dev, stage, or prod."
  }
}
```

## Functions Worth Knowing

| Need | Function | Trap |
|---|---|---|
| Optional attribute that may not exist | `try(x.a, "default")` | `try` swallows *any* error, including typos — keep the expression tiny |
| Test without a value | `can(x.a)` | Returns bool; same swallowing risk |
| First non-null | `coalesce(a, b, c)` | Errors if all are null; `coalesce` treats `""` as a value, not as empty |
| Map lookup with default | `lookup(m, k, default)` | Prefer `m[k]` when the key must exist — you want the error |
| The count 0-or-1 idiom | `one(aws_x.y[*].id)` | Returns null when empty; errors on more than one |
| Flatten nested lists | `flatten()` | Only one level of nesting per call is intuitive; check with `terraform console` |
| Cross product | `setproduct()` | Returns a list of tuples, index with `[0]`/`[1]` |
| Render a template file | `templatefile(path, vars)` | The legacy `template_file` data source needs a provider; this does not |
| Emit JSON | `jsonencode(obj)` | Beats a heredoc for policy documents: correct escaping and it fails on bad structure |
| Subnet math | `cidrsubnet(prefix, newbits, netnum)` | `newbits` is added to the prefix length, not the resulting length |
| Strip sensitivity | `nonsensitive(x)` | Only when the value genuinely is not a secret |

## Values That Change Every Run

`timestamp()` and `uuid()` return a new value on every evaluation, so any attribute holding them shows a diff forever. Use a `random_*` resource with `keepers` instead — it regenerates only when a keeper changes and stores the result in state:

```hcl
resource "random_id" "suffix" {
  keepers = { env = var.env }
  byte_length = 4
}
```

The same reasoning applies to `filemd5()` on a file your build regenerates: it is a *deliberate* trigger, which is fine, or an accidental one, which is a permanent diff (`debug.md`).

## Locals and Known-ness

- `locals` cannot be self-referential and cannot take `depends_on`.
- A local that references a resource attribute is unknown at plan exactly like the attribute is; wrapping something in a local never makes it known.
- Splitting a big expression into locals is free at runtime and the single best readability move in a large module.

## Sensitivity Propagation

- Sensitivity is contagious: merge one sensitive value into a map and the whole map is sensitive.
- A sensitive value cannot be a `for_each` key, and a non-sensitive `output` derived from a sensitive value errors at plan. Both are the system working.
- `nonsensitive()` exists for the case where the sensitivity was inherited rather than real. Reaching for it on an actual secret puts the value in plan output (`secrets.md`).

## Collection Gotchas

- `toset()` deduplicates and drops order; `for_each` over a set uses each element as its own key, so a set of objects is invalid — build a map.
- `element(list, i)` wraps around modulo the length; `list[i]` errors past the end. Wrapping silently returns the wrong element, which is a wrong resource, not an error.
- Sets have no index: you cannot `[0]` a set. Convert with `tolist()` — and accept that the order is the provider's, not yours.
- String templates support `%{ if }` and `%{ for }`; the `~` marker (`%{~ if }`) trims surrounding whitespace, which is what makes generated config files readable.
- `terraform console` evaluates any of this against real state in a second. Use it before writing a plan-based experiment.

## Variable Value Precedence

"My variable is not being applied" is almost always a higher-precedence source you forgot. Last one wins, lowest first:

1. The `default` in the `variable` block.
2. `TF_VAR_<name>` environment variables — invisible in the repo, and the usual culprit in CI (case-sensitive, exact variable name).
3. `terraform.tfvars`, then `terraform.tfvars.json` — auto-loaded from the working directory, never named on the command line.
4. `*.auto.tfvars` and `*.auto.tfvars.json` — auto-loaded too, applied in **alphabetical** filename order, so `10-base.auto.tfvars` loses to `20-prod.auto.tfvars`.
5. `-var` and `-var-file` on the command line, applied in the order written: the last `-var 'region=eu-west-1'` beats every file, including one passed by an earlier `-var-file`.

- Auto-loading is per working directory. A `terraform.tfvars` one directory up is not read — the file next to the root module is, which is why a `dir-per-env` layout works at all.
- Complex-typed variables (`map`, `object`) are replaced wholesale by the winning source, never merged key by key.
- A saved plan freezes the resolved values: `apply tfplan` ignores `-var` entirely and re-passing one errors. Change a variable, re-plan.
- A value for a variable that is not declared is only a warning from an auto-loaded file ("Value for undeclared variable") but an error from `-var`/`-var-file`. A silently ignored setting means a typo in the name, not a precedence problem.
