---
name: simple-product-doc-manager
description: |
  Simple Management of Product Documents - A structured workflow for managing product documentation in Feishu (Lark).
  
  Use this skill when:
  - Creating a new project knowledge base in Feishu
  - Setting up standardized document structure for product development
  - Managing product requirements documents with version control
  - Following the project's documentation workflow (requirements → implementation → archival)
  - Setting up Feishu API integration for automated document management
  
  This skill provides a complete document management system including: requirements thinking docs, project/code documentation, configuration records, and versioned product requirement documents.
---

# Simple Product Doc Manager | 产品文档管理器

> A structured workflow for managing product documentation in Feishu with clear lifecycle management and version control.

## 📋 Document Structure

When setting up a new project, create this structure in Feishu:

```
项目知识库/Project Knowledge Base
├── 📄 需求思考/Requirements Thinking
│   └── (Ongoing) Product insights, user pain points, competitive analysis
├── 📄 项目地址和代码逻辑记录/Project & Code Logic
│   └── (Ongoing) Architecture, key functions, database schemas
├── 📄 配置信息记录/Configuration Records
│   └── (Ongoing) API keys, env variables, deployment configs
└── 📁 产品需求文档/Product Requirements/
    ├── YYYY-M-D-requirement-name-v1.md  (Draft → Finalized)
    ├── YYYY-M-D-requirement-name-v2.md  (New version for iterations)
    └── ...
```

## 🔄 Document Lifecycle

### Requirements Document States

| State | Description | Actions Allowed |
|-------|-------------|-----------------|
| **撰写中/Drafting** | Requirements being written or in development | Edit, update, refine |
| **已定型/Finalized** | Code implemented and approved by user | Read-only, archived |

### State Transition Rules

1. **New Requirement** → Create document with "Drafting" status
2. **Development** → Continuously update document
3. **Code Complete** → User reviews and approves
4. **Approved** → Status changes to "Finalized", document locked
5. **New Iteration** → Create new version document (v2, v3, etc.)

## 📝 Naming Convention

### Requirements Documents

Format: `{YYYY}-{M}-{D}-{requirement-name}-v{version}`

Examples:
- `2026-3-26-mvp-full-requirements-v1`
- `2026-3-28-user-login-feature-v1`
- `2026-4-5-user-login-feature-v2` (iteration)

Rules:
- Use actual date when document is created
- Use lowercase for requirement names
- Use hyphens as separators
- Increment version for same requirement iterations

## 🚀 Workflow

### 1. Project Setup

Create the knowledge base with initial structure:

```json
{
  "action": "create_knowledge_base",
  "name": "Project Name Knowledge Base"
}
```

### 2. Create Core Documents

Create the three ongoing documents:
- Requirements Thinking
- Project & Code Logic Records
- Configuration Records

### 3. Requirements Workflow

```
New Idea → Create Requirements Doc (Drafting)
                ↓
        Write & Refine Requirements
                ↓
        Develop Code (sync to Code Logic doc)
                ↓
        User Review & Approval
                ↓
    ┌───────────────────────┐
    ↓                       ↓
Approved → Finalize    Changes Needed → Update Doc
    ↓                       ↓
Locked (Read-only)    Continue Development
    ↓
New Iteration → Create v2
```

## 📚 Reference Materials

- [references/workflow-examples.md](references/workflow-examples.md) - Concrete examples
- [references/feishu-api-setup.md](references/feishu-api-setup.md) - Complete Feishu API configuration guide

## 🔧 Best Practices

1. **Always use `write`/`append` for Markdown** - These actions auto-render formatting
2. **Never use `update_block` for Markdown** - It stores plain text only
3. **Keep Requirements Thinking updated** - Capture insights as they come
4. **Document code logic immediately** - Don't wait until after implementation
5. **Version clearly** - When in doubt, create a new version rather than overwrite
