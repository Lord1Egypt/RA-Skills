const SENSITIVE_KEY_RE = /(^|_|\b)(authorization|token|secret|temporary[-_]?url|access[-_]?token|refresh[-_]?token|client[-_]?secret|figma[-_].*token|figma[-_].*secret)($|_|\b)/i;

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function redactKnownSecrets(text, secrets) {
  let output = text;
  for (const secret of secrets ?? []) {
    if (typeof secret !== 'string' || secret.length === 0) {
      continue;
    }
    output = output.replace(new RegExp(escapeRegExp(secret), 'g'), '[REDACTED]');
  }
  return output;
}

export function redactString(value, options = {}) {
  if (value === undefined || value === null) {
    return '';
  }

  let output = redactKnownSecrets(String(value), options.secrets);
  output = output.replace(/(Authorization\s*:\s*Bearer\s+)[^\s\r\n]+/gi, '$1[REDACTED]');
  output = output.replace(/(Authorization\s*=\s*Bearer\s+)[^\s\r\n]+/gi, '$1[REDACTED]');
  output = output.replace(/((?:FIGMA_[A-Z0-9_]*(?:TOKEN|SECRET)[A-Z0-9_]*|access_token|refresh_token|client_secret)\s*=\s*)[^\s\r\n&]+/gi, '$1[REDACTED]');
  output = output.replace(/("(?:access_token|refresh_token|client_secret|accessToken|refreshToken|clientSecret|Authorization)"\s*:\s*")[^"]+(")/gi, '$1[REDACTED]$2');
  output = output.replace(/https:\/\/[^\s"']*(?:figma|figma-image)[^\s"']*(?:sig|signature|X-Amz-Signature)=[^\s"']+/gi, '[REDACTED_URL]');
  output = output.replace(/([?&](?:sig|signature|X-Amz-Signature)=)[^&\s"']+/gi, '$1[REDACTED]');
  return output;
}

export function redactObject(value) {
  if (Array.isArray(value)) {
    return value.map((item) => redactObject(item));
  }

  if (value && typeof value === 'object') {
    return Object.fromEntries(
      Object.entries(value).map(([key, entryValue]) => {
        if (SENSITIVE_KEY_RE.test(key)) {
          return [key, '[REDACTED]'];
        }
        return [key, redactObject(entryValue)];
      }),
    );
  }

  if (typeof value === 'string') {
    return redactString(value);
  }

  return value;
}

export function createStableError(code, message, options = {}) {
  const error = new Error(redactString(message ?? code, options));
  error.code = code;
  if (options.retryable !== undefined) {
    error.retryable = options.retryable;
  }
  if (options.status !== undefined) {
    error.status = options.status;
  }
  return error;
}
