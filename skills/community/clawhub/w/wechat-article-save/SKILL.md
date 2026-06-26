---
name: wechat-article-save
description: 微信公众号文章保存工作流。当用户发送微信公众号文章链接（以 https://mp.weixin.qq.com 开头）时，自动执行：抓取正文 → 保存 Markdown 到知识库 →（可选）推送链接到飞书多维表格 →（可选）生成独立发芽笔记。触发词：微信文章链接、公众号文章、mp.weixin.qq.com。
---

# 微信公众号文章保存工作流

收到微信文章链接后，按以下步骤执行。

---

## 配置项（必须填写）

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `{{OBSIDIAN_ROOT}}` | Obsidian 根目录（末尾无斜杠） | `/Users/xxx/Documents/notes` |
| `{{WECHAT_ARTICLE_SUBPATH}}` | 公众号文章保存子目录 | `09_知识库/02_公众号文章` |
| `{{SPROUT_PROMPT_PATH}}` | 发芽笔记提示词路径（默认已设，无需修改） | `{{OBSIDIAN_ROOT}}/06_提示词库/文章内容处理/🌱发芽笔记.md` |
| `{{FEISHU_APP_TOKEN}}` | 飞书多维表格 app_token（不使用则留空） | `Y98wbR6wAa86JgsXYoScqGLXnOf` |
| `{{FEISHU_TABLE_ID}}` | 飞书 table_id（不使用则留空） | `tbljrD0L57sMwcP0` |
| `{{FEISHU_FIELDS}}` | 飞书字段名映射（不使用则留空） | 见下方 |
| `{{BAOYU_SCRIPT_PATH}}` | baoyu 脚本路径（可选，不填则用默认方式抓取） | `~/.openclaw/sandboxes/xxx/skills/baoyu-url-to-markdown/scripts/main.ts` |

**飞书字段名映射格式**（`{{FEISHU_FIELDS}}`，JSON 格式）：
```json
{
  "article_link": "文章链接",
  "title": "标题",
  "full_text": "全文",
  "processing_status": "处理状态",
  "publish_status": "发布状态",
  "failure_reason": "失败原因",
  "retry_count": "重试次数",
  "notes": "附注"
}
```

---

## Step 1 — 识别 & 解析链接

- 触发条件：URL 以 `https://mp.weixin.qq.com/` 开头
- **首选抓取方式**：使用 **baoyu-url-to-markdown**（Chrome CDP 模式）
  ```bash
  npx -y bun {{BAOYU_SCRIPT_PATH}} <url> -o /tmp/wechat-article.md --timeout 60000
  ```
- **fallback 链**：
  1. baoyu 失败 → Jina Reader：`https://r.jina.ai/<url>`
  2. Jina Reader 仍失败 → 用 `browser` 打开页面并抓取正文
- 从 front matter 和正文中提取：`title`（标题）、`author`（作者）、`published`（发布日期，若无则用当天日期）
- 可额外提取：`source`（来源/公众号名），若无则回退为"微信公众号"

---

## Step 2 — 构造文件名并保存 Obsidian

**目录**：`{{OBSIDIAN_ROOT}}/{{WECHAT_ARTICLE_SUBPATH}}/`

**命名格式**：`{日期}_{作者}_{标题}.md`
- 日期格式：`YYYYMMDD`
- 作者若为空则用"未知作者"
- 标题清理：去掉文件名非法字符（`/ \ : * ? " < > |`），过长截断至 100 字符以内
- 所有空格替换为连字符 `-`

**文件内容**：使用抓取到的 Markdown（保留 front matter），文件开头必须保留原文链接。

**冲突处理**：若同名文件已存在，文件名末尾加 `-1` `-2` 递增。

---

## Step 3 —（可选）推送链接到飞书多维表格

**条件**：`{{FEISHU_APP_TOKEN}}` 和 `{{FEISHU_TABLE_ID}}` 均已填写。

**写入方式**：
1. 用 `feishu_bitable_create_record` 创建一条新记录
2. 写入字段（字段名以 `{{FEISHU_FIELDS}}` 中配置为准）：
   - `文章链接`：填入原始微信文章 URL（格式 `https://mp.weixin.qq.com/s/xxx`）
   - `标题`：填入提取的文章标题
   - `全文`：留空（可由后续 pipeline 回填）
   - 若表格里存在以下字段，同时写入：
     - `处理状态` = `new`
     - `发布状态` = `draft`
     - `失败原因` = 空
     - `重试次数` = `0`

**非公众号链接复用**：如果不是公众号链接，但用户明确要求"按公众号版本处理"，同样写入此表，并在 `附注` 字段注明"按公众号版本处理"。

---

## Step 4 —（可选）生成独立发芽笔记

**条件**：`{{SPROUT_PROMPT_PATH}}` 文件存在。

### 4.1 何时跳过

- 用户明确说"仅保存"或"不发芽"时跳过
- 跳过时需在 Step 5 回复中注明

### 4.2 发芽提示词来源

路径：`{{SPROUT_PROMPT_PATH}}`

提示词核心框架为"材料发芽器"结构，包含：
- 步骤1：材料内容理解与提取
- 步骤2：发芽方向识别与选择（深度解读、横向关联、批判性视角、实践应用、哲学升华）
- 步骤3：故事化扩展生成（种子→故事→Aha瞬间的叙事结构）
- 步骤5：思考空间生成

### 4.3 生成流程

1. **读取提示词**：从上述路径读取完整的发芽提示词内容
2. **组织输入**：将已保存的文章 Markdown 内容（不含发芽笔记部分）作为"材料"输入给模型
3. **调用模型**：使用默认模型生成发芽报告，使用以下格式组织 prompt：
   ```
   # 角色
   [从提示词库读取的完整角色定义]

   # 任务
   [从提示词库读取的任务定义]

   # 输入材料
   [文章标题]
   [文章正文内容]

   # 输出要求
   [从提示词库读取的输出要求]
   ```
4. **保存发芽笔记文件**：
   - 目录：`{{OBSIDIAN_ROOT}}/{{WECHAT_ARTICLE_SUBPATH}}/`
   - 文件名：`{文章标题}__🌱发芽笔记.md`
     - 标题清理：去掉文件名非法字符，过长截断至 80 字符以内，空格替换为 `-`
     - 与主文章文件名不冲突，因为多了 `__🌱发芽笔记` 后缀
   - 文件内容直接写入模型输出的发芽报告
   - 若同名文件已存在，文件名末尾加 `-1` `-2` 递增

### 4.4 质量要求

- 发芽报告应为完整的"发芽报告"格式，包含材料核心 + 2-3个发芽方向（每个含种子+故事+Aha瞬间）+ 思考空间
- 总字数约 800-1500 字
- 语言：简体中文
- 故事必须有具体事实支撑，不可空洞

---

## Step 5 — 完成后回复

回复用户，格式：
> ✅ 已保存  
> **标题**：《{文章标题}》  
> **作者**：{作者}  
> **文章路径**：`{{WECHAT_ARTICLE_SUBPATH}}/{文章文件名}.md`  
> **发芽笔记**：`{{WECHAT_ARTICLE_SUBPATH}}/{发芽文件名}.md`（若已生成）  
> **飞书**：已推送/未配置（按实际情况）  
> **发芽**：已生成/已跳过（按用户要求）

如有错误，清楚说明哪一步失败、原因是什么。

---

## Step 6 —（可选）删除记录

**触发条件**：用户明确要求删除某条记录。

**执行步骤**：

1. **定位记录**：用 `feishu_bitable_list_records` 查询多维表格，找出 record_id 和对应标题
   - app_token：`{{FEISHU_APP_TOKEN}}`
   - table_id：`{{FEISHU_TABLE_ID}}`
   - 在输出中搜索标题，找到对应的 record_id

2. **确认删除**：告知用户找到的记录，请用户确认是否删除

3. **执行删除**：
   ```bash
   lark-cli base +record-delete \
     --base-token {{FEISHU_APP_TOKEN}} \
     --table-id {{FEISHU_TABLE_ID}} \
     --record-id <record_id> \
     --yes
   ```

4. **完成回复**：告知用户删除结果

> ✅ 已删除：《{文章标题}》

---

## 附录：已知的坑

1. **baoyu Chrome CDP 冲突**：baoyu 使用 Chrome CDP 端口，与 OpenClaw browser 可能冲突。优先使用 baoyu 抓取，若失败再用 browser fallback。
2. **飞书/Notion 可选**：如未配置对应 token，相关步骤自动跳过，不影响核心保存功能。
3. **文件名冲突**：同名文件加 `-1` `-2` 后缀递增，避免覆盖。