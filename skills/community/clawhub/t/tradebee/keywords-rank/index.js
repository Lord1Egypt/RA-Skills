import { getApiKeyOrError, validatePagination } from "../validation.js";

export default async function KeywordsRank(args = {}) {
    if (!args || typeof args !== "object" || Array.isArray(args)) {
        return {
            status: false,
            msg: "Invalid parameter: request.body. It must be a valid JSON object."
        };
    }

    const { apiKey: API_KEY, error: apiKeyError } = getApiKeyOrError(args);
    if (apiKeyError) return apiKeyError;

    const keywords = typeof args.keywords === "string" ? args.keywords.trim() : "";
    if (args.keywords != null && (!keywords || typeof args.keywords !== "string")) {
        return {
            status: false,
            msg: "Invalid parameter: keywords. Omit this field to read all keyword ranking records or provide one exact non-empty keyword string."
        };
    }

    const hasRank = args.rank != null;
    const rank = hasRank ? Number(args.rank) : null;
    if (hasRank && (!Number.isInteger(rank) || rank < 1 || rank >= 1000)) {
        return {
            status: false,
            msg: "Invalid parameter: rank. Omit this field to read all keyword ranking records, or provide one integer from 1 to 999 to read keywords ranked within the top N positions."
        };
    }

    if (keywords && hasRank) {
        return {
            status: false,
            msg: "Invalid parameter: keywords and rank cannot be used together. Omit both to read all keyword ranking records, or provide exactly one of them."
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
        keywords,
        rank,
        pagination: {
            current_page,
            page_size
        }
    };

    try {
        const response = await fetch(
            "https://platform.tradew.com/openapis/keywords/rank",
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
