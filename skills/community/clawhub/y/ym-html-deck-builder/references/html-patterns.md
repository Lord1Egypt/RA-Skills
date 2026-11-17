# HTML 幻灯片翻页实现模式（references/html-patterns.md）

本文件记录 `scripts/build_deck.py` 采用的翻页交互与主题切换实现模式，供二次开发或排错参考。全部为原生 JS + CSS，无框架、无 CDN。

## 1. 页面结构

- 容器 `.deck` 固定铺满视口（`width:100vw;height:100vh;overflow:hidden`）。
- 每页是一个 `<section class="slide">`，默认 `display:none`；当前页加 `.active` 类变为 `display:flex`。
- 进度条 `.bar`、页码 `.pageinfo`、目录浮层 `.toc` 均为 `position:fixed`，独立于翻页容器。

切换显隐只改 class，不做淡入淡出（保持零依赖、瞬时响应）：

```js
slides.forEach(function(s,j){ s.classList.toggle('active', j===idx); });
```

## 2. 键盘事件表

| 按键 | 行为 | 处理 |
|---|---|---|
| → / 空格 / PgDn | 下一页 | `show(idx+1)` |
| ← / PgUp | 上一页 | `show(idx-1)` |
| Home | 首页 | `show(0)` |
| End | 末页 | `show(slides.length-1)` |
| Esc | 弹出/收起目录 | `toggleToc()` |
| F / f | 全屏切换 | `fs()` |

实现要点：

- 监听 `document` 的 `keydown`，对翻页类按键调用 `e.preventDefault()`，避免空格滚动页面、方向键滚动页面。
- `show(i)` 内部把越界索引夹到 `[0, len-1]`，保证首尾页不会越界。
- 翻页类按键统一归一：右/空格/下页为「前进」，左/上页为「后退」。

## 3. 进度条计算

进度条宽度按「(当前页+1) / 总页数 * 100%」计算，用 CSS `transition:width .2s` 做平滑推进：

```js
var p = (i+1) / slides.length * 100;
document.getElementById('bar').style.width = p + '%';
document.getElementById('pageinfo').textContent = (i+1) + ' / ' + slides.length;
```

页码始终显示「当前 / 总页」，与进度条同源，避免两者不一致。

## 4. 目录浮层

- `.toc` 默认 `display:none`，加 `.open` 类变为 `display:flex` 覆盖全屏。
- 每个目录项是 `<button>`，点击执行两件事：跳到对应页、移除 `.open` 收起浮层：

```js
'<button onclick="show(' + i + ');document.getElementById(\'toc\').classList.remove(\'open\')">' + (i+1) + '. ' + title + '</button>'
```

- 目录项由脚本按大纲标题顺序生成，标题变更后目录自动同步，无需手填。

## 5. 全屏降级

浏览器全屏 API（`requestFullscreen`）仅在 `https://` 或 `localhost` 下可用，直接 `file://` 打开会被拦截。`fs()` 做三件事：

1. 若已全屏则退出；否则尝试进入。
2. 同时兼容 `webkitRequestFullscreen` 前缀（旧版 Safari/Chrome）。
3. 调用包在 `try/catch` 中，失败仅在控制台提示，不影响翻页，用户可改用浏览器自带全屏（F11）。

## 6. 两套主题 CSS 变量约定

通过 `<html data-theme="light|dark">` 切换，所有颜色走 CSS 变量，便于扩展第三套主题：

```css
:root{
  --bg:#ffffff; --fg:#1f2329; --muted:#646a73; --accent:#2f6fed;
  --slide-bg:#ffffff; --bar:#2f6fed; --panel:#f2f3f5;
}
[data-theme="dark"]{
  --bg:#0f1115; --fg:#e6e8eb; --muted:#9aa0a6; --accent:#5b8cff;
  --slide-bg:#161a20; --bar:#5b8cff; --panel:#1d222b;
}
```

扩展新主题：复制 `[data-theme="dark"]` 块，改 `data-theme` 取值并在脚本 `--theme` 的 `choices` 中登记即可，无需改动 JS。

## 7. 中文字体栈（必写全）

```css
font-family:"Microsoft YaHei","PingFang SC","Hiragino Sans GB","Heiti SC","WenQuanYi Micro Hei",sans-serif;
```

只写 `sans-serif` 在部分 Linux 环境会回退成方块；写全栈可覆盖 Windows / macOS / Linux 主流中文环境。
