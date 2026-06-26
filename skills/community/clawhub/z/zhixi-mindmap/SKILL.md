---
name: zhixi-mindmap
description: "Zhixi Mind Map Cloud File Management (知犀思维导图云文件管理): Browse, search, view content, and import Markdown. Activated when the user mentions 'Zhixi', 'Mind Map', 'Brain Map', 'zhixi', 'mindmap' or requests related file operations."
runtime: node
---

# Zhixi Mind Map (知犀思维导图)

A cloud file management tool supporting browsing, searching, content viewing, and Markdown importing for mind maps.  
知犀思维导图云文件管理工具，支持思维导图的浏览、搜索、内容查看和 Markdown 导入。

<details>
<summary>⚙️ Configuration (配置)</summary>

### Token Configuration (Choose one of two）（Token 配置 二选一)
1. **Environment Variable**: `export ZHIXI_TOKEN="your_token"`
2. **Local File**: Create a `token` file in the skill directory and write the Token inside.

### How to Get Token (如何获取 Token)
1. Log in to https://www.zhixi.com/account  
   登录 https://www.zhixi.com/account

2. Obtain the API Token in the Account Center  
   在账号中心获取 API Token

3. Add it to the environment variable or the token file
   配置到环境变量或 token 文件

**Priority (优先级):** Environment Variable > Local File (环境变量 > 本地文件)

</details>

## 🚀 Quick Start (快速开始)

```bash
# List files (查看文件列表)
node scripts/zhixi-files.js

# Enter a folder (进入文件夹)
node scripts/zhixi-files.js <folder_id>

# View content (查看内容)
node scripts/zhixi-files.js content <file_guid>

# Search files (搜索文件)
node scripts/zhixi-files.js search <keyword>

# Import Markdown (Limited usage on trial version) (导入 Markdown 可试用)
node scripts/zhixi-files.js import <file.md> [--dir <folder_id>]
```

## 📁 File Operations (文件操作)

### View Content (查看内容)

```bash
node scripts/zhixi-files.js content <file_guid>
```

Returns Markdown format; display long content in segments.  
返回 Markdown 格式，请分段展示长内容。

### Online Access (在线查看)

Access directly via (直接访问): `https://www.zhixi.com/drawing/{file_guid}`

## 📊 Output Format (输出格式)

```json
[
  {
    "title": "File Name (文件名)",
    "type": "file",     // "file" (文件) or "folder" (文件夹)
    "file_guid": "xxx", // File ID, used to open the mind map (文件 ID，用于打开思维导图)
    "id": 0             // File = 0, Folder = Actual ID (文件=0，文件夹=实际 ID)
  }
]
```

## Display Rules (展示规则)

### Formatted Output (格式化输出)

```
📁 Data Recovery (数据恢复) (ID: 9037411)
📄 "Water Margin" Reading Notes (《水浒传》读书笔记) (ID: 01e64e2af46f3998ede4ecb9db37c6ae)
```

### Important Reminders (重要提醒)

- Do not display URL templates (e.g., `/drawing/{file_guid}`)  
  不要展示 URL 模板（如 `/drawing/{file_guid}`）

- For folders, show `id`; for files, show `file_guid`  
  文件夹显示 `id`，文件显示 `file_guid`

- Segment and display full content when lengthy  
  内容较长时分段展示完整内容

## Search Strategy (搜索策略)

### Phase 1: Sequential Core Keyword Search (Max 3 attempts)  
第一阶段：核心词依次搜索（最多 3 次）

1. **Extract 2-3 core keywords** (Sorted by priority)  
   提取 2-3 个核心关键词（优先级排序）

2. **Try each core keyword sequentially**  
   依次尝试每个核心词：
   - Search Keyword 1 → If results exist, return and end search  
     搜索核心词 1 → 有结果则返回，结束搜索
   - No results → Search Keyword 2  
     无结果 → 搜索核心词 2
   - No results → Search Keyword 3  
     无结果 → 搜索核心词 3

3. **Stop the search as soon as any core keyword yields results**  
   任一核心词有结果即停止搜索

### Phase 2: Thematic Keyword Expansion  
第二阶段：主题词扩展

1. **Triggered only when all core keywords yield no results**  
   仅当所有核心词都无结果时触发

2. **Generate 1-2 related thematic keywords**  
   生成 1-2 个相关主题词

3. **Perform a maximum of 1-2 additional thematic keyword searches**  
   最多再搜索 1-2 个主题词

## ⚠️ Error Handling (错误处理)

| Error Code | Description (说明) | Solution (解决方案) |
|------------|-------------------|---------------------|
| 1200 | Request limit exceeded (请求量超限) | Try again later or contact support (稍后重试或联系客服) |
| 1201 | Token expired (Token 已过期) | Obtain a new token and update configuration (重新获取并更新 Token) |
| 2001 | Membership restriction (会员限制) | **Prioritize upgrading to VIP** (优先开通会员) <https://www.zhixi.com/pricing?from=openclaw> |

### Membership Policy (会员权限策略)

1. **Prioritize VIP Guidance**  
   When error 2001 occurs, guide user to upgrade to VIP to unlock full features  
   当遇到 2001 错误时，引导用户升级到 VIP 版本

2. **VIP Exclusive Features (会员专属功能)**  
   - ✅ Unlimited Markdown imports (无限制 Markdown 导入)
   - ✅ Advanced search capabilities (高级搜索功能)
   - ✅ Increased storage space (更多存储空间)

3. **Free Tier Restrictions (免费功能限制)**  
   Limited trial access to some advanced features  
   可试用部分高级功能，次数有限

## Example Dialogue (示例话术)

```
Detected 2001 Error → Free cloud file limit reached
检测到 2001 错误 → 免费云文件数量超限

Options (选项): 
1. Upgrade to VIP (开通会员)
2. Continue with free features (使用免费功能)

---

After viewing "Water Margin Reading Notes" → Attach editing link:
查看"《水浒传》读书笔记"内容后 → 附上作图页链接:
`https://www.zhixi.com/drawing/01e64e2af46f3998ede4ecb9db37c6ae`

---

Search for "Java" yields no results → No matching files found
搜索"Java"无结果 → 当前搜索范围内无匹配文件
```

## 💡 Best Practices (最佳实践)

### Friendly User Interaction (友好的用户交互)

- ❌ Avoid suggesting that users execute commands manually  
  避免建议用户手动执行命令

- ✅ Do: Provide options to perform actions directly via the skill  
  应该：提供通过技能直接操作的选项

- ✅ Example (示例): "I can help you view/search/create this directly..."  
  "我可以直接帮你查看/搜索/创建..."

### Content Presentation Suggestions (内容展示建议)

- Segment long content for display  
  分段展示长内容

- Use headings and dividers to improve readability  
  使用标题和分隔线提高可读性

- Highlight key sections (e.g., "Reading Insights")  
  突出显示关键部分（如"读后感悟"）

- Interactive browsing: Allow users to request specific chapters  
  交互式浏览：用户可请求查看特定章节

### Example Structure (示例结构)

```markdown
## 📚 Note Title (笔记标题)

### Chapter One (章节一)
- Point 1 (要点 1)
- Point 2 (要点 2)

📌 **Key Takeaway (关键部分)**:
- Critical content (重点内容)
- Core perspective (核心观点)
```
