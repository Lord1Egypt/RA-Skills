// Reproduce the ERR_MODULE_NOT_FOUND logic from dsh's loader.
// dsh loader: when it sees `insert: { name: 'workled-dsh-plugin', path: 'C:/...' }`,
// it calls import('workled-dsh-plugin') from within <dsh-home>/profiles/web/.
// On Node.js ESM semantics, that bare specifier is resolved by walking UP the
// filesystem from the importer dir looking for node_modules/. It never looks
// inside <dsh-home>/plugins/ unless that directory is a node_modules/ and the
// name resolution reaches it via node_modules search, OR the import specifier
// is an absolute/prefixed path like `file:///C:/...`.
//
// So either:
//   A) `name` in the patch row must be an absolute `file:` path (not package name),
//      OR the package must be installed into <dsh-home>/node_modules/ via npm.
//   B) Or `import: workled-dsh-plugin` is resolved through a resolution entry
//      that cordis.patch.yml creates via `cordis:include` with a `path:`.
//
// The error trace says: `Cannot find package 'workled-dsh-plugin' imported from
// C:\Users\jiqia\.dsh\profiles\web\`. So the importer IS profiles/web and the
// loader is doing a bare-specifier import. Let's verify what happens if we
// call node's import from profiles/web with a bare name.

import { pathToFileURL } from "url";
import { join } from "path";
import { execFileSync } from "child_process";

// Test: can Node import bare 'workled-dsh-plugin' from profiles/web ?
const profilesWeb = join(process.env.APPDATA || "", "dsh", "profiles", "web");
// Instead of importing (which will fail and throw in the same process), use
// a child process that does `import.meta.resolve()` from that dir.
const script = `
import { pathToFileURL } from "url";
try {
  const u = await import.meta.resolve("workled-dsh-plugin", pathToFileURL(process.cwd() + "/").href);
  console.log("RESOLVED:", u);
} catch (e) {
  console.log("FAILED:", e.code, e.message.split("\\n")[0]);
}
`;
console.log("== Testing import.meta.resolve('workled-dsh-plugin') from profiles/web ==");
console.log(`cwd: ${profilesWeb}`);
try {
  const out = execFileSync(process.execPath, ["--input-type=module", "-e", script], {
    cwd: profilesWeb,
    encoding: "utf8",
  });
  console.log(out);
} catch (e) {
  console.log("err:", e.stdout || e.message);
}

// Test 2: absolute file:// import of the plugin path (what we want)
console.log("\n== Testing absolute file:// import ==");
const pluginDir = join(process.env.APPDATA || "", "dsh", "plugins", "workled");
const script2 = `
const url = ${JSON.stringify(pathToFileURL(join(pluginDir, "src", "index.js")).href)};
try {
  const m = await import(url);
  console.log("OK: module keys:", Object.keys(m).join(", ") || "(none)");
} catch (e) {
  console.log("FAILED:", e.code, e.message.split("\\n")[0]);
}
`;
try {
  const out = execFileSync(process.execPath, ["--input-type=module", "-e", script2], {
    encoding: "utf8",
  });
  console.log(out);
} catch (e) {
  console.log("err:", e.stdout || e.message);
}
