import { appendPreviewNotice, getApiKeyOrError, hasOwn, isPlainObject, validateLanguage, validateSeo, validateTags } from "../validation.js";

export default async function BlogGroupCreate(args = {}) {
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
            msg: "Missing required parameter: confirmation. Before creating a blog group, require explicit user confirmation that includes the language and blog group payload."
        };
    }

    if (args.confirmation.approved !== true) {
        return {
            status: false,
            msg: "Explicit user confirmation is required before creating a blog group. Set confirmation.approved=true only after showing the user the language and blog group payload to be created."
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

    if (typeof args.bloggroup.group_name !== "string"
        || args.bloggroup.group_name.length < 1
        || args.bloggroup.group_name.length > 100) {
        return {
            status: false,
            msg: "Invalid parameter: bloggroup.group_name. This field is required and must contain 1 to 100 characters."
        };
    }

    const tagsError = validateTags(args.bloggroup.tags, "bloggroup.tags", {
        required: true,
        minItems: 1,
        maxItems: 6,
        minTagLength: 1,
        maxTagLength: 50
    });
    if (tagsError) {
        return {
            status: false,
            msg: tagsError === "Invalid parameter: bloggroup.tags."
                ? "Invalid parameter: bloggroup.tags. Provide 1 to 6 tags."
                : tagsError
        };
    }

    if (typeof args.bloggroup.brief_description !== "undefined"
        && (typeof args.bloggroup.brief_description !== "string" || args.bloggroup.brief_description.length > 300)) {
        return {
            status: false,
            msg: "Invalid parameter: bloggroup.brief_description. If provided, it must contain 0 to 300 characters."
        };
    }

    if (hasOwn(args.bloggroup, "seo")) {
        const seoError = validateSeo(args.bloggroup.seo, "bloggroup");
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
        const response = await fetch(
            "https://platform.tradew.com/openapis/bloggroup/create",
            {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${API_KEY}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(body)
            }
        );

        if (!response.ok) {
            throw new Error("HTTP ERROR");
        }

        return appendPreviewNotice(await response.json());
    } catch (error) {
        return {
            status: false,
            msg: "Request failed."
        };
    }
}
