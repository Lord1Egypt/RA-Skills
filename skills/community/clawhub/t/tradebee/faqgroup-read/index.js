import { getApiKeyOrError, validateFields, validateLanguage, validatePagination } from "../validation.js";

export default async function FaqGroupRead(args = {}) {
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

    const faqgroup_id = Number(args.faqgroup_id ?? 0);
    if (!Number.isInteger(faqgroup_id) || faqgroup_id < 0) {
        return {
            status: false,
            msg: "Invalid parameter: faqgroup_id. Omit this field to read all FAQ groups or provide one exact positive faqgroup_id."
        };
    }

    const fieldsError = validateFields(args.fields, [
        "faqgroup_id",
        "language",
        "group_name",
        "brief_description",
        "seo",
        "faqgroup_url",
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
        faqgroup_id,
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
            "https://platform.tradew.com/openapis/faqgroup/read",
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
