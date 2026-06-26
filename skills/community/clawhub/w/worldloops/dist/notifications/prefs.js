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
exports.DEFAULT_PREFS = exports.DEFAULT_BRIEF_CHANNEL = exports.VALID_CHANNELS = void 0;
exports.getPrefsPath = getPrefsPath;
exports.loadPrefs = loadPrefs;
exports.savePrefs = savePrefs;
exports.initPrefs = initPrefs;
exports.setDotPath = setDotPath;
exports.isInQuietHours = isInQuietHours;
exports.meetsSeverity = meetsSeverity;
const fs = __importStar(require("node:fs"));
const path = __importStar(require("node:path"));
function getWorldLoopsDir() {
    return process.env.WORLDLOOPS_DIR ?? path.join(process.cwd(), '.worldloops');
}
function getPrefsPath() {
    return path.join(getWorldLoopsDir(), 'notification_prefs.json');
}
exports.VALID_CHANNELS = ['local', 'telegram', 'slack', 'discord', 'sms', 'email'];
exports.DEFAULT_BRIEF_CHANNEL = 'local';
exports.DEFAULT_PREFS = {
    dailyBrief: {
        enabled: true,
        time: '09:00',
        timezone: 'UTC',
        channel: exports.DEFAULT_BRIEF_CHANNEL,
        minimumSeverity: 'medium',
        sources: ['gmail', 'calendar', 'slack'],
    },
    proactiveDiscovery: {
        enabled: false,
        scanIntervalMinutes: 30,
        minSeverity: 'medium',
    },
    quietHours: {
        enabled: false,
        start: '21:00',
        end: '08:00',
    },
    eventAlerts: {
        enabled: false,
        rules: [],
    },
    channels: {
        cli: true,
    },
};
function loadPrefs() {
    const prefsPath = getPrefsPath();
    if (!fs.existsSync(prefsPath)) {
        return JSON.parse(JSON.stringify(exports.DEFAULT_PREFS));
    }
    return JSON.parse(fs.readFileSync(prefsPath, 'utf8'));
}
function savePrefs(prefs) {
    const prefsPath = getPrefsPath();
    const dir = path.dirname(prefsPath);
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(prefsPath, JSON.stringify(prefs, null, 2) + '\n', 'utf8');
}
function initPrefs() {
    const prefsPath = getPrefsPath();
    if (fs.existsSync(prefsPath)) {
        return false;
    }
    savePrefs(exports.DEFAULT_PREFS);
    return true;
}
function setDotPath(obj, dotPath, value) {
    const keys = dotPath.split('.');
    let current = obj;
    for (let i = 0; i < keys.length - 1; i++) {
        const key = keys[i];
        if (typeof current[key] !== 'object' || current[key] === null) {
            current[key] = {};
        }
        current = current[key];
    }
    current[keys[keys.length - 1]] = value;
}
function isInQuietHours(prefs, now = new Date()) {
    if (!prefs.quietHours.enabled)
        return false;
    const [startH, startM] = prefs.quietHours.start.split(':').map(Number);
    const [endH, endM] = prefs.quietHours.end.split(':').map(Number);
    const currentMinutes = now.getHours() * 60 + now.getMinutes();
    const startMinutes = startH * 60 + startM;
    const endMinutes = endH * 60 + endM;
    // Spans midnight (e.g. 21:00–08:00)
    if (startMinutes > endMinutes) {
        return currentMinutes >= startMinutes || currentMinutes < endMinutes;
    }
    // Same day (e.g. 09:00–17:00)
    return currentMinutes >= startMinutes && currentMinutes < endMinutes;
}
const SEVERITY_RANK = {
    low: 0,
    medium: 1,
    high: 2,
    critical: 3,
};
function meetsSeverity(candidateSeverity, minSeverity) {
    const candidateRank = SEVERITY_RANK[candidateSeverity ?? 'medium'] ?? 1;
    const minRank = SEVERITY_RANK[minSeverity] ?? 1;
    return candidateRank >= minRank;
}
//# sourceMappingURL=prefs.js.map