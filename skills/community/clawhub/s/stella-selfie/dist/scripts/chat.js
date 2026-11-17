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
exports.parseProviderInventory = parseProviderInventory;
exports.readChatState = readChatState;
exports.prepareChat = prepareChat;
exports.releaseReferences = releaseReferences;
const fs = __importStar(require("node:fs"));
const path = __importStar(require("node:path"));
const node_crypto_1 = require("node:crypto");
const plugin_1 = require("./plugin");
const images_1 = require("./images");
const native_cli_1 = require("./native-cli");
function isRecord(value) {
    return value !== null && typeof value === "object" && !Array.isArray(value);
}
function optionalStringList(value, label) {
    if (value === undefined)
        return undefined;
    if (!Array.isArray(value) || !value.every(item => typeof item === "string")) {
        throw new plugin_1.InputError("CONFIG_INVALID", `Unsupported native image provider inventory: ${label}.`);
    }
    return value;
}
function parseProviderInventory(value) {
    const items = Array.isArray(value) ? value
        : isRecord(value) && Array.isArray(value.providers) ? value.providers
            : undefined;
    if (!items)
        throw new plugin_1.InputError("CONFIG_INVALID", "Unsupported native image provider inventory.");
    const providers = [];
    for (const item of items) {
        if (!isRecord(item) || typeof item.id !== "string" || !item.id) {
            throw new plugin_1.InputError("CONFIG_INVALID", "Unsupported native image provider inventory.");
        }
        if (Object.hasOwn(item, "available") && item.available !== true)
            continue;
        if (Object.hasOwn(item, "configured") && item.configured !== true)
            continue;
        if (!isRecord(item.capabilities) || !isRecord(item.capabilities.edit) || typeof item.capabilities.edit.enabled !== "boolean") {
            throw new plugin_1.InputError("CONFIG_INVALID", "Unsupported native image provider inventory.");
        }
        const edit = item.capabilities.edit;
        const enabled = edit.enabled;
        const maxInputImages = edit.maxInputImages;
        const supportsResolution = edit.supportsResolution;
        const supportsAspectRatio = edit.supportsAspectRatio;
        if (typeof enabled !== "boolean"
            || (maxInputImages !== undefined && (typeof maxInputImages !== "number" || !Number.isInteger(maxInputImages)))
            || (supportsResolution !== undefined && typeof supportsResolution !== "boolean")
            || (supportsAspectRatio !== undefined && typeof supportsAspectRatio !== "boolean")) {
            throw new plugin_1.InputError("CONFIG_INVALID", "Unsupported native image provider inventory.");
        }
        const geometry = item.capabilities.geometry === undefined ? undefined
            : isRecord(item.capabilities.geometry) ? {
                aspectRatios: optionalStringList(item.capabilities.geometry.aspectRatios, "aspectRatios"),
                resolutions: optionalStringList(item.capabilities.geometry.resolutions, "resolutions"),
            } : undefined;
        if (item.capabilities.geometry !== undefined && !geometry) {
            throw new plugin_1.InputError("CONFIG_INVALID", "Unsupported native image provider inventory.");
        }
        providers.push({
            id: item.id,
            models: optionalStringList(item.models, "models"),
            capabilities: {
                edit: {
                    enabled,
                    ...(maxInputImages !== undefined ? { maxInputImages } : {}),
                    ...(supportsResolution !== undefined ? { supportsResolution } : {}),
                    ...(supportsAspectRatio !== undefined ? { supportsAspectRatio } : {}),
                },
                ...(geometry ? { geometry } : {}),
            },
        });
    }
    return providers;
}
async function readChatState(agentId) {
    const agents = await (0, native_cli_1.readAgentLocations)();
    if (!agents.some(a => a.id === agentId))
        throw new plugin_1.InputError("AGENT_NOT_FOUND", "The current conversation Agent does not exist.");
    const [skills, inventory] = await Promise.all([
        (0, native_cli_1.runOpenClawJson)(["config", "get", "skills", "--json"]).catch(error => {
            if (error instanceof native_cli_1.MissingConfigPathError)
                return {};
            throw error;
        }),
        (0, native_cli_1.runOpenClawJson)(["infer", "image", "providers", "--agent", agentId, "--json"]),
    ]);
    return { agents, skills, providers: parseProviderInventory(inventory) };
}
function checkedDirectory(workspace, directory) {
    if (fs.lstatSync(directory).isSymbolicLink() || !fs.statSync(directory).isDirectory()) {
        throw new plugin_1.InputError("CONFIG_INVALID", "Reference scratch directories must be real directories.");
    }
    const real = fs.realpathSync(directory);
    if (!(0, images_1.isPathInside)(workspace, real))
        throw new plugin_1.InputError("CONFIG_INVALID", "Reference scratch path leaves the Agent workspace.");
    return real;
}
function scratchRoot(workspace, create) {
    let current = fs.realpathSync(workspace);
    for (const segment of ["stella-selfie", ".references"]) {
        current = path.join(current, segment);
        if (create) {
            try {
                fs.mkdirSync(current, { mode: 0o700 });
            }
            catch (error) {
                if (error.code !== "EEXIST")
                    throw error;
            }
        }
        checkedDirectory(workspace, current);
    }
    return current;
}
function host(state) {
    return { config: { skills: state.skills }, runtime: {
            agent: {
                resolveAgentWorkspaceDir: (_cfg, id) => state.agents.find(a => a.id === id).workspace,
                resolveAgentDir: (_cfg, id) => state.agents.find(a => a.id === id).agentDir,
            },
            imageGeneration: {
                listProviders: () => state.providers,
            },
        } };
}
function prepareChat(request, state) {
    if (!request || typeof request.agentId !== "string" || !request.agentId ||
        (request.caption !== undefined && typeof request.caption !== "string")) {
        throw new plugin_1.InputError("INPUT_INVALID", "Specify the actual conversation Agent and an optional text caption.");
    }
    const { caption, ...imageRequest } = request;
    const prepared = (0, plugin_1.prepareImageRequest)(host(state), { listAgentIds: () => state.agents.map(a => a.id), onWarning: m => console.error(m) }, imageRequest);
    const root = scratchRoot(prepared.workspace, true);
    const id = (0, node_crypto_1.randomUUID)();
    const directory = fs.mkdtempSync(path.join(root, `${id}-`));
    const token = path.basename(directory);
    const createdFiles = [];
    const writeSnapshot = (name, data) => {
        checkedDirectory(prepared.workspace, directory);
        const fd = fs.openSync(path.join(directory, name), "wx", 0o600);
        // Register ownership before writing: writeFileSync can fail after a partial write.
        createdFiles.push(name);
        try {
            fs.writeFileSync(fd, data);
        }
        catch (error) {
            try {
                fs.closeSync(fd);
            }
            catch { /* Preserve the original write failure. */ }
            throw error;
        }
        fs.closeSync(fd);
    };
    try {
        const files = prepared.params.inputImages.map((image, index) => {
            const name = `ref-${index}${(0, images_1.inspectImage)(image.buffer).extension}`;
            writeSnapshot(name, image.buffer);
            return name;
        });
        writeSnapshot("manifest.json", JSON.stringify({ schemaVersion: 1, kind: "stella-reference-snapshot", agentId: request.agentId, token, files }));
        const { modelOverride, prompt, count, resolution, aspectRatio } = prepared.params;
        return { schemaVersion: 1, ok: true, agentId: request.agentId, referenceToken: token,
            toolInput: { model: modelOverride, prompt, count, images: files.map(name => path.join(directory, name)),
                ...(resolution !== undefined ? { resolution } : {}), ...(aspectRatio ? { aspectRatio } : {}) },
            ...(caption !== undefined ? { caption } : {}),
        };
    }
    catch (error) {
        // Try every owned file, including partial references/manifest, without masking the original error.
        let cleanupFailed = false;
        for (const name of createdFiles) {
            try {
                checkedDirectory(prepared.workspace, directory);
                const file = path.join(directory, name);
                const stat = fs.lstatSync(file);
                if (!stat.isFile() || stat.isSymbolicLink() || !(0, images_1.isPathInside)(directory, fs.realpathSync(file))) {
                    throw new Error("Reference file changed during cleanup.");
                }
                fs.unlinkSync(file);
            }
            catch (cleanupError) {
                if (cleanupError.code !== "ENOENT")
                    cleanupFailed = true;
            }
        }
        try {
            checkedDirectory(prepared.workspace, directory);
            if (fs.readdirSync(directory).length === 0)
                fs.rmdirSync(directory);
            else
                cleanupFailed = true;
        }
        catch {
            cleanupFailed = true;
        }
        if (cleanupFailed)
            console.error(`[stella] Warning: Input scratch cleanup incomplete at ${JSON.stringify(directory)}; explicit cleanup is required.`);
        throw error;
    }
}
function releaseReferences(agent, token) {
    if (!/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}-[A-Za-z0-9]{6}$/.test(token)) {
        throw new plugin_1.InputError("INPUT_INVALID", "Invalid reference token.");
    }
    const workspace = fs.realpathSync(agent.workspace);
    const directory = path.join(scratchRoot(workspace, false), token);
    if (!fs.existsSync(directory))
        return { schemaVersion: 1, ok: true, released: false };
    checkedDirectory(workspace, directory);
    const manifestFile = path.join(directory, "manifest.json");
    const manifestStat = fs.lstatSync(manifestFile);
    if (!manifestStat.isFile() || manifestStat.isSymbolicLink() || manifestStat.size > 8192) {
        throw new plugin_1.InputError("INPUT_INVALID", "Invalid reference manifest file.");
    }
    let parsed;
    try {
        parsed = JSON.parse(fs.readFileSync(manifestFile, "utf8"));
    }
    catch {
        throw new plugin_1.InputError("INPUT_INVALID", "Invalid reference manifest file.");
    }
    const files = isRecord(parsed)
        && parsed.kind === "stella-reference-snapshot"
        && parsed.schemaVersion === 1
        && parsed.agentId === agent.id
        && parsed.token === token
        && Array.isArray(parsed.files)
        && parsed.files.length >= 1 && parsed.files.length <= 5
        && parsed.files.every((name) => typeof name === "string" && /^ref-[0-4]\.(jpg|png|webp)$/.test(name))
        ? parsed.files : undefined;
    if (!files || fs.readdirSync(directory).some(name => name !== "manifest.json" && !files.includes(name))) {
        throw new plugin_1.InputError("INPUT_INVALID", "Reference manifest does not match this Agent or contains unexpected files.");
    }
    for (const name of [...files, "manifest.json"]) {
        checkedDirectory(workspace, directory);
        const file = path.join(directory, name);
        if (!fs.existsSync(file))
            continue;
        if (fs.lstatSync(file).isSymbolicLink() || !(0, images_1.isPathInside)(directory, fs.realpathSync(file)))
            throw new plugin_1.InputError("INPUT_INVALID", "Reference file changed during cleanup.");
        fs.unlinkSync(file);
    }
    fs.rmdirSync(directory);
    return { schemaVersion: 1, ok: true, released: true };
}
//# sourceMappingURL=chat.js.map