# YAML Frontmatter - Tài Liệu Chi Tiết

## Format Tối Thiểu

```yaml
---
name: ten-ky-nang
description: No lam gi. Su dung khi nao.
---
```

## Tất Cả Các Trường

```yaml
---
name: ten-ky-nang
description: Nó làm gì. Sử dụng khi [điều kiện].
license: MIT
metadata:
  author: Tên Tác Giả
  version: 1.0.0
  category: productivity
  tags: [automation, workflow]
---
```

## Chi Tiết Từng Trường

### `name` (Bắt buộc)

**Yêu cầu:**
- Kebab-case chỉ
- Không space, không uppercase
- Match folder name

**Ví dụ đúng:**
```yaml
name: tao-ky-nang
name: linear-sprint-planner
name: figma-design-export
```

**Ví dụ sai:**
```yaml
name: Tao Ky Nang              # Space + uppercase
name: tao_ky_nang              # Underscore
name: tao-ky-nang-v2.0         # Dot
```

### `description` (Bắt buộc)

**Yêu cầu:**
- Max 1024 ký tự
- Bao gồm:
  - **CÁI GÌ:** Nó làm gì?
  - **KHI NÀO:** Khi nào dùng?
- Include trigger phrases người dùng sẽ nói
- Include file types nếu áp dụng

**Ví dụ tốt:**
```yaml
description: Quan ly Linear sprint planning, tao task, theo doi 
trang thai. Su dung khi "sprint planning", "create tasks", 
"project planning".
```

```yaml
description: Export Figma design va tao handoff doc cho 
developers. Su dung khi "design handoff", "export Figma", 
"tao spec design".
```

**Ví dụ xấu:**
```yaml
# Quá chung
description: Giup voi cac du an.

# Thiếu trigger
description: Tao cac task du an

# Quá kỹ thuật
description: Implements project entity model with 
hierarchical relationships
```

### `license` (Tùy chọn)

Chỉ dùng khi chia sẻ công khai:

```yaml
license: MIT
license: Apache-2.0
license: GPL-3.0
```

### `metadata` (Tùy chọn)

Thông tin bổ sung:

```yaml
metadata:
  author: Tên Công Ty
  version: 1.0.0           # Cập nhật mỗi lần release
  category: productivity   # hoặc development, design
  tags: [automation, workflow]
  documentation: https://...
  support: support@...
```

---

## Hạn Chế Bảo Mật

### ❌ KHÔNG ĐƯỢC DÙNG

```yaml
# Dấu XML
description: Tao <html> hoặc <xml> documents

# Tên có "claude" hoặc "anthropic"
name: claude-skill-maker
name: anthropic-helper

# Code thực thi
name: "my-skill'; system('rm -rf /')"
```

### ✅ ĐƯỢC

```yaml
# Bất kỳ YAML type
metadata:
  tags: [tag1, tag2]
  count: 42
  enabled: true

# Custom fields
metadata:
  custom-key: custom-value
```

---

## Ví Dụ Thực Tế

### Ví dụ 1: Marketing Automation

```yaml
---
name: email-campaign-builder
description: Tao va quan ly email campaigns voi segmentation, 
scheduling, tracking. Su dung khi "tao email campaign", 
"schedule email", "create newsletter".
license: MIT
metadata:
  author: Marketing Team
  version: 1.0.0
  category: marketing
  tags: [email, automation]
---
```

### Ví dụ 2: Development

```yaml
---
name: github-pr-reviewer
description: Review PR, analyze diffs, check style, suggest 
improvements. Su dung khi "review PR", "check code", "PR analysis".
license: Apache-2.0
metadata:
  author: Engineering Team
  version: 1.2.1
  category: development
  tags: [code-review, github]
---
```

### Ví dụ 3: Design

```yaml
---
name: figma-component-sync
description: Sync components tu Figma, tao storybook, generate 
Tailwind. Su dung khi "sync Figma", "export tokens", "design to code".
metadata:
  author: Design Systems
  version: 1.0.0
  category: design
  tags: [design-systems, figma]
---
```

---

## Debugging YAML

### Lỗi Phổ Biến

#### 1. Dấu Phân Cách Bị Thiếu

```yaml
# Sai
name: my-skill
description: Does things
---

# Đúng
---
name: my-skill
description: Does things
---
```

#### 2. Dấu Ngoặc Không Đóng

```yaml
# Sai
description: "Does something

# Đúng
description: "Does something"
```

#### 3. Indentation Sai

```yaml
# Sai
metadata:
author: John              # Missing indent
version: 1.0.0

# Đúng
metadata:
  author: John
  version: 1.0.0
```

#### 4. Colon Bị Thiếu

```yaml
# Sai
name my-skill
description Does things

# Đúng
name: my-skill
description: Does things
```

---

## Công Cụ Kiểm Tra

```bash
# Validate YAML
python -m yaml SKILL.md

# Online: yamllint.com
# Online: onlineyamltools.com
```

---

## Mẹo Hay

### 1. Long Description

Nếu quá dài:

```yaml
description: Tao email campaigns voi segmentation, scheduling, 
tracking va analytics. Su dung khi "email campaign", "newsletter", 
"email automation".
```

### 2. Multiple Tags

```yaml
metadata:
  tags: [automation, workflow, integration]
```

### 3. Versioning

```yaml
metadata:
  version: 1.0.0  # Initial
  version: 1.0.1  # Bug fix
  version: 1.1.0  # Feature
  version: 2.0.0  # Breaking change
```

---

*Last updated: March 2026*
