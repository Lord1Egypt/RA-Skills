// Used internally by the runtime config builder. The value is sent as a Bearer header to
// ondemand.thetaedgecloud.com and is never logged or included in command results.
export type ThetaSecretResolverContext = {
  env?: Record<string, string | undefined>;
  getSecret?: (key: string) => Promise<string | undefined>;
};

export async function resolveThetaOnDemandToken(
  ctx: ThetaSecretResolverContext,
  baseToken?: string
): Promise<string | undefined> {
  const callerEnv = ctx.env ?? {};

  if (ctx.getSecret) {
    for (const key of ['THETA_ONDEMAND_API_TOKEN', 'THETA_ONDEMAND_API_KEY', 'THETA_API_KEY']) {
      try {
        const secret = await ctx.getSecret(key);
        if (secret && secret.trim()) return secret.trim();
      } catch {
        // Intentionally swallow provider errors; continue chain.
      }
    }
  }

  for (const key of ['THETA_ONDEMAND_API_TOKEN', 'THETA_ONDEMAND_API_KEY', 'THETA_API_KEY']) {
    const envToken = callerEnv[key];
    if (envToken && envToken.trim()) return envToken.trim();
  }

  if (baseToken && baseToken.trim()) return baseToken.trim();

  return undefined;
}
