export async function resolveThetaOnDemandToken(ctx, baseToken) {
    const env = ctx.env ?? {};
    if (ctx.getSecret) {
        for (const key of ['THETA_ONDEMAND_API_TOKEN', 'THETA_ONDEMAND_API_KEY', 'THETA_API_KEY']) {
            try {
                const secret = await ctx.getSecret(key);
                if (secret && secret.trim())
                    return secret.trim();
            }
            catch {
                // Intentionally swallow provider errors; continue chain.
            }
        }
    }
    for (const key of ['THETA_ONDEMAND_API_TOKEN', 'THETA_ONDEMAND_API_KEY', 'THETA_API_KEY']) {
        const envToken = env[key];
        if (envToken && envToken.trim())
            return envToken.trim();
    }
    if (baseToken && baseToken.trim())
        return baseToken.trim();
    return undefined;
}
