import { getApiKeyOrError, validateFields, validateLanguage } from "../validation.js";

export default async function ProductsGroupRead(args = {}) {
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

    const parent_productsgroup_id = Number(args.parent_productsgroup_id ?? 0);
    if (!Number.isInteger(parent_productsgroup_id) || parent_productsgroup_id < 0) {
        return {
            status: false,
            msg: "Invalid parameter: parent_productsgroup_id. Omit this field or set it to 0 to read top-level groups. If provided, it must be a non-negative product group ID."
        };
    }

    const productsgroup_id = Number(args.productsgroup_id ?? 0);
    if (!Number.isInteger(productsgroup_id) || productsgroup_id < 0) {
        return {
            status: false,
            msg: "Invalid parameter: productsgroup_id. Omit this field to avoid exact-group filtering or provide one exact positive productsgroup_id."
        };
    }

    if (parent_productsgroup_id > 0 && productsgroup_id > 0) {
        return {
            status: false,
            msg: "Invalid parameter: parent_productsgroup_id and productsgroup_id cannot be used together. Omit both to read top-level groups, or provide exactly one of them."
        };
    }

    const fieldsError = validateFields(args.fields, [
        "productsgroup_id",
        "language",
        "group_name",
        "tags",
        "seo",
        "section",
        "productsgroup_url",
        "create_time",
        "update_time"
    ]);
    if (fieldsError) {
        return {
            status: false,
            msg: fieldsError
        };
    }

    const body = {
        language: args.language,
        parent_productsgroup_id,
        productsgroup_id,
        fields: Array.isArray(args.fields) && args.fields.length
            ? args.fields
            : []
    };

    try {
        const response = await fetch(
            "https://platform.tradew.com/openapis/productsgroup/read",
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
