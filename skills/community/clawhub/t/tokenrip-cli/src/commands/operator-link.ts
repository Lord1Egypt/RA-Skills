import { randomUUID } from 'node:crypto';
import { loadIdentity } from '../identity.js';
import { signPayload } from '../crypto.js';
import { getFrontendUrl, loadConfig, saveConfig } from '../config.js';
import { requireAuthClient } from '../auth-client.js';
import { CliError, toCliError } from '../errors.js';
import { outputSuccess } from '../output.js';
import { createHttpClient } from '../client.js';
import { parseDuration } from './share.js';

export interface OperatorLinkIssue {
  code: string;
  message: string;
}

export async function operatorLink(
  options: { expires?: string },
): Promise<void> {
  const identity = loadIdentity();
  if (!identity) {
    throw new CliError('NO_IDENTITY', 'No agent identity found. Run `rip auth register` first.');
  }

  const auth = requireAuthClient();
  let client = auth.client;
  const frontendUrl = getFrontendUrl(auth.config);

  // Generate signed link (local, no server call)
  const exp = options.expires
    ? parseDuration(options.expires)
    : Math.floor(Date.now() / 1000) + 300; // default 5 minutes

  const token = signPayload(
    { sub: 'operator-auth', iss: identity.agentId, exp, jti: randomUUID() },
    identity.secretKey,
  );
  const url = `${frontendUrl}/operator/auth?token=${encodeURIComponent(token)}`;

  // Generate short code (server call, for MCP auth / cross-device)
  let code: string | null = null;
  let codeError: OperatorLinkIssue | null = null;
  let warning: OperatorLinkIssue | null = null;
  try {
    const { data } = await createLinkCode(client);
    code = data.data.code;
  } catch (initialError) {
    if (shouldRecoverLinkCodeError(initialError)) {
      try {
        const recovered = await recoverAuthClient(identity.agentId, identity.secretKey, auth.apiUrl);
        client = recovered.client;
        warning = recovered.warning;
        const { data } = await createLinkCode(client);
        code = data.data.code;
      } catch (retryError) {
        codeError = getErrorDetails(retryError);
      }
    } else {
      codeError = getErrorDetails(initialError);
    }
  }

  const expiresAt = new Date(exp * 1000).toISOString();

  outputSuccess(
    {
      url,
      code,
      code_error: codeError,
      warning,
      agent_id: identity.agentId,
      expires_at: expiresAt,
      ...(code && { link_page: `${frontendUrl}/link` }),
    },
    (data) => {
      const codeError = data.code_error as OperatorLinkIssue | null | undefined;
      const warning = data.warning as OperatorLinkIssue | null | undefined;
      const lines = [
        '',
        `Operator link for ${data.agent_id}:`,
        '',
        `  ${data.url}`,
        '',
      ];
      if (data.code) {
        lines.push(`Link code: ${data.code}`);
        lines.push(`Enter at ${data.link_page} — expires in 10 minutes`);
        lines.push('');
      } else if (codeError?.message) {
        lines.push(`Link code unavailable: ${codeError.message}`);
        lines.push('');
      }
      if (warning?.message) {
        lines.push(`Warning: ${warning.message}`);
        lines.push('');
      }
      lines.push(`Expires: ${data.expires_at}`);
      lines.push('');
      return lines.join('\n');
    },
  );
}

async function createLinkCode(client: ReturnType<typeof createHttpClient>) {
  return client.post('/v0/auth/link-code');
}

export function shouldRecoverLinkCodeError(error: unknown): boolean {
  const cliError = toCliError(error);
  return cliError.code === 'UNAUTHORIZED';
}

export async function recoverAuthClient(agentId: string, secretKey: string, apiUrl: string): Promise<{
  client: ReturnType<typeof createHttpClient>;
  warning: OperatorLinkIssue | null;
}> {
  const exp = Math.floor(Date.now() / 1000) + 300;
  const token = signPayload(
    { sub: 'key-recovery', iss: agentId, exp, jti: randomUUID() },
    secretKey,
  );

  const recoveryClient = createHttpClient({ baseUrl: apiUrl });
  const { data } = await recoveryClient.post('/v0/agents/recover-key', { token });
  const apiKey = data.data.api_key;
  let warning: OperatorLinkIssue | null = null;

  try {
    const config = loadConfig();
    config.apiKey = apiKey;
    saveConfig(config);
  } catch (error) {
    const details = error instanceof Error ? error.message : String(error);
    warning = {
      code: 'KEY_SAVE_FAILED',
      message: `Recovered a replacement API key but could not save it locally (${details}).`,
    };
  }

  return {
    client: createHttpClient({ baseUrl: apiUrl, apiKey }),
    warning,
  };
}

function getErrorDetails(error: unknown): OperatorLinkIssue {
  const cliError = toCliError(error);
  return {
    code: cliError.code || 'UNKNOWN_ERROR',
    message: cliError.message,
  };
}
