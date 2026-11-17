---
name: rez-package-orderers
description: "How rez decides which version of a package to pick — the `package_orderers` setting, the five built-in orderers `sorted` / `version_split` / `per_family` / `soft_timestamp` / `no_order`, how orderers apply to variants as well as packages, writing and registering a custom orderer, and how to prove an orderer is or is not what changed your resolve. Use when rez picks a version you did not expect and the resolve is not failing, or when a studio needs python-2-style version pinning to survive an upgrade. Covers Rez 3.4.0."
---

# Rez package orderers

> **One-sentence summary**: an orderer reorders the version list rez sorts before it solves, so the
> "latest" version rez returns is the latest *by the orderer's rule* — and a configured orderer is
> the only reason a successful resolve picks an older version without any conflict to explain it.

Skill scope: **the orderer mechanism itself** — which orderers exist, how they are configured, and
how to tell whether one is in play. For how version *tokens* compare (`1.0.0` vs `1.0.0-beta`,
alphanumeric vs numeric segments) see `rez-core-concepts`; for a resolve that **fails** see
`rez-resolve-troubleshooting`, since orderers only matter when the resolve succeeds; for reading the
solver trace see `rez-resolve`.

## What an orderer changes

The solver always asks the package repository for versions in a defined order and takes the first
that fits. Orderers change **that order**. They do not forbid anything: a higher version is still
reachable if you request it explicitly.

That is the diagnostic signature. If `rez-env foo` gives you `1.1.0` while `rez-env foo-2` happily
gives you `2.0.0`, and there is no conflict anywhere, an orderer is almost always why.

Orderers apply to **variants** as well as to package versions, so a variant list is reordered the
same way.

## Is an orderer in play?

Check before you theorise — the default is empty:

```bash
rez-config package_orderers
```

An empty list means no orderer is configured and the default (`sorted`, descending) applies. A
non-empty list is inherited through the normal config layering, so also confirm where it came from:

```bash
rez-config --source-list package_orderers
```

## The built-in orderers

| `type` | What it does |
|---|---|
| `sorted` | the default — sort by version, descending |
| `version_split` | versions less than or equal to `first_version` first, then the default order |
| `per_family` | apply different orderers to different package families |
| `soft_timestamp` | versions released before `timestamp` first, then the rest; `rank` relaxes it |
| `no_order` | a no-op — explicitly leave a package's order alone |

### sorted

The default. You only need to name it to change its direction, or to scope it:

```python
package_orderers = [
    {
        "type": "sorted",        # required
        "descending": True,      # required
        "packages": ["python"],  # optional; omit to apply to every package
    }
]
```

`descending: False` inverts it, so the lowest version wins. Verified against a repository holding
`foo-1.0.0`, `foo-1.1.0`, `foo-2.0.0`:

| Orderer | `rez-env foo` resolves |
|---|---|
| none (default) | `foo-2.0.0` |
| `sorted` with `descending: False` | `foo-1.0.0` |

### version_split

Orders every version **less than or equal to** `first_version` first, then falls back to the default
order for the rest. Given `[5, 4, 3, 2, 1]`, an orderer with `first_version=3` yields
`[3, 2, 1, 5, 4]`.

```python
package_orderers = [
    {
        "type": "version_split",
        "first_version": "1.1.0",
    }
]
```

With the same three `foo` versions, `first_version: "1.1.0"` makes `rez-env foo` resolve
`foo-1.1.0` instead of `foo-2.0.0`. Note the comparison is *less than or equal to*, so the named
version itself is included in the preferred group.

The canonical studio use is easing a python-2 to python-3 migration:

```python
package_orderers = [
    {
        "type": "per_family",
        "orderers": [
            {
                "packages": ["python"],
                "type": "version_split",
                "first_version": "2.7.16",
            }
        ],
    }
]
```

For the `python` family, versions at or below `2.7.16` win. An explicit `rez-env python-3` still
gets `3.7.4`.

### per_family

Applies different orderers to different families. Any orderer above can be nested in it, together
with a `packages` list. A family not named by any nested orderer keeps the default order.

This is also how you scope `no_order`.

### soft_timestamp

Prefers packages released before `timestamp` (a Unix epoch integer), in descending order, followed by
everything released after. `rank` relaxes the boundary: a non-zero rank lets version changes at that
rank and above win over the timestamp.

```python
package_orderers = [
    {
        "type": "soft_timestamp",
        "timestamp": 1568001600,  # 2019-09-09
        "rank": 3,
    }
]
```

`rank: 3` is the usual choice under semantic versioning — it allows a different **patch** number
through. Generate the timestamp rather than hand-computing it:

```bash
python -c "import datetime, time; print(int(time.mktime(datetime.date(2019, 9, 9).timetuple())))"
```

Which version wins depends on `rank`, and the effect is not monotonic — a rank that lets a later
patch through can land on a different version than a rank that lets a later minor through. Measure
it against your own repository rather than assuming, because the answer depends on when each version
was actually released.

### no_order

A no-op. It exists so that inside a `per_family` block you can apply an orderer broadly but exempt
one package:

```python
package_orderers = [
    {
        "type": "per_family",
        "orderers": [
            {"packages": ["foo"], "type": "no_order"},
        ],
    }
]
```

## Custom orderers

Subclass `PackageOrder`, implement the mandatory methods, and register it with `register_orderer`.
Everything except `sort_key_implementation` is boilerplate you must supply for serialization:

```python
# rezconfig.py
from rez.package_order import PackageOrder, register_orderer


class MyOrderer(PackageOrder):
    name = "my_orderer"

    def __init__(self, custom_arg, **kwargs):
        super().__init__(**kwargs)
        self.custom_arg = custom_arg

    def sort_key_implementation(self, package_name, version):
        ...

    def __str__(self):
        ...

    def __eq__(self, other):
        ...

    def to_pod(self, other):
        ...

    @classmethod
    def from_pod(cls, data):
        ...


register_orderer(MyOrderer)

package_orderers = [
    {
        "type": "my_orderer",
        "custom_arg": "value here",
    }
]
```

`rezconfig.py` is ordinary Python, so the class is defined and registered at config load time.

> **Do not pass `self` to `super().__init__()`** — `super().__init__(self, **kwargs)` raises
> `TypeError: 'MyOrderer' object is not iterable`, because `self` lands in the `packages` argument
> that the base class sorts. The upstream `package_orderers.rst` at 3.4.0 shows the broken form in
> its custom-orderer example; the correct call is `super().__init__(**kwargs)`.

Upstream explicitly warns against this: a custom orderer makes environments behave in ways users do
not expect, and makes the affected packages harder to share. Prefer a built-in, and prefer
`version_split` over anything bespoke.

## Verifying what an orderer did

Never infer the effect from one command — compare the resolve against the version list.

```bash
rez-search foo                    # every version, as the repository holds them
rez-env foo -o context.rxt        # what the solver actually picked
rez-context --so                  # the resolved version, with the request that produced it
```

If `rez-context --so` shows the version you did not expect, and `rez-search` shows a newer one
exists, the orderer is the explanation. Confirm by repeating the resolve with the setting emptied —
`package_orderers` is a normal config key, so a temporary override is enough to prove it.

## Troubleshooting

| Symptom | Cause |
|---|---|
| An older version wins with no conflict | an orderer reordered the version list |
| `rez-env foo` and `rez-env foo-2` disagree | working as intended — orderers do not forbid explicit requests |
| `no_order` seems to do nothing | that is what it does; it only matters inside `per_family` |
| An unknown `type` is rejected at resolve time | only `sorted`, `version_split`, `per_family`, `soft_timestamp`, `no_order` and registered custom names are accepted |
| The orderer applies to packages I did not name | omit `packages` (outside `per_family`) and it applies to everything |
| A variant is chosen oddly | orderers apply to variants too, not just versions |
| `soft_timestamp` picks a surprising version | `rank` decides how far past the timestamp a version may drift; check it |

## Agent workflow

1. Read `rez-config package_orderers` first — an empty list means orderers are not your problem.
2. Find where a non-empty value comes from with `rez-config --source-list package_orderers`.
3. Distinguish "the version list is ordered unexpectedly" (`rez-search`) from "the solve failed" —
   the latter is `rez-resolve-troubleshooting`, not this skill.
4. Prefer `version_split` and `per_family` over a custom orderer; scope with `packages`.
5. Verify by resolving and inspecting with `rez-context --so`, then repeat with the orderer removed
   to prove it is the cause.
