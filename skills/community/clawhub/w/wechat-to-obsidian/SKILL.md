---
name: wechat-to-obsidian
version: 1.0.3
description: 将微信公众号文章剪藏到 Obsidian：使用真实无头浏览器加载页面，按原文顺序保留文字、图片和 Markdown 标题层级，图片自动下载到 attachments 目录。
metadata:
  openclaw:
    requires:
      bins:
        - agent-browser
        - curl
    install:
      - id: agent-browser
        kind: node
        package: agent-browser
        bins: [agent-browser]
        label: "Install agent-browser (headless browser CLI)"
---

# 微信公众号 → Obsidian 剪藏

这个 Skill 用来把 `mp.weixin.qq.com` 微信公众号文章保存成 Obsidian Markdown 笔记。

核心目标：

- **真实浏览器加载**：用 `agent-browser` 打开页面，避免普通 `curl` / `web_fetch` 被微信反爬拦截。
- **图文顺序保留**：按 DOM 顺序提取正文和图片，图片插入位置尽量贴近原文。
- **图片本地化**：正文图片下载到笔记同级 `attachments/` 目录。
- **Markdown 标题层级保留**：识别原生 `h1-h6` 和微信常见“视觉标题”，输出 `##` / `###`。
- **写入前确认**：除非用户已经明确指定路径，否则必须先询问保存目录，确认后再写文件。

---

## 触发场景

当用户发来微信公众号链接，并表达以下意图时使用本 Skill：

- “存 Obsidian”
- “剪藏”
- “帮我存”
- “保存到这个路径”
- “把这篇公众号文章放进 Obsidian”

链接通常长这样：

```text
https://mp.weixin.qq.com/s/xxxxx
```

---

## 依赖

- `agent-browser` ≥ 0.17
- `curl`
- 本地可访问的 Obsidian Vault

安装 `agent-browser`：

```bash
npm install -g agent-browser
agent-browser install
```

---

## 总体流程

1. 用 `agent-browser` 打开微信公众号文章。
2. 等待页面加载。
3. 滚动全文，触发懒加载图片。
4. 按 DOM 顺序提取标题、正文和图片。
5. 如果用户未明确指定保存路径，先询问并等待确认。
6. 下载图片到 `<note_dir>/attachments/`。
7. 写入 Markdown 笔记。
8. 关闭浏览器。
9. 向用户汇报保存路径、图片数量、失败项。

---

## Step 1 — 打开页面

```bash
agent-browser open "<wechat_url>"
agent-browser wait --load networkidle
```

如果 `networkidle` 等待失败，但页面正文已经可见，可以继续执行下一步。

---

## Step 2 — 获取文章标题

```bash
agent-browser get title
```

优先从页面里的 `#activity-name` 读取标题；如果失败，再用浏览器标题兜底。

---

## Step 3 — 滚动全文，触发懒加载图片

微信图片大量使用懒加载。**必须滚动全文后再提取图片 URL**，否则图片 `src` 可能为空。

```bash
agent-browser eval "
(async () => {
  window.scrollTo(0, document.body.scrollHeight);
  await new Promise(r => setTimeout(r, 2000));
  const step = 600;
  for (let y = 0; y < document.body.scrollHeight; y += step) {
    window.scrollTo(0, y);
    await new Promise(r => setTimeout(r, 300));
  }
  return 'done';
})()"
```

---

## Step 4 — 按 DOM 顺序提取内容，并保留 Markdown 结构

重要规则：

- `agent-browser eval` 内部尽量使用经典 `function(){}` 语法。
- 不要在 `JSON.stringify()` 包裹的大段 JS 里混用复杂 shell 引号。
- 提取结果要保留 `type`：`heading` / `text` / `img`。
- 写笔记时必须把 `heading` 渲染成 Markdown 标题，而不是普通文本。

```bash
agent-browser eval "
(function() {
  function textOf(node) {
    return (node.innerText || '').replace(/\u00a0/g, ' ').trim();
  }
  function maxFontSize(node) {
    var max = 0;
    var els = [node].concat(Array.prototype.slice.call(node.querySelectorAll('*')));
    els.forEach(function(el) {
      var n = parseFloat(getComputedStyle(el).fontSize || '0');
      if (n > max) max = n;
    });
    return max;
  }
  function hasBold(node) {
    if (node.querySelector('strong,b')) return true;
    var els = [node].concat(Array.prototype.slice.call(node.querySelectorAll('*')));
    return els.some(function(el) {
      var fw = getComputedStyle(el).fontWeight || '400';
      return fw === 'bold' || parseInt(fw, 10) >= 600;
    });
  }
  function headingLevel(node, text) {
    var tag = node.tagName;
    if (/^H[1-6]$/.test(tag)) return parseInt(tag.slice(1), 10);
    var size = maxFontSize(node);
    var bold = hasBold(node);
    var short = text.length <= 40;

    // 微信常把视觉标题做成带样式的 p / section，而不是 h2 / h3。
    // 这里保守识别常见中文大纲标题和数字小标题。
    if (/^[一二三四五六七八九十]+[\.．、]\s*/.test(text) && (bold || size >= 19 || short)) return 2;
    if (/^\d+[\.．、]\s*/.test(text) && (bold || size >= 19 || short)) return 3;
    if (short && bold && size >= 20) return 3;
    return 0;
  }
  function inlineMarkdown(node) {
    var text = textOf(node);
    if (!text) return '';
    if (node.querySelector('code')) return text.replace(/`/g, '\\`');
    return text;
  }

  var nodes = document.querySelectorAll('#js_content h1,#js_content h2,#js_content h3,#js_content h4,#js_content h5,#js_content h6,#js_content p,#js_content section,#js_content img');
  var result = [];
  var imgIdx = 0;
  nodes.forEach(function(node) {
    if (node.tagName === 'IMG') {
      var src = node.currentSrc || node.src || node.dataset.src || '';
      if (src && src.includes('mmbiz') &&
          !src.includes('mmbiz.qlogo') &&
          !src.includes('profile')) {
        var h = node.naturalHeight || node.height || 0;
        var alt = (node.alt || '').toLowerCase();
        if ((h >= 50 || h === 0) &&
            !alt.includes('二维码') &&
            !alt.includes('引导') &&
            !alt.includes('赞赏')) {
          result.push({ type: 'img', idx: imgIdx++, src: src });
        }
      }
    } else {
      if (node.tagName === 'SECTION' && node.querySelector('p,img,section')) return;
      var text = textOf(node);
      if (text && text.length > 3) {
        var level = headingLevel(node, text);
        if (level) result.push({ type: 'heading', level: level, text: text });
        else result.push({ type: 'text', text: inlineMarkdown(node) });
      }
    }
  });
  return JSON.stringify(result);
})()"
```

### Markdown 标题规则

- 原生 `h1-h6` → `#` 到 `######`
- `一. / 一、 / 二.` 这类章节标题 → `##`
- `1. Mac / 2. Windows` 这类数字小标题 → `###`
- 短文本 + 加粗 + 20px 以上字号 → `###`

写入时示例：

```markdown
## 一. Claude Code 安装

### 1. Mac
```

图片仍然必须保持在 DOM 原始位置，不要统一堆到文末。

---

## 图片过滤规则

跳过这些图片：

- `mmbiz.qlogo`：公众号头像
- `mp_profile`：账号资料图
- 高度小于 50px：装饰线、分割线
- `alt` 包含 `二维码` / `引导` / `赞赏`：二维码、引导关注、赞赏图

---

## Step 5 — 确认保存位置

如果用户已经明确给出保存路径，可以直接进入 Step 6。

如果用户没有明确路径，必须停下来询问：

```text
📂 建议保存到：<vault_root>/<topic_directory>/
📄 文件名：<title-keywords-YYYY-MM-DD>.md
🖼 图片目录：同级 attachments/
确认保存到这里吗？还是换个位置？
```

**HARD STOP：用户确认前，不要下载图片，不要写入笔记。**

---

## Step 6 — 下载图片

只在用户确认保存路径后执行。

```bash
mkdir -p "<note_dir>/attachments"

curl -s -L --fail \
  -A 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36' \
  -e 'https://mp.weixin.qq.com/' \
  "<image_url>" -o "<note_dir>/attachments/<filename>"
```

关键点：

- 微信图片下载必须带 Referer：`-e 'https://mp.weixin.qq.com/'`
- 文件名建议：`<slug>-图00.png`、`<slug>-图01.jpg`
- 如果 URL 里有 `wx_fmt=jpeg`，扩展名用 `.jpg`；否则默认 `.png`
- 批量下载时用 shell function，不要用 `declare -A`，因为 zsh 不支持关联数组

批量下载函数示例：

```bash
download_img() {
  local idx=$1 url=$2
  local ext="png"
  echo "$url" | grep -q "wx_fmt=jpeg" && ext="jpg"
  local fname=$(printf "<slug>-图%02d.%s" "$idx" "$ext")
  curl -s -L --fail \
    -A 'Mozilla/5.0' \
    -e 'https://mp.weixin.qq.com/' \
    "$url" -o "$fname" \
    && echo "OK $fname" || echo "FAIL $fname"
}
```

---

## Step 7 — 写入 Markdown 笔记

必须严格使用 Step 4 的 DOM 顺序。

```markdown
# {文章标题}

**Source:** WeChat — {作者 / 公众号名}
**Original URL:** {URL}
**Clipped:** {YYYY-MM-DD}
**Tags:** #{tag1} #{tag2}

---

{正文段落}

![[slug-图00.jpg]]

## {二级标题}

{更多正文}

![[slug-图01.png]]

---

**References:**
- {原文链接或正文链接}
```

注意：

- `{ type: 'heading', level: 2, text: '...' }` 必须写成 `## ...`
- `{ type: 'heading', level: 3, text: '...' }` 必须写成 `### ...`
- 图片使用 Obsidian 格式：`![[filename]]`
- 图片放在笔记同级 `attachments/` 目录

---

## Step 8 — 关闭浏览器

```bash
agent-browser close
```

---

## Step 9 — 汇报结果

向用户说明：

- 笔记路径
- 图片目录
- 成功下载图片数量
- 失败图片数量（如有）
- 提醒：如果移动笔记，最好连同同级 `attachments/` 一起移动

---

## 常见问题与修复

| 问题 | 修复 |
|---|---|
| 图片 `src` 为空 | 先滚动全文，触发懒加载 |
| 微信图片下载 403 | `curl` 必须带 `-e 'https://mp.weixin.qq.com/'` |
| 图片顺序错乱 | 按 DOM 单次遍历，不要文字和图片分开收集 |
| zsh 报 `bad substitution` | 不要用 `declare -A`；改用 shell function |
| `SyntaxError: missing ) after argument list` | `agent-browser eval` 里少用复杂箭头函数和嵌套引号 |
| `async` eval 卡住 | 用 `(async () => { ... })()` 包住 |
| 标题变成普通文字 | 使用 `heading` 类型并在写入时转成 `##` / `###` |

---

## 输出质量要求

- 不要遗漏标题层级。
- 不要把图片集中放到开头或结尾。
- 不要在未确认路径时写文件。
- 不要把二维码、公众号头像、赞赏码当正文图片。
- 不要把本地绝对路径、账号、token 写进公开输出。
