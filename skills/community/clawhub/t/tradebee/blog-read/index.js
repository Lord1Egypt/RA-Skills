import { getApiKeyOrError, validateFields, validateLanguage, validatePagination } from "../validation.js";

export default async function BlogRead(args = {}) {
    if (!args || typeof args !== "object" || Array.isArray(args)) {
        return {
            status: false,
            msg: "Invalid parameter: request.body. It must be a valid JSON object."
        };
    }

    const { apiKey: API_KEY, error: apiKeyError } = getApiKeyOrError(args);
    if (apiKeyError) return apiKeyError;

    const languageError = validateLanguage(args.language);
    if (languageError) {
        return {
            status: false,
            msg: languageError
        };
    }

    const blog_id = Number(args.blog_id ?? 0);
    if (!Number.isInteger(blog_id) || blog_id < 0) {
        return {
            status: false,
            msg: "Invalid parameter: blog_id. Omit this field to read all blogs or provide one exact positive blog_id."
        };
    }

    const bloggroup_id = Number(args.bloggroup_id ?? 0);
    if (!Number.isInteger(bloggroup_id) || bloggroup_id < 0) {
        return {
            status: false,
            msg: "Invalid parameter: bloggroup_id. Omit this field to read all blogs or provide one exact positive blog group ID selected from bloggroup-read."
        };
    }

    if (blog_id > 0 && bloggroup_id > 0) {
        return {
            status: false,
            msg: "Invalid parameter: blog_id and bloggroup_id cannot be used together. Omit both to read all blogs, or provide exactly one of them."
        };
    }

    const fieldsError = validateFields(args.fields, [
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
        "create_time",
        "update_time"
    ]);
    if (fieldsError) {
        return {
            status: false,
            msg: fieldsError
        };
    }

    const pagination = validatePagination(args);
    if (pagination.error) {
        return {
            status: false,
            msg: pagination.error
        };
    }
    const { current_page, page_size } = pagination;

    const body = {
        language: args.language,
        blog_id,
        bloggroup_id,
        fields: Array.isArray(args.fields) && args.fields.length
            ? args.fields
            : [],
        pagination: {
            current_page,
            page_size
        }
    };

    try {
        const response = await fetch(
            "https://platform.tradew.com/openapis/blog/read",
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

        return await response.json();
    } catch (error) {
        return {
            status: false,
            msg: "Request failed."
        };
    }
}
