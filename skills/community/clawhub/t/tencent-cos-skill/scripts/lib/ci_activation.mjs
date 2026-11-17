/** Versioned, data-only activation handoff. No cloud request or model approval. */
export const CI_ACTIVATION_COMMANDS = Object.freeze({
  ci: 'create-ci-bucket',
  document: 'create-doc-process-bucket',
  media: 'create-media-bucket',
  voice: 'create-asr-bucket',
  file: 'create-file-process-bucket',
  asyncImage: 'create-async-image-process-bucket',
  asyncContentRecognition: 'create-ai-process-bucket',
});

const STATUS_KEYS = Object.freeze({
  document: 'documentProcessing',
  media: 'mediaProcessing',
  voice: 'voiceProcessing',
  file: 'fileProcessing',
  asyncImage: 'asyncImageProcessing',
  asyncContentRecognition: 'asyncContentRecognition',
});

const ACTIVATION_PATHS = Object.freeze({
  '/docbucket': 'document',
  '/mediabucket': 'media',
  '/asrbucket': 'voice',
  '/file_bucket': 'file',
  '/picbucket': 'asyncImage',
  '/ai_bucket': 'asyncContentRecognition',
});

export function validateRequiredCiService(service) {
  if (typeof service !== 'string' || !Object.hasOwn(CI_ACTIVATION_COMMANDS, service)) {
    const error = new Error(`unsupported required CI service: ${String(service)}`);
    error.code = 'InvalidArgs';
    throw error;
  }
}

export function evaluateCiActivation(snapshot, service) {
  validateRequiredCiService(service);
  const { bucket, region, ciBucketStatus, ciBucketError } = snapshot;
  const blocked = error => ({
    activationStatus: 'blocked',
    activationError: error || {
      code: 'CiActivationStatusUnknown',
      message: 'CI activation state could not be verified; no activation was requested',
    },
  });
  // The legacy status mapper also maps ownership failures to off, and arbitrary
  // errors to on. Only a verified off or the known unbound error is actionable.
  if (ciBucketError && !(ciBucketStatus === 'off' && ciBucketError.code === 'NoSuchBucket')) {
    return blocked(ciBucketError);
  }
  const missing = reason => {
    const interaction = {
      type: 'ci_activation',
      version: 1,
      status: 'requires_confirmation',
      bucket,
      region,
      service,
      reason,
      precheck: { ciBucketStatus, serviceStatus: 'disabled' },
    };
    return {
      activationStatus: 'requires_confirmation',
      interaction,
      // bash stdout is available to the model, while the UI stream can contain
      // only its length. Forward this exact object through invokeClient so the
      // workbench receives a visible, structured interaction request.
      clientAction: {
        skill: 'tencentcloud-cos',
        command: JSON.stringify({ action: 'requestCiActivation', ...interaction }),
      },
    };
  };
  if (ciBucketStatus === 'off') return missing('ci_not_enabled');
  if (ciBucketStatus !== 'on') return blocked();
  if (service === 'ci') return { activationStatus: 'already_enabled' };
  const serviceState = snapshot.dataProcessing?.[STATUS_KEYS[service]];
  if (serviceState?.error) return blocked(serviceState.error);
  if (serviceState?.status === 'disabled') return missing('service_not_enabled');
  if (serviceState?.status === 'enabled') return { activationStatus: 'already_enabled' };
  return blocked();
}

/**
 * Scope validation for a decision copied from the original invokeClient result.
 * This is not a signed authorization token: provenance is provided by the KiKi
 * conversation and Skill instructions, as with its existing confirmation flow.
 */
export function validateCiActivationConfirmation(value, { bucket, region, service }) {
  let decision = value;
  if (typeof value === 'string' && value.length <= 4096) {
    try { decision = JSON.parse(value); } catch { decision = null; }
  }
  const fields = ['type', 'version', 'status', 'bucket', 'region', 'service', 'toolCallId'];
  if (!decision || typeof decision !== 'object' || Array.isArray(decision)
    || Object.keys(decision).length !== fields.length || !fields.every(key => Object.hasOwn(decision, key))
    || decision.type !== 'ci_activation_decision' || decision.version !== 1 || decision.status !== 'confirmed'
    || decision.bucket !== bucket || decision.region !== region || decision.service !== service
    || typeof decision.toolCallId !== 'string' || !decision.toolCallId.trim()
    || decision.toolCallId !== decision.toolCallId.trim() || decision.toolCallId.length > 512) {
    const error = new Error('CI activation requires the confirmed result of the original client interaction for this bucket, region and service');
    error.code = 'InvalidCiActivationConfirmation';
    throw error;
  }
  validateRequiredCiService(service);
  return { ...decision };
}

/** Recognize the existing CI lifecycle write endpoints, including URL variants. */
export function getCiActivationRequestService({ method, host, pathname = '/' }) {
  if (!/(?:^|\.)ci\.[a-z0-9-]+\.myqcloud\.com$/i.test(String(host || ''))) return null;
  const normalizedMethod = String(method || '').trim().toUpperCase();
  let path;
  try {
    // URL parsing resolves dot segments; decoding also catches encoded slashes.
    const decoded = decodeURIComponent(new URL(`https://${host}/${String(pathname).replace(/^\/+/, '')}`).pathname);
    path = new URL(`https://${host}/${decoded.replace(/^\/+/, '')}`).pathname
      .replace(/\/+/g, '/').replace(/\/$/, '') || '/';
  } catch {
    return null;
  }
  if (normalizedMethod === 'PUT' && path === '/') return 'ci';
  return normalizedMethod === 'POST' && Object.hasOwn(ACTIVATION_PATHS, path)
    ? ACTIVATION_PATHS[path]
    : null;
}

export function assertCiActivationRequestAllowed(options, env = process.env) {
  if (String(env.KIKI || '').trim() !== '1') return;
  const service = getCiActivationRequestService(options);
  if (service) {
    // Only the dedicated lifecycle executor passes this scoped decision. Raw
    // ci-request and SDK entry points retain the default write restriction.
    if (options.activationConfirmation) {
      validateCiActivationConfirmation(options.activationConfirmation, {
        bucket: String(options.host).split('.ci.')[0],
        region: String(options.host).split('.ci.')[1]?.split('.myqcloud.com')[0],
        service,
      });
      if (Object.keys(options.query || {}).length === 0 && !String(options.pathname || '').includes('?')) return;
    }
    const error = new Error('CI activation is intercepted in KiKi; use the workbench activation interaction');
    error.code = 'CiActivationRequiresInteraction';
    throw error;
  }
}
