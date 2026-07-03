import { appendPreviewNotice, getApiKeyOrError, getHtmlLengthWithoutImages, hasOwn, isPlainObject, validateHtmlWithoutH1, validateImages, validateLanguage, validateSeo, validateTags } from "../validation.js";

export default async function FaqCreate(args = {}) {
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
            msg: "Missing required parameter: confirmation. Before creating an FAQ, require explicit user confirmation that includes the language and FAQ payload."
        };
    }

    if (args.confirmation.approved !== true) {
        return {
            status: false,
            msg: "Explicit user confirmation is required before creating an FAQ. Set confirmation.approved=true only after showing the user the language and FAQ payload to be created."
        };
    }

    if (typeof args.confirmation.summary !== "string" || !args.confirmation.summary.trim()) {
        return {
            status: false,
            msg: "Missing required parameter: confirmation.summary. It must summarize the language and FAQ payload confirmed by the user."
        };
    }

    const languageError = validateLanguage(args.language);
    if (languageError) {
        return {
            status: false,
            msg: languageError
        };
    }

    if (!isPlainObject(args.faq)) {
        return {
            status: false,
            msg: "Missing required parameter: faq."
        };
    }

    const faqGroupId = Number(args.faq.faqgroup_id ?? 0);
    if (!Number.isInteger(faqGroupId) || faqGroupId <= 0) {
        return {
            status: false,
            msg: "Invalid parameter: faq.faqgroup_id. It is required and must be a positive FAQ group ID selected from faqgroup-read."
        };
    }

    if (hasOwn(args.faq, "cover_image")) {
        const imagesError = validateImages(args.faq.cover_image == null ? [] : [args.faq.cover_image], { required: false });
        if (imagesError) {
            return {
                status: false,
                msg: "Invalid parameter: faq.cover_image. If provided, it must be one {name, base64} object with a valid image not larger than 500 kB."
            };
        }
    }

    if (typeof args.faq.question !== "string" || args.faq.question.length < 1 || args.faq.question.length > 100) {
        return {
            status: false,
            msg: "Invalid parameter: faq.question. This field is required and must contain 1 to 100 characters."
        };
    }

    const tagsError = validateTags(args.faq.tags, "faq.tags", {
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
            msg: "Invalid parameter: faq.tags. Provide 1 to 6 unique tags. Each tag must be 3 to 50 characters."
        };
    }

    if (typeof args.faq.summary !== "string" || args.faq.summary.length < 1 || args.faq.summary.length > 500) {
        return {
            status: false,
            msg: "Invalid parameter: faq.summary. This field is required and must contain 1 to 500 characters."
        };
    }

    if (typeof args.faq.answer !== "string" || args.faq.answer.length < 1 || getHtmlLengthWithoutImages(args.faq.answer) > 100000) {
        return {
            status: false,
            msg: "Invalid parameter: faq.answer. This field is required and must contain 1 to 100000 HTML characters after removing <img> tags."
        };
    }

    const answerStructureError = validateHtmlWithoutH1(args.faq.answer, "faq.answer", {
        required: true,
        actionLabel: "faq-create",
        maxImageCount: 50
    });
    if (answerStructureError) {
        return {
            status: false,
            msg: answerStructureError
        };
    }

    if (hasOwn(args.faq, "seo")) {
        const seoError = validateSeo(args.faq.seo, "faq");
        if (seoError) {
            return {
                status: false,
                msg: seoError
            };
        }
    }

    const body = {
        language: args.language,
        faq: args.faq
    };

    try {
        const response = await fetch(
            "https://platform.tradew.com/openapis/faq/create",
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
