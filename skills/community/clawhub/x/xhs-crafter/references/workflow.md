# XHS Crafter 工作流详细参考

> v7.5 — 5步工作流（默认本地全自动，外部能力需用户同意）

## 完整流程

```
MD文章输入
  ↓ Step 1: Intake — 识别品类（脑内完成）
  ↓ Step 2: Content Plan — 内容规划（脑内完成）
  ↓ Step 3: Compose — 组装HTML（直接执行）
  ↓ Step 4: Validate — 自检（自动执行）
  ↓ Step 5: Screenshot & Deliver — 截图交付（直接执行）
```

## Step 1: Intake — 识别品类

- 读取MD内容，自动推断内容品类
- 参考 `references/category-cookbook.md` 路由到对应风格/主题
- 确定目标平台（默认小红书3:4）
- 识别用户图片（MD中图片标记或指定截图文件夹）
- 仅在品类无法推断时才问用户

## Step 2: Content Plan — 内容规划

- 参考 `references/content-planning.md`
- 压缩阶梯：核心论点1句 → 读者承诺 → 4-8个分论点 → 页面钩子 → 正文片段
- 页面角色分配：7页组图至少5种不同形态
- 页面节奏规划：参考 `references/portrait-fill.md` 的"Three-Layer Rhythm System"
- 5页及以上：封面和封底都必须有图片背景

## Step 3: Compose — 组装HTML

- 拷贝种子模板：Editorial→ `assets/template-editorial-card.html`；Swiss→ `assets/template-swiss-card.html`
- 设置 `data-theme` 或 `data-accent` 属性切换主题
- 在 `<!-- POSTERS_HERE -->` 处添加页面
- 满铺图页遵循 `references/image-overlay.md`
- 密度保障：每页活跃构图≥78%画布高度
- 节奏保障：暗色页插入、氛围强弱交替、版式不重复
- **图片必须下载到本地**：Puppeteer headless无法可靠加载外部API图片
  > ⚠️ **外部下载风险提示（v7.7）**：以下步骤涉及从外部 CDN 下载图片文件到本地。下载内容受 ALLOWED_HOSTS 域名白名单限制（images.pexels.com / images.unsplash.com），防止 SSRF。仅在用户通过 Step 1 图片三选一门控选择 B 或 C 后执行。
  1. 用WebFetch获取API返回的CDN URL
  2. 用curl下载到项目`assets/`目录
  3. HTML中用本地相对路径引用
  4. 禁止直接引用外部URL

## Step 4: Validate — 自检

截图前自动检查，不通过则自动修复：

- **密度检查**：每页活跃构图≥78% | 每页≥3种内容元素 | 纯空白带>216px需理由
- **图片检查**：封面1秒说清主题 | 文字未压主体 | 无broken image
- **节奏检查**：5页+至少1暗色页 | 暗色页不相邻 | 氛围强弱交替 | 版式不重复
- **风格检查**（参考 `references/style-system.md`）

## Step 5: Screenshot & Deliver — 截图交付

### 截图

- 用 `assets/screenshot.js` 截图（自动检测页面ID和Chrome路径）
- 用法：先启动 `python -m http.server 8090 --bind 127.0.0.1`（绑定本地回环，不暴露局域网），然后 `node assets/screenshot.js <项目目录>`
- puppeteer-core + 系统Chrome，deviceScaleFactor:2
- 等待 networkidle0 + fonts.ready + 6秒（确保图片加载）

### 文字压缩

- 保留原话引言+场景描述+核心数据，≤1000字
- 压缩模板：标题(1句) → 场景开场(1-2句) → 核心论点(1-2句) → 关键原话(1-2条) → 数据支撑(3-5个数字) → 结尾原话(1条)

### 交付方式：本地文件夹（默认）+ 飞书云盘同步（可选，需用户同意）

**A. 本地文件夹（默认）**
> ⚠️ **本地文件写入提示**：将在 `$env:TEMP` 创建 `<slug>公众号素材/` 文件夹并写入 PNG+txt 文件。截图完成后告知用户交付路径，再继续后续步骤。
1. 截图完成后，告知用户：`已生成 N 张 PNG + 文字稿，将保存到 $env:TEMP/<slug>公众号素材/`
2. 在 `$env:TEMP` 创建 `<slug>公众号素材/` 文件夹
3. 将PNG+txt复制到该文件夹
4. 用 `explorer.exe` 打开文件夹
5. 完成本地交付后，**询问是否上传到飞书云盘**（不主动执行）

**B. 飞书云盘同步（可选，需用户明确同意）**
> ⚠️ **数据外发提示**：上传会将文章相关PNG和文字稿传输到飞书云服务器，离开本地环境。如果文章包含未发布/敏感/专有内容，请勿启用。需要用户已登录lark-cli。

**飞书同步同意门控**（仅在本地交付完成后触发一次）：
```
本地文件夹已交付。是否需要同步到飞书云盘？
- 是 → 执行下方上传步骤
- 否 → 结束（本地文件夹已是完整交付物）
```

**用户同意后执行**：
1. 用 `lark-cli drive +create-folder` 创建 `<slug>公众号素材` 文件夹
2. cd到output目录，用 `lark-cli drive +upload` 逐个上传
3. 返回飞书云盘文件夹URL

## 封面背景图问题修复

**问题**：CSS background-image 在 Puppeteer headless 模式下可能不加载外部图片。

**解决方案**：
- 使用 `<img>` 标签替代 CSS background-image
- 用绝对定位 + object-fit:cover 实现全屏背景效果
- 外部API图片必须先下载到本地assets/目录再引用
- 截图前等待 networkidle0 + 6秒缓冲
