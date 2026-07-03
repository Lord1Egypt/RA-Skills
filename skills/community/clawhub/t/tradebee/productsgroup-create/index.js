import { appendPreviewNotice, getApiKeyOrError, hasOwn, isPlainObject, validateLanguage, validateSection, validateSeo, validateTags } from "../validation.js";

export default async function ProductsGroupCreate(args = {}) {
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
            msg: "Missing required parameter: confirmation. Before creating a product group, require explicit user confirmation that includes the language and product group payload."
        };
    }

    if (args.confirmation.approved !== true) {
        return {
            status: false,
            msg: "Explicit user confirmation is required before creating a product group. Set confirmation.approved=true only after showing the user the language and product group payload to be created."
        };
    }

    if (typeof args.confirmation.summary !== "string" || !args.confirmation.summary.trim()) {
        return {
            status: false,
            msg: "Missing required parameter: confirmation.summary. It must summarize the language and product group payload confirmed by the user."
        };
    }

    const languageError = validateLanguage(args.language);
    if (languageError) {
        return {
            status: false,
            msg: languageError
        };
    }

    if (!isPlainObject(args.productsgroup)) {
        return {
            status: false,
            msg: "Missing required parameter: productsgroup."
        };
    }

    const parentGroupId = Number(args.productsgroup.parent_productsgroup_id ?? 0);
    if (!Number.isInteger(parentGroupId) || parentGroupId < 0) {
        return {
            status: false,
            msg: "Invalid parameter: productsgroup.parent_productsgroup_id. Omit this field or set it to 0 for a top-level group. If provided, it must be a non-negative integer selected from productsgroup-read."
        };
    }

    if (typeof args.productsgroup.group_name !== "string"
        || args.productsgroup.group_name.length < 1
        || args.productsgroup.group_name.length > 200) {
        return {
            status: false,
            msg: "Invalid parameter: productsgroup.group_name. This field is required for productsgroup-create and must contain 1 to 200 characters."
        };
    }

    const tagsError = validateTags(args.productsgroup.tags, "productsgroup.tags", {
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
            msg: "Invalid parameter: productsgroup.tags. For productsgroup-create, provide 1 to 6 unique tags. Each tag must be 3 to 50 characters."
        };
    }

    if (typeof args.productsgroup.brief_description !== "undefined"
        && (typeof args.productsgroup.brief_description !== "string" || args.productsgroup.brief_description.length > 4000)) {
        return {
            status: false,
            msg: "Invalid parameter: productsgroup.brief_description. If provided, it must contain 1 to 4000 plain-text characters."
        };
    }

    if (hasOwn(args.productsgroup, "seo")) {
        const seoError = validateSeo(args.productsgroup.seo, "productsgroup");
        if (seoError) {
            return {
                status: false,
                msg: seoError
            };
        }
    }

    if (hasOwn(args.productsgroup, "section")) {
        const sectionError = validateSection(args.productsgroup.section, "productsgroup.section", {
            maxImageCount: 50
        });
        if (sectionError) {
            return {
                status: false,
                msg: sectionError
            };
        }
    }

    const body = {
        language: args.language,
        productsgroup: args.productsgroup
    };

    try {
        const response = await fetch(
            "https://platform.tradew.com/openapis/productsgroup/create",
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
