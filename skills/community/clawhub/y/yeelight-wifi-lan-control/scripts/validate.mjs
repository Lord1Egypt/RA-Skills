#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const errors = [];

const required = [
  "SKILL.md",
  "agents/openai.yaml",
  "assets/protocol-catalog.json",
  "scripts/invoke.sh",
  "scripts/invoke.ps1",
  "scripts/invoke.mjs",
  "scripts/runtime-manifest.json",
];
for (const relative of required) {
  if (!fs.existsSync(path.join(root, relative))) errors.push(`missing ${relative}`);
}

const skill = readText("SKILL.md");
if (!/^---\nname:\s+yeelight-wifi-lan-control\n/.test(skill)) errors.push("invalid SKILL.md frontmatter");
if (skill.split(/\r?\n/).length > 500) errors.push("SKILL.md exceeds 500 lines");
if (skill.includes("[TODO:")) errors.push("SKILL.md contains TODO");

const yaml = readText("agents/openai.yaml");
for (const token of ["display_name:", "short_description:", "default_prompt:", "$yeelight-wifi-lan-control", "allow_implicit_invocation: true"]) {
  if (!yaml.includes(token)) errors.push(`agents/openai.yaml missing ${token}`);
}

const catalog = readJSON("assets/protocol-catalog.json");
if (!Array.isArray(catalog.methods) || catalog.methods.length !== 35) errors.push("catalog must contain 35 methods");
if (!Array.isArray(catalog.properties) || catalog.properties.length !== 25) errors.push("catalog must contain 25 properties");
if (new Set((catalog.methods || []).map((method) => method.name)).size !== 35) errors.push("catalog method names must be unique");
if (new Set((catalog.properties || []).map((property) => property.name)).size !== 25) errors.push("catalog property names must be unique");

const manifest = readJSON("scripts/runtime-manifest.json");
if (manifest?.network?.localOnly !== true || manifest?.scheduler?.osInstallation !== false) {
  errors.push("runtime manifest must be local-only and forbid OS scheduler installation");
}

const forbiddenDataNames = /(?:store-v\d+\.json|recovery|snapshot|schedule)\.(?:json|log)$/i;
for (const file of walk(root)) {
  const relative = path.relative(root, file).split(path.sep).join("/");
  if (forbiddenDataNames.test(relative) && !relative.startsWith("assets/")) errors.push(`generated data file shipped: ${relative}`);
}

if (errors.length) {
  console.error(JSON.stringify({ ok: false, errors }, null, 2));
  process.exitCode = 1;
} else {
  console.log(JSON.stringify({ ok: true, skill: "yeelight-wifi-lan-control", methods: 35, properties: 25 }, null, 2));
}

function readText(relative) {
  const file = path.join(root, relative);
  try { return fs.readFileSync(file, "utf8"); } catch { return ""; }
}

function readJSON(relative) {
  try { return JSON.parse(readText(relative)); } catch (error) {
    errors.push(`invalid JSON ${relative}: ${error.message}`);
    return {};
  }
}

function walk(directory) {
  const result = [];
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const current = path.join(directory, entry.name);
    if (entry.isSymbolicLink()) { errors.push(`symlink not allowed: ${path.relative(root, current)}`); continue; }
    if (entry.isDirectory()) result.push(...walk(current));
    else result.push(current);
  }
  return result;
}
