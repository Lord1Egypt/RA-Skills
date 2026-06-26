# Browser Bridge 参考

## 使用模式

### 模式 A：先执行

已经知道页面结构时，直接使用 `exec`：

1. `exec "document.querySelector('.add-to-cart').click()"` 会返回一小段结构化 diff。
2. 调用方可以根据 diff 推断页面变化，不需要重新读取整页。

页面结构已知时，不要走 `scan` -> 检查 HTML -> `exec` -> `scan` 的高 token 循环。只有页面未知时才先 `scan`。

### 模式 B：先观察再执行

用于调研、竞品分析、市场研究或未知页面：

1. `scan --text-only` 获取低 token 的页面概览。
2. 用 `exec` 和定向 selector 抽取结构化数据。
3. 用 `navigate` + `scan --text-only` 逐页深入。
4. 深入后用 `back` 返回。

用 `--size-only` 可以确认 SPA 是否已经渲染内容，同时不返回正文内容。

## SPA 内容抽取

React / Vue 页面通常会动态加载内容。抽取前用 `--wait` 等待元素出现：

```bash
python <skill-dir>/scripts/browser.py exec --wait ".note-item" "
  Array.from(document.querySelectorAll('.note-item')).map(el => ({
    title: el.querySelector('.title')?.textContent,
    link: el.querySelector('a')?.href
  }))
"

python <skill-dir>/scripts/browser.py exec --wait ".result-card" --wait-ms 8000 --timeout 30 "
  return document.querySelectorAll('.result-card').length
"

python <skill-dir>/scripts/browser.py scan --text-only --wait ".product-list" --wait-ms 5000
```

如果你确定页面有内容，但 `exec` 返回空数组 `[]`，先退回 `scan --text-only`。常见原因是页面还没渲染完，或 selector 没匹配上。

## 调研速查表

| 场景 | 命令 | 原因 |
|---|---|---|
| 未知页面初看 | `scan --text-only` | 低 token 页面概览 |
| 快速确认是否渲染 | `scan --size-only` | 不消耗正文 token |
| SPA 动态内容 | `exec --wait ".selector" "..."` | 等待渲染完成 |
| SPA 页面概览 | `scan --text-only --wait ".selector"` | 等待后再扫描 |
| 抽取结构化数据 | `exec "Array.from(...)"` | 精准且低 token |
| 组件证据 | `evidence '[data-slot="switch"]' --name Switch` | 捕获渲染后的组件结构 |
| 信息密集的价格页 / 商店页 | `scan --text-only` | selector 不容易猜 |
| 多平台调研 | `newtab` + `navigate` | 每个来源放在独立 tab |
| 跟随链接再返回 | `navigate <url>` 后 `back` | 深入查看后回到原页 |
| 慢异步操作 | `exec --timeout 30 "..."` | 延长超时时间 |

## 站点专用参考

- `grok.md`：通过 Browser Bridge 操作 `https://grok.com` 的页面结构、输入提交、响应抽取和超时建议。

## 排障

**"No browser tabs available"**：扩展没有连接。检查 Chrome 扩展页，必要时重启 Chrome。

**tab 上没有绿色标记**：扩展不能注入 `chrome://` 页面或 Chrome Web Store 页面，这是正常现象。

**Port 18765 already in use**：另一个 Browser Bridge 实例正在运行。先停止旧实例。

**CSP errors**：扩展会自动回退到 CDP，也就是 `chrome.debugger`。

**navigate 后页面没有加载**：先加 `--no-wait`，之后用 `exec --wait` 或 `scan --wait` 等待目标元素。

**多行 JS**：外层字符串用单引号：

```bash
python <skill-dir>/scripts/browser.py exec '
  const items = document.querySelectorAll(".row");
  return Array.from(items).map(r => r.textContent);
'
```
