# Dev & Engineering (OpenClaw Optimized)

Professional engineering manual for full-stack development, TDD, and DevOps within the OpenClaw workspace.

## 1. The Iron Law of TDD
**NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.**
1. **Red**: Write a test that fails (use `exec` to run it).
2. **Green**: Write the minimal code to pass (use `edit` or `write`).
3. **Refactor**: Clean up the code while keeping the test green.

## 2. Architecture & Design
- **ADRs**: Record major decisions in `docs/adr/`.
- **Diagrams**: Use Mermaid syntax in markdown files for documentation.
- **Patterns**: Prefer "Modular Monolith" for new OpenClaw projects until scale requires microservices.

## 3. Systematic Debugging (4-Phase)
1. **Root Cause**: Use `exec` to gather logs, environment variables, and trace data flow.
2. **Pattern**: Find working vs. broken code comparisons.
3. **Hypothesis**: Formulate "If I change X, then Y should happen."
4. **Fix & Verify**: Apply the fix and run the full test suite.

## 4. Frontend & Backend
- **Frontend**: Next.js 14+ (App Router) is the preferred stack. Use `component_generator.py` (if available) or standard templates.
- **Backend**: FastAPI (Python) or Express (Node.js). Use OpenAPI/Swagger for spec-first design.
- **Database**: PostgreSQL with `prisma` or `drizzle` for type-safe migrations.

## 5. DevOps & CI/CD
- **Automation**: Use GitHub Actions for all CI/CD.
- **Security**: Always run `npm audit` or `pip audit` before new deployments.
- **Docker**: Containerize every service to ensure "Works on Ryder's machine" means "Works everywhere."

---
*Derived from Perplexity Super-Skills & Claude Code. Optimized for OpenClaw by Ryder.*
