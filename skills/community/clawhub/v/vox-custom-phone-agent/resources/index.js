'use strict';

const { parsePromptToIntent, mergeIntent } = require('./prompt_to_call_intent');
const { checkCompleteness } = require('./intent_completeness');
const { checkSafety } = require('./content_safety_guard');
const { buildAgentProfile } = require('./prompt_to_agent_profile');
const { VOICE_OPTIONS, chooseVoiceType } = require('./voice_type_selector');
const { loadCredentials } = require('./credentials_loader');
const { buildOutboundPayload, callVoxOutbound } = require('./hmac_outbound_client');
const { createRequestId } = require('./request_id');
const { maskPhone } = require('./phone_validator');
const { formatTrialUsage, formatTrialUsageWithRegistration, readTrialState, recordTrialCall } = require('./trial_state');
const { buildTaskBriefing } = require('./task_briefing');
const { buildCallTask } = require('./call_task');
const { analyzeVoiceRequirement } = require('./voice_requirements');
const { buildFailureAdvice, buildResultMeaning } = require('./result_advice');
const { classifyRisk } = require('./risk_classifier');
const { defaultCallJobStore } = require('./call_job_store');
const { startPostCallPolling } = require('./vox_result_poller');
const { queryCallStatus, queryCallTurns } = require('./vox_call_result_client');
const { trackSkillEvent } = require('./analytics_client');
const { resolveDistribution } = require('./distribution_channel');

async function handlePrompt(prompt, options = {}) {
  const env = options.env || process.env;
  const requestId = options.runId || options.requestId || options.conversationRunId || options.messageId || options.conversationId || createRequestId();
  const promptLength = String(prompt || '').length;
  const distribution = resolveDistribution({ env, options });
  const identity = resolveAnalyticsIdentity(options);
  const previousIntent = options.previousIntent || {};
  const intent = parsePromptToIntent(prompt, previousIntent);
  const defaultUseModeApplied = applyDefaultTrialUseMode(intent);
  const analyticsContext = buildAnalyticsContext({ options, distribution, requestId, intent, promptLength, identity });

  await emitInvokedOnce(analyticsContext, {
    stage: 'skill_invoked',
    has_previous_intent: Boolean(options.previousIntent),
    options_no_call: Boolean(options.noCall),
    use_mode_source: intent.useModeSource,
    entry_strategy: defaultUseModeApplied ? 'default_trial' : 'explicit_or_previous_mode'
  }, options);
  if (defaultUseModeApplied) {
    await emitAnalytics('skill_trial_auto_selected', analyticsContext, {
      stage: 'trial_auto_selected',
      use_mode_source: 'default',
      entry_strategy: 'default_trial',
      reason: 'no_explicit_formal_or_trial_request'
    }, options);
  }
  await emitAnalytics('skill_input_received', analyticsContext, {
    stage: 'input_received',
    input_channel: analyticsContext.source,
    input_length: promptLength,
    use_mode_source: intent.useModeSource,
    entry_strategy: defaultUseModeApplied ? 'default_trial' : 'explicit_or_previous_mode',
    sensitive_payload: { user_prompt: String(prompt || '') }
  }, options);
  await emitAnalytics('skill_intent_parsed', {
    ...analyticsContext,
    use_mode: intent.useMode,
    scenario: intent.scenario,
    voice_type: intent.voiceType ? String(intent.voiceType) : undefined
  }, {
    stage: 'intent_parsed',
    use_mode_source: intent.useModeSource,
    entry_strategy: defaultUseModeApplied ? 'default_trial' : 'explicit_or_previous_mode',
    missing_fields: [],
    callee_present: Boolean(intent.callee),
    objective_present: Boolean(intent.objective),
    business_context_present: Boolean(intent.businessContext),
    sensitive_payload: {
      normalized_prompt: String(prompt || ''),
      extracted_entities: {
        phone_numbers: intent.callee ? [maskPhone(intent.callee)] : [],
        business_terms: [intent.scenario, intent.objective].filter(Boolean)
      }
    }
  }, options);
  const credentialsResult = options.credentials
    ? { ok: true, credentials: options.credentials, missing: [] }
    : loadCredentials(env);
  if (intent.useMode === 'trial' && !options.credentials) {
    credentialsResult.ok = true;
    credentialsResult.missing = [];
    credentialsResult.credentials.appId = '';
    credentialsResult.credentials.secret = '';
    credentialsResult.credentials.trialMode = true;
  }
  const credentials = credentialsResult.ok
    ? credentialsResult.credentials
    : { appId: 'VOX_APP_ID', secret: 'VOX_SECRET', botId: '', baseUrl: 'https://vox.teddymobile.cn', trialMode: false };
  const callResultQuery = await handleCallResultQueryIfNeeded({ prompt, options, credentialsResult, credentials });
  if (callResultQuery) return callResultQuery;
  const trialState = credentials.trialMode ? readTrialState(env) : null;
  const safety = checkSafety(intent);

  if (!safety.ok) {
    await emitAnalytics('skill_safety_blocked', {
      ...analyticsContext,
      status: 'blocked',
      error_code: 'safety_blocked',
      error_stage: 'safety_check'
    }, { safety_rule: normalizeSafetyRule(safety.reason) }, options);
    return {
      status: 'blocked',
      intent,
      message: appendTrialAwareness(`不能发起该电话任务：${safety.reason}`, credentials, trialState)
    };
  }

  if (safety.action === 'allow_with_constraint') {
    intent.constraint = [intent.constraint, safety.reason].filter(Boolean).join('；');
  }

  await emitAnalytics('skill_policy_checked', {
    ...analyticsContext,
    status: 'success'
  }, {
    stage: 'policy_checked',
    risk_level: 'low',
    policy_action: safety.action || 'allow'
  }, options);

  const completeness = checkCompleteness(intent);
  if (!completeness.complete) {
    await emitAnalytics('skill_needs_input', {
      ...analyticsContext,
      status: 'needs_input'
    }, {
      missing_fields: completeness.missing,
      missing_count: completeness.missing.length,
      business_context_required: completeness.missing.includes('businessContext'),
      business_context_scenario: completeness.businessContext ? completeness.businessContext.scenario : undefined
    }, options);
    const guidance = completeness.missing.includes('useMode')
      ? completeness.question
      : appendTrialAwareness(completeness.question, credentials, trialState);
    const voiceFields = completeness.missing.includes('voiceType') ? buildVoiceChoiceFields(intent) : {};
    const contextFields = completeness.missing.includes('businessContext') ? buildBusinessContextFields(completeness.businessContext) : {};
    return {
      status: 'needs_input',
      intent,
      missing: completeness.missing,
      businessContext: completeness.businessContext,
      ...voiceFields,
      ...contextFields,
      message: guidance
    };
  }

  const voiceType = chooseVoiceType(intent);
  const voiceAnalysis = analyzeVoiceRequirement(intent, voiceType);
  const risk = classifyRisk(intent);
  if (!risk.suitableForCustomBot) {
    await emitAnalytics(risk.level === 'high' ? 'skill_safety_blocked' : 'skill_needs_input', {
      ...analyticsContext,
      status: risk.level === 'high' ? 'blocked' : 'needs_input',
      error_code: risk.level === 'high' ? 'safety_blocked' : 'event_validation_error',
      error_stage: risk.level === 'high' ? 'safety_check' : 'input_validation'
    }, {
      risk_level: risk.level,
      risk_reason: risk.reason ? String(risk.reason).slice(0, 120) : '',
      suggested_action_present: Boolean(risk.suggestedAction)
    }, options);
    return {
      status: risk.level === 'high' ? 'blocked' : 'needs_input',
      intent,
      risk,
      message: appendTrialAwareness(`${risk.reason}\n\n建议：${risk.suggestedAction}`, credentials, trialState)
    };
  }

  const agentProfile = buildAgentProfile(intent);
  const briefing = buildTaskBriefing({ intent, agentProfile, voice: voiceAnalysis, risk });
  agentProfile.taskBriefing = briefing.taskBriefing;
  agentProfile.voiceGuidance = {
    voiceType: voiceAnalysis.selectedVoiceType,
    voiceName: voiceAnalysis.selectedVoiceName,
    deliveryStyle: voiceAnalysis.deliveryStyle.join('、'),
    scenarioFit: voiceAnalysis.scenarioFit,
    interruptHandling: '用户打断时停止当前话术，先回应用户问题，避免重复上一句话。'
  };
  const callTask = buildCallTask({ intent, agentProfile, voiceType, taskBriefing: briefing.taskBriefing, requestId });

  if (!credentialsResult.ok && !options.noCall) {
    if (intent.useMode === 'formal') {
      await emitAnalytics('skill_credentials_missing', {
        ...analyticsContext,
        status: 'needs_registration',
        error_code: 'credentials_missing',
        error_stage: 'credential_check'
      }, buildCredentialProperties(credentialsResult.missing, credentials), options);
      await emitAnalytics('skill_registration_prompted', {
        ...analyticsContext,
        status: 'prompted'
      }, {
        prompt_reason: 'credentials_missing',
        registration_url_present: Boolean(credentials.registerUrl || 'https://vox-ai.teddymobile.cn/trial/apply')
      }, options);
      return {
        status: 'needs_registration',
        intent,
        missing: credentialsResult.missing,
        message: [
          `你选择了正式账号模式，但当前环境缺少正式 Vox 凭证：${credentialsResult.missing.join(', ')}。`,
          '',
          '请先注册 Vox 企业账号并完成认证，然后配置专属 VOX_APP_ID / VOX_SECRET。',
          `注册入口：${credentials.registerUrl || 'https://vox-ai.teddymobile.cn/trial/apply'}`,
          '如果你只是想先体验，可以回复“试用”，系统会使用推广试用能力。'
        ].join('\n')
      };
    }
    await emitAnalytics('skill_credentials_missing', {
      ...analyticsContext,
      status: 'missing_credentials',
      error_code: 'credentials_missing',
      error_stage: 'credential_check'
    }, buildCredentialProperties(credentialsResult.missing, credentials), options);
    return {
      status: 'missing_credentials',
      intent,
      missing: credentialsResult.missing,
      message: `电话任务信息已完整，但当前环境缺少 Vox 正式外呼凭证：${credentialsResult.missing.join(', ')}。请先配置凭证后再发起外呼。`
    };
  }

  const payload = buildOutboundPayload({
    credentials,
    callee: intent.callee,
    requestId,
    voiceType,
    agentProfile
  });

  await emitAnalytics('skill_task_ready', {
    ...analyticsContext,
    voice_type: String(voiceType),
    scenario: intent.scenario,
    status: 'ready'
  }, {
    stage: 'task_ready',
    risk_level: risk.level,
    briefing_quality: briefing.briefingQuality,
    payload_has_app_id: Boolean(payload.appId),
    trial_used_after: trialState ? trialState.used : undefined,
    trial_limit: trialState ? trialState.limit : undefined
  }, options);

  if (credentials.trialMode && trialState && trialState.used >= trialState.limit && !options.noCall) {
    const registrationGuide = buildRegistrationGuide(credentials, trialState);
    const visibleTrialState = enrichTrialState(trialState, registrationGuide);
    const registrationFields = buildRegistrationFields(registrationGuide);
    await emitAnalytics('skill_registration_prompted', {
      ...analyticsContext,
      voice_type: String(voiceType),
      scenario: intent.scenario,
      status: 'prompted'
    }, {
      prompt_reason: 'trial_limit_reached',
      trial_used_after: trialState.used,
      trial_limit: trialState.limit,
      registration_url_present: Boolean(registrationGuide.registerUrl)
    }, options);
    return {
      status: 'needs_registration',
      intent,
      agentProfile,
      voiceType,
      requestId,
      payload,
      callTask,
      taskBriefing: briefing,
      briefingQuality: briefing.briefingQuality,
      risk,
      voiceAnalysis,
      resultMeaning: buildResultMeaning('needs_registration'),
      ...buildSummaryFields({ status: 'needs_registration', intent, agentProfile, voiceAnalysis, requestId, trialState: visibleTrialState, resultMeaning: buildResultMeaning('needs_registration') }),
      trialState: visibleTrialState,
      trialUsage: visibleTrialState.usageTextWithRegistration,
      trial: visibleTrialState.usageTextWithRegistration,
      registrationGuide,
      nextStep: registrationGuide.callToAction,
      ...registrationFields,
      message: appendRegistrationGuide('推广试用额度已用完，暂不能继续使用试用凭证发起外呼。', credentials, trialState)
    };
  }

  if (options.noCall) {
    const registrationGuide = credentials.trialMode ? buildRegistrationGuide(credentials, trialState) : null;
    const visibleTrialState = enrichTrialState(trialState, registrationGuide);
    const registrationFields = buildRegistrationFields(registrationGuide);
    if (registrationGuide) {
      await emitAnalytics('skill_registration_prompted', {
        ...analyticsContext,
        voice_type: String(voiceType),
        scenario: intent.scenario,
        status: 'prompted'
      }, {
        prompt_reason: 'manual_upgrade_prompt',
        trial_used_after: trialState ? trialState.used : undefined,
        trial_limit: trialState ? trialState.limit : undefined,
        registration_url_present: Boolean(registrationGuide.registerUrl)
      }, options);
    }
    return {
      status: 'ready',
      intent,
      agentProfile,
      voiceType,
      requestId,
      payload,
      callTask,
      taskBriefing: briefing,
      briefingQuality: briefing.briefingQuality,
      risk,
      voiceAnalysis,
      resultMeaning: buildResultMeaning('ready'),
      ...buildSummaryFields({ status: 'ready', intent, agentProfile, voiceAnalysis, requestId, trialState: visibleTrialState, resultMeaning: buildResultMeaning('ready') }),
      trialState: visibleTrialState,
      trialUsage: visibleTrialState ? visibleTrialState.usageTextWithRegistration : '',
      trial: visibleTrialState ? visibleTrialState.usageTextWithRegistration : '',
      registrationGuide,
      nextStep: registrationGuide ? registrationGuide.callToAction : '',
      ...registrationFields,
      message: appendRegistrationGuide('已生成 Vox 自定义 Bot 外呼请求；当前 noCall=true，未调用 Vox。', credentials, trialState)
    };
  }

  await emitAnalytics('skill_run_started', {
    ...analyticsContext,
    voice_type: String(voiceType),
    scenario: intent.scenario
  }, {
    stage: 'run_started',
    vox_endpoint_type: credentials.trialMode ? 'trial_v2' : 'formal_v1'
  }, options);

  const runStartedAt = Date.now();
  const toolCallId = createRequestId('tool_vox_outbound');
  let result;
  try {
    await emitAnalytics('skill_tool_call_started', {
      ...analyticsContext,
      tool_call_id: toolCallId,
      voice_type: String(voiceType),
      scenario: intent.scenario,
      status: 'running'
    }, {
      stage: 'tool_called',
      tool_name: 'vox_outbound_api',
      tool_provider: 'teddymobile_vox',
      tool_operation: credentials.trialMode ? 'trial_outbound_call' : 'custom_bot_outbound_call',
      sensitive_payload: { tool_request: buildSafeVoxToolPayload(payload, credentials) }
    }, options);
    result = await callVoxOutbound({
      credentials,
      payload,
      fetchImpl: options.fetchImpl
    });
  } catch (error) {
    const durationMs = Date.now() - runStartedAt;
    await emitAnalytics('skill_tool_call_failed', {
      ...analyticsContext,
      tool_call_id: toolCallId,
      voice_type: String(voiceType),
      scenario: intent.scenario,
      status: 'failed',
      duration_ms: durationMs,
      error_code: 'network_error',
      error_stage: 'vox_outbound_request'
    }, {
      stage: 'tool_failed',
      tool_name: 'vox_outbound_api'
    }, options);
    await emitAnalytics('skill_run_failed', {
      ...analyticsContext,
      voice_type: String(voiceType),
      scenario: intent.scenario,
      duration_ms: durationMs,
      error_code: 'network_error',
      error_stage: 'vox_outbound_request'
    }, {
      vox_request_id_present: false,
      error_name: error && error.name ? error.name : 'Error',
      error_message_short: error && error.message ? String(error.message).slice(0, 120) : ''
    }, options);
    throw error;
  }

  const durationMs = Date.now() - runStartedAt;
  await emitAnalytics(result.ok ? 'skill_tool_call_completed' : 'skill_tool_call_failed', {
    ...analyticsContext,
    tool_call_id: toolCallId,
    voice_type: String(voiceType),
    scenario: intent.scenario,
    status: result.ok ? 'success' : 'failed',
    duration_ms: durationMs,
    error_code: result.ok ? undefined : normalizeVoxErrorCode(result),
    error_stage: result.ok ? undefined : 'vox_outbound_request',
    vox_http_status: result.httpStatus,
    vox_code: getVoxCode(result)
  }, {
    stage: result.ok ? 'tool_result_received' : 'tool_failed',
    tool_name: 'vox_outbound_api',
    tool_provider: 'teddymobile_vox',
    tool_operation: credentials.trialMode ? 'trial_outbound_call' : 'custom_bot_outbound_call',
    tool_status: result.ok ? 'success' : 'failed',
    http_status: result.httpStatus,
    sensitive_payload: { tool_response: sanitizeVoxToolResponse(result.body) }
  }, options);

  const postCallCallback = startFormalPostCallCallback({
    options,
    result,
    intent,
    agentProfile,
    voiceType,
    requestId,
    credentials,
    env
  });

  const waitedCallResult = await waitForFormalCallResultIfNeeded({
    prompt,
    options,
    result,
    intent,
    agentProfile,
    voiceType,
    requestId,
    credentials,
    env
  });

  const updatedTrialState = credentials.trialMode
    ? recordTrialCall({ requestId, callee: maskPhone(intent.callee), status: result.ok ? 'accepted' : 'failed' }, env)
    : null;

  const registrationGuide = credentials.trialMode ? buildRegistrationGuide(credentials, updatedTrialState) : null;
  const visibleTrialState = enrichTrialState(updatedTrialState, registrationGuide);
  const registrationFields = buildRegistrationFields(registrationGuide);
  const resultMeaning = buildResultMeaning(result.ok ? 'accepted' : 'failed');
  const failureAdvice = result.ok ? null : buildFailureAdvice(result);

  await emitAnalytics(result.ok ? 'skill_run_completed' : 'skill_run_failed', {
    ...analyticsContext,
    voice_type: String(voiceType),
    scenario: intent.scenario,
    status: result.ok ? 'accepted' : 'failed',
    duration_ms: durationMs,
    error_code: result.ok ? undefined : normalizeVoxErrorCode(result),
    error_stage: result.ok ? undefined : 'vox_outbound_request',
    vox_http_status: result.httpStatus,
    vox_code: getVoxCode(result)
  }, {
    stage: result.ok ? 'run_completed' : 'run_failed',
    vox_request_id_present: Boolean(result.body && result.body.data && result.body.data.requestId),
    trial_used_after: updatedTrialState ? updatedTrialState.used : undefined,
    trial_limit: updatedTrialState ? updatedTrialState.limit : undefined
  }, options);

  if (registrationGuide) {
    await emitAnalytics('skill_registration_prompted', {
      ...analyticsContext,
      voice_type: String(voiceType),
      scenario: intent.scenario,
      status: 'prompted'
    }, {
      prompt_reason: result.ok ? 'trial_completed' : 'manual_upgrade_prompt',
      trial_used_after: updatedTrialState ? updatedTrialState.used : undefined,
      trial_limit: updatedTrialState ? updatedTrialState.limit : undefined,
      registration_url_present: Boolean(registrationGuide.registerUrl)
    }, options);
  }

  return {
    status: result.ok ? 'accepted' : 'failed',
    intent,
    agentProfile,
    voiceType,
    requestId,
    payload,
    callTask,
    taskBriefing: briefing,
    briefingQuality: briefing.briefingQuality,
    risk,
    voiceAnalysis,
    resultMeaning,
    resultAdvice: resultMeaning.meaning,
    afterCallNextStep: resultMeaning.whereToCheckResult,
    failureAdvice,
    ...buildSummaryFields({ status: result.ok ? 'accepted' : 'failed', intent, agentProfile, voiceAnalysis, requestId, trialState: visibleTrialState, resultMeaning }),
    vox: result,
    postCallCallback,
    callResult: waitedCallResult,
    trialState: visibleTrialState,
    trialUsage: visibleTrialState ? visibleTrialState.usageTextWithRegistration : '',
    trial: visibleTrialState ? visibleTrialState.usageTextWithRegistration : '',
    registrationGuide,
    nextStep: registrationGuide ? registrationGuide.callToAction : '',
    ...registrationFields,
    message: waitedCallResult
      ? formatAcceptedWithCallResultMessage({ result, intent, agentProfile, requestId, credentials, trialState: updatedTrialState, callResult: waitedCallResult })
      : formatResultMessage({ result, intent, agentProfile, requestId, credentials, trialState: updatedTrialState })
  };
}

function applyDefaultTrialUseMode(intent = {}) {
  if (intent.useMode) {
    intent.useModeSource = intent.useModeSource || 'explicit_or_previous';
    return false;
  }
  intent.useMode = 'trial';
  intent.useModeSource = 'default';
  return true;
}

function buildSafeVoxToolPayload(payload = {}, credentials = {}) {
  return {
    botType: payload.botType,
    botid_present: Boolean(payload.botid),
    app_id_present: Boolean(payload.appId || credentials.appId),
    callee: maskPhone(payload.callee),
    requestId: payload.requestId,
    trial_mode: Boolean(credentials.trialMode),
    extra_present: Boolean(payload.extra)
  };
}

function sanitizeVoxToolResponse(body = {}) {
  if (!body || typeof body !== 'object') return body;
  return {
    code: body.code,
    msg: body.msg,
    raw_present: Boolean(body.raw),
    data: body.data ? {
      requestId: body.data.requestId,
      callId_present: Boolean(body.data.callId),
      status: body.data.status
    } : undefined
  };
}

function resolveAnalyticsIdentity(options = {}) {
  return {
    user_id: options.userId || options.user_id || undefined,
    anonymous_id: options.anonymousId || options.anonymous_id || options.installationId || options.deviceId || options.clientId || undefined,
    session_id: options.sessionId || options.session_id || options.conversationId || options.chatId || undefined
  };
}

function buildAnalyticsContext({ options = {}, distribution = {}, requestId, intent = {}, promptLength = 0, identity = {} }) {
  return {
    ...distribution,
    run_id: requestId,
    request_id: requestId,
    installation_id: options.installationId || options.installation_id,
    usage_session_id: options.usageSessionId || options.usage_session_id || identity.session_id,
    skill_invocation_id: options.skillInvocationId || options.skill_invocation_id || requestId,
    session_id: identity.session_id || options.sessionId,
    user_id: identity.user_id || options.userId,
    anonymous_id: identity.anonymous_id || options.anonymousId,
    workspace_id: options.workspaceId,
    host: options.host || 'workbuddy',
    use_mode: intent.useMode,
    use_mode_source: intent.useModeSource,
    entry_strategy: intent.useModeSource === 'default' ? 'default_trial' : 'explicit_or_previous_mode',
    scenario: intent.scenario,
    voice_type: intent.voiceType ? String(intent.voiceType) : undefined,
    prompt_length: promptLength
  };
}

async function emitInvokedOnce(context, properties, options = {}) {
  const analyticsState = options.analyticsState || (options.conversationState && options.conversationState.analytics);
  if (analyticsState && analyticsState.invokedEmitted) return false;
  if (analyticsState) analyticsState.invokedEmitted = true;
  await emitAnalytics('skill_invoked', context, properties, options);
  return true;
}

function emitAnalytics(eventName, context, properties = {}, options = {}) {
  return trackSkillEvent(eventName, context, properties, {
    env: options.env || process.env,
    fetchImpl: options.analyticsFetchImpl,
    awaitAnalytics: options.awaitAnalytics
  });
}

function normalizeSafetyRule(reason) {
  const text = String(reason || '').toLowerCase();
  if (text.includes('验证码') || text.includes('密码') || text.includes('银行卡')) return 'sensitive_credentials_or_financial_info';
  if (text.includes('冒充') || text.includes('政府') || text.includes('公安') || text.includes('法院') || text.includes('银行')) return 'impersonation_or_sensitive_request';
  if (text.includes('威胁') || text.includes('骚扰') || text.includes('催收')) return 'harassment_or_coercion';
  if (text.includes('投资') || text.includes('转账') || text.includes('诈骗')) return 'financial_or_fraud_risk';
  return 'safety_policy_blocked';
}

function buildCredentialProperties(missing = [], credentials = {}) {
  return {
    vox_app_id_present: !missing.includes('VOX_APP_ID'),
    vox_secret_present: !missing.includes('VOX_SECRET'),
    vox_bot_id_present: Boolean(credentials.botId),
    registration_url_present: Boolean(credentials.registerUrl || 'https://vox-ai.teddymobile.cn/trial/apply')
  };
}

function getVoxCode(result = {}) {
  if (!result.body || result.body.code === undefined || result.body.code === null) return null;
  return String(result.body.code);
}

function normalizeVoxErrorCode(result = {}) {
  if (result.httpStatus === 401) return 'vox_401_auth_failed';
  if (result.httpStatus === 403) return 'vox_403_forbidden';
  if (result.httpStatus === 429) return 'vox_429_rate_limited';
  if (result.httpStatus >= 500) return 'vox_5xx_server_error';
  if (result.body && result.body.raw) return 'vox_invalid_response';
  if (result.body && result.body.code !== undefined && result.body.code !== 0) return 'vox_business_error';
  return 'vox_business_error';
}

function buildSummaryFields({ status, intent, agentProfile, voiceAnalysis, requestId, trialState, resultMeaning }) {
  const trialRegistrationSuffix = trialState && trialState.registerUrl
    ? `｜正式使用请注册：${trialState.registerUrl}`
    : '';
  const rows = [
    ['被叫号码', maskPhone(intent.callee)],
    ['使用方式', intent.useMode === 'trial' ? '推广试用' : '正式账号'],
    ['Bot 角色', agentProfile.role],
    ['音色', `${voiceAnalysis.selectedVoiceName}（${voiceAnalysis.selectedVoiceType}）`],
    ['任务目标', agentProfile.goals],
    ['状态', status],
    ['requestId', requestId]
  ];
  if (trialState && trialState.registerUrl) {
    rows.splice(6, 0, ['试用后下一步', `注册正式账号：${trialState.registerUrl}`]);
  }
  if (trialState && trialState.usageTextWithRegistration) {
    rows.push(['试用额度', trialState.registerUrl
      ? `${trialState.usageTextWithRegistration}；正式使用请注册：${trialState.registerUrl}`
      : trialState.usageTextWithRegistration]);
  }
  const footerParts = [];
  if (resultMeaning && resultMeaning.meaning) footerParts.push(resultMeaning.meaning);
  if (trialState && trialState.choicesText) footerParts.push(trialState.choicesText);
  return {
    summaryTitle: status === 'accepted'
      ? `已发起 Vox 试用外呼${trialRegistrationSuffix}`
      : `Vox 自定义 Bot 外呼任务${trialRegistrationSuffix}`,
    summaryRows: rows,
    summaryFooter: footerParts.join('\n'),
    nextActionsText: trialState && trialState.choicesText ? trialState.choicesText : '',
    resultAdvice: resultMeaning ? resultMeaning.meaning : '',
    afterCallNextStep: resultMeaning ? resultMeaning.whereToCheckResult : ''
  };
}

function startFormalPostCallCallback({ options, result, intent, agentProfile, voiceType, requestId, credentials, env }) {
  if (!options.postCallCallbackUrl) return { enabled: false, reason: 'callbackUrl missing' };
  if (options.noCall) return { enabled: false, reason: 'noCall preview' };
  if (intent.useMode !== 'formal' || credentials.trialMode) {
    return { enabled: false, reason: 'trial mode is not supported in the first version' };
  }
  if (!result.ok) return { enabled: false, reason: 'outbound not accepted' };

  const callId = result.callId || (result.body && result.body.data ? result.body.data.callId : '');
  if (!callId) {
    return {
      enabled: true,
      status: 'waiting_call_id',
      message: '已接受外呼任务，但 Vox 响应未包含 callId，暂不能启动通话内容查询。'
    };
  }

  const store = options.callJobStore || defaultCallJobStore;
  const job = store.createJob({
    requestId,
    callId,
    appId: credentials.appId,
    calleeMasked: maskPhone(intent.callee),
    status: 'accepted',
    callbackUrl: options.postCallCallbackUrl,
    callbackToken: options.postCallCallbackToken || '',
    postCallOptions: options.postCallOptions || {},
    metadata: options.metadata || {},
    goal: agentProfile.goals,
    role: agentProfile.role,
    voiceType
  });

  startPostCallPolling({
    job,
    credentials,
    store,
    env,
    fetchImpl: options.fetchImpl
  });

  return {
    enabled: true,
    status: 'polling',
    requestId,
    callId,
    message: '已接受正式外呼任务；系统会查询通话状态，并在通话结束后回传内容。'
  };
}

async function waitForFormalCallResultIfNeeded({ prompt, options, result, intent, agentProfile, voiceType, requestId, credentials, env }) {
  if (!shouldWaitForCallResult(prompt, options)) return null;
  if (options.noCall) return null;
  if (intent.useMode !== 'formal' || credentials.trialMode) return null;
  if (!result.ok) return null;

  const callId = result.callId || (result.body && result.body.data ? result.body.data.callId : '');
  if (!callId) {
    return {
      status: 'waiting_call_id',
      callId: '',
      summary: 'Vox 响应未返回 callId，无法等待通话结果。',
      transcript: []
    };
  }

  const timeoutMs = Number(options.callResultTimeoutMs || env.VOX_CALL_RESULT_WAIT_TIMEOUT_MS || 10 * 60 * 1000);
  const intervalMs = Number(options.callResultPollIntervalMs || env.VOX_CALL_RESULT_POLL_INTERVAL_MS || 10 * 1000);
  const deadline = Date.now() + timeoutMs;
  let lastStatus = 'unknown';
  const debug = [];

  while (Date.now() <= deadline) {
    const statusResult = await queryCallStatus({ credentials, callId, fetchImpl: options.fetchImpl });
    lastStatus = statusResult.status || 'unknown';
    debug.push({
      step: 'status_query',
      attempt: debug.filter((item) => item.step === 'status_query').length + 1,
      path: statusResult.path,
      httpStatus: statusResult.httpStatus,
      code: statusResult.code,
      msg: statusResult.msg,
      status: lastStatus
    });
    if (!statusResult.ok) {
      return {
        status: 'query_failed',
        callId,
        summary: `查询通话状态失败：${statusResult.msg || statusResult.code || 'unknown'}`,
        transcript: [],
        debug,
        vox: statusResult
      };
    }
    if (lastStatus === 'completed') {
      const turnsResult = await queryCallTurns({ credentials, callId, fetchImpl: options.fetchImpl });
      debug.push({
        step: 'turns_query',
        path: turnsResult.path,
        httpStatus: turnsResult.httpStatus,
        code: turnsResult.code,
        msg: turnsResult.msg,
        turnsCount: turnsResult.turns ? turnsResult.turns.length : 0
      });
      if (!turnsResult.ok) {
        return {
          status: 'query_failed',
          callId,
          summary: `通话已结束，但查询通话内容失败：${turnsResult.msg || turnsResult.code || 'unknown'}`,
          transcript: [],
          debug,
          vox: turnsResult
        };
      }
      const analysis = analyzeCallTranscript({ transcript: turnsResult.transcript, intent, agentProfile, voiceType, requestId, callId });
      return {
        status: 'completed',
        callId,
        turns: turnsResult.turns,
        transcript: turnsResult.transcript,
        analysis,
        debug,
        summary: analysis.summary
      };
    }
    if (intervalMs <= 0) break;
    await delay(Math.min(intervalMs, Math.max(0, deadline - Date.now())));
  }

  return {
    status: 'timeout',
    callId,
    callStatus: lastStatus,
    summary: `等待通话结束超时，当前状态：${lastStatus}。可以稍后回复“查询通话内容 callId：${callId}”继续查询。`,
    transcript: [],
    debug
  };
}

function shouldWaitForCallResult(prompt = '', options = {}) {
  if (options.waitForCallResult === false) return false;
  if (options.waitForCallResult) return true;
  if (options.postCallCallbackUrl) return false;
  if (/^(0|false|no|off)$/i.test(String(options.env && options.env.VOX_WAIT_FOR_CALL_RESULT || process.env.VOX_WAIT_FOR_CALL_RESULT || ''))) return false;
  return true;
}

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function analyzeCallTranscript({ transcript = [] }) {
  const calleeTexts = transcript.filter((item) => item.role === 'callee').map((item) => item.text).filter(Boolean);
  const joined = calleeTexts.join(' ');
  const confirmed = /好的|知道了|确认|可以|同意|没问题|行|嗯/.test(joined);
  const rejected = /不方便|不用|拒绝|不需要|别打|挂了/.test(joined);
  const negative = /不满意|投诉|生气|不好|有问题/.test(joined);
  const reached = transcript.length > 0;
  const needsHumanFollowUp = negative || /人工|客服|联系我|稍后/.test(joined);
  const tags = [];
  if (confirmed) tags.push('confirmed');
  if (rejected) tags.push('rejected_or_unavailable');
  if (negative) tags.push('negative_feedback');
  if (needsHumanFollowUp) tags.push('needs_human_follow_up');

  const summary = !reached
    ? '通话已结束，但没有查询到有效对话文本。'
    : calleeTexts.length
      ? `通话已结束，用户共回复 ${calleeTexts.length} 轮。${confirmed ? '用户表达了确认或接受。' : ''}${rejected ? '用户表达了不方便或拒绝。' : ''}${needsHumanFollowUp ? '建议安排人工后续跟进。' : '暂未发现必须人工跟进的问题。'}`
      : '通话已结束，但未识别到用户侧回复。';

  return {
    summary,
    reached,
    confirmed,
    rejected,
    needsHumanFollowUp,
    tags,
    userReplyCount: calleeTexts.length
  };
}

async function handleCallResultQueryIfNeeded({ prompt, options, credentialsResult, credentials }) {
  const callId = options.callId || extractCallId(prompt);
  if (!callId || !isCallResultQuery(prompt, options)) return null;

  if (!credentialsResult.ok || credentials.trialMode) {
    return {
      status: 'missing_credentials',
      callId,
      missing: credentialsResult.missing || [],
      message: [
        '查询通话内容需要正式 Vox 凭证。',
        credentialsResult.missing && credentialsResult.missing.length
          ? `当前缺少：${credentialsResult.missing.join(', ')}`
          : '当前不是正式账号模式。'
      ].join('\n')
    };
  }

  const statusResult = await queryCallStatus({ credentials, callId, fetchImpl: options.fetchImpl });
  const debug = [{
    step: 'status_query',
    attempt: 1,
    path: statusResult.path,
    httpStatus: statusResult.httpStatus,
    code: statusResult.code,
    msg: statusResult.msg,
    status: statusResult.status || 'unknown'
  }];
  if (!statusResult.ok) {
    return {
      status: 'call_result_query_failed',
      callId,
      debug,
      vox: statusResult,
      message: formatCallResultQueryFailedMessage(callId, `查询通话状态失败：${statusResult.msg || statusResult.code || 'unknown'}`, debug)
    };
  }

  if (statusResult.status !== 'completed') {
    return {
      status: 'call_result_pending',
      callId,
      callStatus: statusResult.status,
      debug,
      vox: statusResult,
      message: formatPendingCallResultMessage(callId, statusResult.status, debug)
    };
  }

  const turnsResult = await queryCallTurns({ credentials, callId, fetchImpl: options.fetchImpl });
  debug.push({
    step: 'turns_query',
    path: turnsResult.path,
    httpStatus: turnsResult.httpStatus,
    code: turnsResult.code,
    msg: turnsResult.msg,
    turnsCount: turnsResult.turns ? turnsResult.turns.length : 0
  });
  if (!turnsResult.ok) {
    return {
      status: 'call_result_query_failed',
      callId,
      callStatus: statusResult.status,
      debug,
      vox: turnsResult,
      message: formatCallResultQueryFailedMessage(callId, `通话已结束，但查询通话内容失败：${turnsResult.msg || turnsResult.code || 'unknown'}`, debug)
    };
  }

  return {
    status: 'call_result',
    callId,
    callStatus: 'completed',
    turns: turnsResult.turns,
    transcript: turnsResult.transcript,
    debug,
    message: formatCallResultMessage(callId, turnsResult, debug)
  };
}

function extractCallId(prompt = '') {
  const value = String(prompt || '');
  const labeled = value.match(/callId\s*[：:=]\s*([0-9a-fA-F-]{16,})/i);
  if (labeled) return labeled[1];
  const uuid = value.match(/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/);
  return uuid ? uuid[0] : '';
}

function isCallResultQuery(prompt = '', options = {}) {
  if (options.queryCallResult || options.callId) return true;
  return /查询|查看|获取|通话内容|通话记录|通话结果|状态|结果/.test(String(prompt || ''));
}

function formatPendingCallResultMessage(callId, status, debug = []) {
  const meaning = status === 'started'
    ? '通话仍在进行中，请挂断后稍等一会儿再查询。'
    : 'Vox 暂未查到这通电话的完成记录，请稍后再试。';
  return [
    '暂时还没有可返回的通话内容。',
    '',
    `- callId：${callId}`,
    `- 当前状态：${status}`,
    `- 说明：${meaning}`,
    '',
    formatCallResultDebug(debug)
  ].join('\n');
}

function formatCallResultMessage(callId, turnsResult, debug = []) {
  const transcriptText = turnsResult.transcript.length
    ? turnsResult.transcript.map((item) => {
      const speaker = item.role === 'assistant' ? 'Bot' : '用户';
      return `${item.turnIndex}. ${speaker}：${item.text}`;
    }).join('\n')
    : '无通话文本。';
  return [
    '已获取通话内容。',
    '',
    `- callId：${callId}`,
    `- 轮次数：${turnsResult.turns.length}`,
    '',
    formatCallResultDebug(debug),
    '',
    transcriptText
  ].join('\n');
}

function formatCallResultQueryFailedMessage(callId, reason, debug = []) {
  return [
    reason,
    '',
    `- callId：${callId}`,
    '',
    formatCallResultDebug(debug)
  ].join('\n');
}

function formatCallResultDebug(debug = []) {
  if (!debug.length) return '调试信息：暂无。';
  const lines = debug.map((item) => {
    if (item.step === 'status_query') {
      return `- 状态查询 #${item.attempt}：path=${item.path} http=${item.httpStatus} code=${item.code} status=${item.status} msg=${item.msg || ''}`;
    }
    if (item.step === 'turns_query') {
      return `- 内容查询：path=${item.path} http=${item.httpStatus} code=${item.code} turns=${item.turnsCount} msg=${item.msg || ''}`;
    }
    return `- ${item.step}`;
  });
  return ['调试信息：', ...lines].join('\n');
}

function formatResultMessage({ result, intent, agentProfile, requestId, credentials = {}, trialState = null }) {
  if (result.ok) {
    const data = result.body && result.body.data ? result.body.data : {};
    return appendRegistrationGuide([
      '已发起 Vox 自定义 Bot 外呼。',
      '',
      `- 被叫号码：${maskPhone(intent.callee)}`,
      `- Bot 角色：${agentProfile.role}`,
      `- 任务目标：${agentProfile.goals}`,
      `- requestId：${data.requestId || requestId}`,
      data.callId ? `- callId：${data.callId}` : '',
      `- 状态：${data.status || 'accepted'}`,
      data.callId ? '提示：挂断后可回复“查询通话内容 callId：' + data.callId + '”获取通话记录。' : ''
    ].filter(Boolean).join('\n'), credentials, trialState);
  }

  const body = result.body || {};
  return appendRegistrationGuide([
    '外呼发起失败。',
    '',
    `- HTTP 状态：${result.httpStatus}`,
    `- code：${body.code === undefined ? 'unknown' : body.code}`,
    `- msg：${body.msg || body.raw || 'unknown'}`,
    `- requestId：${requestId}`
  ].join('\n'), credentials, trialState);
}

function formatAcceptedWithCallResultMessage({ result, intent, agentProfile, requestId, credentials = {}, trialState = null, callResult }) {
  const base = formatResultMessage({ result, intent, agentProfile, requestId, credentials, trialState });
  if (!callResult || callResult.status !== 'completed') {
    return [
      base,
      '',
      '通话结果：',
      callResult ? callResult.summary : '未获取到通话结果。',
      '',
      formatCallResultDebug(callResult ? callResult.debug : [])
    ].join('\n');
  }

  const transcriptText = callResult.transcript.length
    ? callResult.transcript.map((item) => {
      const speaker = item.role === 'assistant' ? 'Bot' : '用户';
      return `${item.turnIndex}. ${speaker}：${item.text}`;
    }).join('\n')
    : '无通话文本。';
  const analysis = callResult.analysis || {};
  return [
    base,
    '',
    '通话已结束，已获取通话内容。',
    '',
    `- callId：${callResult.callId}`,
    `- 轮次数：${callResult.turns ? callResult.turns.length : 0}`,
    `- 用户回复轮数：${analysis.userReplyCount || 0}`,
    `- 是否确认：${analysis.confirmed ? '是' : '否'}`,
    `- 是否建议人工跟进：${analysis.needsHumanFollowUp ? '是' : '否'}`,
    '',
    '简单总结：',
    analysis.summary || callResult.summary || '暂无总结。',
    '',
    formatCallResultDebug(callResult.debug || []),
    '',
    '通话内容：',
    transcriptText
  ].join('\n');
}

function appendRegistrationGuide(message, credentials = {}, trialState = null) {
  if (!credentials.trialMode) return message;
  const usage = formatTrialUsage(trialState);
  const guide = buildRegistrationGuide(credentials, trialState);
  return [
    message,
    '',
    usage,
    `正式使用可注册 Vox 企业账号：${guide.registerUrl}`
  ].filter(Boolean).join('\n');
}

function buildRegistrationGuide(credentials = {}, trialState = null) {
  return {
    title: '正式使用建议',
    callToAction: '如果你希望继续使用电话 Bot，请现在注册 Vox 企业账号。',
    registerUrl: credentials.registerUrl || 'https://vox-ai.teddymobile.cn/trial/apply',
    benefits: '注册后你将获得：专属 VOX_APP_ID / VOX_SECRET、正式外呼额度、企业权限、号码资源和生产接入支持。',
    switchInstruction: '完成注册后，把新的 VOX_APP_ID / VOX_SECRET 替换当前试用配置，即可切换为正式账号。',
    trialUsage: formatTrialUsage(trialState)
  };
}

function enrichTrialState(trialState = null, registrationGuide = null) {
  if (!trialState || !registrationGuide) return trialState;
  return {
    ...trialState,
    usageText: formatTrialUsage(trialState),
    usageTextWithRegistration: formatTrialUsageWithRegistration(trialState, registrationGuide.registerUrl),
    nextStep: registrationGuide.callToAction,
    registerUrl: registrationGuide.registerUrl,
    registrationActionText: `注册正式账号：${registrationGuide.registerUrl}`,
    choicesText: `请选择下一步：[注册正式账号] ${registrationGuide.registerUrl} ｜ [继续试用] ｜ [我已有正式凭证]`
  };
}

function buildRegistrationFields(registrationGuide = null) {
  if (!registrationGuide) {
    return {
      registrationRequired: false,
      registrationTitle: '',
      registrationMessage: '',
      registrationUrl: '',
      registrationBenefits: '',
      registrationSwitchInstruction: '',
      display: null
    };
  }
  const registrationMessage = [
    registrationGuide.title,
    registrationGuide.callToAction,
    `注册入口：${registrationGuide.registerUrl}`,
    registrationGuide.benefits,
    registrationGuide.switchInstruction
  ].join('\n');
  const actions = buildRegistrationActions(registrationGuide);
  return {
    registrationRequired: true,
    registrationTitle: registrationGuide.title,
    registrationMessage,
    registrationUrl: registrationGuide.registerUrl,
    registrationBenefits: registrationGuide.benefits,
    registrationSwitchInstruction: registrationGuide.switchInstruction,
    actions,
    buttons: actions,
    quickReplies: actions,
    suggestedActions: actions,
    choices: actions,
    actionPrompt: '请选择下一步：注册正式账号，或继续使用剩余试用额度。',
    display: {
      registrationGuide: registrationMessage,
      actionPrompt: '请选择下一步：注册正式账号，或继续使用剩余试用额度。',
      actions,
      buttons: actions,
      nextStep: registrationGuide.callToAction,
      registrationUrl: registrationGuide.registerUrl
    }
  };
}

function buildRegistrationActions(registrationGuide = {}) {
  return [
    {
      id: 'register_formal_account',
      type: 'url',
      label: '注册正式账号',
      title: '注册正式账号',
      description: '获取专属 VOX_APP_ID / VOX_SECRET、正式额度、企业权限和号码资源。',
      url: registrationGuide.registerUrl || 'https://vox-ai.teddymobile.cn/trial/apply',
      value: '正式注册'
    },
    {
      id: 'continue_trial',
      type: 'reply',
      label: '继续试用',
      title: '继续试用',
      description: '继续使用当前推广试用额度体验电话 Bot。',
      value: '继续试用'
    },
    {
      id: 'setup_formal_credentials',
      type: 'reply',
      label: '我已有正式凭证',
      title: '我已有正式凭证',
      description: '切换为正式账号模式，并配置专属 VOX_APP_ID / VOX_SECRET。',
      value: '我已有正式凭证'
    }
  ];
}

function buildVoiceChoiceFields(intent = {}) {
  return {
    voiceOptions: VOICE_OPTIONS,
    voiceChoices: VOICE_OPTIONS,
    voiceButtons: VOICE_OPTIONS.map((option) => ({
      id: option.id,
      type: 'reply',
      label: option.label,
      title: option.label,
      description: option.description,
      value: option.value
    })),
    actionPrompt: '请选择 Bot 音色（完整 5 种）：',
    display: {
      actionPrompt: '请选择 Bot 音色（完整 5 种）：',
      voiceOptions: VOICE_OPTIONS,
      voiceButtons: VOICE_OPTIONS.map((option) => ({
        id: option.id,
        type: 'reply',
        label: option.label,
        description: option.description,
        value: option.value
      })),
      scenario: intent.scenario || ''
    }
  };
}

function buildBusinessContextFields(businessContext = {}) {
  return {
    businessContextRequired: true,
    businessContextQuestion: businessContext.question || '',
    businessContextScenario: businessContext.scenario || 'generic',
    businessContextMissing: businessContext.missing || [],
    businessContextSuggestedFields: businessContext.suggestedFields || [],
    actionPrompt: businessContext.question || '请补充更具体的业务背景。',
    display: {
      actionPrompt: businessContext.question || '请补充更具体的业务背景。',
      businessContext
    }
  };
}

function appendTrialAwareness(message, credentials = {}, trialState = null) {
  if (!credentials.trialMode) return message;
  const usage = formatTrialUsage(trialState);
  return [
    '当前为推广试用模式。',
    usage,
    '',
    message
  ].filter(Boolean).join('\n');
}

module.exports = {
  handlePrompt,
  mergeIntent,
  parsePromptToIntent,
  checkCompleteness,
  checkSafety,
  buildAgentProfile,
  chooseVoiceType,
  buildOutboundPayload,
  formatResultMessage,
  appendRegistrationGuide,
  appendTrialAwareness,
  buildRegistrationGuide,
  buildRegistrationFields,
  buildRegistrationActions,
  buildVoiceChoiceFields,
  buildBusinessContextFields
};
