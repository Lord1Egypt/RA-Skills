# MC 像素风 Worked Example

## 问答记录（2026-08-09）
- 风格：Minecraft 像素风（通用风格，非直接 IP 复制）
- 色彩：深色底 + 草绿主色 + 泥土棕辅色
- 氛围：怀旧像素感、趣味、温暖
- 可读性：优先，纹理够暗不刺眼

## 设计令牌（:root CSS 变量）

| 变量 | 值 | 说明 |
|------|----|------|
| `--bg` | `#191410` | 主背景（暗泥土） |
| `--bg-elevated` | `#231b13` | 提升层背景 |
| `--bg-muted` | `#2a2117` | 弱化背景 |
| `--bg-content` | `#17120d` | 内容区背景 |
| `--bg-hover` | `#2d241a` | 悬停背景 |
| `--card` | `#201810` | 卡片底色 |
| `--card-foreground` | `#f0e8d8` | 卡片文字（米白） |
| `--chat-text` | `#f0e8d8` | 聊天文字 |
| `--chat-box-inset` | `#120e09` | 输入框内底色 |
| `--border` | `#4a3b2c` | 默认边框（泥土棕） |
| `--border-hover` | `#7ca843` | 悬停边框（草绿） |
| `--border-strong` | `#6b5a40` | 强调边框 |
| `--accent` | `#7ca843` | 主强调色（草绿） |
| `--accent-hover` | `#94c55e` | 悬停强调色 |
| `--accent-muted` | `#6f8f4a` | 弱化强调色 |
| `--accent-foreground` | `#10100a` | 强调色上文字 |
| `--accent-glow` | `rgba(124,168,67,.4)` | 强调色辉光 |
| `--accent-2` | `#8b6940` | 第二强调色（暖棕） |
| `--accent-2-muted` | `#7a5b38` | 弱化第二强调 |
| `--accent-2-subtle` | `#3a2e1f` | 极弱第二强调 |

## 注入架构（双保险）

> 指纹三属性：`data-theme-id`（主题名）/ `data-theme-version`（主题版本）/ `data-upstream-version`（注入时 OpenClaw package.json 的 version，示例值 2026.7.1-2 按实际改）。heal.sh 靠前两个识别主题，靠第三个在重注入前做上游版本比对。

### 1. 根级主题变量（`</head>` 前）
```html
<style id="mc-theme" data-theme-id="mc" data-theme-version="1.0.0" data-upstream-version="2026.7.1-2">
:root {
  --bg: #191410 !important;
  --bg-elevated: #231b13 !important;
  /* ... 全部 20 个变量 ... */
}
</style>
```

### 2. 样式注入器（`</body>` 前）
```html
<script id="mc-injector" data-theme-id="mc" data-theme-version="1.0.0" data-upstream-version="2026.7.1-2">
(function() {
  const STYLE_ID = 'mc-css';
  const INJECTED = new WeakSet();

  function ensureDocStyle() {
    if (document.getElementById(STYLE_ID)) return;
    const style = document.createElement('style');
    style.id = STYLE_ID;
    style.textContent = `
      body, textarea, input, button, [contenteditable="true"],
      .chat-bubble, .chat-sender-name {
        font-family: "Zpix", "Courier New", "Lucida Console",
          ui-monospace, "Cascadia Mono", Consolas, monospace !important;
      }
      .chat-thread {
        background: #17120d url("assets/mc-dirt.png") repeat !important;
      }
      .card, .panel, [class*="sidebar"], [class*="nav"] {
        background: url("assets/mc-stone.png") repeat !important;
      }
      .chat-bubble {
        background: #201810 !important;
        border: 2px solid #4a3b2c !important;
        border-top: 3px solid #7ca843 !important;
        border-radius: 0 !important;
      }
      .chat-sender-name { color: #7ca843 !important; font-weight: bold; }
      .chat-bubble--tool-shell { border-left: 3px solid #7ca843 !important; }
      button, [class*="btn"] {
        background: transparent !important;
        border: 3px solid transparent !important;
        border-image: url("assets/mc-button.png") 3 fill / 3px / 0 stretch !important;
        border-radius: 0 !important;
        font-family: "Zpix", monospace !important;
      }
      button:hover { filter: brightness(1.12); transform: translateY(-1px); }
      button:active { filter: brightness(0.9); transform: translateY(1px); }
      textarea, input {
        border: 2px solid #6b5a40 !important;
        background: #120e09 !important;
        color: #f0e8d8 !important;
      }
      textarea:focus, input:focus {
        outline: 2px solid #7ca843 !important;
        border-color: #7ca843 !important;
      }
      [class*="send"] {
        background: #7ca843 !important;
        color: #10100a !important;
        border: 2px solid #2a2116 !important;
      }
      ::-webkit-scrollbar-thumb { background: #6b5a40 !important; }
      ::-webkit-scrollbar-track { background: #191410 !important; }
      @keyframes mcPop {
        0% { transform: scale(0.9); opacity: 0; }
        60% { transform: scale(1.02); }
        100% { transform: scale(1); opacity: 1; }
      }
      .chat-bubble.fade-in { animation: mcPop 0.25s ease-out; }
    `;
    document.head.appendChild(style);
  }

  function injectToShadow(root) {
    if (INJECTED.has(root)) return;
    const style = document.createElement('style');
    style.textContent = document.getElementById(STYLE_ID)?.textContent || '';
    root.appendChild(style);
    INJECTED.add(root);
  }

  // 递归遍历：shadow root 里还能再套 shadow root（套娃），一层层往下钻
  function walk(root) {
    root.querySelectorAll('*').forEach(el => {
      if (el.shadowRoot) {
        injectToShadow(el.shadowRoot);
        walk(el.shadowRoot);
      }
    });
  }

  function scanAll() {
    walk(document);
  }

  const observer = new MutationObserver(mutations => {
    mutations.forEach(m => {
      m.addedNodes.forEach(node => {
        if (node.nodeType !== 1) return;
        if (node.shadowRoot) {
          injectToShadow(node.shadowRoot);
          walk(node.shadowRoot);
        }
        walk(node); // 新子树里也可能带 shadow root（含套娃）
      });
    });
  });

  ensureDocStyle();
  scanAll();
  observer.observe(document.body, { childList: true, subtree: true });
})();
</script>
```

## 素材生成（PIL 脚本）

### 泥土纹理（32×32，块状噪声——像 MC 泥土不像电视雪花）
```python
from PIL import Image
import random
BLOCK = 4            # 每个色块 4×4 像素
GRID = 32 // BLOCK   # 先画 8×8 个小格
img = Image.new('RGB', (GRID, GRID))
for gy in range(GRID):
    for gx in range(GRID):
        noise = random.randint(-8, 8)
        r = max(0, min(255, 42 + noise))
        g = max(0, min(255, 32 + noise))
        b = max(0, min(255, 24 + noise))
        img.putpixel((gx, gy), (r, g, b))
# 可选：随机撒几个深色「碎石块」，更像 MC 泥土
for gy in range(GRID):
    for gx in range(GRID):
        if random.random() < 0.15:
            img.putpixel((gx, gy), (36, 26, 18))
img = img.resize((32, 32), Image.NEAREST)  # 最近邻放大 → 块状边缘
img.save('mc-dirt.png')
```

### 石头纹理（32×32，块状噪声）
```python
from PIL import Image
import random
BLOCK = 4
GRID = 32 // BLOCK
img = Image.new('RGB', (GRID, GRID))
for gy in range(GRID):
    for gx in range(GRID):
        noise = random.randint(-10, 10)
        r = max(0, min(255, 58 + noise))
        g = max(0, min(255, 58 + noise))
        b = max(0, min(255, 58 + noise))
        img.putpixel((gx, gy), (r, g, b))
img = img.resize((32, 32), Image.NEAREST)
img.save('mc-stone.png')
```

### 9-slice 浮雕按钮（16×16）
```python
from PIL import Image
import random
img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
for i in range(16):  # 外黑边
    img.putpixel((i, 0), (0, 0, 0, 255))
    img.putpixel((i, 15), (0, 0, 0, 255))
    img.putpixel((0, i), (0, 0, 0, 255))
    img.putpixel((15, i), (0, 0, 0, 255))
for i in range(1, 3):  # 上/左高光
    for j in range(1, 15):
        img.putpixel((j, i), (168, 168, 154, 255))
        img.putpixel((i, j), (168, 168, 154, 255))
for i in range(13, 15):  # 下/右阴影
    for j in range(1, 15):
        img.putpixel((j, i), (70, 70, 56, 255))
        img.putpixel((i, j), (70, 70, 56, 255))
for y in range(3, 13):  # 中心填色 + 噪声
    for x in range(3, 13):
        noise = random.randint(-5, 5)
        r = max(0, min(255, 114 + noise))
        g = max(0, min(255, 114 + noise))
        b = max(0, min(255, 70 + noise))
        img.putpixel((x, y), (r, g, b, 255))
img.save('mc-button.png')
```

## 版权
- Zpix 字体：个人/教育免费，商业单产品需付费 ¥7000
- 纹理/按钮：PIL 自绘，零版权，可安全开源
- 灵感：Minecraft 像素风（通用风格，非直接 IP 复制）

## 坑与教训
1. Ctrl+Shift+R 强制刷新才能看到改动，普通刷新有缓存
2. PIL 脚本用相对路径，先在目标目录 cd 再跑
3. Zpix 按 12px 点阵设计，字号取 12 倍数最清晰
4. MutationObserver 只捕获新增节点，已有节点要手动 scanAll()；scanAll 必须**递归**进 shadow root（shadow root 套 shadow root 的套娃也扫到），否则内层组件的主题样式会漏
5. 改 id 时注意 JS 里 getElementById 引用同步改