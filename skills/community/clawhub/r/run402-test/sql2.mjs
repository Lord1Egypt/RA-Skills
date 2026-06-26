import { readFileSync, existsSync } from "fs";
import { join } from "path";
import { homedir } from "os";

const API = "https://api.run402.com";
const CONFIG_DIR = join(homedir(), ".config", "run402");

const projects = JSON.parse(readFileSync(join(CONFIG_DIR, "projects.json"), "utf-8"));
const p = projects.find(x => x.project_id === process.argv[2]);
const headers = Object.fromEntries([["Content-Type","text/plain"],["Authorization",["Bearer", p.service_key].join(" ")]]);

const res = await fetch(`${API}/admin/v1/projects/${process.argv[2]}/sql`, {
  method: "POST", headers, body: process.argv.slice(3).join(" ")
});
console.log(JSON.stringify(await res.json(), null, 2));
