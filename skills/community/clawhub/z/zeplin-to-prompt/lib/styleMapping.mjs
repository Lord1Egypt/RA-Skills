import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, "..");

const toNumberChannel = (value) => {
  if (typeof value !== "number" || Number.isNaN(value)) return 0;
  if (value > 1) return Math.round(Math.max(0, Math.min(255, value)));
  return Math.round(Math.max(0, Math.min(255, value * 255)));
};

const toHex = (channel) => channel.toString(16).padStart(2, "0");

const colorObjectToHex = (color) => {
  if (!color) return null;
  const r = toNumberChannel(color.r ?? color.red ?? 0);
  const g = toNumberChannel(color.g ?? color.green ?? 0);
  const b = toNumberChannel(color.b ?? color.blue ?? 0);
  const alphaRaw = color.a ?? color.alpha;
  let alpha = 1;
  if (typeof alphaRaw === "number" && !Number.isNaN(alphaRaw)) {
    alpha = alphaRaw > 1 ? Math.max(0, Math.min(1, alphaRaw / 255)) : Math.max(0, Math.min(1, alphaRaw));
  }
  const base = `#${toHex(r)}${toHex(g)}${toHex(b)}`;
  if (alpha >= 0.999) return base.toLowerCase();
  return `${base}${toHex(Math.round(alpha * 255))}`.toLowerCase();
};

const colorComponent = (value, fallback = 0) => {
  if (typeof value === "number" && !Number.isNaN(value)) return value;
  return fallback;
};

const colorToCss = (color) => {
  if (!color) return null;
  const r = toNumberChannel(color.r ?? color.red);
  const g = toNumberChannel(color.g ?? color.green);
  const b = toNumberChannel(color.b ?? color.blue);
  let a = colorComponent(color.a ?? color.alpha, 1);
  if (a > 1) a = a / 255;
  if (a < 0) a = 0;
  if (a > 1) a = 1;
  return `rgba(${r}, ${g}, ${b}, ${a})`;
};

const borderToCss = (borders = []) => {
  const border = Array.isArray(borders)
    ? borders.find(b => b?.fill?.color && Number.isFinite(b.thickness))
    : null;
  if (!border) return null;
  const color = colorToCss(border.fill.color);
  if (!color) return null;
  return `${border.thickness}px solid ${color}`;
};

const shadowToCss = (shadows = []) => {
  const shadow = Array.isArray(shadows)
    ? shadows.find(s => s?.color)
    : null;
  if (!shadow) return null;
  const color = colorToCss(shadow.color);
  if (!color) return null;
  const x = shadow.offsetX ?? shadow.x ?? 0;
  const y = shadow.offsetY ?? shadow.y ?? 0;
  const blur = shadow.blurRadius ?? shadow.blur ?? 0;
  const spread = shadow.spread ?? 0;
  return `${x}px ${y}px ${blur}px ${spread}px ${color}`;
};

const formatNumeric = (value) => {
  if (!Number.isFinite(value)) return null;
  if (Math.abs(value - Math.round(value)) < 1e-6) return String(Math.round(value));
  const precision = Math.abs(value) >= 1 ? 2 : 3;
  return parseFloat(value.toFixed(precision)).toString();
};

const toPercentString = (value) => {
  if (!Number.isFinite(value)) return null;
  const raw = value > 1 ? value : value * 100;
  const formatted = formatNumeric(raw);
  return formatted == null ? null : `${formatted}%`;
};

const describeConstraints = (frame, parentFrame) => {
  if (!frame) return null;
  const entries = [];
  const map = {};
  const roundValue = (value) => {
    if (!Number.isFinite(value)) return null;
    const rounded = Math.round(value * 1000) / 1000;
    return Math.abs(rounded) < 1e-6 ? 0 : rounded;
  };
  const pushMetric = (key, value) => {
    const rounded = roundValue(value);
    if (rounded === null) return;
    const display = formatNumeric(rounded);
    if (display == null) return;
    entries.push(`${key}=${display}`);
    map[key] = rounded;
  };

  pushMetric("top", frame.y);
  pushMetric("left", frame.x);

  const parentWidth = Number.isFinite(parentFrame?.width) ? parentFrame.width : null;
  const parentHeight = Number.isFinite(parentFrame?.height) ? parentFrame.height : null;

  if (parentHeight != null && Number.isFinite(frame.height)) {
    pushMetric("bottom", parentHeight - (frame.y ?? 0) - (frame.height ?? 0));
  }

  if (parentWidth != null && Number.isFinite(frame.width)) {
    pushMetric("right", parentWidth - (frame.x ?? 0) - (frame.width ?? 0));
  }

  const centerTolerance = 0.5;
  if (parentWidth != null && Number.isFinite(frame.width) && Number.isFinite(frame.x)) {
    const childCenterX = frame.x + frame.width / 2;
    const parentCenterX = parentWidth / 2;
    if (Number.isFinite(childCenterX) && Math.abs(childCenterX - parentCenterX) <= centerTolerance) {
      entries.push("centerX=super.centerX");
      map.centerX = "super.centerX";
    }
  }

  if (parentHeight != null && Number.isFinite(frame.height) && Number.isFinite(frame.y)) {
    const childCenterY = frame.y + frame.height / 2;
    const parentCenterY = parentHeight / 2;
    if (Number.isFinite(childCenterY) && Math.abs(childCenterY - parentCenterY) <= centerTolerance) {
      entries.push("centerY=super.centerY");
      map.centerY = "super.centerY";
    }
  }

  if (!entries.length) return null;
  return { entries, map };
};

const shouldDisplayBorderRadius = (value) => {
  if (value === undefined || value === null) return false;
  if (typeof value === "number") return Math.abs(value) > 1e-6;
  if (typeof value === "string") return value.trim() !== "0" && value.trim() !== "0px";
  return true;
};

const shouldDisplayOpacity = (value) => {
  if (value === undefined || value === null) return false;
  if (typeof value === "number") return Math.abs(value - 1) > 1e-6;
  if (typeof value === "string") {
    const trimmed = value.trim();
    if (!trimmed) return false;
    const asNumber = Number(trimmed);
    if (!Number.isNaN(asNumber)) return Math.abs(asNumber - 1) > 1e-6;
    return true;
  }
  return true;
};

const normalizeFontFamilyName = (name) => {
  if (!name) return null;
  let normalized = String(name).trim();
  if (!normalized) return null;
  normalized = normalized.replace(/\b(PingFangSC|PingFangTC|PingFangHK)\b/gi, (match) => {
    if (/PingFangSC/i.test(match)) return "PingFang SC";
    if (/PingFangTC/i.test(match)) return "PingFang TC";
    if (/PingFangHK/i.test(match)) return "PingFang HK";
    return match;
  });
  normalized = normalized.replace(/-?(Regular|Medium|Semibold|SemiBold|Bold|Light|Ultralight|UltraLight|Thin|Black|Heavy|Italic|Oblique|Condensed|Cond)\b/gi, "");
  normalized = normalized.replace(/\s{2,}/g, " ").trim();
  return normalized || null;
};

const buildFontFamilyStack = (style = {}) => {
  const stack = [];
  const push = (value) => {
    if (!value) return;
    const trimmed = String(value).trim();
    if (!trimmed) return;
    if (!stack.includes(trimmed)) stack.push(trimmed);
  };
  push(style.fontFamily);
  push(style.fontPostscriptName);
  const normalized = normalizeFontFamilyName(style.fontPostscriptName || style.fontFamily);
  push(normalized);
  if (/PingFangSC/i.test(style.fontFamily || style.fontPostscriptName || "")) {
    push("PingFang SC");
  }
  if (!stack.length) return null;
  return stack;
};


const pruneUndefined = (obj = {}) => Object.fromEntries(Object.entries(obj).filter(([, value]) => value !== undefined && value !== null && value !== ""));

const evaluateExpression = (expr) => {
  const sanitized = expr.replace(/\s+/g, "");
  if (!/^[-+*/0-9.()]+$/.test(sanitized)) return NaN;
  try {
    // eslint-disable-next-line no-new-func
    return Function(`"use strict";return (${sanitized});`)();
  } catch {
    return NaN;
  }
};

const loadColorMapping = (platformKey) => {
  const map = new Map();
  if (!platformKey) return map;
  const platformDir = path.resolve(repoRoot, "Apps", platformKey.toLowerCase());

  const jsonPath = path.join(platformDir, "color.json");
  if (fs.existsSync(jsonPath)) {
    try {
      const json = JSON.parse(fs.readFileSync(jsonPath, "utf-8"));
      for (const [rawHex, name] of Object.entries(json)) {
        if (typeof rawHex !== "string" || typeof name !== "string") continue;
        const normalizedHex = rawHex.trim().toLowerCase();
        if (!normalizedHex) continue;
        map.set(normalizedHex, name.trim() || name);
      }
    } catch (err) {
      console.warn(`Warning: failed to parse color mapping (${jsonPath}): ${err?.message || err}`);
    }
  }

  if (map.size) return map;

  const colorsPath = path.join(platformDir, "Color+Additions.swift");
  if (!fs.existsSync(colorsPath)) return map;
  const content = fs.readFileSync(colorsPath, "utf-8");
  const lines = content.split(/\r?\n/);
  const colorLineRegex = /static let (\w+) = Color\(([^)]+)\)/;
  for (const line of lines) {
    const trimmed = line.trim();
    const match = colorLineRegex.exec(trimmed);
    if (!match) continue;
    const [, name, params] = match;
    const args = Object.fromEntries(params.split(",").map(part => {
      const [key, value] = part.split(":").map(str => str.trim());
      return [key, value];
    }));
    let r; let g; let b; let a;
    if ("white" in args) {
      const greyExpr = args.white;
      const greyVal = evaluateExpression(greyExpr);
      if (Number.isNaN(greyVal)) continue;
      const channel = toNumberChannel(greyVal);
      r = g = b = channel;
    } else if ("red" in args && "green" in args && "blue" in args) {
      const redVal = evaluateExpression(args.red);
      const greenVal = evaluateExpression(args.green);
      const blueVal = evaluateExpression(args.blue);
      if ([redVal, greenVal, blueVal].some(Number.isNaN)) continue;
      r = toNumberChannel(redVal);
      g = toNumberChannel(greenVal);
      b = toNumberChannel(blueVal);
    } else {
      continue;
    }
    if ("opacity" in args) {
      const alphaVal = evaluateExpression(args.opacity);
      if (!Number.isNaN(alphaVal)) a = alphaVal;
    }
    const hex = colorObjectToHex({ r, g, b, a });
    if (!hex) continue;
    map.set(hex.toLowerCase(), name);
  }
  return map;
};

const loadFontMapping = (platformKey) => {
  const map = new Map();
  if (!platformKey) return map;
  const platformDir = path.resolve(repoRoot, "Apps", platformKey.toLowerCase());

  const jsonPath = path.join(platformDir, "font.json");
  if (fs.existsSync(jsonPath)) {
    try {
      const json = JSON.parse(fs.readFileSync(jsonPath, "utf-8"));
      for (const [key, name] of Object.entries(json)) {
        if (typeof key !== "string" || typeof name !== "string") continue;
        const normalizedKey = key.trim();
        if (!normalizedKey) continue;
        map.set(normalizedKey, name.trim() || name);
      }
    } catch (err) {
      console.warn(`Warning: failed to parse font mapping (${jsonPath}): ${err?.message || err}`);
    }
  }

  if (map.size) return map;

  const fontPath = path.join(platformDir, "Font+Additions.swift");
  if (!fs.existsSync(fontPath)) return map;
  const content = fs.readFileSync(fontPath, "utf-8");
  const regex = /static let (\w+) = Font\.custom\("([^"]+)",\s*size:\s*([0-9.]+)/g;
  let match;
  while ((match = regex.exec(content))) {
    const [, alias, postscript, sizeStr] = match;
    const size = parseFloat(sizeStr);
    if (Number.isNaN(size)) continue;
    const key = `${postscript} ${Number.isInteger(size) ? size : size.toString()}`;
    map.set(key, alias);
  }
  return map;
};

const extractBorderInfo = (borders = [], resolveColorName = () => undefined) => {
  if (!Array.isArray(borders)) return null;
  const border = borders.find(item => item?.fill?.color && Number.isFinite(item.thickness));
  if (!border) return null;
  const width = border.thickness;
  const colorHex = colorObjectToHex(border.fill?.color);
  const normalizedHex = colorHex ? colorHex.toLowerCase() : undefined;
  const colorName = normalizedHex ? resolveColorName(normalizedHex) : undefined;
  return {
    width,
    colorHex: normalizedHex,
    colorName,
    color: colorName || normalizedHex
  };
};

const extractGradientInfo = (fills = [], resolveColorName = () => undefined) => {
  if (!Array.isArray(fills)) return null;
  const gradientFill = fills.find(fill => fill?.type === "gradient" && fill.gradient?.colorStops?.length);
  if (!gradientFill) return null;

  const gradient = gradientFill.gradient || {};
  const stops = [];

  for (const stop of gradient.colorStops || []) {
    if (!stop?.color) continue;
    const hex = colorObjectToHex(stop.color);
    const normalizedHex = hex ? hex.toLowerCase() : undefined;
    const displayColor = normalizedHex || colorToCss(stop.color);
    if (!displayColor) continue;
    const colorName = normalizedHex ? resolveColorName(normalizedHex) : undefined;
    const position = typeof stop.position === "number" && Number.isFinite(stop.position)
      ? stop.position
      : undefined;
    const positionDisplay = position !== undefined ? formatNumeric(position) : undefined;
    const entry = {
      color: displayColor,
      ...(normalizedHex ? { hex: normalizedHex } : {}),
      ...(colorName ? { colorName } : {}),
      ...(position !== undefined ? { position } : {})
    };
    if (positionDisplay !== undefined) entry.positionDisplay = positionDisplay;
    stops.push(entry);
  }

  if (!stops.length) return null;

  const description = stops.map(stop => {
    const colorPart = stop.hex || stop.color;
    if (stop.positionDisplay !== undefined) {
      return `${colorPart} (${stop.positionDisplay})`;
    }
    if (stop.position !== undefined) {
      const fallback = formatNumeric(stop.position);
      return `${colorPart} (${fallback ?? stop.position})`;
    }
    return colorPart;
  }).join(" -> ");

  const cssStops = stops.map(stop => {
    const colorPart = stop.hex || stop.color;
    if (!colorPart) return null;
    if (stop.position !== undefined) {
      const percent = toPercentString(stop.position);
      return percent ? `${colorPart} ${percent}` : colorPart;
    }
    return colorPart;
  }).filter(Boolean);

  let css = null;
  if (cssStops.length >= 2) {
    const gradientType = (gradient.type || "").toLowerCase();
    if (gradientType === "radial") {
      css = `radial-gradient(${cssStops.join(", ")})`;
    } else {
      css = `linear-gradient(180deg, ${cssStops.join(", ")})`;
    }
  }

  return {
    type: gradient.type || "linear",
    stops,
    description,
    ...(css ? { css } : {})
  };
};

const isFiniteNumber = (value) => typeof value === "number" && Number.isFinite(value);

const extractFillColor = (fills = [], resolveColorName = () => undefined) => {
  if (!Array.isArray(fills)) return null;
  const fill = fills.find(item => item?.type === "color" && item.color);
  if (!fill) return null;
  const colorHex = colorObjectToHex(fill.color);
  const normalizedHex = colorHex ? colorHex.toLowerCase() : undefined;
  const colorName = normalizedHex ? resolveColorName(normalizedHex) : undefined;
  const color = colorToCss(fill.color);
  if (!color && !normalizedHex) return null;
  return {
    color,
    colorHex: normalizedHex,
    colorName,
    display: colorName || normalizedHex || color
  };
};

const buildTextStyleSnapshot = (style = {}, { resolveColorName = () => undefined, fontNameMap = new Map() } = {}) => {
  const postscriptName = style.postscriptName || style.fontPostscriptName || style.font_postscript_name;
  const fontFamily = style.fontFamily || style.font_family || postscriptName;
  const sizeRaw = style.size ?? style.fontSize ?? style.font_size;
  const fontSize = typeof sizeRaw === "number" ? sizeRaw : (sizeRaw ? parseFloat(sizeRaw) : undefined);
  const fontWeight = style.fontWeight ?? style.font_weight;
  const fontStyle = style.fontStyle ?? style.font_style;
  const lineHeight = style.lineHeight ?? style.line_height;
  const letterSpacing = style.letterSpacing ?? style.letter_spacing;
  const textAlign = style.textAlign
    || style.text_alignment
    || style.textAlignment
    || style.alignment
    || style.align;
  const colorCss = colorToCss(style.color);
  const colorHex = colorObjectToHex(style.color);
  const normalizedHex = colorHex ? colorHex.toLowerCase() : undefined;
  const colorName = colorHex ? resolveColorName(colorHex) : undefined;

  let fontName;
  let fontLookupKey;
  const rawSizeString = sizeRaw != null ? String(sizeRaw).trim() : undefined;
  if (postscriptName && (Number.isFinite(fontSize) || rawSizeString)) {
    const trimmedPostscript = String(postscriptName).trim();
    const sizeVariants = new Set();
    if (rawSizeString) {
      sizeVariants.add(rawSizeString);
      sizeVariants.add(rawSizeString.replace(/px$/i, ""));
    }
    if (Number.isFinite(fontSize)) {
      const baseSizeStr = String(fontSize);
      sizeVariants.add(baseSizeStr);
      sizeVariants.add(baseSizeStr.replace(/\.0+$/, ""));
      sizeVariants.add(Number(fontSize.toFixed(2)).toString());
      sizeVariants.add(Number(fontSize.toFixed(1)).toString());
      sizeVariants.add(Math.round(fontSize).toString());
    }
    const candidates = Array.from(sizeVariants)
      .filter(sizeStr => sizeStr && sizeStr !== "NaN" && sizeStr !== "Infinity" && sizeStr !== "-Infinity")
      .sort((a, b) => a.length - b.length || a.localeCompare(b));
    for (const sizeStr of candidates) {
      const candidateKey = `${trimmedPostscript} ${sizeStr}`;
      const candidateName = fontNameMap.get(candidateKey);
      if (candidateName) {
        fontLookupKey = candidateKey;
        fontName = candidateName;
        break;
      }
    }
  }

  return pruneUndefined({
    fontFamily: fontFamily ? String(fontFamily) : undefined,
    fontPostscriptName: postscriptName ? String(postscriptName) : undefined,
    fontSize: isFiniteNumber(fontSize) ? fontSize : undefined,
    fontWeight: fontWeight ? String(fontWeight) : undefined,
    fontStyle: fontStyle ? String(fontStyle) : undefined,
    lineHeight: isFiniteNumber(lineHeight) ? lineHeight : undefined,
    letterSpacing: isFiniteNumber(letterSpacing) ? letterSpacing : undefined,
    textAlign: textAlign ? String(textAlign) : undefined,
    color: colorCss,
    colorHex: colorHex ? colorHex.toLowerCase() : undefined,
    colorName,
    fontName,
    fontKey: fontLookupKey
  });
};

const extractTextInfo = (layer, options = {}) => {
  if (!layer) return null;
  const { resolveColorName = () => undefined, fontNameMap = new Map() } = options;
  const styleOptions = { resolveColorName, fontNameMap };
  const style = layer.textStyles?.[0]?.style || layer.text?.style || {};
  const content = layer.content ?? layer.plainText ?? layer.text?.content ?? "";
  const styleSnapshot = buildTextStyleSnapshot(style, styleOptions);

  if (!content && !Object.keys(styleSnapshot).length) return null;

  let runs = null;
  const rawTextStyles = layer.textStyles;
  if (Array.isArray(rawTextStyles) && rawTextStyles.length > 1 && content) {
    const sortedTextStyles = rawTextStyles
      .filter(item => item?.range && typeof item.range.location === "number" && typeof item.range.length === "number")
      .sort((a, b) => a.range.location - b.range.location);

    if (sortedTextStyles.length > 1) {
      const builtRuns = [];
      let cursor = 0;
      for (const textStyle of sortedTextStyles) {
        const start = Math.max(0, textStyle.range.location);
        const end = Math.max(start, start + textStyle.range.length);
        if (start > cursor) {
          builtRuns.push({
            text: content.slice(cursor, start),
            style: styleSnapshot
          });
        }
        if (end > start) {
          builtRuns.push({
            text: content.slice(start, end),
            style: buildTextStyleSnapshot(textStyle.style || {}, styleOptions)
          });
        }
        cursor = end;
      }
      if (cursor < content.length) {
        builtRuns.push({
          text: content.slice(cursor),
          style: styleSnapshot
        });
      }
      if (builtRuns.length > 1) {
        runs = builtRuns.filter(run => run.text);
      }
    }
  }

  return {
    content,
    style: styleSnapshot,
    ...(runs?.length ? { runs } : {})
  };
};

const createStyleContext = (platformKey) => {
  const colorNameMap = loadColorMapping(platformKey);
  const fontNameMap = loadFontMapping(platformKey);
  const resolveColorName = (hex) => {
    if (!hex) return undefined;
    const normalized = hex.trim().toLowerCase();
    return colorNameMap.get(normalized);
  };

  return {
    colorNameMap,
    fontNameMap,
    resolveColorName,
    colorToCss,
    colorObjectToHex,
    borderToCss,
    shadowToCss,
    formatNumeric,
    toPercentString,
    describeConstraints,
    shouldDisplayBorderRadius,
    shouldDisplayOpacity,
    buildFontFamilyStack,
    extractGradientInfo: (fills = []) => extractGradientInfo(fills, resolveColorName),
    extractBorderInfo: (borders = []) => extractBorderInfo(borders, resolveColorName),
    extractFillColor: (fills = []) => extractFillColor(fills, resolveColorName),
    extractTextInfo: (layer) => extractTextInfo(layer, { resolveColorName, fontNameMap })
  };
};

export {
  borderToCss,
  colorObjectToHex,
  colorToCss,
  createStyleContext,
  describeConstraints,
  extractBorderInfo,
  extractFillColor,
  extractGradientInfo,
  extractTextInfo,
  formatNumeric,
  loadColorMapping,
  loadFontMapping,
  shadowToCss,
  shouldDisplayBorderRadius,
  shouldDisplayOpacity,
  buildFontFamilyStack,
  toNumberChannel,
  toPercentString
};
