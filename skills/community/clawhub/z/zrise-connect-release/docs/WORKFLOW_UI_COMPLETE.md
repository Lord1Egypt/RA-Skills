# 🎯 Workflow Management UI - Complete!

## ✅ Đã Hoàn Thành

### 1. **Workflow Registry**
- File: `workflow_registry.py`
- List 16+ workflows (built-in + custom + Lobster)
- Search by name, tags, category

### 2. **Workflow Manager (CLI)**
- File: `workflow_manager.py`
- CRUD operations cho workflows
- Validate Lobster YAML
- Test workflows

### 3. **Workflow Manager UI (Web)**
- File: `workflow_manager_ui.py`
- **Port:** 8888
- **Features:**
  - ✅ List workflows
  - ✅ Create new workflow
  - ✅ Edit existing workflow
  - ✅ Delete workflow
  - ✅ Filter by category/owner
  - ✅ YAML editor
  - ✅ Permission control (owner/admin/public)

---

## 🚀 Khởi Động UI

```bash
cd ~/.openclaw/workspace-ai-company/skills/zrise-connect/scripts
python3 workflow_manager_ui.py --port 8888
```

**Truy cập:** http://localhost:8888

---

## 📋 UI Features

### List View
- Hiển thị tất cả workflows
- Filter theo category, owner
- Badge visibility (public/private/team)

### Create/Edit Form
- **Fields:**
  - Name
  - Description
  - Category (custom/analysis/development/qa/docs)
  - Visibility (private/team/public)
  - YAML editor với syntax validation

### Actions
- **Edit** — Sửa workflow
- **Delete** — Xóa workflow (chỉ owner)
- **Test** — Test với sample args

---

## 🔧 Workflow YAML Template

```yaml
# name: my-custom-workflow
# description: My custom workflow for specific tasks
# args:
#   task_id:
#     required: true
#     type: int
#   feedback:
#     default: ""
#     type: string
# steps:
#   - id: fetch_task
#     command: python3 skills/zrise-connect/scripts/fetch_task_data.py {{args.task_id}}
#     description: Fetch task from Zrise
#   
#   - id: process
#     command: python3 skills/zrise-connect/scripts/invoke_agent_for_task.py --task-id {{args.task_id}} --workflow custom
#     description: Process task with custom logic
#   
#   - id: output
#     command: cat
#     stdin: $process.stdout
#     description: Output result
```

---

## 👥 Employee Workflow Setup

### Bước 1: Access UI
```
http://localhost:8888
```

### Bước 2: Create Workflow
1. Click "+ New Workflow"
2. Điền thông tin:
   - Name: "My Analysis Workflow"
   - Description: "Phân tích task theo cách của tôi"
   - Category: "analysis"
   - Visibility: "private" (hoặc "team"/"public")
3. Edit YAML (copy template)
4. Click "Save"

### Bước 3: Test Workflow
1. Click "Edit" trên workflow
2. Click "Test" button
3. Nhập test args (JSON): `{"task_id": 42174}`
4. Xem kết quả

### Bước 4: Share với Team
1. Edit workflow
2. Change visibility to "team"
3. Save
4. Team members có thể thấy và dùng workflow

---

## 📊 Registry Location

**Global Registry:**
```
~/.openclaw/workspace-ai-company/workflows/registry.json
```

**Employee Workflows:**
```
~/.openclaw/workspace-ai-company/workflows/employee-workflows/
├── khoa/
│   ├── my-workflow.lobster
│   └── workflow-meta.json
├── employee2/
│   └── their-workflow.lobster
└── shared/
    └── team-workflow.lobster
```

---

## 🎨 UI Screenshot (Concept)

```
┌─────────────────────────────────────────────────────────┐
│  🔧 Workflow Manager                                     │
├─────────────────────────────────────────────────────────┤
│  [+ New Workflow]  [🔄 Refresh]                         │
├─────────────────────────────────────────────────────────┤
│  📋 General Task Processing                             │
│     [public] Category: general | Owner: system          │
│     Default workflow for general tasks                  │
│     [Edit] [Delete]                                     │
├─────────────────────────────────────────────────────────┤
│  📊 Requirement Analysis                                │
│     [public] Category: analysis | Owner: system         │
│     Analyze requirements, create user stories           │
│     [Edit] [Delete]                                     │
├─────────────────────────────────────────────────────────┤
│  🔧 My Custom Workflow (Khoa)                           │
│     [private] Category: custom | Owner: khoa            │
│     My personal workflow for special tasks              │
│     [Edit] [Delete]                                     │
└─────────────────────────────────────────────────────────┘
```

---

## 🔐 Permissions

| Role | Permissions |
|------|-------------|
| **Owner** | Edit, Delete, Change visibility |
| **Team Member** | View, Use (if team visibility) |
| **Everyone** | View, Use (if public visibility) |

---

## 📝 Next Steps

1. ✅ UI đã chạy tại http://localhost:8888
2. ⏳ Integrate vào OpenClaw main UI
3. ⏳ Add workflow templates library
4. ⏳ Add workflow import/export
5. ⏳ Add workflow versioning

---

## 💡 Tips cho Nhân Viên

1. **Start Simple** — Copy template, modify nhỏ
2. **Test Often** — Test với task thật trước khi dùng
3. **Share Good Ones** — Nếu workflow tốt, share với team
4. **Document** — Thêm mô tả rõ ràng để team hiểu
5. **Iterate** — Cải thiện workflow theo thời gian

---

**Workflow Manager UI đã sẵn sàng!** 🎉

Truy cập: http://localhost:8888
