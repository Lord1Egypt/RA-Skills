---
title: Create Explicit Variants Instead of Mode Flags
impact: MEDIUM
impactDescription: eliminates conditional-logic sprawl
tags: data, api, architecture, variants
---

## Create Explicit Variants Instead of Mode Flags

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
