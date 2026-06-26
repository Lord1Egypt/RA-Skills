---
title: Avoid Redundant Type Suffixes in Names
impact: LOW
impactDescription: reduces noise when types annotate types
tags: naming, types, conventions
---

## Avoid Redundant Type Suffixes in Names

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
