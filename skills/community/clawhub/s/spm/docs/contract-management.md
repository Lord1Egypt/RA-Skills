# Contract Management — Single Source of Truth

This document provides practical guidance for using the OpenAPI contract-first workflow in SPM projects.

---

## Why Contract-First?

- **Eliminates drift**: Backend and frontend share the same type definitions
- **Documents API automatically**: The spec is the source of truth for docs
- **Enables safe refactoring**: Change the spec → regenerate → compiler tells you what breaks
- **Facilitates testing**: Examples in the spec can be used for mock servers

> **Note:** Contract management is an **optional Phase 2 enhancement**. SPM does not require an API spec. Enable it only if your project has API contracts to manage.

---

## Project Structure

```
your-project/
├── api/
│   ├── openapi.yaml         # ⭐ 唯一真实来源 — 编辑这里
│   ├── examples/            # 请求/响应示例 JSON（供测试、文档）
│   │   └── project-response-200.json
│   └── generated/           # 自动生成的文件（gitignore 或提交）
│       ├── api-types.ts            → 后端用
│       └── client/                 → 前端用
├── scripts/
│   ├── generate.sh          # 从 spec 生成代码
│   └── validate_contract.sh # 验证代码与 spec 同步
└── src/
    ├── server/
    │   └── generated/       # 软链或复制到 api/generated/
    └── client/
        └── src/api/generated/
```

---

## Workflow

### 1. Define or Update API in `api/openapi.yaml`

Edit the OpenAPI 3 spec. Use the provided template as a starting point. Common operations:

- Add a new endpoint: add a `paths:/your-endpoint` block
- Add a new schema: add to `components/schemas/`
- Reference schemas with `$ref: '#/components/schemas/YourSchema'`

### 2. Generate Code

```bash
./scripts/generate.sh
```

This:
- Uses `npx openapi-typescript` to generate TypeScript types for the backend
- Uses `npx openapi-typescript-codegen` to generate a fetch-based client for the frontend
- Optionally builds HTML docs to `docs/API.html` (if `redoc-cli` is installed)

### 3. Implement

**Server route example** (`src/server/routes/projects.ts`):

```typescript
import type { components } from '../generated/api-types';

type Project = components['schemas']['Project'];

export async function handleGetProjects(req: Request): Response {
  const projects = await db.projects.findAll();
  return Response.json({ projects, total: projects.length });
}

export async function handleCreateProject(req: Request): Response {
  const body = await req.json();
  // Validate against generated types
  const project = await db.projects.create(body);
  return Response.json(project, { status: 201 });
}
```

**Client usage** (`src/client/src/api.ts`):

```typescript
import { Api } from '@/api/generated/client';

const api = new Api({ baseUrl: import.meta.env.VITE_API_BASE_URL });

async function loadProjects() {
  const res = await api.projects.list({ status: 'active' });
  return res.data.projects; // fully typed
}

async function createProject(name: string) {
  return api.projects.create({ name });
}
```

### 4. Keep Contract in Sync

Before committing or opening a PR, run:

```bash
./scripts/validate_contract.sh
```

If generated files are stale:
```
✗ Server types are stale (older than spec)
  Run ./scripts/generate.sh to update.
```

Fix by re-running `generate.sh` and committing the updated generated files.

---

## CI Enforcement

Add to your GitHub Actions workflow (`.github/workflows/contract.yml`):

```yaml
name: Validate API Contract
on: [pull_request]
jobs:
  contract:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
      - name: Validate contract
        run: ./scripts/validate_contract.sh
```

This blocks PRs that modify the API without updating the spec.

---

## Tips

- **Version your API**: Add `info.version` in `openapi.yaml` and bump it on breaking changes.
- **Use examples**: Populate `examples` in schema properties; they appear in generated docs and help testing.
- **Generate once, commit**: The generated files should be committed to the repository. Do **not** add `generated/` to `.gitignore`. This ensures consumers don't need to run generators.
- **Schema reuse**: Define common patterns (timestamps, pagination, errors) in `components/schemas/` and `$ref` them.
- **Don't hand-write types**: If you find yourself writing an interface that already exists in `api-types.ts`, you're drifting. Delete it and use the generated one.

---

## Troubleshooting

**Q: `generate.sh` fails with "Cannot find module 'openapi-typescript'"**  
A: The script uses `npx` to run generators without global install. Ensure you have Node.js 18+.

**Q: Generated types have `any` in places**  
A: Your OpenAPI spec may have loose types (`{}` or no `type`). Add explicit types (`type: object`, `properties`, `required`).

**Q: I need to add a custom method not in the spec**  
A: That's fine — client libraries can have hand-written wrappers around the generated core. Keep the generated code untouched; write custom code in separate files.

**Q: Should I edit generated files?**  
A: **Never**. Generate → commit → if you need to tweak, fix the spec, then regenerate.

---

## Advanced: JSON Schema Alternative

If OpenAPI feels heavy, you can use JSON Schema directly:

1. Place schemas in `schemas/` (e.g., `task.json`, `project.json`)
2. Use `json-schema-to-typescript` CLI to generate `.ts` files
3. Write your own small fetch wrapper; use schemas for runtime validation with `ajv`

The principle remains: **one source, generate everywhere**.
