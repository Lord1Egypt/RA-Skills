# Template Examples - Các Ví Dụ Thực Tế

## Tạo Skill Mới Trong 30 Phút

### ⏰ Phút 0-5: Chuẩn Bị

```
□ Xác định 2-3 use cases
□ Liệt kê công cụ cần dùng
□ Xác định trigger phrases
```

### ⏰ Phút 5-10: Cấu Trúc

```
□ Tạo folder (kebab-case)
□ Tạo SKILL.md
□ Tạo scripts/, references/
```

### ⏰ Phút 10-20: Viết

```
□ Frontmatter YAML
□ Instructions (bước 1,2,3)
□ Examples (ít nhất 1-2)
□ Troubleshooting
```

### ⏰ Phút 20-25: Test

```
□ python -m yaml SKILL.md
□ Kiểm tra description
□ Đọc lại để tìm lỗi
```

### ⏰ Phút 25-30: Deploy

```
□ Nén thành .zip
□ Tải lên Claude.ai
□ Test 1-2 lần
```

---

## Ví Dụ 1: PDF to Markdown Converter

### Cấu Trúc

```
pdf-to-markdown/
├── SKILL.md
├── scripts/
│   ├── convert.py
│   └── validate.py
├── references/
│   └── supported-formats.md
└── assets/
    └── conversion-template.txt
```

### SKILL.md

```yaml
---
name: pdf-to-markdown
description: Convert PDF to Markdown voi formatting, tables, 
images. Su dung khi "convert PDF", "PDF to markdown", 
"extract PDF text".
license: MIT
metadata:
  author: Claude VN
  version: 1.0.0
---

# PDF sang Markdown Converter

## Hướng Dẫn

### Bước 1: Nhận Diện PDF Type
- Scanned image (cần OCR)
- Text-based (extract trực tiếp)
- Có bảng (cần markdown format)

### Bước 2: Convert

```bash
python scripts/convert.py --input document.pdf --output document.md
```

### Bước 3: Validate

```bash
python scripts/validate.py --markdown document.md
```

## Ví Dụ

### Ví dụ 1: Invoice

**Input:** invoice.pdf

**Xử lý:**
1. Text-based PDF
2. Extract content + tables
3. Markdown format

**Output:** invoice.md (ready to download)

### Ví dụ 2: Scanned Document

**Input:** scanned.pdf

**Xử lý:**
1. Detect need OCR
2. Run OCR
3. Format to markdown
4. Create index

## Khắc Phục Sự Cố

### Lỗi: "Unable to read PDF"
**Nguyên nhân:** File encrypted hoặc corrupt

**Giải pháp:**
- Check file valid
- If encrypted, remove password first
```

---

## Ví Dụ 2: Linear Sprint Planner

```yaml
---
name: linear-sprint-planner
description: Plan sprint automatically in Linear including 
velocity analysis, task prioritization. Su dung khi "sprint 
planning", "create sprint", "plan Q4".
metadata:
  author: Engineering Team
  version: 1.0.0
  mcp-server: linear
---

# Linear Sprint Planner

## Hướng Dẫn

### Bước 1: Fetch Team Data
- Get current tasks từ Linear MCP
- Analyze sprint velocity
- Determine available capacity

### Bước 2: Analysis & Recommendations
- Compare vs historical velocity
- Suggest tasks
- Warn if overloaded

### Bước 3: Create Sprint
Create new sprint in Linear:
- Sprint goal
- Suggested tasks
- Start/end dates

### Bước 4: Notify Team
Announce to Slack/email:
- Sprint goal
- Allocated capacity
- Key tasks

## Ví Dụ

### Q4 Sprint Planning

**User says:** "Plan Q4 sprint with 2 weeks, team has 4 people"

**Process:**
1. Fetch backlog
2. Calculate: 4 people × 2 weeks × velocity = capacity
3. Suggest fitting tasks
4. Create sprint "Q4 Sprint 1"
5. Assign tasks
6. Notify team

**Result:** Sprint created, team notified
```

---

## Ví Dụ 3: Content Writer

```yaml
---
name: ai-content-writer
description: Write blog, newsletter, social posts voi SEO 
optimization. Su dung khi "write blog", "create newsletter", 
"social content".
metadata:
  author: Content Team
  version: 1.0.0
  tags: [writing, content]
---

# AI Content Writer

## Hướng Dẫn

### Bước 1: Gather Info
Ask for:
- Topic / Keywords
- Desired length
- Tone (formal, casual)
- Purpose (blog, LinkedIn, Twitter)

### Bước 2: Create Outline
- Title
- Intro
- 3-5 main sections
- Conclusion
- CTA

### Bước 3: Write Content
- Natural language
- SEO keywords
- Suggested images
- Internal links

### Bước 4: Optimize
- Check SEO
- Add meta description
- Improve readability
- Remove jargon

## Ví Dụ

### Blog: "AI Safety Best Practices"

**Input:**
- Topic: AI Safety
- Length: 1500 words
- Tone: Professional but accessible
- Platform: Blog

**Output:**
1. Title: "5 Critical AI Safety Practices Every Developer..."
2. Meta description (160 chars)
3. Full blog post
4. 3 suggested images
5. Internal links
```

---

## Ví Dụ 4: Project Setup Wizard

```yaml
---
name: notion-project-setup
description: Setup complete Notion workspace voi databases, 
templates, automations. Su dung khi "setup Notion", "create 
workspace", "Notion template".
metadata:
  author: Productivity Team
  version: 1.0.0
  mcp-server: notion
---

# Notion Project Setup Wizard

## Hướng Dẫn

### Bước 1: Define Project Type
- Blog/Content
- Project Management
- Knowledge Base
- CRM
- Other

### Bước 2: Create Databases
Based on type:
- Posts/Articles
- Projects/Tasks
- People/Contacts
- Resources
- Etc.

### Bước 3: Add Templates
- Task templates
- Post templates
- Meeting notes
- Retrospective

### Bước 4: Setup Automations
- Reminders
- Status updates
- Notifications
- Archives

## Ví dụ

### Blog Workspace Setup

**User says:** "Setup a Notion blog workspace"

**Process:**
1. Create Posts database
2. Create Category database
3. Add Post template
4. Create Post status updates
5. Setup published/draft views
6. Add writing guidelines page

**Result:** Full blog workspace ready
```

---

## Template Nhanh: Copy & Paste

```yaml
---
name: my-skill-name
description: No lam gi. Su dung khi [trigger phrases].
license: MIT
metadata:
  author: Your Name
  version: 1.0.0
---

# Skill Name

## Hướng Dẫn

### Bước 1: [...]
...

### Bước 2: [...]
...

## Ví Dụ

### Ví dụ 1: [...]
**User says:** "..."

**Process:**
1. ...
2. ...

**Result:** ...

## Khắc Phục Sự Cố

### Lỗi: [...]
**Nguyên nhân:** ...

**Giải pháp:** ...
```

---

## Cấu Trúc File Tối Thiểu

```
my-skill/
├── SKILL.md                    # BẮT BUỘC
├── scripts/                    # TÙY CHỌN
│   └── validate.py
└── references/                 # TÙY CHỌN
    └── guide.md
```

## Cấu Trúc File Đầy Đủ

```
my-skill/
├── SKILL.md
├── scripts/
│   ├── validate.py
│   ├── process.py
│   └── requirements.txt
├── references/
│   ├── api-guide.md
│   ├── examples.md
│   └── troubleshooting.md
└── assets/
    ├── templates/
    ├── samples/
    └── icons/
```

---

## Checklist: Trước Upload

```
□ SKILL.md tồn tại
□ Tên file chính xác (case-sensitive)
□ Frontmatter có --- ở đầu + cuối
□ name: kebab-case
□ description: < 1024 chars
□ description: có CÁI GÌ + KHI NÀO
□ Hướng dẫn rõ ràng
□ Có ít nhất 1-2 ví dụ
□ Có troubleshooting
□ Scripts có comment
□ Không có file thừa
□ Nén thành .zip
```

---

## Checklist: Sau Upload

```
□ Test kích hoạt trên obvious queries
□ Test kích hoạt trên paraphrased
□ Test không kích hoạt trên unrelated
□ Test chức năng hoạt động đúng
□ Kiểm tra error handling
□ Theo dõi user feedback
□ Cập nhật version nếu cần
□ Iterate trên description
```

---

*Ready to create? Copy a template above and customize!*
