import { createHash } from "node:crypto";

const GENERIC_NAMES = new Set(["未命名灵魂", "新生灵魂", "untitled soul", "new soul"]);

function normalizedText(value) {
  return String(value ?? "").replace(/\s+/g, " ").trim();
}

export function detectCreationLanguage(description) {
  const text = normalizedText(description);
  const hanCharacters = text.match(/\p{Script=Han}/gu)?.length ?? 0;
  const latinWords = text.match(/[A-Za-z]+(?:['-][A-Za-z]+)*/g)?.length ?? 0;
  return hanCharacters > 0 && hanCharacters / 2 >= latinWords ? "zh-CN" : "en";
}

function cleanName(value) {
  return normalizedText(value)
    .replace(/^[“”"'‘’《》]+|[“”"'‘’《》]+$/g, "")
    .replace(/[，。,.；;：:!?！？]+$/g, "")
    .trim()
    .slice(0, 120);
}

export function inferCreationName(description, language = detectCreationLanguage(description)) {
  const text = normalizedText(description);
  const quoted = text.match(/(?:名字(?:是|叫)?|名叫|叫做|叫作|称为|叫|named|called)\s*[“"'‘]([^”"'’]{2,32})[”"'’]/iu);
  if (quoted) return cleanName(quoted[1]);

  if (language === "zh-CN") {
    const chinese = text.match(/(?:名字(?:是|叫)?|名叫|叫做|叫作|称为|叫)\s*([\p{Script=Han}A-Za-z][\p{Script=Han}A-Za-z0-9·_-]{1,15}?)(?=的|[，。,.；;、\s]|$)/u);
    if (chinese) return cleanName(chinese[1]);
    return "未命名灵魂";
  }

  const english = text.match(/\b(?:named|called)\s+([\p{Lu}][\p{L}\p{N}'-]*(?:\s+[\p{Lu}][\p{L}\p{N}'-]*){0,2})/u);
  return english ? cleanName(english[1]) : "Untitled Soul";
}

export function createSoulSlug(name, description = "") {
  const normalizedName = normalizedText(name);
  const ascii = normalizedName
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .replace(/-{2,}/g, "-")
    .slice(0, 64)
    .replace(/-+$/g, "");
  const generic = GENERIC_NAMES.has(normalizedName.toLocaleLowerCase("en-US"));
  if (ascii && !generic) return ascii;
  const digest = createHash("sha256").update(`${normalizedName}\n${normalizedText(description)}`).digest("hex").slice(0, 10);
  return `soul-${digest}`;
}

export function inferAuditionProfiles(description) {
  const text = normalizedText(description);
  const profiles = [];
  if (/(陪伴|伙伴|倾诉|安慰|情绪|关系|亲密|朋友|恋人|家人|姐姐|哥哥|companion|emotional|comfort|relationship|intimate|friend|partner)/iu.test(text)) {
    profiles.push("emotional-companion");
  }
  if (/(工具|代码|编程|文件|任务|工作流|执行|搜索|tool|code|coding|file|workflow|execute|automation)/iu.test(text)) {
    profiles.push("tool-capable");
  }
  return profiles;
}

export function resolveCreationDefaults(input = {}) {
  const description = normalizedText(input.description ?? input.brief ?? "");
  const language = input.language || detectCreationLanguage(description);
  const name = cleanName(input.name) || inferCreationName(description, language);
  const slug = normalizedText(input.slug) || createSoulSlug(name, description);
  return {
    description,
    language,
    name,
    slug,
    profiles: inferAuditionProfiles(description),
  };
}
