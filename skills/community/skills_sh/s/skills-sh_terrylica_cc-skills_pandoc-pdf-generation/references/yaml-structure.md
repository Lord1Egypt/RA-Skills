**Skill**: [Pandoc PDF Generation](../SKILL.md)


### Why Use YAML Front Matter

Instead of using `# Title` as a level-1 heading (which creates numbering issues), use YAML front matter for document metadata:

**Problem with heading-based title:**
```markdown
# Document Title        ← Makes this Section 1
## Executive Summary    ← Becomes 1.1 instead of 1
## Introduction         ← Becomes 1.2 instead of 2
```

**Solution with YAML front matter:**
```markdown
---
title: Document Title
author: Your Name
date: 2025-11-04
---

## Executive Summary    ← Properly numbered as Section 1
## Introduction         ← Properly numbered as Section 2
```

### Full YAML Options

```yaml
---
title: Strategic Technology Advisory Proposal
author: Terry Li
date: November 3, 2025
abstract: |
  Multi-line abstract text here.
  Second line of abstract.
keywords: [automation, AI, compliance]
---
```

