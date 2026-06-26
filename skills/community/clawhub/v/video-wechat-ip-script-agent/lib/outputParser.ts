export function safeJsonParse<T>(raw: string): T | null {
  const candidates = extractJsonCandidates(raw);
  for (const candidate of candidates) {
    try {
      return JSON.parse(candidate) as T;
    } catch {
      // continue
    }
  }
  return null;
}

export function extractJsonCandidates(raw: string): string[] {
  const candidates: string[] = [];
  const trimmed = raw.trim();
  candidates.push(trimmed);

  const fencedMatch = trimmed.match(/```(?:json)?\s*([\s\S]*?)```/i);
  if (fencedMatch?.[1]) {
    candidates.push(fencedMatch[1].trim());
  }

  const firstBrace = trimmed.indexOf("{");
  const lastBrace = trimmed.lastIndexOf("}");
  if (firstBrace >= 0 && lastBrace > firstBrace) {
    candidates.push(trimmed.slice(firstBrace, lastBrace + 1));
  }

  const firstBracket = trimmed.indexOf("[");
  const lastBracket = trimmed.lastIndexOf("]");
  if (firstBracket >= 0 && lastBracket > firstBracket) {
    candidates.push(trimmed.slice(firstBracket, lastBracket + 1));
  }

  return Array.from(new Set(candidates));
}

export function normalizeStringArray(input: unknown): string[] {
  if (Array.isArray(input)) {
    return input.map((item) => String(item).trim()).filter(Boolean);
  }
  if (typeof input === "string") {
    return input
      .split(/\n|\||,|；|;/)
      .map((item) => item.replace(/^[-*\d.\s]+/, "").trim())
      .filter(Boolean);
  }
  return [];
}

export function normalizeMultilineString(input: unknown): string {
  if (typeof input === "string") return input.trim();
  if (Array.isArray(input)) return input.map((item) => String(item)).join("\n").trim();
  if (input && typeof input === "object") return JSON.stringify(input, null, 2);
  return "";
}
