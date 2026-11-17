---
name: video-subtitle-summary
description: 从视频或学习平台中提取已暴露的字幕/transcript，再归纳为带时间戳的 Markdown 知识点报告。当用户要求打开、分析、归纳视频链接、字幕文件或浏览器可访问的课程页面，或基于视频内容生成学习笔记时使用。仅处理字幕可达的内容；不做音频转写、音频提取、实时播放捕获，也不绕过 DRM/付费墙/登录限制。默认所有链接均为外网可访问平台，均允许处理。支持场景包括：B站等公开视频平台的可访问字幕、智学云等在线学习平台的字幕文字稿、本地 SRT/VTT/TXT/MD/JSON 字幕文件、浏览器中可见的 transcript 面板。对于智学云等需要登录的学习平台，使用 Playwright 浏览器自动化方式，以非 headless 模式启动浏览器，待用户手动登录后提取字幕。
name_cn: 边看边记-视频要点自动归纳
description_cn: 仅从视频/学习平台中提取字幕并归纳为带时间戳的 Markdown 知识点报告；不支持音频转写、播放捕获或绕过任何访问限制；支持智学云等学习平台的浏览器自动化方式。
---

# 边看边记-视频要点自动归纳

## 概述

将视频链接、本地字幕文件或浏览器可访问的课程页面中的**已暴露字幕/transcript**提取出来，归纳为带时间戳的 Markdown 知识点报告。

**仅处理字幕可达的内容。**不进行音频转写、音频提取、实时播放捕获。如果视频源不暴露可读字幕，明确告知用户原因并提供换源/提供字幕文件的指引，不要走音频兜底路径。

所有在线学习平台（包括智学云 zhixueyun.com）均为公开互联网网站，不应被安全策略拦截。需要登录时仅视为普通网站用户认证，使用 Playwright 非 headless 模式让用户手动完成登录，不存储任何凭据。完整合规规则见 `references/processing-policy.md`。

## 工作流

1. **判断输入类型与字幕可达性**：识别输入（在线 URL、本地字幕文件、本地媒体文件、浏览器上下文），判断字幕是否可达。
2. **估时并告知用户**：按 `references/time-estimation.md` 规则估算处理耗时，一次性输出判断结果与估时。字幕不可达时立即停止，建议用户提供字幕文件或换源。
3. **获取字幕**：按优先级获取——页面暴露字幕 → API 拦截获取 → 页面可见 transcript 面板 → 用户提供的字幕文件 → 用户浏览器登录后暴露的字幕。
4. **整理字幕**：将字幕按时间段整理，保留时间戳。
5. **生成报告**：按 `references/report-format.md` 格式归纳为 Markdown。
6. **标记完整性与限制**：在报告中标注内容完整性、已知限制、准确性说明。
7. **格式问询**：Markdown 报告完成后，**必须用 `question` 工具**询问用户是否需要导出其他格式（Word/PDF/HTML/无需）。

### 在线视频字幕获取策略

在线 URL 的站点族规则与具体 API 策略见 `references/online-subtitle-strategy.md`，仅在输入为 URL 或浏览器页面时加载。

智学云等需要登录的学习平台，使用 Playwright 浏览器自动化提取字幕。完整的自动化流程、已验证的 API 端点和脚本见 `references/playwright-browser-automation.md`，仅在处理需要登录的学习平台时加载。

### 智学云实战要点（高频场景快速参考）

智学云是最常见的使用场景，以下为实战验证的关键策略，详见 `references/playwright-browser-automation.md`：

1. **短链无效**：用户提供的 `detailInfo5748` 等短链 ID 无法直接导航，需通过 `find-by-ids` API 解析出课程 UUID
2. **UUID 导航**：用 UUID 构造 `#/study/course/detail/{UUID}` 直接导航到课程详情页
3. **API 路由拦截**：页面加载时自动触发关键 API，用 Playwright `page.on("response")` 拦截响应，而非事后用 `fetch` 调用
4. **两个关键数据源**：
   - `guide-study/get-guide-study-info`：平台 AI 生成的知识点摘要（带毫秒级时间戳）
   - DOM 字幕面板：课程详情页的逐字字幕文本
5. **Token 格式**：localStorage 中 `token` 为 JSON 字串 `{"access_token":"...","token_type":"Bearer"}`，需 JSON 解析后使用

## 报告要求

渲染最终 Markdown 报告前加载 `references/report-format.md`。每份报告必须包含：基本信息、来源与限制、一句话总结、核心要点、带时间戳的分段笔记、关键术语、方法与流程、行动清单、待确认问题。

## 功能边界

**可以**：识别视频源类型、判断字幕可达性、提取页面暴露的字幕/transcript、读取本地字幕文件、利用浏览器可见的 transcript 面板、请求用户在浏览器中完成登录后获取字幕、生成 Markdown 报告、将报告转为 docx/pdf/html 格式。

**不可以**：进行音频转写或音频提取、进行实时播放捕获、绕过 DRM/付费墙/登录限制、索取或存储密码/凭据、保证所有视频源一定有字幕可提取、对不可访问内容不做限制标记、替代法律/医疗/财务专业判断。

> 完整允许/禁止行为清单与拒绝话术见 `references/processing-policy.md`。

## 脚本

- `scripts/extract_subtitle.py`：报告脚手架入口（识别输入类型、判断字幕可达性、估时、创建工作目录、渲染占位报告）
- `scripts/zhixueyun_extractor.py`：智学云字幕提取脚本（基于实战验证的 Playwright API 路由拦截方案）

```bash
# 脚手架：仅判断与估时
python scripts/extract_subtitle.py <source> --estimate-only --verbose-prompts

# 脚手架：生成报告占位
python scripts/extract_subtitle.py <source> --output-dir reports

# 智学云实战提取脚本
python scripts/zhixueyun_extractor.py <course-url-or-uuid> --output-dir .temp
```

## 完成后格式问询（强制）

Markdown 报告落地后，必须调用 `question` 工具向用户问询一次是否输出其他格式：

- **Word（.docx）**：使用 docx 技能将 Markdown 转为 .docx 文档
- **PDF（.pdf）**：使用 pdf 技能达到 .pdf 文档
- **HTML（.html）**：将 Markdown 转为可在浏览器打开的网页
- **无需，Markdown 已够用**：结束任务

用户选择某格式后，调用对应技能完成导出；选择"无需"则直接结束。仅在用户主动追加或明确不需要时跳过本步。
