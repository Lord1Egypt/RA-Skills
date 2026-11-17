# Modeling Data — dict, dataclass, NamedTuple, pydantic

The recurring decision is not "which is best" but "where is the boundary": validate untrusted input once at the edge, then carry typed objects the rest of the way.

## Choosing

| Situation | Use | Why not the others |
|---|---|---|
| JSON in flight, shape not yours | plain `dict` + `TypedDict` for the annotation | No runtime cost; a class here just re-serializes |
| Internal record, mutable, no validation needed | `@dataclass` | The default. Free `__init__`, `__repr__`, `__eq__` |
| Value object used as a dict key or in a set | `@dataclass(frozen=True)` | Frozen generates `__hash__`; a mutable record must not be hashable (`classes.md`) |
| Millions of small records | `@dataclass(slots=True)` or `NamedTuple` | No per-instance `__dict__` (`performance.md`) |
| Tuple-compatible, unpacked by position | `NamedTuple` | Adding a field silently breaks `a, b = rec` downstream — accept that cost knowingly |
| Untrusted input: HTTP body, config file, CSV row | `pydantic` (or attrs with validators) | Dataclasses do not validate; a `str` where you declared `int` sails straight through |
| Closed set of values | `enum.Enum` / `StrEnum` (`python >=3.11`) | A bare string constant has no exhaustiveness checking |
| Behavior-rich object with invariants | a plain class | Dataclasses expose every field as public state |
| Anything else | `@dataclass` | Start there and move outward when a specific need appears |

## Dataclass Details That Bite

- Mutable defaults raise for `list`/`dict`/`set` — and pass silently for any other mutable type, sharing one instance across every object. `field(default_factory=...)` for anything mutable (`classes.md`).
- `frozen=True` gives hashability and safety, and blocks `__post_init__` from assigning: use `object.__setattr__(self, "x", v)` for derived fields.
- `kw_only=True` (`python >=3.10`) solves the inheritance failure where a base with defaults makes a child's required field a `TypeError` at class creation. It also stops long positional constructor calls from silently swapping two same-typed fields.
- `compare=False` on volatile fields (timestamps, ids) so equality means what the domain means. `repr=False` on secrets and giant payloads — the repr ends up in logs and tracebacks (`security.md`).
- `__post_init__` for derived values and cheap invariant checks; it is not validation of untrusted input, because it runs after the object exists.
- `slots=True` (`python >=3.10`) breaks `functools.cached_property` and any late attribute assignment — that is the trade, and it is usually worth it for large collections.
- `asdict()` recurses through nested dataclasses and deep-copies; for a shallow view use `dataclasses.replace` or build the dict yourself in hot paths.

## Enums

- `StrEnum` (`python >=3.11`) members ARE strings, so JSON and database round-trips work without conversion. A plain `Enum` member is not equal to its value — `Color.RED == "red"` is False, and that comparison silently failing is the most common enum bug.
- Members are singletons: `is` comparison works and is the idiomatic form.
- `auto()` for values that carry no meaning; explicit values whenever they are persisted, because a reordering must not change what is in the database.
- `Flag` for bit sets; `enum.member`/`nonmember` when you need a class attribute that is not a member.

## Validation At The Boundary

```python
class OrderIn(BaseModel):          # pydantic v2, at the HTTP/config/file edge only
    id: int
    email: EmailStr
    created: datetime

def handle(payload: dict) -> Order:
    data = OrderIn.model_validate(payload)    # raises ValidationError with a field path
    return Order(id=data.id, email=data.email, created=data.created)   # dataclass inside
```

- Validate once, at the edge. Pydantic models threaded through every internal call re-validate on each construction and couple the domain to the library — cost with no new safety.
- Pydantic v2 coerces by default: `"1"` becomes `1`, `"true"` becomes True. `model_config = ConfigDict(strict=True)` when the wire format is supposed to be exact.
- v1 → v2 renames: `parse_obj`→`model_validate`, `.dict()`→`.model_dump()`, `.json()`→`.model_dump_json()`, `@validator`→`@field_validator`, `Config` class → `model_config`. Mixing v1 and v2 idioms in one model fails in confusing ways.
- `model_dump(mode="json")` produces JSON-safe primitives (datetimes as strings); plain `model_dump()` keeps Python objects and will fail in `json.dumps` (`files.md`).
- Aliases: `Field(alias="camelCase")` plus `populate_by_name=True` so internal code can use snake_case and the wire keeps its shape.
- Environment and config files: `pydantic-settings` or an explicit parse function — never `os.environ` reads scattered through modules (`cli.md` precedence order).

## Serialization Round-Trips

- `json.dumps` refuses `datetime`, `Decimal`, `set`, `bytes`, and dataclasses. Define ONE `default=` function per project and use it everywhere; ad-hoc conversions at each call site drift apart (`files.md`).
- Dict keys are strings after a JSON round-trip — integer keys come back as `"1"`.
- `Decimal` must cross as a string to stay exact; a float conversion for JSON reintroduces the error the Decimal existed to avoid (`types.md`).
- Enum values, not names, go on the wire; store the value that the database and other services already agreed on.

## Schema Evolution

- Adding a field: optional with a default, always. A required new field breaks every producer that has not deployed yet.
- Removing a field: stop writing it, wait for consumers, then delete. Two deploys, not one.
- Never reuse a name with a new meaning — old rows and old clients keep the old semantics forever. New name, new field.
- Version the payload (`"v": 2`) as soon as more than one service reads it; the alternative is guessing from which keys are present.
