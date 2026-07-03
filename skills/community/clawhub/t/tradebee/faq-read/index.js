import { getApiKeyOrError, validateFields, validateLanguage, validatePagination } from "../validation.js";

export default async function FaqRead(args = {}) {
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

    const faq_id = Number(args.faq_id ?? 0);
    if (!Number.isInteger(faq_id) || faq_id < 0) {
        return {
            status: false,
            msg: "Invalid parameter: faq_id. Omit this field to read all FAQs or provide one exact positive faq_id."
        };
    }

    const faqgroup_id = Number(args.faqgroup_id ?? 0);
    if (!Number.isInteger(faqgroup_id) || faqgroup_id < 0) {
        return {
            status: false,
            msg: "Invalid parameter: faqgroup_id. Omit this field to read all FAQs or provide one exact positive FAQ group ID selected from faqgroup-read."
        };
    }

    if (faq_id > 0 && faqgroup_id > 0) {
        return {
            status: false,
            msg: "Invalid parameter: faq_id and faqgroup_id cannot be used together. Omit both to read all FAQs, or provide exactly one of them."
        };
    }

    const fieldsError = validateFields(args.fields, [
        "faq_id",
        "language",
        "group",
        "images",
        "question",
        "tags",
        "summary",
        "answer",
        "seo",
        "faq_url",
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
        faq_id,
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
            "https://platform.tradew.com/openapis/faq/read",
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
