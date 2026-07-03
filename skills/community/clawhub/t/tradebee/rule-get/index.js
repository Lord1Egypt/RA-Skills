import { callTradebeeApi, getApiKeyOrError, isPlainObject, validateLanguage, validateRuleScene } from "../validation.js";

export default async function RuleGet(args = {}) {
    if (!isPlainObject(args)) {
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

    const sceneError = validateRuleScene(args.scene);
    if (sceneError) {
        return {
            status: false,
            msg: sceneError
        };
    }

    try {
        return await callTradebeeApi(
            "https://platform.tradew.com/openapis/rule",
            API_KEY,
            {
                language: args.language,
                scene: args.scene
            }
        );
    } catch (error) {
        return {
            status: false,
            msg: "Request failed."
        };
    }
}
