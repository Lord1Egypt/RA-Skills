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
exports.MAX_IMAGE_BYTES = void 0;
exports.inspectImage = inspectImage;
exports.isPathInside = isPathInside;
exports.readImageFile = readImageFile;
exports.readReferenceImage = readReferenceImage;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
exports.MAX_IMAGE_BYTES = 20 * 1024 * 1024;
// Inspect content rather than trusting a filename or a server's Content-Type.
// This checks format signatures, not a full image decode.
function inspectImage(data, maxBytes = exports.MAX_IMAGE_BYTES) {
    if (data.length === 0 || data.length > maxBytes) {
        throw new Error(`Image must contain between 1 byte and ${maxBytes} bytes`);
    }
    if (data.length >= 24 && data.subarray(0, 8).equals(Buffer.from("89504e470d0a1a0a", "hex")) &&
        data.toString("ascii", 12, 16) === "IHDR" && data.readUInt32BE(16) > 0 && data.readUInt32BE(20) > 0) {
        return { mimeType: "image/png", extension: ".png" };
    }
    if (data.length >= 4 && data[0] === 0xff && data[1] === 0xd8 && data[2] === 0xff) {
        return { mimeType: "image/jpeg", extension: ".jpg" };
    }
    if (data.length >= 16 && data.toString("ascii", 0, 4) === "RIFF" &&
        data.toString("ascii", 8, 12) === "WEBP" && ["VP8 ", "VP8L", "VP8X"].includes(data.toString("ascii", 12, 16))) {
        return { mimeType: "image/webp", extension: ".webp" };
    }
    if (data.length >= 10 && ["GIF87a", "GIF89a"].includes(data.toString("ascii", 0, 6))) {
        return { mimeType: "image/gif", extension: ".gif" };
    }
    if (data.length >= 16 && data.toString("ascii", 4, 8) === "ftyp" &&
        ["avif", "avis"].includes(data.toString("ascii", 8, 12))) {
        return { mimeType: "image/avif", extension: ".avif" };
    }
    throw new Error("Unrecognized image content");
}
function isPathInside(root, file) {
    const relative = path.relative(root, file);
    return relative !== ".." && !relative.startsWith(`..${path.sep}`) && !path.isAbsolute(relative);
}
function readImageFile(filePath, allowedRoots) {
    const real = fs.realpathSync(filePath);
    const checkRoot = () => {
        if (allowedRoots && !allowedRoots.some((root) => isPathInside(root, real))) {
            throw new Error("Avatar is outside the authorized image directories");
        }
        if (fs.realpathSync(filePath) !== real)
            throw new Error("Image path changed during validation");
    };
    checkRoot();
    const fd = fs.openSync(real, fs.constants.O_RDONLY | fs.constants.O_NOFOLLOW | fs.constants.O_NONBLOCK);
    try {
        checkRoot();
        const stat = fs.fstatSync(fd);
        const current = fs.statSync(real);
        if (!stat.isFile() || stat.size < 1 || stat.size > exports.MAX_IMAGE_BYTES ||
            stat.dev !== current.dev || stat.ino !== current.ino) {
            throw new Error("Image must be a regular file no larger than 20 MiB");
        }
        // Bounded reads also handle a file growing after fstat without unbounded allocation.
        const buffer = Buffer.alloc(stat.size + 1);
        let length = 0;
        while (length < buffer.length) {
            const read = fs.readSync(fd, buffer, length, buffer.length - length, null);
            if (read === 0)
                break;
            length += read;
        }
        if (length !== stat.size)
            throw new Error("Image size changed during validation");
        const data = buffer.subarray(0, length);
        return { data, ...inspectImage(data) };
    }
    finally {
        fs.closeSync(fd);
    }
}
function readReferenceImage(filePath, allowedRoots) {
    if (!allowedRoots?.length)
        throw new Error("Explicit Agent reference authorization is required.");
    if (![".jpg", ".jpeg", ".png", ".webp"].includes(path.extname(filePath).toLowerCase())) {
        throw new Error("Avatar must use jpg, jpeg, png or webp format");
    }
    const image = readImageFile(filePath, allowedRoots);
    if (!["image/jpeg", "image/png", "image/webp"].includes(image.mimeType)) {
        throw new Error("Unsupported avatar image format");
    }
    return image;
}
//# sourceMappingURL=images.js.map