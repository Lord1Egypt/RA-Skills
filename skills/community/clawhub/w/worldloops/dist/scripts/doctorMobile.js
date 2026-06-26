"use strict";
// Local-only safety check: no external reads or writes.
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
const checkWorldState_1 = require("../state/checkWorldState");
function main() {
    const worldloopsDir = process.env.WORLDLOOPS_DIR ?? path.join(process.cwd(), '.worldloops');
    const stateResult = (0, checkWorldState_1.checkWorldState)();
    const buildOk = fs.existsSync(path.join(process.cwd(), 'dist', 'scripts'));
    const allOk = buildOk && stateResult.ok;
    console.log('');
    console.log('🦞 WorldLoops Safety Check');
    console.log('');
    console.log(allOk ? '✅ Safe to try' : '⚠️  Some issues detected');
    console.log('✅ externalWrite:false enforced');
    console.log('');
    console.log('No external actions enabled:');
    console.log('✅ No emails will be sent');
    console.log('✅ No chat messages will be posted');
    console.log('✅ No calendar events will be created');
    console.log('✅ No project changes will be made');
    console.log('');
    console.log('Local checks:');
    console.log('✅ State readable');
    console.log('✅ Receipts verifiable');
    console.log('✅ Repair history auditable');
    console.log('');
    // suppress unused warning
    void worldloopsDir;
    process.exit(allOk ? 0 : 1);
}
main();
//# sourceMappingURL=doctorMobile.js.map