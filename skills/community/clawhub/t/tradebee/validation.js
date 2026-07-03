import { randomUUID } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

export function isPlainObject(value) {
    return !!value && typeof value === "object" && !Array.isArray(value);
}

export function cloneJson(value) {
    if (value == null) {
        return value;
    }

    return JSON.parse(JSON.stringify(value));
}

export function getApiKeyOrError(args = {}) {
    let envApiKey = "";
    try {
        envApiKey = process.env.BEE_API_KEY || "";
    } catch {
        envApiKey = "";
    }

    const API_KEY = envApiKey;

    if (!API_KEY) {
        return {
            error: {
                status: false,
                msg: "Missing API_KEY. Configure BEE_API_KEY in the environment before use."
            }
        };
    }

    return { apiKey: API_KEY };
}

export function hasOwn(object, key) {
    return isPlainObject(object) && Object.prototype.hasOwnProperty.call(object, key);
}

export function validateLanguage(language, { required = true } = {}) {
    if (language == null || language === "") {
        return required
            ? "Missing required parameter: language."
            : null;
    }

    if (typeof language !== "string" || !/^[a-z]{2}$/.test(language.trim())) {
        return "Invalid parameter: language. Use an exact enabled site language code returned by languages-get, for example en. Do not guess or translate the language value.";
    }

    return null;
}

export function validateRuleScene(scene, { required = true } = {}) {
    if (scene == null || scene === "") {
        return required
            ? "Missing required parameter: scene."
            : null;
    }

    if (typeof scene !== "string") {
        return "Invalid parameter: scene. Use one exact supported scene value.";
    }

    const normalizedScene = scene.trim();
    const allowedScenes = new Set([
        "blog.description",
        "faq.answer",
        "products.description",
        "productsgroup.section.top",
        "productsgroup.section.bottom",
        "custompage.content"
    ]);

    if (!allowedScenes.has(normalizedScene)) {
        return "Invalid parameter: scene. Supported values: blog.description, faq.answer, products.description, productsgroup.section.top, productsgroup.section.bottom, custompage.content.";
    }

    return null;
}

export function validatePagination(args = {}) {
    const currentPageRaw = args.pagination?.current_page ?? args.current_page ?? 1;
    const pageSizeRaw = args.pagination?.page_size ?? args.page_size ?? 5;

    const current_page = Number(currentPageRaw);
    if (!Number.isInteger(current_page) || current_page < 1) {
        return {
            error: "Invalid parameter: pagination.current_page. It must be an integer greater than or equal to 1."
        };
    }

    const page_size = Number(pageSizeRaw);
    if (!Number.isInteger(page_size) || page_size < 1 || page_size > 10) {
        return {
            error: "Invalid parameter: pagination.page_size. It must be an integer between 1 and 10."
        };
    }

    return { current_page, page_size };
}

export function validateFields(fields, allowedFields) {
    if (fields == null) {
        return null;
    }

    if (!Array.isArray(fields)) {
        return "Invalid parameter: fields. It must be an array of field names supported by this API.";
    }

    if (fields.some((field) => typeof field !== "string" || !allowedFields.includes(field))) {
        return `Invalid parameter: fields. Supported values: ${allowedFields.join(", ")}.`;
    }

    return null;
}

export function validateIdList(idList) {
    if (!Array.isArray(idList)) {
        return "Missing required parameter: id_list.";
    }

    if (idList.length < 1 || idList.length > 100) {
        return "Invalid parameter: id_list. It must contain 1 to 100 items.";
    }

    if (idList.some((id) => !Number.isInteger(Number(id)) || Number(id) <= 0)) {
        return "Invalid parameter: id_list. Every item must be a positive integer.";
    }

    return null;
}

export function validateString(value, path, { required = false, min = 0, max = Number.MAX_SAFE_INTEGER } = {}) {
    if (value == null || value === "") {
        return required ? `Missing required parameter: ${path}.` : null;
    }

    if (typeof value !== "string") {
        return `Invalid parameter: ${path}.`;
    }

    const length = value.trim().length;
    if (required && length < min) {
        return `Missing required parameter: ${path}.`;
    }

    if ((!required && value.length > 0 && value.length < min) || value.length > max) {
        return `Invalid parameter: ${path}.`;
    }

    return null;
}

export function validateSeo(
    seo,
    prefix,
    {
        mode = "create",
        actionLabel = null,
        descriptionFieldName = "description",
        descriptionMax = 200
    } = {}
) {
    if (seo == null) {
        return null;
    }

    if (!isPlainObject(seo)) {
        return `Invalid parameter: ${prefix}.seo.`;
    }

    const suffix = mode === "update"
        ? ` for ${actionLabel || "update"}`
        : "";

    if (hasOwn(seo, "title")) {
        if (typeof seo.title !== "string" || (seo.title.length > 0 && seo.title.length > 90)) {
            return `Invalid parameter: ${prefix}.seo.title. If provided${suffix}, it must contain 1 to 90 characters${mode === "update" ? ". Omit this field to keep the current SEO title unchanged." : "."}`;
        }
    }

    if (hasOwn(seo, descriptionFieldName)) {
        if (typeof seo[descriptionFieldName] !== "string" || (seo[descriptionFieldName].length > 0 && seo[descriptionFieldName].length > descriptionMax)) {
            return `Invalid parameter: ${prefix}.seo.${descriptionFieldName}. If provided${suffix}, it must contain 1 to ${descriptionMax} characters${mode === "update" ? `. Omit this field to keep the current SEO ${descriptionFieldName} unchanged.` : "."}`;
        }
    }

    if (hasOwn(seo, "keywords")) {
        if (typeof seo.keywords !== "string" || (seo.keywords.length > 0 && seo.keywords.length > 120)) {
            return `Invalid parameter: ${prefix}.seo.keywords. If provided${suffix}, send one comma-separated string with total length 1 to 120 characters${mode === "update" ? ". Omit this field to keep the current SEO keywords unchanged." : "."}`;
        }
    }

    return null;
}

export function validateTags(tags, path, { required = false, minItems = 0, maxItems = 6, minTagLength = 1, maxTagLength = 50, unique = false } = {}) {
    if (tags == null) {
        return required ? `Missing required parameter: ${path}.` : null;
    }

    if (!Array.isArray(tags)) {
        return `Invalid parameter: ${path}.`;
    }

    if (tags.length < minItems || tags.length > maxItems) {
        return `Invalid parameter: ${path}.`;
    }

    const normalized = [];
    for (const tag of tags) {
        if (typeof tag !== "string" || tag.length < minTagLength || tag.length > maxTagLength) {
            return `Invalid parameter: ${path}.`;
        }
        normalized.push(tag.toLowerCase());
    }

    if (unique && new Set(normalized).size !== normalized.length) {
        return `Invalid parameter: ${path}.`;
    }

    return null;
}

export function validateImages(images, { required = false } = {}) {
    if (images == null) {
        return required ? "Invalid parameter: products.upload_images. For products-create, provide 1 to 5 images. The first image is the main image. Each image must be valid base64 with a supported format and must be 500 kB or smaller." : null;
    }

    if (!Array.isArray(images) || images.length < (required ? 1 : 0) || images.length > 5) {
        return required
            ? "Invalid parameter: products.upload_images. For products-create, provide 1 to 5 images. The first image is the main image. Each image must be valid base64 with a supported format and must be 500 kB or smaller."
            : "Invalid parameter: products.upload_images. If provided, supply 0 to 5 images. Each image must be a {name, base64} object.";
    }

    for (const image of images) {
        if (!isPlainObject(image) || typeof image.name !== "string" || !image.name.trim() || typeof image.base64 !== "string" || !image.base64.trim()) {
            return required
                ? "Invalid parameter: products.upload_images. For products-create, provide 1 to 5 images. The first image is the main image. Each image must be valid base64 with a supported format and must be 500 kB or smaller."
                : "Invalid parameter: products.upload_images. If provided, supply 0 to 5 images. Each image must be a {name, base64} object.";
        }
    }

    return null;
}

export function validateAttributes(attributes) {
    if (attributes == null) {
        return null;
    }

    if (!Array.isArray(attributes) || attributes.length > 15) {
        return "Invalid parameter: products.attributes. If provided, supply 0 to 15 attribute objects.";
    }

    for (const attribute of attributes) {
        if (!isPlainObject(attribute)
            || typeof attribute.name !== "string"
            || attribute.name.length < 1
            || attribute.name.length > 100
            || typeof attribute.value !== "string"
            || attribute.value.length < 1
            || attribute.value.length > 100) {
            return "Invalid parameter: products.attributes. Each item must include name and value strings with 1 to 100 characters.";
        }
    }

    return null;
}

export function getHtmlLengthWithoutImages(html) {
    if (typeof html !== "string" || html === "") {
        return 0;
    }

    return html.replace(/<img\b[^>]*>/gi, "").length;
}

export function getHtmlImageCount(html) {
    if (typeof html !== "string" || html === "") {
        return 0;
    }

    const matches = html.match(/<img\b[^>]*>/gi);
    return matches ? matches.length : 0;
}

export function validateHtmlWithoutH1(html, path, { required = false, actionLabel = "update", maxImageCount = 20 } = {}) {
    if (html == null || html === "") {
        return required ? `Missing required parameter: ${path}.` : null;
    }

    if (typeof html !== "string") {
        return `Invalid parameter: ${path}.`;
    }

    if (/<\s*\/?\s*h1\b/i.test(html)) {
        return `Invalid parameter: ${path}. ${path} must not contain <h1> tags${required ? "" : ` for ${actionLabel}`}. Use <h2> to <h6> or normal block elements instead.`;
    }

    if (getHtmlLengthWithoutImages(html) > 100000) {
        return `Invalid parameter: ${path}. ${path} must contain 1 to 100000 HTML characters after removing <img> tags${required ? "" : ` for ${actionLabel}`}.`;
    }

    if (getHtmlImageCount(html) > maxImageCount) {
        return `Invalid parameter: ${path}. At most ${maxImageCount} <img> tags are allowed${required ? "" : ` for ${actionLabel}`}.`;
    }

    return null;
}

export function validateSection(section, path, { mode = "create", actionLabel = null, maxImageCount = 20 } = {}) {
    if (section == null) {
        return null;
    }

    if (!isPlainObject(section)) {
        return `Invalid parameter: ${path}.`;
    }

    const suffix = mode === "update"
        ? ` for ${actionLabel || "update"}`
        : "";

    if (hasOwn(section, "top")) {
        if (typeof section.top !== "string" || getHtmlLengthWithoutImages(section.top) > 100000) {
            return `Invalid parameter: ${path}.top. If provided${suffix}, it must contain 0 to 100,000 HTML characters after removing <img> tags and must follow the current rule-get fragment structure${mode === "update" ? ". Omit this field to keep the current section top unchanged." : "."}`;
        }
        if (getHtmlImageCount(section.top) > maxImageCount) {
            return `Invalid parameter: ${path}.top. If provided${suffix}, at most ${maxImageCount} <img> tags are allowed${mode === "update" ? ". Omit this field to keep the current section top unchanged." : "."}`;
        }
        if (/<\s*\/?\s*h1\b/i.test(section.top)) {
            return `Invalid parameter: ${path}.top. If provided${suffix}, it must not contain <h1> tags. Use <h2> to <h6> or normal block elements instead${mode === "update" ? ". Omit this field or pass an empty string to keep the current section top unchanged." : "."}`;
        }
    }

    if (hasOwn(section, "bottom")) {
        if (typeof section.bottom !== "string" || getHtmlLengthWithoutImages(section.bottom) > 100000) {
            return `Invalid parameter: ${path}.bottom. If provided${suffix}, it must contain 0 to 100,000 HTML characters after removing <img> tags and must follow the current rule-get fragment structure${mode === "update" ? ". Omit this field to keep the current section bottom unchanged." : "."}`;
        }
        if (getHtmlImageCount(section.bottom) > maxImageCount) {
            return `Invalid parameter: ${path}.bottom. If provided${suffix}, at most ${maxImageCount} <img> tags are allowed${mode === "update" ? ". Omit this field to keep the current section bottom unchanged." : "."}`;
        }
        if (/<\s*\/?\s*h1\b/i.test(section.bottom)) {
            return `Invalid parameter: ${path}.bottom. If provided${suffix}, it must not contain <h1> tags. Use <h2> to <h6> or normal block elements instead${mode === "update" ? ". Omit this field or pass an empty string to keep the current section bottom unchanged." : "."}`;
        }
    }

    return null;
}

export async function callTradebeeApi(url, apiKey, body) {
    const response = await fetch(
        url,
        {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${apiKey}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        }
    );

    if (!response.ok) {
        throw new Error("HTTP ERROR");
    }

    return await response.json();
}

export function appendPreviewNotice(result, message = "Preview the returned url in a browser.") {
    if (!isPlainObject(result)) {
        return result;
    }

    if (result.status !== true || !isPlainObject(result.data) || typeof result.data.url !== "string" || !result.data.url.trim()) {
        return result;
    }

    const next = { ...result };
    const baseMessage = typeof next.msg === "string" && next.msg.trim()
        ? next.msg.trim()
        : "Request succeeded.";

    if (!baseMessage.includes(message)) {
        next.msg = `${baseMessage} ${message}`;
    }

    return next;
}

export function extractFirstRecord(response, preferredKeys = []) {
    const candidates = [];

    const collect = (value) => {
        if (Array.isArray(value)) {
            for (const item of value) {
                if (isPlainObject(item)) {
                    candidates.push(item);
                }
            }
            return;
        }

        if (isPlainObject(value)) {
            candidates.push(value);
        }
    };

    if (isPlainObject(response)) {
        collect(response.data);
        collect(response.list);
        collect(response.result);
    }

    if (isPlainObject(response?.data)) {
        for (const key of preferredKeys) {
            collect(response.data[key]);
        }

        for (const [key, value] of Object.entries(response.data)) {
            if (preferredKeys.includes(key)) {
                continue;
            }
            collect(value);
        }
    }

    return candidates.find((item) => isPlainObject(item)) || null;
}

export function withDefinedProperties(source, allowedKeys) {
    const target = {};
    for (const key of allowedKeys) {
        if (source[key] !== undefined) {
            target[key] = cloneJson(source[key]);
        }
    }
    return target;
}

export function firstPositiveInteger(...values) {
    for (const value of values) {
        const numericValue = Number(value);
        if (Number.isInteger(numericValue) && numericValue > 0) {
            return numericValue;
        }
    }

    return undefined;
}

const skillRootDir = path.dirname(fileURLToPath(import.meta.url));
const backupRootDir = path.join(skillRootDir, "backups");

function sanitizeFileNamePart(value, fallback = "unknown") {
    const text = String(value ?? "").trim();
    if (!text) {
        return fallback;
    }

    return text.replace(/[^a-zA-Z0-9_-]+/g, "-").replace(/-+/g, "-").replace(/^-|-$/g, "") || fallback;
}

// Persists the full pre-update backup bundle to local disk for later restoration.
// Warning: the saved JSON file can contain sensitive business or personal data
// from confirmation_summary, raw_read_response, snapshot,
// requested_update_payload, restore_payload, and restore_limitations.
export async function saveBackupToFile({
    action,
    language,
    entityId,
    rawReadResponse,
    snapshot,
    requestedPayload,
    restoreAction,
    restorePayload,
    restoreLimitations = [],
    confirmationSummary = ""
} = {}) {
    const timestamp = new Date().toISOString();
    const timestampForFile = timestamp.replace(/[:.]/g, "-");
    const backupId = randomUUID();
    const actionPart = sanitizeFileNamePart(action, "action");
    const languagePart = sanitizeFileNamePart(language, "lang");
    const entityPart = sanitizeFileNamePart(entityId, "entity");
    const fileName = `${timestampForFile}_${actionPart}_${languagePart}_${entityPart}_${backupId}.json`;
    const directoryPath = path.join(backupRootDir, actionPart);
    const filePath = path.join(directoryPath, fileName);

    const backupDocument = {
        backup_id: backupId,
        saved_at: timestamp,
        action,
        language,
        entity_id: entityId,
        confirmation_summary: confirmationSummary,
        raw_read_response: cloneJson(rawReadResponse),
        snapshot: cloneJson(snapshot),
        requested_update_payload: cloneJson(requestedPayload),
        restore_action: restoreAction,
        restore_payload: cloneJson(restorePayload),
        restore_limitations: cloneJson(restoreLimitations)
    };

    await mkdir(directoryPath, { recursive: true });
    await writeFile(filePath, `${JSON.stringify(backupDocument, null, 2)}\n`, "utf8");

    return {
        backup_id: backupId,
        saved_at: timestamp,
        directory_path: directoryPath,
        file_path: filePath,
        file_name: fileName
    };
}
