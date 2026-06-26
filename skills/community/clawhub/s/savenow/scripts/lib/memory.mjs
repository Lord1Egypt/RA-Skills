// Shared helpers for savenow scripts.
// Imported by ../merge-daily-memory.mjs and ../preview-diff.mjs.

export function parseArgs(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i += 1) {
    const part = argv[i];
    if (!part.startsWith("--")) continue;
    const key = part.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) {
      out[key] = true;
      continue;
    }
    out[key] = next;
    i += 1;
  }
  return out;
}

export function pad2(value) {
  return String(value).padStart(2, "0");
}

export function localDateStamp(date) {
  return `${date.getFullYear()}-${pad2(date.getMonth() + 1)}-${pad2(date.getDate())}`;
}

export function localTimeStamp(date) {
  return `${pad2(date.getHours())}:${pad2(date.getMinutes())}`;
}

export function stripBom(value) {
  return value.charCodeAt(0) === 0xfeff ? value.slice(1) : value;
}

export function normalizeText(value) {
  return String(value ?? "")
    .normalize("NFKC")
    .toLowerCase()
    .replace(/[`*_#~]+/g, " ")
    .replace(/[^\p{L}\p{N}]+/gu, " ")
    .replace(/\s+/g, " ")
    .trim();
}

export function tokenize(value) {
  const normalized = normalizeText(value);
  return normalized ? new Set(normalized.split(" ")) : new Set();
}

export function jaccard(a, b) {
  if (a.size === 0 || b.size === 0) return 0;
  let overlap = 0;
  for (const token of a) {
    if (b.has(token)) overlap += 1;
  }
  return overlap / (a.size + b.size - overlap);
}

export function sanitizeEntry(entry) {
  if (!entry || typeof entry !== "object") return null;
  const title = String(entry.title ?? "").trim();
  const bullets = Array.isArray(entry.bullets)
    ? entry.bullets.map((item) => String(item ?? "").trim()).filter(Boolean)
    : [];
  if (!title || bullets.length === 0) return null;

  const rawAction = String(entry.action ?? "add").trim().toLowerCase();
  const action = ["add", "skip", "merge"].includes(rawAction) ? rawAction : "add";
  const mergeTargetTitle = action === "merge"
    ? String(entry.merge_target_title ?? "").trim()
    : "";
  const reason = String(entry.reason ?? "").trim();
  const candidateIndex = Number.isFinite(entry.candidate_index)
    ? entry.candidate_index
    : null;

  return { title, bullets, action, mergeTargetTitle, reason, candidateIndex };
}

// Returns sections with startLine/endLine (inclusive, 0-indexed over text.split(/\r?\n/)).
// startLine = line index of `## …` heading
// endLine   = line index of the last `- …` bullet (or heading itself if no bullets)
export function parseExistingSections(text) {
  const lines = text.split(/\r?\n/);
  const sections = [];
  let current = null;

  for (let i = 0; i < lines.length; i += 1) {
    const line = lines[i].trimEnd();
    if (line.startsWith("## ")) {
      if (current) sections.push(current);
      let title = line.slice(3).trim();
      const headingTime = title.match(/^(\d{2}:\d{2})\s*-\s*/);
      const time = headingTime ? headingTime[1] : "";
      title = title.replace(/^\d{2}:\d{2}\s*-\s*/, "").trim();
      current = {
        title,
        time,
        bullets: [],
        startLine: i,
        endLine: i,
        headingLine: i,
      };
      continue;
    }
    if (current && line.startsWith("- ")) {
      current.bullets.push(line.slice(2).trim());
      current.endLine = i;
    }
  }
  if (current) sections.push(current);
  return { sections, lines };
}

export function buildExistingIndex(sections) {
  const bySection = sections.map((section, sectionIndex) => {
    const titleKey = normalizeText(section.title);
    const titleTokens = tokenize(section.title);
    const bulletKeys = new Set(
      section.bullets.map((bullet) => normalizeText(bullet)).filter(Boolean),
    );
    return {
      titleKey,
      titleTokens,
      bulletKeys,
      sectionIndex,
      title: section.title,
      time: section.time,
    };
  });
  const allBulletKeys = new Set();
  for (const section of bySection) {
    for (const bulletKey of section.bulletKeys) {
      allBulletKeys.add(bulletKey);
    }
  }
  return { bySection, allBulletKeys };
}

export function findExistingMatch(entry, existingIndex) {
  const titleKey = normalizeText(entry.title);
  const titleTokens = tokenize(entry.title);
  const bulletKeys = entry.bullets.map((bullet) => normalizeText(bullet)).filter(Boolean);
  if (!titleKey || bulletKeys.length === 0) {
    return { duplicate: true, reason: "empty", match: null, similarity: 1 };
  }
  for (const section of existingIndex.bySection) {
    if (section.titleKey && section.titleKey === titleKey) {
      return { duplicate: true, reason: "exact-title", match: section, similarity: 1 };
    }
    const titleSimilarity = jaccard(titleTokens, section.titleTokens);
    const bulletOverlap = bulletKeys.filter((key) => section.bulletKeys.has(key)).length;
    if (titleSimilarity >= 0.88 && bulletOverlap > 0) {
      return { duplicate: true, reason: "jaccard", match: section, similarity: titleSimilarity };
    }
  }
  if (bulletKeys.every((key) => existingIndex.allBulletKeys.has(key))) {
    return { duplicate: true, reason: "all-bullets-duplicate", match: null, similarity: 1 };
  }
  return { duplicate: false, reason: null, match: null, similarity: 0 };
}

export function topJaccardMatches(entry, existingIndex, limit = 2, minThreshold = 0.2) {
  const titleTokens = tokenize(entry.title);
  const scored = [];
  for (const section of existingIndex.bySection) {
    const similarity = jaccard(titleTokens, section.titleTokens);
    if (similarity >= minThreshold) {
      scored.push({ section, similarity });
    }
  }
  scored.sort((a, b) => b.similarity - a.similarity);
  return scored.slice(0, limit);
}

export function findSectionByTitle(targetTitle, existingIndex) {
  const targetKey = normalizeText(targetTitle);
  if (!targetKey) return null;
  for (const section of existingIndex.bySection) {
    if (section.titleKey === targetKey) return section;
  }
  return null;
}

export function formatEntry(entry, now) {
  const lines = [`## ${localTimeStamp(now)} - ${entry.title}`];
  for (const bullet of entry.bullets) {
    lines.push(`- ${bullet}`);
  }
  return lines.join("\n");
}

export const MERGE_MARKER_PREFIX = "(merged ";
export const MERGE_MARKER_RE = /^\(merged \d{2}:\d{2}\)$/;

export function makeMergeMarker(now) {
  return `(merged ${localTimeStamp(now)})`;
}

// Returns { newLines, addedBullets, newMarker } given the section, candidate bullets, and now.
// - skips bullets whose normalized form already exists in the section
// - replaces an existing (merged HH:MM) marker rather than stacking
export function spliceBulletsIntoSection(lines, section, candidateBullets, now) {
  const existingBulletKeys = new Set(
    section.bullets.map((bullet) => normalizeText(bullet)).filter(Boolean),
  );

  const newBullets = [];
  for (const bullet of candidateBullets) {
    const key = normalizeText(bullet);
    if (!key) continue;
    if (existingBulletKeys.has(key)) continue;
    existingBulletKeys.add(key);
    newBullets.push(bullet);
  }

  if (newBullets.length === 0) {
    return { newLines: lines, addedBullets: [], newMarker: null };
  }

  let endLine = section.endLine;
  let hadMarker = false;
  if (
    endLine > section.headingLine &&
    MERGE_MARKER_RE.test(lines[endLine].trimEnd().replace(/^- /, ""))
  ) {
    hadMarker = true;
    endLine -= 1;
  }

  const marker = makeMergeMarker(now);
  const inserted = [...newBullets.map((b) => `- ${b}`), `- ${marker}`];

  const before = lines.slice(0, endLine + 1);
  const after = hadMarker ? lines.slice(section.endLine + 1) : lines.slice(endLine + 1);
  const newLines = [...before, ...inserted, ...after];

  return { newLines, addedBullets: newBullets, newMarker: marker };
}
