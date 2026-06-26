const esc = (s = "") => String(s)
  .replace(/&/g, "&amp;").replace(/</g, "&lt;")
  .replace(/>/g, "&gt;").replace(/"/g, "&quot;");

/**
 * @param {object} opts
 * @param {string} opts.projectId
 * @param {string} opts.exportedAt
 * @param {Array<{
 *   name: string,
 *   screens: Array<{ name: string, htmlPath: string, thumbnailUrl: string|null }>
 * }>} opts.sections
 */
export const renderIndexHtml = ({ projectId, exportedAt, sections }) => {
  const dateStr = exportedAt
    ? exportedAt.replace("T", " ").replace(/\.\d+Z$/, " UTC")
    : "";

  const sectionsHtml = sections.map(({ name, screens }) => `
  <section class="section">
    <h2>${esc(name)}<span class="count">${screens.length}</span></h2>
    <div class="screen-grid">
      ${screens.map(({ name: sName, htmlPath, thumbnailUrl }) => `
      <a class="screen-card" href="${esc(htmlPath)}" target="_blank">
        <div class="thumb-wrap">
          ${thumbnailUrl
            ? `<img class="thumb" src="${esc(thumbnailUrl)}" alt="" loading="lazy" />`
            : `<div class="thumb-placeholder"></div>`}
        </div>
        <div class="screen-name">${esc(sName)}</div>
      </a>`).join("")}
    </div>
  </section>`).join("\n");

  const zeplinUrl = `https://app.zeplin.io/project/${projectId}`;

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <title>Project Export – ${esc(projectId)}</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; }
    body { margin: 0; padding: 32px 40px; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #f0f2f5; color: #111; }
    h1 { margin: 0 0 4px; font-size: 22px; }
    .zeplin-link { font-size: 12px; color: #1a73e8; text-decoration: none; word-break: break-all; }
    .zeplin-link:hover { text-decoration: underline; }
    .meta { color: #888; font-size: 13px; margin-bottom: 32px; }
    .section { background: #fff; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.07); padding: 20px 24px 24px; margin-bottom: 24px; }
    h2 { margin: 0 0 16px; font-size: 16px; color: #1a1a1a; display: flex; align-items: center; gap: 8px; }
    .count { font-size: 12px; font-weight: 500; background: #f1f5f9; color: #64748b; padding: 2px 8px; border-radius: 999px; }
    .screen-grid { display: flex; flex-wrap: wrap; gap: 16px; }
    .screen-card {
      display: flex; flex-direction: column; align-items: center;
      width: 128px; text-decoration: none; color: inherit;
      border-radius: 8px; overflow: hidden;
      border: 1px solid #e2e8f0; background: #f8fafc;
      transition: box-shadow 0.15s, transform 0.15s;
    }
    .screen-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.12); transform: translateY(-2px); }
    .thumb-wrap { width: 128px; height: 220px; overflow: hidden; background: #e8ecf0; display: flex; align-items: center; justify-content: center; }
    .thumb { width: 100%; height: 100%; object-fit: cover; object-position: top; display: block; }
    .thumb-placeholder { width: 100%; height: 100%; background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%); }
    .screen-name { padding: 6px 8px; font-size: 11px; text-align: center; line-height: 1.3; color: #374151; width: 100%; background: #fff; border-top: 1px solid #e2e8f0; word-break: break-all; }
  </style>
</head>
<body>
  <h1>Project: ${esc(projectId)}</h1>
  <a class="zeplin-link" href="${esc(zeplinUrl)}" target="_blank" rel="noopener">${esc(zeplinUrl)}</a>
  <div class="meta">Exported: ${esc(dateStr)}</div>
  ${sectionsHtml}
</body>
</html>`;
};
