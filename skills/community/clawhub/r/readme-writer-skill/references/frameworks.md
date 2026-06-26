# README Patterns: Code Framework Repositories

Based on analysis of: Express, FastAPI, Gin, NestJS, Laravel, SQLModel

Framework READMEs serve developers who will build *on top of* the framework. The README needs to communicate design philosophy, show a compelling quick-start, and build confidence that the framework is well-maintained and used in production.

---

## Structure Template

```
1. Centered logo
2. Tagline (one sentence)
3. Badges (build, version, license, downloads)
4. Brief description + philosophy
5. Key features (bulleted list)
6. Quick install command
7. Minimal "Hello World" example
8. Progressive examples (optional, for complex frameworks)
9. Performance benchmarks (especially for high-performance frameworks)
10. Sponsors / backers (if applicable)
11. Social proof (companies using it, testimonials)
12. Documentation link
13. Community (Discord, forum, Stack Overflow tag)
14. Contributing
15. License
```

---

## What Makes Framework READMEs Work

### 1. The Minimum Viable Example — Fast
The single most important thing in a framework README is getting to a runnable example quickly. The faster someone can paste your "Hello World" and see it work, the more likely they are to adopt your framework.

**Rule**: The first code example should be ≤15 lines and should be complete (imports, initialization, route/function, and start command).

```python
# FastAPI — first example is 13 lines
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

```go
// Gin — first example includes full main.go
package main

import "github.com/gin-gonic/gin"

func main() {
    r := gin.Default()
    r.GET("/ping", func(c *gin.Context) {
        c.JSON(200, gin.H{"message": "pong"})
    })
    r.Run()
}
```

Express and Gin show the full runnable first example in the README. NestJS and Laravel defer to docs.

### 2. Philosophy / Design Principles
Frameworks have opinions about how code should be written. Make those opinions clear:

```markdown
## Philosophy

Express is designed to be minimal and flexible. It provides a thin layer of fundamental
web application features, without obscuring Node.js features you already know.

```

```markdown
## Why Gin?

Gin uses a custom high-performance HTTP router (httprouter) and custom serialization.
The framework is opinionated about performance — we believe fast responses are more
valuable than magic conventions.
```

This helps developers self-select: if they share the framework's philosophy, they're more likely to be happy with it long-term.

Patterns:
- **Express**: "Minimal and flexible, doesn't obscure Node.js"
- **NestJS**: "Progressive, opinionated architecture for scalable apps"
- **Laravel**: "Expressive, elegant syntax that emphasizes developer happiness"
- **FastAPI**: "Fast to learn, fast to code, fast to run"

### 3. Performance Benchmarks
For frameworks where performance is a selling point (especially Go, Rust, compiled languages), include benchmarks:

```markdown
## Benchmarks

Gin runs as fast as raw net/http in most scenarios.

| Framework | Requests/sec | Latency (avg) |
|---|---|---|
| **Gin** | 68,000 | 0.59ms |
| Echo | 62,000 | 0.65ms |
| Fiber | 71,000 | 0.56ms |
| net/http | 72,000 | 0.55ms |

*Tested on: MacBook Pro M2, Go 1.22, wrk benchmark tool*
```

Gin's README includes a full 26-framework comparison table. This is a primary reason Go developers choose Gin.

For Python/Node.js frameworks, performance claims should be more measured or link to third-party benchmarks (FastAPI links to TechEmpower).

### 4. Social Proof
Frameworks succeed when well-known companies use them. Showcase this:

**Testimonials** (FastAPI approach):
```markdown
## What Developers Are Saying

> "If you are looking to learn one modern framework for building REST APIs in Python,
> FastAPI is the best I've seen."
> — Ines Montani, Explosion AI

> "We've been using FastAPI for our production systems at Netflix."
> — Netflix Engineering
```

**Production Usage** (Gin approach):
```markdown
## Used in Production

- [Project A](https://github.com/...) — description
- [Company B](https://company.com) — what they built
```

**Download/Star count badges** are also a form of social proof.

### 5. Sponsors Section
Mature framework READMEs typically have a sponsors section. This signals financial sustainability:

```markdown
## Sponsors

This project is maintained with the support of our sponsors.

### Gold Sponsors
<a href="https://company.com"><img src="logo.png" width="200"></a>

### Silver Sponsors
...

[Become a sponsor](https://github.com/sponsors/owner) — helps fund development
```

NestJS has the most elaborate sponsor section (Principal / Gold / Silver / Bronze). Express is minimal. Some (Laravel) have none.

### 6. Multi-Language Documentation
For globally popular frameworks, link to translated docs:

```markdown
## Documentation

- 🇺🇸 [English](https://docs.example.com)
- 🇨🇳 [中文](https://docs.example.com/zh)
- 🇰🇷 [한국어](https://docs.example.com/ko)
- 🇯🇵 [日本語](https://docs.example.com/ja)
- 🇵🇹 [Português](https://docs.example.com/pt)
```

NestJS, Gin, and FastAPI all do this. It significantly expands the addressable developer community.

### 7. Progressive Example Complexity
For feature-rich frameworks, build from simple to complex:

```markdown
## Examples

### Basic route
```python
@app.get("/")
def home():
    return "Hello World"
```

### With path parameters
```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"id": user_id}
```

### With request body and validation
```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str

@app.post("/users/")
def create_user(user: User):
    return user
```
```

SQLModel uses this pattern effectively — starting with a SQL table concept, then a Python class, then CRUD operations.

### 8. Ecosystem / Middleware
For frameworks with plugin/middleware ecosystems:

```markdown
## Ecosystem

Official packages: `@myframework/auth` • `@myframework/cors` • `@myframework/cache`

Community packages: [middleware list](https://github.com/owner/awesome-myframework)

Related tools: [CLI generator](link) • [VS Code extension](link) • [DevTools](link)
```

Express links to its GitHub organization for middleware. NestJS has a rich first-party package ecosystem listed in docs.

---

## Section-by-Section Examples

### Complete Quick Start Block
```markdown
## Quick Start

### Install

```bash
pip install myframework
```

### Create your first app

Create `main.py`:
```python
from myframework import App

app = App()

@app.route("/")
def hello():
    return {"message": "Hello World!"}
```

### Run

```bash
myframework dev main.py
```

### Test it

```bash
curl http://localhost:8000/
# {"message": "Hello World!"}
```

Visit http://localhost:8000/docs for the **interactive API documentation**.
```

### Philosophy Block
```markdown
## Design Philosophy

**Convention over Configuration**: sensible defaults that work for 90% of cases.
**Batteries included**: everything you need is in the core package.
**Progressive disclosure**: simple things are simple, complex things are possible.
```

### Dependency / Requirements Block
```markdown
## Requirements

- Python 3.8+
- Starlette 0.27+
- Pydantic 2.0+

```bash
pip install "myframework[all]"  # Install with all optional dependencies
```
```

---

## Tone & Voice

Framework READMEs tend to be:
- **Confident and opinionated**: the framework has made choices, and is proud of them
- **Developer-centric**: assume technical sophistication, focus on DX (developer experience)
- **Long-term focused**: stability, migration guides, and release cycles matter
- **Community-aware**: frameworks live and die by adoption; welcoming tone matters

FastAPI's tone is enthusiastic but grounded — it backs claims with benchmarks and testimonials. Express is minimal and understated — it lets the ecosystem speak. NestJS is formal and enterprise-focused.

---

## Things to Include Based on Framework Maturity

**New framework (<1 year old)**:
- Why this vs existing alternatives
- Roadmap / current status
- Easy contribution path (good first issues)

**Established framework (1-5 years)**:
- Performance benchmarks vs established players
- Migration guide if API is still changing
- Growing ecosystem/integration list

**Mature framework (5+ years)**:
- Migration guides between major versions
- Long-term support statements
- Enterprise support options
- Governance/foundation information

---

## Common Mistakes to Avoid

- ❌ Assuming developers will "just read the docs" without a Quick Start in the README
- ❌ No runnable first example — always show code
- ❌ Performance claims without evidence — link to benchmarks or include a table
- ❌ Missing version compatibility information — Python 3.x? Node 18+?
- ❌ No mention of how to get help — Stack Overflow tag, Discord, GitHub Discussions
- ❌ Dense feature list without examples — show, don't just list
