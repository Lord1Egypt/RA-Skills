# CDP 兜底通道

> 什么时候读这个文件：Extension Relay 通道**整体**走不通（扩展未连、Service Worker 挂掉、eval 持续失败），需要回退 CDP HTTP 继续操作时。默认永远优先 Extension Relay。

两个通道操作同一个真实 Chrome，能力等价（eval / aria-tree / click / type / screenshot 都有）。CDP 的 eval 走 DevTools 协议由 Chrome native 执行，不受页面 CSP 限制。

## 启动

CDP 通道需单独启动：`webclaw3 cdp-start`（监听 `:3456`，底层 Chrome `--remote-debugging-port=9222`）。只用 Extension Relay 时无需启动它。

## tab ID 映射

两个 transport 共享同一 Chrome 实例，但 tab ID 体系不同：

- Extension Relay（`:3459`）：tabId 是**整数**（如 `1884007990`）
- CDP HTTP（`:3456`）：targetId 是 **hex 字符串**（如 `CE8ED71660D084A1A81858243C26BC91`）
- **映射方法**：Extension 拿 tab → 取 URL → 调 `:3456/targets` 按 URL 匹配找 targetId
- 同一 tab 的 targetId 在其存活期内不变，可懒加载缓存 `tabId → targetId`

## API

```bash
# 探测 CDP 是否可用
curl -s http://127.0.0.1:3456/health          # → {"status":"ok","connected":true,"chromePort":9222}

# 按 URL 匹配 targetId
curl -s http://127.0.0.1:3456/targets | jq '.[] | select(.url=="https://example.com/") | {targetId, url, title}'

# eval（POST，body 是原始 JS 表达式字符串，不能包成 JSON；成功返回 {"value":...}）
printf '%s' 'document.querySelectorAll("a").length' > /tmp/eval.js
curl -s -X POST "http://127.0.0.1:3456/eval?target=TARGET_ID" --data-binary @/tmp/eval.js

# aria-tree / 语义点击 / 语义输入 / 截图
curl -s "http://127.0.0.1:3456/aria-tree?target=TARGET_ID"
curl -s -X POST "http://127.0.0.1:3456/click-aria?target=TARGET_ID" -d '{"role":"tab","name":"下载热榜"}'
curl -s -X POST "http://127.0.0.1:3456/type-aria?target=TARGET_ID" -d '{"role":"textbox","name":"搜索","text":"关键词"}'
curl -s "http://127.0.0.1:3456/screenshot?target=TARGET_ID"
```

返回值字段名与 Extension 不同：Extension `{result} | {error}`，CDP `{value} | {error}`。

## 回退判定（重要）

只有 Extension 通道整体不可用/eval 持续失败才回退 CDP；单次 `SyntaxError`、`tab not found` 等属脚本问题，不回退。摸清页面结构后切回 Relay——CDP 是临时探查通道，不要进入沉淀的脚本代码。

## operation_log

上下文声明了 `WC3_OPERATION_LOG` 时，CDP 调用同样要带 logFile（URL query）：

```bash
curl -s "http://127.0.0.1:3456/aria-tree?target=TARGET_ID&logFile=<声明的值>"
```
