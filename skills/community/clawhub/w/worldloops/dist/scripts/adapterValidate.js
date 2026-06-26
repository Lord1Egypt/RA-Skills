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
const fs = __importStar(require("node:fs"));
const path = __importStar(require("node:path"));
const validateAdapterSignal_1 = require("../adapter/validateAdapterSignal");
function main() {
    const filePath = process.argv[2];
    if (!filePath) {
        console.error(JSON.stringify({
            ok: false,
            error: {
                code: 'MISSING_FILE',
                message: 'Usage: npm run adapter:validate -- <path-to-adapter-signal.json>',
            },
            safety: { externalWrite: false },
        }, null, 2));
        process.exit(1);
    }
    let raw;
    try {
        const resolved = path.resolve(filePath);
        raw = JSON.parse(fs.readFileSync(resolved, 'utf8'));
    }
    catch (err) {
        console.error(JSON.stringify({
            ok: false,
            error: {
                code: 'FILE_READ_ERROR',
                message: err instanceof Error ? err.message : String(err),
            },
            safety: { externalWrite: false },
        }, null, 2));
        process.exit(1);
    }
    const result = (0, validateAdapterSignal_1.validateAdapterSignal)(raw);
    if (result.ok) {
        console.log('Valid WorldLoops Adapter Signal');
        console.log(`source: ${result.signal.source}`);
        console.log(`sourceType: ${result.signal.sourceType}`);
        console.log(`externalWrite: ${result.signal.externalWrite}`);
        process.exit(0);
    }
    else {
        console.error(JSON.stringify({
            ok: false,
            errors: result.errors,
            safety: { externalWrite: false },
        }, null, 2));
        process.exit(1);
    }
}
main();
//# sourceMappingURL=adapterValidate.js.map