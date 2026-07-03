import { getApiKeyOrError, isPlainObject } from "../validation.js";

export default async function LanguagesGet(args = {}) {
    if (!isPlainObject(args)) {
        return {
            status: false,
            msg: "Invalid parameter: request.body. It must be a valid JSON object."
        };
    }

    const { apiKey: API_KEY, error: apiKeyError } = getApiKeyOrError(args);
    if (apiKeyError) return apiKeyError;

    try {
        const response = await fetch("https://platform.tradew.com/openapis/languages", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${API_KEY}`,
                "Content-Type": "application/json"
            }
        });

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
