import { appendPreviewNotice, getApiKeyOrError, getHtmlLengthWithoutImages, hasOwn, isPlainObject, validateHtmlWithoutH1, validateImages, validateLanguage, validateSeo, validateTags } from "../validation.js";

export default async function BlogCreate(args = {}) {
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
            msg: "Missing required parameter: confirmation. Before creating a blog, require explicit user confirmation that includes the language and blog payload."
        };
    }

    if (args.confirmation.approved !== true) {
        return {
            status: false,
            msg: "Explicit user confirmation is required before creating a blog. Set confirmation.approved=true only after showing the user the language and blog payload to be created."
        };
    }

    if (typeof args.confirmation.summary !== "string" || !args.confirmation.summary.trim()) {
        return {
            status: false,
            msg: "Missing required parameter: confirmation.summary. It must summarize the language and blog payload confirmed by the user."
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

    const blogGroupId = Number(args.blog.bloggroup_id ?? 0);
    if (!Number.isInteger(blogGroupId) || blogGroupId <= 0) {
        return {
            status: false,
            msg: "Invalid parameter: blog.bloggroup_id. It is required and must be a positive blog group ID selected from bloggroup-read."
        };
    }

    if (typeof args.blog.publisher !== "undefined"
        && (typeof args.blog.publisher !== "string" || args.blog.publisher.length > 100)) {
        return {
            status: false,
            msg: "Invalid parameter: blog.publisher. If provided, it must contain 1 to 100 characters."
        };
    }

    if (typeof args.blog.title !== "string" || args.blog.title.length < 1 || args.blog.title.length > 500) {
        return {
            status: false,
            msg: "Invalid parameter: blog.title. This field is required and must contain 1 to 500 characters."
        };
    }

    const imagesError = validateImages(args.blog.cover_image == null ? [] : [args.blog.cover_image], { required: true });
    if (imagesError) {
        return {
            status: false,
            msg: "Invalid parameter: blog.cover_image. This field is required and must be one {name, base64} object with a valid image not larger than 500 kB."
        };
    }

    const tagsError = validateTags(args.blog.tags, "blog.tags", {
        required: true,
        minItems: 1,
        maxItems: 6,
        minTagLength: 1,
        maxTagLength: 50
    });
    if (tagsError) {
        return {
            status: false,
            msg: tagsError === "Invalid parameter: blog.tags."
                ? "Invalid parameter: blog.tags. Provide 1 to 6 tags."
                : tagsError
        };
    }

    if (typeof args.blog.summary !== "string" || args.blog.summary.length < 1 || args.blog.summary.length > 500) {
        return {
            status: false,
            msg: "Invalid parameter: blog.summary. This field is required and must contain 1 to 500 characters."
        };
    }

    if (typeof args.blog.description !== "string" || args.blog.description.length < 1 || getHtmlLengthWithoutImages(args.blog.description) > 100000) {
        return {
            status: false,
            msg: "Invalid parameter: blog.description. This field is required and must contain 1 to 100000 HTML characters after removing <img> tags."
        };
    }

    const descriptionStructureError = validateHtmlWithoutH1(args.blog.description, "blog.description", {
        required: true,
        actionLabel: "blog-create",
        maxImageCount: 50
    });
    if (descriptionStructureError) {
        return {
            status: false,
            msg: descriptionStructureError
        };
    }

    if (hasOwn(args.blog, "seo")) {
        const seoError = validateSeo(args.blog.seo, "blog");
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
        const response = await fetch(
            "https://platform.tradew.com/openapis/blog/create",
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
