import { appendPreviewNotice, callTradebeeApi, extractFirstRecord, firstPositiveInteger, getApiKeyOrError, hasOwn, isPlainObject, saveBackupToFile, validateLanguage, validateSection, validateSeo, validateTags, withDefinedProperties } from "../validation.js";

function buildRestorePayload(snapshot = {}) {
    return withDefinedProperties(
        {
            productsgroup_id: firstPositiveInteger(snapshot.productsgroup_id),
            group_name: snapshot.group_name,
            tags: snapshot.tags,
            brief_description: snapshot.brief_description,
            seo: snapshot.seo,
            section: snapshot.section
        },
        [
            "productsgroup_id",
            "group_name",
            "tags",
            "brief_description",
            "seo",
            "section"
        ]
    );
}

export default async function ProductsGroupUpdate(args = {}) {
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
            msg: "Missing required parameter: confirmation. Before updating a product group, require explicit user confirmation that includes the language and product group payload."
        };
    }

    if (args.confirmation.approved !== true) {
        return {
            status: false,
            msg: "Explicit user confirmation is required before updating a product group. Set confirmation.approved=true only after showing the user the language and product group payload to be updated."
        };
    }

    if (typeof args.confirmation.summary !== "string" || !args.confirmation.summary.trim()) {
        return {
            status: false,
            msg: "Missing required parameter: confirmation.summary. It must summarize the language and product group payload confirmed by the user."
        };
    }

    const languageError = validateLanguage(args.language);
    if (languageError) {
        return {
            status: false,
            msg: languageError
        };
    }

    if (!isPlainObject(args.productsgroup)) {
        return {
            status: false,
            msg: "Missing required parameter: productsgroup."
        };
    }

    const productGroupId = Number(args.productsgroup.productsgroup_id ?? 0);
    if (!Number.isInteger(productGroupId) || productGroupId <= 0) {
        return {
            status: false,
            msg: "Invalid parameter: productsgroup.productsgroup_id. It is required and must be a positive product group ID selected from productsgroup-read."
        };
    }

    if (hasOwn(args.productsgroup, "group_name")
        && (typeof args.productsgroup.group_name !== "string" || args.productsgroup.group_name.length > 200)) {
        return {
            status: false,
            msg: "Invalid parameter: productsgroup.group_name. If provided, it must contain 1 to 200 characters."
        };
    }

    if (hasOwn(args.productsgroup, "tags")) {
        const tagsError = validateTags(args.productsgroup.tags, "productsgroup.tags", {
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
                msg: "Invalid parameter: productsgroup.tags. If provided, supply 0 to 6 tags."
            };
        }
    }

    if (hasOwn(args.productsgroup, "brief_description")
        && (typeof args.productsgroup.brief_description !== "string" || args.productsgroup.brief_description.length > 4000)) {
        return {
            status: false,
            msg: "Invalid parameter: productsgroup.brief_description. If provided, it must contain 1 to 4,000 characters."
        };
    }

    if (hasOwn(args.productsgroup, "seo")) {
        const seoError = validateSeo(args.productsgroup.seo, "productsgroup", {
            mode: "update",
            actionLabel: "productsgroup-update"
        });
        if (seoError) {
            return {
                status: false,
                msg: seoError
            };
        }
    }

    if (hasOwn(args.productsgroup, "section")) {
        const sectionError = validateSection(args.productsgroup.section, "productsgroup.section", {
            mode: "update",
            actionLabel: "productsgroup-update",
            maxImageCount: 50
        });
        if (sectionError) {
            return {
                status: false,
                msg: sectionError
            };
        }
    }

    const body = {
        language: args.language,
        productsgroup: args.productsgroup
    };

    try {
        const backupResponse = await callTradebeeApi(
            "https://platform.tradew.com/openapis/productsgroup/read",
            API_KEY,
            {
                language: args.language,
                parent_productsgroup_id: 0,
                productsgroup_id: productGroupId,
                fields: [
                    "productsgroup_id",
                    "language",
                    "group_name",
                    "tags",
                    "brief_description",
                    "seo",
                    "section",
                    "update_time"
                ]
            }
        );

        const backupSnapshot = extractFirstRecord(backupResponse, ["productsgroup", "productsgroups", "list", "items", "rows"]);
        if (!backupResponse?.status || !backupSnapshot) {
            return {
                status: false,
                msg: "Backup capture failed before productsgroup-update. Read the current product group with the same language and productsgroup_id first, then retry."
            };
        }

        const restorePayload = {
            language: args.language,
            productsgroup: buildRestorePayload(backupSnapshot)
        };

        const backupFile = await saveBackupToFile({
            action: "productsgroup-update",
            language: args.language,
            entityId: productGroupId,
            rawReadResponse: backupResponse,
            snapshot: backupSnapshot,
            requestedPayload: body,
            restoreAction: "productsgroup-update",
            restorePayload,
            restoreLimitations: [],
            confirmationSummary: args.confirmation.summary
        });

        const result = await callTradebeeApi(
            "https://platform.tradew.com/openapis/productsgroup/update",
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
                action: "productsgroup-update",
                language: args.language,
                entity_id: productGroupId,
                storage: {
                    type: "file",
                    ...backupFile
                },
                snapshot_source: "read_api_response",
                raw_read_response: backupResponse,
                snapshot: backupSnapshot,
                restore_action: "productsgroup-update",
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
