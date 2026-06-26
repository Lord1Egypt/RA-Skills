/**
 * Scene navigation: generates a summary navigation section appended to persona.md.
 *
 * The navigation includes file paths so the agent can use read_file to load
 * scene details on demand (progressive disclosure).
 */

const NAV_HEADER = "---\n## 🗺️ Scene Navigation (Scene Index)";

const NAV_FOOTER = `📌 使用说明：
- Path 即 scene block 的相对路径，可按需使用 read_file 读取详细内容
- 热度：该场景被记忆命中的累计次数，越高越重要
- Summary：场景的核心要点摘要`;

/**
 * Build a fire-emoji string based on heat value (visual priority cue for the agent).
 * @param {number} heat
 * @returns {string}
 */
function heatEmoji(heat) {
  if (heat >= 1000) return " 🔥🔥🔥🔥🔥";
  if (heat >= 500) return " 🔥🔥🔥🔥";
  if (heat >= 200) return " 🔥🔥🔥";
  if (heat >= 100) return " 🔥🔥";
  if (heat >= 50) return " 🔥";
  return "";
}

/**
 * Generate the scene navigation Markdown section.
 * @param {Array<{filename: string, summary: string, heat: number, created?: string, updated?: string}>} entries
 * @returns {string}
 */
export function generateSceneNavigation(entries) {
  if (entries.length === 0) return "";

  const sorted = [...entries].sort((a, b) => b.heat - a.heat);

  const blocks = sorted.map((e) => {
    const pathLine = `### Path: scene_blocks/${e.filename}`;
    const heatLine = `**热度**: ${e.heat}${heatEmoji(e.heat)}${e.updated ? ` | **更新**: ${e.updated}` : ""}`;
    const summaryLine = `Summary: ${e.summary}`;
    return `${pathLine}\n${heatLine}\n${summaryLine}`;
  });

  return `${NAV_HEADER}\n*以下是当前场景记忆的索引，可根据需要 read_file 读取详细内容。*\n\n${blocks.join("\n\n")}\n\n${NAV_FOOTER}`;
}

/**
 * Strip the scene navigation section from persona content.
 * @param {string} personaContent
 * @returns {string}
 */
export function stripSceneNavigation(personaContent) {
  const idx = personaContent.indexOf(NAV_HEADER);
  if (idx === -1) return personaContent;
  return personaContent.slice(0, idx).trimEnd();
}
