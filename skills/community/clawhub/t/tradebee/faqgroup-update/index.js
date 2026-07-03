import { appendPreviewNotice, callTradebeeApi, extractFirstRecord, firstPositiveInteger, getApiKeyOrError, hasOwn, isPlainObject, saveBackupToFile, validateLanguage, validateSeo, withDefinedProperties } from "../validation.js";

function buildRestorePayload(snapshot = {}) {
    return withDefinedProperties(
        {
            faqgroup_id: firstPositiveInteger(snapshot.faqgroup_id),
            group_name: snapshot.group_name,
            brief_description: snapshot.brief_description,
            seo: snapshot.seo
        },
        [
            "faqgroup_id",
            "group_name",
            "brief_description",
            "seo"
        ]
    );
}

export default async function FaqGroupUpdate(args = {}) {
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
            msg: "Missing required parameter: confirmation. Before updating an FAQ group, require explicit user confirmation that includes the language and FAQ group payload."
        };
    }

    if (args.confirmation.approved !== true) {
        return {
            status: false,
            msg: "Explicit user confirmation is required before updating an FAQ group. Set confirmation.approved=true only after showing the user the language and FAQ group payload to be updated."
        };
    }

    if (typeof args.confirmation.summary !== "string" || !args.confirmation.summary.trim()) {
        return {
            status: false,
            msg: "Missing required parameter: confirmation.summary. It must summarize the language and FAQ group payload confirmed by the user."
        };
    }

    const languageError = validateLanguage(args.language);
    if (languageError) {
        return {
            status: false,
            msg: languageError
        };
    }

    if (!isPlainObject(args.faqgroup)) {
        return {
            status: false,
            msg: "Missing required parameter: faqgroup."
        };
    }

    const faqGroupId = Number(args.faqgroup.faqgroup_id ?? 0);
    if (!Number.isInteger(faqGroupId) || faqGroupId <= 0) {
        return {
            status: false,
            msg: "Invalid parameter: faqgroup.faqgroup_id. It is required and must be a positive FAQ group ID selected from faqgroup-read."
        };
    }

    if (hasOwn(args.faqgroup, "group_name")
        && (typeof args.faqgroup.group_name !== "string" || args.faqgroup.group_name.length > 100)) {
        return {
            status: false,
            msg: "Invalid parameter: faqgroup.group_name. If provided, it must contain 1 to 100 characters."
        };
    }

    if (hasOwn(args.faqgroup, "brief_description")
        && (typeof args.faqgroup.brief_description !== "string" || args.faqgroup.brief_description.length > 300)) {
        return {
            status: false,
            msg: "Invalid parameter: faqgroup.brief_description. If provided, it must contain 1 to 300 characters."
        };
    }

    if (hasOwn(args.faqgroup, "seo")) {
        const seoError = validateSeo(args.faqgroup.seo, "faqgroup", { mode: "update", actionLabel: "faqgroup-update" });
        if (seoError) {
            return {
                status: false,
                msg: seoError
            };
        }
    }

    const body = {
        language: args.language,
        faqgroup: args.faqgroup
    };

    try {
        const backupResponse = await callTradebeeApi(
            "https://platform.tradew.com/openapis/faqgroup/read",
            API_KEY,
            {
                language: args.language,
                faqgroup_id: faqGroupId,
                fields: [
                    "faqgroup_id",
                    "language",
                    "group_name",
                    "brief_description",
                    "seo",
                    "update_time"
                ],
                pagination: {
                    current_page: 1,
                    page_size: 10
                }
            }
        );

        const backupSnapshot = extractFirstRecord(backupResponse, ["faqgroup", "faqgroups", "list", "items", "rows"]);
        if (!backupResponse?.status || !backupSnapshot) {
            return {
                status: false,
                msg: "Backup capture failed before faqgroup-update. Read the current FAQ group with the same language and faqgroup_id first, then retry."
            };
        }

        const restorePayload = {
            language: args.language,
            faqgroup: buildRestorePayload(backupSnapshot)
        };

        const backupFile = await saveBackupToFile({
            action: "faqgroup-update",
            language: args.language,
            entityId: faqGroupId,
            rawReadResponse: backupResponse,
            snapshot: backupSnapshot,
            requestedPayload: body,
            restoreAction: "faqgroup-update",
            restorePayload,
            restoreLimitations: [],
            confirmationSummary: args.confirmation.summary
        });

        const result = await callTradebeeApi(
            "https://platform.tradew.com/openapis/faqgroup/update",
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
                action: "faqgroup-update",
                language: args.language,
                entity_id: faqGroupId,
                storage: {
                    type: "file",
                    ...backupFile
                },
                snapshot_source: "read_api_response",
                raw_read_response: backupResponse,
                snapshot: backupSnapshot,
                restore_action: "faqgroup-update",
                restore_payload: restorePayload,
                restore_limitations: []
            }
        });
    } catch (error) {
        return {
            status: false,
            msg: "Request failed."
        };
    }
}
