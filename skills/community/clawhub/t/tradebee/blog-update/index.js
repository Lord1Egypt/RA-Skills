import { appendPreviewNotice, callTradebeeApi, extractFirstRecord, firstPositiveInteger, getApiKeyOrError, getHtmlLengthWithoutImages, hasOwn, isPlainObject, saveBackupToFile, validateHtmlWithoutH1, validateImages, validateLanguage, validateSeo, validateTags, withDefinedProperties } from "../validation.js";

function buildRestorePayload(snapshot = {}) {
    return withDefinedProperties(
        {
            blog_id: firstPositiveInteger(snapshot.blog_id),
            bloggroup_id: firstPositiveInteger(snapshot.bloggroup_id, snapshot.group?.bloggroup_id, snapshot.group?.id),
            publisher: snapshot.publisher,
            publication_date: snapshot.publication_date,
            title: snapshot.title,
            tags: snapshot.tags,
            summary: snapshot.summary,
            description: snapshot.description,
            seo: snapshot.seo
        },
        [
            "blog_id",
            "bloggroup_id",
            "publisher",
            "publication_date",
            "title",
            "tags",
            "summary",
            "description",
            "seo"
        ]
    );
}

export default async function BlogUpdate(args = {}) {
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
            msg: "Missing required parameter: confirmation. Before updating a blog, require explicit user confirmation that includes the language, target blog ID, and payload."
        };
    }

    if (args.confirmation.approved !== true) {
        return {
            status: false,
            msg: "Explicit user confirmation is required before updating a blog. Set confirmation.approved=true only after showing the user the language, target blog ID, and payload to be changed."
        };
    }

    if (typeof args.confirmation.summary !== "string" || !args.confirmation.summary.trim()) {
        return {
            status: false,
            msg: "Missing required parameter: confirmation.summary. It must summarize the language, target blog ID, and payload confirmed by the user."
        };
    }

    const languageError = validateLanguage(args.language);
    if (languageError) {
        return {
            status: false,
            msg: languageError
        };
    }

    if (!isPlainObject(args.blog)) {
        return {
            status: false,
            msg: "Missing required parameter: blog."
        };
    }

    const blogId = Number(args.blog.blog_id ?? 0);
    if (!Number.isInteger(blogId) || blogId <= 0) {
        return {
            status: false,
            msg: "Invalid parameter: blog.blog_id. The blog does not exist, does not belong to this account, or does not belong to the selected language. Use blog-read with the same language to get the correct blog_id first."
        };
    }

    if (hasOwn(args.blog, "bloggroup_id")) {
        const blogGroupId = Number(args.blog.bloggroup_id);
        if (!Number.isInteger(blogGroupId) || blogGroupId <= 0) {
            return {
                status: false,
                msg: "Invalid parameter: blog.bloggroup_id. Omit this field to keep the current group unchanged. If provided, it must be a positive blog group ID selected from bloggroup-read."
            };
        }
    }

    if (hasOwn(args.blog, "publisher")
        && (typeof args.blog.publisher !== "string" || args.blog.publisher.length > 100)) {
        return {
            status: false,
            msg: "Invalid parameter: blog.publisher. If provided for blog-update, it must contain 1 to 100 characters. Omit this field to keep the current publisher unchanged."
        };
    }

    if (hasOwn(args.blog, "publication_date")
        && (typeof args.blog.publication_date !== "string" || !args.blog.publication_date.trim())) {
        return {
            status: false,
            msg: "Invalid parameter: blog.publication_date. If provided for blog-update, it must be a non-empty date string in yyyy/M/d format. Omit this field to keep the current publication date unchanged."
        };
    }

    if (hasOwn(args.blog, "title")
        && (typeof args.blog.title !== "string" || args.blog.title.length > 500)) {
        return {
            status: false,
            msg: "Invalid parameter: blog.title. If provided for blog-update, it must contain 1 to 500 characters. Omit this field to keep the current title unchanged."
        };
    }

    if (hasOwn(args.blog, "cover_image")) {
        const imagesError = validateImages(args.blog.cover_image == null ? [] : [args.blog.cover_image], { required: false });
        if (imagesError) {
            return {
                status: false,
                msg: "Invalid parameter: blog.cover_image. If provided, it must be one {name, base64} object with a valid image not larger than 500 kB."
            };
        }
    }

    if (hasOwn(args.blog, "tags")) {
        const tagsError = validateTags(args.blog.tags, "blog.tags", {
            required: false,
            minItems: 0,
            maxItems: 6,
            minTagLength: 3,
            maxTagLength: 50
        });
        if (tagsError) {
            return {
                status: false,
                msg: "Invalid parameter: blog.tags. If provided, supply 0 to 6 tags. Each tag must be 3 to 50 characters."
            };
        }
    }

    if (hasOwn(args.blog, "summary")
        && (typeof args.blog.summary !== "string" || args.blog.summary.length > 500)) {
        return {
            status: false,
            msg: "Invalid parameter: blog.summary. If provided for blog-update, it must contain 1 to 500 characters. Omit this field to keep the current summary unchanged."
        };
    }

    if (hasOwn(args.blog, "description")
        && (typeof args.blog.description !== "string" || getHtmlLengthWithoutImages(args.blog.description) > 100000)) {
        return {
            status: false,
            msg: "Invalid parameter: blog.description. If provided for blog-update, it must contain 1 to 100000 HTML characters after removing <img> tags. Omit this field to keep the current description unchanged."
        };
    }

    if (hasOwn(args.blog, "description")) {
        const descriptionStructureError = validateHtmlWithoutH1(args.blog.description, "blog.description", {
            actionLabel: "blog-update",
            maxImageCount: 50
        });
        if (descriptionStructureError) {
            return {
                status: false,
                msg: descriptionStructureError
            };
        }
    }

    if (hasOwn(args.blog, "seo")) {
        const seoError = validateSeo(args.blog.seo, "blog", { mode: "update", actionLabel: "blog-update" });
        if (seoError) {
            return {
                status: false,
                msg: seoError
            };
        }
    }

    const body = {
        language: args.language,
        blog: args.blog
    };

    try {
        const backupResponse = await callTradebeeApi(
            "https://platform.tradew.com/openapis/blog/read",
            API_KEY,
            {
                language: args.language,
                blog_id: blogId,
                bloggroup_id: 0,
                fields: [
                    "blog_id",
                    "group",
                    "language",
                    "publisher",
                    "publication_date",
                    "title",
                    "images",
                    "tags",
                    "summary",
                    "description",
                    "seo",
                    "update_time"
                ],
                pagination: {
                    current_page: 1,
                    page_size: 10
                }
            }
        );

        const backupSnapshot = extractFirstRecord(backupResponse, ["blog", "blogs", "list", "items", "rows"]);
        if (!backupResponse?.status || !backupSnapshot) {
            return {
                status: false,
                msg: "Backup capture failed before blog-update. Read the current blog with the same language and blog_id first, then retry."
            };
        }

        const restorePayload = {
            language: args.language,
            blog: buildRestorePayload(backupSnapshot)
        };

        const backupFile = await saveBackupToFile({
            action: "blog-update",
            language: args.language,
            entityId: blogId,
            rawReadResponse: backupResponse,
            snapshot: backupSnapshot,
            requestedPayload: body,
            restoreAction: "blog-update",
            restorePayload,
            restoreLimitations: [
                "cover_image cannot be auto-restored because the read API does not return original image base64 data."
            ],
            confirmationSummary: args.confirmation.summary
        });

        const result = await callTradebeeApi(
            "https://platform.tradew.com/openapis/blog/update",
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
                action: "blog-update",
                language: args.language,
                entity_id: blogId,
                storage: {
                    type: "file",
                    ...backupFile
                },
                snapshot_source: "read_api_response",
                raw_read_response: backupResponse,
                snapshot: backupSnapshot,
                restore_action: "blog-update",
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
