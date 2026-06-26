import fs from "node:fs";
import path from "node:path";

export interface PromptBuildOptions {
  taskPromptFile: string;
  variables?: Record<string, unknown>;
  rootDir?: string;
}

function readText(filePath: string): string {
  return fs.readFileSync(filePath, "utf8").trim();
}

function resolveProjectRoot(rootDir?: string): string {
  if (rootDir) return rootDir;

  const currentDir = path.resolve(__dirname, "..");
  const promptsPath = path.join(currentDir, "prompts");

  if (fs.existsSync(promptsPath)) return currentDir;

  return path.resolve(currentDir, "..");
}

function render(template: string, variables: Record<string, unknown>): string {
  return template.replace(/{{\s*([a-zA-Z0-9_.-]+)\s*}}/g, (_, key: string) => {
    const value = variables[key];
    if (value === undefined || value === null) return "";
    if (Array.isArray(value)) return value.join("\n");
    if (typeof value === "object") return JSON.stringify(value, null, 2);
    return String(value);
  });
}

export function buildPrompt(options: PromptBuildOptions): string {
  const rootDir = resolveProjectRoot(options.rootDir);
  const promptsDir = path.join(rootDir, "prompts");
  const configDir = path.join(rootDir, "config");

  const systemPrompt = readText(path.join(promptsDir, "system-prompt.md"));
  const personaPrompt = readText(path.join(promptsDir, "persona.md"));
  const taskPrompt = readText(path.join(promptsDir, options.taskPromptFile));
  const personaConfig = JSON.parse(readText(path.join(configDir, "persona.json")));
  const platformsConfig = JSON.parse(readText(path.join(configDir, "platforms.json")));
  const stylesConfig = JSON.parse(readText(path.join(configDir, "styles.json")));
  const scriptStructuresConfig = JSON.parse(readText(path.join(configDir, "script-structures.json")));
  const scriptOutputProfilesConfig = JSON.parse(readText(path.join(configDir, "script-output-profiles.json")));
  const topicOutputProfilesConfig = JSON.parse(readText(path.join(configDir, "topic-output-profiles.json")));
  const complianceOutputProfilesConfig = JSON.parse(readText(path.join(configDir, "compliance-output-profiles.json")));
  const rewriteProfilesConfig = JSON.parse(readText(path.join(configDir, "rewrite-profiles.json")));

  const variables = {
    personaConfig,
    platformsConfig,
    stylesConfig,
    scriptStructuresConfig,
    scriptOutputProfilesConfig,
    topicOutputProfilesConfig,
    complianceOutputProfilesConfig,
    rewriteProfilesConfig,
    ...(options.variables ?? {}),
  };

  return [
    "# System",
    render(systemPrompt, variables),
    "",
    "# Persona",
    render(personaPrompt, variables),
    "",
    "# Task",
    render(taskPrompt, variables),
    "",
    "# Runtime Context",
    JSON.stringify(variables, null, 2),
  ].join("\n");
}
