# Zrise Connect - Team Onboarding Guide

## 👋 Welcome to Zrise Connect!

Zrise Connect giúp bạn tự động hóa tasks trên Zrise bằng AI workflows.

---

## 🚀 Quick Start (5 phút)

### Step 1: Access Workflow Manager

```
http://localhost:8888
```

### Step 2: Create Your First Workflow

1. Click **"+ New Workflow"**
2. Fill in:
   - Name: "My First Workflow"
   - Description: "My personal workflow"
   - Category: "custom"
   - Visibility: "private"
3. Copy template:
```yaml
name: my-first-workflow
description: My first workflow
args:
  task_id:
    required: true
    type: int
steps:
  - id: fetch
    command: python3 skills/zrise-connect/scripts/fetch_task_data.py {{args.task_id}}
  
  - id: process
    command: python3 skills/zrise-connect/scripts/invoke_agent_for_task.py --task-id {{args.task_id}} --workflow general
    stdin: $fetch.stdout
  
  - id: output
    command: cat
    stdin: $process.stdout
```
4. Click **"Save"**

### Step 3: Test Your Workflow

```bash
cd skills/zrise-connect/scripts
python3 test_simple_workflow.py --task-id <YOUR_TASK_ID> --approve
```

### Step 4: Check Result on Zrise

```
https://zrise.app/web#id=<YOUR_TASK_ID>
```

---

## 📚 Core Concepts

### 1. Workflows

**What:** Tự động hóa quy trình xử lý task

**Types:**
- `general` — Xử lý tổng quát
- `email-draft` — Soạn email
- `requirement-analysis` — Phân tích requirement
- `technical-design` — Thiết kế kỹ thuật
- `implementation` — Implementation plan
- `testing` — Test plan

### 2. Agents

**What:** AI assistants xử lý tasks

**Available:**
- `zrise-analyst` — Business Analyst
- `zrise-dev` — Developer
- `zrise-qa` — QA Engineer
- `zrise-pm` — Project Manager

### 3. Steps

Every workflow has 3 steps:
```
Fetch Task → Process with Agent → Post Result
```

### 4. Permissions

- **Private** — Chỉ bạn thấy
- **Team** — Team members thấy
- **Public** — Tất cả thấy

---

## 🎓 Learning Path

### Beginner (Day 1-3)

✅ **Goals:**
- Hiểu workflow là gì
- Tạo workflow đơn giản
- Test với task thật

📖 **Read:**
- `docs/WORKFLOW_TEMPLATES.md`
- `docs/WORKFLOW_UI_COMPLETE.md`

🎯 **Practice:**
1. Tạo 1 workflow đơn giản
2. Test với 3 tasks khác nhau
3. Share 1 workflow với team

### Intermediate (Day 4-7)

✅ **Goals:**
- Tạo custom workflows
- Use different agents
- Integrate với Zrise comments

📖 **Read:**
- `docs/TELEGRAM_INTEGRATION.md`
- Lobster workflow syntax

🎯 **Practice:**
1. Tạo workflow cho role của bạn (BA/Dev/QA/PM)
2. Customize agent prompts
3. Setup Telegram notifications

### Advanced (Week 2+)

✅ **Goals:**
- Create complex multi-step workflows
- Add approval gates
- Integrate with external tools

📖 **Read:**
- Lobster advanced features
- OpenClaw Agent API

🎯 **Practice:**
1. Create workflow với approval gates
2. Integrate với Git/GitHub
3. Build custom agent

---

## 🛠️ Common Tasks

### Create Email Draft Workflow

```bash
# 1. Go to UI
open http://localhost:8888

# 2. Click "+ New Workflow"
# 3. Select "email-draft" template
# 4. Customize
# 5. Save
# 6. Test
python3 test_simple_workflow.py --task-id 42174 --approve
```

### Run Requirement Analysis

```bash
python3 invoke_agent_for_task.py \
  --task-id 42174 \
  --workflow requirement-analysis
```

### Post Comment to Zrise

```bash
python3 post_html_comment.py \
  --task-id 42174 \
  --title "Analysis Result" \
  --content "Your content..."
```

### List Available Workflows

```bash
python3 workflow_registry.py --list
```

---

## 📋 Workflow Templates by Role

### For Business Analysts

**Recommended workflows:**
- `requirement-analysis` — Phân tích requirements
- `documentation` — Tạo docs
- `clarification-request` — Request clarification

**Example:**
```yaml
name: ba-analysis
description: BA task analysis
args:
  task_id:
    required: true
steps:
  - id: analyze
    command: python3 invoke_agent_for_task.py --task-id {{args.task_id}} --workflow requirement-analysis
  - id: output
    command: cat
    stdin: $analyze.stdout
```

### For Developers

**Recommended workflows:**
- `technical-design` — Technical design
- `implementation` — Implementation plan
- `code-review` — Code review

### For QA

**Recommended workflows:**
- `testing` — Test planning
- `code-review` — Review test code

### For PMs

**Recommended workflows:**
- `pm-planning` — Planning
- `documentation` — Status reports

---

## 🔧 Troubleshooting

### Workflow không chạy?

**Check:**
1. Task ID đúng chưa?
2. Workflow registered chưa? (`python3 workflow_registry.py --list`)
3. File workflow tồn tại không?

### Comment không hiện trên Zrise?

**Check:**
1. Zrise credentials đúng chưa?
2. API key còn valid không?
3. Task ID tồn tại không?

### Agent không trả lời?

**Check:**
1. Agent configured chưa? (`python3 configure_openclaw_agent.py --check`)
2. Model provider API key có không?
3. Network OK không?

---

## 📞 Support

### Internal

- **Documentation:** `skills/zrise-connect/docs/`
- **Examples:** `skills/zrise-connect/examples/`
- **Tests:** `skills/zrise-connect/scripts/test_*.py`

### Ask for Help

1. Check docs first
2. Run diagnostic: `python3 configure_openclaw_agent.py --check`
3. Contact IT team
4. Create issue on internal tracker

---

## 🎯 Best Practices

### DO ✅

- Test workflows trước khi dùng thật
- Share good workflows với team
- Document custom workflows
- Use descriptive names
- Add tags for searchability
- Review AI output trước khi post

### DON'T ❌

- Don't create duplicate workflows
- Don't skip testing
- Don't share sensitive data
- Don't ignore errors
- Don't over-complicate workflows

---

## 📊 Metrics to Track

**Personal:**
- Workflows created
- Tasks processed
- Time saved

**Team:**
- Workflows shared
- Adoption rate
- Error rate

---

## 🎓 Certification

### Zrise Connect Beginner

**Requirements:**
- ✅ Create 1 workflow
- ✅ Test with real task
- ✅ Post to Zrise

### Zrise Connect Intermediate

**Requirements:**
- ✅ Create 3 custom workflows
- ✅ Use different agents
- ✅ Share with team

### Zrise Connect Advanced

**Requirements:**
- ✅ Create complex workflows
- ✅ Add approval gates
- ✅ Integrate external tools
- ✅ Mentor others

---

## 📅 Training Schedule

### Week 1: Basics
- Day 1-2: Introduction
- Day 3-4: Hands-on practice
- Day 5: Assessment

### Week 2: Advanced
- Day 1-2: Custom workflows
- Day 3-4: Integrations
- Day 5: Final project

---

## 🎉 Next Steps

1. ✅ Complete Quick Start
2. 📖 Read workflow templates
3. 🧪 Test with your tasks
4. 🚀 Create custom workflow
5. 🤝 Share with team

---

**Welcome aboard! Let's automate your workflows!** 🚀
