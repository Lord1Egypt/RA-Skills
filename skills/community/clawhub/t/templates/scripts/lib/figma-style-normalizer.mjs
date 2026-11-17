const REQUIRED_FIELDS = [
  'visible',
  'absoluteBoundingBox',
  'absoluteRenderBounds',
  'relativeTransform',
  'clipsContent',
  'constraints',
  'layoutSizingHorizontal',
  'layoutSizingVertical',
  'layoutMode',
  'primaryAxisSizingMode',
  'counterAxisSizingMode',
  'primaryAxisAlignItems',
  'counterAxisAlignItems',
  'itemSpacing',
  'counterAxisSpacing',
  'paddingTop',
  'paddingRight',
  'paddingBottom',
  'paddingLeft',
  'layoutWrap',
  'characters',
  'style',
  'fills',
  'strokes',
  'background',
  'backgroundColor',
  'opacity',
  'blendMode',
  'strokeWeight',
  'strokeAlign',
  'strokeCap',
  'strokeJoin',
  'dashPattern',
  'cornerRadius',
  'rectangleCornerRadii',
  'effects',
  'componentId',
  'componentKey',
  'componentName',
  'mainComponent',
  'variantProperties',
  'componentProperties',
  'overrides',
  'exposedInstances',
];

function clamp255(value) {
  return Math.max(0, Math.min(255, Math.round(value * 255)));
}

function px(value) {
  return typeof value === 'number' && Number.isFinite(value) ? `${value}px` : null;
}

function firstVisibleSolidPaint(paints) {
  if (!Array.isArray(paints)) {
    return null;
  }
  return paints.find((paint) => paint?.type === 'SOLID' && paint.visible !== false && paint.color) ?? null;
}

export function normalizePaintColor(color) {
  if (!color) {
    return null;
  }
  const a = typeof color.a === 'number' ? color.a : 1;
  const r = clamp255(color.r);
  const g = clamp255(color.g);
  const b = clamp255(color.b);
  return {
    figma: {
      r: color.r,
      g: color.g,
      b: color.b,
      a,
    },
    css: `rgba(${r}, ${g}, ${b}, ${Number(a.toFixed(3))})`,
    hex: `#${[r, g, b].map((part) => part.toString(16).padStart(2, '0').toUpperCase()).join('')}`,
  };
}

function normalizePaint(paint) {
  if (!paint) {
    return null;
  }
  return {
    ...paint,
    normalizedColor: normalizePaintColor({
      ...(paint.color ?? {}),
      a: paint.opacity ?? paint.color?.a ?? 1,
    }),
  };
}

function normalizeLineHeight(node, warnings) {
  const style = node.style ?? {};
  if (style.lineHeightUnit === 'AUTO') {
    warnings.push(`line_height_auto:${node.id ?? 'unknown'}`);
    return null;
  }
  if (typeof style.lineHeightPx === 'number') {
    return `${style.lineHeightPx}px`;
  }
  if (typeof style.lineHeightPercentFontSize === 'number') {
    return `${style.lineHeightPercentFontSize}%`;
  }
  return null;
}

function styleRanges(node) {
  const overrides = Array.isArray(node.characterStyleOverrides) ? node.characterStyleOverrides : [];
  const table = node.styleOverrideTable ?? {};
  if (overrides.length === 0) {
    return [];
  }

  const ranges = [];
  let start = 0;
  let current = overrides[0];
  for (let index = 1; index <= overrides.length; index += 1) {
    if (overrides[index] !== current) {
      ranges.push({
        start,
        end: index,
        styleId: current,
        style: current === 0 ? node.style ?? null : table[current] ?? null,
      });
      start = index;
      current = overrides[index];
    }
  }
  return ranges;
}

function boxShadowHint(effect) {
  if (!effect || effect.visible === false || effect.type !== 'DROP_SHADOW') {
    return null;
  }
  const color = normalizePaintColor(effect.color);
  return `${effect.offset?.x ?? 0}px ${effect.offset?.y ?? 0}px ${effect.radius ?? 0}px ${effect.spread ?? 0}px ${color?.css ?? 'rgba(0, 0, 0, 0)'}`;
}

function borderHint(node) {
  const stroke = firstVisibleSolidPaint(node.strokes);
  if (!stroke || typeof node.strokeWeight !== 'number') {
    return null;
  }
  const color = normalizePaintColor(stroke.color);
  return `${node.strokeWeight}px solid ${color?.css ?? 'transparent'}`;
}

function normalizeFlexDirection(layoutMode) {
  if (layoutMode === 'HORIZONTAL') {
    return 'row';
  }
  if (layoutMode === 'VERTICAL') {
    return 'column';
  }
  return null;
}

function normalizeAlignItems(value) {
  if (value === 'CENTER') {
    return 'center';
  }
  if (value === 'MIN') {
    return 'flex-start';
  }
  if (value === 'MAX') {
    return 'flex-end';
  }
  if (value === 'SPACE_BETWEEN') {
    return 'space-between';
  }
  return null;
}

function normalizeJustifyContent(value) {
  return normalizeAlignItems(value);
}

function inferSpacingForNode(node, contextTree) {
  const box = node.absoluteBoundingBox;
  if (!box || !Array.isArray(contextTree?.siblings)) {
    return null;
  }
  const after = contextTree.siblings
    .filter((sibling) => sibling.id !== node.id && sibling.absoluteBoundingBox)
    .map((sibling) => sibling.absoluteBoundingBox)
    .filter((siblingBox) => siblingBox.y >= box.y + box.height)
    .sort((a, b) => a.y - b.y)[0];
  if (!after) {
    return null;
  }
  return {
    afterY: after.y - (box.y + box.height),
  };
}

function collectRawFields(node) {
  const raw = {
    id: node.id ?? null,
    name: node.name ?? null,
    type: node.type ?? null,
  };
  for (const field of REQUIRED_FIELDS) {
    raw[field] = node[field] ?? null;
  }
  raw.styleRanges = styleRanges(node);
  return raw;
}

function collectMissingFields(node) {
  const missing = [];
  for (const field of REQUIRED_FIELDS) {
    if (node[field] === undefined || node[field] === null) {
      missing.push(`${node.id ?? 'unknown'}.${field}`);
    }
  }
  return missing;
}

function normalizeNode(node, contextTree, globalWarnings) {
  const nodeWarnings = [];
  if (!node.id || !node.name || !node.type) {
    nodeWarnings.push('node_malformed');
  }

  const box = node.absoluteBoundingBox ?? {};
  const backgroundPaint = firstVisibleSolidPaint(node.fills) ?? (node.backgroundColor ? { color: node.backgroundColor } : null);
  const textPaint = node.type === 'TEXT' ? firstVisibleSolidPaint(node.fills) : null;
  const firstShadow = Array.isArray(node.effects) ? node.effects.map((effect) => boxShadowHint(effect)).find(Boolean) ?? null : null;
  const style = node.style ?? {};
  const lineHeight = normalizeLineHeight(node, globalWarnings);
  const inferredSpacing = inferSpacingForNode(node, contextTree);

  return {
    id: node.id ?? null,
    name: node.name ?? null,
    type: node.type ?? null,
    raw: collectRawFields(node),
    normalized: {
      x: px(box.x),
      y: px(box.y),
      width: px(box.width),
      height: px(box.height),
      minWidth: px(node.minWidth),
      maxWidth: px(node.maxWidth),
      minHeight: px(node.minHeight),
      maxHeight: px(node.maxHeight),
      display: node.layoutMode ? 'flex' : null,
      flexDirection: normalizeFlexDirection(node.layoutMode),
      alignItems: normalizeAlignItems(node.counterAxisAlignItems),
      justifyContent: normalizeJustifyContent(node.primaryAxisAlignItems),
      gap: px(node.itemSpacing),
      counterAxisSpacing: px(node.counterAxisSpacing),
      padding: [node.paddingTop, node.paddingRight, node.paddingBottom, node.paddingLeft].every((value) => typeof value === 'number')
        ? `${node.paddingTop}px ${node.paddingRight}px ${node.paddingBottom}px ${node.paddingLeft}px`
        : null,
      paddingTop: px(node.paddingTop),
      paddingRight: px(node.paddingRight),
      paddingBottom: px(node.paddingBottom),
      paddingLeft: px(node.paddingLeft),
      inferredSpacing,
      fontFamily: style.fontFamily ?? null,
      fontStyle: style.fontStyle ?? null,
      fontWeight: style.fontWeight ?? null,
      fontSize: px(style.fontSize),
      lineHeight,
      letterSpacing: typeof style.letterSpacing === 'number' ? `${style.letterSpacing}px` : null,
      textAlignHorizontal: style.textAlignHorizontal ?? null,
      textAlignVertical: style.textAlignVertical ?? null,
      textCase: style.textCase ?? null,
      textDecoration: style.textDecoration ?? null,
      color: textPaint ? normalizePaintColor(textPaint.color) : null,
      backgroundColor: backgroundPaint ? normalizePaintColor(backgroundPaint.color) : null,
      opacity: node.opacity ?? null,
      blendMode: node.blendMode ?? null,
      border: borderHint(node),
      borderRadius: px(node.cornerRadius),
      rectangleCornerRadii: Array.isArray(node.rectangleCornerRadii)
        ? node.rectangleCornerRadii.map((value) => px(value))
        : null,
      boxShadowHint: firstShadow,
      blurHint: Array.isArray(node.effects)
        ? node.effects.find((effect) => effect?.type?.includes('BLUR') && effect.visible !== false) ?? null
        : null,
      fills: Array.isArray(node.fills) ? node.fills.map((paint) => normalizePaint(paint)) : null,
      strokes: Array.isArray(node.strokes) ? node.strokes.map((paint) => normalizePaint(paint)) : null,
      componentId: node.componentId ?? null,
      componentKey: node.componentKey ?? null,
      componentName: node.componentName ?? node.name ?? null,
      mainComponent: node.mainComponent ?? null,
      variantProperties: node.variantProperties ?? null,
      componentProperties: node.componentProperties ?? null,
      overrides: node.overrides ?? null,
      exposedInstances: node.exposedInstances ?? null,
    },
    warnings: nodeWarnings,
  };
}

export function normalizeDesignProperties({ nodes, contextTree }) {
  const warnings = [];
  const normalizedNodes = (nodes ?? []).map((node) => normalizeNode(node, contextTree, warnings));
  const missingFields = (nodes ?? []).flatMap((node) => collectMissingFields(node));
  return {
    schemaVersion: 'figma-design-properties/v1',
    nodes: normalizedNodes,
    warnings: [...new Set(warnings)],
    missingFields,
  };
}

function selectorForNode(node) {
  const safeName = String(node.name ?? node.id ?? 'node')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
  return `.figma-${safeName || 'node'}-${String(node.id ?? 'unknown').replace(/[^a-z0-9]+/gi, '-')}`;
}

function addDeclaration(lines, property, value) {
  if (value !== null && value !== undefined) {
    lines.push(`  ${property}: ${value};`);
  }
}

export function buildCssHints(designProperties) {
  const blocks = [];
  for (const node of designProperties.nodes ?? []) {
    const normalized = node.normalized ?? {};
    const lines = [ `${selectorForNode(node)} {` ];
    addDeclaration(lines, 'font-family', normalized.fontFamily);
    addDeclaration(lines, 'font-size', normalized.fontSize);
    addDeclaration(lines, 'font-weight', normalized.fontWeight);
    if (normalized.lineHeight) {
      addDeclaration(lines, 'line-height', normalized.lineHeight);
    } else if (node.type === 'TEXT') {
      lines.push('  /* line-height is AUTO in Figma; no deterministic CSS hint emitted */');
    }
    addDeclaration(lines, 'letter-spacing', normalized.letterSpacing);
    addDeclaration(lines, 'color', normalized.color?.css);
    addDeclaration(lines, 'background-color', normalized.backgroundColor?.css);
    addDeclaration(lines, 'border', normalized.border);
    addDeclaration(lines, 'border-radius', normalized.borderRadius);
    addDeclaration(lines, 'box-shadow', normalized.boxShadowHint);
    addDeclaration(lines, 'display', normalized.display);
    addDeclaration(lines, 'flex-direction', normalized.flexDirection);
    addDeclaration(lines, 'align-items', normalized.alignItems);
    addDeclaration(lines, 'justify-content', normalized.justifyContent);
    addDeclaration(lines, 'gap', normalized.gap);
    addDeclaration(lines, 'padding', normalized.padding);
    addDeclaration(lines, 'width', normalized.width);
    addDeclaration(lines, 'height', normalized.height);
    if (normalized.inferredSpacing?.afterY !== undefined) {
      lines.push('  /* inferred from sibling positions, not a native Figma margin field */');
      lines.push(`  margin-bottom: ${normalized.inferredSpacing.afterY}px;`);
    }
    lines.push('}');
    blocks.push(lines.join('\n'));
  }
  return `${blocks.join('\n\n')}\n`;
}
