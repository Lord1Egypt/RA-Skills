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
const OUTPUT_DIR = path.join(process.cwd(), '.worldloops', 'inbox');
const OUTPUT_FILE = path.join(OUTPUT_DIR, 'openclaw-observations.json');
function getFlagValue(flag) {
    const args = process.argv.slice(2);
    const idx = args.indexOf(flag);
    if (idx === -1 || idx + 1 >= args.length)
        return undefined;
    return args[idx + 1];
}
function fail(msg) {
    process.stderr.write(`observations:write error: ${msg}\n`);
    process.exit(1);
}
function validateObservation(item, index) {
    const errors = [];
    if (typeof item !== 'object' || item === null || Array.isArray(item)) {
        errors.push(`[${index}] must be an object`);
        return errors;
    }
    const obs = item;
    if (typeof obs.id !== 'string' || !obs.id)
        errors.push(`[${index}] id: required string`);
    if (typeof obs.source !== 'string' || !obs.source)
        errors.push(`[${index}] source: required string`);
    if (typeof obs.sourceId !== 'string' || !obs.sourceId)
        errors.push(`[${index}] sourceId: required string`);
    if (obs.observedBy !== 'openclaw')
        errors.push(`[${index}] observedBy: must be "openclaw"`);
    if (typeof obs.title !== 'string' || !obs.title)
        errors.push(`[${index}] title: required string`);
    if (typeof obs.text !== 'string' || !obs.text)
        errors.push(`[${index}] text: required string`);
    if (typeof obs.timestamp !== 'string' || !obs.timestamp)
        errors.push(`[${index}] timestamp: required string`);
    if (typeof obs.evidence !== 'object' || obs.evidence === null || Array.isArray(obs.evidence)) {
        errors.push(`[${index}] evidence: required object`);
    }
    const validIntents = ['new_loop', 'state_transition', 'noise', 'related_context', 'evidence'];
    if (obs.observationIntent !== undefined && !validIntents.includes(obs.observationIntent)) {
        errors.push(`[${index}] observationIntent: must be one of ${validIntents.join(', ')}`);
    }
    if (obs.confidence !== undefined && (typeof obs.confidence !== 'number' || obs.confidence < 0 || obs.confidence > 1)) {
        errors.push(`[${index}] confidence: must be a number between 0 and 1`);
    }
    return errors;
}
function main() {
    const inputArg = getFlagValue('--input');
    if (!inputArg) {
        fail('--input <json-file> is required\nUsage: npm run observations:write -- --input <path/to/observations.json>');
    }
    const inputPath = path.resolve(process.cwd(), inputArg);
    if (!fs.existsSync(inputPath)) {
        fail(`input file not found: ${inputPath}`);
    }
    let raw;
    try {
        raw = fs.readFileSync(inputPath, 'utf8');
    }
    catch (err) {
        fail(`could not read input file: ${String(err)}`);
    }
    let parsed;
    try {
        parsed = JSON.parse(raw);
    }
    catch (err) {
        fail(`invalid JSON: ${String(err)}`);
    }
    if (!Array.isArray(parsed)) {
        fail('input must be a JSON array of ObservedSignal objects');
    }
    const allErrors = [];
    for (let i = 0; i < parsed.length; i++) {
        allErrors.push(...validateObservation(parsed[i], i));
    }
    if (allErrors.length > 0) {
        process.stderr.write('observations:write validation failed:\n');
        for (const err of allErrors) {
            process.stderr.write(`  ${err}\n`);
        }
        process.exit(1);
    }
    if (!fs.existsSync(OUTPUT_DIR)) {
        fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    }
    const observations = parsed;
    fs.writeFileSync(OUTPUT_FILE, JSON.stringify(observations, null, 2) + '\n', 'utf8');
    console.log(`Observations written: ${observations.length}`);
    console.log(`Output: .worldloops/inbox/openclaw-observations.json`);
    console.log('externalWrite:false');
}
main();
//# sourceMappingURL=observationsWrite.js.map