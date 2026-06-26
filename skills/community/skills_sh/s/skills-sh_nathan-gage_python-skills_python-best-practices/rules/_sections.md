# Sections

This file defines all sections, their ordering, impact levels, and descriptions.
The section ID (in parentheses) is the filename prefix used to group rules.

Section impact is a typical-case label. Individual rules range one level above or below the section — check each rule's frontmatter.

---

## 1. Data Modeling (data)

**Impact:** HIGH  
**Description:** The architectural foundation. Mutable defaults, mutation contracts, timezone-aware datetimes, discriminated unions. Mistakes here compound into state nobody intended.

## 2. Error Handling (error)

**Impact:** MEDIUM-HIGH  
**Description:** Specific exceptions, context managers for resources, preserved cancellation semantics. Sloppy exceptions hide bugs; narrow catches localize them.

## 3. Type Safety (types)

**Impact:** MEDIUM-HIGH  
**Description:** Precise types catch bugs at type-check time. Fix type errors rather than ignore them; no `Any` drift in new code.

## 4. API Design (api)

**Impact:** MEDIUM  
**Description:** Interfaces that age well. Required-before-optional ordering, keyword-only params, no boolean flag soup. Mostly applies to new code.

## 5. Code Simplification (simplify)

**Impact:** LOW-MEDIUM  
**Description:** Python idioms. Comprehensions, `any()`/`all()`, early returns. Mostly stylistic — apply when writing or reviewing.

## 6. Performance (perf)

**Impact:** LOW-MEDIUM  
**Description:** Python-specific optimizations. Set/dict lookups, cached properties, module-level compilation. Applied on measured hot paths, not as a stylistic crusade.

## 7. Naming (naming)

**Impact:** LOW-MEDIUM  
**Description:** Names carry meaning. Specific over generic, consistent terminology, no type suffixes. Mostly applies to new names.

## 8. Imports & Structure (imports)

**Impact:** LOW  
**Description:** Module hygiene. Imports at the top, no import-time side effects, optional deps handled explicitly. Most items linters catch automatically.
