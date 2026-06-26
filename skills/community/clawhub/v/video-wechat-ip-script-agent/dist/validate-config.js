#!/usr/bin/env node
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.validateAllConfigs = validateAllConfigs;
const configLoader_1 = require("./lib/configLoader");
function isRecord(value) {
    return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}
function assert(condition, message) {
    if (!condition)
        throw new Error(message);
}
function assertString(value, message) {
    assert(typeof value === "string" && value.trim().length > 0, message);
}
function assertStringArray(value, message) {
    assert(Array.isArray(value) && value.every((item) => typeof item === "string" && item.trim().length > 0), message);
}
function validateNamedProfiles(fileName, requiredArrayField) {
    const config = (0, configLoader_1.loadJsonConfig)(fileName);
    assert(isRecord(config) && Object.keys(config).length > 0, `${fileName} must be a non-empty object.`);
    for (const [profileName, profileValue] of Object.entries(config)) {
        assert(isRecord(profileValue), `${fileName}:${profileName} must be an object.`);
        const profile = profileValue;
        assertString(profile.name, `${fileName}:${profileName}.name must be a non-empty string.`);
        assertStringArray(profile[requiredArrayField], `${fileName}:${profileName}.${requiredArrayField} must be a non-empty string array.`);
    }
}
function validatePersona() {
    const config = (0, configLoader_1.loadJsonConfig)("persona.json");
    assertString(config.industry, "persona.json:industry must be a non-empty string.");
    assertString(config.tone, "persona.json:tone must be a non-empty string.");
    assertString(config.style, "persona.json:style must be a non-empty string.");
    assertStringArray(config.targetAudience, "persona.json:targetAudience must be a non-empty string array.");
}
function validatePlatforms() {
    const config = (0, configLoader_1.loadJsonConfig)("platforms.json");
    assert(isRecord(config) && Object.keys(config).length > 0, "platforms.json must be a non-empty object.");
    for (const [platformName, platformValue] of Object.entries(config)) {
        assert(isRecord(platformValue), `platforms.json:${platformName} must be an object.`);
        const platform = platformValue;
        assertStringArray(platform.features, `platforms.json:${platformName}.features must be a non-empty string array.`);
        assertString(platform.recommended_duration, `platforms.json:${platformName}.recommended_duration must be a non-empty string.`);
        assertString(platform.cover_text_rule, `platforms.json:${platformName}.cover_text_rule must be a non-empty string.`);
    }
}
function validateStyles() {
    const config = (0, configLoader_1.loadJsonConfig)("styles.json");
    const styles = config.styles;
    assert(Array.isArray(styles) && styles.length > 0, "styles.json:styles must be a non-empty array.");
    const styleList = styles;
    for (const [index, style] of styleList.entries()) {
        assert(isRecord(style), `styles.json:styles[${index}] must be an object.`);
        const styleRecord = style;
        assertString(styleRecord.name, `styles.json:styles[${index}].name must be a non-empty string.`);
        assertString(styleRecord.description, `styles.json:styles[${index}].description must be a non-empty string.`);
    }
}
function validateScriptStructures() {
    const config = (0, configLoader_1.loadJsonConfig)("script-structures.json");
    assert(isRecord(config) && Object.keys(config).length > 0, "script-structures.json must be a non-empty object.");
    for (const [name, value] of Object.entries(config)) {
        assert(isRecord(value), `script-structures.json:${name} must be an object.`);
        const structure = value;
        assertString(structure.name, `script-structures.json:${name}.name must be a non-empty string.`);
        assertStringArray(structure.steps, `script-structures.json:${name}.steps must be a non-empty string array.`);
        assertString(structure.rule, `script-structures.json:${name}.rule must be a non-empty string.`);
    }
}
function validateAllConfigs() {
    validatePersona();
    validatePlatforms();
    validateStyles();
    validateScriptStructures();
    validateNamedProfiles("script-output-profiles.json", "fields");
    validateNamedProfiles("topic-output-profiles.json", "fields");
    validateNamedProfiles("compliance-output-profiles.json", "fields");
    validateNamedProfiles("rewrite-profiles.json", "styles");
    const rewriteProfiles = (0, configLoader_1.loadJsonConfig)("rewrite-profiles.json");
    for (const [profileName, profileValue] of Object.entries(rewriteProfiles)) {
        assert(isRecord(profileValue), `rewrite-profiles.json:${profileName} must be an object.`);
        const profile = profileValue;
        assertStringArray(profile.fields, `rewrite-profiles.json:${profileName}.fields must be a non-empty string array.`);
    }
    return [
        "persona.json",
        "platforms.json",
        "styles.json",
        "script-structures.json",
        "script-output-profiles.json",
        "topic-output-profiles.json",
        "compliance-output-profiles.json",
        "rewrite-profiles.json",
    ];
}
function main() {
    const files = validateAllConfigs();
    process.stdout.write(`Config validation passed for ${files.length} files.\n`);
}
if (require.main === module) {
    try {
        main();
    }
    catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        process.stderr.write(`${message}\n`);
        process.exitCode = 1;
    }
}
