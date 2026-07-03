import { appendPreviewNotice, callTradebeeApi, extractFirstRecord, firstPositiveInteger, getApiKeyOrError, getHtmlLengthWithoutImages, hasOwn, isPlainObject, saveBackupToFile, validateHtmlWithoutH1, validateImages, validateLanguage, validateSeo, validateTags, withDefinedProperties } from "../validation.js";

function buildRestorePayload(snapshot = {}) {
    return withDefinedProperties(
        {
            faq_id: firstPositiveInteger(snapshot.faq_id),
            faqgroup_id: firstPositiveInteger(snapshot.faqgroup_id, snapshot.group?.faqgroup_id, snapshot.group?.id),
            question: snapshot.question,
            tags: snapshot.tags,
            summary: snapshot.summary,
            answer: snapshot.answer,
            seo: snapshot.seo
        },
        [
            "faq_id",
            "faqgroup_id",
            "question",
            "tags",
            "summary",
            "answer",
            "seo"
        ]
    );
}

export default async function FaqUpdate(args = {}) {
    if (!args || typeof args !== "object" || Array.isArray(args)) {
        return {
            status: false,
            msg: "Invalid parameter: request.body. It must be a valid JSON object."
        };
    }

    const { apiKey: API_KEY, error: apiKeyError } = getApiKeyOrError(args);
    if (apiKeyError) return apiKeyError;

    if (!args.confirmation || typeof args.confirmation !== "object" || Array.isArray(args.confirmation)) {
        return {
            status: false,
            msg: "Missing required parameter: confirmation. Before updating an FAQ, require explicit user confirmation that includes the language, target FAQ ID, and payload."
        };
    }

    if (args.confirmation.approved !== true) {
        return {
            status: false,
            msg: "Explicit user confirmation is required before updating an FAQ. Set confirmation.approved=true only after showing the user the language, target FAQ ID, and payload to be changed."
        };
    }

    if (typeof args.confirmation.summary !== "string" || !args.confirmation.summary.trim()) {
        return {
            status: false,
            msg: "Missing required parameter: confirmation.summary. It must summarize the language, target FAQ ID, and payload confirmed by the user."
        };
    }

    const languageError = validateLanguage(args.language);
    if (languageError) {
        return {
            status: false,
            msg: languageError
        };
    }

    if (!isPlainObject(args.faq)) {
        return {
            status: false,
            msg: "Missing required parameter: faq."
        };
    }

    const faqId = Number(args.faq.faq_id ?? 0);
    if (!Number.isInteger(faqId) || faqId <= 0) {
        return {
            status: false,
            msg: "Invalid parameter: faq.faq_id. The FAQ does not exist, does not belong to this account, or does not belong to the selected language. Use faq-read with the same language to get the correct faq_id first."
        };
    }

    if (hasOwn(args.faq, "faqgroup_id")) {
        const faqGroupId = Number(args.faq.faqgroup_id);
        if (!Number.isInteger(faqGroupId) || faqGroupId <= 0) {
            return {
                status: false,
                msg: "Invalid parameter: faq.faqgroup_id. Omit this field to keep the current group unchanged. If provided, it must be a positive FAQ group ID selected from faqgroup-read."
            };
        }
    }

    if (hasOwn(args.faq, "cover_image")) {
        const imagesError = validateImages(args.faq.cover_image == null ? [] : [args.faq.cover_image], { required: false });
        if (imagesError) {
            return {
                status: false,
                msg: "Invalid parameter: faq.cover_image. If provided, it must be one {name, base64} object with a valid image not larger than 500 kB."
            };
        }
    }

    if (hasOwn(args.faq, "question")
        && (typeof args.faq.question !== "string" || args.faq.question.length > 100)) {
        return {
            status: false,
            msg: "Invalid parameter: faq.question. If provided for faq-update, it must contain 1 to 100 characters. Omit this field to keep the current question unchanged."
        };
    }

    if (hasOwn(args.faq, "tags")) {
        const tagsError = validateTags(args.faq.tags, "faq.tags", {
            required: false,
            minItems: 0,
            maxItems: 6,
            minTagLength: 3,
            maxTagLength: 50,
            unique: true
        });
        if (tagsError) {
            return {
                status: false,
                msg: "Invalid parameter: faq.tags. If provided, supply 0 to 6 unique tags. Each tag must be 3 to 50 characters."
            };
        }
    }

    if (hasOwn(args.faq, "summary")
        && (typeof args.faq.summary !== "string" || args.faq.summary.length > 500)) {
        return {
            status: false,
            msg: "Invalid parameter: faq.summary. If provided for faq-update, it must contain 1 to 500 characters. Omit this field to keep the current summary unchanged."
        };
    }

    if (hasOwn(args.faq, "answer")
        && (typeof args.faq.answer !== "string" || getHtmlLengthWithoutImages(args.faq.answer) > 100000)) {
        return {
            status: false,
            msg: "Invalid parameter: faq.answer. If provided for faq-update, it must contain 1 to 100000 HTML characters after removing <img> tags. Omit this field to keep the current answer unchanged."
        };
    }

    if (hasOwn(args.faq, "answer")) {
        const answerStructureError = validateHtmlWithoutH1(args.faq.answer, "faq.answer", {
            actionLabel: "faq-update",
            maxImageCount: 50
        });
        if (answerStructureError) {
            return {
                status: false,
                msg: answerStructureError
            };
        }
    }

    if (hasOwn(args.faq, "seo")) {
        const seoError = validateSeo(args.faq.seo, "faq", { mode: "update", actionLabel: "faq-update" });
        if (seoError) {
            return {
                status: false,
                msg: seoError
            };
        }
    }

    const body = {
        language: args.language,
        faq: args.faq
    };

    try {
        const backupResponse = await callTradebeeApi(
            "https://platform.tradew.com/openapis/faq/read",
            API_KEY,
            {
                language: args.language,
                faq_id: faqId,
                faqgroup_id: 0,
                fields: [
                    "faq_id",
                    "language",
                    "group",
                    "images",
                    "question",
                    "tags",
                    "summary",
                    "answer",
                    "seo",
                    "update_time"
                ],
                pagination: {
                    current_page: 1,
                    page_size: 10
                }
            }
        );

        const backupSnapshot = extractFirstRecord(backupResponse, ["faq", "faqs", "list", "items", "rows"]);
        if (!backupResponse?.status || !backupSnapshot) {
            return {
                status: false,
                msg: "Backup capture failed before faq-update. Read the current FAQ with the same language and faq_id first, then retry."
            };
        }

        const restorePayload = {
            language: args.language,
            faq: buildRestorePayload(backupSnapshot)
        };

        const backupFile = await saveBackupToFile({
            action: "faq-update",
            language: args.language,
            entityId: faqId,
            rawReadResponse: backupResponse,
            snapshot: backupSnapshot,
            requestedPayload: body,
            restoreAction: "faq-update",
            restorePayload,
            restoreLimitations: [
                "cover_image cannot be auto-restored because the read API does not return original image base64 data."
            ],
            confirmationSummary: args.confirmation.summary
        });

        const result = await callTradebeeApi(
            "https://platform.tradew.com/openapis/faq/update",
            API_KEY,
            body
        );

        if (!isPlainObject(result)) {
            return result;
        }

        return appendPreviewNotice({
            ...result,
            backup: {
                captured: true,
                action: "faq-update",
                language: args.language,
                entity_id: faqId,
                storage: {
                    type: "file",
                    ...backupFile
                },
                snapshot_source: "read_api_response",
                raw_read_response: backupResponse,
                snapshot: backupSnapshot,
                restore_action: "faq-update",
                restore_payload: restorePayload,
                restore_limitations: [
                    "cover_image cannot be auto-restored because the read API does not return original image base64 data."
                ]
            }
        });
    } catch (error) {
        return {
            status: false,
            msg: "Request failed."
        };
    }
}
