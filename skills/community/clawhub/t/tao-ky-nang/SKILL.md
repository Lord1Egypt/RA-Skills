---
name: tao-ky-nang
description: Huong dan tao ky nang Claude. Su dung khi muon xay dung skill, tao ky nang, viet YAML, hoac kiểm thu ky nang.
license: MIT
metadata:
  author: Claude VN
  version: 1.0.0
  language: Vietnamese
  category: productivity
---

# Tạo Kỹ Năng Claude - Hướng Dẫn Toàn Diện

## Kỹ Năng Là Gì?

Kỹ năng là một thư mục chứa các hướng dẫn (SKILL.md) dạy cho Claude cách xử lý các tác vụ hoặc quy trình cụ thể. Nó là một cách mạnh mẽ để tùy chỉnh Claude mà không phải giải thích lại ưu tiên trong mỗi cuộc trò chuyện.

### Thích hợp cho:
- Các quy trình lặp lại
- Tác vụ yêu cầu phương pháp nhất quán
- Công việc nhóm cần tiêu chuẩn hóa
- Tích hợp với MCP servers

---

## Bước 1: Định Nghĩa Use Case

Trước khi viết bất kỳ code nào, xác định **2-3 use case cụ thể** mà kỹ năng của bạn nên hỗ trợ.

### Tiêu Chuẩn Định Nghĩa Tốt

```
Use Case: Lập Kế Hoạch Sprint
Trigger: Người dùng nói "giúp tôi lập kế hoạch sprint này" 
         hoặc "tạo các nhiệm vụ sprint"

Bước:
1. Lấy trạng thái dự án hiện tại
2. Phân tích năng suất và dung lượng nhóm
3. Đề xuất ưu tiên tác vụ
4. Tạo tác vụ với nhãn và ước tính phù hợp

Kết Quả: Sprint được lập kế hoạch đầy đủ
```

### Câu Hỏi Cần Đặt
- Người dùng muốn đạt được điều gì?
- Những quy trình đa bước nào cần thiết?
- Cần những công cụ nào (tích hợp sẵn hay MCP)?
- Kiến thức hoặc best practice nào cần nhúng?

---

## Bước 2: Cấu Trúc Thư Mục Kỹ Năng

Tạo thư mục với cấu trúc này:

```
ten-ky-nang/
├── SKILL.md              # Bắt buộc
├── scripts/              # Tùy chọn
│   └── validate.py
├── references/           # Tùy chọn
│   └── examples.md
└── assets/               # Tùy chọn
    └── template.md
```

### Quy Tắc Quan Trọng

| Yêu Cầu | Đúng | Sai |
|---------|------|-----|
| Tên File | SKILL.md | SKILL.MD, skill.md |
| Tên Thư Mục | my-skill-name | My Skill Name |
| Format | kebab-case | snake_case, CamelCase |

---

## Bước 3: Viết YAML Frontmatter

Đây là phần quan trọng nhất.

### Format Tối Thiểu

```yaml
---
name: ten-ky-nang
description: No lam gi. Su dung khi nao.
---
```

### Các Trường

#### `name` (Bắt buộc)
- Chỉ kebab-case: `my-skill-name`
- Không khoảng trắng, không chữ hoa
- Khớp với tên thư mục

#### `description` (Bắt buộc)
Phải bao gồm:
- **CÁI GÌ:** Nó làm gì?
- **KHI NÀO:** Khi nào sử dụng?

```yaml
# Tốt
description: Quan ly Linear sprint planning. Su dung khi 
"sprint planning", "create tasks", "project planning".

# Xấu
description: Giup voi cac du an.
```

#### `license` (Tùy chọn)
```yaml
license: MIT
```

#### `metadata` (Tùy chọn)
```yaml
metadata:
  author: Tác Giả
  version: 1.0.0
  category: productivity
  tags: [automation, workflow]
```

### Lỗi Phổ Biến

```yaml
# Sai - thiếu dấu phân cách
name: my-skill
description: Does things

# Sai - indentation
metadata:
author: John

# Đúng
---
name: my-skill
description: Does things
metadata:
  author: John
---
```

---

## Bước 4: Viết Hướng Dẫn

Sau frontmatter, viết hướng dẫn rõ ràng.

### Cấu Trúc

```markdown
# Tên Kỹ Năng

## Hướng Dẫn

### Bước 1: [Tiêu đề]
Mô tả rõ ràng.

```bash
python scripts/example.py --input file.txt
```

**Kết quả dự kiến:** Mô tả output

### Bước 2: [Tiêu đề khác]
Chi tiết thêm.

## Ví Dụ

### Ví dụ 1: [Kịch bản]
**Người dùng nói:** "..."

**Hành động:**
1. ...
2. ...

**Kết quả:** ...

## Khắc Phục Sự Cố

### Lỗi: [Thông báo lỗi]
**Nguyên nhân:** ...
**Giải pháp:** ...
```

### Best Practices

✅ **Hành động Cụ Thể**
```
Chạy `python scripts/validate.py --input data.csv` để 
kiểm tra dữ liệu.

Nếu xác thực thất bại:
- Trường bắt buộc bị thiếu (thêm vào CSV)
- Định dạng ngày sai (dùng YYYY-MM-DD)
```

✅ **Xử Lý Lỗi**
```markdown
### Lỗi: Kết Nối MCP Không Thành Công

Nếu "Connection refused":
1. Xác minh server MCP chạy
2. Kiểm tra API key hợp lệ
3. Thử kết nối lại
```

✅ **Tham Chiếu Tài Liệu**
```
Xem `references/api-guide.md` để:
- Hướng dẫn rate limiting
- Mẫu pagination
- Xử lý error codes
```

---

## Bước 5: Kiểm Thử Kỹ Năng

### 1. Kiểm Thử Kích Hoạt
**Mục tiêu:** Skill tải khi nên, không tải khi không nên

```
Nên kích hoạt:
- "Giúp tôi tạo kỹ năng"
- "Hướng dẫn viết YAML"
- "Tôi muốn xây dựng skill"

Không nên kích hoạt:
- "Thời tiết hôm nay?"
- "Viết code Python"
```

### 2. Kiểm Thử Chức Năng
**Mục tiêu:** Verify output đúng

```
Test: Tạo dự án với 5 task

Cho: Tên "Q4 Planning", 5 mô tả
Khi: Skill chạy
Thì:
 - Dự án tạo thành công
 - 5 task được tạo
 - Tất cả liên kết với dự án
 - 0 lỗi
```

### 3. So Sánh Hiệu Suất
**Mục tiêu:** Prove skill improve

```
Không có skill:
- 15 tin nhắn chat
- 3 lỗi API
- 12,000 tokens

Với skill:
- 2 câu hỏi
- 0 lỗi
- 6,000 tokens
```

---

## Bước 6: Phát Hành & Chia Sẻ

### Cho Người Dùng Cá Nhân

1. **Tải xuống** thư mục skill
2. **Nén thành** .zip
3. **Tải lên** Claude.ai: Settings > Capabilities > Skills
4. **Bật** skill

### Cho Tổ Chức

- Quản trị viên triển khai toàn workspace
- Cập nhật tự động
- Quản lý tập trung

### Chia Sẻ Trên GitHub

1. **Lưu trữ**
   - Public repo cho open-source
   - README rõ ràng
   - Ví dụ & screenshots

2. **Tài Liệu MCP**
   - Link đến skill
   - Giải thích giá trị
   - Hướng dẫn quick start

---

## Các Mẫu Phổ Biến

### Mẫu 1: Sequential Workflow

```markdown
# Workflow: Onboard Khách Hàng

### Bước 1: Tạo Tài Khoản
Gọi create_customer
Param: name, email, company

### Bước 2: Thanh Toán
Gọi setup_payment_method
Chờ: verification

### Bước 3: Subscription
Gọi create_subscription
Param: plan_id, customer_id

### Bước 4: Email
Gọi send_email
Template: welcome
```

### Mẫu 2: Multi-MCP Coordination

```markdown
# Phase 1: Design (Figma)
1. Export assets
2. Generate spec
3. Create manifest

# Phase 2: Storage (Drive)
1. Create folder
2. Upload assets
3. Generate links

# Phase 3: Tasks (Linear)
1. Create tasks
2. Attach links
3. Assign team
```

### Mẫu 3: Iterative Refinement

```markdown
# Step 1: Draft
1. Fetch data
2. Generate draft
3. Save to temp

# Step 2: Check
1. Run validation
2. Identify issues

# Step 3: Refine
1. Fix issues
2. Regenerate
3. Re-validate
4. Repeat if needed
```

---

## Khắc Phục Sự Cố

### Skill Không Tải Lên

#### "Không tìm SKILL.md"
**Nguyên nhân:** Tên file sai

**Sửa:**
- Đặt tên chính xác `SKILL.md`
- Kiểm tra: `ls -la` nên thấy `SKILL.md`

#### "Frontmatter không hợp lệ"
**Nguyên nhân:** YAML syntax sai

**Sửa:**
```yaml
# Sai
name: my-skill
description: Does things

# Đúng
---
name: my-skill
description: Does things
---
```

#### "Invalid name"
**Nguyên nhân:** Có spaces hoặc uppercase

**Sửa:**
```yaml
# Sai
name: My Cool Skill

# Đúng
name: my-cool-skill
```

### Skill Không Kích Hoạt

**Triệu chứng:** Skill không bao giờ tải

**Nguyên nhân:** Description không tốt

**Sửa:**
- Description quá chung chung? → Thêm trigger phrases
- Không nói khi dùng? → Rõ ràng "use when..."
- Không có ví dụ? → Thêm cụm từ người dùng thực sẽ nói

### Skill Kích Hoạt Quá Thường

**Triệu chứng:** Skill tải cho queries không liên quan

**Sửa:**

1. **Thêm negative triggers**
```yaml
description: Data analysis for CSV files. For statistical modeling,
regression. Do NOT use for simple exploration.
```

2. **Cụ thể hơn**
```yaml
# Xấu
description: Processes documents

# Tốt
description: Processes PDF legal documents for contract review
```

### MCP Connection Issues

**Triệu chứng:** Skill tải nhưng lỗi call MCP

**Kiểm tra:**
1. MCP server connected? (Settings > Extensions)
2. API key valid?
3. Test MCP separately (without skill)
4. Tool names correct? (case-sensitive)

---

## Tiêu Chí Thành Công

### Metrics Định Lượng
- Skill triggers 90%+ relevant queries
- Complete workflow in X tool calls
- 0 failed API per workflow

### Metrics Định Tính
- Users don't ask next steps
- Workflows complete without correction
- Consistent results across sessions

---

## Danh Sách Kiểm Tra

### Trước Bắt Đầu
- [ ] Define 2-3 use cases
- [ ] Identify tools needed
- [ ] Review this guide

### Trong Phát Triển
- [ ] Folder named kebab-case
- [ ] SKILL.md exists
- [ ] Frontmatter has --- delimiters
- [ ] name: kebab-case
- [ ] description: has WHAT + WHEN
- [ ] No XML brackets < >
- [ ] Instructions clear
- [ ] Error handling included
- [ ] Examples provided

### Trước Upload
- [ ] Test triggering on obvious tasks
- [ ] Test doesn't trigger unrelated
- [ ] Functional tests pass
- [ ] Tool integration works
- [ ] Compressed as .zip

### Sau Upload
- [ ] Test in real conversations
- [ ] Monitor triggering
- [ ] Collect feedback
- [ ] Iterate on description
- [ ] Update version

---

## Script Ví Dụ

```python
#!/usr/bin/env python3
"""Validate skill output"""

def validate_output(output_file):
    try:
        with open(output_file, 'r') as f:
            content = f.read()
        
        if not content.strip():
            return False, "File empty"
        
        if "# " not in content:
            return False, "No headings"
        
        return True, "Valid output"
    except Exception as e:
        return False, str(e)
```

---

## Tài Liệu Tham Khảo

- **Anthropic Docs:** anthropic.com/docs
- **Skills Repo:** github.com/anthropics/skills
- **MCP:** modelcontextprotocol.io
- **Discord:** Claude Developers Discord

---

## Tóm Tắt

**Tạo skill trong 5 bước:**

1. **Define use cases** - 2-3 use cases cụ thể
2. **Create structure** - Folder + SKILL.md + scripts/references
3. **Write frontmatter** - name, description, metadata
4. **Write instructions** - Hướng dẫn rõ + ví dụ + troubleshooting
5. **Test & deploy** - Upload & test trong thực tế

**Key points:**
- Use kebab-case for naming
- description = WHAT + WHEN
- Keep SKILL.md focused
- Add progressively disclosed docs in references/
- Test triggering + functionality

---

*Made by Claude VN | MIT License | v1.0.0*
