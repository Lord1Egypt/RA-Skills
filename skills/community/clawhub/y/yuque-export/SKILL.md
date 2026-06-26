---
argument-hint: <语雀知识库URL> [--output=~/Downloads/yuque-export] [--images]
description: 将语雀知识库的所有文档导出为本地 Markdown 文件，保留目录结构。需要 Chrome DevTools MCP。
---

# yuque-export

将指定语雀知识库的所有文档导出为 Markdown 文件，保留知识库的目录层级结构。

## 使用方式

```
/yuque-export https://www.yuque.com/{username}/{repo-name}
/yuque-export https://www.yuque.com/{username}/{repo-name} --output=~/Documents/notes
/yuque-export https://www.yuque.com/{username}/{repo-name} --images
```

- `--output`：指定输出目录，默认 `~/Downloads/yuque-export`
- `--images`：同时下载图片到本地 `_assets/` 目录，并替换 Markdown 中的图片链接

## 前置条件

- **Chrome DevTools MCP** 必须已连接 —— 通过浏览器已登录的 session 访问语雀内部 API。

## 执行步骤

### Step 1：导航并确认登录

用 `mcp__chrome-devtools__navigate_page` 打开知识库 URL（如 `https://www.yuque.com/user/repo`）。

然后用 `mcp__chrome-devtools__evaluate_script` 检查登录状态：

```javascript
const resp = await fetch('/api/mine', { credentials: 'include', headers: { 'Accept': 'application/json' } });
const data = await resp.json();
JSON.stringify({ loggedIn: resp.ok, user: data.data?.name || null });
```

若未登录（`loggedIn: false`），导航到 `https://www.yuque.com/login`，提示用户手动登录，然后用 `mcp__chrome-devtools__wait_for` 等待登录完成（等待 URL 变化离开 login 页面）。

### Step 2：获取 book_id

导航到知识库首页后，语雀会自动发起包含 book_id 的 API 请求。用 `mcp__chrome-devtools__list_network_requests` 过滤 fetch/xhr 请求，从中提取 book_id：

```
查找匹配以下模式的请求 URL：
- /api/books/{book_id}/overview
- /api/docs?book_id={book_id}
```

用正则 `/\/api\/(?:books\/(\d+)|docs\?book_id=(\d+))/` 匹配，提取数字部分即为 book_id。

**注意**：`/api/v2/repos/` 需要 Token 认证，浏览器 session 不够，**不要使用**。

### Step 3：获取目录结构和文档列表

**必须使用 `/api/catalog_nodes` API**（不是 `/api/books/{id}/docs`），只有这个 API 返回完整的目录层级信息：

```javascript
const BOOK_ID = /* Step 2 获取的 book_id */;
const resp = await fetch(`/api/catalog_nodes?book_id=${BOOK_ID}`, {
  credentials: 'include', headers: { 'Accept': 'application/json' }
});
const nodes = (await resp.json()).data || [];
JSON.stringify(nodes.map(n => ({
  title: n.title,
  type: n.type,           // 'DOC' = 文档, 'TITLE' = 目录节点（注意是大写）
  uuid: n.uuid,
  url: n.url,             // 即 slug，用于 API 调取文档内容
  parent_uuid: n.parent_uuid || '',
  level: n.level,         // 层级深度，0=根级
  doc_id: n.doc_id,
  visible: n.visible,
})));
```

**注意**：
- `/api/books/{id}/docs` 和 `/api/docs?book_id=` **不返回** uuid/parent_uuid 字段，无法构建目录树
- catalog_nodes 不需要分页，一次返回全部
- `type` 值是**大写**的 `'DOC'` 和 `'TITLE'`

拿到节点列表后，**在 Claude 端构建目录树**：
1. `type === 'TITLE'` 的节点是纯目录节点（不含内容），其 `title` 用作目录名
2. `type === 'DOC'` 的节点是文档，生成 `{title}.md` 文件
3. 用 `parent_uuid` → `uuid` 关系建立父子层级
4. `parent_uuid` 为空的是根级节点
5. 为每篇 DOC 文档计算相对路径（如 `效率类/Markdown 语法.md`）
6. 只下载 `type === 'DOC'` 的节点内容，TITLE 节点跳过

### Step 4：注入 lakeToMarkdown 转换函数

通过 `mcp__chrome-devtools__evaluate_script` 注入。注意：这个函数很长，**必须单独注入，不要和其他逻辑混在一起**。

```javascript
window._lakeToMarkdown = function(lakeHtml, title) {
  if (!lakeHtml || lakeHtml.trim().length < 10) return `# ${title}\n\n(空文档)\n`;

  let html = lakeHtml;

  // ===== Phase 1: 在 DOMParser 前提取特殊 card 元素 =====

  // 代码块
  html = html.replace(
    /<card[^>]*name="codeblock"[^>]*value="data:([^"]*)"[^>]*\/?>/gi,
    (_, encoded) => {
      try {
        const j = JSON.parse(decodeURIComponent(encoded));
        const code = (j.code || '').replace(/</g, '&lt;');
        return `<pre data-lang="${j.mode || ''}">${code}</pre>`;
      } catch { return '<pre>[代码块解析失败]</pre>'; }
    }
  );

  // 图片
  html = html.replace(
    /<card[^>]*name="image"[^>]*value="data:([^"]*)"[^>]*\/?>/gi,
    (_, enc) => {
      try {
        const j = JSON.parse(decodeURIComponent(enc));
        const alt = j.name || '图片';
        return `<img src="${j.src || ''}" alt="${alt}" />`;
      } catch { return '<span>[图片]</span>'; }
    }
  );

  // 数学公式
  html = html.replace(
    /<card[^>]*name="math"[^>]*value="data:([^"]*)"[^>]*\/?>/gi,
    (_, enc) => {
      try {
        const j = JSON.parse(decodeURIComponent(enc));
        return `<span data-math="block">${j.code || ''}</span>`;
      } catch { return '<span>[公式]</span>'; }
    }
  );

  // 附件
  html = html.replace(
    /<card[^>]*name="file"[^>]*value="data:([^"]*)"[^>]*\/?>/gi,
    (_, enc) => {
      try {
        const j = JSON.parse(decodeURIComponent(enc));
        return `<a href="${j.src || ''}" data-attachment="true">${j.name || '附件'}</a>`;
      } catch { return '<span>[附件]</span>'; }
    }
  );

  // 视频
  html = html.replace(
    /<card[^>]*name="video"[^>]*value="data:([^"]*)"[^>]*\/?>/gi,
    (_, enc) => {
      try {
        const j = JSON.parse(decodeURIComponent(enc));
        return `<a href="${j.src || ''}" data-video="true">[视频: ${j.name || ''}]</a>`;
      } catch { return '<span>[视频]</span>'; }
    }
  );

  // 水平线 card
  html = html.replace(/<card[^>]*name="hr"[^>]*>[\s\S]*?<\/card>/gi, '<hr />');
  html = html.replace(/<card[^>]*name="hr"[^>]*\/>/gi, '<hr />');

  // 复选框 card（任务列表中的勾选框）
  html = html.replace(/<card[^>]*name="checkbox"[^>]*value="data:true"[^>]*>[\s\S]*?<\/card>/gi, '<input type="checkbox" checked />');
  html = html.replace(/<card[^>]*name="checkbox"[^>]*value="data:false"[^>]*>[\s\S]*?<\/card>/gi, '<input type="checkbox" />');
  html = html.replace(/<card[^>]*name="checkbox"[^>]*>[\s\S]*?<\/card>/gi, '<input type="checkbox" />');

  // 语雀内联引用（链接到其他语雀文档）
  html = html.replace(/<card[^>]*name="yuqueinline"[^>]*value="data:([^"]*)"[^>]*>[\s\S]*?<\/card>/gi, (_, enc) => {
    try { const j = JSON.parse(decodeURIComponent(enc)); return `<a href="${j.src || ''}">${j.detail?.title || j.src || '语雀文档'}</a>`; }
    catch { return '<span>[语雀文档]</span>'; }
  });
  html = html.replace(/<card[^>]*name="yuqueinline"[^>]*value="data:([^"]*)"[^>]*\/>/gi, (_, enc) => {
    try { const j = JSON.parse(decodeURIComponent(enc)); return `<a href="${j.src || ''}">${j.detail?.title || j.src || '语雀文档'}</a>`; }
    catch { return '<span>[语雀文档]</span>'; }
  });

  // 语雀文档嵌入（块级）
  html = html.replace(/<card[^>]*name="yuque"[^>]*value="data:([^"]*)"[^>]*>[\s\S]*?<\/card>/gi, (_, enc) => {
    try { const j = JSON.parse(decodeURIComponent(enc)); return `\n<a href="${j.src || ''}">[嵌入文档: ${j.detail?.title || j.src || ''}]</a>\n`; }
    catch { return '\n[嵌入文档]\n'; }
  });
  html = html.replace(/<card[^>]*name="yuque"[^>]*value="data:([^"]*)"[^>]*\/>/gi, (_, enc) => {
    try { const j = JSON.parse(decodeURIComponent(enc)); return `\n<a href="${j.src || ''}">[嵌入文档: ${j.detail?.title || j.src || ''}]</a>\n`; }
    catch { return '\n[嵌入文档]\n'; }
  });

  // 第三方嵌入（bilibili、优酷等）
  html = html.replace(/<card[^>]*name="thirdparty"[^>]*value="data:([^"]*)"[^>]*>[\s\S]*?<\/card>/gi, (_, enc) => {
    try { const j = JSON.parse(decodeURIComponent(enc)); return `\n[外部内容: ${j.src || ''}]\n`; }
    catch { return '\n[外部嵌入内容]\n'; }
  });
  html = html.replace(/<card[^>]*name="thirdparty"[^>]*value="data:([^"]*)"[^>]*\/>/gi, (_, enc) => {
    try { const j = JSON.parse(decodeURIComponent(enc)); return `\n[外部内容: ${j.src || ''}]\n`; }
    catch { return '\n[外部嵌入内容]\n'; }
  });

  // 书签链接
  html = html.replace(/<card[^>]*name="bookmarklink"[^>]*value="data:([^"]*)"[^>]*>[\s\S]*?<\/card>/gi, (_, enc) => {
    try { const j = JSON.parse(decodeURIComponent(enc)); return `\n<a href="${j.src || ''}">${j.detail?.title || j.text || j.src || '链接'}</a>\n`; }
    catch { return '\n[书签链接]\n'; }
  });
  html = html.replace(/<card[^>]*name="bookmarklink"[^>]*value="data:([^"]*)"[^>]*\/>/gi, (_, enc) => {
    try { const j = JSON.parse(decodeURIComponent(enc)); return `\n<a href="${j.src || ''}">${j.detail?.title || j.text || j.src || '链接'}</a>\n`; }
    catch { return '\n[书签链接]\n'; }
  });

  // 图册（多图）
  html = html.replace(/<card[^>]*name="imageGallery"[^>]*value="data:([^"]*)"[^>]*>[\s\S]*?<\/card>/gi, (_, enc) => {
    try {
      const j = JSON.parse(decodeURIComponent(enc));
      const imgs = (j.imageList || []).map(img => `![图片](${img.src || ''})`).join('\n');
      return '\n' + imgs + '\n';
    } catch { return '\n[图册]\n'; }
  });
  html = html.replace(/<card[^>]*name="imageGallery"[^>]*value="data:([^"]*)"[^>]*\/>/gi, (_, enc) => {
    try {
      const j = JSON.parse(decodeURIComponent(enc));
      const imgs = (j.imageList || []).map(img => `![图片](${img.src || ''})`).join('\n');
      return '\n' + imgs + '\n';
    } catch { return '\n[图册]\n'; }
  });

  // 标签
  html = html.replace(/<card[^>]*name="label"[^>]*value="data:([^"]*)"[^>]*>[\s\S]*?<\/card>/gi, (_, enc) => {
    try { const j = JSON.parse(decodeURIComponent(enc)); return `\`${j.label || '标签'}\``; }
    catch { return '`标签`'; }
  });
  html = html.replace(/<card[^>]*name="label"[^>]*value="data:([^"]*)"[^>]*\/>/gi, (_, enc) => {
    try { const j = JSON.parse(decodeURIComponent(enc)); return `\`${j.label || '标签'}\``; }
    catch { return '`标签`'; }
  });

  // 思维导图 / 画板 / 数据表 / 投票 / 打卡 / 日历（复杂 card）—— 标记为不可导出
  html = html.replace(
    /<card[^>]*name="(board|mindmap|diagram|yuque-diagram|puml|dataTable|vote|checkIn|calendar)"[^>]*>[\s\S]*?<\/card>/gi,
    (_, name) => `<span>[${name} - 请在语雀中查看]</span>`
  );
  html = html.replace(
    /<card[^>]*name="(board|mindmap|diagram|yuque-diagram|puml|dataTable|vote|checkIn|calendar)"[^>]*\/>/gi,
    (_, name) => `<span>[${name} - 请在语雀中查看]</span>`
  );

  // 清除其余未识别 card（自闭合 + 配对）
  html = html.replace(/<card[^>]*>[\s\S]*?<\/card>/gi, '');
  html = html.replace(/<card[^>]*\/>/gi, '');

  // ===== Phase 2: DOMParser 解析 =====
  const doc = new DOMParser().parseFromString(html, 'text/html');

  function nodeToMd(node, ctx) {
    ctx = ctx || { indent: '', listIndex: 0, listType: 'ul' };

    if (node.nodeType === 3) return node.textContent;
    if (node.nodeType !== 1) return '';

    const tag = node.tagName.toLowerCase();
    if (tag === 'meta' || tag === 'head' || tag === 'style' || tag === 'script') return '';

    const children = (overrideCtx) =>
      Array.from(node.childNodes).map(c => nodeToMd(c, overrideCtx || ctx)).join('');

    // --- 标题 ---
    if (/^h([1-6])$/.test(tag)) {
      const level = parseInt(RegExp.$1);
      const text = (node.innerText || children()).trim();
      return text ? `\n${'#'.repeat(level)} ${text}\n\n` : '';
    }

    // --- 段落 ---
    if (tag === 'p') {
      const t = children().trim();
      return t ? `\n${t}\n` : '\n';
    }

    // --- 列表 ---
    if (tag === 'ul' || tag === 'ol') {
      const newCtx = {
        indent: ctx.indent + (node.parentElement?.tagName?.toLowerCase() === 'li' ? '' : ''),
        listIndex: 0,
        listType: tag,
        parentIndent: ctx.indent
      };
      return '\n' + Array.from(node.children).map((li, i) => {
        newCtx.listIndex = i + 1;
        return nodeToMd(li, newCtx);
      }).join('') + '\n';
    }

    if (tag === 'li') {
      const prefix = ctx.listType === 'ol' ? `${ctx.listIndex}. ` : '- ';
      // 检查是否是任务列表
      const checkbox = node.querySelector(':scope > input[type="checkbox"]');
      let content;
      if (checkbox) {
        const checked = checkbox.checked ? 'x' : ' ';
        content = `- [${checked}] `;
        // 移除 checkbox 后获取剩余内容
        const clone = node.cloneNode(true);
        clone.querySelector('input[type="checkbox"]')?.remove();
        content += Array.from(clone.childNodes).map(c => nodeToMd(c, ctx)).join('').trim();
      } else {
        content = `${prefix}${children().trim()}`;
      }
      // 处理嵌套列表的缩进
      const indent = ctx.parentIndent || '';
      const lines = content.split('\n');
      return indent + lines[0] + '\n' +
        lines.slice(1).filter(l => l.trim()).map(l => indent + '  ' + l).join('\n') +
        (lines.length > 1 ? '\n' : '');
    }

    // --- 表格 ---
    if (tag === 'table') {
      const rows = Array.from(node.querySelectorAll('tr'));
      if (!rows.length) return '';
      const result = rows.map((r, i) => {
        const cells = Array.from(r.querySelectorAll('th,td')).map(c =>
          (c.innerText || '').trim().replace(/\|/g, '\\|').replace(/\n/g, ' ')
        );
        const line = '| ' + cells.join(' | ') + ' |';
        if (i === 0) {
          return line + '\n| ' + cells.map(() => '---').join(' | ') + ' |';
        }
        return line;
      }).join('\n');
      return `\n\n${result}\n\n`;
    }

    // --- 引用 ---
    if (tag === 'blockquote') {
      const inner = children().trim();
      return '\n' + inner.split('\n').map(l => `> ${l}`).join('\n') + '\n';
    }

    // --- 预格式代码块 ---
    if (tag === 'pre') {
      const lang = node.getAttribute('data-lang') || '';
      const code = node.innerText || children();
      return `\n\n\`\`\`${lang}\n${code}\n\`\`\`\n\n`;
    }

    // --- 行内代码 ---
    if (tag === 'code') {
      // 如果父级是 pre，直接返回内容
      if (node.parentElement?.tagName?.toLowerCase() === 'pre') return node.innerText || children();
      const t = node.innerText || children();
      return `\`${t}\``;
    }

    // --- 加粗 ---
    if (tag === 'strong' || tag === 'b') {
      const t = children();
      return t.trim() ? `**${t}**` : '';
    }

    // --- 斜体 ---
    if (tag === 'em' || tag === 'i') {
      const t = children();
      return t.trim() ? `*${t}*` : '';
    }

    // --- 删除线 ---
    if (tag === 'del' || tag === 's') {
      const t = children();
      return t.trim() ? `~~${t}~~` : '';
    }

    // --- 下划线（Markdown 无原生语法，用 HTML） ---
    if (tag === 'u') return `<u>${children()}</u>`;

    // --- 高亮 / mark ---
    if (tag === 'mark') return `==${children()}==`;

    // --- 链接 ---
    if (tag === 'a') {
      if (node.getAttribute('data-attachment') === 'true') {
        return `[📎 ${children()}](${node.getAttribute('href') || ''})`;
      }
      if (node.getAttribute('data-video') === 'true') {
        return children();
      }
      const href = node.getAttribute('href') || '';
      const text = children();
      return href ? `[${text}](${href})` : text;
    }

    // --- 图片 ---
    if (tag === 'img') {
      const src = node.getAttribute('src') || '';
      const alt = node.getAttribute('alt') || '图片';
      return `![${alt}](${src})`;
    }

    // --- 分割线 ---
    if (tag === 'hr') return '\n\n---\n\n';

    // --- 换行 ---
    if (tag === 'br') return '\n';

    // --- 数学公式 ---
    if (node.getAttribute('data-math') === 'block') {
      const formula = node.textContent || '';
      return `\n\n$$\n${formula}\n$$\n\n`;
    }

    // --- 行内公式（语雀用 <span data-type="inline-math"> 或 class） ---
    if (node.getAttribute('data-type') === 'inline-math') {
      return `$${node.textContent || ''}$`;
    }

    // --- 默认递归 ---
    return children();
  }

  let md = `# ${title}\n\n` + nodeToMd(doc.body);

  // ===== Phase 3: 后处理 =====
  // 清理连续空行（最多保留 2 个换行）
  md = md.replace(/\n{3,}/g, '\n\n');
  // 清理行尾空格
  md = md.replace(/[ \t]+$/gm, '');

  return md.trim() + '\n';
};
'lakeToMarkdown injected';
```

### Step 5：分批下载文档并传回 Claude

**不要一次性下载所有文档**。按 5 篇一批下载，每批的结果通过 `evaluate_script` 返回给 Claude，由 Claude 在本地写文件。

对每一批，执行：

```javascript
const BOOK_ID = /* ... */;
const slugs = /* 本批次的 slug 列表，如 ['slug1', 'slug2', ...] */;
const titles = /* 对应的 title 列表 */;

const results = await Promise.all(slugs.map(async (slug, i) => {
  for (let retry = 0; retry < 3; retry++) {
    try {
      const r = await fetch(`/api/docs/${slug}?book_id=${BOOK_ID}`, {
        credentials: 'include', headers: { 'Accept': 'application/json' }
      });
      if (r.status === 429) {
        await new Promise(ok => setTimeout(ok, 2000 * (retry + 1)));
        continue;
      }
      const data = await r.json();
      const content = data.data?.content || data.data?.body_lake || data.data?.body_html || '';
      return { slug, title: titles[i], md: window._lakeToMarkdown(content, titles[i]), ok: true };
    } catch (e) {
      if (retry === 2) return { slug, title: titles[i], md: `# ${titles[i]}\n\n(导出失败: ${e.message})\n`, ok: false };
      await new Promise(ok => setTimeout(ok, 1000));
    }
  }
}));

JSON.stringify(results);
```

**重要**：
- 文档内容字段优先级：`content`（主字段，lake HTML 格式）→ `body_lake` → `body_html`
- 每批完成后向用户报告进度：「已下载 15/42 篇文档...」
- 如果 `evaluate_script` 返回结果被截断（内容过长），将批次大小减至 2 或 1

### Step 6：写入本地文件

拿到每批的 JSON 结果后，立即用 Bash 的 `cat <<'HEREDOC'` 或 Python 写入对应的文件：

1. 根据 Step 3 构建的目录树，计算每篇文档的输出路径
2. 用 `mkdir -p` 创建目录结构
3. 将 Markdown 内容写入文件

```python
import os, json, sys

output_dir = sys.argv[1]  # 输出目录
data = json.loads(sys.argv[2])  # [{"slug": ..., "title": ..., "md": ..., "path": ...}]

for doc in data:
    filepath = os.path.join(output_dir, doc['path'])
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(doc['md'])
```

**注意**：如果 JSON 太大无法通过命令行参数传递，改用临时文件。

### Step 7（可选）：下载图片到本地

仅在用户指定 `--images` 时执行。

1. 扫描所有已写入的 `.md` 文件，提取 `![...](https://cdn.nlark.com/...)` 中的图片 URL
2. 用 `curl` 或 `wget` 批量下载到 `{output_dir}/_assets/` 目录
3. 将 Markdown 中的 URL 替换为相对路径 `_assets/xxx.png`

```bash
# 提取所有图片 URL
grep -roh 'https://cdn\.nlark\.com/[^)]*' OUTPUT_DIR/*.md | sort -u > /tmp/yuque-images.txt

# 批量下载
mkdir -p OUTPUT_DIR/_assets
cd OUTPUT_DIR/_assets
while IFS= read -r url; do
  filename=$(echo "$url" | sed 's/.*\///' | sed 's/?.*//')
  curl -sL "$url" -o "$filename" &
done < /tmp/yuque-images.txt
wait
```

然后用 `sed` 或 Python 批量替换路径。

### Step 8：生成导出报告

完成后向用户汇报：

- 知识库名称
- 导出目录路径
- 文档总数 / 成功数 / 失败数
- 目录结构概览（用 `tree` 或 `ls -R` 展示前几层）
- 如有失败文档，列出失败的标题和原因

## 目录结构构建算法

`/api/catalog_nodes` 返回的节点包含 `uuid`、`parent_uuid`、`type`、`level` 字段。构建目录树的逻辑：

1. 创建 uuid → node 的映射
2. `parent_uuid` 为空字符串的是根级节点
3. `type === 'TITLE'`（大写）的节点是纯目录节点（不含内容），其 `title` 用作目录名
4. `type === 'DOC'`（大写）的节点是文档，生成 `{title}.md` 文件；其 `url` 字段即 slug
5. 递归构建路径：从文档出发，沿 `parent_uuid` 向上追溯到根，拼接路径
6. 文件名清理：将 `< > : " / \ | ? *` 替换为 `_`，截断到 80 字符
7. **注意**：DOC 节点也可能是其他节点的 parent（如"如何构建知识网络"既是文档也是目录），此时该 DOC 既导出为 md 文件，也作为其子文档的父目录

示例输出结构：
```
yuque-export/
├── 快速开始.md
├── 基础/
│   ├── 安装.md
│   └── 配置.md
└── 进阶/
    ├── 插件开发.md
    └── API 参考.md
```

## 错误处理

- **401 未登录**：引导用户登录后重试
- **404 知识库不存在**：检查 URL 是否正确，namespace 是否匹配
- **429 限流**：自动指数退避重试（2s → 4s → 8s），最多 3 次
- **单文档下载失败**：记录失败，继续下载其他文档，最终汇报失败列表
- **evaluate_script 返回截断**：减小批次大小重试
- **空文档**：正常标记为空，不视为错误

## 注意事项

- **必须使用 Chrome DevTools MCP**：需要浏览器的登录 session
- **lake 格式**：语雀自研格式，代码块/图片/公式等存储为 URL 编码的 JSON card
- **图片默认不下载**：导出的 Markdown 引用语雀 CDN 链接，需要 `--images` 才下载到本地
- **大知识库**：超过 100 篇文档时，耐心等待，每批会报告进度
- **特殊内容**：思维导图、画板等复杂元素无法导出为 Markdown，会标记提示在语雀中查看
