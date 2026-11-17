# Static Typing — mypy, pyright, and Gradual Adoption

Type hints do nothing at runtime (`types.md`). Their value is entirely in the checker you run, which means the adoption strategy matters more than the annotations.

## Adopting Without A Rewrite

1. Turn the checker on in "do not fail" mode and count the errors. That number is the baseline, not the backlog.
2. Freeze the baseline in CI: new errors block, existing ones do not. Any tool that can diff error counts works; the discipline is what matters.
3. Ratchet per package, not per rule: pick the module with the most callers, set `disallow_untyped_defs` for it in the config, fix it, move on. A single global `strict = true` on a large codebase produces thousands of errors and gets reverted within a week.
4. Annotate boundaries first — public functions, dataclasses, and anything crossing a module edge. Local variables are inferred; annotating them is noise.
5. New code is typed from the start. That rule alone converts a codebase in a year.

```toml
[tool.mypy]
python_version = "3.11"
warn_unused_ignores = true       # deletes ignores that stopped being needed
warn_redundant_casts = true
warn_return_any = true

[[tool.mypy.overrides]]
module = "myapp.core.*"
disallow_untyped_defs = true     # the ratchet: one package at a time
```

## mypy vs pyright

- **mypy** is the reference implementation, has the deepest plugin ecosystem (`django-stubs`, `sqlalchemy`), and is what most libraries test against. Slower on large trees; use `dmypy run` (the daemon) for interactive speed.
- **pyright/Pylance** is faster, infers more aggressively, and is what VS Code users already have running — so it is the checker your team actually reads. Its strict mode is stricter than mypy's.
- They disagree in real ways (inference of empty containers, narrowing of `self`, third-party stub resolution). Pick one as the CI gate; running both means two sets of ignore comments and no owner. A second checker in editors only is fine.

## Ignores

- Always with the code: `# type: ignore[arg-type]`. A bare `# type: ignore` also silences the NEXT error introduced on that line, which is how bugs hide.
- `warn_unused_ignores = true` turns stale ignores into errors — the only mechanism that keeps them from accumulating forever.
- `cast(X, value)` asserts to the checker without runtime effect; use it when you know something the checker cannot see, and never as a shortcut for narrowing you could have written.
- An ignore on the same line for six months is a bug or a missing stub. Both deserve an issue, not a comment.

## The Annotations That Earn Their Keep

- **Parameters general, returns specific**: accept `Iterable[str]`, return `list[str]`. Accepting `list[str]` for a function that only iterates rejects tuples, generators, and dict keys for no reason.
- **Invariance**: `list[Dog]` is NOT a `list[Animal]`, because the callee could append a Cat. This is the "Argument of type list[Dog] cannot be assigned to list[Animal]" error, and the fix is `Sequence[Animal]` (covariant, read-only) in the signature.
- **`Protocol`** for duck-typed interfaces: `class Closeable(Protocol): def close(self) -> None: ...` types anything with that method without inheritance. ABCs are for when you also want shared implementation and `isinstance`. `@runtime_checkable` only checks method NAMES at runtime, never signatures.
- **`TypedDict`** for JSON-shaped dicts you cannot turn into classes; `NotRequired[...]` (`python >=3.11`) for optional keys. Zero runtime cost, unlike a model class.
- **`Literal`** for closed string sets (`mode: Literal["r", "w"]`) and **`Final`** for constants — both catch typos the tests will not.
- **`Self`** (`python >=3.11`) as the return type of builders and `__enter__`, so subclasses get the right type instead of the base.
- **`@override`** (`python >=3.12`) fails the check when a base method is renamed and your override silently becomes dead code.
- **`ParamSpec`** (`python >=3.10`) so a decorator preserves the wrapped signature instead of collapsing it to `(*args, **kwargs)` (`functions.md`).
- Generics: `def first[T](xs: Sequence[T]) -> T` (PEP 695, `python >=3.12`) or the `TypeVar` form below that floor.
- `Any` disables checking transitively everywhere the value flows; `object` forces a narrowing before use. When you mean "anything, and the caller must check", write `object` (`types.md`).

## Narrowing

- `if x is None: return` / `if not isinstance(x, str): raise` narrow the rest of the block — write the guard, not a `cast`.
- `assert x is not None` narrows too, but disappears under `python -O` (`security.md`); in library code raise instead.
- `match` statements narrow by pattern; `TypeGuard`/`TypeIs` annotate your own predicate functions so `if is_valid(x):` narrows for the checker.
- Narrowing does not survive a function call or a mutable attribute: `if self.x is not None:` is invalidated by anything the checker cannot prove is pure. Bind to a local first.

## Third-Party Types

- Missing stubs: install them (`types-requests`, `types-PyYAML`) rather than blanket-ignoring the import. `--ignore-missing-imports` globally is a baseline setting, not a permanent one.
- Shipping your own types: a `py.typed` marker file in the package (declared in the build config) is what makes your annotations visible to consumers. Without it, every user of your library sees `Any`.
- `from __future__ import annotations` makes annotations strings, which breaks libraries that read them at runtime (older pydantic, some dataclass tooling) and helps with forward references and import cycles (`imports.md`). PEP 649 in `python >=3.14` makes annotations lazy natively, retiring the trade-off.
- Runtime validation is a separate job: a checker cannot verify JSON off the network. Validate at the boundary with pydantic or attrs, then trust the types inside (`data-modeling.md`).
