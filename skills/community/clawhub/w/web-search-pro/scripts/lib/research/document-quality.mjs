const INTERSTITIAL_PATTERNS = Object.freeze([
  /just a moment/i,
  /verify you are human/i,
  /enable javascript and cookies/i,
  /checking your browser/i,
  /attention required/i,
  /security check/i,
  /cloudflare/i,
]);

const BOILERPLATE_LINE_PATTERNS = Object.freeze([
  /^skip to (main )?content$/i,
  /^main navigation$/i,
  /^search docs$/i,
  /^table of contents$/i,
  /^on this page$/i,
  /^menu$/i,
  /^navigation$/i,
  /^previous$/i,
  /^next$/i,
  /^terms$/i,
  /^privacy$/i,
  /^cookies?$/i,
  /^all rights reserved$/i,
  /^sign in$/i,
  /^log in$/i,
  /^sign up$/i,
  /^try for free$/i,
]);

const INLINE_BOILERPLATE_PATTERNS = Object.freeze([
  /\bskip to (main )?content\b/gi,
  /\bmain navigation\b/gi,
  /\bsearch docs\b/gi,
  /\btable of contents\b/gi,
  /\bon this page\b/gi,
  /\bterms\b/gi,
  /\bprivacy\b/gi,
  /\bcookies?\b/gi,
]);

function normalizeWhitespace(value = "") {
  return String(value ?? "").replace(/\r/g, "").replace(/\t/g, " ").trim();
}

function stripMarkdownArtifacts(value = "") {
  return String(value ?? "")
    .replace(/!\[([^\]]*)\]\([^)]+\)/g, " $1 ")
    .replace(/\[([^\]]*)\]\([^)]+\)/g, (_, label) => ` ${String(label ?? "").trim()} `)
    .replace(/^[*-]\s+/gm, "")
    .replace(/[`>#]+/g, " ");
}

function splitIntoLines(value = "") {
  return normalizeWhitespace(stripMarkdownArtifacts(value))
    .split(/\n+/)
    .map((line) => line.replace(/\s+/g, " ").trim())
    .filter(Boolean);
}

function stripInlineBoilerplate(value = "") {
  let text = normalizeWhitespace(value);
  for (const pattern of INLINE_BOILERPLATE_PATTERNS) {
    text = text.replace(pattern, " ");
  }
  return text.replace(/\s+/g, " ").trim();
}

function cleanResearchText(value = "") {
  const raw = normalizeWhitespace(value);
  if (!raw) {
    return {
      cleanedText: "",
      boilerplateRatio: 0,
      removedChars: 0,
    };
  }

  const lines = splitIntoLines(raw);
  const seen = new Set();
  const kept = [];
  let removedChars = 0;

  for (const line of lines) {
    const normalizedLine = stripInlineBoilerplate(line);
    if (!normalizedLine) {
      removedChars += line.length;
      continue;
    }
    if (BOILERPLATE_LINE_PATTERNS.some((pattern) => pattern.test(normalizedLine))) {
      removedChars += line.length;
      continue;
    }
    const dedupeKey = normalizedLine.toLowerCase();
    if (seen.has(dedupeKey)) {
      removedChars += line.length;
      continue;
    }
    seen.add(dedupeKey);
    kept.push(normalizedLine);
  }

  const cleanedText = kept.join("\n").trim();
  const denominator = Math.max(raw.length, 1);
  const ratio = Math.max(0, Math.min(1, (denominator - cleanedText.length) / denominator));
  return {
    cleanedText,
    boilerplateRatio: Number(ratio.toFixed(3)),
    removedChars: Math.max(0, raw.length - cleanedText.length),
  };
}

function detectInterstitial(value = "") {
  const text = normalizeWhitespace(value);
  if (!text) {
    return false;
  }
  return INTERSTITIAL_PATTERNS.some((pattern) => pattern.test(text));
}

function analyzeStructure(value = "") {
  const rawLines = normalizeWhitespace(value)
    .split(/\n+/)
    .map((line) => line.trim())
    .filter(Boolean);
  if (rawLines.length === 0) {
    return {
      listHeavy: false,
      sentenceLikeLines: 0,
    };
  }

  let linkishLines = 0;
  let sentenceLikeLines = 0;
  for (const line of rawLines) {
    if (/\[[^\]]*\]\([^)]+\)/.test(line) || /^[*-]\s+/.test(line)) {
      linkishLines += 1;
    }
    const cleanedLine = stripInlineBoilerplate(stripMarkdownArtifacts(line));
    if (/[.!?]/.test(cleanedLine) && cleanedLine.split(/\s+/).length >= 6) {
      sentenceLikeLines += 1;
    }
  }

  return {
    listHeavy: rawLines.length >= 4 && linkishLines / rawLines.length >= 0.5,
    sentenceLikeLines,
  };
}

function hasPrimaryContentByKind(taskKind, cleanedContent, cleanedSnippet, cleanedTitle, structure) {
  const contentLength = cleanedContent.length;
  const snippetLength = cleanedSnippet.length;
  const titleLength = cleanedTitle.length;

  if (taskKind === "map") {
    return titleLength > 0;
  }
  if (structure.listHeavy && structure.sentenceLikeLines === 0) {
    return false;
  }
  if (taskKind === "search") {
    return (
      snippetLength >= 20 ||
      (contentLength >= 20 && structure.sentenceLikeLines >= 1) ||
      titleLength >= 24
    );
  }
  return (
    (contentLength >= 60 && structure.sentenceLikeLines >= 1) ||
    (snippetLength >= 40 && structure.sentenceLikeLines >= 1)
  );
}

function inferDocumentQuality({
  taskKind,
  interstitial,
  hasPrimaryContent,
  cleanedContent,
  cleanedSnippet,
  boilerplateRatio,
  structure,
}) {
  if (interstitial) {
    return "low";
  }
  if (structure.listHeavy && structure.sentenceLikeLines === 0) {
    return "low";
  }
  if (!hasPrimaryContent && boilerplateRatio >= 0.4) {
    return "low";
  }

  const usableLength = Math.max(cleanedContent.length, cleanedSnippet.length);
  if (taskKind === "search") {
    if (hasPrimaryContent && usableLength >= 20 && boilerplateRatio <= 0.4) {
      return "high";
    }
    return hasPrimaryContent ? "medium" : "low";
  }

  if (hasPrimaryContent && usableLength >= 60 && boilerplateRatio <= 0.55) {
    return "high";
  }
  if (hasPrimaryContent) {
    return "medium";
  }
  return "low";
}

export function assessResearchDocumentQuality({
  taskKind = "search",
  title = "",
  snippet = "",
  content = "",
} = {}) {
  const cleanedTitle = stripInlineBoilerplate(title);
  const snippetQuality = cleanResearchText(snippet);
  const contentQuality = cleanResearchText(content);
  const interstitial = detectInterstitial(`${title}\n${snippet}\n${content}`);
  const structure = analyzeStructure(content || snippet);
  const boilerplateRatio = Math.max(
    snippetQuality.boilerplateRatio,
    contentQuality.boilerplateRatio,
  );
  const hasPrimaryContent = hasPrimaryContentByKind(
    taskKind,
    contentQuality.cleanedText,
    snippetQuality.cleanedText,
    cleanedTitle,
    structure,
  );
  const documentQuality = inferDocumentQuality({
    taskKind,
    interstitial,
    hasPrimaryContent,
    cleanedContent: contentQuality.cleanedText,
    cleanedSnippet: snippetQuality.cleanedText,
    boilerplateRatio,
    structure,
  });

  return {
    interstitial,
    cleanedTitle,
    cleanedSnippet: snippetQuality.cleanedText,
    cleanedContent: contentQuality.cleanedText,
    boilerplateRatio,
    hasPrimaryContent,
    documentQuality,
    listHeavy: structure.listHeavy,
  };
}
