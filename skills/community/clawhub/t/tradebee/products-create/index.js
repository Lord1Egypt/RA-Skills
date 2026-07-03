import { appendPreviewNotice, getApiKeyOrError, getHtmlLengthWithoutImages, hasOwn, isPlainObject, validateAttributes, validateHtmlWithoutH1, validateImages, validateLanguage, validateSeo, validateTags } from "../validation.js";

export default async function ProductsCreate(args = {}) {
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
            msg: "Missing required parameter: confirmation. Before creating a product, require explicit user confirmation that includes the language and product payload."
        };
    }

    if (args.confirmation.approved !== true) {
        return {
            status: false,
            msg: "Explicit user confirmation is required before creating a product. Set confirmation.approved=true only after showing the user the language and product payload to be created."
        };
    }

    if (typeof args.confirmation.summary !== "string" || !args.confirmation.summary.trim()) {
        return {
            status: false,
            msg: "Missing required parameter: confirmation.summary. It must summarize the language and product payload confirmed by the user."
        };
    }

    const languageError = validateLanguage(args.language);
    if (languageError) {
        return {
            status: false,
            msg: languageError
        };
    }

    if (!isPlainObject(args.products)) {
        return {
            status: false,
            msg: "Missing required parameter: products."
        };
    }

    const productGroupId = Number(args.products.productsgroup_id ?? 0);
    if (!Number.isInteger(productGroupId) || productGroupId <= 0) {
        return {
            status: false,
            msg: "Invalid parameter: products.productsgroup_id. It is required and must be a positive leaf group ID selected from productsgroup-read where is_leaf=true. Parent group IDs and 0 are not allowed."
        };
    }

    if (typeof args.products.product_name !== "string" || args.products.product_name.length < 1 || args.products.product_name.length > 300) {
        return {
            status: false,
            msg: "Invalid parameter: products.product_name. This field is required for products-create and must contain 1 to 300 characters."
        };
    }

    if (typeof args.products.model !== "undefined"
        && (typeof args.products.model !== "string" || args.products.model.length > 50)) {
        return {
            status: false,
            msg: "Invalid parameter: products.model. If provided, it must be 50 characters or fewer."
        };
    }

    const imagesError = validateImages(args.products.upload_images, { required: true });
    if (imagesError) {
        return {
            status: false,
            msg: imagesError
        };
    }

    const attributesError = validateAttributes(args.products.attributes);
    if (attributesError) {
        return {
            status: false,
            msg: attributesError
        };
    }

    const tagsError = validateTags(args.products.tags, "products.tags", {
        required: true,
        minItems: 1,
        maxItems: 6,
        minTagLength: 3,
        maxTagLength: 50,
        unique: true
    });
    if (tagsError) {
        return {
            status: false,
            msg: "Invalid parameter: products.tags. For products-create, provide 1 to 6 unique tags. Each tag must be 3 to 50 characters."
        };
    }

    if (typeof args.products.brief_description !== "string"
        || args.products.brief_description.length < 1
        || args.products.brief_description.length > 127) {
        return {
            status: false,
            msg: "Invalid parameter: products.brief_description. This field is required for products-create and must contain 1 to 127 plain-text characters."
        };
    }

    if (typeof args.products.description !== "string"
        || args.products.description.length < 1
        || getHtmlLengthWithoutImages(args.products.description) > 100000) {
        return {
            status: false,
            msg: "Invalid parameter: products.description. This field is required for products-create and must contain 1 to 100000 HTML characters after removing <img> tags."
        };
    }

    const descriptionStructureError = validateHtmlWithoutH1(args.products.description, "products.description", {
        required: true,
        actionLabel: "products-create",
        maxImageCount: 50
    });
    if (descriptionStructureError) {
        return {
            status: false,
            msg: descriptionStructureError
        };
    }

    if (hasOwn(args.products, "seo")) {
        const seoError = validateSeo(args.products.seo, "products");
        if (seoError) {
            return {
                status: false,
                msg: seoError
            };
        }
    }

    const body = {
        language: args.language,
        products: args.products
    };

    try {
        const response = await fetch(
            "https://platform.tradew.com/openapis/products/create",
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
