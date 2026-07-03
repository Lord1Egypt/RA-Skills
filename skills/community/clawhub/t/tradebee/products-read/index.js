import { getApiKeyOrError, validateFields, validateLanguage, validatePagination } from "../validation.js";

export default async function ProductsRead(args = {}) {
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

    const products_id = Number(args.products_id ?? 0);
    if (!Number.isInteger(products_id) || products_id < 0) {
        return {
            status: false,
            msg: "Invalid parameter: products_id. Omit this field to read all products or provide one exact positive products_id."
        };
    }

    const productsgroup_id = Number(args.productsgroup_id ?? 0);
    if (!Number.isInteger(productsgroup_id) || productsgroup_id < 0) {
        return {
            status: false,
            msg: "Invalid parameter: productsgroup_id. Omit this field to read all products or provide one exact positive leaf group ID selected from productsgroup-read where is_leaf=true."
        };
    }

    if (products_id > 0 && productsgroup_id > 0) {
        return {
            status: false,
            msg: "Invalid parameter: products_id and productsgroup_id cannot be used together. Omit both to read all products, or provide exactly one of them."
        };
    }

    const fieldsError = validateFields(args.fields, [
        "products_id",
        "language",
        "group",
        "product_name",
        "model",
        "images",
        "tags",
        "attributes",
        "brief_description",
        "description",
        "seo",
        "view_count",
        "inquiry_count",
        "products_url",
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
        products_id,
        productsgroup_id,
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
            "https://platform.tradew.com/openapis/products/read",
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
