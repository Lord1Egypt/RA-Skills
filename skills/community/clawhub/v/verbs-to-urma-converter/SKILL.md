---
name: verbs-to-urma-converter
description: Migrate RDMA verbs code to URMA API. Use this skill when user wants to convert infiniband verbs code to URMA, or during RDMA/InfiniBand migration, or when user mentions verbs APIs, ibv_*, rdma, or wants to use URMA instead of traditional RDMA. This skill handles complete migration including API mapping, data structure conversion, and URMA-specific optimizations.
---

# Verbs to URMA Migration Skill

> Version: 1.0 | URMA API Version: 25.12.0

This skill migrates RDMA Verbs (libibverbs) code to URMA (Unified Remote Memory Access) API.

## When to Use This Skill

Trigger this skill in the following situations:
- User mentions "verbs", "libibverbs", "ibv_*" functions
- User mentions "RDMA", "InfiniBand", "RoCE"
- User wants to migrate infiniband code to URMA
- User mentions "urma" and "migration", "conversion", "port", "translate"
- User wants to convert RDMA application to use URMA

---

## Migration Hard Constraints (Applicable Throughout)

The following constraints apply throughout the entire migration; no phase may violate them:

1. **Original files are immutable** — All output goes to `urma_output/`, preserving original directory structure; original files must not be modified
2. **4 phases cannot be skipped** — Phase 4 catches runtime semantic errors that compilation cannot detect; skipping leads to resource leaks, logic errors, etc.
3. **System header files are highest authority** — API signatures, type definitions use `urma_api.h` / `urma_types.h` as authority; when conflicts with reference documents, use header files
4. **Structs must be zero-initialized** — Use `{0}` or `{.field = value}` for initialization; uninitialized fields cause undefined behavior
5. **Verification cannot be skipped** — Check patterns/pitfalls item by item for each file; FAIL cannot be left behind
6. **Cannot proceed without header files** — Without authoritative API source, Agent will fabricate non-existent functions; must find header files first

### URMA vs Verbs Overview

| RDMA Verbs Concept | URMA Equivalent |
|---|---|
| PD (Protection Domain) | Implicit in URMA |
| MR (Memory Region) | `urma_target_seg_t` via `urma_register_seg()` |
| CQ (Completion Queue) | `urma_jfc_t` via `urma_create_jfc()` |
| QP (Queue Pair) | `urma_jetty_t` or `urma_jfs_t` + `urma_jfr_t` |
| SRQ (Shared Receive Queue) | `urma_jfr_t` with `share_jfr=1` flag |
| Completion Channel | `urma_jfce_t` via `urma_create_jfce()` |
| LID + GID | `urma_eid_t` (16-byte endpoint ID; LID removed) |
| QPN | JPN (Jetty Pair Number) |
| PSN | PSN (Packet Sequence Number) |

### Quick Reference (Full list in `mapping.md §1`)

| Verbs | URMA |
|-------|------|
| `ibv_open_device()` | `urma_create_context()` |
| `ibv_reg_mr()` | `urma_register_seg()` |
| `ibv_create_cq()` | `urma_create_jfc()` |
| `ibv_create_qp()` | `urma_create_jetty()` |
| `ibv_modify_qp(RTR/RTS)` | `urma_import_jetty()` + `urma_bind_jetty()` |
| `ibv_post_send()` | `urma_post_jetty_send_wr()` |

---

## Migration Workflow

### Phase 1: Preparation

**Goal**: Understand source code and establish complete API mapping.

**Mandatory deliverables** (must be produced at phase end):
1. Source file classification list: which contain verbs APIs (need conversion), which don't (copy as-is)
2. Verbs API list and URMA mapping table: handling method for each API (replace/delete/pending confirmation)
3. Transport mode and connection model judgment (RC/RM/UM, import+bind, etc.)
4. User confirmation (present above deliverables; can proceed to Phase 2 only after permission)

**Must complete** (hard constraints during phase):
- System header files (urma_api.h / urma_types.h / urma_opcode.h) found and read as authoritative source
  - Common location: `/usr/include/ub/umdk/urma/`
  - If not found: ask user to install or provide path; do not continue without header files
- Each Verbs API has been looked up in mapping.md for equivalent
- APIs that cannot be mapped have been confirmed for deletion in mapping.md §No URMA Equivalents, or marked as pending confirmation
- URMA complete resource lifecycle understood (refer to patterns.md §1)

**Reference consultation path** (recommended, not mandatory):
- patterns.md §1 → understand URMA complete lifecycle
- mapping.md → look up mapping item by item
- pitfalls.md → understand common error overview

---

### Phase 2: Conversion

**Goal**: Create converted code in `urma_output/` directory; original files remain unchanged.

**Mandatory deliverables** (must be produced at phase end):
1. `urma_output/` directory containing all converted files, preserving original directory structure
2. Verification results for each file (see verification requirements)
3. Mapping item execution traceability for each file (see mapping traceability)
4. Project-level mapping traceability summary (see mapping traceability)
5. Build config updated

**Conversion constraints** (must be satisfied):
- All converted code goes to `urma_output/`; original files must not be modified
- Header type definition changes must be consistent with all source files referencing it
- Build files (Makefile) updated after all code files are converted
- Files with most Verbs APIs should be converted first to discover mapping issues early

**Each file's conversion content**:
- `#include <infiniband/verbs.h>` → `#include <ub/umdk/urma/urma_api.h>`
- Verbs API calls → URMA equivalents (consult mapping.md); calls with no equivalent deleted directly (consult mapping.md §No URMA Equivalents)
- Struct field name updates (e.g., `wc.qp_num` → `cr.local_id`)
- Enum value updates (e.g., `IBV_MTU_1024` → `URMA_MTU_1024`)
- Connection establishment flow updates (consult mapping.md §Connection Establishment Decision Tree; choose correct operation by RC/RM/UM)
- Address exchange format updates (`lid:qpn:psn:gid` → `jpn:eid`; consult mapping.md §Address Exchange Format Decision)
- Cleanup order updates (consult mapping.md §Cleanup Order Decision; choose correct order by transport mode)

**Build config must be updated**:
- Link libraries: `-libverbs` → `-lurma -lurma_common`
- Header file paths: `infiniband/verbs.h` → `ub/umdk/urma/urma_api.h`
- If original project has no Makefile, create one (link `-lurma -lurma_common`)

#### Mapping Traceability (Preventing Mapping Item Omissions)

> **Problem**: After Phase 1 produces mapping plan, Phase 2 file-by-file conversion easily omits non-core path mapping items (e.g., `ibv_create_comp_channel → urma_create_jfce`), because verification only compares patterns/pitfalls (general knowledge), not Phase 1 mapping plan (project-specific checklist).

**Two-layer traceability mechanism**:

**File-level traceability** (verify immediately after each file is converted):
- Verify each Verbs API directly appearing in that file has been handled
- Must not omit: calls in conditional branches, helper functions, initialization/cleanup paths
- Verification results become part of that file's verification

**Project-level traceability** (aggregate verification after all files are converted):
- Verify each item in Phase 1 mapping table has been handled in at least one file
- No mapping items allowed in "unprocessed" state
- Output traceability summary: status of each mapping item (converted/deleted) and file where handled

---

#### Verification Requirements (Must Be Satisfied After Each File Conversion)

**Must verify**:
- Each chapter of patterns.md: does this file's code conform to this pattern
- Each chapter of pitfalls.md: did this file's code step into this pitfall
- Numbering: P-XX corresponds to patterns.md chapter numbers, PIT-XX corresponds to pitfalls.md chapter numbers
- File-level mapping traceability: has each Verbs API in this file been handled

**Must achieve state**:
- Each item judged as **conforming** (pattern matched / pitfall avoided) or **not applicable** (N/A, reason required, e.g., "this file has no RDMA operations")
- **Non-conforming items** (FAIL) must be fixed and re-verified; cannot be left behind
- **Must not skip any chapter** — iterate through reference file's actual chapter numbers
- Numbering comes from reference files' actual chapters; new chapters in reference files automatically included

**Output method**: List verification results and judgment basis for each chapter item by item, ensuring auditable. Cannot substitute item-by-item checks with general statements like "verified".

---

### Phase 3: Verification

**Goal**: Compile, link, and verify converted code.

**Mandatory deliverables** (must be produced at phase end):
1. Compilation success (no errors)
2. Linking correct (depends on `liburma.so` and `liburma_common.so`)

**Must complete** (hard constraints during phase):
- Compilation passes, no undefined references, type mismatches, or other errors
- Linking verification confirms dependency on correct URMA library
- Compilation errors investigated and fixed

**Common compilation errors and troubleshooting directions**:

| Error Type | Possible Cause | Troubleshooting Direction |
|------------|----------------|---------------------------|
| Undefined reference | Wrong API name | Check correct function signature in urma_api.h |
| No member named 'jetty_id' | Wrong field name | `cr.local_id`, not `cr.jetty_id` (see mapping.md) |
| Macro redefinition | Macro already exists in header | Delete self-defined macros |
| Type mismatch | Wrong parameter type | Match exact signature in urma_api.h |
| Missing header file | Correct header not included | Add `#include <ub/umdk/urma/urma_api.h>` |

---

### Phase 4: Review and Optimization (Mandatory)

**Goal**: Check cross-file semantic issues from project perspective; verify correctness beyond compilation.

> **Why cannot look at single file only**: Resource lifecycle spans files (created in A, destroyed in B), type declarations modified in .h but .c references not synced, Verbs residue may only appear in "copied as-is" utility files — these are issues that single-file perspective cannot discover.

**Mandatory deliverables** (must be produced at phase end):
1. Cross-file consistency confirmed: header type definitions and source file references synced, shared variable declarations consistent
2. Resource lifecycle completeness: each URMA resource's create→destroy chain complete without omissions
3. Verbs residue zero: no `ibv_*` / `verbs.h` / `infiniband` references in `urma_output/`
4. Runtime semantic correctness: import/unimport pairing, wait/ack pairing, cleanup paths complete
5. User-confirmed review summary

**Must complete** (hard constraints during phase):

1. **Header→Source consistency**: For type definition changes in .h, confirm all .c files referencing that .h have been updated; no residual old types
2. **Shared variable consistency**: For cross-file shared variables (e.g., global `ibv_cq *g_cq` → `urma_jfc_t *g_jfc`), confirm .h declarations and all .c uses are consistent
3. **Resource ownership and lifecycle**: Trace each URMA resource (context, jfc, jfr, jetty, tseg, tjetty, import_seg) to identify which file creates and which destroys; confirm create→destroy chain complete without omissions
4. **Verbs residue scan**: Confirm no Verbs residual references in `urma_output/`
5. **Re-examine N/A items**: Items marked N/A in Phase 2 may apply from cross-file perspective (e.g., single file has no RDMA code, but other files trigger import_seg requirements)
6. **Cleanup path completeness**: Does each success path have corresponding complete cleanup sequence (unbind→unimport→delete)
7. **Resource leak check**: Does each `urma_import_*` have corresponding `urma_unimport_*`; does each `urma_wait_jfc` have `urma_ack_jfc`

Fix and recompile until clean.

#### Phase 4 Checkpoint

Present to user:
- Issues discovered and fixed in Phase 4
- Residual risks (known issues that cannot be resolved during migration)
- New knowledge (new mappings/patterns/pitfalls discovered during migration)
- Whether to add new knowledge to reference files (requires user consent)

---

## Output Format

**Mandatory**: All converted code goes to new directory. Original files remain unchanged.

**Final output structure**:
```
project/
├── (original files - unchanged)
└── urma_output/
    ├── (converted .c files)
    ├── (converted .h files)
    ├── (copied non-Verbs files as-is)
    └── Makefile
```

---

## Contributing New Knowledge

After successful migration, you may discover new mappings, patterns, or pitfalls.

**Steps**:

1. **Collect new discoveries**:
   - New API mappings (verbs → urma)
   - New struct field mappings
   - New code patterns
   - New pitfalls

2. **Present discoveries to user**:
   ```
   I discovered the following new information during migration:

   [List discoveries clearly]

   Should I add these to the reference files?
   ```

3. **If user agrees**:
   - **New API mapping**: Add to `references/mapping.md`
   - **New code patterns**: Add to `references/patterns.md`
   - **New pitfalls**: Add to `references/pitfalls.md`

4. **If user refuses**:
   - Skip updating reference files

This ensures the skill improves with actual usage, but only with user consent.

---

## Reference Files Overview

| File | Purpose | Agent Usage Scenario |
|------|---------|---------------------|
| `mapping.md` | Verbs → URMA lookup table | "What is X's URMA equivalent?" |
| `patterns.md` | Complete code patterns | "Show me how to write X" |
| `pitfalls.md` | Known issues and fixes | "Why did X fail?" |
| `urma_sample.md` | Complete working example (~1280 lines) | Read on demand only when patterns.md is not detailed enough |

**Recommended reading order**:
1. `mapping.md` - Learn API equivalents
2. `patterns.md` - View complete working code
3. `pitfalls.md` - Avoid common errors
4. `urma_sample.md` - Read only when complete reference implementation needed (~1280 lines, load on demand)