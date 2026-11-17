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
exports.selectAvatars = selectAvatars;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const images_1 = require("./images");
const SUPPORTED_EXTENSIONS = new Set([".jpg", ".jpeg", ".png", ".webp"]);
function toPosixPath(p) {
    // Normalize for consistent downstream handling across platforms (tests, logs, consumers)
    return p.replace(/\\/g, "/");
}
/**
 * Get the best available creation/modification time for a file.
 * Priority: birthtime > mtime > ctime
 */
function getFileTime(stat) {
    const birthtime = stat.birthtimeMs;
    const mtime = stat.mtimeMs;
    const ctime = stat.ctimeMs;
    // birthtime is 0 or equal to epoch on some systems (Linux ext4 without birth time support)
    if (birthtime && birthtime > 0) {
        return birthtime;
    }
    if (mtime && mtime > 0) {
        return mtime;
    }
    return ctime;
}
/**
 * Resolve a file path to its real path, returning null on error.
 */
function safeRealpath(filePath) {
    try {
        return fs.realpathSync(filePath);
    }
    catch {
        return null;
    }
}
function selectAvatars(options) {
    const { avatar, avatarsDir, avatarMaxRefs, avatarBlendEnabled } = options;
    const warn = options.onWarning ?? console.warn;
    const seenRealpaths = new Set();
    const result = [];
    // Add primary Avatar first
    if (avatar) {
        if (fs.existsSync(avatar)) {
            try {
                const image = (0, images_1.readReferenceImage)(avatar, options.allowedRoots);
                const real = safeRealpath(avatar);
                if (real) {
                    seenRealpaths.add(real);
                    result.push({ filePath: toPosixPath(avatar), buffer: image.data, mimeType: image.mimeType });
                }
            }
            catch (err) {
                warn(`[stella] Warning: Invalid Avatar: ${err.message}`);
            }
        }
        else {
            warn(`[stella] Warning: Avatar not found: ${avatar}`);
        }
    }
    // Scan AvatarsDir if blending is enabled
    if (avatarBlendEnabled && avatarsDir) {
        if (!fs.existsSync(avatarsDir)) {
            warn(`[stella] Warning: AvatarsDir not found: ${avatarsDir}`);
        }
        else {
            let entries;
            try {
                entries = fs.readdirSync(avatarsDir, { withFileTypes: true });
            }
            catch (err) {
                warn(`[stella] Warning: Cannot read AvatarsDir: ${avatarsDir} — ${err.message}`);
                entries = [];
            }
            const candidates = [];
            for (const entry of entries) {
                if (!entry.isFile())
                    continue;
                const ext = path.extname(entry.name).toLowerCase();
                if (!SUPPORTED_EXTENSIONS.has(ext))
                    continue;
                // Use POSIX-style paths for consistent behavior across platforms.
                // Node on Windows accepts forward slashes in most filesystem APIs.
                const filePath = toPosixPath(path.join(avatarsDir, entry.name));
                try {
                    const stat = fs.statSync(filePath);
                    candidates.push({ filePath, time: getFileTime(stat) });
                }
                catch {
                    // Skip unreadable files silently
                }
            }
            // Sort newest first
            candidates.sort((a, b) => b.time - a.time || a.filePath.localeCompare(b.filePath));
            for (const candidate of candidates) {
                if (result.length >= avatarMaxRefs)
                    break;
                const real = safeRealpath(candidate.filePath);
                if (!real || seenRealpaths.has(real))
                    continue;
                let image;
                try {
                    image = (0, images_1.readReferenceImage)(candidate.filePath, options.allowedRoots);
                }
                catch (err) {
                    warn(`[stella] Warning: Invalid reference image: ${err.message}`);
                    continue;
                }
                seenRealpaths.add(real);
                result.push({ filePath: toPosixPath(candidate.filePath), buffer: image.data, mimeType: image.mimeType });
            }
        }
    }
    return result;
}
//# sourceMappingURL=avatars.js.map