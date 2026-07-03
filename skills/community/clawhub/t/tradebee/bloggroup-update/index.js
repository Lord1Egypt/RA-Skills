import { appendPreviewNotice, callTradebeeApi, extractFirstRecord, firstPositiveInteger, getApiKeyOrError, hasOwn, isPlainObject, saveBackupToFile, validateLanguage, validateSeo, validateTags, withDefinedProperties } from "../validation.js";

function buildRestorePayload(snapshot = {}) {
    return withDefinedProperties(
        {
            bloggroup_id: firstPositiveInteger(snapshot.bloggroup_id),
            group_name: snapshot.group_name,
            tags: snapshot.tags,
            brief_description: snapshot.brief_description,
            seo: snapshot.seo
        },
        [
            "bloggroup_id",
            "group_name",
            "tags",
            "brief_description",
            "seo"
        ]
    );
}

export default async function BlogGroupUpdate(args = {}) {
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
            msg: "Missing required parameter: confirmation. Before updating a blog group, require explicit user confirmation that includes the language and blog group payload."
        };
    }

    if (args.confirmation.approved !== true) {
        return {
            status: false,
            msg: "Explicit user confirmation is required before updating a blog group. Set confirmation.approved=true only after showing the user the language and blog group payload to be updated."
        };
    }

    if (typeof args.confirmation.summary !== "string" || !args.confirmation.summary.trim()) {
        return {
            status: false,
            msg: "Missing required parameter: confirmation.summary. It must summarize the language and blog group payload confirmed by the user."
        };
    }

    const languageError = validateLanguage(args.language);
    if (languageError) {
        return {
            status: false,
            msg: languageError
        };
    }

    if (!isPlainObject(args.bloggroup)) {
        return {
            status: false,
            msg: "Missing required parameter: bloggroup."
        };
    }

    const blogGroupId = Number(args.bloggroup.bloggroup_id ?? 0);
    if (!Number.isInteger(blogGroupId) || blogGroupId <= 0) {
        return {
            status: false,
            msg: "Invalid parameter: bloggroup.bloggroup_id. It is required and must be a positive blog group ID selected from bloggroup-read."
        };
    }

    if (hasOwn(args.bloggroup, "group_name")
        && (typeof args.bloggroup.group_name !== "string" || args.bloggroup.group_name.length > 100)) {
        return {
            status: false,
            msg: "Invalid parameter: bloggroup.group_name. If provided, it must contain 1 to 100 characters."
        };
    }

    if (hasOwn(args.bloggroup, "tags")) {
        const tagsError = validateTags(args.bloggroup.tags, "bloggroup.tags", {
            required: false,
            minItems: 0,
            maxItems: 6,
            minTagLength: 1,
            maxTagLength: 50
        });
        if (tagsError) {
            return {
                status: false,
                msg: "Invalid parameter: bloggroup.tags. If provided, supply 0 to 6 tags."
            };
        }
    }

    if (hasOwn(args.bloggroup, "brief_description")
        && (typeof args.bloggroup.brief_description !== "string" || args.bloggroup.brief_description.length > 300)) {
        return {
            status: false,
            msg: "Invalid parameter: bloggroup.brief_description. If provided, it must contain 1 to 300 characters."
        };
    }

    if (hasOwn(args.bloggroup, "seo")) {
        const seoError = validateSeo(args.bloggroup.seo, "bloggroup", { mode: "update", actionLabel: "bloggroup-update" });
        if (seoError) {
            return {
                status: false,
                msg: seoError
            };
        }
    }

    const body = {
        language: args.language,
        bloggroup: args.bloggroup
    };

    try {
        const backupResponse = await callTradebeeApi(
            "https://platform.tradew.com/openapis/bloggroup/read",
            API_KEY,
            {
                language: args.language,
                bloggroup_id: blogGroupId,
                fields: [
                    "bloggroup_id",
                    "language",
                    "group_name",
                    "tags",
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

        const backupSnapshot = extractFirstRecord(backupResponse, ["bloggroup", "bloggroups", "list", "items", "rows"]);
        if (!backupResponse?.status || !backupSnapshot) {
            return {
                status: false,
                msg: "Backup capture failed before bloggroup-update. Read the current blog group with the same language and bloggroup_id first, then retry."
            };
        }

        const restorePayload = {
            language: args.language,
            bloggroup: buildRestorePayload(backupSnapshot)
        };

        const backupFile = await saveBackupToFile({
            action: "bloggroup-update",
            language: args.language,
            entityId: blogGroupId,
            rawReadResponse: backupResponse,
            snapshot: backupSnapshot,
            requestedPayload: body,
            restoreAction: "bloggroup-update",
            restorePayload,
            restoreLimitations: [],
            confirmationSummary: args.confirmation.summary
        });

        const result = await callTradebeeApi(
            "https://platform.tradew.com/openapis/bloggroup/update",
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
                action: "bloggroup-update",
                language: args.language,
                entity_id: blogGroupId,
                storage: {
                    type: "file",
                    ...backupFile
                },
                snapshot_source: "read_api_response",
                raw_read_response: backupResponse,
                snapshot: backupSnapshot,
                restore_action: "bloggroup-update",
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
