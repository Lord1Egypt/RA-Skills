---
name: visnote-image-creator
version: v1.0.0
description: This skill should be used when generating XiaoHongShu (小红书) style images. The AI analyzes user requirements, reads template registry to select appropriate template, extracts and merges data with template defaults, and invokes generation script with properly constructed command-line arguments.
---

# VisNote Images Creator

This skill automates generation of XiaoHongShu-style images by combining AI intelligence with Playwright-driven browser automation. The AI analyzes user requests, selects templates from live registry, and orchestrates image generation process.

## When to Use This Skill

Use this skill when:
- User requests to generate XiaoHongShu-style images
- User provides content descriptions (titles, tags, body text, etc.)
- User mentions template types (避坑, 干货, OOTD, etc.) or specific keywords
- Creating social media cover images or content visuals
- Automating batch image production for content creation

## AI Workflow

### 0. Prerequisites Check (MANDATORY)

**Before processing any user request, check the following:**

1. **Check API KEY in config.json:**
   ```bash
   cat config.json
   ```
   - If file doesn't exist or `apikey` field is empty: **STOP** and inform user:
     ```
     ⚠️ 需要先在 config.json 中设置 apikey 才能使用图片生成功能。

     请按以下步骤设置：
     1. 访问 VisNote 个人主页获取 API Key：https://vis-note.netlify.app/profile，复制 API Key
     2. 复制项目根目录的 example-config.json 文件，并重命名为 config.json
     3. 将复制的 API Key 填入 config.json 的 "your_api_key_here" 位置

     设置完成后，再次尝试生成图片。
     ```
   - If file exists and `apikey` is set: Proceed with step 1

### 1. Analyze User Request

Extract following information from user's request:
- **Content Type**: 避坑/干货/教程, OOTD/探店, 语录/情感, 故事/对话, etc.
- **Text Content**: Title, subtitle, body text, tag, author mentions
- **Keywords**: Specific terms that map to template categories
- **Format Preferences**: Cover style, comparison style, list style, etc.
- **Output Path** (optional): If user explicitly specifies custom output path, use it; otherwise generate timestamped filename

### 2. Get Template Registry from API

**Fetch the template list from the API:**
```
GET /api/open/templates
```

**Caching Strategy (IMPORTANT):**

**First request in conversation:** Always fetch the latest template list from the API.

**Subsequent requests in the same conversation:**
- If the user asks to "换个模板" (change template), "再生成一张" (generate another), or similar follow-up requests → **Reuse the previously fetched template list** from this conversation
- If the user provides a completely new topic/content request → **Fetch the latest template list** from the API again

**Examples of cache reuse:**
- "换个模板" → use cached template list
- "再生成一张" → use cached template list
- "换个风格" → use cached template list
- "用其他模板试试" → use cached template list

**Examples of cache invalidation (fetch new):**
- "生成一张关于xxx的新封面" (new topic) → fetch new template list
- "帮我做一个关于yyy的图" (new content) → fetch new template list
- User starts a completely new generation task → fetch new template list

**Optional query parameters:**
- `keyword`: Search by template name/desc/tags (e.g., `?keyword=封面`, `?keyword=正文`)

**Example using curl:**
```bash
# Get all templates
curl "https://vis-note.netlify.app/api/open/templates"

# Search for cover templates
curl "https://vis-note.netlify.app/api/open/templates?keyword=封面"
```

**Response structure:**
```json
{
  "success": true,
  "data": [
    {
      "id": "yellow",
      "name": "高对比大字报",
      "desc": "适合：避坑/干货/教程",
      "image": "https://...",
      "tags": ["封面"],
      "value": {
        "title": "示例标题",
        "subtitle": "示例副标题",
        "tag": "标签",
        "color": "#EAB308"
      }
    }
  ]
}
```

**Template object fields:**
- `id`: Unique identifier (used in `--template` parameter)
- `name`: Template display name
- `desc`: Description with use case patterns (e.g., "适合：避坑/干货/教程")
- `tags`: Classification tags (免费, VIP, 封面, 图片)
- `value`: Default data structure with all available fields for the template(used in `--data` parameter)

**Critical**: 
- Always call this API at runtime to get latest template configurations. Do NOT hardcode template information in responses.
- **Apply caching strategy**: Reuse template list within the same conversation for follow-up requests to avoid redundant API calls.

### 3. Select Appropriate Template

Analyze templates from the registry array and select based on:

#### Template Selection Logic

1. **Direct ID Match**: If user specifies template ID (e.g., "使用 yellow 模板"), find template with matching `id` field and use it directly
2. **Tag-Based Selection (Priority)**:
   - **For covers/focus images**: Select templates with `'封面'` in `tags` field
   - **For body/content images**: Select templates without `'封面'` tag, or with `'图片'` tag
   - **For images with main photo**: Select templates with `'图片'` in `tags` field
   - **For comparison content**: Select templates with `'对比'` keyword in `desc` or name
   - **For tutorial/step content**: Select templates with `'步骤'` keyword in `desc` or name
3. **Category Match**: Search template `desc` field for keywords like 避坑, 干货, OOTD, 情感, etc. that match user request
4. **Format Match**: Match format preferences from user request (对比, 封面, 清单, etc.)
5. **Content Match**: For tool/software content (Chrome插件, etc.), prefer templates with `desc` containing 工具/清单/测评
6. **Fallback**: Default to `yellow` for high-contrast visibility

#### Tag-Based Selection Examples

**Scenario 1: Generating Cover + Content Images**
- Cover: Use template with `tags: ['封面']` (e.g., yellow, magazine, laser-holographic, etc.)
- Content: Use template without '封面' tag (e.g., glass, memo, newspaper, etc.)

**Scenario 2: Image with Main Photo**
- Use template with `tags: ['图片']` (e.g., tape-polaroid, soft-glass-border, etc.)

**Scenario 3: Comparison/Before-After Content**
- Look for templates with '对比' in `desc` or name (e.g., classic-before-after, polaroid-before-after)

**Scenario 4: Tutorial/Step Content**
- Look for templates with '步骤' in `desc` or name (e.g., single-image-step, double-row-step, sidebar-nav-step)

#### Template Analysis Process

For each template in the registry array:
1. Read `desc` field to understand use cases (format: "适合：类别1/类别2/类别3")
2. Read `tags` field to understand classification (免费, VIP, 封面, 图片)
3. Read `value` field to understand data structure and available fields
4. Match against user request using above selection logic

### 4. Extract User Data and Merge with Template Defaults

**Critical**: The template's `value` object is the foundation - it contains ALL default values including default images, colors, text, etc. Always start with this complete object and only override what user explicitly provides.

#### Data Extraction Rules

**Title Extraction:**
- Explicit title format: `标题是"xxx"` or `标题是'xxx'`
- Quoted content: Look for content in quotes that seems like a title
- If not specified: Use template's `value.title` (template default)

**Subtitle/Body Text Extraction:**
- Check if template's `value` has `subtitle` or `bodyText` fields
- If user explicitly provides subtitle/body: use user value
- If user doesn't explicitly provide but mentions secondary content (e.g., "OOTD 穿搭封面"):
  - Extract from description and fill appropriate field
  - Example: "生成 OOTD 穿搭封面" → `subtitle` could be "穿搭分享 | 日常记录"
  - Example: "日常碎碎念" → `bodyText` could be "今天天气真好\n心情超级棒"
- If no user content available: Use template's `value.subtitle` or `value.bodyText` (template default)

**Image Fields (Critical):**
- Check if template's `value` contains `image`, `image2`, etc.
- **Always keep template default images** if user doesn't explicitly provide their own image paths
- Template defaults ensure template works without user-supplied images
- Example: Magazine template has `image: '/images/jimeng-20260125.png'` → keep this unless user specifies otherwise

**Tag Extraction:**
- Look for category tags: 干货, 教程, 避坑, 分享, 笔记, 生活, 日常, etc.
- Format as "xxx分享" if needed
- If not specified: Use template's `value.tag` (template default)

**Author Extraction:**
- Extract @mentions: @username patterns
- Set as `author` field if template supports it
- If not specified: Use template's `value.author` if exists (template default)

**Color Extraction:**
- Look for hex color codes: #RRGGBB format
- Set as `color` field if template supports it
- If not specified: Use template's `value.color` if exists (template default)

**Template-Specific Fields:**
- Identify ALL fields present in template's `value` object
- For each field:
  - If user explicitly provides value: use user value
  - If user doesn't provide: use template's default value
- Examples: `image`, `image2` for comparison styles; `step` for tutorial styles

#### Merge Strategy

1. **Start with template defaults**: Copy the **entire** `value` object from selected template - this is your foundation and includes all required fields
2. **Extract user-provided values**: Identify what the user explicitly wants to override (title, color, etc.)
3. **Smart fill for missing fields**: If user mentions relevant content but doesn't specify exact field, intelligently assign:
   - Example: User says "生成 OOTD 穿搭" + title is provided
     → If template has `subtitle`, fill it with "穿搭分享 | 日常记录"
     → If template has `tag`, fill it with "生活分享"
4. **Override with user data**: Replace fields where user provided explicit values
5. **Keep ALL template defaults**: Never remove fields that exist in template's `value` - use template defaults for unspecified fields
6. **Validate structure**: Ensure final data object matches template's expected structure exactly

### 5. Construct Command

Build command with proper JSON escaping:

```bash
node scripts/generate-image.mjs \
  --template <templateId> \
  --data '<json_data>' \
  --out <absolute-output-path> \
```

#### Parameter Requirements

- `--template`: Required. Use the `id` field from selected template
- `--data`: Required if overriding defaults. JSON string from merged data object
- `--out`: Optional.
  - If user explicitly specifies output path: use user-provided path
  - If user does NOT specify output path: generate filename as `visnote-YYYYMMDDHHmmss.png` where YYYYMMDDHHmmss is current timestamp in that format
  - Use project's default output directory (e.g., `~/Downloads/`) for the full absolute path

**Note:** API key is automatically read from `config.json`, no need to pass it as a parameter.

#### JSON Construction

- Use the merged data object from step 4
- Ensure all field values match the template's `value` structure
- Properly escape special characters for shell command:
  - Wrap entire JSON in single quotes
  - Escape inner single quotes if present: `\'`
  - Escape newlines if present: `\\n`
  - Escape backslashes if present: `\\\\`

Example:
```bash
--data '{"title":"我的标题","subtitle":"副标题","color":"#EF4444"}'
```

### 6. Execute and Handle Output

Execute the constructed command:

1. **Run the command** with proper error handling
2. **Verify success** by checking exit code and output messages
3. **Report to user**:
   - Output file location
   - Template used (name and id)
   - Any relevant status messages
4. **Handle errors** with clear, actionable explanations:
   - Server startup issues
   - Template not found
   - Missing required fields
   - File permission issues

## Template Registry API

**Endpoint:** `GET /api/open/templates`

**Base URL:** `https://vis-note.netlify.app`

**Usage:**
```bash
# Get all templates
curl "https://vis-note.netlify.app/api/open/templates"

# Search templates by keyword
curl "https://vis-note.netlify.app/api/open/templates?keyword=封面"
```

**Call this API with caching strategy:**
- **First request or new topic**: Always fetch the latest template list
- **Follow-up requests** ("换个模板", "再生成一张", etc.): Reuse previously fetched template list from this conversation

This API is the single source of truth for:
- All available templates and their IDs
- Template descriptions and use cases
- Default data structure for each template (via `value` field)
- Field names and formats
- Tag classifications

**Never hardcode template information** in responses, as:
- Templates may be added or removed
- Template data structures may change
- Descriptions may be updated
- New fields may be added to `value` objects

**Caching benefits:**
- Reduces redundant API calls within the same conversation
- Improves response speed for follow-up requests
- Balances performance with data freshness (new topics still fetch latest data)

## Example AI Processing

### Example 1: Tool/Software Content

**User Request:** "帮我生成一张 Chrome插件 的图片，标题是 一键下载微博文章"

**AI Processing:**

1. **Analyze Request**: Tool/software content + specific title in quotes
2. **Fetch Template Registry**: Call `GET /api/open/templates` to get all templates
3. **Select Template**: Find template with `desc` containing 工具/清单/测评 (for tool/software content) → `academic-notes`
4. **Extract User Data**:
   - Title: "一键下载微博文章" (from `标题是"..."` pattern)
   - Tag: 提取"插件" → "插件分享"
5. **Merge with Template Defaults**:
   ```json
   {
     "title": "一键下载微博文章",  // user-provided
     "bodyText": "核心知识点一\n避坑指南二\n保姆级教程三",  // from template.value
     "tag": "插件分享",  // extracted + formatted
     "author": "@你的名字",  // from template.value
     "color": "#F59E0B"  // from template.value
   }
   ```
6. **Construct Command**:
   ```bash
   node scripts/generate-image.mjs \
     --template academic-notes \
     --data '{"title":"一键下载微博文章","bodyText":"核心知识点一\\n避坑指南二\\n保姆级教程三","tag":"插件分享","author":"@你的名字","color":"#F59E0B"}' \
     --out ~/Downloads/visnote-20260302143022.png
   ```
   *Note: Since user didn't specify output path, generated timestamped filename `visnote-20260302143022.png`*
7. **Execute**: Run command and report results to user

### Example 2: Tutorial with Explicit Template

**User Request:** "使用 yellow 模板生成一张干货封面，标题是3秒抓住用户注意力"

**AI Processing:**

1. **Analyze Request**: Explicit template ID specified + category + title
2. **Fetch Template Registry**: Call `GET /api/open/templates` to get all templates
3. **Select Template**: Find template with `id` = "yellow" → `yellow` template
4. **Extract User Data**:
   - Title: "3秒抓住用户注意力"
5. **Merge with Template Defaults**:
   ```json
   {
     "title": "3秒抓住用户注意力",  // user-provided
     "subtitle": "3秒抓住用户注意力 | 涨粉秘籍",  // from template.value
     "tag": "干货分享",  // extracted from "干货"
     "color": "#EAB308"  // from template.value
   }
   ```
6. **Construct Command**:
   ```bash
   node scripts/generate-image.mjs \
     --template yellow \
     --data '{"title":"3秒抓住用户注意力","subtitle":"3秒抓住用户注意力 | 涨粉秘籍","tag":"干货分享","color":"#EAB308"}' \
     --out ~/Downloads/visnote-20260302143022.png
   ```

### Example 3: Comparison Style

**User Request:** "生成一张装修前后对比图，标题装修改造"

**AI Processing:**

1. **Analyze Request**: Comparison content (前后对比) + title
2. **Fetch Template Registry**: Call `GET /api/open/templates` to get all templates
3. **Select Template**: Find template with `desc` containing 对比 or name containing 对比 → `classic-before-after`
4. **Extract User Data**:
   - Title: "装修改造"
5. **Merge with Template Defaults**:
   ```json
   {
     "title": "装修改造",  // user-provided
     "subtitle": "3秒抓住用户注意力 | 涨粉秘籍",  // from template.value
     "color": "#EF4444"  // from template.value
   }
   ```
6. **Construct Command**:
   ```bash
   node scripts/generate-image.mjs \
     --template classic-before-after \
     --data '{"title":"装修改造","subtitle":"3秒抓住用户注意力 | 涨粉秘籍","color":"#EF4444"}' \
     --out ~/Downloads/visnote-20260302143022.png
   ```

### Example 4: Batch Generation with Tag-Based Selection

**User Request:** "根据文档内容生成封面图和几张内容图，内容是关于小红书配图工具的"

**AI Processing:**

1. **Analyze Request**: Need cover image + multiple content images, topic is about xhs image tool
2. **Fetch Template Registry**: Call `GET /api/open/templates` to get all templates
3. **Select Templates**:
   - **Cover**: Find template with `tags` containing `'封面'` → `yellow` (high-contrast, eye-catching)
   - **Content**: Find template without '封面' tag, suitable for body text → `glass` (情绪磨砂玻璃, good for sharing)
4. **Generate Cover Image**:
   - Extract title: "做小红书配图终于省心了"
   - Extract tag: "实测分享"
   - Merge with yellow template defaults
   ```bash
   node scripts/generate-image.mjs \
     --template yellow \
     --data '{"title":"做小红书\n配图终于省心了","subtitle":"同一套模板搞定封面+正文","color":"#EAB308","tag":"实测分享"}' \
     --out ~/Downloads/visnote-20260302220201.png
   ```
5. **Generate Content Images** (using `glass` template, varying colors):
   - Image 1 (痛点): "以前的痛点" + subtitle about issues
   - Image 2 (新做法): "新的做法" + subtitle about solution
   - Image 3 (变化一): "变化一" + subtitle about benefit 1
   - Image 4 (变化二): "变化二" + subtitle about benefit 2
   - Image 5 (变化三): "变化三" + subtitle about benefit 3
   - Image 6 (建议): "建议" + subtitle about tips
6. **Important**: When generating multiple images, wait 10-15 seconds between requests to avoid Next.js server timeout

## Important Notes for AI

1. **Apply caching strategy** - Reuse template list within conversation for follow-up requests; fetch fresh data for new topics
2. **Always read template registry** - Never assume template structure
2. **Use absolute paths** for `--out` parameter
3. **Properly escape JSON data** - Single quotes for shell, escape inner quotes and newlines
4. **Default to free templates** unless user explicitly needs VIP features or specifies VIP template
5. **Extract @author mentions** from user requests
6. **Preserve line breaks** in titles using `\\n` when appropriate
7. **Match keywords carefully** - Consider content type, format, and user intent together
8. **Handle edge cases** - If no clear match, default to `yellow` template
9. **Verify command syntax** before execution, especially JSON escaping
10. **Respect template defaults** - Only override fields explicitly provided by user
11. **Use tags for smart selection**:
    - For covers: select templates with `'封面'` in `tags`
    - For images with photos: select templates with `'图片'` in `tags`
    - For content body: select templates without `'封面'` tag
    - For comparison: look for '对比' in `desc` or name
    - For tutorials/steps: look for '步骤' in `desc` or name
12. **Batch generation tip**: When generating multiple images, wait 10-15 seconds between requests to avoid Next.js server timeout

## Prerequisites for Execution

**IMPORTANT: API Key Required**

This skill requires the API key to be set in `config.json`. Without it, the image generation will fail.

### Setting API Key

**First-time setup:**
```bash
# Create or edit config.json in project root
cat > config.json << 'EOF'
{
  "apikey": "your_api_key_here"
}
EOF
```

**Verification:**
```bash
cat config.json
```

Ensure the file exists and contains a valid API key in the `apikey` field.

**Where to get your API key:**
- Visit VisNote profile page: https://vis-note.netlify.app/profile
- Copy the generated API Key

### API Key Validation

Before generating any image, the script will validate the API key by calling `${server}/api/open/check` endpoint. The following checks will be performed:

1. **API Key Existence**: Verifies the API key exists in the system
   - Error message: "API Key 不存在"
   - Solution: Check your API key in config.json, get a new key from profile page

2. **Membership Status**: Checks if user is a VIP member
   - Error message: "您还不是会员"
   - Solution: Subscribe to VIP membership

3. **Membership Expiry**: Checks if VIP membership is still valid
   - Error message: "您的会员已过期"
   - Solution: Renew your VIP membership

4. **Available Quota**: Checks if user has remaining image generation quota
   - Error message: "生图额度已用完"
   - Solution: Purchase additional quota or wait for quota reset

**Note**: All validation errors will stop the image generation process immediately with a clear error message.

### Other Requirements

- Playwright dependencies installed:
  ```bash
  npm install playwright
  npx playwright install chromium
  ```
- VisNote API endpoints are accessible:
  - Template list: `${server}/api/open/templates`
  - API key check: `${server}/api/open/check`

## Troubleshooting

### API Key Does Not Exist
**Error message:** "API Key 不存在"
- Verify config.json exists in project root: `cat config.json`
- Ensure `apikey` field is set with a valid API key
- Get a new API key from: https://vis-note.netlify.app/profile

### Not A VIP Member
**Error message:** "您还不是会员"
- Visit VisNote to subscribe to VIP membership
- Membership is required to use image generation service

### VIP Membership Expired
**Error message:** "您的会员已过期"
- Renew your VIP membership
- Check your membership expiration date in profile

### Insufficient Quota
**Error message:** "生图额度已用完"
- Purchase additional quota
- Wait for quota reset if applicable
- Check available quota in your account dashboard

### Missing #render Element
- Confirm `/editor` route exists
- Verify page contains required elements
- Check template ID validity

### Download Failures
- Verify browser download permissions
- Check output directory exists and is writable
- Ensure Next.js server is responding

### Template Not Found
- Verify template ID spelling
- Call template API to check available templates: `${server}/api/open/templates`
- Ensure template ID exists in the template registry
