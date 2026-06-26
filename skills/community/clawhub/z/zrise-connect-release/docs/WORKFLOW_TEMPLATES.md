# Zrise Connect - Workflow Templates Library

## 📚 Available Workflow Templates

### 1. **email-draft** ✅
**Purpose:** Soạn thảo email thông báo
**Category:** communication
**Steps:** Fetch → Draft → Output

**Usage:**
```bash
python3 invoke_agent_for_task.py --task-id 42174 --workflow email-draft
```

**Output:**
- Email với tiêu đề
- Nội dung formatted
- Signature

---

### 2. **general** ✅
**Purpose:** Xử lý task tổng quát
**Category:** general
**Steps:** Fetch → Process → Output

**Output:**
- Summary
- Analysis
- Recommendations
- Next steps
- Risks

---

### 3. **requirement-analysis**
**Purpose:** Phân tích requirement chi tiết
**Category:** analysis
**Best for:** BA tasks

**Output:**
- User Stories
- Acceptance Criteria
- Questions cần làm rõ
- Assumptions
- Priority recommendation
- Risks

**Template:**
```yaml
name: requirement-analysis
description: Analyze requirements, create user stories, acceptance criteria
args:
  task_id:
    required: true
    type: int
steps:
  - id: fetch
    command: python3 skills/zrise-connect/scripts/fetch_task_data.py {{args.task_id}}
  
  - id: analyze
    command: python3 skills/zrise-connect/scripts/invoke_agent_for_task.py --task-id {{args.task_id}} --workflow requirement-analysis
    stdin: $fetch.stdout
  
  - id: output
    command: cat
    stdin: $analyze.stdout
```

---

### 4. **technical-design**
**Purpose:** Thiết kế kỹ thuật
**Category:** design
**Best for:** Architect tasks

**Output:**
- Architecture overview
- Data model changes
- API endpoints
- Integration points
- Technical decisions
- Non-functional requirements

---

### 5. **implementation**
**Purpose:** Phân tích implementation
**Category:** development
**Best for:** Dev tasks

**Output:**
- Files cần thay đổi
- Implementation plan
- Code patterns
- Dependencies
- Estimated effort
- Potential issues

---

### 6. **code-review**
**Purpose:** Review code
**Category:** review
**Best for:** PR review

**Output:**
- Strengths
- Issues
- Suggestions
- Risk assessment
- Priority
- Overall verdict

---

### 7. **testing**
**Purpose:** Lên kế hoạch test
**Category:** qa
**Best for:** QA tasks

**Output:**
- Test scenarios
- Test cases
- Automation candidates
- Test data needed
- Coverage gaps
- Acceptance checklist

---

### 8. **documentation**
**Purpose:** Tạo documentation
**Category:** docs
**Best for:** Technical writer tasks

**Output:**
- Document structure
- Content draft
- Target audience
- Missing info
- Related docs

---

### 9. **pm-planning**
**Purpose:** PM planning
**Category:** pm
**Best for:** PM tasks

**Output:**
- Scope definition
- Deliverables
- Dependencies
- Timeline
- Resource needs
- Risks

---

### 10. **clarification-request**
**Purpose:** Yêu cầu làm rõ thông tin
**Category:** clarification
**Best for:** Tasks thiếu thông tin

**Output:**
- Missing info detected
- Clarification questions
- Suggested stage (Clarification)
- Tagged user

---

## 🚀 How to Use Templates

### Option 1: Via Web UI
```
1. Open http://localhost:8888
2. Click "+ New Workflow"
3. Select template from dropdown
4. Customize YAML
5. Save
```

### Option 2: Via CLI
```bash
# Create from template
python3 workflow_manager.py --create \
  --name "my-analysis" \
  --from-template requirement-analysis \
  --visibility private
```

### Option 3: Copy Template
```bash
# Copy template file
cp workflows/requirement-analysis.lobster workflows/my-workflow.lobster

# Edit and register
python3 workflow_manager.py --create --name "my-workflow" --file my-workflow.lobster
```

---

## 📝 Template Structure

Every template includes:
1. **Metadata** (name, description, category)
2. **Args schema** (task_id required, optional params)
3. **Steps** (fetch → process → output)
4. **Agent assignment** (which agent to use)
5. **Output format** (structured response)

---

## 🎨 Customization

### Customize Agent Prompt
```yaml
# In invoke_agent_for_task.py WORKFLOW_PROMPTS
'my-custom': """Bạn là [role].

Output:
1. **Section 1**
2. **Section 2**
...

Viết bằng tiếng Việt."""
```

### Customize Steps
```yaml
steps:
  - id: fetch
    command: ...
  
  - id: validate
    command: python3 validate.py {{args.task_id}}
  
  - id: process
    command: ...
  
  - id: post
    command: python3 post_html_comment.py --task-id {{args.task_id}}
```

---

## 📊 Template Usage Stats

| Template | Uses | Rating |
|----------|------|--------|
| general | 5 | ⭐⭐⭐⭐ |
| email-draft | 3 | ⭐⭐⭐⭐⭐ |
| requirement-analysis | 2 | ⭐⭐⭐⭐ |
| technical-design | 1 | ⭐⭐⭐ |
| implementation | 1 | ⭐⭐⭐ |

---

## 🔧 Creating New Templates

### Step 1: Define Purpose
- What problem does it solve?
- Who is the target user?
- What's the expected output?

### Step 2: Create YAML
```yaml
name: my-template
description: What this template does
args:
  task_id:
    required: true
    type: int
  custom_param:
    default: ""
    type: string
steps:
  - id: step1
    command: ...
  - id: step2
    command: ...
```

### Step 3: Add Agent Prompt
```python
# In invoke_agent_for_task.py
WORKFLOW_PROMPTS['my-template'] = """..."""
```

### Step 4: Test
```bash
python3 test_simple_workflow.py --task-id 42174
```

### Step 5: Register
```bash
python3 workflow_manager.py --create --name "my-template" --file my-template.lobster
```

---

## 📚 Template Best Practices

1. **Clear Purpose** — One specific task type
2. **Structured Output** — Use sections and bullets
3. **Actionable** — Concrete next steps
4. **Bilingual** — Vietnamese primary, English technical terms
5. **Tested** — Verify with real tasks

---

**Templates library ready!** 📚
