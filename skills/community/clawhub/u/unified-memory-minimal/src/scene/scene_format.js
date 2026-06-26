/**
 * Scene Block file format: parse and format the META-delimited Markdown files.
 */

/**
 * @typedef {Object} SceneBlockMeta
 * @property {string} created
 * @property {string} updated
 * @property {string} summary
 * @property {number} heat
 */

/**
 * @typedef {Object} SceneBlock
 * @property {string} filename
 * @property {SceneBlockMeta} meta
 * @property {string} content
 */

const META_START = "-----META-START-----";
const META_END = "-----META-END-----";

/**
 * Parse a Scene Block file into structured data.
 * @param {string} raw
 * @param {string} filename
 * @returns {SceneBlock}
 */
export function parseSceneBlock(raw, filename) {
  const startIdx = raw.indexOf(META_START);
  const endIdx = raw.indexOf(META_END);

  if (startIdx === -1 || endIdx === -1) {
    return {
      filename,
      meta: { created: "", updated: "", summary: "", heat: 0 },
      content: raw.trim(),
    };
  }

  const metaBlock = raw.slice(startIdx + META_START.length, endIdx).trim();
  const content = raw.slice(endIdx + META_END.length).trim();

  const meta = {
    created: extractMetaField(metaBlock, "created"),
    updated: extractMetaField(metaBlock, "updated"),
    summary: extractMetaField(metaBlock, "summary"),
    heat: parseInt(extractMetaField(metaBlock, "heat"), 10) || 0,
  };

  return { filename, meta, content };
}

/**
 * Format a Scene Block back into file content.
 * @param {SceneBlockMeta} meta
 * @param {string} content
 * @returns {string}
 */
export function formatSceneBlock(meta, content) {
  return `${formatMeta(meta)}\n\n${content}`;
}

/**
 * Format the META section.
 * @param {SceneBlockMeta} meta
 * @returns {string}
 */
export function formatMeta(meta) {
  return [
    META_START,
    `created: ${meta.created}`,
    `updated: ${meta.updated}`,
    `summary: ${meta.summary}`,
    `heat: ${meta.heat}`,
    META_END,
  ].join("\n");
}

/**
 * @param {string} metaBlock
 * @param {string} field
 * @returns {string}
 */
function extractMetaField(metaBlock, field) {
  const re = new RegExp(`^${field}:\\s*(.*)$`, "m");
  const m = metaBlock.match(re);
  return m ? m[1].trim() : "";
}
