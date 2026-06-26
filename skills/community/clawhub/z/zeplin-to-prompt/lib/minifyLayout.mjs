const isFiniteNumber = (value) => typeof value === "number" && Number.isFinite(value);

const roundNumber = (value, precision = 2) => {
  if (!isFiniteNumber(value)) return undefined;
  const factor = 10 ** precision;
  const rounded = Math.round(value * factor) / factor;
  return Object.is(rounded, -0) ? 0 : rounded;
};

const toFrameArray = (frame, precision = 2) => {
  if (!frame) return undefined;
  const values = [frame.x, frame.y, frame.width, frame.height].map(value => roundNumber(value, precision));
  if (values.some(value => value === undefined)) return undefined;
  return values;
};

const normalizeColor = (value) => {
  if (!value || typeof value !== "string") return value;
  return value.replace(/\s+/g, "").toLowerCase();
};

const createIndexer = (prefix) => {
  const map = new Map();
  const dict = {};
  const getId = (value) => {
    if (value === undefined || value === null || value === "") return null;
    const key = JSON.stringify(value);
    let id = map.get(key);
    if (!id) {
      id = `${prefix}${map.size + 1}`;
      map.set(key, id);
      dict[id] = value;
    }
    return id;
  };
  return { dict, getId };
};

const buildFontEntry = (style, precision = 2) => {
  if (!style) return null;
  const family = style.fontFamily || style.fontPostscriptName || style.fontName || null;
  const name = style.fontName || style.fontKey || null;
  const size = isFiniteNumber(style.fontSize) ? roundNumber(style.fontSize, precision) : (style.fontSize ?? null);
  const weight = style.fontWeight ?? null;
  const lineHeight = isFiniteNumber(style.lineHeight) ? roundNumber(style.lineHeight, precision) : (style.lineHeight ?? null);
  const entry = [family, name, size, weight, lineHeight];
  while (entry.length && (entry[entry.length - 1] === null || entry[entry.length - 1] === "")) {
    entry.pop();
  }
  return entry.length ? entry : null;
};

const buildColorValue = (style) => {
  if (!style) return null;
  const colorValue = style.colorHex || style.color || style.colorName;
  return normalizeColor(colorValue) || null;
};

const buildImageValue = (node) => {
  if (!node?.image) return null;
  return node.image.assetName || node.image.url || node.image.originalUrl || null;
};

const typeMap = new Map([
  ["group", "g"],
  ["text", "t"],
  ["shape", "s"],
  ["image", "i"],
  ["bitmap", "i"],
  ["symbol", "g"]
]);

export const minifyLayerTree = (tree, options = {}) => {
  const { precision = 2, bounds = null } = options;
  const fontIndex = createIndexer("f");
  const colorIndex = createIndexer("c");
  const imageIndex = createIndexer("i");

  const minifyNode = (node) => {
    if (!node) return null;
    const item = {};
    const rawType = node.image ? "image" : node.type;
    item.t = typeMap.get(rawType) || rawType || "u";

    const frame = toFrameArray(node.frame || node.absoluteFrame, precision);
    if (frame) item.f = frame;

    if (typeof node.textContent === "string" && node.textContent.length) {
      item.x = node.textContent;
    }

    if (node.textStyle) {
      const fontEntry = buildFontEntry(node.textStyle, precision);
      const fontId = fontEntry ? fontIndex.getId(fontEntry) : null;
      if (fontId) item.fn = fontId;

      const colorValue = buildColorValue(node.textStyle);
      const colorId = colorValue ? colorIndex.getId(colorValue) : null;
      if (colorId) item.cl = colorId;
    }

    if (Array.isArray(node.textRuns) && node.textRuns.length > 1) {
      item.ru = node.textRuns.map(run => {
        const runItem = { x: run.text };
        const fontEntry = buildFontEntry(run.style, precision);
        const fontId = fontEntry ? fontIndex.getId(fontEntry) : null;
        if (fontId) runItem.fn = fontId;

        const colorValue = buildColorValue(run.style);
        const colorId = colorValue ? colorIndex.getId(colorValue) : null;
        if (colorId) runItem.cl = colorId;
        return runItem;
      });
    }

    const imageValue = buildImageValue(node);
    const imageId = imageValue ? imageIndex.getId(imageValue) : null;
    if (imageId) item.i = imageId;

    if (Array.isArray(node.children) && node.children.length) {
      const children = node.children.map(minifyNode).filter(Boolean);
      if (children.length) item.c = children;
    }

    return item;
  };

  const roots = Array.isArray(tree) ? tree : [];
  let root;
  if (roots.length === 1) {
    root = minifyNode(roots[0]);
  } else {
    const frame = bounds
      ? {
          x: bounds.minX,
          y: bounds.minY,
          width: bounds.maxX - bounds.minX,
          height: bounds.maxY - bounds.minY
        }
      : null;
    const rootFrame = toFrameArray(frame, precision);
    root = {
      t: "g",
      ...(rootFrame ? { f: rootFrame } : {}),
      c: roots.map(minifyNode).filter(Boolean)
    };
  }

  return {
    v: 1,
    dict: {
      f: fontIndex.dict,
      c: colorIndex.dict,
      i: imageIndex.dict
    },
    root
  };
};
