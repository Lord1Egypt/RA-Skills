# Pattern 1: Tool Wrapper

## Core Purpose

Inject domain-specific expertise for particular libraries/frameworks into the Agent, **load on-demand**, without occupying everyday conversation context.

## Use Cases

- Team internal coding conventions
- Framework best practices (FastAPI/React/Verilog)
- API usage conventions
- Domain-specific terminology

## Directory Structure

```
skills/api-expert/
├── SKILL.md
└── references/
    └── conventions.md
```

## SKILL.md Template

```markdown
---
name: api-expert
description: FastAPI development best practices. Activates when users build, review, or debug FastAPI applications, REST APIs, or Pydantic models.
metadata:
  pattern: tool-wrapper
  domain: fastapi
  trigger-keywords: [fastapi, pydantic, REST API, endpoint, dependency injection]
---

You are a FastAPI development expert. Apply the following conventions to user's code or questions.

## Core Conventions

When user requests involve FastAPI, **must** load `references/conventions.md` to get complete convention list.

## When Reviewing Code
1. Load convention file
2. Check user code against each convention
3. For each violation: cite specific rule + provide fix suggestion

## When Writing Code
1. Load convention file
2. Strictly follow each convention
3. Add type annotations to all function signatures
4. Use Annotated style for dependency injection

## Example Output Format

```python
# ❌ Wrong example
@app.get("/users")
def get_users():
    return db.query(User).all()

# ✅ Correct example
@app.get("/users", response_model=list[UserSchema])
async def get_users(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> list[UserSchema]:
    result = await db.execute(select(User))
    return result.scalars().all()
```
```

## references/conventions.md Template

```markdown
# FastAPI Team Conventions v1.0

## 1. Project Structure
- Use `src/` layout
- Split routes by feature module: `routes/users.py`, `routes/items.py`
- Schema definitions in `schemas/` directory

## 2. Async Conventions
- All I/O operations must use async/await
- Database sessions use AsyncSession
- Prohibit calling synchronous blocking methods in async functions

## 3. Error Handling
- Use HTTPException to throw standard status codes
- Custom exception handlers registered centrally in `exceptions.py`
- Error responses include: `detail`, `error_code`, `timestamp`

## 4. Dependency Injection
- Database connections, authentication, logging all use Depends()
- Dependency function naming: `get_xxx()`
- Use Annotated[Type, Depends(func)] style

## 5. Pydantic Models
- All requests/responses must be wrapped with Schema
- Prohibit returning ORM objects directly
- Use model_config = ConfigDict(from_attributes=True)

## 6. Testing Conventions
- Use pytest + httpx.TestClient
- At least one test per endpoint
- Mock external dependencies, don't rely on real database
```

## Activation Condition Design

Specify trigger keywords in `description`:

```yaml
description: >
  FastAPI development best practices.
  Activation words: fastapi, pydantic, REST API, endpoint, dependency injection,
  routes, schema, Depends, HTTPException, async
```

## Pros & Cons

| Pros | Cons |
|-----|------|
| Load on-demand, saves tokens | Depends on keyword matching accuracy |
| Conventions maintained independently, easy to update | Multiple Tool Wrappers may conflict |
| Combinable (activate multiple simultaneously) | Needs clear trigger word design |

## Variants

### Variant A: Multi-Convention Switching

```markdown
Load corresponding conventions based on tech stack user mentions:
- FastAPI → `references/fastapi-conventions.md`
- Django → `references/django-conventions.md`
- Flask → `references/flask-conventions.md`
```

### Variant B: Team-Specific Conventions

```markdown
You are a [Company Name] backend development assistant.
**Must** prioritize internal conventions in `references/team-conventions.md`,
then reference general best practices.
```

---

## Checklist

- [ ] `description` contains clear trigger keywords
- [ ] `references/` directory exists with concrete content
- [ ] SKILL.md clearly explains when to load conventions
- [ ] Has correct/incorrect comparison examples
- [ ] Conventions can be updated independently without modifying SKILL.md
