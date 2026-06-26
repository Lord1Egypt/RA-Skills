"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.validateConfig = exports.WindowsTtsClient = exports.createTools = exports.manifest = void 0;
exports.default = init;
const openclaw_plugin_json_1 = __importDefault(require("./openclaw.plugin.json"));
const client_1 = require("./client");
const config_1 = require("./config");
const tools_1 = require("./tools");
const TOOL_NAMES = [
    "tts_notify",
    "tts_get_status",
    "tts_list_voices",
    "tts_set_volume"
];
function init(api) {
    const config = (0, config_1.validateConfig)(api.config ?? {});
    const client = new client_1.WindowsTtsClient(config);
    const tools = (0, tools_1.createTools)({ client, config });
    const register = api.registerTool ?? api.tool;
    if (!register) {
        throw new Error("OpenClaw API does not expose registerTool/tool.");
    }
    TOOL_NAMES.forEach((name) => {
        register(name, async (input) => tools[name](input));
    });
}
exports.manifest = openclaw_plugin_json_1.default;
var tools_2 = require("./tools");
Object.defineProperty(exports, "createTools", { enumerable: true, get: function () { return tools_2.createTools; } });
var client_2 = require("./client");
Object.defineProperty(exports, "WindowsTtsClient", { enumerable: true, get: function () { return client_2.WindowsTtsClient; } });
var config_2 = require("./config");
Object.defineProperty(exports, "validateConfig", { enumerable: true, get: function () { return config_2.validateConfig; } });
