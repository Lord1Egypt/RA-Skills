#!/usr/bin/env node
"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const node_fs_1 = require("node:fs");
const node_path_1 = __importDefault(require("node:path"));
const index_1 = require("./index");
function readStdin() {
    return new Promise((resolve, reject) => {
        let data = "";
        process.stdin.setEncoding("utf8");
        process.stdin.on("data", (chunk) => {
            data += chunk;
        });
        process.stdin.on("end", () => resolve(data));
        process.stdin.on("error", reject);
    });
}
function parseArgs(argv) {
    const args = {};
    for (let index = 0; index < argv.length; index += 1) {
        const current = argv[index];
        if (current === "--input")
            args.input = argv[index + 1];
        if (current === "--file")
            args.file = argv[index + 1];
        if (current === "--action")
            args.action = argv[index + 1];
        if (current === "--payload")
            args.payload = argv[index + 1];
        if (current === "--payload-file")
            args.payloadFile = argv[index + 1];
        if (current === "--help" || current === "-h")
            args.help = true;
    }
    return args;
}
function printHelp() {
    const scriptName = node_path_1.default.basename(process.argv[1] ?? "openclaw.js");
    process.stdout.write([
        `Usage: node dist/${scriptName} [options]`,
        "",
        "Options:",
        "  --input <json>         Full request JSON string",
        "  --file <path>          Full request JSON file",
        `  --action <name>        Action name: ${(0, index_1.getSupportedActions)().join(" | ")}`,
        "  --payload <json>       Payload JSON string for the selected action",
        "  --payload-file <path>  Payload JSON file for the selected action",
        "  --help, -h             Show help",
        "",
        "Examples:",
        "  node dist/openclaw.js --input '{\"action\":\"script\",\"payload\":{\"topic\":\"测试主题\"}}'",
        "  node dist/openclaw.js --action script --payload '{\"topic\":\"测试主题\"}'",
    ].join("\n"));
}
async function resolveRequest() {
    const { input, file, action, payload, payloadFile, help } = parseArgs(process.argv.slice(2));
    if (help) {
        printHelp();
        process.exit(0);
    }
    if (input) {
        return (0, index_1.validateOpenClawSkillRequest)(JSON.parse(input));
    }
    if (file) {
        return (0, index_1.validateOpenClawSkillRequest)(JSON.parse((0, node_fs_1.readFileSync)(file, "utf8")));
    }
    if (action && (payload || payloadFile)) {
        const resolvedPayload = payload
            ? JSON.parse(payload)
            : JSON.parse((0, node_fs_1.readFileSync)(payloadFile, "utf8"));
        return (0, index_1.validateOpenClawSkillRequest)({
            action,
            payload: resolvedPayload,
        });
    }
    const stdin = await readStdin();
    if (!stdin.trim()) {
        throw new Error("Missing skill input. Provide --input, --file, --action with --payload/--payload-file, or JSON via stdin.");
    }
    return (0, index_1.validateOpenClawSkillRequest)(JSON.parse(stdin));
}
async function main() {
    const request = await resolveRequest();
    const result = await (0, index_1.runOpenClawSkill)(request);
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
}
if (require.main === module) {
    main().catch((error) => {
        const message = error instanceof Error ? error.message : String(error);
        process.stderr.write(`${message}\n`);
        process.exitCode = 1;
    });
}
