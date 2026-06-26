---
name: xiaohongshu-publish-workflow
description: "小红书发布流水线：XHS排版→主编审核→自动化发布→数据复盘。在已有Markdown定稿基础上执行小红书格式化和发布。触发词：发布到小红书、小红书排版、小红书发布。需先完成内容创作。"
license: MIT
version: 1.0.0
---

# 小红书发布流水线

在已有 Markdown 定稿基础上，完成小红书笔记的排版格式化、发布和数据复盘。

## 前置条件

- 已通过 `/content-creation` 部署内容创作团队（墨白参与审核）
- 已通过 `/xiaohongshu-publisher-setup` 部署小红书发布团队（灵格、星阑）
- 已完成小红书登录初始化（`xhs_publish.cjs login`）
- 已有 Markdown 定稿（来自 `/content-workflow` 或用户直接提供）

## 工作流概述

```
定稿 → 灵格(XHS排版) → 墨白(审核) → 星阑(发布+复盘)
```

## Phase 3：小红书排版（灵格主导，墨白审核）

1. 灵格根据 Markdown 定稿完成小红书内容包：
   - **标题方案**：3-5 个标题，每个 ≤20 字，含 emoji，标注推荐（★）
   - **封面大字**：2-8 字冲击力短句（2-3 个方案）
   - **正文排版**：分段（≤3行/段）、emoji 标注、口语化改写、互动引导结尾
   - **话题标签**：5-10 个（热门+垂直+长尾，分层规划）
   - **配图建议**：3-9 张图的概念（第1张为封面，附文字叠加建议）
2. 提交给墨白审核
3. 最多迭代 2 轮
4. 输出：XHS 内容包定稿

## Phase 4：发布与复盘（星阑主导）

### 4.1 发布前准备

1. 星阑确定最佳发布时间，提交给用户确认
2. 验证登录状态：
   ```bash
   node {baseDir}/scripts/xhs_publish.cjs check-login
   ```
   - 未登录 → 提示用户运行：
     ```bash
     node {baseDir}/scripts/xhs_publish.cjs login
     ```
3. 用户准备好图片文件（按配图建议）

### 4.2 生成发布 JSON

星阑根据定稿内容生成 `content.json`：
```json
{
  "title": "最终确定的笔记标题（含emoji）",
  "body": "完整正文（含emoji排版和话题标签）",
  "tags": ["话题1", "话题2", "话题3"],
  "images": ["/path/to/cover.jpg", "/path/to/img2.jpg"],
  "type": "normal"
}
```

### 4.3 用户确认发布

1. 展示发布预览（标题、正文摘要、话题标签、图片数量、发布时间）
2. **必须获得用户明确确认后才能执行发布**

### 4.4 执行发布

用户确认后：
```bash
node {baseDir}/scripts/xhs_publish.cjs publish content.json
```

- 浏览器将自动打开，自动填写内容
- 填写完成后再次让用户在浏览器中确认，避免误操作
- 发布成功后记录笔记 ID 和发布时间

### 4.5 数据追踪与复盘

1. 发布后 24h 初步数据报告：
   ```bash
   node {baseDir}/scripts/xhs_publish.cjs get-note <笔记ID>
   ```
   - 核心指标：点赞、收藏、评论、涨粉
   - 初步判断：超预期 / 符合预期 / 低于预期

2. 发布后 48h 完整数据复盘报告：
   - 与近期历史均值对比
   - 数据洞察（突出/欠缺的指标及原因分析）
   - 至少 3 条可操作优化建议（按优先级排序）
   - 对下一篇内容的建议

3. 墨白主持复盘，确定下一轮选题优化方向

## 灵活调用规则

- 用户可以跳过排版（如"直接用这个格式发布"）→ 跳到 Phase 4
- 用户可以只做排版不发布（如"帮我排版小红书格式"）→ Phase 3 结束后停止
- 用户可以单独让星阑分析数据（如"帮我看一下这篇笔记的数据"）→ 直接执行数据查询
- 用户可以单独检查登录状态（如"检查一下小红书登录"）→ 执行 check-login

## 质量门控

- XHS 内容包需经墨白审核（标题、正文风格、话题标签合规性）
- 发布操作必须获得用户明确确认（两次：确认发布 + 浏览器内确认）
- 发现事实性错误 → 回退到内容创作阶段（使用 /content-workflow）
- 标题长度超过 20 字 → 灵格必须重新调整，不允许超标发布

## 脚本说明

`xhs_publish.cjs` 位于 `{baseDir}/scripts/` 或已部署到 `~/.openclaw/workspace-xiaohongshu-publisher/scripts/`。

**依赖说明：**
- 需要 `playwright` npm 包（`npm install playwright`）
- 需要 Chromium 浏览器（`npx playwright install chromium`）
- 发布为半自动化：脚本自动填写内容，用户在浏览器中最终确认后提交
