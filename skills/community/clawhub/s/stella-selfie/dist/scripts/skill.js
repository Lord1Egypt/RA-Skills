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
exports.runSkill = runSkill;
const fs = __importStar(require("node:fs"));
const plugin_1 = require("./plugin");
const chat_1 = require("./chat");
const native_cli_1 = require("./native-cli");
const errors_1 = require("./errors");
async function runSkill(args = process.argv.slice(2)) {
    if (args.length === 2 && args[0] === "prepare") {
        const stat = fs.statSync(args[1]);
        if (!stat.isFile() || stat.size > 2 * 1024 * 1024)
            throw new plugin_1.InputError("INPUT_INVALID", "Input must be a JSON file no larger than 2 MiB.");
        let request;
        try {
            request = JSON.parse(fs.readFileSync(args[1], "utf8"));
        }
        catch {
            throw new plugin_1.InputError("INPUT_INVALID", "Invalid request JSON.");
        }
        if (!request || typeof request !== "object" || Array.isArray(request)) {
            throw new plugin_1.InputError("INPUT_INVALID", "Specify the actual conversation Agent; chat has no default Agent.");
        }
        const body = request;
        if (typeof body.agentId !== "string" || !plugin_1.AGENT_ID.test(body.agentId)) {
            throw new plugin_1.InputError("INPUT_INVALID", "Specify the actual conversation Agent; chat has no default Agent.");
        }
        return (0, chat_1.prepareChat)(body, await (0, chat_1.readChatState)(body.agentId));
    }
    if (args.length === 3 && args[0] === "release") {
        const agent = (await (0, native_cli_1.readAgentLocations)()).find(a => a.id === args[1]);
        if (!agent)
            throw new plugin_1.InputError("AGENT_NOT_FOUND", "The conversation Agent does not exist.");
        return (0, chat_1.releaseReferences)(agent, args[2]);
    }
    throw new plugin_1.InputError("INPUT_INVALID", "Use: skill.js prepare <request.json> or skill.js release <agentId> <referenceToken>. Legacy targets, batches and save-dir are unsupported.");
}
if (require.main === module) {
    runSkill().then(result => console.log(JSON.stringify(result))).catch(error => {
        const safe = error instanceof plugin_1.InputError
            ? { code: error.code, message: error.message, actionHint: (0, errors_1.localActionHint)(error.code) }
            : (0, errors_1.normalizeNativeError)(error);
        console.log(JSON.stringify({ schemaVersion: 1, ok: false, error: safe }));
        process.exitCode = error instanceof plugin_1.InputError ? 2 : 1;
    });
}
//# sourceMappingURL=skill.js.map