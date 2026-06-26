import fs from "node:fs/promises";
import path from "node:path";
import { HttpError } from "./errors.js";

function isObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

export async function loadRegistry(templatesDir) {
  const actions = new Map();
  const resolvedDir = path.resolve(templatesDir);
  const entries = await fs.readdir(resolvedDir, { withFileTypes: true });

  for (const entry of entries) {
    if (!entry.isFile() || !entry.name.endsWith(".json")) continue;
    const filePath = path.join(resolvedDir, entry.name);
    const raw = await fs.readFile(filePath, "utf-8");
    const json = JSON.parse(raw);

    if (!json || typeof json.name !== "string" || !json.name) {
      throw new Error(`Invalid template ${entry.name}: missing name`);
    }
    if (!json.host || !json.path) {
      throw new Error(`Invalid template ${entry.name}: missing host/path`);
    }
    if (json.enabled === false) continue;

    actions.set(json.name, { template: json });
  }

  return {
    actions,
    list: () =>
      Array.from(actions.values()).map((a) => ({
        name: a.template.name,
        label: a.template.label,
        description: a.template.description,
        querySchema: a.template.querySchema,
        bodySchema: a.template.bodySchema,
        pathParams: a.template.pathParams,
        headerSchema: a.template.headerSchema,
        tags: a.template.tags,
        version: a.template.version
      }))
  };
}

export function requireAction(registry, name) {
  const action = registry.actions.get(name);
  if (!action) {
    throw new HttpError(404, `Unknown action: ${name}`);
  }
  return action;
}

export function extractParams(input, schema) {
  const out = {};
  if (!schema) return out;
  if (!isObject(schema)) {
    throw new HttpError(400, "Invalid schema format");
  }
  for (const [key, rules] of Object.entries(schema)) {
    const value = input[key] ?? rules?.default;
    if (value === undefined || value === null) {
      if (rules?.required) {
        throw new HttpError(400, `Missing required parameter: ${key}`);
      }
      continue;
    }
    out[key] = value;
  }
  return out;
}

export function applyParamMapping(input, mapping) {
  const buckets = { query: {}, body: {}, path: {}, header: {} };
  if (!mapping) return buckets;
  if (!isObject(mapping)) {
    throw new HttpError(400, "Invalid paramMapping format");
  }
  for (const [inputKey, target] of Object.entries(mapping)) {
    const value = input[inputKey];
    if (value === undefined) continue;
    const [bucket, field] = String(target).split(".");
    if (!bucket || !field || !buckets[bucket]) {
      throw new HttpError(400, `Invalid paramMapping target: ${target}`);
    }
    buckets[bucket][field] = value;
  }
  return buckets;
}

export function applyPathParams(pathTemplate, params) {
  let out = pathTemplate;
  for (const [key, value] of Object.entries(params || {})) {
    out = out.replace(`{${key}}`, encodeURIComponent(String(value)));
  }
  return out;
}
