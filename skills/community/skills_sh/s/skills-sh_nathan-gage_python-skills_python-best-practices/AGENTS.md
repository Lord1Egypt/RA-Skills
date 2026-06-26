# Python Best Practices

**Version 1.3.0**
Python Best Practices
April 2026

> **Note:**
> This document is optimized for AI agents and LLMs that maintain, generate,
> or refactor Python codebases. Humans may also find it useful, but the
> guidance, examples, and framing prioritize consistency and pattern-matching
> for AI-assisted workflows.

---

## Abstract

Python software engineering guidelines for agent consumption. 70 rules across 8 categories, prioritized by impact from data modeling and error handling down to naming and import hygiene. Each rule is observational — it describes the pattern and what it costs, shows incorrect and correct code, and cites primary sources where the rule depends on language or library behavior. Rules assume Python 3.11+ as a baseline; rules depending on a higher version (e.g., 3.13 for warnings.deprecated) are called out inline. A rule match is a signal, not a verdict: most rules are design preferences for new code rather than bugs to fix across the repo.

---

## Table of Contents

1. [Data Modeling](#1-data-modeling) — **HIGH**
   - 1.1 [Brand Primitive IDs With NewType](#11-brand-primitive-ids-with-newtype)
   - 1.2 [Create Explicit Variants Instead of Mode Flags](#12-create-explicit-variants-instead-of-mode-flags)
   - 1.3 [Delete Dead Variants](#13-delete-dead-variants)
   - 1.4 [Derive, Don't Store](#14-derive-dont-store)
   - 1.5 [Encapsulate Mutable State in the Narrowest Clear Scope](#15-encapsulate-mutable-state-in-the-narrowest-clear-scope)
   - 1.6 [Never Use Mutable Default Arguments](#16-never-use-mutable-default-arguments)
   - 1.7 [Phase Related Optional Fields Into Nested Structs](#17-phase-related-optional-fields-into-nested-structs)
   - 1.8 [Pick a Mutation Contract](#18-pick-a-mutation-contract)
   - 1.9 [Use Discriminated Unions Over Optional Bags](#19-use-discriminated-unions-over-optional-bags)
   - 1.10 [Use Timezone-Aware Datetimes at Boundaries](#110-use-timezone-aware-datetimes-at-boundaries)
   - 1.11 [Use a Sentinel Object When None Is a Real Domain Value](#111-use-a-sentinel-object-when-none-is-a-real-domain-value)
2. [Error Handling](#2-error-handling) — **MEDIUM-HIGH**
   - 2.1 [Catch Specific Exception Types](#21-catch-specific-exception-types)
   - 2.2 [Consolidate try/except Blocks with the Same Handler](#22-consolidate-tryexcept-blocks-with-the-same-handler)
   - 2.3 [Inherit New Exceptions from Existing Base Exceptions](#23-inherit-new-exceptions-from-existing-base-exceptions)
   - 2.4 [Preserve Tracebacks When Logging Exceptions](#24-preserve-tracebacks-when-logging-exceptions)
   - 2.5 [Trust Validated State Within the Same Trust Domain](#25-trust-validated-state-within-the-same-trust-domain)
   - 2.6 [Use !r Format for Identifiers in Error Messages](#26-use-r-format-for-identifiers-in-error-messages)
   - 2.7 [Use assert Only for Debug-Only Internal Invariants](#27-use-assert-only-for-debug-only-internal-invariants)
   - 2.8 [Use assert_never for Exhaustiveness Checks](#28-use-assertnever-for-exhaustiveness-checks)
   - 2.9 [Use raise ... from to Preserve Exception Causality](#29-use-raise-from-to-preserve-exception-causality)
   - 2.10 [Use with / async with for Resource Lifetimes](#210-use-with-async-with-for-resource-lifetimes)
   - 2.11 [Validate Input at System Boundaries](#211-validate-input-at-system-boundaries)
3. [Type Safety](#3-type-safety) — **MEDIUM-HIGH**
   - 3.1 [Avoid Any Annotations](#31-avoid-any-annotations)
   - 3.2 [Fix Type Definitions Instead of cast()](#32-fix-type-definitions-instead-of-cast)
   - 3.3 [Fix Type Errors, Don't Ignore Them](#33-fix-type-errors-dont-ignore-them)
   - 3.4 [Narrow Type Signatures to Runtime Reality](#34-narrow-type-signatures-to-runtime-reality)
   - 3.5 [Remove Redundant `| None` When Values Are Guaranteed](#35-remove-redundant-none-when-values-are-guaranteed)
   - 3.6 [Trust the Type Checker — Remove Redundant Runtime Checks](#36-trust-the-type-checker-remove-redundant-runtime-checks)
   - 3.7 [Use Literal Types for Fixed String Sets](#37-use-literal-types-for-fixed-string-sets)
   - 3.8 [Use TYPE_CHECKING for Optional Dependencies](#38-use-typechecking-for-optional-dependencies)
   - 3.9 [Use TypedDict or Dataclass Instead of dict[str, Any]](#39-use-typeddict-or-dataclass-instead-of-dictstr-any)
   - 3.10 [Use isinstance() for Type Checking, Not hasattr/getattr](#310-use-isinstance-for-type-checking-not-hasattrgetattr)
4. [API Design](#4-api-design) — **MEDIUM**
   - 4.1 [Avoid Boolean Flag Parameters in Public APIs](#41-avoid-boolean-flag-parameters-in-public-apis)
   - 4.2 [Choose the Simplest Namespace That Matches Ownership and Polymorphism](#42-choose-the-simplest-namespace-that-matches-ownership-and-polymorphism)
   - 4.3 [Don't Access Private Attributes](#43-dont-access-private-attributes)
   - 4.4 [Keep Data Models Flat and Non-Redundant](#44-keep-data-models-flat-and-non-redundant)
   - 4.5 [Keep Old Names as Deprecated Aliases](#45-keep-old-names-as-deprecated-aliases)
   - 4.6 [Order Required Fields Before Optional Fields](#46-order-required-fields-before-optional-fields)
   - 4.7 [Return New Collections from Transforms](#47-return-new-collections-from-transforms)
   - 4.8 [Underscore Prefix for Private Names](#48-underscore-prefix-for-private-names)
   - 4.9 [Use Keyword-Only Parameters for Optional Config](#49-use-keyword-only-parameters-for-optional-config)
5. [Code Simplification](#5-code-simplification) — **LOW-MEDIUM**
   - 5.1 [Extract Duplicated Logic Once Drift Risk Appears](#51-extract-duplicated-logic-once-drift-risk-appears)
   - 5.2 [Flatten Nested if Statements Into and Conditions](#52-flatten-nested-if-statements-into-and-conditions)
   - 5.3 [Inline Single-Use Intermediate Variables](#53-inline-single-use-intermediate-variables)
   - 5.4 [Remove Commented-Out and Dead Code](#54-remove-commented-out-and-dead-code)
   - 5.5 [Return Early to Flatten Control Flow](#55-return-early-to-flatten-control-flow)
   - 5.6 [Use @cached_property Only When the Instance Supports It](#56-use-cachedproperty-only-when-the-instance-supports-it)
   - 5.7 [Use Comprehensions Over for+append Loops](#57-use-comprehensions-over-forappend-loops)
   - 5.8 [Use any() / all() Over Boolean-Flag Loops](#58-use-any-all-over-boolean-flag-loops)
   - 5.9 [Use x or default for Fallback Values](#59-use-x-or-default-for-fallback-values)
6. [Performance](#6-performance) — **LOW-MEDIUM**
   - 6.1 [Build a Dict Index Instead of Nested Loops](#61-build-a-dict-index-instead-of-nested-loops)
   - 6.2 [Combine Filter and Map Into One Pass](#62-combine-filter-and-map-into-one-pass)
   - 6.3 [Compile Static Regex Patterns at Module Level](#63-compile-static-regex-patterns-at-module-level)
   - 6.4 [Define TypeAdapter Instances at Module Level](#64-define-typeadapter-instances-at-module-level)
   - 6.5 [Prefer Tuple Syntax in isinstance() Only on Profiled Hot Paths](#65-prefer-tuple-syntax-in-isinstance-only-on-profiled-hot-paths)
   - 6.6 [Stream with Generators When Memory or First-Result Latency Matters](#66-stream-with-generators-when-memory-or-first-result-latency-matters)
   - 6.7 [Use functools.lru_cache for Pure Functions](#67-use-functoolslrucache-for-pure-functions)
   - 6.8 [Use set for Repeated Membership Checks](#68-use-set-for-repeated-membership-checks)
7. [Naming](#7-naming) — **LOW-MEDIUM**
   - 7.1 [Avoid Redundant Type Suffixes in Names](#71-avoid-redundant-type-suffixes-in-names)
   - 7.2 [Drop Redundant Prefixes When Context Is Clear](#72-drop-redundant-prefixes-when-context-is-clear)
   - 7.3 [Rename When Behavior Changes](#73-rename-when-behavior-changes)
   - 7.4 [Use Consistent Terminology Across Code and Docs](#74-use-consistent-terminology-across-code-and-docs)
   - 7.5 [Use Specific Parameter and Variable Names](#75-use-specific-parameter-and-variable-names)
   - 7.6 [Use UPPER_CASE for Module Constants](#76-use-uppercase-for-module-constants)
8. [Imports & Structure](#8-imports-structure) — **LOW**
   - 8.1 [Handle Optional Dependencies Explicitly](#81-handle-optional-dependencies-explicitly)
   - 8.2 [Keep Modules Cheap to Import](#82-keep-modules-cheap-to-import)
   - 8.3 [No Duplicate Imports](#83-no-duplicate-imports)
   - 8.4 [Place Imports at the Top of the File](#84-place-imports-at-the-top-of-the-file)
   - 8.5 [Remove Unused Imports](#85-remove-unused-imports)
   - 8.6 [Scope Helpers and Constants to Their Usage Site](#86-scope-helpers-and-constants-to-their-usage-site)

---

## 1. Data Modeling

**Impact: HIGH**

The architectural foundation. Mutable defaults, mutation contracts, timezone-aware datetimes, discriminated unions. Mistakes here compound into state nobody intended.

### 1.1 Brand Primitive IDs With NewType

**Impact: MEDIUM (catches ID-confusion bugs at type-check time)**

When `user_id` and `team_id` are both `str`, a function accepting `UserId` will happily take a `TeamId` and fail at runtime — or worse, silently return wrong data. `NewType` makes them distinct at the type level without runtime overhead.

**Incorrect (interchangeable strings):**

```python
UserId = str
TeamId = str

def fetch_user(user_id: UserId) -> User: ...

team_id: TeamId = "team_xyz"
fetch_user(team_id)  # type checker is fine with this — runtime crash
```

`UserId = str` is a type *alias*, not a new type. The checker treats them identically.

**Correct (NewType creates a distinct nominal type):**

```python
from typing import NewType

UserId = NewType("UserId", str)
TeamId = NewType("TeamId", str)

def fetch_user(user_id: UserId) -> User: ...

team_id = TeamId("team_xyz")
fetch_user(team_id)  # type error: TeamId is not UserId
```

At runtime, `UserId("abc")` is just the string `"abc"` — no wrapper, no overhead. At type-check time, the checker refuses to confuse them.

**Construct at the boundary:** wrap raw strings as soon as they enter the system (API deserialization, DB rows). Once wrapped, they flow through the codebase as the branded type, and the checker enforces correctness.

**When NOT to brand:** short-lived local variables, truly interchangeable strings (raw log message bodies, arbitrary user text). Reserve branding for domain identifiers that must not be mixed up.

### 1.2 Create Explicit Variants Instead of Mode Flags

**Impact: MEDIUM (eliminates conditional-logic sprawl)**

When a class grows `is_thread`, `is_editing`, `is_forwarding` flags — or a mode parameter like `mode: Literal["thread", "edit", "forward"]` — stop. Each flag doubles the state space; each mode check adds conditional logic at every call site. Split into explicit classes instead.

**Incorrect (one class, many modes, exponential conditionals):**

```python
@dataclass
class MessageComposer:
    on_submit: Callable[[str], None]
    mode: Literal["channel", "thread", "dm_thread", "edit", "forward"]
    channel_id: str | None = None
    dm_id: str | None = None
    message_id: str | None = None

    def render(self) -> Frame:
        if self.mode == "dm_thread":
            extra = AlsoSendToDMField(self.dm_id)
        elif self.mode == "thread":
            extra = AlsoSendToChannelField(self.channel_id)
        else:
            extra = None
        if self.mode == "edit":
            actions = EditActions()
        elif self.mode == "forward":
            actions = ForwardActions()
        else:
            actions = DefaultActions()
        return Frame(extra, actions)
```

`MessageComposer(mode="thread", channel_id=x)` — which combinations are valid? Readers have to inspect the implementation to know.

**Correct (explicit variants; each self-contained):**

```python
@dataclass
class ChannelComposer:
    channel_id: str
    on_submit: Callable[[str], None]
    def render(self) -> Frame:
        return Frame(extra=None, actions=DefaultActions())

@dataclass
class ThreadComposer:
    channel_id: str
    on_submit: Callable[[str], None]
    def render(self) -> Frame:
        return Frame(AlsoSendToChannelField(self.channel_id), DefaultActions())

@dataclass
class EditMessageComposer:
    message_id: str
    on_submit: Callable[[str], None]
    def render(self) -> Frame:
        return Frame(extra=None, actions=EditActions())
```

Each class declares the fields its variant actually needs. Impossible combinations are unrepresentable. When variants genuinely share logic, extract helpers or a small base class that holds the common interface only — not a mega-class that mode-switches internally.

**Related:** this rule is about splitting behavior across classes. `data-discriminated-unions` is the same idea at the data-shape level — tag the variants so consumers can narrow with `match`/`if isinstance`. Reach for either when optional fields start accumulating to encode modes.

### 1.3 Delete Dead Variants

**Impact: LOW-MEDIUM (removes code paths that can't be reached)**

If a type has a variant that is never constructed — a `status: Literal["open", "closed", "archived"]` where `"archived"` is never set — delete the variant. Agents leave them behind "in case we need them later." The result is defensive branches in every consumer for a state that cannot occur.

**Incorrect ("archived" variant is declared but never produced):**

```python
from typing import Literal

OrderStatus = Literal["open", "paid", "shipped", "archived"]

def render_status(status: OrderStatus) -> str:
    match status:
        case "open": return "Awaiting payment"
        case "paid": return "Preparing to ship"
        case "shipped": return "In transit"
        case "archived": return "Archived"  # when does this branch ever run?
```

Grep the codebase: nothing assigns `"archived"`. That branch is unreachable, yet every consumer must handle it. It's a ghost.

**Correct (delete it):**

```python
from typing import Literal

OrderStatus = Literal["open", "paid", "shipped"]

def render_status(status: OrderStatus) -> str:
    match status:
        case "open": return "Awaiting payment"
        case "paid": return "Preparing to ship"
        case "shipped": return "In transit"
```

One fewer imaginary case. When "archived" actually becomes a requirement, add it then — tied to the real code that creates it.

**When NOT to delete:** if the variant exists in serialized data (old database rows, historical JSON) you still need to parse, keep it — but mark the non-canonical variants clearly (e.g., with a comment pointing to the migration that will remove them).

### 1.4 Derive, Don't Store

**Impact: HIGH (eliminates flag-sync bugs and halves the state space)**

Every boolean you add doubles the theoretical state space. When a value can be computed from data you already have, do not store it. Cached derived values require multiple mutation sites to stay in sync — and they won't.

**Incorrect (four flags that must be kept in sync):**

```python
from dataclasses import dataclass

@dataclass
class ThreadState:
    was_interrupted: bool
    did_assistant_finish: bool
    did_assistant_error: bool
    was_tool_call_only: bool

def should_show_footer(state: ThreadState) -> bool:
    return (
        state.did_assistant_finish
        and not state.was_interrupted
        and not state.did_assistant_error
        and not state.was_tool_call_only
    )
```

Four fields to answer one question. Four mutation sites elsewhere that must keep them synchronized. One missed update and the footer lies.

**Correct (derive from the event log):**

```python
def should_show_footer(events: list[SessionEvent]) -> bool:
    latest = get_latest_assistant_message(events)
    if latest is None:
        return False
    return (
        latest.completed
        and not latest.error
        and latest.finish_reason != "tool_calls"
    )
```

The answer is now computed from evidence that already exists. No sync required — one source of truth.

**When NOT to derive:**

- The domain genuinely has a state machine with ordered transitions (a checkout step *is* the state, not a cached conclusion)
- Temporal or external data that cannot be re-derived (timestamps from async processes, API responses needed downstream)
- The derivation is meaningfully more expensive than the stored value *and* you've measured the cost

**The debugging payoff:** pure derivation means tests become data-in, answer-out. Load fixtures, call the function, assert the result. No mocks, no timing reproduction.

### 1.5 Encapsulate Mutable State in the Narrowest Clear Scope

**Impact: MEDIUM (keeps mutation scoped to the owning object)**

Give mutable state the narrowest scope where the surrounding code still reads clearly. A closure fits when the interface is one or two callables and nothing needs to inspect the state. A focused class fits when state has identity — multiple methods share it, or tests, logs, or subclasses need to see it. A wide-open class where every method can touch the state is how invariants rot.

**Incorrect (state visible to every method on the class — too wide):**

```python
class DebouncedWriter:
    def __init__(self, callback: Callable[[], None], delay_ms: int = 300):
        self._callback = callback
        self._delay_ms = delay_ms
        self._timeout_handle: TimerHandle | None = None  # touched by every method

    def queue_send(self, text: str) -> None: ...
    def flush_now(self) -> None: ...
    def something_else(self) -> None: ...  # nothing prevents a bug here
```

**Correct (focused class — state scoped to the methods that need it):**

```python
@dataclass
class DebouncedAction:
    callback: Callable[[], None]
    delay_ms: int = 300
    _timeout: TimerHandle | None = field(default=None, init=False, repr=False)

    def trigger(self) -> None:
        if self._timeout is not None:
            self._timeout.cancel()
        self._timeout = schedule_after(self.delay_ms, self._fire)

    def _fire(self) -> None:
        self._timeout = None
        self.callback()

    def clear(self) -> None:
        if self._timeout is not None:
            self._timeout.cancel()
            self._timeout = None
```

A closure returning `(trigger, clear)` is the right alternative when no one needs to inspect, type, serialize, or mock the state — the surface is just the two callables. Module-level globals deserve more pushback than either; prefer dependency injection.

### 1.6 Never Use Mutable Default Arguments

**Impact: CRITICAL (prevents shared-state bugs across calls and instances)**

A default argument is evaluated **once**, when the `def` statement runs — not each call. A mutable default (`[]`, `{}`, `set()`, a dataclass instance) is therefore shared across every call that doesn't override it. Appending to the "default" list on one call mutates the default for every subsequent call. The same trap applies to dataclass and Pydantic field defaults. Always use `None` + body construction, or `default_factory`.

**Incorrect (the `[]` is one object, reused across calls):**

```python
def append_item(item: int, items: list[int] = []) -> list[int]:
    items.append(item)
    return items

append_item(1)  # [1]
append_item(2)  # [1, 2]   ← surprise: same list as before
```

**Correct (function — sentinel + per-call construction):**

```python
def append_item(item: int, items: list[int] | None = None) -> list[int]:
    if items is None:
        items = []
    items.append(item)
    return items
```

**Correct (dataclass / Pydantic — `default_factory` calls the constructor per instance):**

```python
from dataclasses import dataclass, field
from pydantic import BaseModel, Field

@dataclass
class User:
    tags: list[str] = field(default_factory=list)

class Config(BaseModel):
    tags: list[str] = Field(default_factory=list)
```

`@dataclass` rejects bare mutable defaults with `ValueError`. Pydantic v2 happens to deep-copy the default for each instance, but `Field(default_factory=list)` makes the intent explicit and survives version changes. Safe to use directly as defaults: tuples, frozensets, strings, ints, `None`, and frozen dataclasses — anything that can't be mutated.

### 1.7 Phase Related Optional Fields Into Nested Structs

**Impact: MEDIUM (one optional check instead of eight)**

When fields are "all present or all absent" in practice, don't model them as eight independent optionals at the top level. The flattened alternative forces consumers to `profile.first_name or defaults.first_name` eight times, and the type says nothing about which fields co-occur.

**Incorrect (twelve independent optionals; co-occurrence invisible to the type):**

```python
@dataclass
class UserProfile:
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    company: str | None = None
    job_title: str | None = None
    billing_address: str | None = None
    billing_city: str | None = None
    billing_zip: str | None = None
    card_last4: str | None = None
    card_brand: str | None = None
    card_expires: str | None = None
```

**Correct (grouped into phases; one optional check per group):**

```python
@dataclass
class Identity:
    first_name: str
    last_name: str
    email: str
    phone: str | None = None

@dataclass
class Billing:
    address: str
    city: str
    zip_code: str
    card_last4: str
    card_brand: str
    card_expires: str

@dataclass
class UserProfile:
    identity: Identity | None = None
    billing: Billing | None = None
```

Consumers check one optional: `if profile.billing is not None: use profile.billing.card_last4`. Every billing field is guaranteed present when `billing` is. The type system enforces the co-occurrence that was always true in practice. Rule of thumb: three or more optionals that always set/unset together belong in a nested struct.

### 1.8 Pick a Mutation Contract

**Impact: HIGH (prevents ambiguous caller expectations)**

A function that mutates its input *and* returns the same reference gives callers no way to tell whether to use the return value or the original. Pick one: mutate and return `None`, or clone and return the new value. Never both.

**Incorrect (mutates and returns — callers can't tell which to use):**

```python
def with_pending_action(state: AppState, action: str) -> AppState:
    state.pending_action = action  # mutation
    return state                   # and return
```

A caller reading `new_state = with_pending_action(state, "confirm")` reasonably assumes `state` is unchanged. It isn't. Another caller reads `with_pending_action(state, "confirm")` (ignoring the return) and assumes that's fine. It is — but only because the mutation happened. Two callers, two wrong mental models.

**Correct (mutate, return None):**

```python
def apply_pending_action(state: AppState, action: str) -> None:
    state.pending_action = action
```

The `None` return and the imperative verb (`apply_`) signal that this is a command. Caller knows the input was modified.

**Also correct (clone, return new):**

```python
from dataclasses import replace

def with_pending_action(state: AppState, action: str) -> AppState:
    return replace(state, pending_action=action)
```

`with_` naming signals a functional transform. The input is untouched; the caller must use the returned value.

**Naming conventions:**
- `apply_*`, `set_*`, `update_*_inplace` — mutate, return `None`
- `with_*`, `update_*`, `derive_*` — return a new value, leave input alone

The contract should be obvious from the name and signature without reading the body.

### 1.9 Use Discriminated Unions Over Optional Bags

**Impact: MEDIUM (tags variants explicitly in new designs; retrofit is expensive)**

Every optional field is a question the rest of the codebase must answer every time it touches the data. Optional fields accumulate as features grow, producing models where half the combinations are semantically invalid. Use a tagged (discriminated) union so the type system enforces which fields travel together.

**Incorrect (optional fields create impossible state combinations):**

```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class PaymentState:
    status: Literal["idle", "processing", "settled"]
    gateway: Literal["stripe", "paypal"] | None = None
    transaction_id: str | None = None
    initiated_at: str | None = None
    settled_at: str | None = None
```

When `status == "idle"`, should `gateway` exist? The type says maybe. When `status == "settled"`, is `settled_at` guaranteed? The type says no. Every consumer defensively checks for `None` on fields that must be present, or forgets to check fields that might not be.

**Correct (each variant carries exactly the fields it needs):**

```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class PaymentIdle:
    status: Literal["idle"] = "idle"

@dataclass
class PaymentProcessing:
    gateway: Literal["stripe", "paypal"]
    transaction_id: str
    initiated_at: str
    status: Literal["processing"] = "processing"

@dataclass
class PaymentSettled:
    gateway: Literal["stripe", "paypal"]
    transaction_id: str
    settled_at: str
    status: Literal["settled"] = "settled"

PaymentState = PaymentIdle | PaymentProcessing | PaymentSettled
```

Now `match payment.status:` narrows exactly, `transaction_id` is non-optional on the variants that have it, and impossible combinations (idle with a transaction ID, settled without a timestamp) are unrepresentable.

**With Pydantic** *(applicability: pydantic)*: use `Field(discriminator="status")` and a `status: Literal[...]` tag on each variant — Pydantic will validate and narrow automatically.

**Null over sentinels:** don't invent `"none"` action values. `pending_action: PendingAction | None` beats `pending_action: Literal["none", "confirm-address", "select-shipping"]`. Absence is not an action.

**Related:** `data-explicit-variants` applies the same idea at the behavior level — split a mode-flag class into one class per mode. Use discriminated unions when the variants are data; use explicit variants when the variants have meaningfully different methods.

### 1.10 Use Timezone-Aware Datetimes at Boundaries

**Impact: HIGH (prevents off-by-hours bugs across timezones, daylight saving, and storage)**

A `datetime` with no `tzinfo` is **naive**: two naive datetimes that look identical may refer to different absolute moments. Naive values leak into databases, JSON, logs, and inter-service messages, then surface as off-by-hours bugs during DST or when hosts differ. At any boundary the value crosses (HTTP, DB, queue, file, log, comparison), it must be timezone-aware. Store and transport in UTC; convert to local zones at display.

**Incorrect (`datetime.utcnow()` returns naive; deprecated in 3.12+):**

```python
from datetime import datetime

def stamp() -> datetime:
    return datetime.utcnow()              # naive — a serializer reading it as local time writes the wrong value
```

**Correct (UTC-aware at the boundary; local zone only for display):**

```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

def stamp() -> datetime:
    return datetime.now(timezone.utc)     # aware; round-trips through isoformat() cleanly

stored = datetime.now(timezone.utc)
display = stored.astimezone(ZoneInfo("America/Los_Angeles"))  # named zone, DST handled
```

`zoneinfo` (3.9+, PEP 615) reads from system tzdata and handles DST and historical offsets. Use named zones (`"America/Los_Angeles"`), not raw offsets (`-08:00`).

**Parsing input:** if callers can send naive datetimes, decide once whether to reject or assume a fixed zone. Never *silently* treat naive as UTC. For Pydantic v2, `AwareDatetime` rejects naive values at the model boundary. For PostgreSQL, use `TIMESTAMPTZ`; for SQLite/MySQL, store ISO-8601 strings with `+00:00` or epoch milliseconds.

Naive is acceptable only inside a tight block where every value is naive and the timezone is documented in scope, or for pure date arithmetic (use `date`, not `datetime`). If the value outlives the function it's created in, it should be aware.

### 1.11 Use a Sentinel Object When None Is a Real Domain Value

**Impact: MEDIUM (distinguishes "no value passed" from "None passed deliberately")**

When `None` carries semantic meaning — "user cleared this field," "no parent," "no assignee" — `None` can't also be the "not provided" default. Use a private sentinel instead. The sentinel is a unique object compared with `is`, never `==`. Complements `types-remove-redundant-optional`: that rule says drop `| None` when `None` is impossible; this one says use a sentinel when `None` is meaningfully different from "not passed."

**Incorrect (`None` does double duty as "absent" and "cleared"):**

```python
def update_user(user_id: str, nickname: str | None = None) -> User:
    user = db.get(user_id)
    user.nickname = nickname        # was the caller clearing it, or not passing it?
    db.save(user)
    return user
```

**Correct (sentinel default; `None` means "clear"):**

```python
from typing import Final

class _Unset:
    def __repr__(self) -> str:
        return "UNSET"

UNSET: Final = _Unset()

def update_user(user_id: str, nickname: str | None | _Unset = UNSET) -> User:
    user = db.get(user_id)
    if nickname is not UNSET:
        user.nickname = nickname     # may be None (cleared) or a real string
    db.save(user)
    return user

update_user("u1")                    # nickname untouched
update_user("u1", nickname=None)     # nickname cleared
update_user("u1", nickname="bob")    # nickname set to "bob"
```

Pydantic's PATCH pattern uses the same idea — `Field(default=UNSET)` + filtering `{k: v for k, v in model_dump().items() if v is not UNSET}` gives you "omitted field" vs. "explicit null."

A private `_SENTINEL = object()` is fine for tiny internal cases — PEP 661 itself uses that idiom. Prefer a named sentinel class (as above) when the sentinel appears in signatures, reprs, logs, or tracebacks, since the `__repr__` makes debugging easier. PEP 661 proposes a standard `sentinel(...)` helper, but it is still Draft and has not shipped in the `typing` module; do not claim `typing.Sentinel` exists. And don't reach for sentinels when `None` already means "absent" — two-state `Optional` doesn't need them.

## 2. Error Handling

**Impact: MEDIUM-HIGH**

Specific exceptions, context managers for resources, preserved cancellation semantics. Sloppy exceptions hide bugs; narrow catches localize them.

### 2.1 Catch Specific Exception Types

**Impact: HIGH (prevents masked bugs and broken Ctrl-C / cancellation)**

Catch the exception types you intend to handle. A broad `except Exception:` catches every regular error including your own bugs. A bare `except:` or `except BaseException:` is worse — it also catches `KeyboardInterrupt`, `SystemExit`, and `asyncio.CancelledError`, which must propagate.

**Incorrect (catches your own bugs):**

```python
def fetch_user(user_id: str) -> User | None:
    try:
        response = http.get(f"/users/{user_id}")
        return parse_user(response.json())
    except Exception:  # swallows KeyError from a typo in parse_user
        return None
```

**Correct (catch what you actually handle):**

```python
def fetch_user(user_id: str) -> User | None:
    try:
        response = http.get(f"/users/{user_id}")
    except (HTTPError, TimeoutError):
        return None
    return parse_user(response.json())  # bugs here propagate
```

Never use bare `except:` or `except BaseException:` — both catch `KeyboardInterrupt`, `SystemExit`, and `asyncio.CancelledError`. A broad `except Exception:` is fine at an outer boundary when you log and re-raise:

```python
def handle_request(req: Request) -> Response:
    try:
        return process(req)
    except Exception:
        logger.exception("unhandled error in request handler")
        raise
```

**Cancellation semantics (asyncio / anyio):** On Python 3.8+, `asyncio.CancelledError` inherits from `BaseException`, **not** `Exception`. So `except Exception:` is cancellation-safe — do not flag it as "swallowing cancellation." Only `except BaseException:` (or bare `except:`) catches cancellation. If you do catch `BaseException` or `anyio.get_cancelled_exc_class()`, re-raise. Wrap must-complete cleanup in `asyncio.shield()` — under cancellation, `finally:` blocks race against the cancellation itself.

For meaningful handling, create domain-specific exception types (`ToolTimeoutError(ToolExecutionError)`, etc.) so handlers match on failure mode rather than error text.

### 2.2 Consolidate try/except Blocks with the Same Handler

**Impact: LOW-MEDIUM (reduces duplication and simplifies control flow)**

When multiple adjacent operations raise the same exception and need the same handling, merge them into one block. Separate blocks duplicate the handler — and if the handling logic ever changes, you now need to update N places.

**Incorrect (three blocks, three copies of the same handler):**

```python
def load_config(path: Path) -> Config | None:
    try:
        raw = path.read_text()
    except FileNotFoundError:
        logger.warning("config missing: %s", path)
        return None

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        logger.warning("config invalid json: %s", path)
        return None

    try:
        return Config(**data)
    except ValidationError:
        logger.warning("config validation failed: %s", path)
        return None
```

Three copies of "log and return None." Changing the log level, adding a metric, or switching return value means editing three places.

**Correct (one block, one handler):**

```python
def load_config(path: Path) -> Config | None:
    try:
        raw = path.read_text()
        data = json.loads(raw)
        return Config(**data)
    except (FileNotFoundError, json.JSONDecodeError, ValidationError) as e:
        logger.warning("config load failed: %s (%s)", path, e)
        return None
```

One block, one handler, one place to change. The caller sees the same behavior; the implementation is simpler.

**When to keep blocks separate:**

- Different exceptions need **different** handling (log-and-return vs. retry vs. re-raise)
- Intermediate values matter for the handler (you want the partial result when the second step fails)
- The blocks are far apart in the function (folding them together would nest too much)

**Use `contextlib.suppress` for trivial "ignore the error" cases:**

```python
from contextlib import suppress

def try_cleanup(path: Path) -> None:
    with suppress(FileNotFoundError):
        path.unlink()
```

Cleaner than a full try/except for the "best effort, doesn't matter if it fails" pattern.

### 2.3 Inherit New Exceptions from Existing Base Exceptions

**Impact: MEDIUM (preserves backward compatibility for callers)**

When adding a new exception type to a module that already has an exception hierarchy, inherit from the relevant base. Callers that catch the base will continue to catch the new type; skipping the base forces every caller to add a new `except` branch.

**Incorrect (new exception inherits from Exception directly):**

```python
class ToolError(Exception): ...
class ToolTimeoutError(ToolError): ...
class ToolValidationError(ToolError): ...

# New failure mode added in v2:
class ToolRateLimitError(Exception):  # doesn't inherit from ToolError
    ...

# Existing caller:
try:
    run_tool(t, args)
except ToolError:  # no longer catches ToolRateLimitError
    retry()
```

The existing `except ToolError:` no longer catches the new error. Every caller must be updated — a silent breaking change.

**Correct (inherit from the existing base):**

```python
class ToolError(Exception): ...
class ToolTimeoutError(ToolError): ...
class ToolValidationError(ToolError): ...
class ToolRateLimitError(ToolError):  # fits the hierarchy
    ...

# Existing caller still works:
try:
    run_tool(t, args)
except ToolError:  # catches ToolRateLimitError too
    retry()
```

Callers that want to handle rate limits specifically can add `except ToolRateLimitError:` — but existing broad handlers keep working.

**Design the hierarchy deliberately:**

```python
class PackageError(Exception): ...            # root for everything the package raises
class UserError(PackageError): ...            # user-correctable
class ConfigError(UserError): ...
class UsageError(UserError): ...
class SystemError(PackageError): ...          # environmental / transient
class NetworkError(SystemError): ...
class TimeoutError(SystemError): ...
```

Callers can catch at whichever level of specificity they need. Adding new subtypes is non-breaking.

**Don't invert the hierarchy:** `class TimeoutError(PackageError)` is fine; `class PackageError(TimeoutError)` is nonsense. The base is the broader category, subclasses are narrower.

**Use `__init_subclass__` or explicit checks** if you need to prevent direct instantiation of the base — keep the type system as the contract enforcement.

### 2.4 Preserve Tracebacks When Logging Exceptions

**Impact: MEDIUM (keeps diagnostics intact when recovering from failures)**

When you catch an exception to recover or return a fallback, keep the traceback in the log. `logger.error(str(e))` records the message but loses the stack that explains where the failure came from — which is usually the part that makes the log useful.

**Incorrect (traceback discarded):**

```python
try:
    response = client.fetch(user_id)
except TimeoutError as e:
    logger.error("fetch failed: %s", e)
    return None
```

The log line records "fetch failed: timeout" with no stack — the caller sees a timeout but can't tell which code path produced it.

**Correct (`logger.exception` inside the `except` block):**

```python
try:
    response = client.fetch(user_id)
except TimeoutError:
    logger.exception("fetch failed for user_id=%r", user_id)
    return None
```

`logger.exception(...)` implicitly attaches `exc_info` from the current exception, so the traceback is included at ERROR level. Outside an `except` block — for example, when logging a handled exception from a worker queue — pass `exc_info=True` (or `exc_info=e`) explicitly:

```python
logger.error("task %r failed", task_id, exc_info=exc)
```

**When not to log:**

- You're re-raising (`raise` or `raise NewError(...) from e`) at the same boundary. The outer handler logs once; duplicating here produces two stacks for one failure.
- The exception is expected and recovery is routine (e.g., cache miss). A `logger.debug` or no log at all is often right.

### 2.5 Trust Validated State Within the Same Trust Domain

**Impact: MEDIUM (removes clutter without losing real safety)**

Once a value has been validated *and the validated object is immutable, locally constructed, and stays in the same trust domain*, internal helpers can skip re-checking it. The cousin of `types-trust-the-checker`: same principle, but state requires more care because state can change after validation.

**Incorrect (re-checking validated immutable state in the same module):**

```python
class ValidatedOrder(BaseModel):
    model_config = {"frozen": True}
    items: list[Item]
    total: int

    @model_validator(mode="after")
    def _check(self) -> "ValidatedOrder":
        if not self.items:
            raise ValueError("order must have items")
        if self.total < 0:
            raise ValueError("total must be non-negative")
        return self


def fulfill_order(order: ValidatedOrder) -> None:
    if not order.items:           # validator guarantees this
        raise ValueError("order must have items")
    if order.total < 0:           # validator guarantees this
        raise ValueError("total must be non-negative")
    for item in order.items:
        process(item)
```

**Correct (trust the invariant):**

```python
def fulfill_order(order: ValidatedOrder) -> None:
    for item in order.items:
        process(item)
```

**Keep the check when any of these fail:** (1) object is mutable, (2) constructed outside this process (rehydrated from cache, queue, DB), (3) an untyped or plugin caller could produce a bad instance, (4) the object has been exposed to code that might have mutated it. Rehydration is the most common miss — `ValidatedOrder.model_validate_json(...)` freshly out of the validator is fine; the same type pulled from a cache with no re-validation is not.

When you do trust the invariant, a single `assert order.items, "validator guarantees non-empty"` at the entry point documents the reasoning without sprinkling defensive `if` chains through the body.

### 2.6 Use !r Format for Identifiers in Error Messages

**Impact: LOW (produces consistent, unambiguous messages)**

`{name!r}` calls `repr(name)` — producing `'foo'` instead of `foo`, `42` instead of `42`, `None` instead of nothing. Use it for identifiers (names, paths, IDs) in error messages so values are clearly delimited and edge cases (empty strings, whitespace-only names, `None`) render visibly.

**Incorrect (ambiguous formatting):**

```python
raise ValueError(f"Tool {tool_name} not found in registry")
# "Tool  not found in registry" — did tool_name have leading/trailing spaces? was it empty?
# "Tool None not found in registry" — was the literal string "None" or actual None?
```

**Correct (`!r` delimits and disambiguates):**

```python
raise ValueError(f"Tool {tool_name!r} not found in registry")
# "Tool '' not found in registry"      — clearly empty string
# "Tool 'my tool' not found in registry" — spaces visible
# "Tool None not found in registry"    — unambiguously the None sentinel
```

Quotes frame the value. `None`, numbers, and special types render with their `repr` — always unambiguous.

**Apply consistently:**

- **Names, IDs, paths:** `!r`
- **Numeric counts:** plain `{}` (e.g., `f"retrying {count} times"`)
- **Prose:** plain `{}`

```python
raise ValueError(f"tool {name!r} failed after {retries} retries")
raise FileNotFoundError(f"config not found at {path!r}")
raise KeyError(f"unknown key {key!r} in {registry_name!r}")
```

**When backticks are preferable:** some codebases use Markdown-style backticks for user-facing messages (CLI output, log lines humans read). Pick one convention per project and stick to it. `!r` is usually right for Python exception messages; backticks are usually right for log strings rendered in docs or notebooks.

### 2.7 Use assert Only for Debug-Only Internal Invariants

**Impact: MEDIUM (`-O` strips asserts; use for debug-only invariants, not runtime contracts)**

`assert` is a debug-only statement — Python emits no code for it under `-O` or `PYTHONOPTIMIZE`. That makes `assert` the right tool for "this can never happen if my code is correct" and the wrong tool for any check that must run in production.

**Incorrect (runtime contract that vanishes under `-O`):**

```python
def transfer_funds(account_id: str, amount: int) -> None:
    assert amount > 0, "amount must be positive"  # stripped under -O
    assert account_id, "account_id required"      # stripped under -O
    ...
```

**Correct (real exceptions for contracts that must hold; `assert` only for programmer-error invariants):**

```python
def transfer_funds(account_id: str, amount: int) -> None:
    if not account_id:
        raise ValueError("account_id required")
    if amount <= 0:
        raise ValueError("amount must be positive")
    ...

def process_step(step: Step) -> Result:
    # Step is a closed union; hitting the default branch is a programmer error.
    if isinstance(step, InitStep): return init()
    if isinstance(step, RunStep):  return run()
    if isinstance(step, DoneStep): return done()
    assert False, f"unhandled Step variant: {step!r}"  # debug-only
```

If the input crosses a trust boundary (user input, external API, deserialized data), always use a real exception — `AssertionError` is a poor signal at a system boundary even when it does fire. For exhaustiveness checks specifically, `typing.assert_never` is sharper than `assert False` (see `error-assert-never-exhaustiveness`). Rule of thumb: if you can't articulate why losing the check under `-O` is acceptable, it shouldn't be an `assert`.

### 2.8 Use assert_never for Exhaustiveness Checks

**Impact: MEDIUM (turns "missing variant" into a type-check error)**

`typing.assert_never()` (Python 3.11+) tells static checkers "every variant has been handled here." If the union later grows a new member, the checker reports the missed branch as a type error before the code ships. At runtime it raises `AssertionError`, so a missed case still fails loudly even if the checker is bypassed. This is separate from `assert` — that statement is debug-only and can be stripped under `-O`.

**Incorrect (the checker can't see this branch is exhaustive):**

```python
Step = InitStep | RunStep | DoneStep

def process_step(step: Step) -> Result:
    if isinstance(step, InitStep): return init()
    if isinstance(step, RunStep):  return run()
    if isinstance(step, DoneStep): return done()
    raise RuntimeError(f"unexpected step: {step!r}")  # adding PausedStep slips past the checker
```

**Correct (`assert_never` — type error if the union grows, runtime error if reached):**

```python
from typing import assert_never

def process_step(step: Step) -> Result:
    match step:
        case InitStep(): return init()
        case RunStep():  return run()
        case DoneStep(): return done()
        case _:
            assert_never(step)
```

When `Step` becomes `InitStep | RunStep | DoneStep | PausedStep`, the checker reports that `step` is `PausedStep` at the `assert_never` call. Use it for closed sums: `Literal` unions, sealed dataclass hierarchies, discriminated unions, enum dispatch. On Python <3.11, import from `typing_extensions` — semantics are identical and both mypy and pyright recognize either source.

### 2.9 Use raise ... from to Preserve Exception Causality

**Impact: LOW-MEDIUM (explicit `__cause__` chain vs implicit `__context__`; often invisible to end callers)**

When you catch one exception and raise another, include `from original` to preserve the chain. Without it, the traceback prints "During handling of the above exception, another exception occurred" — which is usually right, but the explicit form is clearer and survives `__cause__` suppression in some runtimes.

**Incorrect (original exception lost or implicit):**

```python
def load_config(path: Path) -> Config:
    try:
        raw = path.read_text()
    except FileNotFoundError:
        raise ConfigError(f"config missing: {path}")  # loses the original FileNotFoundError context
```

The traceback will still show both — Python implicitly sets `__context__` — but the intent isn't explicit, and `__cause__` is `None`, which some tools use to distinguish "we meant this chain" vs. "an error happened while handling."

**Correct (explicit `raise ... from`):**

```python
def load_config(path: Path) -> Config:
    try:
        raw = path.read_text()
    except FileNotFoundError as e:
        raise ConfigError(f"config missing: {path}") from e
```

The traceback prints "The above exception was the direct cause of the following exception" — a deliberate chain. `__cause__` is set, so programmatic handlers and logging can walk the chain cleanly.

**Use `from None` to suppress the context:**

When the original exception is genuinely internal and the caller shouldn't see it:

```python
def parse_timestamp(s: str) -> datetime:
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        raise ValueError(f"invalid timestamp: {s!r}") from None
```

The user-facing error is clean (`ValueError: invalid timestamp: 'abc'`) without the implementation's internal `ValueError: Invalid isoformat string:`.

**Three patterns:**

- `raise NewError() from original` — explicit chain; `__cause__` set
- `raise NewError()` inside `except` — implicit chain; `__context__` set
- `raise NewError() from None` — suppress the original context entirely

Default to `from original` when translating between exception types. Reach for `from None` when the internal cause is noise to the caller.

### 2.10 Use with / async with for Resource Lifetimes

**Impact: HIGH (deterministic cleanup even on exceptions)**

Any object that owns a finite resource — files, sockets, DB connections, locks, temp dirs, HTTP clients, GPU contexts — should be acquired with `with` (or `async with`). The protocol guarantees `__exit__` runs even when the body raises, so cleanup happens deterministically. Manual `close()` forgets to fire on exceptions, leaks resources under failure, and is easy to misorder during refactors.

**Incorrect (manual close — leaks on exception):**

```python
def write_report(path: Path, rows: list[Row]) -> None:
    f = path.open("w")
    for row in rows:
        f.write(format_row(row))   # if this raises, f is never closed
    f.close()
```

**Correct (`with` — close runs on success, exception, or early return):**

```python
def write_report(path: Path, rows: list[Row]) -> None:
    with path.open("w") as f:
        for row in rows:
            f.write(format_row(row))
```

**Async clients use `async with`:**

```python
async def fetch_user(user_id: str) -> User:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"/users/{user_id}")
        return User.model_validate_json(response.content)
```

For multiple resources acquired together, `contextlib.ExitStack` closes all of them in reverse order even if one acquisition raises. Write your own with `@contextlib.contextmanager` (or `@asynccontextmanager`) when a resource isn't already a context manager — `yield` the resource inside a `try` / `finally`.

If you're writing `try` / `finally` to call `close()`, `release()`, or `disconnect()`, you almost certainly want `with` instead.

### 2.11 Validate Input at System Boundaries

**Impact: MEDIUM (fails fast and prevents bad data from spreading)**

Validate once, at the edge — not repeatedly in every internal function. Sprinkling defensive checks throughout the call chain "in case something got through" bloats internals without catching anything a boundary check didn't. Push validation to the boundary (API handler, CLI entrypoint, deserialization), then trust the validated value.

**Incorrect (validation scattered through every internal function):**

```python
def process_order(order_id: str) -> None:
    if not order_id:
        raise ValueError("order_id required")
    order = load_order(order_id)
    fulfill(order)

def load_order(order_id: str) -> Order:
    if not order_id:  # checked again
        raise ValueError("order_id required")
    ...

def fulfill(order: Order) -> None:
    if not order.id:  # and again
        raise ValueError("order has no id")
    ...
```

Every internal function re-validates. If the validation rule changes (e.g., order IDs must match a pattern), every copy must change.

**Correct (validate at entry; trust internally):**

```python
# boundary: the API handler
def handle_fulfill_request(req: Request) -> Response:
    try:
        body = FulfillRequest.model_validate(req.json())  # Pydantic does the work
    except ValidationError as e:
        return error_response(400, str(e))

    process_order(body.order_id)
    return success_response()

# internal: takes a validated value, trusts it
def process_order(order_id: OrderId) -> None:
    order = load_order(order_id)
    fulfill(order)
```

One validation point. Internal code takes `OrderId` (a branded `NewType`) and trusts it — the validation already happened.

**Boundaries that need validation:**

- HTTP request parsing (headers, path params, query strings, body)
- CLI argument parsing
- Reading files or database rows that originated outside the system
- Message queue consumers
- Foreign API responses

**Heuristic:** data at a boundary is untrusted. Validate it into a typed model (Pydantic, dataclass with a validator, `NewType` + explicit check). Once validated, the typed model flows through internal code unchecked.

**Fail fast:** validate before expensive operations. Don't read a 10MB file, parse it, and *then* reject it for missing a required field — check the field first.

## 3. Type Safety

**Impact: MEDIUM-HIGH**

Precise types catch bugs at type-check time. Fix type errors rather than ignore them; no `Any` drift in new code.

### 3.1 Avoid Any Annotations

**Impact: MEDIUM (narrows types in new code; retrofitting existing `Any` is churn)**

`Any` turns off the type checker for that value — it accepts anything, produces anything, and propagates silently into every call site that consumes it. `Any` is common when the right type feels hard to write; almost always, a `Protocol`, `TypeVar`, or `Union` is available.

**Incorrect (Any leaks through the system):**

```python
from typing import Any

def process_items(items: Any) -> Any:
    return [transform(item) for item in items]

def transform(item: Any) -> Any:
    return item.value.upper()
```

The checker cannot help here. A caller passing a `dict` instead of a list silently walks into runtime errors. `item.value.upper()` is unchecked — a typo in `value` would never be caught.

**Correct (precise types; Protocol for duck-typed inputs):**

```python
from typing import Protocol

class HasValue(Protocol):
    value: str

def process_items(items: list[HasValue]) -> list[str]:
    return [transform(item) for item in items]

def transform(item: HasValue) -> str:
    return item.value.upper()
```

The checker now verifies that every call site passes a list of objects with a `.value: str` attribute. Typos in `.value` get caught. Return types propagate.

**Correct (TypeVar for truly generic containers):**

```python
from typing import TypeVar

T = TypeVar("T")

def first_or_none(items: list[T]) -> T | None:
    return items[0] if items else None
```

Generic, not unchecked.

**When `Any` is genuinely unavoidable** (interop with dynamically typed libraries, some JSON boundaries), restrict its scope to one line, narrow to a concrete type immediately, and document the invariant in a comment.

### 3.2 Fix Type Definitions Instead of cast()

**Impact: MEDIUM (keeps source type definitions honest)**

`cast(T, value)` tells the checker to pretend `value` is a `T` with no runtime check. When called to paper over a structural mismatch, it hides a design problem. Reach for it only when runtime logic genuinely narrows in a way the checker can't express.

**Incorrect (cast masks an unnecessarily wide return type):**

```python
from typing import cast

def load_config() -> dict[str, object]:
    return json.loads(CONFIG_PATH.read_text())

def get_timeout() -> int:
    config = load_config()
    return cast(int, config["timeout"])  # we're just telling the checker to trust us
```

The real issue: `load_config` returns `dict[str, object]` because `json.loads` does. But this project's config has a known shape — fix the source type.

**Correct (declare the real structure):**

```python
from typing import TypedDict

class Config(TypedDict):
    timeout: int
    retries: int

def load_config() -> Config:
    return json.loads(CONFIG_PATH.read_text())  # validate or cast here, once

def get_timeout() -> int:
    config = load_config()
    return config["timeout"]  # known to be int from Config
```

Now every downstream consumer benefits from the typed shape.

**When `cast()` is the right tool:** when runtime logic narrows beyond what the checker can prove — e.g., after a literal tag check, a custom predicate, or a known invariant enforced elsewhere.

```python
from typing import cast

def handle_success(result: ApiResponse) -> str:
    # An earlier check already verified result.status == "success"
    # but the checker can't propagate that narrowing here
    assert result.status == "success"
    return cast(SuccessResponse, result).data  # ok; narrowing is real
```

Even then, `isinstance` or a `TypeGuard` function is usually cleaner. Reserve `cast` for cases where those don't fit.

**Rule of thumb:** before reaching for `cast`, ask whether the source type should be narrower. 8 times out of 10, yes.

### 3.3 Fix Type Errors, Don't Ignore Them

**Impact: HIGH (prevents masked errors from compounding)**

`# type: ignore` and `# pyright: ignore` silence the checker — but the underlying problem stays. Ignore comments are common when a type looks hard; each one degrades the signal from every future run. Fix the error properly, and when a suppression is genuinely unavoidable, document why.

**Incorrect (ignore comment masks the real problem):**

```python
def compute(items: list[int] | None) -> int:
    return sum(items)  # type: ignore  # noqa
```

The checker flagged this because `sum(None)` crashes at runtime. The ignore hides a real bug.

**Correct (handle the None case):**

```python
def compute(items: list[int] | None) -> int:
    if items is None:
        return 0
    return sum(items)
```

The type system caught a real bug; fixing it is the right answer.

**When a suppression is genuinely required** (a complex generic the checker can't handle, a known checker limitation, an external library with bad stubs), include:

1. The specific error code (e.g., `# type: ignore[arg-type]`)
2. A comment explaining the safety reasoning

```python
# mypy cannot narrow through the factory's return type, but the
# registry guarantees adapters[cls] returns cls instances.
# See: https://github.com/python/mypy/issues/XXXX
adapter = adapters[cls]  # type: ignore[assignment]
```

A reviewer should be able to read the comment and confirm the suppression is justified without re-deriving the reasoning.

**Escape hatches to prefer before ignoring:**
- `cast(T, value)` with a comment (see `types-fix-types-not-cast` for when it's appropriate)
- `assert isinstance(x, T)` — runtime check plus narrowing
- `TypeGuard` functions for reusable narrowing
- Actually fixing the type signatures upstream

Reach for `# type: ignore` last, not first.

### 3.4 Narrow Type Signatures to Runtime Reality

**Impact: MEDIUM (eliminates unreachable branches and false permissiveness)**

If control flow (a `match` statement, an API contract, an earlier `isinstance` check) guarantees that only a subset of a union reaches a code path, the annotation should reflect that — not the wider union. Over-broad annotations create dead branches and suggest possibilities the code can't actually handle.

**Incorrect (signature wider than reality):**

```python
def render_tool_result(part: MessagePart) -> str:
    # by contract this is only called with ToolResultPart or ToolCallPart
    if isinstance(part, ToolResultPart):
        return f"Result: {part.content}"
    if isinstance(part, ToolCallPart):
        return f"Call: {part.tool_name}"
    if isinstance(part, TextPart):
        return part.text  # unreachable — caller never passes TextPart
    raise ValueError(f"unexpected part: {part}")
```

The `TextPart` branch can't run (the caller guarantees it), but the type says `MessagePart`. Readers have to figure out the contract from context.

**Correct (tighten the annotation):**

```python
ToolPart = ToolCallPart | ToolResultPart

def render_tool_result(part: ToolPart) -> str:
    if isinstance(part, ToolResultPart):
        return f"Result: {part.content}"
    return f"Call: {part.tool_name}"  # must be ToolCallPart
```

The signature documents the contract. No dead branches. A caller that tries to pass a `TextPart` gets a type error, not a runtime `ValueError`.

**When the wider type is necessary:** when the function genuinely handles the full union at some call sites and a subset at others, accept the widest used type and narrow inside. Don't invent a separate wider signature "to be safe."

**Exhaustiveness check:**

```python
from typing import assert_never

def render_tool_result(part: ToolPart) -> str:
    match part:
        case ToolResultPart(): return f"Result: {part.content}"
        case ToolCallPart(): return f"Call: {part.tool_name}"
        case _: assert_never(part)  # checker fails if union grows
```

`assert_never` ensures that if `ToolPart` gains a new variant, every `match` on it is re-examined.

### 3.5 Remove Redundant `| None` When Values Are Guaranteed

**Impact: LOW-MEDIUM (eliminates false uncertainty in the type signature)**

An annotation of `X | None` tells readers and the checker that `None` is a real possibility — every consumer now writes a `None` check. When the value is guaranteed to be set (by the constructor, by the control flow, by an earlier validation), `| None` lies about the API.

**Incorrect (optional annotation on a guaranteed-present value):**

```python
from dataclasses import dataclass

@dataclass
class Session:
    user_id: str
    token: str | None = None  # but we always generate a token in __post_init__

    def __post_init__(self) -> None:
        if self.token is None:
            self.token = generate_token()
```

Every consumer of `session.token` now writes `if session.token is not None: ...` — for a value that is always present.

**Correct (use a factory default; drop the optional):**

```python
from dataclasses import dataclass, field

@dataclass
class Session:
    user_id: str
    token: str = field(default_factory=generate_token)
```

`session.token` is now unambiguously a `str`. No defensive `None` checks downstream.

**Also incorrect (`| None` on `NotRequired` TypedDict fields):**

```python
from typing import TypedDict, NotRequired

class Config(TypedDict):
    name: str
    timeout: NotRequired[int | None]  # already optional via NotRequired
```

`NotRequired` already expresses "may be absent." Adding `| None` lets the caller pass `None` *instead of* omitting — which is rarely what you want. Either the field is absent (`NotRequired`) or it has a value (no `| None`).

**When `| None` is correct:** when `None` is a real, semantic value — "no assignee," "no parent," "not yet fetched." Absence as a meaningful state deserves `None`.

**Heuristic:** if every consumer writes `if x is not None:` before using the value, either `None` is never really set (remove `| None`) or you should have a different sentinel (a default, a distinct variant).

### 3.6 Trust the Type Checker — Remove Redundant Runtime Checks

**Impact: LOW-MEDIUM (removes noise and signals confidence in the types)**

When types already constrain a value, runtime checks for the same constraint add noise and imply the types aren't trustworthy. Every redundant `assert` or `isinstance` is a vote of no confidence in the rest of the type system.

**Incorrect (runtime checks that duplicate the type):**

```python
def process_user(user: User) -> str:
    assert user is not None        # type says User, not User | None
    assert isinstance(user, User)   # type already says User
    assert user.name                # if name: str, this only catches empty strings
    return user.name.upper()
```

The first two lines add nothing. The third conflates "empty string" with "None" — if that matters, say so with a dedicated check and a real error message.

**Correct (trust the signature):**

```python
def process_user(user: User) -> str:
    return user.name.upper()
```

If callers pass `None` against the signature, that's a bug in the caller — and the type checker will flag it at the call site.

**Also incorrect (defensive check after validation):**

```python
def process_request(raw: str) -> Response:
    validated = validate(raw)  # returns ValidatedRequest, never None
    if validated is None:
        raise ValueError("invalid")  # unreachable
    return handle(validated)
```

`validate` returns `ValidatedRequest` by its signature — no `None`. The check is dead.

**When runtime checks are the right tool:**

- At **trust boundaries**: external API responses, deserialized user input, third-party callbacks where the type is aspirational
- As **narrowing aids**: `assert isinstance(x, T)` to narrow from a wider type the checker can't otherwise see
- For **invariants the checker can't express**: "this list is sorted," "this counter is positive"

Inside your own code, let the types do the work.

### 3.7 Use Literal Types for Fixed String Sets

**Impact: MEDIUM (catches invalid strings at type-check time)**

When a parameter accepts one of a fixed set of string values, `str` is too wide — every typo is legal. `Literal["a", "b", "c"]` narrows the type to exactly those values and enables `match` exhaustiveness checking.

**Incorrect (plain str accepts anything):**

```python
def set_log_level(level: str) -> None:
    ...

set_log_level("DEUBG")  # typo — compiles fine, runtime surprise
```

The checker cannot tell you `"DEUBG"` is invalid. A typo at a call site silently passes through until the function hits an unexpected branch.

**Correct (Literal restricts to the valid set):**

```python
from typing import Literal

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR"]

def set_log_level(level: LogLevel) -> None:
    ...

set_log_level("DEUBG")  # type error — caught at type-check time
```

IDEs autocomplete the valid values. Typos are flagged before running.

**Pairs well with `match`:**

```python
def level_priority(level: LogLevel) -> int:
    match level:
        case "DEBUG": return 10
        case "INFO": return 20
        case "WARNING": return 30
        case "ERROR": return 40
```

If a new level is added to the `Literal` type without updating this `match`, checkers with exhaustiveness support flag the missing case.

**When to use `Enum` instead:** when the values have methods or rich behavior (e.g., `LogLevel.DEBUG.name`, `LogLevel.DEBUG.value`). Enums also work well with exhaustiveness checking but carry more ceremony than `Literal`. For plain string tags, `Literal` is lighter.

**When to use plain `str`:** free-form user input, message bodies, URLs, any field that isn't a finite enumeration.

### 3.8 Use TYPE_CHECKING for Optional Dependencies

**Impact: LOW-MEDIUM (preserves type hints without forcing the import)**

When a module's type hints reference a class from an optional dependency, importing the module should not require that dependency to be installed. `if TYPE_CHECKING:` blocks let the checker see the import while the runtime stays lean.

**Incorrect (importing an optional dep at runtime):**

```python
import anthropic  # crashes if anthropic is not installed

class AnthropicProvider:
    def __init__(self, client: anthropic.Client) -> None:
        self._client = client
```

A user installing just the core package and never touching Anthropic still gets a `ModuleNotFoundError` at import time.

**Incorrect (falling back to `Any`):**

```python
from typing import Any

class AnthropicProvider:
    def __init__(self, client: Any) -> None:  # we gave up on the type
        self._client = client
```

This works at runtime but loses type safety on every method that uses `self._client`.

**Correct (TYPE_CHECKING block + quoted hint):**

```python
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import anthropic

class AnthropicProvider:
    def __init__(self, client: anthropic.Client) -> None:
        self._client = client
```

With `from __future__ import annotations`, all annotations are strings at runtime — so `anthropic.Client` in the signature doesn't need the import to resolve. The checker still resolves it during type-check because it sees the `TYPE_CHECKING` branch.

**Pattern for optional-dep packages:**

```python
# At module top
try:
    import anthropic
except ImportError as e:
    raise ImportError(
        "Please install the anthropic extra: `pip install 'mylib[anthropic]'`"
    ) from e
```

Combine the runtime guard (helpful error if the user hits a code path that needs the dep) with `TYPE_CHECKING` for the hints.

### 3.9 Use TypedDict or Dataclass Instead of dict[str, Any]

**Impact: MEDIUM (structured alternative to `dict[str, Any]` when writing new code)**

When the shape of a dict is known — config objects, API payloads, structured events — `dict[str, Any]` is a lie about the data. The structure exists; it's just not declared, so every access is a runtime gamble. `TypedDict` or `dataclass` restores type-checker coverage.

**Incorrect (structure erased):**

```python
from typing import Any

def create_user(config: dict[str, Any]) -> User:
    name = config["name"]            # what type?
    age = config.get("age", 0)       # what type?
    prefs = config.get("prefs", {})  # dict or the passed-in value?
    return User(name=name.upper(), age=age + 1, prefs=prefs)
```

**Correct (`TypedDict` — dict-shaped but typed; use at serialization boundaries):**

```python
from typing import TypedDict, NotRequired

class UserConfig(TypedDict):
    name: str
    age: NotRequired[int]
    prefs: NotRequired["UserPreferences"]

def create_user(config: UserConfig) -> User:
    return User(name=config["name"].upper(), age=config.get("age", 0))
```

For in-memory values with behavior and defaults, prefer a `dataclass`; when you also need runtime validation, `pydantic.BaseModel`. `dict[str, Any]` is the right answer only for genuinely unstructured data — log context, free-form metadata. If you know the fields, declare them.

### 3.10 Use isinstance() for Type Checking, Not hasattr/getattr

**Impact: MEDIUM (enables proper type narrowing for the checker)**

Type checkers narrow types through `isinstance()` checks, discriminator match statements, and `TypeGuard` functions — not through `hasattr()`, `getattr()`, or `type(obj).__name__ == "..."`. `hasattr` is common for "flexibility"; the actual cost is that the checker can't narrow and refactors silently break string comparisons.

**Incorrect (hasattr/getattr defeats type narrowing):**

```python
def process(part: MessagePart) -> str:
    if hasattr(part, "tool_name"):
        return f"Tool: {part.tool_name}"  # type checker: attribute is Any
    if getattr(part, "kind", None) == "text":
        return part.text  # type checker: does part.text exist? unclear
    if type(part).__name__ == "ImagePart":
        return f"Image: {part.url}"  # fragile: renaming ImagePart breaks this
    return "unknown"
```

The checker gives up on every branch. If `ToolPart` is renamed, the `type(...).__name__` string comparison silently stops matching — and no tests catch it because the function still runs.

**Correct (isinstance enables narrowing):**

```python
def process(part: MessagePart) -> str:
    if isinstance(part, ToolPart):
        return f"Tool: {part.tool_name}"  # narrowed to ToolPart
    if isinstance(part, TextPart):
        return part.text                    # narrowed to TextPart
    if isinstance(part, ImagePart):
        return f"Image: {part.url}"         # narrowed to ImagePart
    return "unknown"
```

Now the checker verifies that `part.tool_name`, `part.text`, and `part.url` each exist on the narrowed type. Renaming a class triggers type errors at every use site.

**For tagged unions, use `match` on the discriminator:**

```python
def process(part: MessagePart) -> str:
    match part.kind:
        case "tool":  return f"Tool: {part.tool_name}"
        case "text":  return part.text
        case "image": return f"Image: {part.url}"
```

When `part.kind` is a `Literal` discriminator on a `Union`, `match` narrows each branch to the matching variant.

**When to reach for `hasattr`:** genuinely optional extension protocols where classes may or may not implement a method. Even then, prefer `isinstance(obj, Protocol)` with a `runtime_checkable` Protocol over raw attribute probing.

## 4. API Design

**Impact: MEDIUM**

Interfaces that age well. Required-before-optional ordering, keyword-only params, no boolean flag soup. Mostly applies to new code.

### 4.1 Avoid Boolean Flag Parameters in Public APIs

**Impact: MEDIUM (prevents call sites that read like "do_thing(thing, True, False)")**

A boolean parameter is a binary mode switch hiding behind a generic type. `download(url, True, False, True)` is unreadable, the body branches on the flag with near-duplicate paths, and adding a third mode later breaks the API. The function-level cousin of `data-explicit-variants`: when behavior meaningfully changes on a flag, prefer split functions or a `Literal`/`Enum` parameter.

**Incorrect (boolean flags — call sites lose meaning):**

```python
def export_report(rows: list[Row], to_csv: bool = True, compress: bool = False) -> bytes:
    data = render_csv(rows) if to_csv else render_json(rows)
    return gzip.compress(data) if compress else data

export_report(rows, False, True)   # JSON, compressed? CSV, compressed? Reader can't tell.
```

**Correct (`Literal` parameter when the modes share most of the body):**

```python
from typing import Literal

Format = Literal["csv", "json", "parquet"]

def export_report(rows: list[Row], format: Format, *, compress: bool = False) -> bytes:
    match format:
        case "csv":     data = render_csv(rows)
        case "json":    data = render_json(rows)
        case "parquet": data = render_parquet(rows)
    return gzip.compress(data) if compress else data

export_report(rows, format="csv", compress=True)
```

Adding a fourth format is a one-line change to the `Literal`; call sites read meaningfully. Use an `Enum` when modes carry behavior or constants (e.g. `CompressionLevel.BEST` with value `9`). Split into separate functions when bodies barely overlap and composition is orthogonal.

A single keyword-only `bool` is still fine when the name clearly answers "what does `True` mean?" (`include_archived=True`, `strict=True`, `dry_run=True`) and the body is a small filter rather than two near-duplicate paths. Read call sites out loud: `export_report(rows, True, False)` fails; `export_report(rows, format="csv", compress=True)` passes.

### 4.2 Choose the Simplest Namespace That Matches Ownership and Polymorphism

**Impact: LOW-MEDIUM (avoids unnecessary coupling without forcing a binary choice)**

Python lets the same logic live as a module function, instance method, `@classmethod`, `@staticmethod`, or Protocol. None is universally right. Pick the smallest namespace that captures **ownership** (does this operation belong to one object?) and **polymorphism** (will multiple types provide their own version?). Start at module scope; promote to a method only when ownership or polymorphism actually demand it.

**Incorrect (instance method that doesn't need `self` and isn't overridden):**

```python
class DateFormatter:
    def format_iso(self, d: date) -> str:
        return d.isoformat()  # self unused, no subclasses overriding
```

**Correct (module-level function — simpler namespace):**

```python
def format_iso(d: date) -> str:
    return d.isoformat()
```

Conversely, a module function that threads state through a single parameter usually belongs on that type:

```python
# Awkward: mutates `user`, names it in every parameter list, no second caller type
def update_user_preferences(user: User, key: str, value: object) -> None:
    user.prefs[key] = value
    user.last_modified = now()

# Better: the method form matches ownership
class User:
    def update_preference(self, key: str, value: object) -> None:
        self.prefs[key] = value
        self.last_modified = now()
```

Use `@classmethod` for alternative constructors (`Event.from_json(raw)`); the method needs the class for subclass-friendly construction but not an instance. Use a `Protocol` when several unrelated types need to provide the same interface without a shared base. `@staticmethod` is the rarest tier — if there's no `self` and no `cls`, a module function is usually cleaner. Starting too coupled (everything on a class) is harder to undo than starting too loose (a free function you later move).

### 4.3 Don't Access Private Attributes

**Impact: LOW-MEDIUM (internals are free to change without notifying external callers)**

`_prefixed` names are the author's contract: "this is internal, it may change." Reaching into another module's or class's private attributes couples your code to implementation details you weren't invited into. Use the public API, or ask the owner to expose what you need.

**Incorrect (poking at private state):**

```python
from some_lib import Client

client = Client()
# peeking at a private attribute because there's no public way
retry_count = client._retry_state["count"]
client._pool.clear()  # mutating private state
```

Next version of `some_lib` renames `_retry_state` to `_retries` (it's private, they're allowed to) — your code breaks with no warning. Or worse, `_pool.clear()` no longer does what you assumed, and you corrupt state silently.

**Correct (use the public API):**

```python
from some_lib import Client

client = Client()
retry_count = client.stats.retries  # public property
client.reset_pool()                  # public method
```

If `some_lib` doesn't expose what you need, open an issue or PR. Using `_private` is a workaround, not a fix.

**Inside your own code:** same rule applies between modules. If `module_a` finds itself reaching into `module_b._helpers`, the helper probably shouldn't be private — or `module_a` shouldn't need it.

**The exception:** testing your own internals. Unit tests for a class may legitimately assert on `_private` state. Even then, prefer testing through the public interface when feasible — tests that poke at internals are brittle to refactoring.

**Double underscore (`__name`) is stronger:** Python name-mangles `__name` to `_ClassName__name`, making accidental access even harder. Use it for attributes you're committed to keeping inaccessible.

### 4.4 Keep Data Models Flat and Non-Redundant

**Impact: MEDIUM (reduces API surface and prevents field drift)**

Data models drift when fields duplicate each other, wrap single values in unnecessary containers, or mirror fields from the parent structure. Each duplicate is a second source of truth that can go stale. Each single-key wrapper adds access ceremony for no gain.

**Incorrect (redundant fields, single-key wrappers, unnecessary lists):**

```python
from dataclasses import dataclass

@dataclass
class ToolReturn:
    tool_name: str                           # also in parent
    call_id: str                             # also in parent
    content: dict[str, object]               # single-key wrapper around return_value
    return_value: dict[str, object]          # duplicated in content
    messages: list[Message]                  # always contains exactly one Message

@dataclass
class ToolCall:
    tool_name: str
    call_id: str
    return_part: ToolReturn
```

`tool_name` and `call_id` are carried on both the parent and the child — they'll drift. `content` wraps `return_value`. `messages` is a list that always has length one.

**Correct (flat, non-redundant):**

```python
from dataclasses import dataclass

@dataclass
class ToolReturn:
    content: object  # the actual return value, unwrapped
    message: Message

@dataclass
class ToolCall:
    tool_name: str
    call_id: str
    return_part: ToolReturn
```

`tool_name` and `call_id` live on the parent only. `content` holds the value directly. `message` is singular because there's only ever one.

**Check for:**

- Fields that exist on both parent and child (pick one, usually parent)
- `data: {"value": X}` single-key wrappers (unwrap to `data: X`)
- Lists that always contain exactly one element (use a scalar)
- Fields that are computed from other fields (derive, don't store)

**Why it matters:** redundancy means every mutation site has two (or more) places to update. Skipping one creates a drift bug that's only visible when the fields disagree.

**Related:** `data-derive-dont-store` is the same idea at the field level — if one field is computable from another, compute it, don't store it.

### 4.5 Keep Old Names as Deprecated Aliases

**Impact: MEDIUM (enables gradual migration without breakage)**

Renaming a public function, class, or parameter is a breaking change. Users upgrade at their own pace; if the old name vanishes, they can't. Keep the old name as a deprecated alias for at least one release, pointing at the new name.

**Incorrect (rename breaks existing code immediately):**

```python
# v1.0
def get_user(user_id: str) -> User: ...

# v1.1
def fetch_user(user_id: str) -> User: ...  # v1.0 callers now crash
```

**Correct (Python 3.13+: `@warnings.deprecated` marks the symbol for type checkers too):**

```python
import warnings

@warnings.deprecated("get_user is deprecated; use fetch_user instead.")
def get_user(user_id: str) -> User:
    return fetch_user(user_id)
```

On older Pythons, call `warnings.warn("...", DeprecationWarning, stacklevel=2)` inside the alias body — same runtime effect, minus the static-checker signal.

For renamed *parameters*, `@warnings.deprecated` doesn't apply — it decorates whole symbols. Accept the old keyword as a compatibility path with a sentinel default, forward to the new name, and emit `warnings.warn(..., DeprecationWarning, stacklevel=2)` when the old path is taken. Remove the alias in a later major version. Skip deprecation only when the name was never public (starts with `_`, not in `__all__`, not in docs).

### 4.6 Order Required Fields Before Optional Fields

**Impact: HIGH (Python enforces this at class-definition time)**

Python's dataclass implementation requires fields without defaults to precede fields with defaults — trying to put an optional field before a required one is a `TypeError` at class-definition time. More importantly, the order communicates intent: required first, defaults last.

**Incorrect (raises `TypeError`):**

```python
from dataclasses import dataclass

@dataclass
class Tool:
    name: str
    description: str = ""
    version: str         # TypeError: non-default argument follows default argument
```

**Correct (required fields first):**

```python
from dataclasses import dataclass

@dataclass
class Tool:
    name: str
    version: str
    description: str = ""
```

**When a required field must come after an optional one:** use keyword-only with `KW_ONLY`. This lets you reorder freely while still enforcing "required" via the type system:

```python
from dataclasses import dataclass, KW_ONLY

@dataclass
class Tool:
    name: str
    _: KW_ONLY
    description: str = ""
    version: str  # required, keyword-only — order no longer constrained
```

Everything after `_: KW_ONLY` is keyword-only, so the "required before optional" rule stops applying — the caller must pass them by name.

**Same rule applies to function parameters:**

```python
# bad: positional default before positional required
def connect(host="localhost", port): ...  # SyntaxError

# good: required first
def connect(port, host="localhost"): ...

# also good: keyword-only lets you mix freely
def connect(*, port, host="localhost", retries): ...
```

### 4.7 Return New Collections from Transforms

**Impact: MEDIUM (prevents surprising side effects)**

A function called `filter_active(users)` that mutates `users` in place is a trap — the name says "filter," the behavior says "modify." Default to returning new collections. Reserve mutation for functions whose names make it unmistakable (`sort_in_place`, `update_items`).

**Incorrect (transform that secretly mutates):**

```python
def filter_active(users: list[User]) -> list[User]:
    users[:] = [u for u in users if u.is_active]  # mutates input!
    return users
```

A caller doing `active = filter_active(all_users); log_total(len(all_users))` gets a confusing bug — `all_users` was modified, but the call site doesn't reveal that.

**Correct (return a new list):**

```python
def filter_active(users: list[User]) -> list[User]:
    return [u for u in users if u.is_active]
```

Input is untouched. Behavior matches the name.

**When in-place mutation is appropriate:** when it's performance-critical on a measured hot path, and the name signals it unambiguously.

```python
def sort_in_place(items: list[int]) -> None:
    items.sort()

def update_status_inplace(user: User, status: str) -> None:
    user.status = status
```

Name conventions:
- `*_in_place` / `*_inplace` — mutates, returns `None`
- `update_*` — mutates (if state-management convention) or returns new (if data-transform convention); be consistent within the codebase
- `with_*`, `filter_*`, `map_*`, `derive_*` — returns new, input untouched

**Rule of thumb:** if the function's name is a verb phrase describing a transformation, default to returning new. If it's imperative and clearly a command (`sort`, `apply`, `set`), mutation is expected.

### 4.8 Underscore Prefix for Private Names

**Impact: LOW-MEDIUM (signals internal API and limits backward-compat obligations)**

Names that start with `_` are internal. Names that don't are public — and public means "backward-compatible forever unless deprecated." Without language-level enforcement, implementation details often stay public; underscore them on the way in, not after they've leaked.

**Incorrect (implementation detail treated as public):**

```python
# mymodule.py
def format_date(d):
    return _to_iso_string(d)

def to_iso_string(d):    # helper — but no underscore, so it's public
    return d.isoformat()

__all__ = ["format_date", "to_iso_string"]  # accidentally exported
```

Now `to_iso_string` is part of the module's public API. Changing its signature, renaming it, or removing it breaks anyone who imported it.

**Correct (underscore the helper; exclude from `__all__`):**

```python
# mymodule.py
def format_date(d):
    return _to_iso_string(d)

def _to_iso_string(d):
    return d.isoformat()

__all__ = ["format_date"]
```

`_to_iso_string` is clearly internal. You can rename it, delete it, change its signature — no backward-compat obligation.

**Same rule for class attributes and methods:**

```python
class Cache:
    def get(self, key: str) -> object | None: ...     # public
    def _evict_lru(self) -> None: ...                  # internal helper
    def _entries(self) -> dict[str, object]: ...       # internal state access
```

**Don't reach into `_private` from outside.** If you find yourself writing `obj._internal`, either (a) the attribute should be public and the owner should know, or (b) the design has a gap — add a public method instead. Reaching into `_private` couples you to implementation details that may change.

**`__all__` is the contract:** `from mymodule import *` respects `__all__`. Tools like Sphinx and type checkers also use it to determine the public surface. Keep it minimal and accurate.

### 4.9 Use Keyword-Only Parameters for Optional Config

**Impact: MEDIUM (prevents breakage when adding or reordering params)**

Positional parameters lock in their order forever — adding a new parameter in the middle breaks every caller. Keyword-only parameters (after `*` in functions, after `_: KW_ONLY` in dataclasses) let you add, remove, or reorder without breaking callers. Positional is Python's default; keyword-only is an explicit choice.

**Incorrect (positional config — order is now part of the API):**

```python
def fetch(url, timeout=30, retries=3, verify_ssl=True, backoff=1.5):
    ...

fetch("https://api.example.com", 60, 5, False)
```

What do `60, 5, False` mean at this call site? Only the function signature knows. And if you want to add `user_agent` between `retries` and `verify_ssl`, every positional call site breaks.

**Correct (keyword-only for config params):**

```python
def fetch(url, *, timeout=30, retries=3, verify_ssl=True, backoff=1.5):
    ...

fetch("https://api.example.com", timeout=60, retries=5, verify_ssl=False)
```

The `*` forces everything after it to be passed by name. Call sites self-document. New params can slot anywhere without breaking callers.

**For dataclasses, use `KW_ONLY`:**

```python
from dataclasses import dataclass, KW_ONLY

@dataclass
class FetchOptions:
    url: str
    _: KW_ONLY
    timeout: int = 30
    retries: int = 3
    verify_ssl: bool = True
    backoff: float = 1.5
```

Callers must pass `timeout=`, `retries=`, etc. by name.

**Heuristic:** the first one or two params can be positional (the "thing" the function operates on). Everything else — especially optional configuration — should be keyword-only.

**For public APIs this is non-negotiable:** once a library ships positional config params, every reorder or addition is a breaking change.

## 5. Code Simplification

**Impact: LOW-MEDIUM**

Python idioms. Comprehensions, `any()`/`all()`, early returns. Mostly stylistic — apply when writing or reviewing.

### 5.1 Extract Duplicated Logic Once Drift Risk Appears

**Impact: MEDIUM (prevents divergent implementations of the same logic)**

The first copy is fine. The second copy is the decision point: extract now, or accept drift later. A third copy is the safe default for "rule of three," but if the logic encodes a domain rule (validation, formatting, permissions) that must stay consistent, extract at the second copy. The cost of delay is bugs where copies evolved in subtly different directions.

**Incorrect (same logic duplicated across handlers):**

```python
def handle_stream(stream: AsyncIterator[Chunk]) -> Response:
    collected = []
    async for chunk in stream:
        if chunk.kind == "text":
            collected.append(chunk.text)
        elif chunk.kind == "tool":
            collected.append(format_tool(chunk))
    return Response(content="".join(collected))

def handle_non_stream(response: RawResponse) -> Response:
    collected = []
    for chunk in response.chunks:
        if chunk.kind == "text":
            collected.append(chunk.text)
        elif chunk.kind == "tool":
            collected.append(format_tool(chunk))
    return Response(content="".join(collected))
```

Two copies of the chunk-formatting logic. A new chunk kind gets added — two places need updates. One gets missed, and the streaming handler silently produces different output than the non-streaming one.

**Correct (extract once, use twice):**

```python
def _format_chunk(chunk: Chunk) -> str:
    match chunk.kind:
        case "text": return chunk.text
        case "tool": return format_tool(chunk)
        case _: return ""

async def handle_stream(stream: AsyncIterator[Chunk]) -> Response:
    parts = [_format_chunk(c) async for c in stream]
    return Response(content="".join(parts))

def handle_non_stream(response: RawResponse) -> Response:
    parts = [_format_chunk(c) for c in response.chunks]
    return Response(content="".join(parts))
```

Now a new chunk kind means one change. The two handlers can't drift apart.

**When NOT to extract:**

- The two occurrences look similar but serve genuinely different purposes — premature abstraction locks them together
- The shared logic is 2-3 trivial lines and naming a helper is more noise than value
- Each caller would need the helper to accept so many optional parameters that it becomes a mode-switch

**Location of the helper:**

- Private (`_name`) in the same module if it's specific to that module
- Module-level utility if multiple modules share it
- Base class method if it's a shared class operation (`data-explicit-variants`)

### 5.2 Flatten Nested if Statements Into and Conditions

**Impact: LOW (reduces indentation and improves readability)**

When nested `if` statements share the same body with no intervening code, collapse them into a single `if` with `and`. The nested form implies the branches do something different; when they don't, the structure lies.

**Incorrect (nested if with no intervening code):**

```python
def should_notify(user: User, event: Event) -> bool:
    if user.is_active:
        if user.notifications_enabled:
            if event.priority >= user.notification_threshold:
                return True
    return False
```

**Correct (one combined condition):**

```python
def should_notify(user: User, event: Event) -> bool:
    return (
        user.is_active
        and user.notifications_enabled
        and event.priority >= user.notification_threshold
    )
```

Keep the nesting when intermediate logging, validation, or early returns happen between checks, or when the branches do genuinely different work. The rule: if every nested branch only holds another `if` until the final body, flatten. For chains where the happy path is the final action, the guard-clause form from `simplify-early-return` often reads cleanest.

### 5.3 Inline Single-Use Intermediate Variables

**Impact: LOW (reduces noise and indirection)**

When a variable is assigned once and used once immediately after, inlining it removes a name that doesn't earn its keep. Intermediates like `_filtered`, `_cleaned`, `_copy` show up "for clarity" — but the clarity is usually from the name, and if the name isn't informative, the variable is just noise.

**Incorrect (intermediates that add nothing):**

```python
def top_admins(users: list[User], limit: int) -> list[User]:
    filtered_users = [u for u in users if u.is_admin]
    sorted_users = sorted(filtered_users, key=lambda u: u.rank)
    result = sorted_users[:limit]
    return result
```

Four lines, four names — each used exactly once. The names restate the operations, not the purpose.

**Correct (inline when the operation is its own explanation):**

```python
def top_admins(users: list[User], limit: int) -> list[User]:
    return sorted(
        (u for u in users if u.is_admin),
        key=lambda u: u.rank,
    )[:limit]
```

Four operations, zero intermediate names. Each step's intent is visible in place.

**When an intermediate variable earns its place:**

- The name adds genuine information the expression doesn't convey
- The value is used more than once
- The expression would be too long to read as one unit
- Debugging benefits from a named step (breakpoints, logging)

```python
# the name "eligible" adds information the expression doesn't
def distribute_bonuses(users: list[User], amount: Decimal) -> None:
    eligible = [u for u in users if u.tenure_months >= 12 and not u.on_leave]
    share = amount / len(eligible)
    for user in eligible:
        pay_bonus(user, share)
```

Here `eligible` is used twice and the name documents the business rule. Keep it.

**Heuristic:** if you can't give the intermediate a name more meaningful than a restatement of the operation, inline it.

### 5.4 Remove Commented-Out and Dead Code

**Impact: LOW-MEDIUM (reduces confusion about intent)**

Commented-out code, superseded implementations, unused imports, and definitions nothing calls — delete them. Version control preserves history; dead code in the file confuses readers about which implementation is actually active.

**Incorrect (commented alternatives and stale code):**

```python
def fetch_user(user_id: str) -> User:
    # Old implementation:
    # response = requests.get(f"/users/{user_id}")
    # return User(**response.json())

    response = http_client.get(f"/users/{user_id}")
    return User.model_validate(response.json())

    # TODO: switch to async version once available
    # async def fetch_user(user_id): ...

def _unused_helper(x: int) -> int:  # nothing calls this
    return x * 2
```

Readers wonder: is the commented version the fallback? Is the TODO still accurate? Is `_unused_helper` called dynamically somewhere I'm missing?

**Correct (delete; let git remember):**

```python
def fetch_user(user_id: str) -> User:
    response = http_client.get(f"/users/{user_id}")
    return User.model_validate(response.json())
```

If you need the old implementation back, `git log` has it.

**Targets to delete:**

- Commented-out blocks of code
- Functions, methods, classes that nothing calls (verify with grep across the codebase first)
- Unused imports (`ruff` or `pyflakes` finds these)
- Unused variables
- Dead branches (if a condition can never be true)
- `print()` statements left over from debugging
- Commented-out log lines

**When to keep what looks like dead code:**

- Called dynamically (by name, via `getattr`, via a registry)
- Part of a public API contract that external callers may use
- Intentionally present for future use, with a TODO that links to a tracking issue

**For "intentional TODOs," link to the tracking issue:**

```python
# TODO(ISSUE-123): switch to async http_client when the migration lands
```

A TODO with a link is a commitment. A TODO without one is a wish.

### 5.5 Return Early to Flatten Control Flow

**Impact: LOW-MEDIUM (keeps the happy path unnested and readable)**

When a function has preconditions to check, return as soon as one fails. Deeply nested "if valid, if authorized, if ..." pyramids bury the happy path five levels in. Guard clauses flatten the structure and make the happy path the most visible branch.

**Incorrect (pyramid of nesting — the actual work is five levels in):**

```python
def process_request(req: Request) -> Response:
    if req.authenticated:
        if req.authorized:
            if req.body is not None:
                if req.body.is_valid:
                    return do_process(req.body)
                else:
                    return error(400, "invalid body")
            else:
                return error(400, "missing body")
        else:
            return error(403, "forbidden")
    else:
        return error(401, "unauthenticated")
```

**Correct (guard clauses; happy path unindented at the end):**

```python
def process_request(req: Request) -> Response:
    if not req.authenticated:
        return error(401, "unauthenticated")
    if not req.authorized:
        return error(403, "forbidden")
    if req.body is None:
        return error(400, "missing body")
    if not req.body.is_valid:
        return error(400, "invalid body")

    return do_process(req.body)
```

The same pattern applies to loops — `if not item.active: continue` instead of nesting the work inside `if item.active:`. Keep `if/else` when the two branches do comparable work (`"positive"` vs. `"negative"` vs. `"zero"`); guard-clause when one branch is an error and the other is the real work.

### 5.6 Use @cached_property Only When the Instance Supports It

**Impact: MEDIUM (defers work safely; misuse causes races and silent staleness)**

`@cached_property` defers expensive derivations until first access and caches the result in `instance.__dict__`. It fits when the inputs are effectively immutable, the getter is idempotent, the class has a writable `__dict__`, and nothing is racing on first access. Outside that envelope it masks real bugs: stale caches when inputs mutate, `TypeError` on `__slots__` classes without `__dict__`, and duplicated work when two threads hit the property simultaneously.

**Incorrect (mutable inputs — silent staleness):**

```python
from functools import cached_property
from dataclasses import dataclass, field

@dataclass
class Report:
    rows: list[Row] = field(default_factory=list)  # callers can append

    @cached_property
    def summary_stats(self) -> Stats:
        return compute_stats(self.rows)

r = Report()
r.summary_stats          # caches based on empty rows
r.rows.append(new_row)   # mutates input
r.summary_stats          # still the old cached Stats — stale, no warning
```

**Correct (frozen container; cache cannot go stale):**

```python
@dataclass(frozen=True)
class Report:
    rows: tuple[Row, ...]

    @cached_property
    def summary_stats(self) -> Stats:
        return compute_stats(self.rows)
```

**Caveats:** not thread-safe — two threads racing on first access can both run the getter. `__slots__` classes without `"__dict__"` raise `TypeError` at first access. `copy.copy` carries the cached value over; clear it manually if the copy's inputs differ. For module-level pure functions, use `functools.lru_cache` / `functools.cache` instead (see `perf-lru-cache-pure-fns`) — `@cached_property` is the per-instance equivalent.

### 5.7 Use Comprehensions Over for+append Loops

**Impact: LOW (more concise, often faster, and idiomatic Python)**

Comprehensions express "build a collection from an iterable" in one line. C-style loops with `append()` have more variables and more places for off-by-one and wrong-list bugs. Reach for a comprehension by default.

**Incorrect (imperative loop + append):**

```python
def active_usernames(users: list[User]) -> list[str]:
    result = []
    for user in users:
        if user.is_active:
            result.append(user.name)
    return result
```

**Correct (list, dict, set, and generator forms):**

```python
def active_usernames(users: list[User]) -> list[str]:
    return [user.name for user in users if user.is_active]

name_to_id = {user.name: user.id for user in users}
unique_tags = {tag for post in posts for tag in post.tags}
total = sum(item.price for item in items)   # generator, no intermediate list
```

Break a comprehension into a loop when the expression stops reading like English — multi-step logic, side effects, or nested conditionals with intermediate variables are signs the comprehension has outgrown one line. For boolean reductions, prefer `any(u.is_admin for u in users)` over `any([...])` — the generator short-circuits and avoids materializing the list.

### 5.8 Use any() / all() Over Boolean-Flag Loops

**Impact: LOW (shorter, short-circuits, no manual flag management)**

When you're checking "does any element satisfy X?" or "do all elements satisfy X?", Python has built-ins for that. Agents sometimes write manual `found = False` / `break` patterns — more code, more bugs, no short-circuit benefit.

**Incorrect (manual flag + break):**

```python
def has_admin(users: list[User]) -> bool:
    found = False
    for user in users:
        if user.is_admin:
            found = True
            break
    return found

def all_ready(services: list[Service]) -> bool:
    for s in services:
        if not s.ready:
            return False
    return True
```

**Correct (built-ins):**

```python
def has_admin(users: list[User]) -> bool:
    return any(u.is_admin for u in users)

def all_ready(services: list[Service]) -> bool:
    return all(s.ready for s in services)
```

Both short-circuit — `any()` stops at the first truthy, `all()` stops at the first falsy.

**Pass a generator, not a list:**

```python
# wasteful — builds the full list before checking
any([expensive_check(x) for x in items])

# right — lazy generator, stops at first match
any(expensive_check(x) for x in items)
```

**Other built-ins worth remembering:**

```python
# count matches
count = sum(1 for x in items if x.valid)

# min / max with a key
cheapest = min(items, key=lambda x: x.price)

# first matching element (or None)
first_error = next((x for x in items if x.failed), None)
```

`next(generator, default)` is the Pythonic "find first or default" — more direct than a loop with an early return.

**When to use a loop instead:** when you need the loop variable for something else, the logic has side effects, or the condition is too complex to fit in a generator cleanly.

### 5.9 Use x or default for Fallback Values

**Impact: LOW (more concise and idiomatic than if/else)**

For the common "use `x` if it's truthy, otherwise `default`" pattern, `x or default` beats the verbose `if`/`else`. The catch: this triggers on every falsy value (`0`, `''`, `[]`, `None`) — so only use it when those aren't semantically meaningful.

**Incorrect (verbose if/else for a simple fallback):**

```python
def display_name(user: User) -> str:
    if user.nickname:
        return user.nickname
    else:
        return user.username
```

**Correct (or-fallback):**

```python
def display_name(user: User) -> str:
    return user.nickname or user.username
```

Shorter, idiomatic, and clear.

**When `or` is WRONG:** when falsy values are semantically valid.

```python
# wrong — if count is 0, we'd return DEFAULT_COUNT instead of 0
def get_count(config: Config) -> int:
    return config.count or DEFAULT_COUNT

# right — explicit about the None case
def get_count(config: Config) -> int:
    return config.count if config.count is not None else DEFAULT_COUNT
```

Zero, empty string, empty list, and empty dict are all falsy but often meaningful. `0 retries` ≠ `default retries`. `"" name` is probably a bug but it's not the same as "name was never set."

**Use `... if ... is not None else ...` when you specifically mean "None":**

```python
timeout = config.timeout if config.timeout is not None else DEFAULT_TIMEOUT
```

**Use `... if ... else ...` when the condition is more elaborate:**

```python
label = name.strip() if name and name.strip() else "anonymous"
```

**Rule of thumb:** `or` for truthy/falsy semantics; explicit `is not None` for optional-value semantics.

## 6. Performance

**Impact: LOW-MEDIUM**

Python-specific optimizations. Set/dict lookups, cached properties, module-level compilation. Applied on measured hot paths, not as a stylistic crusade.

### 6.1 Build a Dict Index Instead of Nested Loops

**Impact: MEDIUM (O(n) instead of O(n²))**

When code says "for each item in A, find the matching item in B," the naive pattern is nested `for` + `if x.id == y.id` — that's O(n × m). Build a dict from B once, then it's O(n + m) with each lookup O(1).

**Incorrect (nested scan — 100M comparisons for 10k × 10k):**

```python
def attach_profiles(users: list[User], profiles: list[Profile]) -> list[EnrichedUser]:
    result = []
    for user in users:
        matching = None
        for profile in profiles:
            if profile.user_id == user.id:
                matching = profile
                break
        result.append(EnrichedUser(user=user, profile=matching))
    return result
```

**Correct (dict index — O(n + m)):**

```python
def attach_profiles(users: list[User], profiles: list[Profile]) -> list[EnrichedUser]:
    profiles_by_user = {p.user_id: p for p in profiles}
    return [
        EnrichedUser(user=user, profile=profiles_by_user.get(user.id))
        for user in users
    ]
```

For one-to-many grouping, `collections.defaultdict(list)` avoids the "check-then-create" dance: `posts_by_author[post.author_id].append(post)`. `itertools.groupby` groups already-sorted inputs without building a dict. Nested loops stay fine for small collections (under ~50 × 50), for one-off operations, or when the inner loop has rich logic that doesn't reduce to a key lookup.

### 6.2 Combine Filter and Map Into One Pass

**Impact: LOW (one iteration instead of two or three)**

When you filter a collection and then map (or map and filter, etc.), it's often one comprehension, not two or three chained operations. Each chained step allocates an intermediate list and iterates.

**Incorrect (three passes, two intermediate lists):**

```python
def prices_for_sale_items(items: list[Item]) -> list[Decimal]:
    sale_items = [i for i in items if i.on_sale]
    discounted = [i for i in sale_items if i.discount > 0]
    prices = [i.price * (1 - i.discount) for i in discounted]
    return prices
```

Three allocations, three passes.

**Correct (one pass, one list):**

```python
def prices_for_sale_items(items: list[Item]) -> list[Decimal]:
    return [
        item.price * (1 - item.discount)
        for item in items
        if item.on_sale and item.discount > 0
    ]
```

One pass, one list. Conditions combined; mapping in the expression.

**When chaining is clearer:**

If each step has enough logic that inlining makes the comprehension hard to read, keep them separate — readability wins over a small constant-factor performance gain:

```python
# fine — each step has real logic
eligible = [normalize(u) for u in users if u.tenure_months >= 12]
grouped = group_by_team(eligible)
summaries = [compute_summary(team, members) for team, members in grouped.items()]
```

**For reductions, use the built-in that takes a generator:**

```python
# don't build a list just to sum it
total = sum([i.price for i in items if i.on_sale])

# better — generator, no intermediate list
total = sum(i.price for i in items if i.on_sale)
```

Same for `min`, `max`, `any`, `all`, `''.join(...)`.

For multi-step transforms, `itertools` provides streaming building blocks (`chain`, `islice`, `groupby`). Most of the time, one comprehension is enough.

### 6.3 Compile Static Regex Patterns at Module Level

**Impact: LOW (marginal outside tight loops; Python's re cache handles most cases)**

Compile static regexes at module scope when the pattern is reused, named, or sits on a measured hot path. Python's `re` module caches recent compiled patterns from the module-level calls (`re.search`, `re.match`, etc.), so a one-shot call outside a hot path is not paying a real recompilation cost. The win from hoisting is mostly readability and naming — and, on genuinely hot paths, bypassing the cache lookup.

**Incorrect (reused pattern buried inline, no name):**

```python
import re

def extract_version(text: str) -> str | None:
    match = re.search(r"v(\d+\.\d+\.\d+)", text)
    return match.group(1) if match else None
```

The pattern is a named concept (`VERSION_RE`) shared across the module but inlined anonymously. If a second function needs the same regex, it gets copied.

**Correct (compiled once at module scope with a descriptive name):**

```python
import re

_VERSION_RE = re.compile(r"v(\d+\.\d+\.\d+)")

def extract_version(text: str) -> str | None:
    match = _VERSION_RE.search(text)
    return match.group(1) if match else None
```

The name documents intent, other call sites reuse the same object, and a tight loop avoids the internal cache lookup.

**Naming:**

- `_UPPER_CASE` for module-level private regex constants (or whatever your project's constant convention is)
- Descriptive names — `_VERSION_RE`, `_EMAIL_RE`, not `_PATTERN1`

**Don't hoist when:**

- The pattern depends on a runtime value (different per call)
- The regex is one-shot startup parsing and an inline call reads more clearly

**Related:** the same "build once, use many" instinct applies to other reusable objects — `TypeAdapter`, `json.JSONDecoder` with custom hooks, precompiled templates.

### 6.4 Define TypeAdapter Instances at Module Level

**Impact: LOW-MEDIUM (avoids repeated schema construction)**

**Applicability:** Pydantic v2's `TypeAdapter`. The same principle applies to any object whose constructor does real work.

`TypeAdapter` builds a validation schema on construction by walking the target type, resolving annotations, and assembling the validation tree. Inside a hot function, every call rebuilds it. Create once at module scope; reuse.

**Incorrect (schema rebuilt on every call):**

```python
from pydantic import TypeAdapter

def parse_users(raw: bytes) -> list[User]:
    adapter = TypeAdapter(list[User])  # schema built every call
    return adapter.validate_json(raw)
```

**Correct (module-level constant):**

```python
_USERS_ADAPTER: TypeAdapter[list[User]] = TypeAdapter(list[User])

def parse_users(raw: bytes) -> list[User]:
    return _USERS_ADAPTER.validate_json(raw)
```

When the target type depends on a runtime value, cache per type with `@functools.cache`:

```python
@cache
def _adapter_for(model_type: type) -> TypeAdapter:
    return TypeAdapter(model_type)
```

The same pattern applies to `json.JSONDecoder` with custom hooks, `msgpack.Packer` / `Unpacker` with configuration, compiled templates, and precomputed lookup tables — anything whose constructor does real work.

### 6.5 Prefer Tuple Syntax in isinstance() Only on Profiled Hot Paths

**Impact: LOW (tiny per-call savings; only relevant in tight loops)**

Both `isinstance(x, (A, B, C))` and `isinstance(x, A | B | C)` are correct and supported in Python 3.10+. They produce the same result. The tuple form is *marginally* faster on each call because the union form constructs a `types.UnionType` object, but the gap is small enough that it only matters inside loops you've actually profiled. **Do not blanket-rewrite a codebase from union to tuple syntax** — the noise is rarely worth the diff.

This is a micro-optimization, not a correctness rule. Apply it only when:

1. The check is inside a measured hot path (a tight loop, called millions of times per request, etc.)
2. You have profiling data showing `isinstance` is a meaningful share of the time
3. You'd otherwise reach for a more invasive change (rewriting the dispatch, caching results)

In normal code, write whichever reads more naturally. `isinstance(x, int | float)` mirrors a type annotation and is a fine default.

**Incorrect (rewriting `A | B` to `(A, B)` everywhere as a stylistic crusade):**

```python
# A drive-by PR that flips every isinstance() in the codebase.
def is_numeric(x: object) -> bool:
    return isinstance(x, (int, float))   # was: isinstance(x, int | float)
```

The diff is pure churn. Annotations elsewhere use `int | float`; the inconsistency makes the codebase harder to read and the savings are imperceptible outside hot paths.

**Correct (apply only on a measured hot path, with a named module-level tuple):**

```python
# This validator runs once per row across ~10M rows in the ETL job — profiled.
_PRIMITIVE_TYPES = (int, float, str, bool)

def is_primitive(x: object) -> bool:
    return isinstance(x, _PRIMITIVE_TYPES)
```

Caching the tuple at module scope and giving it a clear name documents the intent ("this check is hot"). Anywhere else, `isinstance(x, int | float)` is fine.

**Do not rewrite for style alone.** A diff that flips `isinstance(x, A | B)` to `isinstance(x, (A, B))` across a codebase is pure churn — you lose the visual symmetry with type annotations and gain a few microseconds on a path that runs once.

**Annotations are unaffected.** In type annotations, `X | Y` is the modern form (PEP 604). The tuple form is only relevant inside `isinstance()` / `issubclass()` calls — and only on hot paths.

### 6.6 Stream with Generators When Memory or First-Result Latency Matters

**Impact: LOW-MEDIUM (bounded memory and lazy evaluation for large or infinite sequences)**

Generators trade materialization for laziness: one value at a time, no intermediate list, caller can stop early. This is a memory and streaming rule, not "generators are categorically better." When you need every result, re-iterate, want random access, or will sort anyway, a list comprehension is often clearer and sometimes faster.

**Incorrect (materializes a multi-GB file three times for a count):**

```python
def count_errors(path: Path) -> int:
    lines = path.read_text().splitlines()                    # full file in memory
    parsed = [parse_line(line) for line in lines]            # second full copy
    matching = [p for p in parsed if p.level == "ERROR"]     # third full copy
    return len(matching)
```

**Correct (streaming — constant memory regardless of file size):**

```python
def count_errors(path: Path) -> int:
    with path.open() as f:
        return sum(1 for line in f if parse_line(line).level == "ERROR")
```

Reach for a generator when the input is large, unbounded, or the consumer can stop early (`any()`, `next()`, `break`). Reach for a list when you need `len()`, iterate more than once, need random access, or will sort the whole sequence. A generator exhausted by the first loop reading zero on the second is a real bug, not a perf issue. `itertools` (`chain`, `islice`, `takewhile`, `groupby`) yields lazily for pipelines that stay streaming.

### 6.7 Use functools.lru_cache for Pure Functions

**Impact: LOW-MEDIUM (trades memory for CPU on repeatable computations)**

When a function is pure (same input → same output, no side effects) and called repeatedly with the same arguments, `@lru_cache` caches the result so subsequent calls are free. Agents often forget this exists and either hand-roll a dict cache or eat the recomputation cost.

**Incorrect (recomputing the same answer):**

```python
def parse_version(version_str: str) -> Version:
    # called from many call sites, often with the same string
    return Version.parse(version_str)
```

If 100 call sites ask `parse_version("1.2.3")`, you parse it 100 times.

**Correct (cached):**

```python
from functools import lru_cache

@lru_cache(maxsize=256)
def parse_version(version_str: str) -> Version:
    return Version.parse(version_str)
```

First call parses and stores; subsequent calls return the cached `Version`. `maxsize` caps the cache to 256 entries (LRU eviction).

**`functools.cache` (Python 3.9+) for unbounded:**

```python
from functools import cache

@cache
def load_schema(name: str) -> Schema:
    return Schema.from_file(SCHEMA_DIR / f"{name}.json")
```

No size limit. Good when the key space is naturally small (like schema names) and entries are expensive to build.

**Requirements:**

- Arguments must be **hashable** (no mutable lists, dicts, or sets as args)
- Function must be **pure** — same inputs produce the same output
- No side effects that callers depend on happening each call

**When NOT to cache:**

- Arguments are unhashable (convert to tuple first, or use a different strategy)
- The function has meaningful side effects (logging, writes)
- The key space is unbounded and entries are large (cache grows without limit)
- The computation is cheap and the call frequency is low

**Hand-rolled caches:**

If `@lru_cache` doesn't fit (unhashable args, multi-level keys, time-based invalidation), build a module-level `dict` cache — but name it clearly and document the invalidation strategy. Uncontrolled hand-rolled caches leak memory.

**For instance methods, prefer `@cached_property`** when the "arguments" are just `self` — see `simplify-cached-property`.

### 6.8 Use set for Repeated Membership Checks

**Impact: MEDIUM (O(1) beats O(n))**

`x in some_list` scans the list every time — O(n). `x in some_set` is a hash lookup — O(1). When you're checking membership repeatedly against the same collection, the set conversion pays for itself quickly.

**Incorrect (list membership in a loop):**

```python
def filter_allowed(items: list[Item], allowed: list[str]) -> list[Item]:
    return [item for item in items if item.id in allowed]
```

For each of `len(items)` checks, `in allowed` scans the whole list. If both are 10k, that's 100M comparisons.

**Correct (convert once, check many):**

```python
def filter_allowed(items: list[Item], allowed: list[str]) -> list[Item]:
    allowed_set = set(allowed)
    return [item for item in items if item.id in allowed_set]
```

Conversion is O(n); each `in` check is O(1). Total: O(n + m) instead of O(n × m).

**When to use `frozenset`:**

Module-level constants with fixed membership — can't be modified accidentally, hashable so it can be used as a dict key:

```python
_ADMIN_ROLES: frozenset[str] = frozenset({"admin", "owner", "superuser"})

def is_admin(role: str) -> bool:
    return role in _ADMIN_ROLES
```

**When NOT to convert to set:**

- Only checking membership once (conversion costs more than the scan)
- The collection is tiny (under ~10 elements) — list scan is competitive
- Order matters and you need the list semantics

**For lookups by key (not just membership), use a dict:**

```python
# bad — scanning a list for "the one with this id"
user = next((u for u in users if u.id == target_id), None)

# good — build once, look up many
users_by_id = {u.id: u for u in users}
user = users_by_id.get(target_id)
```

Same asymptotic improvement as set membership, and you get the associated value instead of just a boolean.

## 7. Naming

**Impact: LOW-MEDIUM**

Names carry meaning. Specific over generic, consistent terminology, no type suffixes. Mostly applies to new names.

### 7.1 Avoid Redundant Type Suffixes in Names

**Impact: LOW (reduces noise when types annotate types)**

`user_list: list[User]`, `config_dict: dict[str, str]`, `name_str: str` — the suffix repeats what the type annotation already says. Python has type annotations; let them do the work. Hungarian-style suffixes "make the type clear" at the cost of restating what's already on the next token.

**Incorrect (suffix restates the type):**

```python
def filter_users(user_list: list[User], active_dict: dict[str, bool]) -> list[User]:
    name_str = user_list[0].name_str
    result_list: list[User] = []
    ...
```

Every name repeats its type. The code is harder to read because the meaningful word is buried.

**Correct (let types speak):**

```python
def filter_users(users: list[User], active_by_id: dict[str, bool]) -> list[User]:
    name = users[0].name
    result: list[User] = []
    ...
```

`users` and `active_by_id` describe what the value is for; the types describe the shape.

**Suffixes to drop:**

- `_list`, `_dict`, `_set`, `_tuple` — shape is in the type
- `_str`, `_int`, `_float`, `_bool` — primitive type is in the type
- `Value`, `Type`, `Class` — usually redundant (`UserType` vs. just `User`)

**When a type-ish suffix genuinely helps:**

- `_by_key` names signal the dict's key (`users_by_id`, `posts_by_author`)
- `_count`, `_index`, `_id` signal the semantic role, not the type
- `_bytes` / `_str` on a variable that could be either (`body_bytes` vs. `body_text`) — disambiguating two valid forms is useful

**Class names:** don't suffix with `Class`. `UserClass` is just `User`. The definition is `class User:`.

**Enum values:** keep them short and meaningful. `Color.RED` reads better than `Color.COLOR_RED`.

**Private helpers:** same rule applies. `_parse_user_dict` where the return is `dict[str, User]` — just `_parse_users`.

**Exception classes:** convention is to end with `Error` (`ValidationError`, `TimeoutError`). This is the established Python pattern and worth keeping.

### 7.2 Drop Redundant Prefixes When Context Is Clear

**Impact: LOW-MEDIUM (reduces noise and improves readability)**

When a field is accessed as `tool_config.tool_description`, the `tool_` prefix adds nothing — the class name already provides that context. Repeating the class name in every field ("just to be clear") produces noise that makes real information harder to find.

**Incorrect (prefix repeats the class context):**

```python
from dataclasses import dataclass

@dataclass
class ToolConfig:
    tool_name: str
    tool_description: str
    tool_version: str
    tool_timeout: float
```

Every access reads `config.tool_name`, `config.tool_description`. The `tool_` adds zero information.

**Correct (name without the redundant prefix):**

```python
@dataclass
class ToolConfig:
    name: str
    description: str
    version: str
    timeout: float
```

Now `config.name`, `config.description` — shorter and just as clear.

**The rule:** drop the prefix when the class, module, or variable name already establishes the context.

**Examples from real codebases:**

```python
# before → after
server.server_label       → server.label
mcp_server.mcp_version    → mcp_server.version   (or just version on the class)
user_profile.user_id      → user_profile.user_id (probably keep — "id" alone is too generic)
```

The last example is a judgment call. `user_profile.id` would be unambiguous in context, but `user_id` reads well when passing it around as a variable. Lean toward dropping when it's a *field on* a class, keep the prefix when the value *travels as* a parameter.

**When to keep a prefix:**

- The field is a **foreign key** to another entity (`user_id` on a `Post`, `author_id` on a `Comment`) — the prefix signals what it points to
- Two related fields share a type and need disambiguation (`created_at` vs. `updated_at`)
- Dropping the prefix makes the name ambiguous (`format` could mean many things; `date_format` is specific)

**Be consistent:** whatever you pick, apply it uniformly across sibling fields. `tool_name` with `description` (mixed) reads worse than either all-prefixed or all-bare.

### 7.3 Rename When Behavior Changes

**Impact: MEDIUM (prevents misleading names from hiding behavior changes)**

A function's name is a promise about what it does. When the behavior changes — wider scope, different return type, side effects added — the old name lies. Names often stay stable because "it's a smaller diff"; the cost is that every future reader has to figure out the name is wrong.

**Incorrect (name no longer matches behavior):**

```python
# v1: called only for function tools
def _call_function_tool(tool: FunctionTool, args: dict) -> Result:
    return tool.invoke(args)

# v2: extended to handle output tools too, but name unchanged
def _call_function_tool(tool: FunctionTool | OutputTool, args: dict) -> Result:
    if isinstance(tool, FunctionTool):
        return tool.invoke(args)
    return tool.build_output(args)  # wait, this isn't a "function tool"
```

Every reader now has to re-learn what `_call_function_tool` means. The name says "function tool"; the body says "any tool."

**Correct (rename to reflect the wider scope):**

```python
def _call_tool(tool: FunctionTool | OutputTool, args: dict) -> Result:
    if isinstance(tool, FunctionTool):
        return tool.invoke(args)
    return tool.build_output(args)
```

Name matches behavior again.

**Signals that a rename is due:**

- The function's scope expanded (handles more types, more cases)
- The return type changed substantively
- Side effects were added or removed
- The function's "level" changed (was a leaf, now orchestrates; was a command, now a query)

**When in-place rename is fine:**

- Private (`_`-prefixed) functions — callers are all internal, update them
- Internal helpers with a small number of call sites

**When rename needs a migration:**

- Public API — add the new name, keep the old as a deprecated alias (see `api-deprecated-aliases`)
- Widely-used internal helpers — IDE-assisted rename is safer than hand-edit

**For method renames across a class hierarchy** — use the `@override` decorator when the intent is to override, and let the checker catch stragglers:

```python
from typing import override

class MemoryToolset(Toolset):
    @override
    def list_tools(self) -> list[Tool]: ...
```

If `Toolset` renames `list_tools`, `@override` makes the subclass fail type-checking until updated.

### 7.4 Use Consistent Terminology Across Code and Docs

**Impact: MEDIUM (prevents fragmented searches and user confusion)**

When the same concept appears as `message` in one module, `last_message` in another, and `latest` in a third, readers can't grep. Pick one term per concept and use it everywhere — in code, docstrings, error messages, and external docs.

**Incorrect (same concept, three names):**

```python
# module_a.py
def get_last_message(session): ...

# module_b.py
def fetch_latest(session): ...

# module_c.py
def current_message(session): ...

# error message
raise ValueError("no recent message found")
```

A user searching for "latest message" in code finds one match; in docs, another; in error messages, a third. The concept is fragmented.

**Correct (one term, everywhere):**

```python
# everywhere
def get_latest_message(session): ...
raise ValueError("no latest message found")
# docs: "The latest message is..."
```

One word per concept. Search works.

**Choose deliberately — and write it down:**

- `latest` vs. `last` vs. `most_recent` — pick one
- `message` vs. `msg` — pick one
- `tool` vs. `function` vs. `capability` — pick one
- `user` vs. `account` vs. `member` — pick one

If the codebase has a `GLOSSARY.md` or `CONTRIBUTING.md`, list the canonical terms and their boundaries. If not, pick through current usage by grepping — whichever is most common wins.

**When different terms are genuinely different things:**

Sometimes "message" and "msg" mean different things (a full message object vs. a short string body). That's fine — but then the distinction should be explicit and documented. If you need two terms, you need two concepts.

**Refactoring legacy inconsistency:**

- Add the canonical alias first, deprecate the old
- Update docstrings and error messages in the same PR
- Don't let PRs introduce new variants (`message`, `msg`, `messageObj` in one diff) — pick one, stick to it

**Why it matters:** users grep. Docs search. Error messages end up in Stack Overflow questions. When terminology fragments, every question becomes "how do I look this up?" — and the answer gets split across three terms that mean the same thing.

### 7.5 Use Specific Parameter and Variable Names

**Impact: LOW-MEDIUM (prevents confusion when multiple instances are in scope)**

Generic names like `id`, `name`, `data`, `info` communicate nothing about the value's role. When multiple IDs or data objects share a scope, they collide. Names that convey the semantic role make call sites self-documenting.

**Incorrect (generic names — call site is ambiguous):**

```python
def transfer(id: str, id2: str, data: dict, info: dict) -> None:
    ...

transfer("u123", "t456", {...}, {...})  # which is sender, which is recipient?
```

**Correct (specific — names carry the semantic role):**

```python
def transfer(
    sender_id: str,
    recipient_id: str,
    transfer_data: TransferRequest,
    audit_info: AuditContext,
) -> None:
    ...
```

Generic is acceptable for truly generic helpers (`def first(items: list[T]) -> T`), when there's only one of the type in scope (`def render(user: User)`), or following convention (`self`, `cls`, `_`, loop indices `i` / `j` in math contexts). The red flag is ending up with `id`, `id2`, `id3` or `data`, `info`, `details`, `meta` all in the same scope — the number suffixes tell you the names aren't doing their job. In nested loops, `for user in users` beats `for x in users` once the body is more than a couple of lines.

### 7.6 Use UPPER_CASE for Module Constants

**Impact: LOW (signals immutability and public/private scope)**

Module-level values that don't change during execution are constants. The `UPPER_CASE` convention signals "don't reassign this" and is widely recognized across Python codebases. A reader seeing `default_timeout` can't tell at a glance whether it's a constant or a mutable config someone might reassign.

**Incorrect (looks like a reassignable variable):**

```python
default_timeout = 30
max_retries = 3
allowed_hosts = frozenset({"localhost", "127.0.0.1"})
```

**Correct (UPPER_CASE for constants; `_` prefix for internal):**

```python
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
ALLOWED_HOSTS = frozenset({"localhost", "127.0.0.1"})
_DEFAULT_CACHE_SIZE = 512
```

The underscore keeps internal constants out of `from module import *` and signals they're not part of the public API. Enum members and class-level constants follow the same convention (`Color.RED`, `Cache.DEFAULT_SIZE`). For machine-enforced immutability, pair with `typing.Final`:

```python
from typing import Final

DEFAULT_TIMEOUT: Final[int] = 30  # checker flags any reassignment
```

Keep `lower_case` for values that look like constants but aren't — derived from `os.environ` at import, intentionally reassignable feature flags, or test-mutable hooks. The convention is for *intentional* constants.

## 8. Imports & Structure

**Impact: LOW**

Module hygiene. Imports at the top, no import-time side effects, optional deps handled explicitly. Most items linters catch automatically.

### 8.1 Handle Optional Dependencies Explicitly

**Impact: LOW-MEDIUM (clear error messages instead of cryptic ImportError)**

When a package has optional integrations, importing the module should not require every optional dep. Handle `ImportError` at module scope with a message pointing to the install extra; raising `None`-valued placeholders produces `AttributeError` far from the root cause.

**Incorrect (silently swallowing the ImportError):**

```python
try:
    import anthropic
except ImportError:
    anthropic = None  # downstream code crashes with AttributeError later

class AnthropicProvider:
    def __init__(self):
        client = anthropic.Client()  # AttributeError: 'NoneType' has no 'Client'
```

**Correct (raise with an actionable install hint; preserve the original cause):**

```python
try:
    import anthropic
except ImportError as e:
    raise ImportError(
        "anthropic is required for AnthropicProvider. "
        "Install with: pip install 'mylib[anthropic]'"
    ) from e

class AnthropicProvider:
    ...
```

If the dep is optional at the *feature* level rather than the *module* level, defer the import into the function that needs it — users who never call it never pay the cost. Pair module-scope optional imports with a `TYPE_CHECKING` block (see `types-type-checking-imports`) when type hints should resolve without requiring the runtime dep.

### 8.2 Keep Modules Cheap to Import

**Impact: MEDIUM (faster CLIs, faster tests, faster worker startup)**

Anything at module top-level — opening files, reading env vars, building large data structures, connecting to databases, registering handlers, hitting the network — runs every time anything in that module is imported. That cost compounds across CLI cold-starts, test collection, worker pools, and serverless functions. It also makes modules hard to mock. Push side effects into functions, factories, or lazy properties that callers invoke explicitly.

**Incorrect (network call, heavy init, and env read at import):**

```python
# config.py
import requests

CONFIG = requests.get("https://config.example.com/v1").json()  # network at import
DB_URL = CONFIG["db_url"]

# embeddings.py
MODEL = SentenceTransformer("all-MiniLM-L6-v2")                # 90 MB download + GPU init

# keys.py
API_KEY = os.environ["MY_API_KEY"]                             # KeyError on import if unset
```

Importing any of these for a type or constant triggers the work. A CLI's `--help` takes seconds; offline CI breaks; reading the module docstring fails without the env var set.

**Correct (lazy — pay only when the feature runs):**

```python
from functools import cache

@cache
def get_config() -> dict[str, object]:
    return requests.get("https://config.example.com/v1").json()

@cache
def get_model() -> "SentenceTransformer":
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")

def api_key() -> str:
    key = os.environ.get("MY_API_KEY")
    if not key:
        raise RuntimeError("MY_API_KEY is required to call this API")
    return key
```

`@cache` gives you "once per process" semantics without the "every import" cost.

Fine at import time: pure-Python constants, `re.compile` for a static pattern, class and function definitions, stdlib imports, cheap registrations. Push out of import time: network/disk I/O, subprocess launches, large model loads, env-var reads that may fail, DB/queue connections, heavy third-party imports the module doesn't unconditionally use. If `python -c "import yourpackage"` takes more than ~100 ms or hits the network, something at module scope should be deferred.

### 8.3 No Duplicate Imports

**Impact: LOW (prevents confusion and redundant work)**

Two imports of the same name are either redundant (if they're identical) or a sign that a refactor left both in place. Either way, delete one. Tools flag this, but agents sometimes add a new import on top of an existing one without checking.

**Incorrect (same name imported twice):**

```python
import json
from typing import Any
from pathlib import Path

# ... later in the file, after a later edit ...
from pathlib import Path       # duplicate
from pathlib import Path as P  # different alias, same underlying import
```

The first duplicate is pure redundancy. The second is worse — now `Path` and `P` both exist in the namespace, pointing to the same class.

**Correct (one import per name):**

```python
import json
from typing import Any
from pathlib import Path
```

If two aliases are genuinely needed (very rare — usually a code-smell), pick one:

```python
from pathlib import Path  # use this name everywhere
```

**When "duplicates" are actually distinct:**

```python
from foo import bar
from foo.baz import bar as baz_bar  # different bar, aliased to avoid collision
```

These are different objects with the same name in different namespaces. Aliasing one disambiguates. This is fine — but it's *not* a duplicate; the names differ.

**Detection:**

- `ruff check --select F811` flags redefinitions
- `pyflakes` also catches these

Add to pre-commit or CI.

**Root cause:** duplicate imports usually appear after:

- Merging branches that both added the same import
- An IDE auto-import on top of an existing import
- Refactoring that copied a block without cleaning up the imports

Reviewing the imports block after any merge or mass edit catches these before they land.

### 8.4 Place Imports at the Top of the File

**Impact: LOW (makes dependencies visible at a glance)**

Imports belong at the top of the module, grouped (stdlib, third-party, local) with blank lines between groups. Inline imports inside functions hide dependencies from readers, confuse static analysis, and surprise anyone debugging a `ModuleNotFoundError` raised in the middle of a call. `ruff` / `isort` automate the grouping.

**Incorrect (imports scattered through function bodies):**

```python
def fetch_user(user_id: str) -> User:
    import requests  # hidden dependency
    response = requests.get(f"/users/{user_id}")
    return User(**response.json())

def process():
    from .helpers import validate  # easily missed
    import json                    # another one
    data = json.dumps(result)
```

**Correct (all imports at the top, PEP 8 ordering):**

```python
import json
from typing import Any

import requests

from .helpers import validate


def fetch_user(user_id: str) -> User:
    response = requests.get(f"/users/{user_id}")
    return User(**response.json())
```

Inline imports are legitimate only for: breaking circular imports (add a comment so readers don't "fix" it), deferring truly optional/heavy deps behind a runtime gate (see `imports-optional-dependencies`), or avoiding module-load-time side effects. Outside those cases, top-of-file is the rule.

### 8.5 Remove Unused Imports

**Impact: LOW (prevents accidental dependencies and reduces noise)**

Every import is a declaration of "this module depends on X." Unused imports lie about dependencies, add reading noise, risk circular imports, and mask refactoring errors — the import survives long after the only call site was deleted.

**Incorrect (imports for names that aren't used):**

```python
import json
import re
from typing import Any, Optional, Union

from .helpers import validate, format_date  # format_date never used

def compact(data: dict[str, Any]) -> str:
    return json.dumps(data, separators=(",", ":"))
```

**Correct (just what's needed):**

```python
import json
from typing import Any

def compact(data: dict[str, Any]) -> str:
    return json.dumps(data, separators=(",", ":"))
```

`ruff check --select F401` flags unused imports — wire it into pre-commit or CI. If a module intentionally re-exports names (common in `__init__.py`), use the `from .client import Client as Client` form or list them in `__all__`; both signal "intentional, not forgotten." If an import is used only in annotations, move it under `if TYPE_CHECKING:` (see `types-type-checking-imports`). Keep an otherwise-unused import only when importing it has a required side effect (plugin self-registration) — and comment it: `# noqa: F401 — registers handlers at import time`.

### 8.6 Scope Helpers and Constants to Their Usage Site

**Impact: LOW (reduces namespace pollution and clarifies intent)**

Scope tiny helpers and one-off constants near their only use. Promote a helper to module scope when it is substantial, reused, independently testable, expensive to rebuild, or part of the module's contract. Nested functions are cheap inside a small callable, but stacking nontrivial logic inside another function hurts readability and makes the helper harder to test directly.

**Incorrect (tiny one-off constant hoisted into the module namespace):**

```python
# somewhere in a 500-line module
_DEFAULT_MAX_LENGTH = 280

def summarize(text: str) -> str:
    normalized = " ".join(text.split())
    return normalized[:_DEFAULT_MAX_LENGTH]

# ... 400 more lines, no other use of _DEFAULT_MAX_LENGTH
```

A future reader sees `_DEFAULT_MAX_LENGTH` at module scope and assumes it's shared. If it isn't, that's noise.

**Correct (trivial constant local to its one caller):**

```python
def summarize(text: str) -> str:
    DEFAULT_MAX_LENGTH = 280
    normalized = " ".join(text.split())
    return normalized[:DEFAULT_MAX_LENGTH]
```

**When to promote to module scope:**

- Reused by more than one function
- Substantial enough to want its own unit tests
- Expensive to rebuild per call (compiled regex, `TypeAdapter`, precomputed table)
- Part of the module's contract (constants referenced by name, e.g., `MyClass.DEFAULT_TIMEOUT`)
- Needs to be patched in tests (module-level constants are easy to monkeypatch)

Prefer module-level over a nested `def` whenever the helper has real logic. Nested functions are appropriate for short closures or very small transforms; they stop being appropriate once the helper grows past a few lines.

**Imports follow the opposite default** (see `imports-top-of-file`): imports live at the top of the module unless there's a specific reason (optional deps, circular, expensive-to-import) to defer them.


## References

- https://docs.python.org/3/library/typing.html
- https://docs.python.org/3/library/dataclasses.html
- https://docs.python.org/3/library/exceptions.html
- https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement
- https://docs.pydantic.dev/
- https://mypy.readthedocs.io/
- https://docs.astral.sh/ruff/
- https://peps.python.org/pep-0008/
- https://peps.python.org/pep-0544/
- https://peps.python.org/pep-0604/
- https://peps.python.org/pep-0615/
- https://peps.python.org/pep-0661/
- https://peps.python.org/pep-0695/
- https://peps.python.org/pep-0702/
- https://github.com/pydantic/pydantic-ai
