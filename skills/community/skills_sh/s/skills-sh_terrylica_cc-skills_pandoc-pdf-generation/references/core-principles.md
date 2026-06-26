**Skill**: [Pandoc PDF Generation](../SKILL.md)

# Core Development Principles for PDF Generation

## Overview

This document captures production-learned principles from PDF generation failures, elevated to universal development practices applicable beyond just PDF workflows.

## Canonical Implementations Over Ad-Hoc Solutions

### Principle

When tooling or workflows exist in `~/.claude/`, always use the canonical implementation rather than creating ad-hoc alternatives.

### Why This Matters

- **Canonical implementations encode production-tested configurations**
  - They capture edge cases discovered through actual usage
  - Example: LaTeX `\raggedright` requirement for proper bullet list rendering

- **Ad-hoc solutions inevitably miss critical details**
  - Quick inline commands seem to work initially
  - Hidden edge cases only surface in production
  - Example: PDF bullet lists rendered as inline text with justified alignment

- **Maintenance burden multiplies with each ad-hoc variant**
  - Every custom script needs independent updates
  - Bug fixes don't propagate automatically
  - Knowledge fragments across codebase

### Examples

✅ **Correct - Use Canonical Implementation**:

```bash
# Invoke the skill which uses production-proven build script
Skill(doc-tools:pandoc-pdf-generation)

# Or use the bundled build script directly (relative to skill location)
./assets/build-pdf.sh input.md output.pdf
```

❌ **Wrong - Ad-Hoc Pandoc Command**:

```bash
# Missing critical LaTeX preamble (\raggedright), will break bullet lists
pandoc input.md -o output.pdf --pdf-engine=xelatex --toc
```

✅ **Correct - Symlink for Project Use**:

```bash
# Create symlink to canonical script (git-friendly)
# Marketplace plugins install to: ~/.claude/plugins/cache/cc-skills/plugins/doc-tools/
PLUGIN_PATH=~/.claude/plugins/cache/cc-skills/plugins/doc-tools
ln -s "$PLUGIN_PATH/skills/pandoc-pdf-generation/assets/build-pdf.sh" build-pdf.sh
./build-pdf.sh
```

❌ **Wrong - Copy-Paste and Modify**:

```bash
# Creates divergence, misses future updates to canonical version
cp path/to/build-pdf.sh ./my-custom-build.sh
# Edit my-custom-build.sh...
```

### When to Create New Canonical Implementations

Only create new canonical implementations when:

1. **Functionality doesn't exist** in `~/.claude/`
2. **Existing implementation has fundamental limitations** that can't be addressed through configuration
3. **After creation**:
   - Document in appropriate skill
   - Add to relevant documentation indexes
   - Update CLAUDE.md with link if universally applicable

## Verification is Mandatory, Not Optional

### Principle

All generated artifacts (PDFs, compiled binaries, deployed services) must be verified before presenting to users or marking tasks complete.

### Verification Requirements

1. **Automated checks**: Scripts that verify expected properties
   - Exit code checks
   - Output format validation
   - Pattern matching for known failure signatures

2. **Visual inspection**: Human review of critical outputs
   - Open generated files in appropriate viewers
   - Spot-check formatting, layout, content
   - Verify edge cases mentioned in requirements

3. **Documented verification process**: Add checks to skills documentation
   - Update SKILL.md with verification steps
   - Add to reference docs as troubleshooting patterns
   - Create automated verification scripts when applicable

### Examples for PDF Generation

**Automated Verification**:

```bash
# Check for broken bullet rendering (expect 0 matches)
pdftotext output.pdf - | grep -E '^\w.*: -'

# Check for visible bare URLs (expect 0 matches)
pdftotext output.pdf - | grep -c "https://"

# Verify PDF metadata
pdfinfo output.pdf | grep -E "Pages|File size"
```

**Visual Verification Checklist**:

- [ ] Bullet lists render as bullets (•), not inline dashes
- [ ] Tables don't overflow page margins
- [ ] All hyperlinks are clickable (no bare URLs visible)
- [ ] Font rendering is consistent
- [ ] Page breaks are appropriate
- [ ] Table of contents links work correctly

**Verification Scripts**:

- Project-level skill: `pdf-generation-verification`
- Comprehensive automated checks + reporting
- Integration with build workflows

### Failure Mode

**Presenting unverified work creates reactive debugging cycles**:

1. User receives unverified output
2. User discovers formatting issue
3. Developer investigates root cause
4. Fix is applied and regenerated
5. User verifies again → repeat if issues remain

This wastes both developer and user time, erodes confidence in deliverables.

**Prevention**: Verification before presentation catches issues at step 1.

## Document Root Causes When Failures Occur

### Principle

When a production failure occurs (like PDF bullet rendering), document the root cause comprehensively for future reference.

### Documentation Requirements

1. **Root Cause Analysis**:
   - What actually went wrong technically
   - Why did it happen (underlying mechanism)
   - What edge case was missed

2. **Prevention Measures**:
   - How to avoid recurrence
   - What checks to add
   - What configurations are required

3. **Update Skills Documentation**:
   - Integrate learnings into existing skills
   - Add troubleshooting sections
   - Update verification checklists

4. **Update Global Memory**:
   - Add holistic principles to CLAUDE.md (if universally applicable)
   - Link to detailed documentation in skills
   - Ensure patterns are discoverable

### Examples

**PDF Bullet Rendering Failure** (November 2025):

**Root Cause Analysis Created**:

- Skills documentation: `troubleshooting-pandoc.md` → "Bullet Lists Rendering as Inline Text" section
- Detailed technical explanation of LaTeX justified text breaking list structures
- Test case verification showing when it fails vs. works

**Skills Documentation Updated**:

- `pandoc-pdf-generation/SKILL.md` - Added verification requirements
- `pdf-generation-verification/SKILL.md` - Added bullet rendering checks
- `pdf-generation-verification/references/pdf-best-practices.md` - Added LaTeX preamble requirements

**Global Memory Updated**:

- CLAUDE.md - Links to pandoc-pdf-generation skill
- Reference to this principles document

### Why This Matters

**Documentation transforms individual failures into organizational knowledge**:

- Future work automatically benefits from past learnings
- Prevents entire classes of errors, not just specific bugs
- New team members (or AI agents in new sessions) inherit knowledge
- Failure patterns become searchable and discoverable

## Application Beyond PDF Generation

While these principles were learned through PDF generation failures, they apply universally:

### Canonical Implementations

- Build scripts for any compiled language
- Deployment automation scripts
- Configuration management tools
- Testing frameworks

### Verification Requirements

- Compiled binaries (run test suites)
- Deployed services (health checks)
- Database migrations (validation queries)
- API responses (contract testing)

### Root Cause Documentation

- Production outages (postmortem documents)
- Security vulnerabilities (security advisories)
- Performance regressions (performance analysis reports)
- Integration failures (integration debugging guides)

## Related Resources

- **PDF Generation Skill**: [SKILL.md](../SKILL.md) - Main skill documentation
- **Troubleshooting Guide**: [troubleshooting-pandoc.md](./troubleshooting-pandoc.md)
- **PDF Verification Skill**: Project-level `.claude/skills/pdf-generation-verification/SKILL.md` (when available)
- **Global Memory**: `~/.claude/CLAUDE.md` - Hub-and-spoke navigation
- **Skill Invocation**: `Skill(doc-tools:pandoc-pdf-generation)`

## Summary

**Three Universal Principles**:

1. **Use Canonical Implementations** - Don't recreate what already exists and works
2. **Verify Before Presenting** - Catch issues before users do
3. **Document Root Causes** - Transform failures into organizational knowledge

These principles prevent entire classes of errors through systematic application of production-learned patterns.
