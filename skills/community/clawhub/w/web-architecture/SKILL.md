---
name: web-architecture
description: Multi-agent orchestration for complex TypeScript/Next.js/Convex projects. Phased builds, functional verification, the full playbook for delegating to sub-agents without chaos.
---

# Web Architecture

Multi-agent development workflow for TypeScript/Next.js/Convex projects.

*Born from: 29 agents, 50K lines, 212 errors, 1 hard lesson*

---

## ⚠️ SUB-AGENT POLICY (READ FIRST)

### No Timeouts
**Sub-agents MUST run without timeout limits.** A 10-minute timeout that cuts off an agent mid-implementation leaves broken, partial code. Let agents finish.

### Completion Means Working, Not Compiling
**"Build passes" is necessary but NOT sufficient.**

Before marking ANY phase complete, verify:
1. **Functions actually work** — Call them, verify data flows
2. **UI actually renders data** — Not just loading spinners forever
3. **User flows complete end-to-end** — Click through, verify state changes persist
4. **Error states are handled** — Not just happy path

### The Lesson
An agent produced 15K lines of "working" code that:
- ✅ Compiled with zero TypeScript errors
- ✅ Passed `bun run build`
- ❌ Had ZERO actual functionality
- ❌ All data was mocked or hardcoded
- ❌ Every button was a no-op

**Self-grade: 5/10** — A prototype, not a product.

---

## The Core Lesson

> **Single agent with full context > Many agents with partial context**

29 parallel agents wrote 50K lines of code that didn't compile. Why?
- No schema coordination → duplicate table definitions
- No type contracts → frontend expected `user.role`, backend returned `profile.plan`
- No initialization → `npx convex dev` never ran, no generated types
- No integration checkpoints → errors discovered only at the end

**The fix:** One agent with full context rewrote the entire Convex backend in 11 minutes.

---

## When to Use Multi-Agent

✅ **Good for parallel work:**
- Marketing pages (after design system exists)
- Documentation files (independent)
- Isolated features with clear contracts

❌ **Bad for parallel work:**
- Schema design (needs single owner)
- Core type definitions (must be shared)
- Interconnected backend functions
- Component library (needs consistency)

---

## The Workflow

### Phase 0: Bootstrap (SEQUENTIAL — One Agent)

**Must complete before spawning ANY other agents.**

1. Initialize project structure
2. Initialize Convex: `npx convex dev --once`
3. Create complete `schema.ts` (ALL tables)
4. Run `npx convex dev` to generate types
5. Create `CONTRACTS.md` (all data shapes)
6. Create shared types in `lib/types.ts`
7. Verify: `bun run build` passes

**Deliverables:**
- [ ] `convex/schema.ts` — Complete, no TODOs
- [ ] `convex/_generated/` — Types generated
- [ ] `CONTRACTS.md` — API shapes documented
- [ ] `lib/types.ts` — Shared frontend types
- [ ] `bun run build` — Passes with 0 errors

---

### Phase 1: Foundation Documents (CAN BE PARALLEL)

Only spawn AFTER Phase 0 completes.

| Agent | Output | Dependencies |
|-------|--------|--------------|
| Tech Requirements | `TECH-REQ.md` | None |
| Compliance | `COMPLIANCE.md` | None |
| Design Principles | `DESIGN.md` | None |
| Coding Standards | `STANDARDS.md` | None |

**Rule:** These agents READ the schema. They do NOT modify it.

---

### Phase 2: Backend Implementation (SEQUENTIAL or CAREFUL PARALLEL)

**Option A: Single Backend Agent (Recommended)**
- One agent implements all Convex functions
- Consistent patterns, no conflicts

**Option B: Parallel with File Locks**
- Each agent owns specific files
- NO shared file writes
- Must reference CONTRACTS.md

**Functional Requirements:**
1. Test CRUD operations — Create, read, update, delete
2. Verify queries return data — Not empty arrays
3. Check mutations persist — Data survives refresh
4. Test auth guards — Protected functions reject unauthorized
5. Verify indexes work — Queries return correct filtered data

---

### Phase 3: Component Library (SEQUENTIAL)

**Single agent builds the component library.**

Why? Components reference each other. Parallel work creates duplicate components with different APIs.

**Functional Requirements:**
1. Interactive states work — Buttons trigger onClick
2. Form components submit — Not just styled divs
3. Loading/error states exist
4. Accessibility basics — Labels, ARIA, keyboard nav
5. Consistent API — All components follow same patterns

---

### Phase 4: Features & Pages (CAN BE PARALLEL)

Now safe to parallelize because schema is locked, types exist, components exist.

| Agent | Scope | Can Modify |
|-------|-------|------------|
| Admin Suite | `/app/(admin)/**` | Own files only |
| Support Portal | `/app/(support)/**` | Own files only |
| Marketing Pages | `/app/(marketing)/**` | Own files only |
| User Flows | `/app/(app)/**` | Own files only |

**Rules:**
1. Read schema, types, contracts — don't modify
2. Use existing components — don't recreate
3. Write to assigned directories only

**Functional Requirements:**
- [ ] Page loads without console errors
- [ ] Data appears (not mock/placeholder)
- [ ] Forms submit and persist data
- [ ] Can complete full user flow (create → view → edit → delete)
- [ ] Refresh preserves state

**Red flags (NOT complete):**
- `// TODO` comments in business logic
- Hardcoded arrays instead of useQuery
- onClick handlers that console.log instead of mutate
- "Coming soon" placeholders in core features

---

### Phase 5: Integration & QA (SEQUENTIAL)

1. `bun run build` (must pass)
2. `npx convex dev --once` (must pass)
3. Generate sitemap from routes
4. Route crawl & 404 check
5. Browser smoke test (all routes return 200)
6. **End-to-end flow verification**

**E2E Verification Checklist:**

Auth Flow:
- [ ] Sign up creates user in database
- [ ] Sign in authenticates and redirects
- [ ] Protected routes redirect to sign-in

Core CRUD Flow:
- [ ] Create: Form submits → record appears
- [ ] Read: List shows real data
- [ ] Update: Edit form saves → changes persist
- [ ] Delete: Remove action → record gone

---

## Directory Structure

```
project/
├── convex/
│   ├── schema.ts            # 🔒 Phase 0 only
│   ├── _generated/          # 🔒 Auto-generated
│   └── [domain].ts
├── lib/
│   ├── types.ts             # 🔒 Phase 0 only
│   └── utils.ts
├── components/
│   ├── ui/                  # Component library agent
│   └── [domain]/            # Feature agents
├── app/
│   ├── (admin)/             # Admin agent
│   ├── (app)/               # App agent
│   └── (marketing)/         # Marketing agents
└── CONTRACTS.md             # 🔒 Phase 0 only
```

🔒 = Locked after Phase 0. Agents read, don't modify.

---

## Agent Spawn Order

```
1. Bootstrap Agent (MUST COMPLETE FIRST)
   └── schema.ts, types, contracts
   
2. Doc Agents (parallel)
   ├── TECH-REQ.md
   ├── COMPLIANCE.md
   └── DESIGN.md
   
3. Backend Agent (single)
   └── All convex/*.ts functions
   
4. Component Agent (single)
   └── All components/ui/*
   
5. Feature Agents (parallel, isolated directories)
   ├── Admin Suite
   ├── Support Portal
   ├── Marketing Pages
   └── User Flows
   
6. Integration Agent (single)
   └── Final build, fixes, QA
```

---

## Anti-Patterns

❌ **Spawn all agents at once** — No coordination, duplicate work

❌ **Let agents invent types** — Use CONTRACTS.md, not imagination

❌ **Skip Phase 0** — "We'll figure out the schema later" = disaster

❌ **Parallel schema writes** — One owner only

❌ **Frontend before backend types** — Generates type mismatches

❌ **No build checkpoints** — Errors compound

---

## Related Files

- [TECH-REQ.md](./TECH-REQ.md) — Full stack specification
- [CODING-STANDARDS.md](./CODING-STANDARDS.md) — TypeScript/React/Convex patterns
- [CONTRACTS-TEMPLATE.md](./CONTRACTS-TEMPLATE.md) — API contracts template
