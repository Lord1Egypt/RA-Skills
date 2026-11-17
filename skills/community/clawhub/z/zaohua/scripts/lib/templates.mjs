import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { FORGE_NAME, FORGE_VERSION, RUNTIME_FILES, SOUL6_URL, SOUL6_VERSION } from "./constants.mjs";
import { resolveCreationDefaults } from "./creation-defaults.mjs";
import { assertEmptyDirectory, assertSlug, normalizeLanguage, writeJson, writeText } from "./files.mjs";
import { writePackageReadme } from "./readme.mjs";

const currentDirectory = path.dirname(fileURLToPath(import.meta.url));
const skillDirectory = path.resolve(currentDirectory, "..", "..");

function replaceKnownTokens(content, values) {
  return content
    .replaceAll("{{NAME}}", values.name)
    .replaceAll("{{SLUG}}", values.slug)
    .replaceAll("{{BRIEF}}", values.brief);
}

export async function initializePackage(outputDirectory, input) {
  const defaults = resolveCreationDefaults(input);
  const name = defaults.name;
  if (!name || name.length < 2 || name.length > 120) throw new Error("Name must contain 2 to 120 characters.");
  const slug = assertSlug(defaults.slug);
  const language = normalizeLanguage(defaults.language);
  const provenanceMode = input.provenance ?? "original";
  if (!["original", "authorized", "inspired"].includes(provenanceMode)) throw new Error(`Unsupported provenance mode: ${provenanceMode}`);
  const authorization = input.authorization?.trim() || null;
  if (provenanceMode === "authorized" && !authorization) throw new Error("Authorized provenance requires --authorization.");
  const brief = input.brief?.trim() || defaults.description || (language === "zh-CN" ? "根据用户描述在纯本地环境创建。" : "Created locally from the user's description.");
  await assertEmptyDirectory(outputDirectory);
  const templateDirectory = path.join(skillDirectory, "assets", "templates", language);
  const values = { name, slug, brief };

  for (const file of [...RUNTIME_FILES, "forge-report.md"]) {
    const template = await readFile(path.join(templateDirectory, file), "utf8");
    await writeText(path.join(outputDirectory, file), replaceKnownTokens(template, values));
  }

  const manifest = {
    schemaVersion: "aisoul.package.v1",
    artifactType: "AISOUL",
    name,
    slug,
    version: input.version ?? "0.1.0",
    language,
    license: input.license ?? "UNLICENSED",
    offline: true,
    entrypoints: {
      identity: "IDENTITY.md",
      user: "USER.md",
      soul: "SOUL.md",
      agents: "AGENTS.md",
      tools: "TOOLS.md",
      memory: "MEMORY.md",
    },
    standards: [{ name: "SOUL-6", version: SOUL6_VERSION, profile: "canonical", source: "AISoulHub.io", url: SOUL6_URL }],
    provenance: { mode: provenanceMode, summary: brief, authorization, sources: [] },
    generator: { name: FORGE_NAME, version: FORGE_VERSION, offline: true, host: input.host?.trim() || null },
    artifacts: {
      readme: "README.md",
      soul6Report: "soul6-report.json",
      qualityCheck: "quality-check.md",
      forgeReport: "forge-report.md",
      auditionSuite: "auditions/suite.json",
      auditionReport: "auditions/report.json",
    },
    createdAt: new Date().toISOString(),
  };
  await writeJson(path.join(outputDirectory, "manifest.json"), manifest);
  await writeText(path.join(outputDirectory, "CHANGELOG.md"), [
    "# Changelog",
    "",
    `## ${manifest.version}`,
    "",
    language === "zh-CN" ? "- 创建本地 AI 灵魂包脚手架。" : "- Created the local AI Soul package scaffold.",
  ].join("\n"));
  await writePackageReadme(outputDirectory);
  return manifest;
}
