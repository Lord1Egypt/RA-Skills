import { appendPreviewNotice, callTradebeeApi, extractFirstRecord, firstPositiveInteger, getApiKeyOrError, getHtmlLengthWithoutImages, hasOwn, isPlainObject, saveBackupToFile, validateHtmlWithoutH1, validateLanguage, validateSeo, withDefinedProperties } from "../validation.js";

function buildRestorePayload(snapshot = {}) {
    return withDefinedProperties(
        {
            custompage_id: firstPositiveInteger(snapshot.custompage_id),
            title: snapshot.title,
            content: snapshot.content,
            seo: snapshot.seo
        },
        [
            "custompage_id",
            "title",
            "content",
            "seo"
        ]
    );
}

export default async function CustomPageUpdate(args = {}) {
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
            msg: "Missing required parameter: confirmation. Before updating a custom page, require explicit user confirmation that includes the language, target custom page ID, and payload."
        };
    }

    if (args.confirmation.approved !== true) {
        return {
            status: false,
            msg: "Explicit user confirmation is required before updating a custom page. Set confirmation.approved=true only after showing the user the language, target custom page ID, and payload to be changed."
        };
    }

    if (typeof args.confirmation.summary !== "string" || !args.confirmation.summary.trim()) {
        return {
            status: false,
            msg: "Missing required parameter: confirmation.summary. It must summarize the language, target custom page ID, and payload confirmed by the user."
        };
    }

    const languageError = validateLanguage(args.language);
    if (languageError) {
        return {
            status: false,
            msg: languageError
        };
    }

    if (!isPlainObject(args.custompage)) {
        return {
            status: false,
            msg: "Missing required parameter: custompage."
        };
    }

    const customPageId = Number(args.custompage.custompage_id ?? 0);
    if (!Number.isInteger(customPageId) || customPageId <= 0) {
        return {
            status: false,
            msg: "Invalid parameter: custompage.custompage_id. The custom page does not exist, does not belong to this account, or does not belong to the selected language. Use custompage-read with the same language to get the correct custompage_id first."
        };
    }

    if (hasOwn(args.custompage, "title")
        && (typeof args.custompage.title !== "string" || args.custompage.title.length > 100)) {
        return {
            status: false,
            msg: "Invalid parameter: custompage.title. If provided for custompage-update, it must contain 1 to 100 characters. Omit this field to keep the current title unchanged."
        };
    }

    if (hasOwn(args.custompage, "content")
        && (typeof args.custompage.content !== "string" || getHtmlLengthWithoutImages(args.custompage.content) > 100000)) {
        return {
            status: false,
            msg: "Invalid parameter: custompage.content. If provided for custompage-update, it must contain 1 to 100000 HTML characters after removing <img> tags. Each <img> may use a normal URL or a supported data:image base64 source. Omit this field to keep the current content unchanged."
        };
    }

    if (hasOwn(args.custompage, "content")) {
        const contentStructureError = validateHtmlWithoutH1(args.custompage.content, "custompage.content", {
            actionLabel: "custompage-update",
            maxImageCount: 50
        });
        if (contentStructureError) {
            return {
                status: false,
                msg: contentStructureError
            };
        }
    }

    if (hasOwn(args.custompage, "seo")) {
        const seoError = validateSeo(args.custompage.seo, "custompage", {
            mode: "update",
            actionLabel: "custompage-update",
            descriptionFieldName: "description"
        });
        if (seoError) {
            return {
                status: false,
                msg: seoError
            };
        }
    }

    const body = {
        language: args.language,
        custompage: args.custompage
    };

    try {
        const backupResponse = await callTradebeeApi(
            "https://platform.tradew.com/openapis/custompage/read",
            API_KEY,
            {
                language: args.language,
                custompage_id: customPageId,
                fields: [
                    "custompage_id",
                    "language",
                    "title",
                    "content",
                    "seo",
                    "update_time"
                ],
                pagination: {
                    current_page: 1,
                    page_size: 10
                }
            }
        );

        const backupSnapshot = extractFirstRecord(backupResponse, ["custompage", "custompages", "list", "items", "rows"]);
        if (!backupResponse?.status || !backupSnapshot) {
            return {
                status: false,
                msg: "Backup capture failed before custompage-update. Read the current custom page with the same language and custompage_id first, then retry."
            };
        }

        const restorePayload = {
            language: args.language,
            custompage: buildRestorePayload(backupSnapshot)
        };

        const backupFile = await saveBackupToFile({
            action: "custompage-update",
            language: args.language,
            entityId: customPageId,
            rawReadResponse: backupResponse,
            snapshot: backupSnapshot,
            requestedPayload: body,
            restoreAction: "custompage-update",
            restorePayload,
            restoreLimitations: [],
            confirmationSummary: args.confirmation.summary
        });

        const result = await callTradebeeApi(
            "https://platform.tradew.com/openapis/custompage/update",
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
                action: "custompage-update",
                language: args.language,
                entity_id: customPageId,
                storage: {
                    type: "file",
                    ...backupFile
                },
                snapshot_source: "read_api_response",
                raw_read_response: backupResponse,
                snapshot: backupSnapshot,
                restore_action: "custompage-update",
                restore_payload: restorePayload,
                restore_limitations: []
            }
        });
    } catch {
        return {
            status: false,
            msg: "Request failed."
        };
    }
}
