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
exports.ReportStore = void 0;
const crypto = __importStar(require("crypto"));
class ReportStore {
    constructor() {
        this.reports = new Map();
        this.insertionOrder = [];
    }
    /**
     * Store a scan report and return a unique report ID.
     */
    store(report) {
        const id = crypto.randomUUID();
        this.reports.set(id, report);
        this.insertionOrder.push(id);
        return id;
    }
    /**
     * Retrieve a report by ID.
     */
    get(id) {
        return this.reports.get(id) ?? null;
    }
    /**
     * List the most recent scan reports.
     */
    list(limit = 20) {
        const ids = this.insertionOrder.slice(-limit).reverse();
        return ids.map(id => this.reports.get(id));
    }
    /**
     * Get the most recent scan report for a given skill name.
     */
    getBySkillName(name) {
        for (let i = this.insertionOrder.length - 1; i >= 0; i--) {
            const report = this.reports.get(this.insertionOrder[i]);
            if (report.skillName === name) {
                return report;
            }
        }
        return null;
    }
}
exports.ReportStore = ReportStore;
//# sourceMappingURL=report-store.js.map