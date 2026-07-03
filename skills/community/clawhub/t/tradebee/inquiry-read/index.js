import { getApiKeyOrError, validateFields, validateLanguage, validatePagination } from "../validation.js";

export default async function InquiryRead(args = {}) {
    if (!args || typeof args !== "object" || Array.isArray(args)) {
        return {
            status: false,
            msg: "Invalid parameter: request.body. It must be a valid JSON object."
        };
    }

    const { apiKey: API_KEY, error: apiKeyError } = getApiKeyOrError(args);
    if (apiKeyError) return apiKeyError;

    const languageError = validateLanguage(args.language, { required: false });
    if (languageError) {
        return {
            status: false,
            msg: languageError
        };
    }

    const recent_days = Number(args.recent_days ?? 0);
    if (!Number.isInteger(recent_days) || recent_days < 0 || recent_days > 36500) {
        return {
            status: false,
            msg: "Invalid parameter: recent_days. It must be an integer between 0 and 36500."
        };
    }

    const fieldsError = validateFields(args.fields, [
        "inquiry_id",
        "language",
        "is_read",
        "title",
        "country_code",
        "ip",
        "contact",
        "content",
        "source",
        "target_products",
        "attachment",
        "create_time"
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
        recent_days,
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
            "https://platform.tradew.com/openapis/inquiry/read",
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
