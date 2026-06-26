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
exports.getExecutionContractsPath = getExecutionContractsPath;
exports.loadExecutionContracts = loadExecutionContracts;
exports.saveExecutionContract = saveExecutionContract;
exports.findExecutionContractById = findExecutionContractById;
exports.listExecutionContracts = listExecutionContracts;
const fs = __importStar(require("node:fs"));
const path = __importStar(require("node:path"));
function getWorldLoopsDir() {
    return process.env.WORLDLOOPS_DIR ?? path.join(process.cwd(), '.worldloops');
}
function getExecutionContractsPath() {
    return path.join(getWorldLoopsDir(), 'execution_contracts.json');
}
function loadExecutionContracts() {
    const contractsPath = getExecutionContractsPath();
    if (!fs.existsSync(contractsPath)) {
        return [];
    }
    return JSON.parse(fs.readFileSync(contractsPath, 'utf8'));
}
function saveExecutionContract(contract) {
    const contractsPath = getExecutionContractsPath();
    const dir = path.dirname(contractsPath);
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
    const existing = loadExecutionContracts();
    const upserted = existing.filter((c) => c.id !== contract.id);
    upserted.push(contract);
    fs.writeFileSync(contractsPath, JSON.stringify(upserted, null, 2) + '\n', 'utf8');
}
function findExecutionContractById(id) {
    return loadExecutionContracts().find((c) => c.id === id) ?? null;
}
function listExecutionContracts() {
    return loadExecutionContracts();
}
//# sourceMappingURL=executionContracts.js.map