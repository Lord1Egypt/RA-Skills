"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.buildPrompt = buildPrompt;
const node_fs_1 = __importDefault(require("node:fs"));
const node_path_1 = __importDefault(require("node:path"));
function readText(filePath) {
    return node_fs_1.default.readFileSync(filePath, "utf8").trim();
}
function resolveProjectRoot(rootDir) {
    if (rootDir)
        return rootDir;
    const currentDir = node_path_1.default.resolve(__dirname, "..");
    const promptsPath = node_path_1.default.join(currentDir, "prompts");
    if (node_fs_1.default.existsSync(promptsPath))
        return currentDir;
    return node_path_1.default.resolve(currentDir, "..");
}
function render(template, variables) {
    return template.replace(/{{\s*([a-zA-Z0-9_.-]+)\s*}}/g, (_, key) => {
        const value = variables[key];
        if (value === undefined || value === null)
            return "";
        if (Array.isArray(value))
            return value.join("\n");
        if (typeof value === "object")
            return JSON.stringify(value, null, 2);
        return String(value);
    });
}
function buildPrompt(options) {
    const rootDir = resolveProjectRoot(options.rootDir);
    const promptsDir = node_path_1.default.join(rootDir, "prompts");
    const configDir = node_path_1.default.join(rootDir, "config");
    const systemPrompt = readText(node_path_1.default.join(promptsDir, "system-prompt.md"));
    const personaPrompt = readText(node_path_1.default.join(promptsDir, "persona.md"));
    const taskPrompt = readText(node_path_1.default.join(promptsDir, options.taskPromptFile));
    const personaConfig = JSON.parse(readText(node_path_1.default.join(configDir, "persona.json")));
    const platformsConfig = JSON.parse(readText(node_path_1.default.join(configDir, "platforms.json")));
    const stylesConfig = JSON.parse(readText(node_path_1.default.join(configDir, "styles.json")));
    const scriptStructuresConfig = JSON.parse(readText(node_path_1.default.join(configDir, "script-structures.json")));
    const scriptOutputProfilesConfig = JSON.parse(readText(node_path_1.default.join(configDir, "script-output-profiles.json")));
    const topicOutputProfilesConfig = JSON.parse(readText(node_path_1.default.join(configDir, "topic-output-profiles.json")));
    const complianceOutputProfilesConfig = JSON.parse(readText(node_path_1.default.join(configDir, "compliance-output-profiles.json")));
    const rewriteProfilesConfig = JSON.parse(readText(node_path_1.default.join(configDir, "rewrite-profiles.json")));
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
