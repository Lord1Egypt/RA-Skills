export const CANVAS_SCHEMA_VERSION = "2.0";

export const BLOCK_TYPES = Object.freeze([
  "section-header",
  "narrative",
  "callout",
  "table",
  "metric-card",
  "price-chart",
  "sentiment",
  "news-feed",
  "watchlist",
  "market-mood",
]);

const MAX_XML_BYTES = 65_536;
const MAX_BLOCKS = 48;
const MAX_PROPS = 16;
const MAX_STRING = 8_192;
const ID_PATTERN = /^[A-Za-z][A-Za-z0-9_.:-]{0,63}$/;
const SNAPSHOT_PATTERN = /^[A-Za-z][A-Za-z0-9_.:-]{0,127}$/;
const CORE_ATTRS = new Set(["id", "type", "width"]);
const ROOT_ATTRS = new Set(["id", "title", "created", "schemaVersion", "author", "tags", "version", "template"]);
const WIDTHS = new Set(["full", "half", "third"]);

const RULES = Object.freeze({
  "section-header": { allowed: ["title", "subtitle"], required: ["title"], content: false },
  narrative: { allowed: ["title"], required: [], content: true },
  callout: { allowed: ["tone", "title"], required: ["tone"], content: true },
  table: {
    allowed: ["title", "dataRef", "columns", "rows", "asOf", "synthetic"],
    required: [], content: false, data: { live: ["dataRef"], inline: ["columns", "rows", "asOf", "synthetic"], inlineFields: ["columns", "rows", "asOf", "synthetic"] },
  },
  "metric-card": {
    allowed: ["label", "field", "dataRef", "value", "asOf", "synthetic"],
    required: ["label"], content: false, data: { live: ["dataRef", "field"], inline: ["value", "asOf", "synthetic"], inlineFields: ["value", "asOf", "synthetic"] },
  },
  "price-chart": {
    allowed: ["ticker", "range", "dataRef", "points", "asOf", "synthetic"],
    required: ["ticker", "range"], content: false, data: { live: ["dataRef"], inline: ["points", "asOf", "synthetic"], inlineFields: ["points", "asOf", "synthetic"] },
  },
  sentiment: {
    allowed: ["ticker", "dataRef", "value", "score", "asOf", "synthetic"],
    required: ["ticker"], content: false, data: { live: ["dataRef"], inline: ["value", "asOf", "synthetic"], inlineFields: ["value", "score", "asOf", "synthetic"] },
  },
  "news-feed": {
    allowed: ["ticker", "dataRef", "items", "asOf", "synthetic"],
    required: ["ticker"], content: false, data: { live: ["dataRef"], inline: ["items", "asOf", "synthetic"], inlineFields: ["items", "asOf", "synthetic"] },
  },
  watchlist: {
    allowed: ["title", "dataRef", "items", "asOf", "synthetic"],
    required: ["title"], content: false, data: { live: ["dataRef"], inline: ["items", "asOf", "synthetic"], inlineFields: ["items", "asOf", "synthetic"] },
  },
  "market-mood": {
    allowed: ["dataRef", "score", "phase", "asOf", "synthetic"],
    required: [], content: false, data: { live: ["dataRef"], inline: ["score", "phase", "asOf", "synthetic"], inlineFields: ["score", "phase", "asOf", "synthetic"] },
  },
});

function failure(code, message, path) {
  return { ok: false, error: { code, message, ...(path ? { path } : {}) } };
}

function scalar(value) {
  return typeof value === "string" && value.length <= MAX_STRING;
}

function displayScalar(value) {
  return scalar(value) && !/[<>]/.test(value);
}

function isoDateTime(value) {
  if (typeof value !== "string") return false;
  const match = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d{1,9})?(?:Z|[+-]\d{2}:\d{2})$/.exec(value);
  if (!match) return false;
  const [, year, month, day, hour, minute, second] = match.map(Number);
  if (month < 1 || month > 12 || hour > 23 || minute > 59 || second > 59) return false;
  const days = new Date(Date.UTC(year, month, 0)).getUTCDate();
  return day >= 1 && day <= days && Number.isFinite(Date.parse(value));
}

function safeUrl(value) {
  try {
    const url = new URL(value);
    return url.protocol === "https:" || url.protocol === "http:";
  } catch {
    return false;
  }
}

function parseBoundedJson(value, path, expected) {
  let parsed;
  try { parsed = JSON.parse(value); } catch { return failure("INVALID_PROPS", `${path} must be valid JSON`, path); }
  if (expected === "array" && !Array.isArray(parsed)) return failure("INVALID_PROPS", `${path} must be a JSON array`, path);
  if (JSON.stringify(parsed).length > MAX_STRING) return failure("SCHEMA_LIMIT", `${path} exceeds the serialized data limit`, path);
  if (Array.isArray(parsed) && parsed.length > 50) return failure("SCHEMA_LIMIT", `${path} has more than 50 items`, path);
  return { ok: true };
}

function safeRecord(item, allowed, required, path) {
  if (!item || typeof item !== "object" || Array.isArray(item)) return failure("INVALID_PROPS", `${path} must be an object`, path);
  const keys = Object.keys(item);
  if (keys.some((key) => !allowed.includes(key)) || required.some((key) => !Object.hasOwn(item, key))) return failure("INVALID_PROPS", `${path} has an invalid shape`, path);
  for (const value of Object.values(item)) if (!(value === null || ["string", "number", "boolean"].includes(typeof value)) || (typeof value === "number" && !Number.isFinite(value)) || (typeof value === "string" && value.length > 500)) return failure("INVALID_PROPS", `${path} has an unsafe value`, path);
  return { ok: true };
}

function validateInlineData(type, props, path) {
  if (type === "table") {
    const columns = JSON.parse(props.columns); const rows = JSON.parse(props.rows);
    if (!columns.length || columns.length > 12 || columns.some((value) => typeof value !== "string" || !value || value.length > 80)) return failure("INVALID_PROPS", "table columns are invalid", `${path}.columns`);
    if (rows.some((row) => !Array.isArray(row) || row.length !== columns.length || row.some((cell) => !(cell === null || ["string", "number", "boolean"].includes(typeof cell)) || (typeof cell === "number" && !Number.isFinite(cell)) || (typeof cell === "string" && cell.length > 500)))) return failure("INVALID_PROPS", "table rows do not match columns", `${path}.rows`);
  }
  if (type === "price-chart") {
    const points = JSON.parse(props.points);
    for (let index = 0; index < points.length; index += 1) {
      const result = safeRecord(points[index], ["time", "value"], ["time", "value"], `${path}.points[${index}]`);
      if (!result.ok) return result;
      if (typeof points[index].time !== "string" || !points[index].time || typeof points[index].value !== "number" || !Number.isFinite(points[index].value)) return failure("INVALID_PROPS", "chart point needs a time and finite numeric value", `${path}.points[${index}]`);
    }
  }
  if (type === "news-feed") {
    const items = JSON.parse(props.items);
    for (let index = 0; index < items.length; index += 1) {
      const result = safeRecord(items[index], ["title", "source", "url", "publishedAt", "summary"], ["title"], `${path}.items[${index}]`);
      if (!result.ok) return result;
      if (typeof items[index].title !== "string" || !items[index].title.trim()) return failure("INVALID_PROPS", "news item requires a title string", `${path}.items[${index}].title`);
      if (items[index].url && !safeUrl(items[index].url)) return failure("UNSAFE_URL", "news item URL must use http or https", `${path}.items[${index}].url`);
    }
  }
  if (type === "watchlist") {
    const items = JSON.parse(props.items);
    for (let index = 0; index < items.length; index += 1) {
      const result = safeRecord(items[index], ["ticker", "change", "value", "label"], ["ticker"], `${path}.items[${index}]`);
      if (!result.ok) return result;
      if (typeof items[index].ticker !== "string" || !items[index].ticker.trim()) return failure("INVALID_PROPS", "watchlist item requires a ticker string", `${path}.items[${index}].ticker`);
    }
  }
  return { ok: true };
}

function validateProps(type, props, path) {
  const rule = RULES[type];
  if (!props || typeof props !== "object" || Array.isArray(props)) return failure("INVALID_PROPS", "props must be an object", `${path}.props`);
  const entries = Object.entries(props);
  if (entries.length > MAX_PROPS) return failure("SCHEMA_LIMIT", "too many block props", `${path}.props`);
  for (const [key, value] of entries) {
    if (!rule.allowed.includes(key) || /^on/i.test(key)) return failure("INVALID_PROPS", `prop ${key} is not allowed for ${type}`, `${path}.props.${key}`);
    if (!scalar(value)) return failure("INVALID_PROPS", `prop ${key} must be a bounded string`, `${path}.props.${key}`);
    if (/[<>]/.test(value)) return failure("UNSAFE_CONTENT", `prop ${key} contains markup`, `${path}.props.${key}`);
  }
  for (const key of rule.required) {
    if (!props[key]) return failure("MISSING_PROP", `${type} requires prop ${key}`, `${path}.props.${key}`);
  }
  if (props.dataRef && !SNAPSHOT_PATTERN.test(props.dataRef)) return failure("INVALID_PROPS", "dataRef is not a valid snapshot ID", `${path}.props.dataRef`);
  if (props.synthetic && props.synthetic !== "true") return failure("INVALID_PROPS", "synthetic must be the string true", `${path}.props.synthetic`);
  if (props.asOf !== undefined && !isoDateTime(props.asOf)) return failure("INVALID_PROPS", "asOf must be a valid ISO date-time", `${path}.props.asOf`);
  if (type === "callout" && !["neutral", "bullish", "bearish", "warning"].includes(props.tone)) {
    return failure("INVALID_PROPS", "callout tone is not recognized", `${path}.props.tone`);
  }
  if (rule.data) {
    const live = rule.data.live.every((key) => Boolean(props[key]));
    const inline = rule.data.inline.every((key) => Boolean(props[key])) && props.synthetic === "true";
    const strayInline = rule.data.inlineFields.some((key) => props[key] !== undefined);
    if ((live && strayInline) || (!live && !inline) || (inline && props.dataRef !== undefined)) return failure("INVALID_DATA_MODE", `${type} requires exactly one live dataRef mode or dated synthetic inline mode`, `${path}.props`);
  }
  for (const key of ["columns", "rows", "points", "items"]) {
    if (props[key]) {
      const result = parseBoundedJson(props[key], `${path}.props.${key}`, "array");
      if (!result.ok) return result;
    }
  }
  if (rule.data && props.synthetic === "true") {
    const result = validateInlineData(type, props, `${path}.props`);
    if (!result.ok) return result;
  }
  return { ok: true };
}

function validateBlock(block, path, expectedWidth, seen) {
  if (!block || typeof block !== "object" || Array.isArray(block)) return failure("INVALID_BLOCK", "block must be an object", path);
  const keys = Object.keys(block);
  if (keys.some((key) => !["id", "type", "width", "props", "content"].includes(key))) return failure("INVALID_BLOCK", "block has an unknown field", path);
  if (typeof block.id !== "string" || !ID_PATTERN.test(block.id)) return failure("INVALID_ID", "block id is invalid", `${path}.id`);
  if (seen.has(block.id)) return failure("DUPLICATE_ID", `duplicate id ${block.id}`, `${path}.id`);
  seen.add(block.id);
  if (!BLOCK_TYPES.includes(block.type)) return failure("UNKNOWN_BLOCK_TYPE", `unknown block type ${block.type}`, `${path}.type`);
  if (!WIDTHS.has(block.width) || block.width !== expectedWidth) return failure("INVALID_WIDTH", `block width must be ${expectedWidth}`, `${path}.width`);
  const rule = RULES[block.type];
  if (rule.content) {
    if (!scalar(block.content) || !block.content.trim()) return failure("INVALID_CONTENT", `${block.type} requires text content`, `${path}.content`);
    if (/<\/?(?:script|style|iframe|object|embed|svg|math)\b|<[^>]+>/i.test(block.content)) return failure("UNSAFE_CONTENT", "block content contains markup", `${path}.content`);
  } else if (block.content !== undefined) {
    return failure("INVALID_CONTENT", `${block.type} does not accept text content`, `${path}.content`);
  }
  return validateProps(block.type, block.props, path);
}

export function validateCanvasAst(canvas) {
  if (!canvas || typeof canvas !== "object" || Array.isArray(canvas)) return failure("INVALID_CANVAS", "canvas must be an object", "$");
  const allowed = new Set(["schemaVersion", "id", "title", "created", "author", "tags", "version", "template", "blocks"]);
  if (Object.keys(canvas).some((key) => !allowed.has(key))) return failure("INVALID_CANVAS", "canvas has an unknown field", "$");
  if (canvas.schemaVersion !== CANVAS_SCHEMA_VERSION) return failure("VERSION_MISMATCH", `expected canvas schema ${CANVAS_SCHEMA_VERSION}`, "$.schemaVersion");
  if (typeof canvas.id !== "string" || !ID_PATTERN.test(canvas.id)) return failure("INVALID_ID", "canvas id is invalid", "$.id");
  if (!displayScalar(canvas.title) || !canvas.title.trim() || canvas.title.length > 160) return failure("INVALID_CANVAS", "canvas title is invalid", "$.title");
  if (!isoDateTime(canvas.created)) return failure("INVALID_CANVAS", "canvas created must be a valid ISO date-time", "$.created");
  for (const key of ["author", "version", "template"]) if (canvas[key] !== undefined && !displayScalar(canvas[key])) return failure("INVALID_CANVAS", `${key} must be a safe bounded string`, `$.${key}`);
  if (canvas.tags !== undefined && (!Array.isArray(canvas.tags) || canvas.tags.length > 12 || canvas.tags.some((tag) => !displayScalar(tag) || !tag.trim() || tag.length > 48))) return failure("INVALID_CANVAS", "tags must be a bounded string array", "$.tags");
  if (!Array.isArray(canvas.blocks) || canvas.blocks.length < 1 || canvas.blocks.length > MAX_BLOCKS) return failure("SCHEMA_LIMIT", `canvas requires 1 to ${MAX_BLOCKS} top-level items`, "$.blocks");
  let serialized;
  try { serialized = JSON.stringify(canvas); } catch { return failure("INVALID_CANVAS", "canvas must be serializable", "$"); }
  if (new TextEncoder().encode(serialized).length > MAX_XML_BYTES) return failure("SCHEMA_LIMIT", "canvas AST exceeds the byte limit", "$");
  const totalBlocks = canvas.blocks.reduce((count, item) => count + (item?.type === "row" && Array.isArray(item.blocks) ? item.blocks.length : 1), 0);
  if (totalBlocks > MAX_BLOCKS) return failure("SCHEMA_LIMIT", `canvas has more than ${MAX_BLOCKS} blocks`, "$.blocks");
  const seen = new Set([canvas.id]);
  for (let index = 0; index < canvas.blocks.length; index += 1) {
    const item = canvas.blocks[index];
    const path = `$.blocks[${index}]`;
    if (item?.type === "row") {
      if (Object.keys(item).some((key) => !["type", "blocks"].includes(key))) return failure("INVALID_ROW", "row has an unknown field", path);
      if (!Array.isArray(item.blocks) || ![2, 3].includes(item.blocks.length)) return failure("INVALID_ROW", "row requires two or three blocks", `${path}.blocks`);
      const width = item.blocks.length === 2 ? "half" : "third";
      for (let child = 0; child < item.blocks.length; child += 1) {
        if (item.blocks[child]?.type === "row") return failure("NESTED_ROW", "rows cannot be nested", `${path}.blocks[${child}]`);
        const result = validateBlock(item.blocks[child], `${path}.blocks[${child}]`, width, seen);
        if (!result.ok) return result;
      }
    } else {
      const result = validateBlock(item, path, "full", seen);
      if (!result.ok) return result;
    }
  }
  return { ok: true, canvas };
}

function decodeEntities(value, path) {
  if (/&(?!#x[0-9a-fA-F]+;|#[0-9]+;|amp;|lt;|gt;|quot;|apos;)/.test(value)) {
    return failure("UNKNOWN_ENTITY", "unknown or unterminated XML entity", path);
  }
  let bad = null;
  const decoded = value.replace(/&(#x[0-9a-fA-F]+|#[0-9]+|amp|lt|gt|quot|apos);/g, (match, entity) => {
    if (entity === "amp") return "&";
    if (entity === "lt") return "<";
    if (entity === "gt") return ">";
    if (entity === "quot") return '"';
    if (entity === "apos") return "'";
    const code = entity[1].toLowerCase() === "x" ? Number.parseInt(entity.slice(2), 16) : Number.parseInt(entity.slice(1), 10);
    const validXmlChar = code === 0x9 || code === 0xa || code === 0xd || (code >= 0x20 && code <= 0xd7ff) || (code >= 0xe000 && code <= 0xfffd) || (code >= 0x10000 && code <= 0x10ffff);
    if (!Number.isFinite(code) || !validXmlChar) { bad = match; return ""; }
    return String.fromCodePoint(code);
  });
  if (bad) return failure("UNKNOWN_ENTITY", `unknown or invalid XML entity ${bad}`, path);
  return { ok: true, value: decoded };
}

function parseTag(source, path) {
  if (source.includes("<")) return failure("MALFORMED_XML", "raw < is not allowed inside a tag", path);
  let cursor = 0;
  const skip = () => { while (/\s/.test(source[cursor] || "")) cursor += 1; };
  skip();
  const nameMatch = /^[A-Za-z][A-Za-z0-9-]*/.exec(source.slice(cursor));
  if (!nameMatch) return failure("MALFORMED_XML", "tag name is invalid", path);
  const name = nameMatch[0]; cursor += name.length;
  const attrs = {};
  while (cursor < source.length) {
    if (!/\s/.test(source[cursor])) return failure("MALFORMED_XML", "attributes must be separated by whitespace", path);
    skip();
    if (cursor >= source.length) break;
    const keyMatch = /^[A-Za-z][A-Za-z0-9-]*/.exec(source.slice(cursor));
    if (!keyMatch) return failure("MALFORMED_XML", "attribute name is invalid", path);
    const key = keyMatch[0]; cursor += key.length; skip();
    if (source[cursor] !== "=") return failure("MALFORMED_XML", `attribute ${key} is missing =`, path);
    cursor += 1; skip();
    const quote = source[cursor];
    if (quote !== '"' && quote !== "'") return failure("MALFORMED_XML", `attribute ${key} must be quoted`, path);
    cursor += 1;
    const end = source.indexOf(quote, cursor);
    if (end < 0) return failure("MALFORMED_XML", `attribute ${key} is not closed`, path);
    if (Object.hasOwn(attrs, key)) return failure("DUPLICATE_ATTRIBUTE", `duplicate attribute ${key}`, path);
    const decoded = decodeEntities(source.slice(cursor, end), `${path}@${key}`);
    if (!decoded.ok) return decoded;
    attrs[key] = decoded.value; cursor = end + 1;
  }
  return { ok: true, name, attrs };
}

export function parseCanvasXml(xml, options = {}) {
  if (typeof xml !== "string") return failure("MALFORMED_XML", "XML input must be a string", "$");
  const maxBytes = options.maxBytes ?? MAX_XML_BYTES;
  if (new TextEncoder().encode(xml).length > maxBytes) return failure("XML_TOO_LARGE", `XML exceeds ${maxBytes} bytes`, "$");
  if (/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/.test(xml)) return failure("FORBIDDEN_XML", "XML contains a forbidden control character", "$");
  if (/<!|<\?/.test(xml)) return failure("FORBIDDEN_XML", "DTD, declarations, comments, CDATA and processing instructions are not allowed", "$");
  const tokens = [];
  const re = /<([^>]+)>/g;
  let last = 0; let match;
  while ((match = re.exec(xml))) {
    const text = xml.slice(last, match.index);
    if (text.includes("<")) return failure("MALFORMED_XML", "unclosed tag delimiter", "$");
    if (text) tokens.push({ kind: "text", value: text });
    tokens.push({ kind: "tag", value: match[1] }); last = re.lastIndex;
  }
  if (xml.slice(last).includes("<")) return failure("MALFORMED_XML", "unclosed tag delimiter", "$");
  if (xml.slice(last)) tokens.push({ kind: "text", value: xml.slice(last) });
  const stack = [];
  let root = null;
  for (const token of tokens) {
    if (token.kind === "text") {
      if (!token.value.trim()) continue;
      if (!stack.length || stack.at(-1).name !== "block") return failure("UNEXPECTED_TEXT", "text is allowed only inside narrative or callout blocks", "$");
      stack.at(-1).text += token.value;
      continue;
    }
    const raw = token.value.trim();
    if (/^\s/.test(token.value) || (/^\//.test(raw) && !/^\/[A-Za-z]/.test(raw))) return failure("MALFORMED_XML", "tag names cannot contain leading whitespace", "$");
    if (raw.startsWith("/")) {
      const close = raw.slice(1).trim();
      if (!/^[A-Za-z][A-Za-z0-9-]*$/.test(close) || !stack.length || stack.at(-1).name !== close) return failure("MALFORMED_XML", `unexpected closing tag ${close}`, "$");
      const node = stack.pop();
      if (node.name === "block" && node.text) {
        const decoded = decodeEntities(node.text, `block:${node.attrs.id || "unknown"}`);
        if (!decoded.ok) return decoded;
        node.output.content = decoded.value.trim();
      }
      continue;
    }
    const selfClosing = raw.endsWith("/");
    const parsed = parseTag(selfClosing ? raw.slice(0, -1) : raw, "$");
    if (!parsed.ok) return parsed;
    const { name, attrs } = parsed;
    if (!["canvas", "row", "block"].includes(name)) return failure("UNKNOWN_ELEMENT", `unknown element ${name}`, "$");
    const parent = stack.at(-1);
    let output;
    if (name === "canvas") {
      if (root || parent) return failure("INVALID_ROOT", "canvas must be the single root", "$");
      for (const key of Object.keys(attrs)) if (!ROOT_ATTRS.has(key)) return failure("INVALID_ATTRIBUTE", `canvas attribute ${key} is not allowed`, `$.${key}`);
      for (const key of ["id", "title", "created", "schemaVersion"]) if (!attrs[key]) return failure("MISSING_ATTRIBUTE", `canvas requires ${key}`, `$.${key}`);
      output = { schemaVersion: attrs.schemaVersion, id: attrs.id, title: attrs.title, created: attrs.created, blocks: [] };
      for (const key of ["author", "version", "template"]) if (attrs[key] !== undefined) output[key] = attrs[key];
      if (attrs.tags !== undefined) output.tags = attrs.tags.split(",").map((tag) => tag.trim()).filter(Boolean);
      root = output;
    } else if (name === "row") {
      if (!parent || parent.name !== "canvas") return failure("NESTED_ROW", "row must be a direct canvas child", "$");
      if (Object.keys(attrs).length) return failure("INVALID_ATTRIBUTE", "row does not accept attributes", "$");
      output = { type: "row", blocks: [] }; parent.output.blocks.push(output);
    } else {
      if (!parent || !["canvas", "row"].includes(parent.name)) return failure("INVALID_BLOCK", "block must be inside canvas or row", "$");
      for (const key of ["id", "type", "width"]) if (!attrs[key]) return failure("MISSING_ATTRIBUTE", `block requires ${key}`, "$");
      const props = {};
      for (const [key, value] of Object.entries(attrs)) if (!CORE_ATTRS.has(key)) props[key] = value;
      output = { id: attrs.id, type: attrs.type, width: attrs.width, props };
      if (parent.name === "row") parent.output.blocks.push(output); else parent.output.blocks.push(output);
    }
    if (!selfClosing) stack.push({ name, attrs, output, text: "" });
    else if (name !== "block") return failure("MALFORMED_XML", `${name} cannot be self-closing`, "$");
  }
  if (stack.length) return failure("MALFORMED_XML", `unclosed ${stack.at(-1).name} element`, "$");
  if (!root) return failure("INVALID_ROOT", "canvas root is missing", "$");
  return validateCanvasAst(root);
}
