import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { escapeHtml, renderTreeHTML } from "./renderTree.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));
const STYLES = readFileSync(join(__dirname, "previewStyles.css"), "utf8");
const CLIENT_SCRIPT = readFileSync(join(__dirname, "previewClient.js"), "utf8");

export const makeTreeHTMLDocument = (nodes, meta, options = {}) => {
  const styleHelpers = options.styleHelpers || {};
  const minifiedTree = options.minifiedTree || null;
  const minifiedRootWrapped = options.minifiedRootWrapped === true;
  const minifiedTreeJson = minifiedTree
    ? JSON.stringify(minifiedTree).replace(/</g, "\\u003c")
    : null;
  const minifiedTreeScript = minifiedTreeJson
    ? `<script type="application/json" id="minifiedTree">${minifiedTreeJson}</script>`
    : "";
  const storageKey = `zeplin-layer-instructions:${meta.project || ""}:${meta.screen || ""}`;
  const backUrl = meta.backUrl || null;
  const zeplinUrl = meta.project && meta.screenId
    ? `https://app.zeplin.io/project/${meta.project}/screen/${meta.screenId}`
    : null;

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>ZeplinToPrompt</title>
  <style>
${STYLES}  </style>
</head>
<body>
  <div id="appConfig" data-minified-root-wrapped="${minifiedRootWrapped ? 'true' : 'false'}" data-storage-key="${escapeHtml(storageKey)}" style="display:none"></div>
  <div class="layout-left">
    <div class="page-header">
      ${backUrl ? `<a class="back-link" href="${escapeHtml(backUrl)}">← Back to Index</a>` : ""}
      <h1>ZeplinToPrompt</h1>
      <div class="meta">Project: ${escapeHtml(meta.project || "")} · Screen: ${escapeHtml(meta.screen || "")} · ${escapeHtml(meta.exportedAt ? meta.exportedAt.replace("T", " ").replace(/\.\d+Z$/, " UTC") : "")}</div>${zeplinUrl ? `<a class="zeplin-link" href="${escapeHtml(zeplinUrl)}" target="_blank" rel="noopener">View Original in Zeplin: ${escapeHtml(zeplinUrl)}</a>` : ""}
    </div>
    <section class="preview-section">
      ${meta.preview || ""}
      <div class="multi-select-toolbar" id="multiSelectToolbar">
        <span class="multi-select-count" id="multiSelectCount">0 selected</span>
        <button id="multiCopyButton">Copy Prompt</button>
        <button id="multiCopyAlignedButton">Copy Prompt (Aligned)</button>
        <button class="btn-clear" id="multiClearButton">Clear Selection</button>
      </div>
      <div class="preview-instruction-editor" id="previewInstructionEditor">
        <div class="preview-instruction-title" id="previewInstructionTitle">Edit Prompt</div>
        <textarea id="previewInstructionTextarea" placeholder="Describe implementation requirements for this layer, for example: use UIStackView here; align all content to the left."></textarea>
        <div class="preview-instruction-toolbar">
          <div class="preview-instruction-hint">Edit from the preview right-click menu. Copied JSON will be written to the instruction field.</div>
          <div class="preview-instruction-actions">
            <button type="button" class="instruction-save" id="previewInstructionSaveButton">Save</button>
            <button type="button" class="instruction-close" id="previewInstructionCloseButton">Close</button>
          </div>
        </div>
      </div>
    </section>
  </div>
  <div class="layout-right">
    <section class="description-panel">
      <h3>Layer Descriptions</h3>
      <div class="description-content" id="layerDescriptionList">${renderTreeHTML(nodes, styleHelpers)}</div>
    </section>
  </div>
  <div class="copied-toast" id="copiedToast">Copied</div>
  <div class="context-copy-menu" id="contextCopyMenu">
    <button id="contextEditInstructionButton">Add Prompt</button>
    <button id="contextCopyButton">Copy Prompt</button>
    <button id="contextCopyAlignedButton">Copy Prompt (Alignment Info)</button>
  </div>
  <div class="sidebar-btns">
    <button class="debug-toggle-btn" id="debugToggleBtn">Layer Debug</button>
    <button class="multi-select-btn" id="multiSelectBtn">Multi-Select</button>
  </div>
  ${minifiedTreeScript}
  <script>${CLIENT_SCRIPT}</script>
</body>
</html>`;
};
