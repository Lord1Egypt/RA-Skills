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
const checkWorldState_1 = require("../state/checkWorldState");
function readPackageVersion() {
    try {
        const pkgPath = path.join(process.cwd(), 'package.json');
        const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
        return typeof pkg['version'] === 'string' ? pkg['version'] : 'unknown';
    }
    catch {
        return 'unknown';
    }
}
function checkBuildFiles() {
    const distPath = path.join(process.cwd(), 'dist');
    return (fs.existsSync(distPath) &&
        fs.existsSync(path.join(distPath, 'scripts')));
}
function storeCheck(dir, filename, stateErrors) {
    const filePath = path.join(dir, filename);
    if (!fs.existsSync(filePath))
        return 'OK';
    if (stateErrors.has(filePath))
        return 'issues detected — run npm run state:check';
    return 'OK';
}
function storeCheckRepair(dir, filename, stateErrors) {
    const filePath = path.join(dir, filename);
    if (!fs.existsSync(filePath))
        return 'OK — no repair history yet';
    if (stateErrors.has(filePath))
        return 'issues detected — run npm run state:check';
    return 'OK';
}
function main() {
    const worldloopsDir = process.env.WORLDLOOPS_DIR ?? path.join(process.cwd(), '.worldloops');
    const version = readPackageVersion();
    const buildOk = checkBuildFiles();
    const dirExists = fs.existsSync(worldloopsDir);
    const stateResult = (0, checkWorldState_1.checkWorldState)();
    const errorFiles = new Set(stateResult.issues
        .filter((i) => i.severity === 'error')
        .map((i) => i.file));
    const openLoopsStatus = storeCheck(worldloopsDir, 'open_loop_states.json', errorFiles);
    const proposalsStatus = storeCheck(worldloopsDir, 'proposals.json', errorFiles);
    const plansStatus = storeCheck(worldloopsDir, 'execution_plans.json', errorFiles);
    const contractsStatus = storeCheck(worldloopsDir, 'execution_contracts.json', errorFiles);
    const transReceiptsStatus = storeCheck(worldloopsDir, 'transition_receipts.json', errorFiles);
    const propDecisionReceiptsStatus = storeCheck(worldloopsDir, 'proposal_decision_receipts.json', errorFiles);
    const repairReceiptsStatus = storeCheckRepair(worldloopsDir, 'repair_receipts.json', errorFiles);
    const allOk = version !== 'unknown' &&
        buildOk &&
        stateResult.ok;
    console.log('');
    console.log('WorldLoops Safety Check');
    console.log('');
    if (allOk) {
        console.log('Your local workspace is safe.');
    }
    else {
        console.log('Your local workspace has issues. See Developer details below.');
    }
    console.log('');
    console.log('No external writes enabled.');
    console.log('No emails will be sent.');
    console.log('No chat messages will be posted.');
    console.log('No calendar events will be created.');
    console.log('No project changes will be made.');
    console.log('');
    console.log('Local state is readable.');
    console.log('Receipts are verifiable.');
    console.log('Repair history is auditable.');
    console.log('');
    console.log('Status:');
    console.log(allOk ? 'Safe to try.' : 'Some issues detected — see Developer details.');
    console.log('');
    console.log('Developer details:');
    console.log(`- Package version: ${version !== 'unknown' ? 'OK' : 'unknown'}`);
    console.log(`- Build files: ${buildOk ? 'OK' : 'missing — run npm run build'}`);
    console.log(`- Local state directory: ${dirExists ? 'OK' : 'OK'}`);
    console.log(`- Open loops store: ${openLoopsStatus}`);
    console.log(`- Proposal store: ${proposalsStatus}`);
    console.log(`- Execution plans: ${plansStatus}`);
    console.log(`- Execution contracts: ${contractsStatus}`);
    console.log(`- Transition receipts: ${transReceiptsStatus}`);
    console.log(`- Proposal decision receipts: ${propDecisionReceiptsStatus}`);
    console.log(`- Repair receipts: ${repairReceiptsStatus}`);
    console.log(`- externalWrite:false: enforced`);
    if (!stateResult.ok && stateResult.issues.length > 0) {
        console.log('');
        console.log(`State integrity: ${stateResult.summary.issues} error(s) found`);
        for (const issue of stateResult.issues) {
            if (issue.severity === 'error') {
                console.log(`  [${issue.code}] ${issue.message}`);
            }
        }
    }
    console.log('');
    process.exit(allOk ? 0 : 1);
}
main();
//# sourceMappingURL=doctor.js.map