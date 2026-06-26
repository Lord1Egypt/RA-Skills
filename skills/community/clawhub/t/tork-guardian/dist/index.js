"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ReportStore = exports.formatReportForAPI = exports.scanFromSource = exports.scanFromURL = exports.generateBadgeJSON = exports.generateBadgeMarkdown = exports.generateBadge = exports.SCAN_RULES = exports.SkillScanner = exports.ENTERPRISE_CONFIG = exports.PRODUCTION_CONFIG = exports.DEVELOPMENT_CONFIG = exports.MINIMAL_CONFIG = exports.NetworkMonitor = exports.STRICT_NETWORK_POLICY = exports.DEFAULT_NETWORK_POLICY = exports.TorkClient = exports.GovernanceDeniedError = exports.validateDNS = exports.validateEgress = exports.validatePortBind = exports.NetworkAccessHandler = exports.governToolCall = exports.governLLMRequest = exports.TorkGuardian = void 0;
exports.redactPII = redactPII;
exports.generateReceipt = generateReceipt;
const client_1 = require("./client");
const config_1 = require("./config");
const llm_1 = require("./interceptors/llm");
const tool_1 = require("./interceptors/tool");
const network_access_1 = require("./handlers/network-access");
class TorkGuardian {
    constructor(config) {
        this.config = config_1.TorkConfigSchema.parse(config);
        this.client = new client_1.TorkClient(this.config.apiKey, this.config.baseUrl);
        this.networkHandler = new network_access_1.NetworkAccessHandler(this.config, this.client);
    }
    async governLLM(request) {
        return (0, llm_1.governLLMRequest)(this.client, request, this.config);
    }
    governTool(tool) {
        return (0, tool_1.governToolCall)(tool, this.config);
    }
    async redactPII(content) {
        return this.client.redact(content);
    }
    async generateReceipt(content) {
        return this.client.govern(content);
    }
    getConfig() {
        return { ...this.config };
    }
    getNetworkHandler() {
        return this.networkHandler;
    }
}
exports.TorkGuardian = TorkGuardian;
// Standalone function exports
async function redactPII(apiKey, content) {
    const client = new client_1.TorkClient(apiKey);
    return client.redact(content);
}
async function generateReceipt(apiKey, content) {
    const client = new client_1.TorkClient(apiKey);
    return client.govern(content);
}
var llm_2 = require("./interceptors/llm");
Object.defineProperty(exports, "governLLMRequest", { enumerable: true, get: function () { return llm_2.governLLMRequest; } });
var tool_2 = require("./interceptors/tool");
Object.defineProperty(exports, "governToolCall", { enumerable: true, get: function () { return tool_2.governToolCall; } });
var network_access_2 = require("./handlers/network-access");
Object.defineProperty(exports, "NetworkAccessHandler", { enumerable: true, get: function () { return network_access_2.NetworkAccessHandler; } });
Object.defineProperty(exports, "validatePortBind", { enumerable: true, get: function () { return network_access_2.validatePortBind; } });
Object.defineProperty(exports, "validateEgress", { enumerable: true, get: function () { return network_access_2.validateEgress; } });
Object.defineProperty(exports, "validateDNS", { enumerable: true, get: function () { return network_access_2.validateDNS; } });
var llm_3 = require("./interceptors/llm");
Object.defineProperty(exports, "GovernanceDeniedError", { enumerable: true, get: function () { return llm_3.GovernanceDeniedError; } });
var client_2 = require("./client");
Object.defineProperty(exports, "TorkClient", { enumerable: true, get: function () { return client_2.TorkClient; } });
var network_default_1 = require("./policies/network-default");
Object.defineProperty(exports, "DEFAULT_NETWORK_POLICY", { enumerable: true, get: function () { return network_default_1.DEFAULT_NETWORK_POLICY; } });
var network_strict_1 = require("./policies/network-strict");
Object.defineProperty(exports, "STRICT_NETWORK_POLICY", { enumerable: true, get: function () { return network_strict_1.STRICT_NETWORK_POLICY; } });
var network_monitor_1 = require("./utils/network-monitor");
Object.defineProperty(exports, "NetworkMonitor", { enumerable: true, get: function () { return network_monitor_1.NetworkMonitor; } });
var examples_1 = require("./examples");
Object.defineProperty(exports, "MINIMAL_CONFIG", { enumerable: true, get: function () { return examples_1.MINIMAL_CONFIG; } });
Object.defineProperty(exports, "DEVELOPMENT_CONFIG", { enumerable: true, get: function () { return examples_1.DEVELOPMENT_CONFIG; } });
Object.defineProperty(exports, "PRODUCTION_CONFIG", { enumerable: true, get: function () { return examples_1.PRODUCTION_CONFIG; } });
Object.defineProperty(exports, "ENTERPRISE_CONFIG", { enumerable: true, get: function () { return examples_1.ENTERPRISE_CONFIG; } });
var scanner_1 = require("./scanner");
Object.defineProperty(exports, "SkillScanner", { enumerable: true, get: function () { return scanner_1.SkillScanner; } });
var rules_1 = require("./scanner/rules");
Object.defineProperty(exports, "SCAN_RULES", { enumerable: true, get: function () { return rules_1.SCAN_RULES; } });
var badge_1 = require("./scanner/badge");
Object.defineProperty(exports, "generateBadge", { enumerable: true, get: function () { return badge_1.generateBadge; } });
Object.defineProperty(exports, "generateBadgeMarkdown", { enumerable: true, get: function () { return badge_1.generateBadgeMarkdown; } });
Object.defineProperty(exports, "generateBadgeJSON", { enumerable: true, get: function () { return badge_1.generateBadgeJSON; } });
var api_1 = require("./scanner/api");
Object.defineProperty(exports, "scanFromURL", { enumerable: true, get: function () { return api_1.scanFromURL; } });
Object.defineProperty(exports, "scanFromSource", { enumerable: true, get: function () { return api_1.scanFromSource; } });
Object.defineProperty(exports, "formatReportForAPI", { enumerable: true, get: function () { return api_1.formatReportForAPI; } });
var report_store_1 = require("./scanner/report-store");
Object.defineProperty(exports, "ReportStore", { enumerable: true, get: function () { return report_store_1.ReportStore; } });
//# sourceMappingURL=index.js.map