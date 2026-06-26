export const escapeHtml = (text = "") => String(text)
  .replace(/&/g, "&amp;")
  .replace(/</g, "&lt;")
  .replace(/>/g, "&gt;")
  .replace(/"/g, "&quot;")
  .replace(/'/g, "&#39;");

export const renderTreeHTML = (nodes, styleHelpers = {}) => {
  const {
    formatNumeric = (value) => Number.isFinite(value) ? String(value) : null,
    shouldDisplayBorderRadius = () => false,
    shouldDisplayOpacity = () => false
  } = styleHelpers;
  const renderNode = (node, path = []) => {
    const rel = node.frame ? `(${node.frame.x}, ${node.frame.y}, ${node.frame.width}, ${node.frame.height})` : "(none)";
    const metaParts = [
      `type=${escapeHtml(node.type || "")}`
    ];
    if (node.rotation) metaParts.push(`rotation=${node.rotation}`);
    if (shouldDisplayOpacity(node.opacity)) {
      const opacityDisplay = formatNumeric(node.opacity);
      metaParts.push(`opacity=${opacityDisplay ?? node.opacity}`);
    }
    if (node.shadow) metaParts.push(`shadow=${escapeHtml(node.shadow)}`);
    if (shouldDisplayBorderRadius(node.borderRadius)) metaParts.push(`borderRadius=${node.borderRadius}`);
    if (node.borderWidth !== undefined) metaParts.push(`borderWidth=${node.borderWidth}`);
    if (node.borderColorName) {
      metaParts.push(`borderColorName=${escapeHtml(node.borderColorName)}`);
    } else if (node.borderColor) {
      metaParts.push(`borderColor=${escapeHtml(node.borderColor)}`);
    }
    if (node.fillColorName) {
      metaParts.push(`fillColorName=${escapeHtml(node.fillColorName)}`);
    } else if (node.fillColorHex) {
      metaParts.push(`fillColor=${escapeHtml(node.fillColorHex)}`);
    } else if (node.fillColor) {
      metaParts.push(`fillColor=${escapeHtml(node.fillColor)}`);
    }
    if (node.constraints && Object.keys(node.constraints).length) {
      const constraintPairs = Object.entries(node.constraints).map(([key, value]) => {
        if (typeof value === "number") {
          const display = formatNumeric(value);
          return `${escapeHtml(key)}=${escapeHtml(display ?? String(value))}`;
        }
        return `${escapeHtml(key)}=${escapeHtml(String(value))}`;
      });
      if (constraintPairs.length) metaParts.push(`constraints:${constraintPairs.join(", ")}`);
    }
    if (node.textContent) {
      const textSnippet = node.textContent.length > 100
        ? `${node.textContent.slice(0, 97)}...`
        : node.textContent;
      metaParts.push(`text="${escapeHtml(textSnippet)}"`);
    }
    if (node.textStyle) {
      if (node.textStyle.fontFamily) metaParts.push(`font=${escapeHtml(node.textStyle.fontFamily)}`);
      if (node.textStyle.fontName) metaParts.push(`fontName=${escapeHtml(node.textStyle.fontName)}`);
      if (node.textStyle.fontSize) metaParts.push(`size=${node.textStyle.fontSize}px`);
      if (node.textStyle.fontWeight) metaParts.push(`weight=${escapeHtml(node.textStyle.fontWeight)}`);
      if (node.textStyle.lineHeight) {
        const lh = node.textStyle.lineHeight;
        const lhDisplay = typeof lh === "number" ? `${lh}px` : String(lh);
        metaParts.push(`lineHeight=${escapeHtml(lhDisplay)}`);
      }
      if (node.textStyle.textAlign) metaParts.push(`textAlign=${escapeHtml(node.textStyle.textAlign)}`);
      if (node.textStyle.colorName) metaParts.push(`colorName=${escapeHtml(node.textStyle.colorName)}`);
      if (node.textStyle.color) metaParts.push(`color=${escapeHtml(node.textStyle.color)}`);
    }
    if (node.image) {
      if (node.image.assetName) {
        metaParts.push(`imageName=${escapeHtml(node.image.assetName)}`);
      }
    }
    if (node.gradientColor) {
      metaParts.push(`gradientColor=${escapeHtml(node.gradientColor)}`);
    } else if (node.gradient?.description) {
      metaParts.push(`gradientColor=${escapeHtml(node.gradient.description)}`);
    }
    const meta = metaParts.join(" · ");
    const indentDots = path.length ? `${"• ".repeat(path.length)}` : "";
    const summary = `${indentDots}${escapeHtml(node.name || node.id || "")} ${meta}` +
      ` · frame=${rel}`;
    const childList = Array.isArray(node.children) ? node.children : [];
    const children = childList.length
      ? `<ul>${childList.map((child, index) => renderNode(child, path.concat(index + 1))).join("")}</ul>`
      : "";
    const descId = escapeHtml(node.generatedId || node.descId || node.id || "");
    const originalId = escapeHtml(node.id || "");
    const idAttrParts = [];
    if (descId) idAttrParts.push(`data-layer-desc-id="${descId}"`, `id="desc-${descId}"`);
    if (originalId) idAttrParts.push(`data-layer-original-id="${originalId}"`);
    if (path.length) idAttrParts.push(`data-layer-path="${path.join(".")}"`);
    const idAttr = idAttrParts.join(" ");
    return `<li class="layer-desc" ${idAttr}><details open><summary>${summary}</summary>${children}</details></li>`;
  };
  const rootList = Array.isArray(nodes) ? nodes : [];
  return `<ul class="tree">${rootList.map((node, index) => renderNode(node, [index + 1])).join("")}</ul>`;
};
