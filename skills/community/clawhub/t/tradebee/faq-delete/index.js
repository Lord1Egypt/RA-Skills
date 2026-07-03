import { getApiKeyOrError, validateIdList, validateLanguage } from "../validation.js";

export default async function FaqDelete(args = {}) {
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
            msg: "Missing required parameter: confirmation. Before deleting FAQs, require explicit user confirmation that includes the language and FAQ IDs to be moved to the recycle bin."
        };
    }

    if (args.confirmation.approved !== true) {
        return {
            status: false,
            msg: "Explicit user confirmation is required before deleting FAQs. Set confirmation.approved=true only after showing the user the language and FAQ IDs to be moved to the recycle bin."
        };
    }

    if (typeof args.confirmation.summary !== "string" || !args.confirmation.summary.trim()) {
        return {
            status: false,
            msg: "Missing required parameter: confirmation.summary. It must summarize the language and FAQ IDs confirmed by the user."
        };
    }

    const languageError = validateLanguage(args.language);
    if (languageError) {
        return {
            status: false,
            msg: languageError
        };
    }

    const idListError = validateIdList(args.id_list);
    if (idListError) {
        return {
            status: false,
            msg: idListError
        };
    }

    const body = {
        language: args.language,
        id_list: args.id_list
    };

    try {
        const response = await fetch(
            "https://platform.tradew.com/openapis/faq/delete",
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
