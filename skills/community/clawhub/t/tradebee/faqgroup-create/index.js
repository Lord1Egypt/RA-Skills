import { appendPreviewNotice, getApiKeyOrError, hasOwn, isPlainObject, validateLanguage, validateSeo } from "../validation.js";

export default async function FaqGroupCreate(args = {}) {
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
            msg: "Missing required parameter: confirmation. Before creating an FAQ group, require explicit user confirmation that includes the language and FAQ group payload."
        };
    }

    if (args.confirmation.approved !== true) {
        return {
            status: false,
            msg: "Explicit user confirmation is required before creating an FAQ group. Set confirmation.approved=true only after showing the user the language and FAQ group payload to be created."
        };
    }

    if (typeof args.confirmation.summary !== "string" || !args.confirmation.summary.trim()) {
        return {
            status: false,
            msg: "Missing required parameter: confirmation.summary. It must summarize the language and FAQ group payload confirmed by the user."
        };
    }

    const languageError = validateLanguage(args.language);
    if (languageError) {
        return {
            status: false,
            msg: languageError
        };
    }

    if (!isPlainObject(args.faqgroup)) {
        return {
            status: false,
            msg: "Missing required parameter: faqgroup."
        };
    }

    if (typeof args.faqgroup.group_name !== "string"
        || args.faqgroup.group_name.length < 1
        || args.faqgroup.group_name.length > 100) {
        return {
            status: false,
            msg: "Invalid parameter: faqgroup.group_name. This field is required and must contain 1 to 100 characters."
        };
    }

    if (typeof args.faqgroup.brief_description !== "undefined"
        && (typeof args.faqgroup.brief_description !== "string" || args.faqgroup.brief_description.length > 300)) {
        return {
            status: false,
            msg: "Invalid parameter: faqgroup.brief_description. If provided, it must contain 0 to 300 characters."
        };
    }

    if (hasOwn(args.faqgroup, "seo")) {
        const seoError = validateSeo(args.faqgroup.seo, "faqgroup");
        if (seoError) {
            return {
                status: false,
                msg: seoError
            };
        }
    }

    const body = {
        language: args.language,
        faqgroup: args.faqgroup
    };

    try {
        const response = await fetch(
            "https://platform.tradew.com/openapis/faqgroup/create",
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
