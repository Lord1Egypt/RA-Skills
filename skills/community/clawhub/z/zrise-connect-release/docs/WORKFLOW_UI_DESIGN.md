# OpenClaw Workflow Management UI

## 📋 Mục Tiêu

Tạo giao diện web để nhân viên có thể:
1. ✅ **Xem** danh sách workflows available
2. ✅ **Tạo** workflow mới (Lobster)
3. ✅ **Sửa** workflow (edit YAML/JSON)
4. ✅ **Đăng ký** workflow vào registry
5. ✅ **Test** workflow với sample task
6. ✅ **Phân quyền** (owner/admin/public)

---

## 🏗️ Architecture

```
OpenClaw Web UI
      ↓
/workflows
  ├── /list          — Danh sách workflows
  ├── /create        — Tạo workflow mới
  ├── /edit/:id      — Sửa workflow
  ├── /test/:id      — Test workflow
  └── /registry      — Workflow registry
      ↓
API Endpoints
  ├── GET  /api/workflows          — List workflows
  ├── POST /api/workflows          — Create workflow
  ├── PUT  /api/workflows/:id      — Update workflow
  ├── DEL  /api/workflows/:id      — Delete workflow
  ├── POST /api/workflows/:id/test — Test workflow
  └── GET  /api/workflows/registry — Get registry
      ↓
Backend Services
  ├── workflow_registry.py         — Registry management
  ├── workflow_validator.py        — Validate Lobster YAML
  └── workflow_runner.py           — Run/test workflows
```

---

## 📁 File Structure

```
~/.openclaw/
├── web-ui/
│   ├── workflows/
│   │   ├── list.html             — List view
│   │   ├── create.html           — Create form
│   │   ├── edit.html             — Edit form
│   │   ├── test.html             — Test interface
│   │   └── registry.html         — Registry view
│   └── api/
│       └── workflows.py          — API handlers
├── workflows/
│   ├── employee-workflows/       — Employee custom workflows
│   │   ├── khoa/
│   │   │   ├── my-workflow.lobster
│   │   │   └── workflow-meta.json
│   │   └── shared/
│   │       └── team-workflow.lobster
│   └── registry.json             — Global workflow registry
└── config/
    └── workflow-permissions.json — Access control
```

---

## 🔧 Implementation

### 1. Workflow Registry with Metadata

```json
{
  "workflow_id": "general",
  "name": "General Task Processing",
  "description": "Default workflow for general tasks",
  "category": "general",
  "tags": ["general", "default"],
  "file": "skills/zrise-connect/workflows/general.lobster",
  "owner": "system",
  "visibility": "public",
  "created_at": "2026-03-18T00:00:00Z",
  "updated_at": "2026-03-18T00:00:00Z",
  "version": "1.0.0",
  "agent": "zrise-analyst",
  "args_schema": {
    "task_id": {"type": "int", "required": true},
    "feedback": {"type": "string", "default": ""}
  },
  "test_cases": [
    {"args": {"task_id": 42174}, "expected": "success"}
  ]
}
```

### 2. UI Components

**List View:**
```
┌─────────────────────────────────────────────────────────┐
│  Workflow Management                                     │
├─────────────────────────────────────────────────────────┤
│  [+ New Workflow]  [🔍 Search]  [📁 Categories]         │
├─────────────────────────────────────────────────────────┤
│  📋 General Task Processing                             │
│     Category: general | Owner: system | Public          │
│     [Edit] [Test] [Duplicate]                           │
├─────────────────────────────────────────────────────────┤
│  📊 Requirement Analysis                                │
│     Category: analysis | Owner: system | Public         │
│     [Edit] [Test] [Duplicate]                           │
├─────────────────────────────────────────────────────────┤
│  🔧 My Custom Workflow (Khoa)                           │
│     Category: custom | Owner: khoa | Private            │
│     [Edit] [Test] [Delete] [Share]                      │
└─────────────────────────────────────────────────────────┘
```

**Create/Edit Form:**
```
┌─────────────────────────────────────────────────────────┐
│  Create New Workflow                                     │
├─────────────────────────────────────────────────────────┤
│  Name: [________________________]                       │
│  Description: [________________________]                │
│  Category: [Dropdown ▼]                                │
│  Tags: [________________________]                       │
│  Visibility: ○ Public  ○ Private  ○ Team               │
│  Agent: [Dropdown ▼]                                   │
├─────────────────────────────────────────────────────────┤
│  Workflow Definition (Lobster YAML):                    │
│  ┌─────────────────────────────────────────────────┐   │
│  │ name: my-workflow                               │   │
│  │ description: My custom workflow                  │   │
│  │ args:                                           │   │
│  │   task_id:                                      │   │
│  │     required: true                              │   │
│  │     type: int                                   │   │
│  │ steps:                                          │   │
│  │   - id: step1                                   │   │
│  │     command: echo "Hello"                       │   │
│  └─────────────────────────────────────────────────┘   │
│  [Validate YAML] [Save Draft] [Test] [Publish]         │
└─────────────────────────────────────────────────────────┘
```

---

## 💻 Code Implementation
