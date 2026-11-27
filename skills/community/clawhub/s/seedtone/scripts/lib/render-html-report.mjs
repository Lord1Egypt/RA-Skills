/**
 * 渲染单文件、零依赖的人类可读 HTML 配色交付报告
 * 回答核心问题：1. 有什么颜色？ 2. 怎么安排（Web/App 场景）？ 3. 为什么稳定（WCAG + APCA 实测）？
 */
export function renderHtmlReport(data) {
	const { meta, flatLight, flatDark, metrics } = data;
	const lightVars = Object.entries(flatLight).map(([k, v]) => `--${k}: ${v};`).join("\n      ");
	const darkVars = Object.entries(flatDark).map(([k, v]) => `--${k}: ${v};`).join("\n      ");

	const roleRows = [
		{ name: "bgColor.default", desc: "页面主背景 / 纸面", rule: "全站最底层画布，禁止直接放未配对的浅灰字" },
		{ name: "bgColor.muted", desc: "次级面板 / 表头 / 卡片衬底", rule: "与 default 区分层级；暗色下若对比 <1.2:1 须加 borderColor.muted 兜边" },
		{ name: "bgColor.accent.emphasis", desc: "主按钮 / 刊头 / 整块强调平涂", rule: "一屏仅一处主强调色相，其上文字必须用 fgColor.onEmphasis" },
		{ name: "bgColor.deep", desc: "深图版 / 封面 / 深色 Banner", rule: "亮暗两主题均保持深底，其上文字必须用 fgColor.onDeep" },
		{ name: "fgColor.default", desc: "主标题 / 正文", rule: "最高可读性（≥7:1 AAA），用于核心阅读内容" },
		{ name: "fgColor.muted", desc: "时间 / 摘要 / 辅助说明", rule: "用于次要元数据，避免大段正文使用" },
		{ name: "fgColor.accent", desc: "链接 / 可交互文字与图标", rule: "仅代表可点击交互，不做纯装饰用途" },
		{ name: "fgColor.accentHover", desc: "链接与文本按钮 Hover 态", rule: "只改亮度不改色相，提供明确悬停反馈" },
		{ name: "fgColor.onEmphasis", desc: "强调实底上的反白文字", rule: "严禁直接写 #fff，必须与 bgColor.accent.emphasis 成对" },
		{ name: "fgColor.disabled", desc: "禁用态文字与图标", rule: "必须配合不可点击状态与位置/文案提示，不可单独表义" },
		{ name: "borderColor.default", desc: "输入框 / 按钮边框", rule: "≥3:1 图形对比度，保证控件边界清晰" },
		{ name: "borderColor.muted", desc: "列表分割线 / 卡片兜边", rule: "柔和分隔内容区块，不抢夺视觉焦点" },
		{ name: "focus.outlineColor", desc: "键盘焦点环", rule: "独立可访问性角色，建议 2px solid" },
		{ name: "fgColor.danger", desc: "危险 / 错误提示（异色）", rule: "与主强调色保持区分，必须搭配图标或文字冗余" },
	];

	if (meta.withSemantic) {
		roleRows.push(
			{ name: "fgColor.success / bgColor.success.*", desc: "成功 / 完成状态（异色）", rule: "浅底配语义字，或实底配反白字" },
			{ name: "fgColor.warning / bgColor.warning.*", desc: "警告 / 注意状态（异色）", rule: "高警示提示条，避免大面积平涂" },
			{ name: "fgColor.info / bgColor.info.*", desc: "信息 / 引导状态（异色）", rule: "已自动与主色相保持 ≥35° 分离" },
		);
	}

	const renderSwatchGroup = (title, keys, themeObj) => `
    <div class="swatch-group">
      <div class="group-title">${title}</div>
      <div class="swatch-grid">
        ${keys
			.filter((k) => themeObj[k])
			.map(
				(k) => `
          <button type="button" class="swatch-card" data-copy="--${k}" title="点击复制 CSS 变量 --${k}">
            <span class="swatch-chip" style="background:${themeObj[k]}"></span>
            <span class="swatch-meta">
              <strong class="mono">--${k}</strong>
              <span class="mono hex">${themeObj[k]}</span>
            </span>
          </button>`,
			)
			.join("")}
      </div>
    </div>`;

	const renderMetricsTable = (rows) => `
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>配对角色</th>
            <th>前景色</th>
            <th>背景色</th>
            <th>WCAG 2.1</th>
            <th>APCA Lc</th>
            <th>校验结果</th>
          </tr>
        </thead>
        <tbody>
          ${rows
				.map(
					(r) => `
            <tr>
              <td>${r.label}<div class="sub-var mono">${r.fg} / ${r.bg}</div></td>
              <td><span class="dot" style="background:${r.fgHex}"></span><span class="mono">${r.fgHex}</span></td>
              <td><span class="dot" style="background:${r.bgHex}"></span><span class="mono">${r.bgHex}</span></td>
              <td class="mono"><strong>${r.wcag}:1</strong> <span class="req">(&ge;${r.wcagMin})</span></td>
              <td class="mono"><strong>Lc ${r.lc}</strong> <span class="req">(&ge;${r.apcaMin})</span></td>
              <td><span class="badge ${r.passWcag ? "badge-ok" : "badge-warn"}">${r.passWcag ? "WCAG PASS" : "CHECK"}</span></td>
            </tr>`,
				)
				.join("")}
        </tbody>
      </table>
    </div>`;

	const allCssExport = `:root {\n  ${lightVars}\n}\n\n.dark {\n  ${darkVars}\n}`;

	return `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>配色方案交付报告 · Seed ${meta.seed}</title>
  <style>
    :root {
      ${lightVars}
    }
    html.dark {
      ${darkVars}
    }
    *, *::before, *::after { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bgColor-default);
      color: var(--fgColor-default);
      font-family: "Inter", "Noto Sans SC", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      font-size: 15px;
      line-height: 1.65;
      transition: background-color .2s ease, color .2s ease;
    }
    .mono { font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
    .container { max-width: 1180px; margin: 0 auto; padding: 0 24px 80px; }

    /* 顶部栏 */
    .topbar {
      position: sticky; top: 0; z-index: 20;
      background: var(--bgColor-default);
      border-bottom: 1px solid var(--borderColor-muted);
      backdrop-filter: blur(8px);
    }
    .topbar-inner {
      max-width: 1180px; margin: 0 auto; padding: 14px 24px;
      display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px;
    }
    .brand { display: flex; align-items: center; gap: 10px; font-weight: 700; font-size: 16px; }
    .seed-pill {
      display: inline-flex; align-items: center; gap: 8px;
      padding: 4px 10px; border-radius: 999px;
      background: var(--bgColor-muted); border: 1px solid var(--borderColor-muted);
      font-size: 12px;
    }
    .seed-dot { width: 12px; height: 12px; border-radius: 50%; background: ${meta.seed}; border: 1px solid var(--borderColor-default); }
    .actions { display: flex; gap: 10px; align-items: center; }
    .btn {
      appearance: none; border: 1px solid var(--borderColor-default);
      background: var(--bgColor-default); color: var(--fgColor-default);
      padding: 7px 14px; border-radius: 8px; font-size: 13px; font-weight: 600; cursor: pointer;
    }
    .btn:hover { border-color: var(--borderColor-accent); color: var(--fgColor-accent); }
    .btn-primary {
      background: var(--bgColor-accent-emphasis); color: var(--fgColor-onEmphasis);
      border-color: var(--bgColor-accent-emphasis);
    }
    .btn-primary:hover { opacity: 0.92; color: var(--fgColor-onEmphasis); }

    /* Hero */
    .hero { padding: 48px 0 32px; border-bottom: 1px solid var(--borderColor-muted); }
    .hero h1 { margin: 0 0 12px; font-size: clamp(28px, 4vw, 42px); letter-spacing: -0.02em; line-height: 1.15; }
    .hero p { margin: 0; color: var(--fgColor-muted); max-width: 72ch; }
    .pillars {
      display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 12px; margin-top: 24px;
    }
    .pillar {
      background: var(--bgColor-muted); border: 1px solid var(--borderColor-muted);
      border-radius: 10px; padding: 14px 16px;
    }
    .pillar .k { font-size: 11px; text-transform: uppercase; letter-spacing: .08em; color: var(--fgColor-accent); font-weight: 700; }
    .pillar .v { font-size: 14px; font-weight: 600; margin: 4px 0; }
    .pillar .d { font-size: 12.5px; color: var(--fgColor-muted); }

    /* 章节 */
    section { padding-top: 48px; }
    section h2 { font-size: 22px; margin: 0 0 8px; }
    section .lede { color: var(--fgColor-muted); margin: 0 0 24px; font-size: 14px; }

    /* 场景预览：Web & App */
    .preview-grid { display: grid; grid-template-columns: 1.45fr 1fr; gap: 24px; align-items: start; }
    @media (max-width: 900px) { .preview-grid { grid-template-columns: 1fr; } }
    .mockup {
      border: 1px solid var(--borderColor-default); border-radius: 14px; overflow: hidden;
      background: var(--bgColor-default);
    }
    .mockup-bar {
      display: flex; align-items: center; justify-content: space-between;
      padding: 10px 16px; background: var(--bgColor-muted); border-bottom: 1px solid var(--borderColor-muted);
      font-size: 12px; color: var(--fgColor-muted);
    }
    .web-nav {
      display: flex; align-items: center; justify-content: space-between;
      padding: 14px 20px; border-bottom: 1px solid var(--borderColor-muted);
    }
    .web-nav .links { display: flex; gap: 16px; font-size: 13px; }
    .web-nav a { color: var(--fgColor-muted); text-decoration: none; }
    .web-nav a.active { color: var(--fgColor-accent); font-weight: 600; }
    .web-hero {
      background: var(--bgColor-deep); color: var(--fgColor-onDeep);
      padding: 28px 24px;
    }
    .web-hero h3 { margin: 0 0 8px; font-size: 20px; }
    .web-hero p { margin: 0 0 16px; font-size: 13px; opacity: .86; }
    .web-body { padding: 20px; display: grid; gap: 14px; }
    .card-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    .mini-card {
      background: var(--bgColor-muted); border: 1px solid var(--borderColor-muted);
      border-radius: 10px; padding: 14px;
    }
    .mini-card h4 { margin: 0 0 4px; font-size: 14px; }
    .mini-card p { margin: 0; font-size: 12.5px; color: var(--fgColor-muted); }
    .input-row { display: flex; gap: 8px; }
    .mock-input {
      flex: 1; padding: 8px 12px; border-radius: 8px;
      border: 1px solid var(--borderColor-default); background: var(--bgColor-default);
      color: var(--fgColor-default); font-size: 13px;
    }
    .mock-input:focus { outline: 2px solid var(--focus-outlineColor); outline-offset: 1px; }
    .alerts-stack { display: grid; gap: 8px; }
    .alert {
      padding: 8px 12px; border-radius: 8px; font-size: 12.5px; font-weight: 500;
      border: 1px solid var(--borderColor-muted);
    }

    /* 手机 App 预览 */
    .phone-frame {
      max-width: 340px; margin: 0 auto; border: 2px solid var(--borderColor-emphasis);
      border-radius: 26px; overflow: hidden; background: var(--bgColor-default);
    }
    .phone-header {
      padding: 16px 18px 12px; border-bottom: 1px solid var(--borderColor-muted);
      display: flex; justify-content: space-between; align-items: center;
    }
    .phone-content { padding: 16px; display: grid; gap: 12px; }
    .phone-tabs {
      display: grid; grid-template-columns: repeat(3, 1fr);
      border-top: 1px solid var(--borderColor-muted); background: var(--bgColor-muted);
      text-align: center; font-size: 12px;
    }
    .phone-tabs div { padding: 10px 4px; color: var(--fgColor-muted); }
    .phone-tabs div.active { color: var(--fgColor-accent); font-weight: 700; border-top: 2px solid var(--borderColor-accent); }

    /* 色板网格 */
    .swatch-group { margin-bottom: 24px; }
    .group-title { font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; color: var(--fgColor-muted); margin-bottom: 10px; }
    .swatch-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 10px; }
    .swatch-card {
      display: flex; align-items: center; gap: 12px; padding: 10px;
      background: var(--bgColor-muted); border: 1px solid var(--borderColor-muted);
      border-radius: 10px; text-align: left; cursor: pointer; color: inherit;
    }
    .swatch-card:hover { border-color: var(--borderColor-accent); }
    .swatch-chip { width: 38px; height: 38px; border-radius: 8px; border: 1px solid var(--borderColor-default); flex-shrink: 0; }
    .swatch-meta { display: flex; flex-direction: column; min-width: 0; }
    .swatch-meta strong { font-size: 12px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .swatch-meta .hex { font-size: 11.5px; color: var(--fgColor-muted); }

    /* 表格 */
    .table-wrap { overflow-x: auto; border: 1px solid var(--borderColor-muted); border-radius: 10px; }
    table { width: 100%; border-collapse: collapse; font-size: 13px; }
    th, td { padding: 10px 14px; border-bottom: 1px solid var(--borderColor-muted); text-align: left; }
    th { background: var(--bgColor-muted); font-size: 12px; color: var(--fgColor-muted); font-weight: 600; }
    tr:last-child td { border-bottom: none; }
    .sub-var { font-size: 11px; color: var(--fgColor-muted); }
    .dot { display: inline-block; width: 12px; height: 12px; border-radius: 3px; border: 1px solid var(--borderColor-default); vertical-align: -2px; margin-right: 6px; }
    .req { font-size: 11px; color: var(--fgColor-muted); }
    .badge { display: inline-block; padding: 2px 8px; border-radius: 999px; font-size: 11px; font-weight: 700; }
    .badge-ok { border: 1px solid var(--borderColor-accent); color: var(--fgColor-accent); }
    .badge-warn { border: 1px solid var(--fgColor-danger); color: var(--fgColor-danger); }

    .toast {
      position: fixed; bottom: 24px; right: 24px; padding: 10px 16px; border-radius: 8px;
      background: var(--bgColor-deep); color: var(--fgColor-onDeep); font-size: 13px;
      opacity: 0; pointer-events: none; transition: opacity .2s ease;
    }
    .toast.show { opacity: 1; }
  </style>
</head>
<body>
  <header class="topbar">
    <div class="topbar-inner">
      <div class="brand">
        <span>Color System Delivery</span>
        <span class="seed-pill mono"><span class="seed-dot"></span>Seed ${meta.seed} · ${meta.tint}</span>
      </div>
      <div class="actions">
        <button class="btn" id="toggleTheme">切换暗色/亮色预览</button>
        <button class="btn btn-primary" id="copyCss">复制全套 CSS 变量</button>
      </div>
    </div>
  </header>

  <main class="container">
    <section class="hero">
      <h1>只给一个色号，交付一整套稳定配色</h1>
      <p>本方案由胶水架构自动求解生成：基于 <strong>GitHub Primer</strong> 的语义角色分工，结合 <strong>OKLCH 微染色中性阶</strong>、<strong>Adobe Leonardo 对比度强调阶</strong> 与 <strong>W3C DTCG</strong> 标准，并经过 <strong>WCAG 2.1 + APCA</strong> 双重可访问性核算。</p>
      <div class="pillars">
        <div class="pillar">
          <div class="k">起源 01 · 语义角色</div>
          <div class="v">Primer Primitives</div>
          <div class="d">规定 fg / bg / border / focus 职责边界，不乱用色块</div>
        </div>
        <div class="pillar">
          <div class="k">起源 02 · 对比度数学</div>
          <div class="v">Adobe Leonardo + OKLCH</div>
          <div class="d">钉死纸色不漂移，亮暗双主题独立保证对比度</div>
        </div>
        <div class="pillar">
          <div class="k">起源 03 · 工程承载</div>
          <div class="v">W3C DTCG + Style Dictionary</div>
          <div class="d">同步输出 CSS 变量、Tailwind v4 @theme 与 DTCG JSON</div>
        </div>
        <div class="pillar">
          <div class="k">起源 04 · 感知校验</div>
          <div class="v">WCAG 2.1 + APCA Lc</div>
          <div class="d">同时校验亮度比与现代视觉感知对比度</div>
        </div>
      </div>
    </section>

    <section>
      <h2>1. 真实场景怎么安排？（Web 网站 & 移动端 App）</h2>
      <p class="lede">点击右上角“切换暗色/亮色预览”，直接观察同一套语义变量在网页与手机界面下的稳定表现。</p>
      <div class="preview-grid">
        <div class="mockup">
          <div class="mockup-bar"><span>Web / SaaS 场景预览</span><span class="mono">bgColor-default + deep + accent</span></div>
          <div class="web-nav">
            <strong class="mono">Brand.</strong>
            <div class="links">
              <a href="javascript:void(0)" class="active">概览</a>
              <a href="javascript:void(0)">文档</a>
              <a href="javascript:void(0)">配置</a>
            </div>
          </div>
          <div class="web-hero">
            <h3>深图版刊头（bgColor.deep + fgColor.onDeep）</h3>
            <p>无论亮色还是暗色模式，深图版始终保持沉稳深底，适合做 Hero、封面或重点数据板。</p>
            <button class="btn btn-primary" type="button">主操作按钮（accent.emphasis）</button>
          </div>
          <div class="web-body">
            <div class="card-row">
              <div class="mini-card">
                <h4>次级容器（bgColor.muted）</h4>
                <p>搭配 borderColor.muted 兜边，暗色模式下依然层次分明。</p>
              </div>
              <div class="mini-card">
                <h4>交互链接（fgColor.accent）</h4>
                <p>点击这里查看 <a href="javascript:void(0)" style="color:var(--fgColor-accent)">详情说明 →</a></p>
              </div>
            </div>
            <div class="input-row">
              <input class="mock-input" type="text" value="聚焦查看 focus.outlineColor 焦点环" />
              <button class="btn" type="button" disabled style="color:var(--fgColor-disabled);cursor:not-allowed">禁用态</button>
            </div>
            <div class="alerts-stack">
              <div class="alert" style="color:var(--fgColor-danger);background:${meta.withSemantic ? "var(--bgColor-danger-muted)" : "var(--bgColor-muted)"}">危险提示：操作不可逆，请确认后删除。</div>
              ${meta.withSemantic ? `
              <div class="alert" style="color:var(--fgColor-success);background:var(--bgColor-success-muted)">成功提示：配色令牌已编译并校验通过。</div>
              <div class="alert" style="color:var(--fgColor-warning);background:var(--bgColor-warning-muted)">警告提示：请勿在业务代码中硬编码 Hex 色值。</div>
              <div class="alert" style="color:var(--fgColor-info);background:var(--bgColor-info-muted)">信息提示：所有异色已自动避开主品牌色相。</div>` : ""}
            </div>
          </div>
        </div>

        <div class="phone-frame">
          <div class="phone-header">
            <strong>App 移动端预览</strong>
            <span class="mono" style="font-size:11px;color:var(--fgColor-accent)">编辑</span>
          </div>
          <div class="phone-content">
            <div class="mini-card">
              <div style="font-size:11px;color:var(--fgColor-muted)">今日概览</div>
              <div style="font-size:22px;font-weight:700;margin:4px 0">98.4%</div>
              <div style="font-size:12px;color:var(--fgColor-accent)">对比度健康度达标</div>
            </div>
            <button class="btn btn-primary" style="width:100%" type="button">立即应用主题</button>
            <button class="btn" style="width:100%" type="button">导出 Tailwind 配置</button>
          </div>
          <div class="phone-tabs">
            <div class="active">首页</div>
            <div>组件</div>
            <div>设置</div>
          </div>
        </div>
      </div>
    </section>

    <section>
      <h2>2. 有什么颜色？（点击任意色卡复制变量名）</h2>
      <p class="lede">下方展示当前预览主题（随右上角切换）的所有语义色值。</p>
      <div id="swatches-light">
        ${renderSwatchGroup("亮色模式 · 背景与表面 (bgColor)", ["bgColor-default", "bgColor-muted", "bgColor-accent-emphasis", "bgColor-deep"], flatLight)}
        ${renderSwatchGroup("亮色模式 · 文字与图标 (fgColor)", ["fgColor-default", "fgColor-muted", "fgColor-disabled", "fgColor-accent", "fgColor-accentHover", "fgColor-onEmphasis", "fgColor-onDeep", "fgColor-danger"], flatLight)}
        ${renderSwatchGroup("亮色模式 · 边框与焦点 (borderColor / focus)", ["borderColor-default", "borderColor-muted", "borderColor-emphasis", "borderColor-accent", "focus-outlineColor"], flatLight)}
        ${meta.withSemantic ? renderSwatchGroup("亮色模式 · 扩展异色 (success / warning / info / danger)", ["fgColor-success", "bgColor-success-muted", "bgColor-success-emphasis", "fgColor-warning", "bgColor-warning-muted", "bgColor-warning-emphasis", "fgColor-info", "bgColor-info-muted", "bgColor-info-emphasis", "bgColor-danger-muted", "bgColor-danger-emphasis"], flatLight) : ""}
      </div>
      <div id="swatches-dark" style="display:none">
        ${renderSwatchGroup("暗色模式 · 背景与表面 (bgColor)", ["bgColor-default", "bgColor-muted", "bgColor-accent-emphasis", "bgColor-deep"], flatDark)}
        ${renderSwatchGroup("暗色模式 · 文字与图标 (fgColor)", ["fgColor-default", "fgColor-muted", "fgColor-disabled", "fgColor-accent", "fgColor-accentHover", "fgColor-onEmphasis", "fgColor-onDeep", "fgColor-danger"], flatDark)}
        ${renderSwatchGroup("暗色模式 · 边框与焦点 (borderColor / focus)", ["borderColor-default", "borderColor-muted", "borderColor-emphasis", "borderColor-accent", "focus-outlineColor"], flatDark)}
        ${meta.withSemantic ? renderSwatchGroup("暗色模式 · 扩展异色 (success / warning / info / danger)", ["fgColor-success", "bgColor-success-muted", "bgColor-success-emphasis", "fgColor-warning", "bgColor-warning-muted", "bgColor-warning-emphasis", "fgColor-info", "bgColor-info-muted", "bgColor-info-emphasis", "bgColor-danger-muted", "bgColor-danger-emphasis"], flatDark) : ""}
      </div>
    </section>

    <section>
      <h2>3. 角色安排速查表（怎么用 & 禁止怎么用）</h2>
      <p class="lede">遵循“字与面成对、一屏一强调色相、颜色不单独表义”三条不变量。</p>
      <div class="table-wrap">
        <table>
          <thead><tr><th>语义角色</th><th>职责定义</th><th>安排与禁忌规则</th></tr></thead>
          <tbody>
            ${roleRows.map((r) => `<tr><td class="mono"><strong>${r.name}</strong></td><td>${r.desc}</td><td>${r.rule}</td></tr>`).join("")}
          </tbody>
        </table>
      </div>
    </section>

    <section>
      <h2>4. 对比度实测报告（WCAG 2.1 + APCA Lc）</h2>
      <p class="lede">暗色模式下 WCAG 2.1 有时会低估浅字可读性，因此同时提供 APCA 感知对比度（|Lc| ≥ 60 适合正文，≥ 30 适合大字/边框）。</p>
      <h3>亮色模式实测</h3>
      ${renderMetricsTable(metrics.light)}
      <h3 style="margin-top:24px">暗色模式实测</h3>
      ${renderMetricsTable(metrics.dark)}
    </section>
  </main>

  <textarea id="cssSource" style="position:fixed;left:-9999px">${allCssExport}</textarea>
  <div class="toast" id="toast">已复制到剪贴板</div>

  <script>
    const html = document.documentElement;
    const swLight = document.getElementById("swatches-light");
    const swDark = document.getElementById("swatches-dark");
    const toast = document.getElementById("toast");

    function showToast(msg) {
      toast.textContent = msg;
      toast.classList.add("show");
      setTimeout(() => toast.classList.remove("show"), 1800);
    }

    document.getElementById("toggleTheme").addEventListener("click", () => {
      const isDark = html.classList.toggle("dark");
      swLight.style.display = isDark ? "none" : "block";
      swDark.style.display = isDark ? "block" : "none";
    });

    document.getElementById("copyCss").addEventListener("click", async () => {
      await navigator.clipboard.writeText(document.getElementById("cssSource").value);
      showToast("已复制全套 :root / .dark CSS 变量");
    });

    document.querySelectorAll(".swatch-card").forEach((el) => {
      el.addEventListener("click", async () => {
        const varName = el.getAttribute("data-copy");
        await navigator.clipboard.writeText("var(" + varName + ")");
        showToast("已复制 var(" + varName + ")");
      });
    });
  </script>
</body>
</html>`;
}
