# zrise-connect - Zrise Integration Skill v3.3

## 🎯 Purpose

Kết nối và vận hành Zrise qua XML-RPC API.

## ⚠️ QUAN TRỌNG — Quy tắc xử lý task

Khi được yêu cầu "làm task", agent **PHẢI** dùng Lobster workflow. **KHÔNG** tự:
- Generate kết quả luôn
- Post kết quả lên Zrise mà chưa được approve
- Kéo stage Done mà chưa được approve
- Gọi script riêng lẻ

### 🔄 Flow chuẩn (bắt buộc qua Lobster)

```
lobster run skills/zrise-connect/workflows/zrise-execute.lobster \
  --args-json '{"task_id": 42349, "user_message": "viết giới thiệu công ty"}'
```

**Flow steps:**
```
1. Fetch task từ Zrise
2. AI phân tích intent + lên plan
3. Post plan lên Zrise
4. Kéo stage → In Process
⏸️  APPROVAL: Review plan
   → lobster(action="resume", token=..., approve=true)  # approve
   → lobster(action="resume", token=..., approve=false) # reject
5. AI execute task theo plan
⏸️  APPROVAL: Review kết quả
   → lobster(action="resume", token=..., approve=true)  # approve → auto writeback + timesheet + Done
   → lobster(action="resume", token=..., approve=false) # reject → cần revise thủ công
6. (auto) Writeback kết quả lên Zrise
7. (auto) Fill timesheet
8. (auto) Stage → Done
```

### Khi revise sau reject:
```bash
lobster resume --token "..." --approve false
```

---

## 📦 Scripts (chỉ dùng cho debug/manual)

```bash
# Fetch task data
python3 scripts/fetch_task_data.py <task_id>

# Update stage
python3 scripts/update_task_stage.py <task_id> "In Process" --comment "Bắt đầu"

# Post comment
echo "nội dung" | python3 scripts/writeback_to_zrise.py --task-id <id> --workflow general

# Fill timesheet
python3 scripts/fill_timesheet.py --task-id <id> --hours 0.5 --description "mô tả"

# Poll pending tasks (cron)
python3 scripts/poll_employee_work.py --employee-id <ID> --limit 10 --json
```

## ⚠️ Zrise XML-RPC Gotchas

```python
# write(): [id, {vals}]
models.execute_kw(db, uid, pwd, 'model', 'write', [id, {'field': val}])

# message_post(): [[id]], {kwargs}
models.execute_kw(db, uid, pwd, 'model', 'message_post', [[id]], {'body': '...', 'message_type': 'comment'})

# Timesheet TRƯỚC stage Done (Zrise bắt buộc)
```

## 🔧 Lobster Setup

```bash
# Cài lobster (nếu chưa có)
cd /tmp && git clone https://github.com/openclaw/lobster.git && cd lobster && npm install && npx tsc -p tsconfig.json
export PATH="$HOME/bin:$PATH"
ln -sf /tmp/lobster/bin/lobster.js ~/bin/lobster
lobster version
```

## 🔑 Key Concepts

- **Employee ID** = `hr.employee.id` (not user ID)
- **Task assignment** = `project.task.user_ids` (Many2many to `res.users`)
- All scripts use `zrise_utils.connect_zrise()` (SSL-safe)
