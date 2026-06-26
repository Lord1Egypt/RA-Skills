import { extractImageInfo } from "./assets.mjs";

const toFrame = (rect) => rect ? ({
  x: rect.x,
  y: rect.y,
  width: rect.width,
  height: rect.height
}) : null;

const isFiniteNumber = (value) => typeof value === "number" && Number.isFinite(value);

const hasRect = (rect) => rect && [rect.x, rect.y, rect.width, rect.height].every(isFiniteNumber);

const areaOf = (rect) => {
  if (!hasRect(rect)) return null;
  const width = Math.abs(rect.width);
  const height = Math.abs(rect.height);
  return width * height;
};

const framesEqual = (a, b, epsilon = 0.5) => {
  if (!hasRect(a) || !hasRect(b)) return false;
  return Math.abs((a.x ?? 0) - (b.x ?? 0)) <= epsilon &&
    Math.abs((a.y ?? 0) - (b.y ?? 0)) <= epsilon &&
    Math.abs((a.width ?? 0) - (b.width ?? 0)) <= epsilon &&
    Math.abs((a.height ?? 0) - (b.height ?? 0)) <= epsilon;
};

const rectContains = (outer, inner, epsilon = 0) => {
  if (!hasRect(outer) || !hasRect(inner)) return false;
  const eps = Math.max(0, epsilon);
  const innerRight = inner.x + inner.width;
  const innerBottom = inner.y + inner.height;
  const outerRight = outer.x + outer.width;
  const outerBottom = outer.y + outer.height;
  return inner.x >= outer.x - eps &&
    inner.y >= outer.y - eps &&
    innerRight <= outerRight + eps &&
    innerBottom <= outerBottom + eps;
};

const flattenLayers = (
  layers,
  parentOrigin = { x: 0, y: 0 },
  parentKey = null,
  acc = [],
  state = { autoKey: 0, exportId: 0 },
  ctx = {},
  parentFrame = null
) => {
  const {
    describeConstraints = () => null,
    extractTextInfo = () => null,
    extractGradientInfo = () => null,
    extractBorderInfo = () => null,
    extractFillColor = () => null,
    shadowToCss = () => null,
    shouldDisplayBorderRadius = () => false,
    shouldDisplayOpacity = () => false
  } = ctx.styleHelpers || {};

  if (!Array.isArray(layers)) return acc;
  for (const layer of layers) {
    const frame = toFrame(layer.rect);
    const absoluteFrame = frame ? ({
      x: (parentOrigin.x ?? 0) + (frame.x ?? 0),
      y: (parentOrigin.y ?? 0) + (frame.y ?? 0),
      width: frame.width,
      height: frame.height
    }) : null;
    const constraintInfo = describeConstraints(frame, parentFrame);
    const key = layer.id || `__layer_${state.autoKey++}`;
    const generatedId = `layer_${state.exportId++}`;
    const renderIndex = acc.length;
    const textInfo = layer.type === "text" ? extractTextInfo(layer) : null;
    const imageInfo = extractImageInfo(layer, ctx);
    const shadow = shadowToCss(layer.shadows);
    const borderInfo = extractBorderInfo(layer.borders);
    const borderRadius = layer.borderRadius;
    const gradientInfo = extractGradientInfo(layer.fills);
    const fillInfo = extractFillColor(layer.fills);
    const rawHasFill = Array.isArray(layer.fills) && layer.fills.some(fill => fill && (fill.type === "color" || fill.type === "gradient"));
    const lineHeightValue = textInfo?.style?.lineHeight;
    const descId = generatedId;
    const node = {
      __key: key,
      originalIndex: acc.length,
      originalParentKey: parentKey,
      generatedId,
      id: layer.id,
      name: layer.name,
      type: layer.type,
      frame,
      absoluteFrame,
      visible: layer.visible !== false,
      ...(shouldDisplayOpacity(layer.opacity) ? { opacity: layer.opacity } : {}),
      rotation: layer.rotation,
      parentId: null,
      descId,
      renderIndex,
      ...(textInfo ? { textContent: textInfo.content, textStyle: textInfo.style, ...(textInfo.runs ? { textRuns: textInfo.runs } : {}) } : {}),
      ...(imageInfo ? { image: imageInfo } : {}),
      ...(imageInfo?.imgUrl ? { imgUrl: imageInfo.imgUrl } : {}),
      ...(shadow ? { shadow } : {}),
      ...(lineHeightValue !== undefined ? { lineHeight: lineHeightValue } : {}),
      ...(shouldDisplayBorderRadius(borderRadius) ? { borderRadius } : {}),
      ...(borderInfo ? {
        borderWidth: borderInfo.width,
        borderColor: borderInfo.color,
        ...(borderInfo.colorName ? { borderColorName: borderInfo.colorName } : {})
      } : {}),
      ...(fillInfo ? {
        fillColor: fillInfo.color || fillInfo.display,
        ...(fillInfo.colorHex ? { fillColorHex: fillInfo.colorHex } : {}),
        ...(fillInfo.colorName ? { fillColorName: fillInfo.colorName } : {})
      } : {}),
      ...(rawHasFill ? { rawHasFill: true } : {}),
      ...(gradientInfo ? {
        gradient: gradientInfo,
        gradientColor: gradientInfo.description
      } : {}),
      ...(constraintInfo?.map ? { constraints: constraintInfo.map } : {})
    };
    if (layer && typeof layer === "object") {
      Object.defineProperty(layer, "__generatedId", {
        value: generatedId,
        configurable: true,
        enumerable: false,
        writable: false
      });
      if (imageInfo) {
        Object.defineProperty(layer, "__imageInfo", {
          value: imageInfo,
          configurable: true,
          enumerable: false,
          writable: false
        });
      }
    }
    acc.push(node);
    const nextOrigin = absoluteFrame ? { x: absoluteFrame.x ?? parentOrigin.x ?? 0, y: absoluteFrame.y ?? parentOrigin.y ?? 0 } : parentOrigin;
    const nextParentFrame = frame
      ? {
          width: Number.isFinite(frame.width) ? frame.width : parentFrame?.width,
          height: Number.isFinite(frame.height) ? frame.height : parentFrame?.height
        }
      : parentFrame;
    flattenLayers(layer.layers, nextOrigin, key, acc, state, ctx, nextParentFrame);
  }
  return acc;
};

const mergeCoLocatedLayers = (node, epsilon, log = () => {}) => {
  if (!node?.children || !node.children.length) return;
  node.children.forEach(child => mergeCoLocatedLayers(child, epsilon, log));

  const displayName = (layer) => layer?.name || layer?.id || layer?.generatedId || layer?.descId || "unknown";
  const mergedChildren = [];

  const tryMerge = (parent, child) => {
    const parentFrame = parent.absoluteFrame || parent.frame;
    const childFrame = child.absoluteFrame || child.frame;
    const parentHasImage = !!parent.image;
    const hasSingleChild = Array.isArray(parent.children) && parent.children.length === 1;

    const isFillOnly = (node, logPrefix = "", parentImageName = "") => {
      if (!node) return false;
      const hasChildren = Array.isArray(node.children) && node.children.length > 0;
      if (hasChildren) return false;
      const hasText = node.textContent || (node.textStyle && Object.keys(node.textStyle).length);
      const hasImage = !!node.image;
      const hasGradient = !!node.gradient || !!node.gradientColor;
      const hasBorder = node.borderWidth !== undefined || node.borderColor !== undefined || node.borderColorName !== undefined;
      const hasShadow = !!node.shadow;
      const hasFill = node.fillColor || node.fillColorHex || node.fillColorName || node.rawHasFill;
      const fillValues = {
        fillColor: node.fillColor,
        fillColorHex: node.fillColorHex,
        fillColorName: node.fillColorName,
        rawHasFill: node.rawHasFill
      };
      const allowTypes = new Set(["shape", "group"]);
      const result = allowTypes.has(node.type) && !hasText && !hasImage && !hasGradient && !hasBorder && !hasShadow && !!hasFill;
      if (logPrefix) {
        const imageName = node.image?.assetName || node.image?.url || node.imageName || node.name || "";
        const fillValue = node.fillColorName || node.fillColorHex || node.fillColor;
        const parentImg = parentImageName || "";
        log(`${logPrefix} fillOnly=${result} type=${node.type} hasChildren=${hasChildren} hasText=${!!hasText} hasImage=${hasImage} hasGradient=${hasGradient} hasBorder=${hasBorder} hasShadow=${hasShadow} hasFill=${hasFill} fillValue=${fillValue ?? ""} fillFields=${JSON.stringify(fillValues)} imageName=${imageName} parentImage=${parentImg}`);
      }
      return result;
    };

    if (parentHasImage && hasSingleChild) {
      if (isFillOnly(child, `[merge][${displayName(child)}][image-single-child]`, parent.image?.assetName || parent.image?.url || parent.imageName || parent.name || "")) {
        log(`[merge] Removed the only fill child under image layer ${displayName(child)} (parent contains image)`);
        return true;
      }
      log(`[merge][${displayName(child)}][image-single-child] skip (not fill-only or has extra properties)`);
    }

    if (parentHasImage && isFillOnly(child, `[merge][${displayName(child)}][image-with-fill-child]`, parent.image?.assetName || parent.image?.url || parent.imageName || parent.name || "")) {
      const contained = rectContains(parentFrame, childFrame, epsilon) || framesEqual(parentFrame, childFrame, epsilon);
      if (contained) {
        log(`[merge] Removed fill child ${displayName(child)} under image parent`);
        return true;
      }
    }

    if (!framesEqual(parentFrame, childFrame, epsilon)) return false;
    if (child.type === "text") return false;
    if (child.children && child.children.length) return false;

    if (parentHasImage && isFillOnly(child, `[merge][${displayName(child)}]`, parent.image?.assetName || parent.image?.url || parent.imageName || parent.name || "")) {
      log(`[merge] Removed single fill child ${displayName(child)} under image parent`);
      return true;
    }

    const conflicts = [];
    const mergedProps = [];
    const applyProp = (key, value, label = key) => {
      if (value === undefined || value === null) return;
      if (parent[key] === undefined || parent[key] === value) {
        if (parent[key] === undefined) {
          parent[key] = value;
          mergedProps.push(label);
        }
        return;
      }
      conflicts.push(label);
    };

    const normalizeToken = (value) => {
      if (value === undefined || value === null) return "";
      if (typeof value === "string") return value.trim().toLowerCase();
      return String(value).trim().toLowerCase();
    };
    const getFillValueToken = (node) => (
      normalizeToken(node.fillColorHex) ||
      normalizeToken(node.fillColor)
    );
    const getFillNameToken = (node) => normalizeToken(node.fillColorName);
    const parentFillValueToken = getFillValueToken(parent);
    const childFillValueToken = getFillValueToken(child);
    const parentFillNameToken = getFillNameToken(parent);
    const childFillNameToken = getFillNameToken(child);
    const parentHasFillValue = !!(parent.fillColorHex || parent.fillColor);
    const childHasFillValue = !!(child.fillColorHex || child.fillColor);
    const parentHasFillName = !!parent.fillColorName;
    const childHasFillName = !!child.fillColorName;
    const sameFillValue = parentHasFillValue && childHasFillValue && parentFillValueToken && parentFillValueToken === childFillValueToken;
    const sameFillName = parentHasFillName && childHasFillName && parentFillNameToken && parentFillNameToken === childFillNameToken;

    if (childHasFillValue) {
      if (!parentHasFillValue) {
        if (child.fillColorHex !== undefined) applyProp("fillColorHex", child.fillColorHex, "fillColorHex");
        if (child.fillColor !== undefined) applyProp("fillColor", child.fillColor, "fillColor");
      } else if (!sameFillValue) {
        conflicts.push("fillColorHex", "fillColor");
      }
    }
    if (childHasFillName) {
      if (!parentHasFillName) {
        if (child.fillColorName !== undefined) applyProp("fillColorName", child.fillColorName, "fillColorName");
      } else if (!sameFillName) {
        conflicts.push("fillColorName");
      }
    }

    applyProp("gradient", child.gradient, "gradient");
    applyProp("gradientColor", child.gradientColor, "gradientColor");
    applyProp("shadow", child.shadow, "shadow");
    applyProp("opacity", child.opacity, "opacity");
    applyProp("borderRadius", child.borderRadius, "borderRadius");
    applyProp("borderWidth", child.borderWidth, "borderWidth");
    applyProp("borderColorName", child.borderColorName, "borderColorName");
    applyProp("borderColor", child.borderColor, "borderColor");
    if (child.image) {
      if (!parent.image) {
        parent.image = child.image;
        mergedProps.push("image");
      } else {
        const parentImageName = parent.image?.assetName || parent.image?.url || parent.imageName || parent.name || "";
        const childImageName = child.image?.assetName || child.image?.url || child.imageName || child.name || "";
        if (parentImageName !== childImageName) {
          conflicts.push("image");
        }
      }
    }

    if (conflicts.length) {
      log(`[merge] Skipped merge ${displayName(child)} -> ${displayName(parent)} due to property conflicts: ${conflicts.join(", ")}`);
      return false;
    }

    if (mergedProps.length) {
      log(`[merge] Merged ${displayName(child)} -> ${displayName(parent)} with properties: ${mergedProps.join(", ")}`);
    } else {
      log(`[merge] Removed same-size child ${displayName(child)} (no mergeable properties)`);
    }
    return true;
  };

  for (const child of node.children) {
    const merged = tryMerge(node, child);
    if (!merged) {
      mergedChildren.push(child);
    }
  }
  node.children = mergedChildren;
  if (!node.children.length) delete node.children;
};

export const buildLayerTree = (layers, options = {}) => {
  const epsilon = options.epsilon ?? 0.5;
  const debug = options.debug ?? false;
  const verbose = options.verbose === true;
  const log = options.log || (() => {});
  const styleHelpers = options.styleHelpers || {};
  const describeConstraints = styleHelpers.describeConstraints || (() => null);
  const debugLog = (...args) => { if (debug) log("[buildLayerTree]", ...args); };
  const mergeLog = (...args) => {
    const hasWarning = args.some(arg => typeof arg === "string" && arg.includes("⚠️"));
    if (hasWarning || verbose) {
      log(...args);
    }
  };

  const ctx = { assetLookup: options.assetLookup, styleHelpers };
  const rootFrame = options.rootFrame && typeof options.rootFrame === "object"
    ? {
        width: Number.isFinite(options.rootFrame.width) ? options.rootFrame.width : undefined,
        height: Number.isFinite(options.rootFrame.height) ? options.rootFrame.height : undefined
      }
    : null;
  const flat = flattenLayers(layers || [], { x: 0, y: 0 }, null, [], { autoKey: 0, exportId: 0 }, ctx, rootFrame);
  if (!flat.length) return [];

  const spatial = [];
  const nonSpatial = [];
  for (const node of flat) {
    node.children = [];
    const area = areaOf(node.absoluteFrame);
    if (area !== null) {
      node.__area = area;
      spatial.push(node);
    } else {
      nonSpatial.push(node);
    }
  }

  spatial.sort((a, b) => {
    if (b.__area !== a.__area) return b.__area - a.__area;
    return a.originalIndex - b.originalIndex;
  });

  debugLog(`flattened=${flat.length} spatial=${spatial.length} nonSpatial=${nonSpatial.length}`);

  const roots = [];
  const lookup = new Map();

  const registerNode = (node, parent) => {
    if (parent) {
      node.parentId = parent.id ?? null;
      parent.children.push(node);
      debugLog(`attach ${node.name || node.id || node.__key} -> ${parent.name || parent.id || parent.__key}`);
    } else {
      node.parentId = null;
      roots.push(node);
      debugLog(`new root ${node.name || node.id || node.__key}`);
    }
    lookup.set(node.__key, node);
  };

  const findBestParent = (target) => {
    if (!hasRect(target.absoluteFrame)) return null;
    let best = null;
    const visit = (node) => {
      if (!hasRect(node.absoluteFrame)) return;
      if (!rectContains(node.absoluteFrame, target.absoluteFrame, epsilon)) return;
      if (!best || (node.__area ?? Infinity) < (best.__area ?? Infinity)) {
        best = node;
      }
      for (const child of node.children) {
        visit(child);
      }
    };
    for (const root of roots) {
      visit(root);
    }
    if (best) {
      debugLog(`parent candidate for ${target.name || target.id || target.__key}: ${best.name || best.id || best.__key}`);
    } else {
      debugLog(`no parent for ${target.name || target.id || target.__key}`);
    }
    return best;
  };

  for (const node of spatial) {
    const parent = findBestParent(node);
    registerNode(node, parent);
  }

  nonSpatial.sort((a, b) => a.originalIndex - b.originalIndex);
  for (const node of nonSpatial) {
    const parent = node.originalParentKey ? lookup.get(node.originalParentKey) : null;
    registerNode(node, parent || null);
  }

  const getOrder = (node) => Number.isFinite(node.renderIndex)
    ? node.renderIndex
    : (Number.isFinite(node.originalIndex) ? node.originalIndex : Number.POSITIVE_INFINITY);

  const sortChildrenByOrder = (nodes) => {
    nodes.sort((a, b) => getOrder(a) - getOrder(b));
    for (const node of nodes) {
      if (node.children && node.children.length) {
        sortChildrenByOrder(node.children);
      } else {
        delete node.children;
      }
    }
  };

  sortChildrenByOrder(roots);

  roots.forEach(root => mergeCoLocatedLayers(root, epsilon, mergeLog));

  const recomputeNodeGeometry = (node, parentAbsoluteFrame = null, parentConstraintFrame = rootFrame) => {
    if (!node) return;

    if (hasRect(node.absoluteFrame)) {
      if (hasRect(parentAbsoluteFrame)) {
        node.frame = {
          x: node.absoluteFrame.x - parentAbsoluteFrame.x,
          y: node.absoluteFrame.y - parentAbsoluteFrame.y,
          width: node.absoluteFrame.width,
          height: node.absoluteFrame.height
        };
      } else {
        node.frame = {
          x: node.absoluteFrame.x,
          y: node.absoluteFrame.y,
          width: node.absoluteFrame.width,
          height: node.absoluteFrame.height
        };
      }
    }

    const currentConstraintFrame = hasRect(parentAbsoluteFrame)
      ? { width: parentAbsoluteFrame.width, height: parentAbsoluteFrame.height }
      : parentConstraintFrame;
    const constraintInfo = node.frame ? describeConstraints(node.frame, currentConstraintFrame) : null;
    if (constraintInfo?.map && Object.keys(constraintInfo.map).length) {
      node.constraints = constraintInfo.map;
    } else {
      delete node.constraints;
    }

    if (node.children && node.children.length) {
      for (const child of node.children) {
        recomputeNodeGeometry(child, node.absoluteFrame, {
          width: Number.isFinite(node.frame?.width) ? node.frame.width : currentConstraintFrame?.width,
          height: Number.isFinite(node.frame?.height) ? node.frame.height : currentConstraintFrame?.height
        });
      }
    }
  };

  roots.forEach(root => recomputeNodeGeometry(root, null, rootFrame));

  const cleanup = (node) => {
    delete node.__key;
    delete node.__area;
    delete node.originalIndex;
    delete node.originalParentKey;
    if (node.children) {
      node.children.forEach(cleanup);
    }
    delete node.rawHasFill;
  };
  roots.forEach(cleanup);

  return roots;
};

export const computeBounds = (nodes) => {
  const bounds = { minX: Infinity, minY: Infinity, maxX: -Infinity, maxY: -Infinity };
  const visit = (node) => {
    if (node?.absoluteFrame) {
      const { x = 0, y = 0, width = 0, height = 0 } = node.absoluteFrame;
      bounds.minX = Math.min(bounds.minX, x);
      bounds.minY = Math.min(bounds.minY, y);
      bounds.maxX = Math.max(bounds.maxX, x + width);
      bounds.maxY = Math.max(bounds.maxY, y + height);
    }
    (node?.children || []).forEach(visit);
  };
  nodes.forEach(visit);
  if (!Number.isFinite(bounds.minX)) {
    return { minX: 0, minY: 0, maxX: 0, maxY: 0 };
  }
  return bounds;
};

export { toFrame };
