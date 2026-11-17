"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.MissingConfigPathError = exports.HostQueryError = void 0;
exports.findOpenClawCli = findOpenClawCli;
exports.parseCliJson = parseCliJson;
exports.runOpenClawJson = runOpenClawJson;
exports.readAgentLocations = readAgentLocations;
const fs = __importStar(require("node:fs"));
const path = __importStar(require("node:path"));
const node_child_process_1 = require("node:child_process");
class HostQueryError extends Error {
    code = "HOST_QUERY_FAILED";
}
exports.HostQueryError = HostQueryError;
class MissingConfigPathError extends HostQueryError {
}
exports.MissingConfigPathError = MissingConfigPathError;
/** Locate a trusted installed Node CLI entry; never execute a shell wrapper with user text. */
function findOpenClawCli(env = process.env) {
    if (env.OPENCLAW_CLI_PATH) {
        const entry = path.resolve(env.OPENCLAW_CLI_PATH);
        try {
            if (!fs.statSync(entry).isFile())
                throw new Error();
        }
        catch {
            throw new HostQueryError("OPENCLAW_CLI_PATH must identify the installed Node CLI entry.");
        }
        return entry;
    }
    const dirs = [path.dirname(process.execPath), ...(env.PATH ?? env.Path ?? "").split(path.delimiter)];
    for (const dir of dirs.filter(Boolean)) {
        for (const candidate of [path.join(dir, "node_modules/openclaw/openclaw.mjs"), path.join(dir, "openclaw.mjs"), path.join(dir, "openclaw")]) {
            try {
                if (!fs.statSync(candidate).isFile())
                    continue;
                const real = fs.realpathSync(candidate);
                // PATH can contain a shell forwarding wrapper, especially with nvm.
                if (/\.[cm]?js$/.test(real))
                    return real;
                const fd = fs.openSync(real, "r");
                try {
                    const header = Buffer.alloc(128);
                    const length = fs.readSync(fd, header, 0, header.length, 0);
                    if (/^#![^\r\n]*\bnode\b/.test(header.toString("utf8", 0, length)))
                        return real;
                }
                finally {
                    fs.closeSync(fd);
                }
            }
            catch { /* Try next installed bin. */ }
        }
    }
    throw new HostQueryError("OpenClaw CLI entry was not found; install it on PATH or set OPENCLAW_CLI_PATH to openclaw.mjs.");
}
function parseCliJson(raw) {
    try {
        return JSON.parse(raw);
    }
    catch {
        // A CLI startup notice may precede JSON. Do not accept arbitrary trailing output.
        for (const match of raw.matchAll(/^[\[{]/gm)) {
            try {
                return JSON.parse(raw.slice(match.index));
            }
            catch { /* Keep looking for the result boundary. */ }
        }
        throw new HostQueryError("OpenClaw did not return valid JSON.");
    }
}
async function runOpenClawJson(args) {
    const entry = findOpenClawCli();
    return new Promise((resolve, reject) => {
        const child = (0, node_child_process_1.spawn)(process.execPath, [entry, ...args], { shell: false, windowsHide: true, stdio: ["ignore", "pipe", "pipe"] });
        let output = "", diagnostics = "", bytes = 0, settled = false;
        const finish = (error) => {
            if (settled)
                return;
            settled = true;
            clearTimeout(timer);
            if (error)
                reject(error);
            else {
                try {
                    resolve(parseCliJson(output));
                }
                catch (e) {
                    reject(e);
                }
            }
        };
        const timer = setTimeout(() => { child.kill(); finish(new HostQueryError("OpenClaw metadata query timed out.")); }, 120000);
        child.stdout.setEncoding("utf8");
        child.stdout.on("data", (data) => {
            bytes += Buffer.byteLength(data);
            if (bytes > 32 * 1024 * 1024) {
                child.kill();
                finish(new HostQueryError("OpenClaw metadata result is too large."));
            }
            else
                output += data;
        });
        // Inspect only a bounded diagnostic; never expose raw config/provider output.
        child.stderr.setEncoding("utf8");
        child.stderr.on("data", (data) => { if (diagnostics.length < 8192)
            diagnostics += data.slice(0, 8192 - diagnostics.length); });
        child.once("error", () => finish(new HostQueryError("OpenClaw CLI could not be started.")));
        child.once("close", code => {
            const missingSkills = args.length === 4 && args.join(" ") === "config get skills --json" &&
                /^Config path not found: skills\s*$/m.test(diagnostics);
            finish(code === 0 ? undefined : missingSkills ? new MissingConfigPathError("Optional skills configuration is absent.")
                : new HostQueryError("OpenClaw metadata query failed; check host configuration and access."));
        });
    });
}
async function readAgentLocations() {
    const value = await runOpenClawJson(["agents", "list", "--json"]);
    if (!Array.isArray(value) || !value.every(a => a && typeof a.id === "string" &&
        typeof a.workspace === "string" && path.isAbsolute(a.workspace) && typeof a.agentDir === "string" && path.isAbsolute(a.agentDir))) {
        throw new HostQueryError("Unsupported OpenClaw agents list result.");
    }
    return value.map(a => ({ id: a.id, workspace: a.workspace, agentDir: a.agentDir }));
}
//# sourceMappingURL=native-cli.js.map