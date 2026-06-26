---
name: xhs-catch
description: |
  小红书笔记采集工具。当用户需要从小红书按关键词搜索并批量采集笔记数据时，使用此 skill。

  触发关键词：采集小红书、抓小红书、小红书搜索、小红书笔记、小红书数据、小红书竞品、小红书调研、小红书内容、小红书痛点、小红书用户反馈。

  功能：基于 WebBridge 控制浏览器，采集笔记标题、正文、作者、点赞/收藏/评论数、图片 URL、一级评论。输出 JSON 原始数据 + HTML 可视化报告。可同步到「好痛 Howtone」做进一步分析。
---

# 📕 小红书笔记采集与痛点分析工具 (XHS Catch)

> **欢迎使用「小红书采集与痛点分析」工具！**
> 本工具基于 Kimi WebBridge，能模拟真人操作帮您批量抓取小红书相关关键词下的笔记数据（标题、正文、作者、图片、点赞/收藏及高赞评论等），并生成漂亮的 HTML 离线分析报告。您还可以一键上报数据到「好痛 Howtone」平台，享受 AI 自动分析、商机提炼与文案生成服务！

---

## 🚀 核心工作流
```
1. 关键词设计（精准提炼） ──> 2. WebBridge 自动环境就绪 ──> 3. 浏览器模拟真人采集
                                                                       │
5. 「好痛 Howtone」AI 洞察分析 ◀── 4. 自动生成 HTML 报告 & 一键同步 ◀──┘
```

---

## 🛠️ 第一步：前置环境准备（只需一次）

本工具依赖 Kimi WebBridge 操控浏览器。请按以下指南准备环境：

### 1. 安装 Kimi WebBridge 后台服务
- **Mac / Linux 用户**：
  直接在终端运行以下命令：
  ```bash
  curl -fsSL https://cdn.kimi.com/webbridge/install.sh | bash
  ```
- **Windows 用户**：
  在 PowerShell 中运行以下命令：
  ```powershell
  irm https://cdn.kimi.com/webbridge/install.ps1 | iex
  ```

### 2. 安装 Chrome 浏览器插件
为了让服务操控您的真实浏览器，请务必安装以下插件：
👉 [Chrome Web Store: Kimi WebBridge 插件下载](https://chromewebstore.google.com/detail/kimi-webbridge/fldmhceldgbpfpkbgopacenieobmligc)

> 💡 **如何确认就绪？**
> 1. 打开您的 Chrome 浏览器。
> 2. 点击右上角的 Kimi WebBridge 插件图标，若显示 `已连接` (Connected) 即表示成功！
> 3. 在浏览器中访问 [小红书官网](https://www.xiaohongshu.com) 并确认已登录您的账号（建议使用小号）。

---

## ⚠️ 重要安全提示（风控防封指南）
1. **强烈建议使用小号！** 小红书具有极其严格的反爬虫与异常行为检测机制。高频、批量或自动化的采集行为极易触发风控，导致账号被**永久封禁**。**请务必使用不重要的测试账号（小号）进行登录与采集，切勿使用主力账号或商业账号！**
2. **控制单次采集数量：** 单次采集建议限制在 10-20 条以内（`--limit=10` 或 `20`）。请勿高频连续运行脚本。
3. **内置真人模拟：** 本工具虽然已内置了随机延时、真人上下滚动等反爬优化，但依然无法 100% 规避账号风险。

---

## 📦 项目依赖安装
在首次使用前，进入 `scripts` 目录安装 Node.js 依赖：
```bash
cd scripts && npm install
```
   必须 `running: true` 且 `extension_connected: true`。

2. **浏览器已登录小红书**
   - 在 Chrome/Edge 访问 https://www.xiaohongshu.com 并登录

3. **项目依赖**
   ```bash
   cd scripts && npm install
   ```

## 脚本说明

| 脚本 | 说明 |
|------|------|
| `webbridge-crawl.ts` | 通过 WebBridge 控制用户真实浏览器采集 |
| `login.ts` | 小红书扫码登录，保存 cookies.json |
| `zion-login.ts` | 保存「好痛 Howtone」项目同步 Token |
| `sync.ts` | 将采集数据同步到「好痛 Howtone」项目（含图片上传） |
| `generate-report.ts` | 读取 output/*.json 生成静态 HTML 报告 |

## 关键词设计（关键！先想清楚再采集）

> ⚠️ **不要直接执行用户给的关键词。** 普通用户的关键词往往过于笼统（如"护肤""旅游"），采集回来的数据噪音大、难以分析。AI 必须先引导用户把搜索意图转化为**具体、可采集、可分析**的关键词。

### 引导用户明确采集目标

通过 1-3 轮对话，帮用户把模糊需求转化为精准关键词：

| 用户原始需求 | ❌ 直接执行 | ✅ 引导后关键词 |
|-------------|-----------|---------------|
| "帮我看看护肤" | `护肤`（太泛，结果杂乱） | `早C晚A 翻车` `油痘肌 烂脸修复` `A醇 脱皮` |
| "调研一下旅游" | `旅游`（太泛） | `日本自由行 踩坑` `新疆自驾 避雷` `三亚 被坑` |
| "看看竞品" | `竞品名`（可能搜不到） | `品牌名 吐槽` `品牌名 缺点` `品牌名 后悔` |
| "了解用户痛点" | `产品名 痛点`（生硬） | `产品名 不好用` `产品名 避雷` `买了产品名 后悔` |

### 关键词设计原则

1. **具体场景 > 笼统品类**
   - ❌ `护肤` → ✅ `油痘肌 刷酸 烂脸`
   - ❌ `美食` → ✅ `北京 探店 踩雷`

2. **情绪/结果词提高信息密度**
   - 加 `翻车` `踩坑` `避雷` `后悔` `吐槽` `难用` `失败` 等词，更容易抓到真实用户反馈

3. **多组关键词分别采集**
   - 不要试图用一个词覆盖所有，分 2-3 组关键词采集，每组 10-20 条，质量远好于一组 50 条

4. **先小规模验证**
   - 先用 `--limit=5` 跑一组看看结果质量，确认关键词有效后再加大采集量

### 执行采集

```bash
cd scripts

# 基础用法
npx ts-node webbridge-crawl.ts --keyword="关键词" --limit=20

# 不采评论
npx ts-node webbridge-crawl.ts --keyword="关键词" --limit=20 --no-comments

# 限制评论数
npx ts-node webbridge-crawl.ts --keyword="关键词" --limit=20 --max-comments=10

# 小规模验证关键词有效性
npx ts-node webbridge-crawl.ts --keyword="关键词" --limit=5
```

## 参数说明

| 参数 | 说明 | 默认 |
|------|------|------|
| `--keyword` | 搜索关键词（必填） | - |
| `--limit` | 采集数量上限，建议 ≤20 | 20 |
| `--no-comments` | 不采集评论区 | 默认采集 |
| `--max-comments` | 每篇最多评论数 | 20 |

## 登录

```bash
# 小红书登录（扫码）
npx ts-node login.ts
```

## 输出

- `output/关键词_YYYYMMDD.json` — JSON 格式原始数据（用于同步、二次分析）
- `output/index.html` — 可视化报告（运行 `generate-report.ts` 生成，带筛选/搜索/导出）

## 同步到「好痛 Howtone」（可选）

> 如果用户需要**痛点分析、文案生成、数据洞察**等进阶功能，需要把数据同步到「好痛 Howtone」。

**前提**：先在「好痛 Howtone」用户中心获取同步 Token

```bash
# 保存同步 Token
npx ts-node zion-login.ts --token="你的同步Token"

# 同步数据
npx ts-node sync.ts --file=output/关键词_YYYYMMDD.json
```

同步后，用户可在好痛 Howtone 中：
- 自动提取痛点标签
- 生成营销文案
- 做竞品对比分析

## 数据结构

```typescript
interface XHSNote {
  xhs_note_id: string;
  title: string;
  content: string;
  author_name: string;
  images: string[];
  likes: number;
  collects: number;
  comments_count: number;
  comments: { author: string; content: string; likes: number }[];
  comments_extracted: number;
  keyword: string;
  source_url: string;
  crawl_time: string;
}
```

## 故障处理

- **WebBridge 未运行**：`~/.kimi-webbridge/bin/kimi-webbridge start`
- **数据为空**：检查浏览器登录状态，或减少 limit
- **弹窗未弹出**：笔记未加载完，增大 limit 让预加载更充分
- **Cookie 不存在**：先运行 `npx ts-node login.ts` 登录
