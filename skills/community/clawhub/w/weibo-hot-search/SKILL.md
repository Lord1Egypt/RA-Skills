---
name: weibo-hot-search-anonymous
description: 无需登录微博账号，匿名抓取微博实时热搜榜并保存为 Markdown 文件。当用户说"获取微博热搜"、"抓取热搜"、"微博热搜榜"、"不用登录查热搜"、"匿名获取热搜"、"get Weibo hot search"、"weibo trending" 时使用。
version: 1.0.0
metadata:
  openclaw:
    requires:
      anyBins:
        - bun
        - npx
---

# 微博热搜抓取（匿名版）

**无需微博账号，无需登录**，通过 Chrome/Edge CDP 以匿名身份访问微博热搜页面（`https://weibo.com/newlogin?tabtype=search`），采集实时热搜列表并保存为 Markdown 表格。

微博热搜页面对未登录用户完全公开，本 skill 利用全新空白的浏览器配置目录访问，不依赖任何账号 Cookie。页面使用虚拟滚动，每次 DOM 中约保留 30 条，脚本缓慢滚动并在每步采集快照，覆盖全部约 50 条热搜。广告条目自动过滤，置顶条目保留并标注。

## 脚本目录

**重要**：所有脚本位于本 skill 的 `scripts/` 子目录中。

**Agent 执行说明**：
1. 将本 SKILL.md 所在目录路径记为 `{baseDir}`
2. 脚本路径 = `{baseDir}/scripts/weibo-hot-search.ts`
3. 将文档中所有 `{baseDir}` 替换为实际路径
4. 确定 `${BUN_X}` 运行时：已安装 `bun` → 使用 `bun`；有 `npx` → 使用 `npx -y bun`；否则提示安装 bun

## 前置条件

- Google Chrome、Chromium 或 Microsoft Edge
- `bun` 运行时
- **无需微博账号，无需任何登录操作**

## 用法

```bash
# 采集热搜，保存到当前目录下 ./<今天日期>-weibo-hot-search.md
${BUN_X} {baseDir}/scripts/weibo-hot-search.ts

# 指定输出路径
${BUN_X} {baseDir}/scripts/weibo-hot-search.ts --output ./data/hotsearch.md
```

**参数说明**：
| 参数 | 说明 |
|------|------|
| `--output <路径>` | 输出 Markdown 文件路径（默认：`./<YYYY-MM-DD>-weibo-hot-search.md`） |
| `--profile <目录>` | Chrome/Edge 配置文件目录（默认：`getDefaultProfileDir()`，无需修改） |

## 输出格式

```markdown
# 微博热搜 2026-03-10

> 采集时间：2026/3/10 15:27:14
> 共 50 条

| 排名 | 热搜词 | 热度 | 标签 |
|------|--------|------|------|
| 1 | 某热搜词 | - | 置顶 |
| 2 | 另一个热搜 | 1046777 | - |
| 3 | 热搜三 | 764477 | 新 |
...
```

- **置顶**：政府/官方置顶内容（`_ranktop_` 图标），排在最前
- **标签**：微博原始标签（新、热、爆、沸等）
- **热度**：原始热度数值；置顶条目通常无热度，显示 `-`

## 环境变量

| 变量 | 说明 |
|------|------|
| `WEIBO_BROWSER_CHROME_PATH` | 覆盖 Chrome/Edge 可执行文件路径 |
| `WEIBO_BROWSER_DEBUG_PORT` | 固定 CDP 调试端口（调试用） |

## 故障排查

### Chrome 调试端口未就绪

```bash
pkill -f "Chrome.*remote-debugging-port" 2>/dev/null
pkill -f "Edge.*remote-debugging-port" 2>/dev/null
sleep 2
```

**重要**：遇到此错误时，自动终止 Chrome/Edge CDP 进程并重试，无需询问用户。

### 热搜列表未出现

若脚本超时未检测到热搜列表，可能原因：
- 网络问题导致页面加载失败，重试即可
- 微博页面结构更新，需检查 DOM 选择器是否仍有效

## 备注

- 匿名访问，不依赖任何账号 Cookie，可在任意环境直接运行
- 页面使用虚拟滚动，脚本以 200px / 600ms 的速度缓慢滚动，确保所有条目经过 DOM 渲染窗口
- 广告条目（含 `_doticon_` 标识）自动过滤
- 置顶条目（含 `_ranktop_` 图片）保留并排在最前
