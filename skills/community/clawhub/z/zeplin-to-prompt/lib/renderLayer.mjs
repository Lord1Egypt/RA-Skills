import { extractImageInfo } from "./assets.mjs";
import { toFrame } from "./layerTree.mjs";
import { escapeHtml } from "./renderTree.mjs";

const renderLayerPreview = (layer, parentAbs, origin, zIndexRef, ctx = {}, depth = 0) => {
  const styleHelpers = ctx.styleHelpers || {};
  const previewOnlyHierarchy = ctx.previewOnlyHierarchy === true;
  const useNormalizedTree = ctx.useNormalizedTree === true;
  const {
    extractGradientInfo = () => null,
    colorToCss = () => null,
    borderToCss = () => null,
    shadowToCss = () => null,
    shouldDisplayBorderRadius = () => false,
    shouldDisplayOpacity = () => false,
    extractBorderInfo = () => null,
    extractTextInfo = () => null,
    describeConstraints = () => null,
    buildFontFamilyStack = null
  } = styleHelpers;

  if (!layer || layer.visible === false) return "";
  const frame = useNormalizedTree
    ? (layer.frame || toFrame(layer.rect))
    : toFrame(layer.rect);
  const abs = useNormalizedTree
    ? (
        layer.absoluteFrame ||
        (frame ? {
          x: parentAbs.x + (frame.x ?? 0),
          y: parentAbs.y + (frame.y ?? 0),
          width: frame.width ?? 0,
          height: frame.height ?? 0
        } : parentAbs)
      )
    : (
        frame ? ({
          x: parentAbs.x + (frame.x ?? 0),
          y: parentAbs.y + (frame.y ?? 0),
          width: frame.width ?? 0,
          height: frame.height ?? 0
        }) : parentAbs
      );

  const styles = ["position:absolute", "box-sizing:border-box"];
  const relativeLeft = frame ? (depth === 0 ? (abs.x - origin.x) : (frame.x ?? 0)) : (depth === 0 ? abs?.x - origin.x : 0);
  const relativeTop = frame ? (depth === 0 ? (abs.y - origin.y) : (frame.y ?? 0)) : (depth === 0 ? abs?.y - origin.y : 0);
  if (Number.isFinite(relativeLeft)) styles.push(`left:${relativeLeft}px`);
  if (Number.isFinite(relativeTop)) styles.push(`top:${relativeTop}px`);
  const widthValue = frame?.width ?? (depth === 0 ? abs?.width : undefined);
  const heightValue = frame?.height ?? (depth === 0 ? abs?.height : undefined);
  if (Number.isFinite(widthValue)) styles.push(`width:${widthValue}px`);
  if (Number.isFinite(heightValue)) styles.push(`height:${heightValue}px`);
  if (!previewOnlyHierarchy && shouldDisplayOpacity(layer.opacity)) styles.push(`opacity:${layer.opacity}`);
  if (layer.rotation) styles.push(`transform:rotate(${layer.rotation}deg)`);
  if (!previewOnlyHierarchy && layer.type === "text") styles.push("overflow:hidden");

  const textInfo = useNormalizedTree
    ? (layer.textContent ? { content: layer.textContent, style: layer.textStyle || {}, ...(layer.textRuns ? { runs: layer.textRuns } : {}) } : null)
    : (layer.type === "text" ? extractTextInfo(layer) : null);
  const imageInfo = useNormalizedTree
    ? (layer.image || null)
    : (extractImageInfo(layer, ctx) || layer.__imageInfo || null);
  const fillInfo = useNormalizedTree
    ? (
        layer.fillColor || layer.fillColorHex || layer.fillColorName
          ? {
              color: layer.fillColor,
              colorHex: layer.fillColorHex,
              colorName: layer.fillColorName,
              display: layer.fillColorName || layer.fillColorHex || layer.fillColor
            }
          : null
      )
    : (styleHelpers.extractFillColor ? styleHelpers.extractFillColor(layer.fills) : null);
  const gradientInfo = useNormalizedTree ? (layer.gradient || null) : extractGradientInfo(layer.fills);
  if (!previewOnlyHierarchy) {
    if (gradientInfo?.css) {
      styles.push(`background:${gradientInfo.css}`);
    } else if (!useNormalizedTree) {
      const fill = (layer.fills || []).find(f => f?.type === "color" && f.color);
      if (fill) {
        const fillColor = colorToCss(fill.color);
        if (fillColor) styles.push(`background:${fillColor}`);
      }
    }
  }

  const border = useNormalizedTree
    ? (layer.borderWidth !== undefined && (layer.borderColor || layer.borderColorName)
        ? `${layer.borderWidth}px solid ${layer.borderColor || layer.borderColorName}`
        : null)
    : borderToCss(layer.borders);
  if (!previewOnlyHierarchy && border) styles.push(`border:${border}`);

  const borderInfo = useNormalizedTree
    ? (
        layer.borderWidth !== undefined || layer.borderColor || layer.borderColorName
          ? {
              width: layer.borderWidth,
              colorHex: layer.borderColor,
              colorName: layer.borderColorName
            }
          : null
      )
    : extractBorderInfo(layer.borders);

  if (!previewOnlyHierarchy && shouldDisplayBorderRadius(layer.borderRadius)) styles.push(`border-radius:${layer.borderRadius}px`);

  const shadow = useNormalizedTree ? (layer.shadow || null) : shadowToCss(layer.shadows);
  if (!previewOnlyHierarchy && shadow) styles.push(`box-shadow:${shadow}`);

  styles.push(`z-index:${zIndexRef.value++}`);

  const generatedId = layer.generatedId || layer.descId || layer.__generatedId || layer.id || layer.sourceId || `layer_${Math.random().toString(36).slice(2)}`;
  const descId = generatedId;
  const dataAttrs = [
    generatedId ? `data-layer-id="${escapeHtml(generatedId)}"` : "",
    layer.id ? `data-layer-original-id="${escapeHtml(layer.id)}"` : "",
    layer.name ? `data-layer-name="${escapeHtml(layer.name)}"` : "",
    descId ? `data-layer-desc-id="${escapeHtml(descId)}"` : ""
  ].filter(Boolean);

  const stylesForCopy = Object.fromEntries(styles.map(s => {
    const idx = s.indexOf(":");
    if (idx === -1) return [s.trim(), ""];
    return [s.slice(0, idx).trim(), s.slice(idx + 1).trim()];
  }));
  dataAttrs.push(`data-layer-style="${escapeHtml(JSON.stringify(stylesForCopy))}"`);

  if (imageInfo) {
    dataAttrs.push(`data-layer-image="${escapeHtml(JSON.stringify(imageInfo))}"`);
  }
  if (gradientInfo) {
    dataAttrs.push(`data-layer-gradient="${escapeHtml(JSON.stringify(gradientInfo))}"`);
  }
  if (textInfo?.runs) {
    dataAttrs.push(`data-layer-text-runs="${escapeHtml(JSON.stringify(textInfo.runs))}"`);
  }

  const contentParts = [];
  if (!previewOnlyHierarchy && imageInfo?.url) {
    contentParts.push(`<img class="layer-image" src="${escapeHtml(imageInfo.url)}" alt="" />`);
  }

  if (!previewOnlyHierarchy && textInfo) {
    const textStyles = [
      "position:absolute",
      "left:0",
      "top:0",
      "width:100%",
      "height:100%",
      "white-space:pre-wrap",
      "display:block",
      "box-sizing:border-box",
      "padding:0",
      "overflow:hidden"
    ];
    if (textInfo.style.fontFamily || textInfo.style.fontPostscriptName) {
      const stack = buildFontFamilyStack
        ? buildFontFamilyStack(textInfo.style)
        : [textInfo.style.fontFamily || textInfo.style.fontPostscriptName];
      const fontStack = (stack || [])
        .map(value => String(value).replace(/'/g, "\\'"))
        .map(value => `'${value}'`)
        .join(", ");
      if (fontStack) textStyles.push(`font-family:${fontStack}`);
    }
    if (Number.isFinite(textInfo.style.fontSize)) textStyles.push(`font-size:${textInfo.style.fontSize}px`);
    if (textInfo.style.fontWeight) textStyles.push(`font-weight:${textInfo.style.fontWeight}`);
    if (textInfo.style.fontStyle) textStyles.push(`font-style:${textInfo.style.fontStyle}`);
    if (Number.isFinite(textInfo.style.lineHeight)) textStyles.push(`line-height:${textInfo.style.lineHeight}px`);
    if (Number.isFinite(textInfo.style.letterSpacing)) textStyles.push(`letter-spacing:${textInfo.style.letterSpacing}px`);
    if (textInfo.style.textAlign) textStyles.push(`text-align:${textInfo.style.textAlign}`);
    if (textInfo.style.color) textStyles.push(`color:${textInfo.style.color}`);

    dataAttrs.push(`data-layer-text-style="${escapeHtml(JSON.stringify(textInfo.style))}"`);
    if (textInfo.content) {
      dataAttrs.push(`data-layer-text="${escapeHtml(textInfo.content)}"`);
    }
    if (textInfo.runs && textInfo.runs.length > 1) {
      const buildRunCss = (runStyle = {}) => {
        const runStyles = [];
        if (runStyle.fontFamily || runStyle.fontPostscriptName) {
          const stack = buildFontFamilyStack
            ? buildFontFamilyStack(runStyle)
            : [runStyle.fontFamily || runStyle.fontPostscriptName];
          const fontStack = (stack || [])
            .map(value => String(value).replace(/'/g, "\\'"))
            .map(value => `'${value}'`)
            .join(", ");
          if (fontStack) runStyles.push(`font-family:${fontStack}`);
        }
        if (Number.isFinite(runStyle.fontSize)) runStyles.push(`font-size:${runStyle.fontSize}px`);
        if (runStyle.fontWeight) runStyles.push(`font-weight:${runStyle.fontWeight}`);
        if (runStyle.fontStyle) runStyles.push(`font-style:${runStyle.fontStyle}`);
        if (Number.isFinite(runStyle.lineHeight)) runStyles.push(`line-height:${runStyle.lineHeight}px`);
        if (Number.isFinite(runStyle.letterSpacing)) runStyles.push(`letter-spacing:${runStyle.letterSpacing}px`);
        if (runStyle.color) runStyles.push(`color:${runStyle.color}`);
        return runStyles.join(";");
      };
      const runContent = textInfo.runs
        .map(run => `<span style="${buildRunCss(run.style)}">${escapeHtml(run.text || "")}</span>`)
        .join("");
      contentParts.push(`<span class="text-content" style="${textStyles.join(";")}">${runContent}</span>`);
    } else {
      contentParts.push(`<span class="text-content" style="${textStyles.join(";")}">${escapeHtml(textInfo.content || "")}</span>`);
    }
  }

  const isFillOnlyChild = (child) => {
    if (!child) return false;
    if (child.type === "text") return false;
    const textChild = child.type === "text" || child.text || child.textContent || (child.textStyles && child.textStyles.length);
    if (textChild) return false;
    const childGradient = extractGradientInfo(child.fills);
    if (childGradient) return false;
    const childBorder = extractBorderInfo(child.borders);
    if (childBorder?.width) return false;
    const childShadow = shadowToCss(child.shadows);
    if (childShadow) return false;
    const childImage = extractImageInfo(child, ctx);
    if (childImage) return false;
    const childFill = styleHelpers.extractFillColor ? styleHelpers.extractFillColor(child.fills) : null;
    if (childFill) return true;
    return Array.isArray(child.fills) && child.fills.some(f => f?.type === "color" && f.color);
  };

  let childLayers = Array.isArray(layer.children)
    ? layer.children
    : (Array.isArray(layer.layers) ? layer.layers : []);
  if (!useNormalizedTree && !previewOnlyHierarchy && imageInfo && childLayers.length) {
    childLayers = childLayers.filter(child => {
      if (!isFillOnlyChild(child)) return true;
      const childFrame = toFrame(child.rect) || child.absoluteFrame || child.frame || null;
      const parentFrame = frame || { x: 0, y: 0, width: abs?.width, height: abs?.height };
      const contained = parentFrame && childFrame
        ? (
            childFrame.x >= 0 &&
            childFrame.y >= 0 &&
            (childFrame.x + (childFrame.width ?? 0)) <= (parentFrame.width ?? Infinity) &&
            (childFrame.y + (childFrame.height ?? 0)) <= (parentFrame.height ?? Infinity)
          )
        : true;
      return !contained;
    });
  }

  const childrenHtml = childLayers.length
    ? childLayers.map(child => renderLayerPreview(child, abs || parentAbs, origin, zIndexRef, ctx, depth + 1)).join("")
    : "";

  const constraintInfo = frame ? describeConstraints(frame, parentAbs) : null;
  const constraintDescription = constraintInfo ? `constraints: ${constraintInfo.entries.join(", ")}` : null;

  const descriptionParts = [];
  if (layer.name) descriptionParts.push(`Name: ${layer.name}`);
  if (layer.type) descriptionParts.push(`Type: ${layer.type}`);
  if (abs) {
    const coords = [abs.x, abs.y, abs.width, abs.height]
      .map(value => Number.isFinite(value) ? Math.round(value * 100) / 100 : value ?? "-")
      .join(",");
    descriptionParts.push(`frame: ${coords}`);
  }
  if (textInfo?.content) {
    const snippet = textInfo.content.length > 80
      ? `${textInfo.content.slice(0, 77)}...`
      : textInfo.content;
    descriptionParts.push(`Text: ${snippet}`);
  }
  if (textInfo?.style) {
    if (textInfo.style.fontFamily) descriptionParts.push(`font: ${textInfo.style.fontFamily}`);
    if (textInfo.style.fontName) descriptionParts.push(`fontName: ${textInfo.style.fontName}`);
    if (textInfo.style.fontSize) descriptionParts.push(`fontSize: ${textInfo.style.fontSize}px`);
    if (textInfo.style.fontWeight) descriptionParts.push(`fontWeight: ${textInfo.style.fontWeight}`);
    if (textInfo.style.lineHeight) {
      const lhValue = textInfo.style.lineHeight;
      const lhDisplay = typeof lhValue === "number" ? `${lhValue}px` : `${lhValue}`;
      descriptionParts.push(`lineHeight: ${lhDisplay}`);
    }
    if (textInfo.style.textAlign) descriptionParts.push(`textAlign: ${textInfo.style.textAlign}`);
    if (textInfo.style.colorName) descriptionParts.push(`colorName: ${textInfo.style.colorName}`);
    if (textInfo.style.color) descriptionParts.push(`color: ${textInfo.style.color}`);
  }
  if (shadow) descriptionParts.push(`shadow=${shadow}`);
  if (shouldDisplayOpacity(layer.opacity)) {
    const opacityDisplay = styleHelpers.formatNumeric
      ? styleHelpers.formatNumeric(layer.opacity)
      : String(layer.opacity);
    descriptionParts.push(`opacity=${opacityDisplay ?? layer.opacity}`);
  }
  if (shouldDisplayBorderRadius(layer.borderRadius)) descriptionParts.push(`borderRadius=${layer.borderRadius}`);
  if (borderInfo?.width !== undefined) descriptionParts.push(`borderWidth=${borderInfo.width}`);
  if (borderInfo?.colorName) {
    descriptionParts.push(`borderColor=${borderInfo.colorName}`);
  } else if (borderInfo?.colorHex) {
    descriptionParts.push(`borderColor=${borderInfo.colorHex}`);
  }
  if (fillInfo?.display) {
    descriptionParts.push(`fillColor=${fillInfo.display}`);
  }
  if (constraintDescription) descriptionParts.push(constraintDescription);
  if (gradientInfo?.description) {
    descriptionParts.push(`gradientColor: ${gradientInfo.description}`);
  }
  if (imageInfo?.assetName) descriptionParts.push(`imageName=${imageInfo.assetName}`);
  if (descriptionParts.length) {
    dataAttrs.push(`data-layer-desc="${escapeHtml(descriptionParts.join(" · "))}"`);
  }
  if (constraintInfo?.map && Object.keys(constraintInfo.map).length) {
    dataAttrs.push(`data-layer-constraints="${escapeHtml(JSON.stringify(constraintInfo.map))}"`);
  }

  const attrString = dataAttrs.join(" ");
  return `<div class="layer layer-${escapeHtml(layer.type || "unknown")}" ${attrString} style="${styles.join(";")}">${contentParts.join("")}${childrenHtml}</div>`;
};

export const renderDesignPreview = (layers, origin, bounds, options = {}) => {
  const zIndexRef = { value: 1 };
  const ctx = {
    assetLookup: options.assetLookup,
    styleHelpers: options.styleHelpers || {},
    previewOnlyHierarchy: options.previewOnlyHierarchy !== false,
    useNormalizedTree: options.useNormalizedTree === true
  };
  const width = Math.max(0, Math.round(bounds.maxX - bounds.minX));
  const height = Math.max(0, Math.round(bounds.maxY - bounds.minY));
  const rootParent = { x: origin.x ?? 0, y: origin.y ?? 0, width, height };
  const backgroundImage = options.backgroundImage || null;
  const backgroundFrame = options.backgroundImageFrame || null;
  let backgroundImageHtml = "";
  if (backgroundImage) {
    const frameX = Number.isFinite(backgroundFrame?.x) ? backgroundFrame.x : 0;
    const frameY = Number.isFinite(backgroundFrame?.y) ? backgroundFrame.y : 0;
    const frameWidth = Number.isFinite(backgroundFrame?.width) ? backgroundFrame.width : width;
    const frameHeight = Number.isFinite(backgroundFrame?.height) ? backgroundFrame.height : height;
    const left = frameX - (origin.x ?? 0);
    const top = frameY - (origin.y ?? 0);
    backgroundImageHtml = `<img class="screen-bg" src="${escapeHtml(backgroundImage)}" alt="" style="left:${left}px;top:${top}px;width:${frameWidth}px;height:auto;" data-frame-height="${frameHeight}" />`;
  }
  const body = (layers || []).map(layer => renderLayerPreview(layer, rootParent, origin, zIndexRef, ctx)).join("");
  const background = options.background ? `background:${options.background};` : "";
  return `<div class="preview"><div class="canvas" style="width:${width}px;height:${height}px;${background}">${backgroundImageHtml}${body}</div></div>`;
};
