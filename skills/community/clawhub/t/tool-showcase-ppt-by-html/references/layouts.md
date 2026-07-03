# 页面布局库(Layouts)

24 种工具介绍专用布局骨架。每种都是完整可粘贴的 `<section>` 代码块,替换文案/图片即可使用。

---

## 预检(Pre-flight)

- **所有类名必须在 `template.html` 的 `<style>` 里有定义**。不确定时先读 template.html 确认
- 不要发明新类名。如需自定义,用 `style="..."` inline
- 图片用标准路径 `images/xxx.png`,放在 `{工具名}.html` 同级 images/ 下
- `grep "[必填]" {工具名}.html` 确认 title 已替换(任务 5 完成后)
- 每页 `<section>` 必须是 `slide light` 或 `slide dark` 或 `slide hero light` 或 `slide hero dark` 之一

---

## 主题节奏规划

- Hero 页(封面/CTA)和正文页交替,每 3-4 页插一个 hero
- Light/Dark 交替,连续不超过 3 页同色
- 8 页以上必须有 ≥1 个 hero dark + ≥1 个 hero light

---

## T01: Hero 封面

工具名 + 一句话定位 + 主视觉截图。用 `hero dark` 开场。

```html
<section class="slide hero dark">
  <div class="chrome-min">
    <span>工具介绍</span>
    <span>01 / 08</span>
  </div>
  <div class="frame center" style="gap:3vh">
    <div class="kicker" data-anim="d1">效率工具 · 截图 & 标注</div>
    <h1 class="h-hero" data-anim="d2">ScreenCap</h1>
    <p class="lead" style="max-width:50vw;text-align:center" data-anim="d3">
      一键截图、智能识别窗口、像素级标注 —— 比系统自带好用 10 倍。
    </p>
    <div class="cta-group" style="justify-content:center" data-anim="d4">
      <a href="#" class="cta-btn primary">
        <i data-lucide="download" style="width:1.2em;height:1.2em"></i> 免费下载
      </a>
      <a href="#" class="cta-btn secondary">
        <i data-lucide="github" style="width:1.2em;height:1.2em"></i> GitHub
      </a>
    </div>
  </div>
  <div class="footer-min">
    <span>v2.1.0 · Windows 10+</span>
    <span>github.com/user/screencap</span>
  </div>
</section>
```

---

## T02: 功能卡片网格

3-6 个核心功能,卡片式展示。用 `slide light`。

```html
<section class="slide light">
  <div class="chrome-min">
    <span>核心功能</span>
    <span>02 / 08</span>
  </div>
  <div class="frame" style="padding-top:4vh">
    <div class="kicker" data-anim="d1">Features</div>
    <h2 class="h-xl" data-anim="d2">六大核心能力</h2>

    <div class="grid-6" style="margin-top:4vh">
      <div class="feat-card" data-anim="d1">
        <div class="feat-icon"><i data-lucide="camera"></i></div>
        <div class="feat-title">全屏截图</div>
        <div class="feat-desc">一键捕获整个屏幕,支持多显示器,快捷键自定义</div>
      </div>
      <div class="feat-card" data-anim="d2">
        <div class="feat-icon"><i data-lucide="scan-eye"></i></div>
        <div class="feat-title">窗口识别</div>
        <div class="feat-desc">自动识别活动窗口区域,智能裁剪,无需手动框选</div>
      </div>
      <div class="feat-card" data-anim="d3">
        <div class="feat-icon"><i data-lucide="pencil"></i></div>
        <div class="feat-title">像素标注</div>
        <div class="feat-desc">箭头、矩形、文字、马赛克,像素级精确标注</div>
      </div>
      <div class="feat-card" data-anim="d4">
        <div class="feat-icon"><i data-lucide="pipette"></i></div>
        <div class="feat-title">屏幕取色</div>
        <div class="feat-desc">实时取色器,HEX/RGB/HSL 多格式,一键复制</div>
      </div>
      <div class="feat-card" data-anim="d5">
        <div class="feat-icon"><i data-lucide="copy"></i></div>
        <div class="feat-title">剪贴板集成</div>
        <div class="feat-desc">截图自动复制到剪贴板,直接粘贴到任意应用</div>
      </div>
      <div class="feat-card feat-card accent" data-anim="d6">
        <div class="feat-icon"><i data-lucide="zap"></i></div>
        <div class="feat-title">极速启动</div>
        <div class="feat-desc">常驻系统托盘,毫秒级响应,不占资源</div>
      </div>
    </div>
  </div>
  <div class="footer-min">
    <span>Features · 6 Core</span>
    <span>—</span>
  </div>
</section>
```

**要点**:
- 3 个功能用 `.grid-3`,4 个用 `.grid-4`,6 个用 `.grid-6`
- 核心/主打功能用 `.feat-card.accent` 突出
- 图标用 Lucide: `camera / scan-eye / pencil / pipette / copy / zap`

---

## T03: 大图截图展示

单张完整界面截图,展示工具全貌。用 `slide dark` 突出截图。

```html
<section class="slide dark">
  <div class="chrome-min">
    <span>界面展示</span>
    <span>03 / 08</span>
  </div>
  <div class="frame center" style="gap:2vh;padding-top:2vh">
    <h2 class="h-lg" data-anim="d1">主界面一览</h2>
    <div class="screenshot-wrap" style="max-width:80vw" data-anim="d2">
      <img src="images/03-main-ui.png" alt="主界面截图" style="max-height:55vh;width:100%;object-fit:contain">
    </div>
    <p class="screenshot-cap" data-anim="d3">▲ 主界面 · 截图标注模式</p>
  </div>
  <div class="footer-min">
    <span>Interface · Main Window</span>
    <span>—</span>
  </div>
</section>
```

---

## T04: 操作流程

3-5 步使用步骤,适合讲解工具怎么用。用 `slide light`。

```html
<section class="slide light">
  <div class="chrome-min">
    <span>使用流程</span>
    <span>04 / 08</span>
  </div>
  <div class="frame" style="padding-top:4vh">
    <div class="kicker" data-anim="d1">How it Works</div>
    <h2 class="h-xl" data-anim="d2">三步搞定截图</h2>

    <div class="steps" style="margin-top:5vh">
      <div class="step-item" data-anim="d3">
        <div class="step-num">01</div>
        <div class="step-img"><img src="images/04-step1.png" alt="步骤1"></div>
        <div class="step-title">按快捷键</div>
        <div class="step-desc">按下 Ctrl+Shift+S 激活截图,系统托盘常驻随时可用</div>
      </div>
      <div class="step-item" data-anim="d4">
        <div class="step-num">02</div>
        <div class="step-img"><img src="images/04-step2.png" alt="步骤2"></div>
        <div class="step-title">框选区域</div>
        <div class="step-desc">智能吸附窗口边界,也支持自由拖拽,实时显示像素尺寸</div>
      </div>
      <div class="step-item" data-anim="d5">
        <div class="step-num">03</div>
        <div class="step-img"><img src="images/04-step3.png" alt="步骤3"></div>
        <div class="step-title">标注保存</div>
        <div class="step-desc">箭头/文字/马赛克标注后,一键复制或保存为 PNG</div>
      </div>
    </div>
  </div>
  <div class="footer-min">
    <span>Workflow · 3 Steps</span>
    <span>—</span>
  </div>
</section>
```

---

## T05: 数据大字报

抛硬数据:性能、体积、速度等。用 `slide hero light` 制造视觉冲击。

```html
<section class="slide hero light">
  <div class="chrome-min">
    <span>性能数据</span>
    <span>05 / 08</span>
  </div>
  <div class="frame center" style="gap:5vh">
    <div class="kicker" data-anim="d1">Benchmark</div>

    <div class="grid-3" style="width:100%;max-width:70vw">
      <div class="stat-card" data-anim="d2">
        <div class="stat-label">启动速度</div>
        <div class="stat-value">&lt;0.2<span class="unit">s</span></div>
        <div class="stat-note">常驻托盘后热键唤醒,毫秒级响应</div>
      </div>
      <div class="stat-card" data-anim="d3">
        <div class="stat-label">安装体积</div>
        <div class="stat-value">8.6<span class="unit">MB</span></div>
        <div class="stat-note">单文件绿色版,无需安装依赖</div>
      </div>
      <div class="stat-card" data-anim="d4">
        <div class="stat-label">内存占用</div>
        <div class="stat-value">&lt;30<span class="unit">MB</span></div>
        <div class="stat-note">空闲时仅 12MB,比 Chrome 一个标签页还少</div>
      </div>
    </div>
  </div>
  <div class="footer-min">
    <span>Performance · Measured on Win11 i5-13500H</span>
    <span>—</span>
  </div>
</section>
```

---

## T06: 使用前后对比

Before/After 对照,展示工具带来的改变。用 `slide dark`。

```html
<section class="slide dark">
  <div class="chrome-min">
    <span>效果对比</span>
    <span>06 / 08</span>
  </div>
  <div class="frame" style="padding-top:4vh">
    <div class="kicker" data-anim="d1">Before & After</div>
    <h2 class="h-xl" data-anim="d2">有了它,效率翻倍</h2>

    <div class="grid-2-6-6" style="margin-top:4vh">
      <div class="compare-col" data-anim="d3">
        <div class="compare-label before">Before · 没有 ScreenCap</div>
        <div class="compare-img" style="aspect-ratio:16/10">
          <img src="images/06-before.png" alt="使用前" style="height:100%;object-fit:cover;object-position:top center">
        </div>
        <p class="body-sm" style="margin-top:1vh">
          Win+Shift+S → 粘贴到画图 → 手动标注 → 另存为 → 插入文档。至少 5 步,3 个软件。
        </p>
      </div>
      <div class="compare-divider" data-anim="d4">→</div>
      <div class="compare-col" data-anim="d5">
        <div class="compare-label after">After · 使用 ScreenCap</div>
        <div class="compare-img" style="aspect-ratio:16/10">
          <img src="images/06-after.png" alt="使用后" style="height:100%;object-fit:cover;object-position:top center">
        </div>
        <p class="body-sm" style="margin-top:1vh">
          快捷键 → 框选 → 标注 → 自动复制到剪贴板。全程 2 秒,一个软件。
        </p>
      </div>
    </div>
  </div>
  <div class="footer-min">
    <span>Comparison · Before vs After</span>
    <span>—</span>
  </div>
</section>
```

---

## T07: 技术规格表

系统要求、支持格式、技术参数。用 `slide light`。

```html
<section class="slide light">
  <div class="chrome-min">
    <span>技术规格</span>
    <span>07 / 08</span>
  </div>
  <div class="frame" style="padding-top:4vh">
    <div class="kicker" data-anim="d1">Tech Specs</div>
    <h2 class="h-xl" data-anim="d2">技术参数</h2>

    <table class="spec-table" style="margin-top:4vh" data-anim="d3">
      <tr><td class="spec-key">操作系统</td><td class="spec-val">Windows 10 / 11 <span class="spec-badge">64-bit</span></td></tr>
      <tr><td class="spec-key">安装方式</td><td class="spec-val">绿色便携版 · 单文件 EXE · 无需安装</td></tr>
      <tr><td class="spec-key">输出格式</td><td class="spec-val">PNG / JPG / BMP / WebP</td></tr>
      <tr><td class="spec-key">标注工具</td><td class="spec-val">箭头 · 矩形 · 圆形 · 文字 · 马赛克 · 高亮</td></tr>
      <tr><td class="spec-key">取色格式</td><td class="spec-val">HEX / RGB / HSL / CMYK</td></tr>
      <tr><td class="spec-key">快捷键</td><td class="spec-val">全局热键 · 支持自定义 · 不冲突检测</td></tr>
      <tr><td class="spec-key">多屏支持</td><td class="spec-val">最多 4 屏 · 不同 DPI 自动适配</td></tr>
      <tr><td class="spec-key">开发技术</td><td class="spec-val">Python + PyQt5 + Nuitka 编译</td></tr>
    </table>
  </div>
  <div class="footer-min">
    <span>Specifications · v2.1.0</span>
    <span>—</span>
  </div>
</section>
```

---

## T08: 场景卡片

展示工具的适用场景/人群。用 `slide dark`。

```html
<section class="slide dark">
  <div class="chrome-min">
    <span>适用场景</span>
    <span>08 / 08</span>
  </div>
  <div class="frame" style="padding-top:4vh">
    <div class="kicker" data-anim="d1">Use Cases</div>
    <h2 class="h-xl" data-anim="d2">谁在用?</h2>

    <div class="grid-4" style="margin-top:4vh">
      <div class="uc-card" data-anim="d2">
        <div class="uc-icon">📝</div>
        <div class="uc-title">写作者</div>
        <div class="uc-desc">写公众号文章需要配图?截图 + 标注,5 秒出图。</div>
      </div>
      <div class="uc-card" data-anim="d3">
        <div class="uc-icon">💻</div>
        <div class="uc-title">开发者</div>
        <div class="uc-desc">提 Issue 需要截图?一键截取 + 箭头标注,bug 描述更清晰。</div>
      </div>
      <div class="uc-card" data-anim="d4">
        <div class="uc-icon">🎨</div>
        <div class="uc-title">设计师</div>
        <div class="uc-desc">像素级取色,标注设计稿问题,比设计工具更快。</div>
      </div>
      <div class="uc-card" data-anim="d5">
        <div class="uc-icon">📊</div>
        <div class="uc-title">产品经理</div>
        <div class="uc-desc">写 PRD 需要界面截图?标注重点,一键粘贴到文档。</div>
      </div>
    </div>
  </div>
  <div class="footer-min">
    <span>Use Cases · 4 Personas</span>
    <span>—</span>
  </div>
</section>
```

---

## T09: 下载引导 CTA

下载链接/GitHub/二维码,强行动号召。用 `slide hero light` 收尾。

```html
<section class="slide hero light">
  <div class="chrome-min">
    <span>获取工具</span>
    <span>09 / 09</span>
  </div>
  <div class="frame center" style="gap:4vh">
    <div class="kicker" data-anim="d1">Get Started</div>
    <h2 class="h-xl" data-anim="d2">免费下载,即刻使用</h2>
    <p class="lead" style="text-align:center;max-width:45vw" data-anim="d3">
      绿色便携版,解压即用。Windows 10/11 通用,32MB 不到。
    </p>
    <div class="cta-group" style="justify-content:center" data-anim="d4">
      <a href="#" class="cta-btn primary" style="font-size:min(1.5vw,3vh);padding:1.8vh 3vw">
        <i data-lucide="download" style="width:1.3em;height:1.3em"></i> 下载 Windows 版
      </a>
      <a href="#" class="cta-btn secondary" style="font-size:min(1.3vw,2.6vh)">
        <i data-lucide="github" style="width:1.2em;height:1.2em"></i> 查看源码
      </a>
    </div>
    <div style="margin-top:3vh;opacity:.5;font-family:var(--mono);font-size:12px" data-anim="d5">
      v2.1.0 · 发布于 2026-06 · github.com/user/screencap
    </div>
  </div>
  <div class="footer-min">
    <span>Download · Free & Open Source</span>
    <span>MIT License</span>
  </div>
</section>
```

---

## T10: 功能详情(左文右图)

单个功能深入展示。用 `slide light` 或 `slide dark` 交替。

```html
<section class="slide light">
  <div class="chrome-min">
    <span>功能详解</span>
    <span>03 / 08</span>
  </div>
  <div class="frame grid-2-7-5" style="padding-top:4vh">
    <div style="display:flex;flex-direction:column;gap:3vh">
      <div>
        <div class="kicker" data-anim="d1">Highlight</div>
        <h2 class="h-xl" data-anim="d2">智能窗口识别</h2>
      </div>
      <p class="body-text" data-anim="d3">
        拖拽截图框时自动吸附窗口边界,识别精度达到像素级。
        支持多显示器环境,每个屏幕独立识别。
      </p>
      <ul class="body-sm" style="list-style:none;display:flex;flex-direction:column;gap:1.2vh" data-anim="d4">
        <li><span style="color:var(--accent);font-weight:700">✓</span> 自动吸附活动窗口</li>
        <li><span style="color:var(--accent);font-weight:700">✓</span> 识别子控件区域</li>
        <li><span style="color:var(--accent);font-weight:700">✓</span> 跨 DPI 精确映射</li>
        <li><span style="color:var(--accent);font-weight:700">✓</span> 按住 Alt 自由模式</li>
      </ul>
    </div>
    <div class="img-frame cover" style="aspect-ratio:16/10;max-height:50vh" data-anim="d5">
      <img src="images/10-window-detect.png" alt="窗口识别" style="height:100%">
    </div>
  </div>
  <div class="footer-min">
    <span>Feature Detail · Window Detection</span>
    <span>—</span>
  </div>
</section>
```

---

## T11: FAQ 常见问题

解答用户最常问的问题。用 `slide light`,手风琴式展开。

**所需 CSS 类**: `faq-item`, `faq-q`, `faq-a` (template.html 已定义)

```html
<section class="slide light">
  <div class="chrome-min">
    <span>常见问题</span>
    <span>07 / 10</span>
  </div>
  <div class="frame" style="padding-top:4vh">
    <div class="kicker" data-anim="d1">FAQ</div>
    <h2 class="h-xl" data-anim="d2">你可能想问</h2>

    <div style="margin-top:4vh;display:flex;flex-direction:column;gap:1.6vh;max-width:56vw">
      <div class="faq-item" data-anim="d2">
        <div class="faq-q">收费吗?</div>
        <div class="faq-a">完全免费,开源 MIT 协议。无需注册、无广告、无数据收集。</div>
      </div>
      <div class="faq-item" data-anim="d3">
        <div class="faq-q">支持 Mac/Linux 吗?</div>
        <div class="faq-a">目前仅支持 Windows 10/11。Mac 版在路线图中,预计 Q3 发布。</div>
      </div>
      <div class="faq-item" data-anim="d4">
        <div class="faq-q">截图会自动上传吗?</div>
        <div class="faq-a">不会。所有操作完全本地,截图保存在你指定的文件夹,从不联网。</div>
      </div>
      <div class="faq-item" data-anim="d5">
        <div class="faq-q">怎么反馈 bug?</div>
        <div class="faq-a">GitHub Issues 或通过工具内「帮助→反馈」直接提交,48 小时内回复。</div>
      </div>
    </div>
  </div>
  <div class="footer-min">
    <span>FAQ · Common Questions</span>
    <span>—</span>
  </div>
</section>
```

**要点**:
- 3-5 个最常见问题即可,不要放太多
- 问题简洁,答案 1-2 句
- faq-item hover 有轻微背景高亮

---

## T12: 价格方案卡片

展示付费方案/版本对比。用 `slide dark` 突出卡片。

**所需 CSS 类**: `pricing-card`, `pricing-card.featured`, `price-amount`, `price-period`, `price-features` (template.html 已定义)

```html
<section class="slide dark">
  <div class="chrome-min">
    <span>方案选择</span>
    <span>08 / 10</span>
  </div>
  <div class="frame" style="padding-top:3vh">
    <div class="kicker" data-anim="d1">Pricing</div>
    <h2 class="h-xl" data-anim="d2">选择你的方案</h2>

    <div class="grid-3" style="margin-top:4vh;align-items:stretch">
      <div class="pricing-card" data-anim="d2">
        <div class="price-plan">Free</div>
        <div class="price-amount">¥0</div>
        <div class="price-period">永久免费</div>
        <ul class="price-features">
          <li>基础截图功能</li>
          <li>5 种标注工具</li>
          <li>PNG 导出</li>
          <li>社区支持</li>
        </ul>
        <a href="#" class="cta-btn secondary" style="width:100%;justify-content:center;margin-top:auto">免费下载</a>
      </div>
      <div class="pricing-card featured" data-anim="d3">
        <div class="price-plan">Pro</div>
        <div class="price-amount">¥29<span style="font-size:.35em;font-weight:400;opacity:.7">/月</span></div>
        <div class="price-period">年付 ¥19/月</div>
        <ul class="price-features">
          <li>全部 Free 功能</li>
          <li>20+ 标注工具</li>
          <li>WebP/GIF 导出</li>
          <li>批量处理</li>
          <li>优先技术支持</li>
        </ul>
        <a href="#" class="cta-btn primary" style="width:100%;justify-content:center;margin-top:auto">开始试用</a>
      </div>
      <div class="pricing-card" data-anim="d4">
        <div class="price-plan">Team</div>
        <div class="price-amount">¥99<span style="font-size:.35em;font-weight:400;opacity:.7">/月</span></div>
        <div class="price-period">5 人起 · 年付 ¥79/月</div>
        <ul class="price-features">
          <li>全部 Pro 功能</li>
          <li>团队共享标注库</li>
          <li>SSO 登录</li>
          <li>管理后台</li>
          <li>专属客服</li>
        </ul>
        <a href="#" class="cta-btn secondary" style="width:100%;justify-content:center;margin-top:auto">联系销售</a>
      </div>
    </div>
  </div>
  <div class="footer-min">
    <span>Pricing · All plans include 14-day free trial</span>
    <span>—</span>
  </div>
</section>
```

**要点**:
- 推荐方案用 `.pricing-card.featured` 突出(放大 + 彩色边框)
- 3 个方案用 `.grid-3`,2 个用 `.grid-2`
- 免费版也放出来,不要只展示付费方案

---

## T13: 版本时间线

展示发展历程/重要版本。用 `slide light`。

**所需 CSS 类**: `timeline`, `tl-item`, `tl-dot`, `tl-content`, `tl-date`, `tl-title` (template.html 已定义)

```html
<section class="slide light">
  <div class="chrome-min">
    <span>版本历史</span>
    <span>06 / 10</span>
  </div>
  <div class="frame" style="padding-top:4vh">
    <div class="kicker" data-anim="d1">Changelog</div>
    <h2 class="h-xl" data-anim="d2">一路走来</h2>

    <div class="timeline" style="margin-top:4vh">
      <div class="tl-item" data-anim="d2">
        <div class="tl-dot"></div>
        <div class="tl-content">
          <div class="tl-date">2026.06 · v2.1</div>
          <div class="tl-title">批量处理 & GIF 导出</div>
          <p class="body-sm">支持批量截图标注,新增 GIF 录制导出,内存优化至 12MB。</p>
        </div>
      </div>
      <div class="tl-item" data-anim="d3">
        <div class="tl-dot"></div>
        <div class="tl-content">
          <div class="tl-date">2026.03 · v2.0</div>
          <div class="tl-title">全新界面 & 窗口识别</div>
          <p class="body-sm">PyQt5 重写 UI,智能窗口识别上线,标注工具增至 12 种。</p>
        </div>
      </div>
      <div class="tl-item" data-anim="d4">
        <div class="tl-dot"></div>
        <div class="tl-content">
          <div class="tl-date">2025.11 · v1.0</div>
          <div class="tl-title">首个公开版本</div>
          <p class="body-sm">基础截图 + 标注功能,单文件 Nuitka 编译,开源发布 GitHub。</p>
        </div>
      </div>
    </div>
  </div>
  <div class="footer-min">
    <span>Timeline · Since 2025</span>
    <span>—</span>
  </div>
</section>
```

**要点**:
- 3-5 个关键版本节点即可
- tl-dot 自动连线(左侧竖线),最新版在最上
- 未来版本可以加半透明虚线表示"规划中"

---

## T14: 用户口碑

用户评价/推荐语。用 `slide hero light` 烘托信任感。

**所需 CSS 类**: `tst-card`, `tst-quote`, `tst-author`, `tst-role` (template.html 已定义)

```html
<section class="slide hero light">
  <div class="chrome-min">
    <span>用户评价</span>
    <span>09 / 10</span>
  </div>
  <div class="frame" style="padding-top:3vh">
    <div class="kicker" data-anim="d1">Testimonials</div>
    <h2 class="h-xl" data-anim="d2">用过的都说好</h2>

    <div class="grid-3" style="margin-top:4vh;align-items:stretch">
      <div class="tst-card" data-anim="d2">
        <div class="tst-quote">"写公众号终于不用在截图和画图之间来回切了。一键搞定,效率提升了不止一倍。"</div>
        <div class="tst-author">
          <div class="tst-name">David Chen</div>
          <div class="tst-role">科技博主 · 5 万关注</div>
        </div>
      </div>
      <div class="tst-card" data-anim="d3">
        <div class="tst-quote">"提 Issue 时截图 + 标注一气呵成,比系统自带好用太多。开源 + 绿色版,完美。"</div>
        <div class="tst-author">
          <div class="tst-name">Xiao Wang</div>
          <div class="tst-role">全栈开发者 · GitHub 1.2k stars</div>
        </div>
      </div>
      <div class="tst-card" data-anim="d4">
        <div class="tst-quote">"像素级标注和取色功能太实用了,设计评审时直接在截图上圈问题,省去大量沟通成本。"</div>
        <div class="tst-author">
          <div class="tst-name">Lisa Zhou</div>
          <div class="tst-role">UI 设计师 · Figma 社区贡献者</div>
        </div>
      </div>
    </div>
  </div>
  <div class="footer-min">
    <span>Testimonials · Real users, real feedback</span>
    <span>—</span>
  </div>
</section>
```

**要点**:
- 3-4 个真实(或看起来真实)的用户评价
- 不同角色/场景各一人,展现覆盖面
- 评价控制在 2-3 句话,不要长篇
- 如果工具还没用户,用"典型场景"口吻写

---

## T15: 安装指南

零基础安装步骤,配代码块。用 `slide dark`。

**所需 CSS 类**: `install-step`, `install-num`, `install-code`, `install-note` (template.html 已定义)

```html
<section class="slide dark">
  <div class="chrome-min">
    <span>安装指南</span>
    <span>05 / 10</span>
  </div>
  <div class="frame" style="padding-top:4vh">
    <div class="kicker" data-anim="d1">Installation</div>
    <h2 class="h-xl" data-anim="d2">三步安装</h2>

    <div style="margin-top:4vh;display:flex;flex-direction:column;gap:2.5vh;max-width:56vw">
      <div class="install-step" data-anim="d2">
        <div class="install-num">01</div>
        <div class="install-body">
          <div class="install-title">下载压缩包</div>
          <p class="body-sm">从 GitHub Releases 下载最新版 zip,解压到任意目录。</p>
          <div class="install-code">screencap-v2.1.0-win64.zip  (8.6 MB)</div>
          <div class="install-note">SHA256: a1b2c3d4... — 请核对校验码</div>
        </div>
      </div>
      <div class="install-step" data-anim="d3">
        <div class="install-num">02</div>
        <div class="install-body">
          <div class="install-title">运行程序</div>
          <p class="body-sm">双击 ScreenCap.exe,系统托盘出现图标即启动成功。</p>
          <div class="install-code"># 或从命令行启动(查看日志)
screencap.exe --debug</div>
          <div class="install-note">首次运行 Windows 可能弹出 SmartScreen 警告,点击"更多信息→仍要运行"即可</div>
        </div>
      </div>
      <div class="install-step" data-anim="d4">
        <div class="install-num">03</div>
        <div class="install-body">
          <div class="install-title">设置自启动(可选)</div>
          <p class="body-sm">右键系统托盘图标 → 设置 → 勾选「开机自启」。</p>
          <div class="install-note">推荐开启,以便随时用 Ctrl+Shift+S 截图</div>
        </div>
      </div>
    </div>
  </div>
  <div class="footer-min">
    <span>Installation · Windows 10/11 · 3 steps</span>
    <span>—</span>
  </div>
</section>
```

**要点**:
- 2-4 步,每步有命令行/代码块
- `.install-code` 用 monospace 字体,模拟终端
- `.install-note` 放注意事项(浅色小字)

---

## T16: 功能对比矩阵

与同类工具横向对比。用 `slide light`。

**所需 CSS 类**: `matrix-table`, `matrix-head`, `matrix-row`, `matrix-check`, `matrix-cross`, `matrix-partial` (template.html 已定义)

```html
<section class="slide light">
  <div class="chrome-min">
    <span>横向对比</span>
    <span>07 / 10</span>
  </div>
  <div class="frame" style="padding-top:4vh">
    <div class="kicker" data-anim="d1">Comparison</div>
    <h2 class="h-xl" data-anim="d2">为什么选我们?</h2>

    <div style="margin-top:4vh;overflow-x:auto">
      <table class="matrix-table" data-anim="d2">
        <thead>
          <tr>
            <th class="matrix-head">能力</th>
            <th class="matrix-head highlight">ScreenCap</th>
            <th class="matrix-head">系统截图</th>
            <th class="matrix-head">Snipaste</th>
          </tr>
        </thead>
        <tbody>
          <tr class="matrix-row">
            <td>窗口识别</td>
            <td class="highlight"><span class="matrix-check"><i data-lucide="check" style="width:1em;height:1em"></i></span> 智能吸附</td>
            <td><span class="matrix-cross"><i data-lucide="x" style="width:1em;height:1em"></i></span></td>
            <td><span class="matrix-partial"><i data-lucide="minus" style="width:1em;height:1em"></i></span> 手动</td>
          </tr>
          <tr class="matrix-row">
            <td>标注工具</td>
            <td class="highlight"><span class="matrix-check"><i data-lucide="check" style="width:1em;height:1em"></i></span> 15 种</td>
            <td><span class="matrix-cross"><i data-lucide="x" style="width:1em;height:1em"></i></span></td>
            <td><span class="matrix-check"><i data-lucide="check" style="width:1em;height:1em"></i></span> 8 种</td>
          </tr>
          <tr class="matrix-row">
            <td>屏幕取色</td>
            <td class="highlight"><span class="matrix-check"><i data-lucide="check" style="width:1em;height:1em"></i></span> 4 种格式</td>
            <td><span class="matrix-cross"><i data-lucide="x" style="width:1em;height:1em"></i></span></td>
            <td><span class="matrix-check"><i data-lucide="check" style="width:1em;height:1em"></i></span> HEX 仅</td>
          </tr>
          <tr class="matrix-row">
            <td>体积</td>
            <td class="highlight"><span class="matrix-check"><i data-lucide="check" style="width:1em;height:1em"></i></span> 8.6 MB</td>
            <td><span class="matrix-check"><i data-lucide="check" style="width:1em;height:1em"></i></span> 系统内置</td>
            <td><span class="matrix-partial"><i data-lucide="minus" style="width:1em;height:1em"></i></span> 21 MB</td>
          </tr>
          <tr class="matrix-row">
            <td>开源</td>
            <td class="highlight"><span class="matrix-check"><i data-lucide="check" style="width:1em;height:1em"></i></span> MIT</td>
            <td><span class="matrix-cross"><i data-lucide="x" style="width:1em;height:1em"></i></span></td>
            <td><span class="matrix-cross"><i data-lucide="x" style="width:1em;height:1em"></i></span></td>
          </tr>
        </tbody>
      </table>
    </div>
    <p class="body-sm" style="margin-top:2vh;opacity:.5" data-anim="d4">
      测试环境: Windows 11 · i5-13500H · 16GB RAM。数据截至 2026.06。
    </p>
  </div>
  <div class="footer-min">
    <span>Feature Matrix · ScreenCap vs Alternatives</span>
    <span>—</span>
  </div>
</section>
```

**要点**:
- 第一列是自家工具,用 `.highlight` 突出
- 对比 2-3 个同类工具即可
- 5-8 个对比维度,每个用 ✓ / ✗ / — 三元表示
- 底部注明测试环境,确保数据真实

---

## T17: 数据仪表盘

关键指标 + 进度条,适合展示工具的性能维度。用 `slide dark` + `bg-particles`。

**所需 CSS 类**: `stat-card`, `progress-bar`, `progress-fill`, `progress-label` (template.html 已定义)

```html
<section class="slide dark bg-particles">
  <div class="chrome-min">
    <span>性能仪表盘</span>
    <span>05 / 12</span>
  </div>
  <div class="frame" style="padding-top:4vh">
    <div class="kicker" data-anim="d1">Dashboard</div>
    <h2 class="h-xl" data-anim="d2">核心指标一览</h2>

    <div class="grid-2" style="margin-top:4vh;gap:3vh 4vw">
      <div class="col" style="gap:3vh" data-anim="d3">
        <div class="stat-card">
          <div class="stat-label">剪贴板容量</div>
          <div class="stat-value">1000<span class="unit">条</span></div>
          <div class="stat-note">智能去重后实际存储,可搜索全文</div>
        </div>
        <div class="progress-label"><span>内存效率</span><span class="prog-val">92%</span></div>
        <div class="progress-bar" style="--p:92%"><div class="progress-fill"></div></div>
      </div>
      <div class="col" style="gap:3vh" data-anim="d4">
        <div class="stat-card">
          <div class="stat-label">响应时间</div>
          <div class="stat-value">&lt;50<span class="unit">ms</span></div>
          <div class="stat-note">从热键按下到界面出现,无感知延迟</div>
        </div>
        <div class="progress-label"><span>CPU 占用</span><span class="prog-val">3%</span></div>
        <div class="progress-bar" style="--p:3%"><div class="progress-fill"></div></div>
      </div>
    </div>
  </div>
  <div class="footer-min"><span>Dashboard · Real-time Metrics</span><span>—</span></div>
</section>
```

**要点**:
- 2-4 个指标 + 2-4 条进度条,左右分栏
- `--p` 是进度百分比,需要在 `.progress-bar` 上设置
- 进度条在页面切换时自动动画到目标值

---

## T18: 功能筛选栏

标签式筛选 + 功能卡片联动,适合功能多的工具。用 `slide light`。

**所需 CSS 类**: `tag-bar`, `tag-item`, `feat-card` (template.html 已定义)

```html
<section class="slide light">
  <div class="chrome-min">
    <span>全部功能</span>
    <span>04 / 12</span>
  </div>
  <div class="frame" style="padding-top:3vh">
    <div class="kicker" data-anim="d1">All Features</div>
    <h2 class="h-lg" data-anim="d2">20+ 能力等你发现</h2>

    <div class="tag-bar" style="margin-top:2.5vh" data-anim="d3">
      <span class="tag-item active">全部</span>
      <span class="tag-item">采集</span>
      <span class="tag-item">管理</span>
      <span class="tag-item">分享</span>
      <span class="tag-item">自动化</span>
    </div>

    <div class="grid-6" style="margin-top:3vh">
      <div class="feat-card" data-anim="d2">
        <div class="feat-icon"><i data-lucide="copy"></i></div>
        <div class="feat-title">智能去重</div>
        <div class="feat-desc">相同内容自动合并,节省空间</div>
      </div>
      <div class="feat-card" data-anim="d3">
        <div class="feat-icon"><i data-lucide="search"></i></div>
        <div class="feat-title">全文搜索</div>
        <div class="feat-desc">毫秒级检索全部剪贴历史</div>
      </div>
      <div class="feat-card feat-card accent" data-anim="d4">
        <div class="feat-icon"><i data-lucide="star"></i></div>
        <div class="feat-title">收藏片段</div>
        <div class="feat-desc">常用内容一键置顶</div>
      </div>
    </div>
  </div>
  <div class="footer-min"><span>Features · Tag & Filter</span><span>—</span></div>
</section>
```

**要点**:
- `.tag-item.active` 标出当前选中项
- 筛选栏和卡片是视觉关联,无实际交互逻辑(纯演示)
- 卡片数可 3/4/6,用对应 grid

---

## T19: 大引用页

一句有分量的推荐语或核心理念。用 `slide hero light` + blobs。

**所需 CSS 类**: `quote-block`, `quote-text`, `quote-author` (template.html 已定义)

```html
<section class="slide hero light">
  <div class="chrome-min"><span>用户说</span><span>08 / 12</span></div>
  <div class="blob a"></div>
  <div class="blob b"></div>
  <div class="frame center">
    <div class="quote-block" data-anim="d1">
      <div class="quote-text">"用了 ClipFlow 之后,我再也没打开过记事本记临时内容。它就像我的第二大脑。"</div>
      <div class="quote-author">— David, 全栈开发者 · 3 年用户</div>
    </div>
  </div>
  <div class="footer-min"><span>Testimonial · Real User</span><span>—</span></div>
</section>
```

**要点**:
- 只放一条最有分量的引用
- 配合 blobs 做温暖的视觉氛围
- quote 控制在 30 字以内

---

## T20: 能力雷达

多条进度条展示工具在不同维度的表现。用 `slide dark` + `bg-stripes`。

**所需 CSS 类**: `progress-bar`, `progress-fill`, `progress-label` (template.html 已定义)

```html
<section class="slide dark bg-stripes">
  <div class="chrome-min"><span>能力评估</span><span>07 / 12</span></div>
  <div class="frame" style="padding-top:4vh">
    <div class="kicker" data-anim="d1">Capability Radar</div>
    <h2 class="h-xl" data-anim="d2">全方位能力覆盖</h2>

    <div class="col" style="margin-top:4vh;gap:2.5vh;max-width:52vw" data-anim="d3">
      <div>
        <div class="progress-label"><span>数据采集速度</span><span class="prog-val">98%</span></div>
        <div class="progress-bar" style="--p:98%"><div class="progress-fill"></div></div>
      </div>
      <div>
        <div class="progress-label"><span>智能识别准确率</span><span class="prog-val">95%</span></div>
        <div class="progress-bar" style="--p:95%"><div class="progress-fill"></div></div>
      </div>
      <div>
        <div class="progress-label"><span>跨平台兼容性</span><span class="prog-val">80%</span></div>
        <div class="progress-bar" style="--p:80%"><div class="progress-fill"></div></div>
      </div>
      <div>
        <div class="progress-label"><span>社区生态活跃度</span><span class="prog-val">72%</span></div>
        <div class="progress-bar" style="--p:72%"><div class="progress-fill"></div></div>
      </div>
      <div>
        <div class="progress-label"><span>文档完善度</span><span class="prog-val">88%</span></div>
        <div class="progress-bar" style="--p:88%"><div class="progress-fill"></div></div>
      </div>
    </div>
    <p class="body-sm" style="margin-top:2vh;opacity:.4" data-anim="d4">评分基于内部基准测试与用户反馈综合评估</p>
  </div>
  <div class="footer-min"><span>Capability · 5 Dimensions</span><span>—</span></div>
</section>
```

**要点**:
- 5-7 个维度为宜
- 数据要有依据,注明评估方法
- 配合 `bg-stripes` 增强科技感

---

## T21: 架构总览

展示工具的架构/工作流示意图。用 `slide light` + `bg-geo`。

```html
<section class="slide light bg-geo">
  <div class="chrome-min"><span>技术架构</span><span>06 / 12</span></div>
  <div class="frame" style="padding-top:4vh">
    <div class="kicker" data-anim="d1">Architecture</div>
    <h2 class="h-xl" data-anim="d2">系统架构一览</h2>

    <div style="margin-top:4vh;display:flex;align-items:center;gap:2vw;justify-content:center;flex-wrap:wrap" data-anim="d3">
      <div class="feat-card" style="width:14vw;min-width:140px;text-align:center;align-items:center">
        <div class="feat-icon"><i data-lucide="monitor"></i></div>
        <div class="feat-title">GUI 前端</div>
        <div class="feat-desc">PyQt5 · 系统托盘</div>
      </div>
      <div style="font-family:var(--mono);font-size:1.5vw;opacity:.25">→</div>
      <div class="feat-card" style="width:14vw;min-width:140px;text-align:center;align-items:center">
        <div class="feat-icon"><i data-lucide="cpu"></i></div>
        <div class="feat-title">核心引擎</div>
        <div class="feat-desc">Rust · 异步处理</div>
      </div>
      <div style="font-family:var(--mono);font-size:1.5vw;opacity:.25">→</div>
      <div class="feat-card" style="width:14vw;min-width:140px;text-align:center;align-items:center">
        <div class="feat-icon"><i data-lucide="database"></i></div>
        <div class="feat-title">存储层</div>
        <div class="feat-desc">SQLite · 本地加密</div>
      </div>
    </div>
    <p class="body-sm" style="text-align:center;margin-top:2vh;opacity:.45" data-anim="d4">▲ 三层分离架构,各模块独立编译</p>
  </div>
  <div class="footer-min"><span>Architecture · 3-Layer Design</span><span>—</span></div>
</section>
```

**要点**:
- 用卡片表示模块,箭头表示数据流
- 3-5 个模块为宜,横向排列
- 底部加一行小字说明

---

## T22: 生态集成

展示工具与第三方服务的集成。用 `slide dark` + `bg-hex`。

**所需 CSS 类**: `icon-row`, `icon-cell` (template.html 已定义)

```html
<section class="slide dark bg-hex">
  <div class="chrome-min"><span>生态集成</span><span>10 / 12</span></div>
  <div class="frame" style="padding-top:4vh">
    <div class="kicker" data-anim="d1">Ecosystem</div>
    <h2 class="h-xl" data-anim="d2">无缝连接你的工作流</h2>

    <div class="icon-row" style="margin-top:5vh" data-anim="d3">
      <div class="icon-cell">
        <div class="ic-icon"><i data-lucide="github"></i></div>
        <div class="ic-name">GitHub</div>
        <div class="ic-sub">Issue/Markdown</div>
      </div>
      <div class="icon-cell">
        <div class="ic-icon"><i data-lucide="file-text"></i></div>
        <div class="ic-name">Notion</div>
        <div class="ic-sub">API 同步</div>
      </div>
      <div class="icon-cell">
        <div class="ic-icon"><i data-lucide="slack"></i></div>
        <div class="ic-name">Slack</div>
        <div class="ic-sub">消息推送</div>
      </div>
      <div class="icon-cell">
        <div class="ic-icon"><i data-lucide="cloud"></i></div>
        <div class="ic-name">iCloud</div>
        <div class="ic-sub">多端同步</div>
      </div>
      <div class="icon-cell">
        <div class="ic-icon"><i data-lucide="terminal"></i></div>
        <div class="ic-name">VS Code</div>
        <div class="ic-sub">插件支持</div>
      </div>
    </div>
    <p class="body-sm" style="text-align:center;margin-top:4vh;opacity:.45" data-anim="d4">更多集成开发中 · 欢迎提交 PR</p>
  </div>
  <div class="footer-min"><span>Ecosystem · 5+ Integrations</span><span>—</span></div>
</section>
```

**要点**:
- 4-6 个集成为佳,用 `.icon-row` 居中排列
- Lucide 图标需对应真实服务名
- 配合 `bg-hex` 六边形背景增强专业感

---

## T23: 动图/GIF 展示

嵌入动图或视频展示操作效果。用 `slide light`。

```html
<section class="slide light">
  <div class="chrome-min"><span>操作演示</span><span>05 / 12</span></div>
  <div class="frame center" style="padding-top:2vh;gap:2vh">
    <div class="kicker" data-anim="d1">Demo</div>
    <h2 class="h-lg" data-anim="d2">看一遍,胜过读十遍</h2>
    <div class="screenshot-wrap" style="max-width:60vw;aspect-ratio:16/10" data-anim="d3">
      <div class="img-slot" style="aspect-ratio:16/10;border-color:var(--accent);opacity:.3">GIF DEMO HERE</div>
    </div>
    <p class="screenshot-cap" data-anim="d4">▲ 一键截图 → 智能标注 → 自动复制,全程不到 3 秒</p>
  </div>
  <div class="footer-min"><span>Demo · 3 Seconds Workflow</span><span>—</span></div>
</section>
```

**要点**:
- 替换 `.img-slot` 为 `<img>` 或 `<video>` 标签
- 动图控制在 15 秒以内
- `.screenshot-cap` 放操作说明

---

## T24: 多入口 CTA

下载/GitHub/文档/社区,多个行动入口。用 `slide hero dark` + `bg-glow`。

**所需 CSS 类**: `alert-box`, `cta-btn`, `cta-group`, `icon-cell` (template.html 已定义)

```html
<section class="slide hero dark bg-glow">
  <div class="chrome-min"><span>开始使用</span><span>12 / 12</span></div>
  <div class="frame center" style="gap:4vh">
    <div class="kicker" data-anim="d1">Get Started Today</div>
    <h2 class="h-xl" data-anim="d2">选择你的起点</h2>

    <div class="icon-row" style="margin-top:1vh" data-anim="d3">
      <div class="icon-cell" style="cursor:default">
        <div class="ic-icon" style="width:4vw;height:4vw;min-width:40px;min-height:40px"><i data-lucide="download"></i></div>
        <div class="ic-name" style="font-size:max(14px,1vw)">下载</div>
        <div class="ic-sub">Windows 10+</div>
      </div>
      <div class="icon-cell" style="cursor:default">
        <div class="ic-icon" style="width:4vw;height:4vw;min-width:40px;min-height:40px"><i data-lucide="github"></i></div>
        <div class="ic-name" style="font-size:max(14px,1vw)">GitHub</div>
        <div class="ic-sub">MIT 开源</div>
      </div>
      <div class="icon-cell" style="cursor:default">
        <div class="ic-icon" style="width:4vw;height:4vw;min-width:40px;min-height:40px"><i data-lucide="book-open"></i></div>
        <div class="ic-name" style="font-size:max(14px,1vw)">文档</div>
        <div class="ic-sub">快速上手</div>
      </div>
      <div class="icon-cell" style="cursor:default">
        <div class="ic-icon" style="width:4vw;height:4vw;min-width:40px;min-height:40px"><i data-lucide="message-circle"></i></div>
        <div class="ic-name" style="font-size:max(14px,1vw)">社区</div>
        <div class="ic-sub">Discord</div>
      </div>
    </div>

    <div class="alert-box info" style="max-width:40vw" data-anim="d4">
      无需注册,无需付费,解压即用。我们相信好工具应该触手可及。
    </div>
    <div class="cta-group" style="justify-content:center" data-anim="d5">
      <a href="#" class="cta-btn primary" style="font-size:min(1.5vw,3vh);padding:1.8vh 3vw">
        <i data-lucide="download" style="width:1.3em;height:1.3em"></i> 下载 v2.1.0
      </a>
    </div>
  </div>
  <div class="footer-min"><span>Ready · One Click Away</span><span>Free Forever</span></div>
</section>
```

**要点**:
- 4 个入口图标 + 1 个主 CTA 按钮
- 用 `.alert-box.info` 放一句暖心话
- 配合 `bg-glow` 打造高端氛围

---

## 背景选择指南

> AI 在 SKILL.md Step 1 中根据**页面目标+情绪基调+明暗+主题**自主选择背景，以下为按氛围查询的速查表。

| 页面目标 | 可用背景池 | 最佳明暗 |
|---------|-----------|---------|
| 🔥 视觉冲击（Hero/CTA/过渡） | blobs, bg-glow, bg-meteor, bg-stars, bg-hex, bg-diagonal, bg-stripeflow | dark |
| 📋 信息展示（功能/规格/FAQ） | bg-geo, bg-dots, bg-grid, bg-noise, bg-ripple | light + dark |
| 📊 数据强调（大字报/仪表盘） | bg-particles, bg-stripes, bg-grid, bg-circuit, bg-waveline | dark |
| ⚖️ 对比矩阵（竞品对比） | bg-circuit, bg-grid, bg-stripes | light + dark |
| 🧭 流程引导（步骤/安装/二维码） | bg-geo, bg-wave, 留白 | light |
| 🤝 人文社交（口碑/团队/案例） | bg-wave, bg-geo, blobs | light |

**氛围维度速查**：

| 页面氛围 | 推荐的背景类 | 适用主题 |
|---------|------------|---------|
| 科技/数据感 | bg-circuit, bg-particles, bg-grid, bg-stripes, bg-waveline | 科技蓝、极客紫、暗夜黑 |
| 优雅/专业感 | bg-geo, bg-hex, bg-dots, bg-ripple | 海洋青、午夜金、森琥珀 |
| 温暖/人文感 | blobs, bg-wave, bg-glow | 日落橙、玫瑰粉、效率绿 |
| 质感/沉稳感 | bg-noise, blobs, bg-stars | 暗夜黑、午夜金 |
| 纯净/留白感 | 只用 hero + blobs，不带背景类 | 所有主题 |
| 炫酷/视觉冲击 | bg-meteor, bg-glow, bg-hex, bg-diagonal, bg-stripeflow | 极客紫、暗夜黑、科技蓝 |

---

## 动画参考

本模板使用**纯 CSS transition**做入场动画,无需 Motion One:

- 每个需动效的元素加 `data-anim="d1"` ~ `data-anim="d6"`,数字越大延迟越长
- 页面切换时自动给当前 `.slide` 加 `.active` 类,触发 CSS transition
- 不加 `data-anim` 的元素始终可见(如 chrome-min, footer-min)
- `data-anim-x` 为左侧滑入,`data-anim-pop` 为缩放弹入

## 图标参考

使用 Lucide 图标,CDN 已引入。常用图标名:

| 用途 | 图标名 |
|------|--------|
| 下载 | `download` |
| GitHub | `github` |
| 截图 | `camera` |
| 窗口 | `scan-eye` / `monitor` |
| 标注 | `pencil` |
| 取色 | `pipette` |
| 速度 | `zap` |
| 剪贴板 | `copy` / `clipboard` |
| 对比 | `arrow-left-right` |
| 设置 | `settings` |
| 勾选 | `check-circle` |
| 搜索 | `search` |
| 帮助 | `help-circle` |
| 价格 | `tag` / `dollar-sign` |
| 时间 | `clock` / `calendar` |
| 用户 | `user` / `users` |
| 代码 | `code` / `terminal` |
| 星标 | `star` |
| 对勾 | `check` |
| 叉号 | `x` |
| 减号 | `minus` |

---

## T25: 代码展示

嵌代码块展示工具核心逻辑或配置。用 `slide dark`。

**所需 CSS 类**: `code-showcase`, `code-header`, `code-dot`, `code-lang`, `code-body`, `code-keyword`, `code-func`, `code-str`, `code-comment`, `code-num` (template.html 已定义)

```html
<section class="slide dark">
  <div class="chrome-min">
    <span>核心代码</span>
    <span>05 / 12</span>
  </div>
  <div class="frame" style="padding-top:3vh;align-items:center">
    <div class="kicker" data-anim="d1">Code Preview</div>
    <h2 class="h-xl" data-anim="d2">三行代码搞定</h2>

    <div class="code-showcase" data-anim="d3">
      <div class="code-header">
        <span class="code-dot r"></span>
        <span class="code-dot y"></span>
        <span class="code-dot g"></span>
        <span class="code-lang">screencap.py · Python 3.11</span>
      </div>
      <div class="code-body">
        <span class="code-keyword">from</span> screencap <span class="code-keyword">import</span> capture<br>
        <br>
        <span class="code-comment"># 一键截图 + 智能标注</span><br>
        img = <span class="code-func">capture</span>(region=<span class="code-str">"auto"</span>)<br>
        img.<span class="code-func">annotate</span>(arrows=<span class="code-num">True</span>, copy=<span class="code-num">True</span>)<br>
      </div>
    </div>
    <p class="body-sm" style="margin-top:2vh;opacity:.5" data-anim="d4">
      核心逻辑不到 10 行，基于 PyQt5 + PIL 实现
    </p>
  </div>
  <div class="footer-min">
    <span>Code · Minimal API</span>
    <span>—</span>
  </div>
</section>
```

**要点**:
- 代码高亮用 inline span（`.code-keyword` 紫色、`.code-func` 蓝色、`.code-str` 绿色、`.code-comment` 灰色、`.code-num` 橙色）
- 3-8 行代码为宜，不要贴整文件
- `.code-showcase` 自带 macOS 三色点装饰

---

## T26: 数据卡片墙

多指标数据一览，适合展示工具的多维度表现。用 `slide light` 或 `slide dark`。

**所需 CSS 类**: `metric-grid`, `metric-card`, `metric-icon`, `metric-value`, `metric-label`, `metric-change` (template.html 已定义)

```html
<section class="slide light">
  <div class="chrome-min">
    <span>核心指标</span>
    <span>05 / 12</span>
  </div>
  <div class="frame" style="padding-top:3vh">
    <div class="kicker" data-anim="d1">Metrics</div>
    <h2 class="h-xl" data-anim="d2">全方位数据一览</h2>

    <div class="metric-grid" style="margin-top:4vh">
      <div class="metric-card" data-anim="d2">
        <div class="metric-icon"><i data-lucide="zap"></i></div>
        <div class="metric-value">&lt;0.2<span style="font-size:.35em;font-weight:400;opacity:.6">s</span></div>
        <div class="metric-label">启动速度</div>
        <div class="metric-change up">↑ 比上代快 3x</div>
      </div>
      <div class="metric-card" data-anim="d3">
        <div class="metric-icon"><i data-lucide="hard-drive"></i></div>
        <div class="metric-value">8.6<span style="font-size:.35em;font-weight:400;opacity:.6">MB</span></div>
        <div class="metric-label">安装体积</div>
        <div class="metric-change down">↓ 比 v1.0 小 40%</div>
      </div>
      <div class="metric-card" data-anim="d4">
        <div class="metric-icon"><i data-lucide="cpu"></i></div>
        <div class="metric-value">&lt;30<span style="font-size:.35em;font-weight:400;opacity:.6">MB</span></div>
        <div class="metric-label">内存占用</div>
        <div class="metric-change up">↑ 空闲仅 12MB</div>
      </div>
      <div class="metric-card" data-anim="d5">
        <div class="metric-icon"><i data-lucide="download"></i></div>
        <div class="metric-value">12<span style="font-size:.35em;font-weight:400;opacity:.6">k+</span></div>
        <div class="metric-label">累计下载</div>
        <div class="metric-change up">↑ 月增 2k+</div>
      </div>
    </div>
  </div>
  <div class="footer-min">
    <span>Metrics · Real Data · Jun 2026</span>
    <span>—</span>
  </div>
</section>
```

**要点**:
- 4 个指标用 `.metric-grid`（4 列），2-3 个用 `.grid-2` 或 `.grid-3` 配合 `.stat-card`
- `.metric-change.up` 绿色，`.metric-change.down` 红色
- hover 有上浮 + 边框发光效果

---

## T27: 用户案例卡片

展示真实用户的使用场景和成果。用 `slide light`。

**所需 CSS 类**: `case-card`, `case-img`, `case-body`, `case-title`, `case-desc`, `case-result`, `case-tag` (template.html 已定义)

```html
<section class="slide light">
  <div class="chrome-min">
    <span>用户案例</span>
    <span>08 / 12</span>
  </div>
  <div class="frame" style="padding-top:3vh">
    <div class="kicker" data-anim="d1">Case Studies</div>
    <h2 class="h-xl" data-anim="d2">他们用上了</h2>

    <div class="grid-3" style="margin-top:4vh">
      <div class="case-card" data-anim="d2">
        <div class="case-img"><img src="images/case1.png" alt="案例1"></div>
        <div class="case-body">
          <span class="case-tag">公众号运营</span>
          <div class="case-title">截图效率提升 5x</div>
          <div class="case-desc">原来写一篇推文需要 15 次截图+标注，现在 3 次搞定，全程快捷键。</div>
          <div class="case-result">▲ 节省 60% 配图时间</div>
        </div>
      </div>
      <div class="case-card" data-anim="d3">
        <div class="case-img"><img src="images/case2.png" alt="案例2"></div>
        <div class="case-body">
          <span class="case-tag">开发团队</span>
          <div class="case-title">Bug 描述更清晰</div>
          <div class="case-desc">Issue 里附带的截图从模糊手机拍照变成精确标注，沟通成本直降。</div>
          <div class="case-result">▲ 往返沟通减少 70%</div>
        </div>
      </div>
      <div class="case-card" data-anim="d4">
        <div class="case-img"><img src="images/case3.png" alt="案例3"></div>
        <div class="case-body">
          <span class="case-tag">设计评审</span>
          <div class="case-title">标注精度达像素级</div>
          <div class="case-desc">在截图上直接圈出问题区域，比口头描述直观 10 倍。</div>
          <div class="case-result">▲ 评审效率提升 3x</div>
        </div>
      </div>
    </div>
  </div>
  <div class="footer-min">
    <span>Case Studies · Real Users</span>
    <span>—</span>
  </div>
</section>
```

---

## T28: 左右分屏对比

左右两栏展示两种状态/方案/模式。用 `slide dark`。

**所需 CSS 类**: `split-view`, `split-panel`, `split-divider-v`, `split-label`, `sp-title`, `sp-list` (template.html 已定义)

```html
<section class="slide dark">
  <div class="chrome-min">
    <span>模式对比</span>
    <span>06 / 12</span>
  </div>
  <div class="frame" style="padding-top:3vh">
    <div class="kicker" data-anim="d1">Comparison</div>
    <h2 class="h-xl" data-anim="d2">两种模式，随意切换</h2>

    <div class="split-view" style="margin-top:4vh" data-anim="d3">
      <div class="split-panel left">
        <div class="sp-title">🖥️ 截图模式</div>
        <ul class="sp-list">
          <li>框选区域截图</li>
          <li>智能窗口识别</li>
          <li>实时标注工具</li>
          <li>自动复制到剪贴板</li>
        </ul>
      </div>
      <div class="split-divider-v"><span class="split-label">VS</span></div>
      <div class="split-panel right">
        <div class="sp-title">🎬 录制模式</div>
        <ul class="sp-list">
          <li>全屏/区域 GIF 录制</li>
          <li>按键操作可视化</li>
          <li>生成永久回放链接</li>
          <li>AI 自动生成步骤文档</li>
        </ul>
      </div>
    </div>
  </div>
  <div class="footer-min">
    <span>Comparison · 2 Modes</span>
    <span>—</span>
  </div>
</section>
```

---

## T29: 更新动态流

版本更新日志的时间线展示。用 `slide light`。

**所需 CSS 类**: `feed-list`, `feed-item`, `feed-dot-wrap`, `feed-dot`, `feed-line`, `feed-body`, `feed-time`, `feed-title`, `feed-desc`, `feed-tag` (template.html 已定义)

```html
<section class="slide light">
  <div class="chrome-min">
    <span>更新动态</span>
    <span>07 / 12</span>
  </div>
  <div class="frame" style="padding-top:3vh">
    <div class="kicker" data-anim="d1">Changelog</div>
    <h2 class="h-xl" data-anim="d2">最近更新</h2>

    <div class="feed-list" style="margin-top:4vh">
      <div class="feed-item" data-anim="d2">
        <div class="feed-dot-wrap">
          <div class="feed-dot major"></div>
          <div class="feed-line"></div>
        </div>
        <div class="feed-body">
          <div class="feed-time">2026.06.15 · v2.1.0</div>
          <div class="feed-title">批量处理 & GIF 录制</div>
          <div class="feed-desc">支持批量截图标注，新增 GIF 录制导出，内存优化至 12MB。</div>
          <span class="feed-tag new">New</span>
        </div>
      </div>
      <div class="feed-item" data-anim="d3">
        <div class="feed-dot-wrap">
          <div class="feed-dot"></div>
          <div class="feed-line"></div>
        </div>
        <div class="feed-body">
          <div class="feed-time">2026.03.20 · v2.0.0</div>
          <div class="feed-title">全新界面 & 窗口识别</div>
          <div class="feed-desc">PyQt5 重写 UI，智能窗口识别上线，标注工具增至 12 种。</div>
          <span class="feed-tag improve">Improve</span>
        </div>
      </div>
      <div class="feed-item" data-anim="d4">
        <div class="feed-dot-wrap">
          <div class="feed-dot"></div>
        </div>
        <div class="feed-body">
          <div class="feed-time">2025.11.08 · v1.0.0</div>
          <div class="feed-title">首个公开版本</div>
          <div class="feed-desc">基础截图 + 标注功能，单文件 Nuitka 编译，开源发布 GitHub。</div>
          <span class="feed-tag new">New</span>
        </div>
      </div>
    </div>
  </div>
  <div class="footer-min">
    <span>Changelog · Since 2025</span>
    <span>—</span>
  </div>
</section>
```

---

## T30: 章节过渡页

大章节之间的过渡页，纯视觉冲击。用 `slide hero dark` 或 `slide hero light`。

**所需 CSS 类**: `chapter-wrap`, `chapter-num`, `chapter-title`, `chapter-sub`, `chapter-line` (template.html 已定义)

```html
<section class="slide hero dark">
  <div class="blob a"></div>
  <div class="blob b"></div>
  <div class="frame center">
    <div class="chapter-wrap" data-anim="d1">
      <div class="chapter-num">02</div>
      <div class="chapter-line"></div>
      <h2 class="chapter-title">深入内核</h2>
      <p class="chapter-sub">看看背后用了什么技术</p>
    </div>
  </div>
  <div class="footer-min">
    <span>Chapter 2 · Deep Dive</span>
    <span>—</span>
  </div>
</section>
```

**要点**:
- `chapter-num` 是大号章节号（半透明），`chapter-title` 是章节名
- 适合在长 PPT 里插入，帮助观众理清结构
- 配合 `hero dark` + blobs 使用效果最佳

---

## 背景选择指南

> 完整背景选池 + 氛围速查见上方同名章节。AI 选择逻辑见 SKILL.md Step 1「场景驱动」流程。

---

## 动画参考

本模板使用**纯 CSS transition** 做入场动画，无需 Motion One：

- 每个需动效的元素加 `data-anim="d1"` ~ `data-anim="d6"`，数字越大延迟越长
- 页面切换时自动给当前 `.slide` 加 `.active` 类，触发 CSS transition
- 不加 `data-anim` 的元素始终可见（如 chrome-min, footer-min）
- `data-anim-x` 为左侧滑入，`data-anim-pop` 为缩放弹入，`data-anim-zoom` 为从中心缩放，`data-anim-blur` 为模糊→清晰，`data-anim-slide-up` 为底部大幅滑入，`data-anim-rotate` 为旋转淡入

### 新增交互动画（CSS 已定义，直接使用）

| 效果 | 用法 | 说明 |
|------|------|------|
| 光泽扫过 | `.cta-btn.primary` 自带 | CTA 按钮自带 shimmer 动画 |
| 点击缩放 | `.cta-btn:active` 自带 | 点击时 scale(.97) |
| 卡片上浮 | `.feat-card:hover` 自带 | hover 时上浮 + 边框高亮 |
| 截图放大 | `.screenshot-wrap:hover img` 自带 | hover 时 scale(1.02) |
| 图标旋转 | 加 `.icon-hover` 在父元素 | hover 时图标 scale(1.15) rotate(-5deg) |
| 下划线揭示 | 加 `.underline-reveal` | hover 时下划线从左到右展开 |
| 卡片发光 | 加 `.card-glow` | hover 时边框发光 + 外阴影 |
| 标签脉冲 | 加 `.tag-pulse` | hover 时 scale(1.05) + 阴影 |
| 数字跳动 | 加 `.count-up` | hover 时 scale(1.08) + 变色 |

### 数字滚动动画（需 JS 配合）

在页面中需要数字滚动的地方，使用 `.num-roll` 类 + `data-target` 属性：

```html
<!-- 在 .stat-value 或 .metric-value 中使用 -->
<span class="stat-value num-roll" data-target="200">0</span>
<span class="unit">ms</span>
```

JS 已内置在模板 `&lt;script>` 中，页面激活时自动从 0 滚动到 `data-target` 值。

---

## 图标参考

使用 Lucide 图标，CDN 已引入。常用图标名:

| 用途 | 图标名 |
|------|--------|
| 下载 | `download` |
| GitHub | `github` |
| 截图 | `camera` |
| 窗口 | `scan-eye` / `monitor` |
| 标注 | `pencil` |
| 取色 | `pipette` |
| 速度 | `zap` |
| 剪贴板 | `copy` / `clipboard` |
| 对比 | `arrow-left-right` |
| 设置 | `settings` |
| 勾选 | `check-circle` |
| 搜索 | `search` |
| 帮助 | `help-circle` |
| 价格 | `tag` / `dollar-sign` |
| 时间 | `clock` / `calendar` |
| 用户 | `user` / `users` |
| 代码 | `code` / `terminal` |
| 星标 | `star` |
| 对勾 | `check` |
| 叉号 | `x` |
| 减号 | `minus` |
| 播放 | `play` |
| 视频 | `video` |
| 二维码 | `qr-code` |
| 微信 | `message-circle` |
| 团队 | `users` / `user-plus` |
| 星星 | `star` / `sparkle` |

---

## T31: 团队成员

展示开源项目贡献者或公司团队。用 `slide light`。

**所需 CSS 类**: `team-grid`, `member-card`, `member-avatar`, `member-name`, `member-role`, `member-links` (template.html 已定义)

```html
<section class="slide light">
  <div class="chrome-min">
    <span>开发团队</span>
    <span>07 / 12</span>
  </div>
  <div class="frame" style="padding-top:3vh">
    <div class="kicker" data-anim="d1">Team</div>
    <h2 class="h-xl" data-anim="d2">谁在开发</h2>

    <div class="team-grid" style="margin-top:4vh">
      <div class="member-card" data-anim="d2">
        <div class="member-avatar">A</div>
        <div class="member-name">Alex Chen</div>
        <div class="member-role">核心开发 · Python/Qt</div>
        <div class="member-links">
          <a href="#"><i data-lucide="github" style="width:1em;height:1em"></i></a>
        </div>
      </div>
      <div class="member-card" data-anim="d3">
        <div class="member-avatar">B</div>
        <div class="member-name">Bob Wang</div>
        <div class="member-role">UI 设计 · Figma</div>
        <div class="member-links">
          <a href="#"><i data-lucide="github" style="width:1em;height:1em"></i></a>
        </div>
      </div>
      <div class="member-card" data-anim="d4">
        <div class="member-avatar">C</div>
        <div class="member-name">Carol Li</div>
        <div class="member-role">测试 & 文档</div>
        <div class="member-links">
          <a href="#"><i data-lucide="github" style="width:1em;height:1em"></i></a>
        </div>
      </div>
      <div class="member-card" data-anim="d5">
        <div class="member-avatar">+</div>
        <div class="member-name">你来？</div>
        <div class="member-role">PR 欢迎 👏</div>
        <div class="member-links">
          <a href="#"><i data-lucide="heart" style="width:1em;height:1em"></i></a>
        </div>
      </div>
    </div>
  </div>
  <div class="footer-min">
    <span>Team · Contributors Welcome</span>
    <span>MIT License</span>
  </div>
</section>
```

**要点**:
- 4 个成员用 `.team-grid`（4 列），3 个用 `.grid-3`
- `.member-avatar` 自动显示姓名首字母，深色背景 + 白色文字
- 最后一个卡片可以放「贡献者招募」引导 PR

---

## T32: 视频嵌入

嵌入操作演示视频。用 `slide dark` 或 `slide light`。

**所需 CSS 类**: `video-wrap`, `video-cap`, `video-play-btn` (template.html 已定义)

```html
<section class="slide dark">
  <div class="chrome-min">
    <span>操作演示</span>
    <span>05 / 12</span>
  </div>
  <div class="frame center" style="gap:2vh;padding-top:2vh">
    <div class="kicker" data-anim="d1">Video Demo</div>
    <h2 class="h-lg" data-anim="d2">30 秒上手</h2>

    <div class="video-wrap" data-anim="d3">
      <video poster="images/video-cover.png" preload="metadata" controls style="width:100%;height:100%">
        <source src="images/demo.mp4" type="video/mp4">
      </video>
    </div>
    <p class="video-cap" data-anim="d4">▲ 完整操作流程演示 · 30 秒</p>
  </div>
  <div class="footer-min">
    <span>Video · 30s Demo</span>
    <span>—</span>
  </div>
</section>
```

**要点**:
- 本地视频放 `images/demo.mp4`，或用 `<iframe>` 嵌入 B站/YouTube
- `poster` 放封面图，视频加载前显示
- `.video-wrap` 自带 16:9 比例，自动适配

---

## T33: 二维码 / 微信引导

微信社群、公众号、小程序二维码引导页。用 `slide hero light` 或 `slide hero dark`。

**所需 CSS 类**: `qr-grid`, `qr-card`, `qr-img`, `qr-label`, `qr-desc`, `wechat-steps`, `wx-step`, `wx-step-num`, `wx-step-body`, `wx-step-title`, `wx-step-desc` (template.html 已定义)

```html
<section class="slide hero light">
  <div class="blob a"></div>
  <div class="blob b"></div>
  <div class="frame center" style="gap:3vh">
    <div class="kicker" data-anim="d1">Join Community</div>
    <h2 class="h-xl" data-anim="d2">加入用户群</h2>
    <p class="lead" style="text-align:center;max-width:50vw" data-anim="d3">
      扫码加入微信用户群，第一时间获取更新通知、使用技巧、专属福利。
    </p>

    <div class="qr-grid" data-anim="d4">
      <div class="qr-card">
        <div class="qr-img"><img src="images/qr-wechat.png" alt="微信群二维码"></div>
        <div class="qr-label">微信群</div>
        <div class="qr-desc">活跃用户群，提问秒回</div>
      </div>
      <div class="qr-card">
        <div class="qr-img"><img src="images/qr-public.png" alt="公众号二维码"></div>
        <div class="qr-label">公众号</div>
        <div class="qr-desc">每周推送使用技巧</div>
      </div>
    </div>
  </div>
  <div class="footer-min">
    <span>Community · WeChat Group</span>
    <span>Free Support</span>
  </div>
</section>
```

**要点**:
- 二维码图片建议用 `images/qr-*.png`，尺寸 ≥300x300
- `.wechat-steps` 是可选的「操作步骤」补充，没有可省略
- 用 `hero light` + blobs 效果最温暖，适合社群引导

---

## 背景选择指南（完整版）

> AI 选择逻辑见 SKILL.md Step 1「场景驱动」流程。以下为氛围速查 + 特殊用法。

| 页面氛围 | 推荐的背景类 | 适用主题 |
|---------|------------|---------|
| 科技/数据感 | bg-circuit, bg-particles, bg-grid, bg-stripes, bg-waveline | 科技蓝、极客紫、暗夜黑 |
| 优雅/专业感 | bg-geo, bg-hex, bg-dots, bg-ripple | 海洋青、午夜金、森琥珀 |
| 温暖/人文感 | blobs, bg-wave, bg-glow | 日落橙、玫瑰粉、效率绿 |
| 质感/沉稳感 | bg-noise, blobs, bg-stars | 暗夜黑、午夜金 |
| 纯净/留白感 | 只用 hero + blobs，不带背景类 | 所有主题 |
| 炫酷/视觉冲击 | bg-meteor, bg-glow, bg-hex, bg-diagonal, bg-stripeflow | 极客紫、暗夜黑、科技蓝 |

**特殊用法速查**：
- `bg-meteor`：需在 `<section>` 内添加 5 个 `<div class="meteor-trail"></div>`
- `bg-waveline`：Canvas 自动渲染，无需添加子元素；翻页自动启停
- `bg-diagonal`：`::before` + `::after` 双伪元素叠加，无需手动添加子元素

---

## 动画参考（完整版）

本模板使用**纯 CSS transition** 做入场动画，无需 Motion One：

- 每个需动效的元素加 `data-anim="d1"` ~ `data-anim="d6"`，数字越大延迟越长
- 页面切换时自动给当前 `.slide` 加 `.active` 类，触发 CSS transition
- 不加 `data-anim` 的元素始终可见（如 chrome-min, footer-min）
- `data-anim-x` 为左侧滑入，`data-anim-pop` 为缩放弹入，`data-anim-zoom` 为从中心缩放，`data-anim-blur` 为模糊→清晰，`data-anim-slide-up` 为底部大幅滑入，`data-anim-rotate` 为旋转淡入

### 新增交互动画（CSS 已定义，直接使用）

| 效果 | 用法 | 说明 |
|------|------|------|
| 光泽扫过 | `.cta-btn.primary` 自带 | CTA 按钮自带 shimmer 动画 |
| 点击缩放 | `.cta-btn:active` 自带 | 点击时 scale(.97) |
| 卡片上浮 | `.feat-card:hover` 自带 | hover 时上浮 + 边框高亮 |
| 截图放大 | `.screenshot-wrap:hover img` 自带 | hover 时 scale(1.02) |
| 图标旋转 | 加 `.icon-hover` 在父元素 | hover 时图标 scale(1.15) rotate(-5deg) |
| 下划线揭示 | 加 `.underline-reveal` | hover 时下划线从左到右展开 |
| 卡片发光 | 加 `.card-glow` | hover 时边框发光 + 外阴影 |
| 标签脉冲 | 加 `.tag-pulse` | hover 时 scale(1.05) + 阴影 |
| 数字跳动 | 加 `.count-up` | hover 时 scale(1.08) + 变色 |
| 数字滚动 | 加 `.num-roll` + `data-target="N"` | 页面激活时从 0 滚动到 N |

### 数字滚动使用说明

```html
<!-- 在 .stat-value 或 .metric-value 中使用 -->
<span class="stat-value num-roll" data-target="200">0</span>
<span class="unit">ms</span>

<!-- 大数字示例 -->
<span class="big-num num-roll" data-target="12000">0</span>
<span class="unit">条</span>
```

JS 已内置在模板 `<script>` 中，页面激活时自动从 0 滚动到 `data-target` 值（持续 1.5s，easeOutCubic 缓动）。
