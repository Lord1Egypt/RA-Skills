import { getApiKeyOrError, validateFields, validateLanguage, validatePagination } from "../validation.js";

export default async function CustomPageRead(args = {}) {
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

    const custompage_id = Number(args.custompage_id ?? 0);
    if (!Number.isInteger(custompage_id) || custompage_id < 0) {
        return {
            status: false,
            msg: "Invalid parameter: custompage_id. Omit this field to read all custom pages or provide one exact positive custompage_id."
        };
    }

    const fieldsError = validateFields(args.fields, [
        "custompage_id",
        "custompage_url",
        "language",
        "title",
        "content",
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
        custompage_id,
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
            "https://platform.tradew.com/openapis/custompage/read",
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
    } catch {
        return {
            status: false,
            msg: "Request failed."
        };
    }
}
