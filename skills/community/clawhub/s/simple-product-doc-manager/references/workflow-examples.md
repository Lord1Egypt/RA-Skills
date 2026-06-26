# Workflow Examples | 工作流示例

## Example 1: Creating a New Project Knowledge Base

### Step 1: Create Knowledge Base

Use Feishu API to create a new knowledge base:

```bash
curl -X POST "https://open.feishu.cn/open-apis/wiki/v2/spaces" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Project Knowledge Base",
    "description": "Product documentation and requirements management"
  }'
```

### Step 2: Create Core Documents

Create the three ongoing documents using `feishu_doc` tool:

```json
{
  "action": "create",
  "title": "需求思考 | Requirements Thinking",
  "folder_token": "SPACE_TOKEN"
}
```

```json
{
  "action": "create", 
  "title": "项目地址和代码逻辑记录 | Project & Code Logic",
  "folder_token": "SPACE_TOKEN"
}
```

```json
{
  "action": "create",
  "title": "配置信息记录 | Configuration Records", 
  "folder_token": "SPACE_TOKEN"
}
```

### Step 3: Create Product Requirements Folder

Create a folder/document group for PRDs:

```json
{
  "action": "create",
  "title": "产品需求文档 | Product Requirements",
  "folder_token": "SPACE_TOKEN"
}
```

---

## Example 2: Adding a New Requirement

### Step 1: Create Requirements Document

```json
{
  "action": "create",
  "title": "2026-3-26-user-authentication-v1",
  "folder_token": "PRD_FOLDER_TOKEN"
}
```

### Step 2: Write Initial Requirements

```json
{
  "action": "write",
  "doc_token": "DOC_TOKEN",
  "content": "# 用户认证功能 | User Authentication Feature\n\n**Status**: 撰写中 | Drafting\n**Created**: 2026-03-26\n**Owner**: @username\n\n## Background | 背景\n\n[Describe the problem or opportunity]\n\n## Requirements | 需求\n\n### Functional Requirements | 功能需求\n\n1. **Login with phone number**\n   - Support SMS verification\n   - Rate limiting: 3 attempts per minute\n\n2. **Login with password**\n   - Minimum 8 characters\n   - Must include letters and numbers\n\n### Non-Functional Requirements | 非功能需求\n\n- Response time < 200ms\n- Support 10,000 concurrent users\n\n## Acceptance Criteria | 验收标准\n\n- [ ] SMS login works end-to-end\n- [ ] Password login works end-to-end\n- [ ] Rate limiting enforced\n- [ ] Unit tests coverage > 80%\n\n## Notes | 备注\n\n[Any additional context]"
}
```

### Step 3: Update Requirements Thinking Document

Add context to the requirements thinking doc:

```json
{
  "action": "append",
  "doc_token": "THINKING_DOC_TOKEN",
  "content": "\n## 2026-03-26: User Authentication\n\n**Problem**: Users currently cannot save their progress without authentication.\n\n**Considerations**:\n- Phone login is preferred in China\n- SMS costs should be monitored\n- Need fallback for international users\n\n**Decision**: Implement phone + password login first, add email later."
}
```

---

## Example 3: Finalizing a Requirement

### Step 1: Update Document Status

When code is complete and approved, update the document:

```json
{
  "action": "write",
  "doc_token": "DOC_TOKEN",
  "content": "# 用户认证功能 | User Authentication Feature\n\n**Status**: 已定型 | Finalized ✅\n**Created**: 2026-03-26\n**Finalized**: 2026-03-28\n**Owner**: @username\n\n## Background | 背景\n\n[Original content...]\n\n## Implementation Notes | 实现记录\n\n- API endpoint: `/api/v1/auth/login`\n- Database table: `users`\n- SMS provider: Aliyun\n\n---\n\n*This document is finalized. For iterations, create a new version.*"
}
```

### Step 2: Update Code Logic Document

```json
{
  "action": "append",
  "doc_token": "CODE_DOC_TOKEN",
  "content": "\n## User Authentication Implementation\n\n**Files**:\n- `src/services/auth.ts` - Main authentication logic\n- `src/routes/auth.ts` - API routes\n- `src/models/user.ts` - User data model\n\n**Key Functions**:\n- `sendSMS(phone)` - Sends verification code\n- `verifyCode(phone, code)` - Validates SMS code\n- `createUser(phone)` - Creates new user record\n\n**Database Schema**:\n```sql\nCREATE TABLE users (\n  id UUID PRIMARY KEY,\n  phone VARCHAR(20) UNIQUE,\n  password_hash VARCHAR(255),\n  created_at TIMESTAMP\n);\n```"
}
```

---

## Example 4: Starting a New Iteration

When the same feature needs changes after being finalized:

### Step 1: Create New Version Document

```json
{
  "action": "create",
  "title": "2026-4-5-user-authentication-v2",
  "folder_token": "PRD_FOLDER_TOKEN"
}
```

### Step 2: Reference Previous Version

```json
{
  "action": "write",
  "doc_token": "NEW_DOC_TOKEN",
  "content": "# 用户认证功能 V2 | User Authentication Feature V2\n\n**Status**: 撰写中 | Drafting\n**Created**: 2026-04-05\n**Previous Version**: 2026-3-26-user-authentication-v1 (Finalized)\n**Owner**: @username\n\n## Changes from V1 | V1 的变更\n\n### New Requirements | 新增需求\n\n1. **Add email login option**\n   - For international users\n   - Optional, phone remains primary\n\n2. **Social login**\n   - WeChat integration\n   - Apple Sign-In for iOS\n\n### Modified Requirements | 修改需求\n\n- Rate limiting: Changed from 3/min to 5/min (user feedback)\n\n### Unchanged | 保持不变\n\n- Password requirements\n- Response time requirements\n\n## Full Requirements | 完整需求\n\n[Include all requirements, not just changes]"
}
```

---

## Quick Reference: Document States

| Action | Document State | Next Step |
|--------|---------------|-----------|
| Create new requirement | Drafting | Write requirements |
| Code in development | Drafting | Update code logic doc |
| Code approved by user | Finalized | Lock document |
| Need changes to finalized | - | Create v2 document |
