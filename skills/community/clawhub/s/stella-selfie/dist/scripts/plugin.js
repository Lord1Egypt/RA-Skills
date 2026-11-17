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
exports.InputError = exports.RESOLUTIONS = exports.AGENT_ID = void 0;
exports.prepareImageRequest = prepareImageRequest;
exports.generateForPlugin = generateForPlugin;
const fs = __importStar(require("node:fs"));
const path = __importStar(require("node:path"));
const identity_1 = require("./identity");
const avatars_1 = require("./avatars");
const images_1 = require("./images");
const errors_1 = require("./errors");
exports.AGENT_ID = /^[a-z0-9][a-z0-9_-]*$/;
exports.RESOLUTIONS = ["1K", "2K", "4K"];
class InputError extends Error {
    code;
    constructor(code, message) {
        super(message);
        this.code = code;
    }
}
exports.InputError = InputError;
function object(value) {
    return value !== null && typeof value === "object" && !Array.isArray(value)
        ? value : {};
}
function validateRequest(value) {
    const r = object(value);
    const allowed = ["schemaVersion", "agentId", "prompt", "resolution", "aspectRatio"];
    if (Object.keys(r).some(key => !allowed.includes(key)) || r.schemaVersion !== 1 ||
        typeof r.prompt !== "string" || !r.prompt.trim() || r.prompt.includes("\0") ||
        (r.agentId !== undefined && (typeof r.agentId !== "string" || !exports.AGENT_ID.test(r.agentId))) ||
        (r.resolution !== undefined && (typeof r.resolution !== "string" || !exports.RESOLUTIONS.includes(r.resolution))) ||
        (r.aspectRatio !== undefined && (typeof r.aspectRatio !== "string" || !/^\d+:\d+$/.test(r.aspectRatio)))) {
        throw new InputError("INPUT_INVALID", "Use a v1 single-image request with prompt, optional agentId, resolution and aspectRatio.");
    }
    return r;
}
function parseModelRef(model) {
    if (typeof model !== "string") {
        throw new InputError("CONFIG_INVALID", "Use a host native image model as provider/model.");
    }
    const slash = model.indexOf("/");
    if (slash <= 0 || slash === model.length - 1 || /\s/.test(model)) {
        throw new InputError("CONFIG_INVALID", "Use a host native image model as provider/model.");
    }
    return { model, providerId: model.slice(0, slash), modelId: model.slice(slash + 1) };
}
function geometrySupported(declared, allowed, value) {
    if (declared === false)
        return false;
    if (allowed)
        return allowed.includes(value);
    return declared === true;
}
function supportsResolution(provider, resolution) {
    return geometrySupported(provider.capabilities.edit.supportsResolution, provider.capabilities.geometry?.resolutions, resolution);
}
function supportsAspectRatio(provider, aspectRatio) {
    return geometrySupported(provider.capabilities.edit.supportsAspectRatio, provider.capabilities.geometry?.aspectRatios, aspectRatio);
}
function modelAccepted(models, modelId, fullRef) {
    return !!models && (models.includes(modelId) || models.includes(fullRef));
}
function settings(config, workspace) {
    const cfg = object(config);
    const entry = object(object(object(cfg.skills).entries)["stella-selfie"]);
    if (entry.config !== undefined && (entry.config === null || typeof entry.config !== "object" || Array.isArray(entry.config))) {
        throw new InputError("CONFIG_INVALID", "Stella config must be an object.");
    }
    const options = object(entry.config), legacy = object(entry.env);
    const get = (key, fallback) => Object.hasOwn(options, key) ? options[key]
        : process.env[key] ?? legacy[key] ?? fallback;
    const legacyProvider = process.env.Provider ?? legacy.Provider;
    if (legacyProvider !== undefined && legacyProvider !== "gemini") {
        throw new InputError("CONFIG_INVALID", "Remove the legacy Provider setting and use config.model for the host native image model.");
    }
    const parsed = parseModelRef(Object.hasOwn(options, "model") ? options.model : "google/gemini-3-pro-image");
    const blend = get("AvatarBlendEnabled", true);
    const max = get("AvatarMaxRefs", 3);
    const rawRoots = get("AvatarAllowedRoots", undefined);
    if (!(typeof blend === "boolean" || (typeof blend === "string" && ["true", "false"].includes(blend.toLowerCase()))) ||
        !(typeof max === "number" || (typeof max === "string" && /^\d+$/.test(max))) ||
        !Number.isInteger(Number(max)) || Number(max) < 1) {
        throw new InputError("CONFIG_INVALID", "Use a host native image model, a boolean AvatarBlendEnabled and a positive integer AvatarMaxRefs.");
    }
    let roots = rawRoots;
    if (typeof roots === "string") {
        try {
            roots = JSON.parse(roots);
        }
        catch {
            throw new InputError("CONFIG_INVALID", "AvatarAllowedRoots must be a non-empty array of absolute directories.");
        }
    }
    if (roots !== undefined && (!Array.isArray(roots) || roots.length === 0 ||
        !roots.every(root => typeof root === "string" && path.isAbsolute(root)))) {
        throw new InputError("CONFIG_INVALID", "AvatarAllowedRoots must be a non-empty array of absolute directories.");
    }
    let allowedRoots;
    try {
        // Do not realpath default children: an assets/avatars link must not authorize its outside target.
        allowedRoots = roots === undefined ? [path.join(workspace, "assets"), path.join(workspace, "avatars")]
            : roots.map(root => {
                const real = fs.realpathSync(root);
                if (!fs.statSync(real).isDirectory())
                    throw new Error("Not a directory");
                return real;
            });
    }
    catch {
        throw new InputError("CONFIG_INVALID", "An authorized reference directory is unavailable.");
    }
    return { ...parsed, blend: String(blend).toLowerCase() !== "false", max: Number(max), allowedRoots };
}
/** Shared validated inputs for native chat tools and in-process plugin calls. */
function prepareImageRequest(api, integration, value, onReference = () => { }) {
    const request = validateRequest(value);
    const agentId = request.agentId ?? "main";
    if (!integration.listAgentIds(api.config).includes(agentId)) {
        throw new InputError("AGENT_NOT_FOUND", `The bound Agent '${agentId}' does not exist.`);
    }
    let workspace;
    try {
        workspace = fs.realpathSync(api.runtime.agent.resolveAgentWorkspaceDir(api.config, agentId));
    }
    catch {
        throw new InputError("IDENTITY_UNREADABLE", "The bound Agent workspace is unavailable.");
    }
    const config = settings(api.config, workspace);
    const provider = api.runtime.imageGeneration.listProviders({ config: api.config }).find(p => p.id === config.providerId);
    const maxInputImages = provider?.capabilities.edit.maxInputImages;
    const maxRefs = maxInputImages !== undefined ? Math.min(16, maxInputImages) : 5;
    if (!provider?.capabilities.edit.enabled || !modelAccepted(provider.models, config.modelId, config.model) || config.max > maxRefs) {
        throw new InputError("CONFIG_INVALID", "The selected native image model or reference count is unsupported by this host.");
    }
    if ((request.resolution !== undefined && !supportsResolution(provider, request.resolution)) ||
        (request.aspectRatio !== undefined && !supportsAspectRatio(provider, request.aspectRatio))) {
        throw new InputError("INPUT_INVALID", "The selected model does not support the requested resolution or aspect ratio.");
    }
    const agentDir = api.runtime.agent.resolveAgentDir(api.config, agentId);
    if (!path.isAbsolute(agentDir))
        throw new InputError("CONFIG_INVALID", "The host must resolve an absolute Agent authentication directory.");
    onReference();
    let identity;
    try {
        identity = (0, identity_1.parseIdentity)(workspace);
    }
    catch {
        throw new InputError("IDENTITY_UNREADABLE", "The bound Agent IDENTITY.md could not be read.");
    }
    const references = (0, avatars_1.selectAvatars)({
        ...identity, avatarMaxRefs: config.max, avatarBlendEnabled: config.blend,
        allowedRoots: config.allowedRoots, onWarning: integration.onWarning ?? (() => { }),
    });
    if (references.length === 0)
        throw new InputError("NO_VALID_REFERENCE", "At least one authorized JPEG, PNG or WebP reference is required.");
    // First-read bytes cross the runtime boundary; do not reopen the original path.
    const inputImages = references.map(({ buffer, mimeType }) => ({ buffer, mimeType }));
    const params = {
        cfg: api.config, agentDir, prompt: request.prompt, modelOverride: config.model,
        autoProviderFallback: false, count: 1, inputImages,
        ...(request.resolution !== undefined ? { resolution: request.resolution }
            : supportsResolution(provider, "2K") ? { resolution: "2K" } : {}),
        ...(request.aspectRatio !== undefined ? { aspectRatio: request.aspectRatio } : {}),
    };
    return { agentId, workspace, params };
}
/** Generate one in-memory persona image. The caller owns preview, persistence and publishing. */
async function generateForPlugin(api, integration, value) {
    let stage = "validate";
    let generationOutcome = "not_started";
    try {
        const { agentId, params } = prepareImageRequest(api, integration, value, () => { stage = "reference"; });
        stage = "generate";
        generationOutcome = "unknown";
        const result = await api.runtime.imageGeneration.generate(params);
        generationOutcome = "succeeded";
        const { providerId, modelId, model } = parseModelRef(params.modelOverride);
        if (result.provider !== providerId || !modelAccepted([result.model], modelId, model) ||
            result.ignoredOverrides.length > 0 || result.images.length !== 1 || !Buffer.isBuffer(result.images[0].buffer)) {
            throw new InputError("OUTPUT_INVALID", "The native result did not satisfy the single-image request.");
        }
        const image = result.images[0];
        // Native output limits belong to the host; the 20 MiB reference cap is not an output cap.
        let format;
        try {
            format = (0, images_1.inspectImage)(image.buffer, image.buffer.length);
        }
        catch {
            throw new InputError("OUTPUT_INVALID", "The native provider returned an empty or invalid image.");
        }
        if (format.mimeType !== image.mimeType)
            throw new InputError("OUTPUT_INVALID", "The image content and MIME type disagree.");
        return { schemaVersion: 1, ok: true, agentId, generatedAt: new Date().toISOString(),
            image: { buffer: image.buffer, mimeType: format.mimeType } };
    }
    catch (error) {
        if (error instanceof InputError) {
            return { schemaVersion: 1, ok: false, error: {
                    code: error.code, stage, generationOutcome, message: error.message,
                    actionHint: (0, errors_1.localActionHint)(error.code),
                } };
        }
        const details = (0, errors_1.normalizeNativeError)(error);
        return { schemaVersion: 1, ok: false, error: {
                code: details.code, stage, generationOutcome,
                // Never expose the provider's raw response, key, original error or stack to the calling workflow.
                message: details.message, actionHint: details.actionHint,
            } };
    }
}
//# sourceMappingURL=plugin.js.map