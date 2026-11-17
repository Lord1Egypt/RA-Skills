// Fuzz: try several plausible patch formats with a cordis:include row for
// an absolute path plugin. This script does not run cordis — it writes each
// candidate to cordis.patch.yml and prints the diff, then the user runs
// `npx @deepseek-ai/dsh web` to test.

// The only facts we have from the error stack:
//   1) dsh loader creates a "cordis:include" loader entry for each `- insert:`
//      row that carries a plugin module.
//   2) The import specifier it uses is `name`, and the error says
//      "Cannot find package 'workled-dsh-plugin' imported from profiles/web/".
//   3) Therefore: `name` is being handed to the loader as a bare Node.js specifier,
//      so we must either:
//        a) make the specifier resolve (npm install into dsh/node_modules), OR
//        b) make `name` itself be a resolvable URL (absolute file:// or path).
//
// This test tries option (b) variants + documents option (a).
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "fs";
import { join } from "path";
import { dshHome } from "../utils.js";

const home = dshHome();
const profilesWeb = join(home, "profiles", "web");
mkdirSync(profilesWeb, { recursive: true });
const patchFile = join(profilesWeb, "cordis.patch.yml");
const pluginDir = join(home, "plugins", "workled").replace(/\\/g, "/");
const pluginFile = join(home, "plugins", "workled", "src", "index.js").replace(/\\/g, "/");
const url = process.env.WORKLED_MCP_URL || "http://192.168.31.146:18791/mcp";

const candidates = [
  {
    name: "v1: name=bare + path=dir (CURRENT, fails with ERR_MODULE_NOT_FOUND)",
    body: `# Your patch layer for this dsh profile.\n- insert:\n    - id: workled\n      name: 'workled-dsh-plugin'\n      path: '${pluginDir}'\n      config:\n        url: '${url}'\n        timeout: 1500\n        enabled: true\n`,
  },
  {
    name: "v2: name=absolute file:// URL to plugin src/index.js",
    body: `# Your patch layer for this dsh profile.\n- insert:\n    - id: workled\n      name: 'file:///${pluginFile}'\n      path: '${pluginDir}'\n      config:\n        url: '${url}'\n        timeout: 1500\n        enabled: true\n`,
  },
  {
    name: "v3: name=absolute Windows path with forward slashes",
    body: `# Your patch layer for this dsh profile.\n- insert:\n    - id: workled\n      name: '${pluginFile}'\n      path: '${pluginDir}'\n      config:\n        url: '${url}'\n        timeout: 1500\n        enabled: true\n`,
  },
  {
    name: "v4: include: directive on outer (cordis:include target spec)",
    body: `# Your patch layer for this dsh profile.\n- include:\n    - id: workled\n      name: 'workled-dsh-plugin'\n      path: '${pluginDir}'\n      config:\n        url: '${url}'\n        timeout: 1500\n        enabled: true\n`,
  },
  {
    name: "v5: insert + import (cordis 'import:' path specifier)",
    body: `# Your patch layer for this dsh profile.\n- insert:\n    - id: workled\n      import: 'file:///${pluginFile}'\n      path: '${pluginDir}'\n      config:\n        url: '${url}'\n        timeout: 1500\n        enabled: true\n`,
  },
  {
    name: "v6: insert + path=file with name dropped entirely",
    body: `# Your patch layer for this dsh profile.\n- insert:\n    - id: workled\n      path: '${pluginFile}'\n      config:\n        url: '${url}'\n        timeout: 1500\n        enabled: true\n`,
  },
];

// Print candidates with header line; user can then paste each body into
// cordis.patch.yml and run `npx @deepseek-ai/dsh web` to check.
console.log("=== dsh cordis.patch.yml candidate formats (6 variants) ===\n");
for (const c of candidates) {
  console.log(`#### ${c.name}`);
  console.log(c.body);
  console.log("");
}

// Default: write v2 (file:// specifier) so user can test immediately.
const chosen = candidates[1];
console.log(`\n>> Writing variant: ${chosen.name}\n>> to ${patchFile}`);
writeFileSync(patchFile, chosen.body, "utf8");
console.log(">> Now run: npx @deepseek-ai/dsh web");
console.log(">> If it still fails, paste variants v3..v6 into cordis.patch.yml one by one.");
