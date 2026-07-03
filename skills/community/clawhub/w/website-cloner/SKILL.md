# Website Cloner — 网站 1:1 本地复刻

## 定位

将任意在线网站完整复刻到本地，保持视觉、交互、页面层级结构一致。适用于研究学习、本地改造、离线浏览。

## 执行流程（6 步）

### Step 1 — 站点侦察

```bash
# 确认站点可访问性
curl -sL -o /tmp/site_index.html -w "HTTP %{http_code} Size %{size_download}" --max-time 15 <URL>

# 判断站点类型
head -50 /tmp/site_index.html  # SPA 通常 <body> 很空，由 JS 渲染；传统站点 HTML 内容丰富
```

**关键判断：**
- SPA（hash 路由 / JS 渲染）：必须下载 JS 数据文件，HTML 只是壳
- 传统多页：wget 镜像即可，注意 CSS/JS/图片路径
- 混合型：首页静态 + 内页 JS 渲染

### Step 2 — 资源清单

不要只下载 HTML！必须递归发现所有依赖：

```bash
# 1. 提取 HTML 中的资源
grep -oE 'src="[^"]*"|href="[^"]*"' index.html | sort -u

# 2. ⚠️ 关键：检查 CSS 中的 @import 链
grep -n '@import\|@font-face\|url(' *.css tokens/*.css 2>/dev/null

# 3. 检查 JS 中的数据文件引用
grep -oE '"[a-z_/]+\.(css|js|png|jpg|webp|woff2|svg|json|otf)"' app.js | sort -u

# 4. 检查 JS 中的全局变量（数据可能内嵌在 JS 中）
grep -oE 'window\.WY_[A-Z_]+' app.js | sort -u

# 5. 检查字体文件引用
grep -rh 'font-face\|\.otf\|\.woff2\|\.ttf' tokens/ 2>/dev/null
```

**⚠️ 最常见的遗漏：CSS token/变量文件**

很多现代站点把 CSS 变量（颜色、字体、间距）拆成独立文件：
```
styles.css → @import tokens/fonts.css
           → @import tokens/colors.css    ← 丢了 = 所有颜色/背景/主题失效
           → @import tokens/typography.css ← 丢了 = 所有字体/字号/行高失效
           → @import tokens/spacing.css   ← 丢了 = 所有间距/圆角/动效失效
```

### Step 3 — 批量下载

```bash
# 创建目录结构
mkdir -p local-site/{assets/cards,assets/thumbs,data,tokens,fonts}

# 下载核心文件
curl -sL --max-time 15 -o index.html <URL>/
curl -sL --max-time 15 -o app.css <URL>/app.css
curl -sL --max-time 15 -o app.js <URL>/app.js

# ⚠️ 下载所有 token 文件（如果 styles.css 是 @import 入口）
curl -sL --max-time 15 -o tokens/fonts.css <URL>/tokens/fonts.css
curl -sL --max-time 15 -o tokens/colors.css <URL>/tokens/colors.css
curl -sL --max-time 15 -o tokens/typography.css <URL>/tokens/typography.css
curl -sL --max-time 15 -o tokens/spacing.css <URL>/tokens/spacing.css

# 下载字体
curl -sL --max-time 15 -o fonts/brand-medium.otf <URL>/fonts/brand-medium.otf

# 下载 favicon / logo / og 图
curl -sL --max-time 15 -o assets/logo.png <URL>/assets/logo.png
curl -sL --max-time 15 -o assets/favicon-32.png <URL>/assets/favicon-32.png
```

### Step 4 — 本地适配

**必须修改的内容：**

```bash
# 1. 移除第三方统计/追踪
sed -i '' '/vercel\|analytics\|gtag\|ga.js\|script.js/d' index.html

# 2. 注释 Google Fonts CDN（国内免翻，用系统字体回退）
sed -i '' 's|@import url(.https://fonts.googleapis.com.|/* Google Fonts 已注释（本地版用系统字体回退）\n@import url(https://fonts.googleapis.com.|' tokens/fonts.css
# 手动补上 */ 闭合注释

# 3. 替换作者/外链信息为用户自己的
sed -i '' 's|原始作者名|你的名字|g' app.js
sed -i '' 's|https://github.com/original|#|g' app.js
sed -i '' 's|https://x.com/original|#|g' app.js

# 4. 如果图片格式不匹配（如站点用 webp 但只有 jpg）
sed -i '' 's|.webp|.jpg|g' app.js

# 5. 检查 og:url / canonical 等绝对 URL
grep -rn 'https://原始域名' .
```

**不要改的内容：**
- localStorage key 前缀（不影响功能）
- CSS class 命名
- JS 路由逻辑

### Step 5 — 图片处理

如果站点图片无法直接下载，可从其他来源补充：

```bash
# PNG → JPG（macOS 内置 sips）
sips -s format jpeg -s formatOptions 85 source.png --out dest.jpg

# 生成缩略图
sips -s format jpeg -s formatOptions 60 -Z 480 source.png --out thumb.jpg

# 批量转换
for f in *.png; do
  id=$(echo "$f" | sed 's/\.png$//')
  sips -s format jpeg -s formatOptions 85 "$f" --out cards/${id}.jpg
  sips -s format jpeg -s formatOptions 60 -Z 480 "$f" --out thumbs/${id}.jpg
done
```

### Step 6 — 验证闭环

```bash
# 1. 启动本地服务器
cd local-site && python3 -m http.server 8765 &

# 2. HTTP 状态检查
curl -s -o /dev/null -w "%{http_code}" http://localhost:8765/
curl -s -o /dev/null -w "%{http_code}" http://localhost:8765/app.css
curl -s -o /dev/null -w "%{http_code}" http://localhost:8765/assets/cards/001.jpg

# 3. agent-browser 截图验证
npx -y agent-browser@latest open http://localhost:8765/
npx -y agent-browser@latest screenshot /tmp/local_screenshot.png

# 4. AI 视觉对比（调用任意视觉模型识别截图内容，验证布局/文字/色彩）
# 示例：python3 analyze_image.py /tmp/local_screenshot.png

# 5. 页面路由抽查
npx -y agent-browser@latest open "http://localhost:8765/#/gallery"
npx -y agent-browser@latest get count ".card"  # 确认数据量正确
npx -y agent-browser@latest open "http://localhost:8765/#/about"
npx -y agent-browser@latest get text "h3"      # 确认关于页面文字正确
```

## 核心经验

### 必查清单

| 检查项 | 方法 | 遗漏后果 |
|--------|------|----------|
| CSS @import 链 | `grep '@import' styles.css` | 全部颜色/字体/间距失效 |
| 字体文件 | `grep 'font-face\|\.otf\|\.woff2' tokens/*.css` | 中文显示异常 |
| JS 数据文件 | `grep 'src="data/' index.html` | SPA 内容为空 |
| 图片格式 | `grep '\.webp\|\.png\|\.jpg' app.js` | 图片全部裂开 |
| Google Fonts | `grep 'fonts.googleapis' tokens/*.css` | 国内加载阻塞 |
| 统计脚本 | `grep 'vercel\|analytics\|gtag' index.html` | 产生无效请求 |

### 常见问题速查

| 症状 | 根因 | 解决 |
|------|------|------|
| 所有颜色/背景/字体不对 | tokens CSS 文件未下载 | 补下载所有 @import 引用的文件 |
| 页面空白无内容 | SPA 的数据 JS 文件缺失 | 下载 data/*.js |
| 图片全部不显示 | 图片格式不匹配（webp vs jpg） | 替换 app.js 中的扩展名 |
| 加载很久才出内容 | Google Fonts CDN 被墙 | 注释掉 @import，用系统字体回退 |
| 布局混乱元素错位 | 缺少 spacing/typography tokens | 下载 tokens/*.css |
| 按钮样式全无 | 缺少 colors.css（CSS 变量未定义） | 下载 tokens/colors.css |

## 工具清单

| 工具 | 用途 | 安装 |
|------|------|------|
| `curl` | 下载站点文件 | macOS 内置 |
| `sips` | 图片格式转换/缩放 | macOS 内置 |
| `python3 -m http.server` | 本地静态服务器 | macOS 内置 |
| `agent-browser` | 无头浏览器截图/交互 | `npx -y agent-browser@latest` |
| 视觉模型 | AI 视觉识别验证 | 任意支持图片分析的视觉 LLM |
| `sed` | 批量文本替换 | macOS 内置 |

## 触发条件

当用户说以下关键词时调用此 skill：
- "复刻这个网站" / "把这个网站复制到本地" / "1:1 做本地版"
- "镜像网站" / "克隆网站" / "扒下来"
- "像上次复刻网站那样" / "用之前的复刻方法"

## 参考案例

- 2026-06 — 某传统文化 SPA 站点 1:1 本地复刻（100条数据，完整成功）
  - 踩坑：遗漏 tokens/ CSS 文件导致首版布局混乱
  - 解决：AI 视觉对比发现 → 回溯 CSS @import 链 → 补下载 token 文件
