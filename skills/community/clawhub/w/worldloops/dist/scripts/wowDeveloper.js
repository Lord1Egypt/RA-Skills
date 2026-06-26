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
const path = __importStar(require("node:path"));
const runAdapterTest_1 = require("../adapter/runAdapterTest");
const checkWorldState_1 = require("../state/checkWorldState");
function main() {
    const slackFixture = path.join(process.cwd(), 'examples', 'adapters', 'slack-message.json');
    console.log('');
    console.log('Developer Verification');
    console.log('');
    const adapterResult = (0, runAdapterTest_1.runAdapterTest)(slackFixture);
    const adapterPassed = adapterResult.validate === 'passed' &&
        adapterResult.reconcile === 'passed' &&
        adapterResult.openLoopPersisted === true &&
        adapterResult.proposalPersisted === true &&
        adapterResult.idempotency === 'passed' &&
        adapterResult.externalWrite === false;
    console.log(`Adapter signal validation: ${adapterResult.validate}`);
    if (adapterResult.validateErrors) {
        for (const err of adapterResult.validateErrors) {
            console.log(`  error: ${err}`);
        }
    }
    console.log(`Reconcile: ${adapterResult.reconcile}`);
    if (adapterResult.reconcileError) {
        console.log(`  error: ${adapterResult.reconcileError}`);
    }
    console.log(`Open loop persisted: ${String(adapterResult.openLoopPersisted)}`);
    console.log(`Proposal persisted: ${String(adapterResult.proposalPersisted)}`);
    console.log(`Idempotency: ${adapterResult.idempotency}`);
    const stateResult = (0, checkWorldState_1.checkWorldState)();
    console.log(`State check: ${stateResult.status}`);
    const receiptsResult = (0, checkWorldState_1.checkReceipts)();
    console.log(`Receipts verification: ${receiptsResult.status}`);
    console.log(`externalWrite:false: enforced`);
    console.log('');
    const allPassed = adapterPassed && stateResult.ok && receiptsResult.ok;
    process.exit(allPassed ? 0 : 1);
}
main();
//# sourceMappingURL=wowDeveloper.js.map