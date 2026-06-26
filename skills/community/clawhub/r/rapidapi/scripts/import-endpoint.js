import fs from "node:fs/promises";
import path from "node:path";

function readStdin() {
  return new Promise((resolve, reject) => {
    let data = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => (data += chunk));
    process.stdin.on("end", () => resolve(data));
    process.stdin.on("error", reject);
  });
}

function toSnake(name) {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "_")
    .replace(/^_+|_+$/g, "")
    .replace(/_+/g, "_");
}

function parseEndpoint(payload) {
  if (!payload) throw new Error("Missing payload");
  const endpoint = payload.endpoint || payload.data?.endpoint || payload;
  if (!endpoint || !endpoint.method || !endpoint.route) {
    throw new Error("Missing endpoint.method or endpoint.route");
  }
  return endpoint;
}

const raw = await readStdin();
if (!raw) {
  console.error("Expected JSON input via stdin");
  process.exit(2);
}

let input;
try {
  input = JSON.parse(raw);
} catch (_err) {
  console.error("Invalid JSON input");
  process.exit(2);
}

const endpoint = parseEndpoint(input);
const host = input.host || input.rapidApiHost || input.rapidapiHost;
if (!host) {
  console.error("Missing host. Provide {\"host\":\"api-host.p.rapidapi.com\"} at top-level.");
  process.exit(2);
}

const querySchema = {};
const params = endpoint.params?.parameters || [];
for (const p of params) {
  if (!p || !p.name) continue;
  const required = String(p.condition || "").toUpperCase() === "REQUIRED";
  const type = String(p.paramType || "STRING").toLowerCase();
  querySchema[p.name] = {
    type: ["string", "number", "boolean", "object", "array"].includes(type) ? type : "string",
    required,
    description: p.description || ""
  };
  if (!required && p.value !== undefined && p.value !== "") {
    querySchema[p.name].default = p.value;
  }
}

const name = toSnake(endpoint.name || endpoint.route || "endpoint");
const template = {
  name,
  label: endpoint.name || name,
  description: endpoint.description || "",
  host,
  path: endpoint.route,
  method: String(endpoint.method).toUpperCase(),
  querySchema,
  response: {
    type: "json"
  }
};

const templatesDir = path.resolve("./templates");
await fs.mkdir(templatesDir, { recursive: true });
const filePath = path.join(templatesDir, `${name}.json`);
await fs.writeFile(filePath, JSON.stringify(template, null, 2));

console.log(JSON.stringify({ ok: true, file: filePath, name }, null, 2));
