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
exports.parseIdentity = parseIdentity;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
/**
 * Resolve a path from IDENTITY.md relative to the workspace root.
 * Absolute paths are returned as-is.
 */
function resolvePath(value, workspaceRoot) {
    if (path.isAbsolute(value)) {
        return value;
    }
    return path.resolve(workspaceRoot, value);
}
/**
 * Parse a single key: value line from IDENTITY.md.
 * Supports plain `Key: value` as well as Markdown list+bold variants:
 *   - **Key:** value
 *   - **Key**: value
 *   * **Key:** value
 * Returns null if the line doesn't match.
 */
function parseLine(line) {
    const match = line.match(/^(?:[-*]\s*)?(?:\*{1,2})?([A-Za-z][A-Za-z0-9_]*)\*{0,2}:\*{0,2}\s*(.+?)\s*(?:#.*)?$/);
    if (!match)
        return null;
    return [match[1], match[2]];
}
/**
 * Read and parse IDENTITY.md from the OpenClaw workspace.
 * Returns resolved absolute paths for Avatar and AvatarsDir.
 */
function parseIdentity(workspaceRoot) {
    const identityPath = path.join(workspaceRoot, "IDENTITY.md");
    if (!fs.existsSync(identityPath)) {
        throw new Error(`IDENTITY.md not found at: ${identityPath}`);
    }
    const content = fs.readFileSync(identityPath, "utf-8");
    const lines = content.split("\n");
    let avatar = null;
    let avatarsDir = null;
    for (const line of lines) {
        const parsed = parseLine(line.trim());
        if (!parsed)
            continue;
        const [key, value] = parsed;
        if (key === "Avatar") {
            avatar = resolvePath(value, workspaceRoot);
        }
        else if (key === "AvatarsDir") {
            avatarsDir = resolvePath(value, workspaceRoot);
        }
    }
    return { avatar, avatarsDir };
}
//# sourceMappingURL=identity.js.map