# Class Traps

Choosing between a class, a dataclass, a NamedTuple, and a validated model is a separate decision: `data-modeling.md`. This file is the mechanics once you have a class.

## Shared state
- `class A: items = []` — one list shared by every instance; `a.items.append(x)` shows up on `b.items`. Mutable state belongs in `__init__`. Reading `self.items` finds the class attribute until the first instance assignment shadows it — which is why the bug appears only on mutation, not assignment.
- Dataclasses raise at class creation for `field: list = []` — but only for list/dict/set. A mutable default of any OTHER type (custom class instance) passes silently and is shared. Always `field(default_factory=...)` for anything mutable.
- The class body runs at IMPORT time: a database call, a file read, or a heavy computation there taxes every consumer of the module and cannot be caught by the caller (`imports.md`).

## Equality and hashing
- Defining `__eq__` sets `__hash__ = None` — instances become unhashable, breaking sets and dict keys. Define `__hash__` over the same fields `__eq__` compares, or the object misbehaves in hash containers.
- Same rule inside `@dataclass`: `eq=True` (the default) kills hashing unless `frozen=True` (auto-hash) or explicit `unsafe_hash=True`. A dataclass that stops working in a set after adding fields usually lost frozen.
- Hash and equality must agree, and both must be stable while the object is in a container: mutating a field that `__hash__` reads makes the object unfindable in the set that holds it (`collections.md`).
- Ordering: implement `__lt__` and add `functools.total_ordering` rather than writing all six comparisons — three of the six are usually inconsistent when hand-written.

## Construction and inheritance
- `__init__` initializes an EXISTING instance and must return None; `__new__` creates the instance. Subclassing immutables (tuple, str, int) requires overriding `__new__` — by `__init__` time the value is already fixed.
- `super()` follows the MRO of the RUNTIME class, not "my parent". In multiple inheritance, every class in the diamond must call `super().__init__(**kwargs)` and pass through unknown kwargs, or the chain silently stops at the first non-cooperative class.
- `type(x) == T` rejects subclasses; `isinstance(x, T)` is the default. The exception: when subclass substitution is exactly the bug you are guarding against (e.g., bool passing an int check).
- `@classmethod` for alternative constructors (`Config.from_file(path)`) — it receives the subclass, so subclasses get correctly-typed instances for free. `@staticmethod` usually signals a plain module-level function that got adopted by a class.
- Prefer composition when the only thing inheritance buys is code reuse; inherit when callers must be able to substitute the subclass. Structural interfaces without inheritance: `Protocol` (`type-checking.md`).

## Attribute machinery
- `hasattr`/`getattr(x, 'attr', default)` swallow only AttributeError — but a BUG inside a `@property` getter that raises AttributeError (a typo'd self-attribute) looks identical to "attribute missing". Symptom: property "disappears". Debug by calling the property directly.
- `@property` setter requires the getter defined first under the same name (`@x.setter` needs `@property def x` above it) — wrong order is a NameError at class-body execution.
- `__getattr__` runs ONLY when normal lookup fails; `__getattribute__` runs on every access and is where infinite recursion lives (`self.x` inside it calls itself — use `object.__getattribute__`). Reach for `__getattr__` for proxies and lazy attributes, never for validation.
- `__slots__` removes `__dict__`: no ad-hoc attributes, and `functools.cached_property` breaks (it stores into `__dict__`). Every class in the hierarchy must declare `__slots__` or instances get a dict anyway and the memory saving silently vanishes.
- `__x` name-mangles to `_ClassName__x` — its purpose is avoiding subclass name collisions, not privacy. It also breaks `getattr(self, '__x')` and pickling of the raw name; prefer single underscore unless collision is the actual concern.
- `__init_subclass__` and `__set_name__` (`python >=3.6`) cover most registration/validation use cases that used to require a metaclass — reach for a metaclass only when you must change class CREATION itself.

## Lifecycle and representation
- `__del__` is not a destructor: it runs when the last reference disappears, at an unpredictable time, possibly never at interpreter shutdown, and exceptions inside it are printed and swallowed. Resource cleanup belongs in a context manager (SKILL.md rule 6).
- Write `__repr__` for every class you will ever debug: unambiguous, ideally reconstructible (`Order(id=12, total=Decimal('9.99'))`). `__str__` falls back to `__repr__`, so one method covers both. Keep secrets out of it — reprs land in logs and tracebacks (`security.md`).
- `copy.deepcopy` and `pickle` use `__reduce__`/`__getstate__`/`__setstate__`. A class holding a socket, a file handle, or a lock is not copyable or picklable — which surfaces as an obscure error the first time it crosses a process boundary (`concurrency.md`).
