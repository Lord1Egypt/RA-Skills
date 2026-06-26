---
name: uplo-legal
description: AI-powered legal knowledge management. Search contracts, compliance requirements, legal cases, and policy documents with structured extraction.
---

# UPLO Legal — Contract & Compliance Intelligence

You have access to organizational knowledge through UPLO, focused on **legal** domain expertise.

## Session Start

When you begin a new session, fetch your organizational context:
```bash
mcporter call uplo-legal.get_identity_context
```

## When to Use

- Questions about legal policies, procedures, or processes
- Looking up domain-specific knowledge and documentation
- Finding subject matter experts
- Verifying facts against the knowledge base

## Key Tools

**Search knowledge:**
```bash
mcporter call uplo-legal.search_knowledge query="your question here"
```

**Search with full context (GraphRAG):**
```bash
mcporter call uplo-legal.search_with_context query="complex question with org context"
```

**Export org context:**
```bash
mcporter call uplo-legal.export_org_context
```

**Get directives:**
```bash
mcporter call uplo-legal.get_directives
```

## Session End

Log the conversation:
```bash
mcporter call uplo-legal.log_conversation summary="Brief summary" topics='["topic1"]' tools_used='["search_knowledge"]'
```

## Important

- Always cite sources when sharing UPLO information
- Respect classification levels
- If UPLO doesn't have the answer, say so rather than guessing
