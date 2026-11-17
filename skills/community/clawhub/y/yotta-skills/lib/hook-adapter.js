'use strict';

const crypto = require('crypto');
const fs = require('fs');
const os = require('os');
const path = require('path');

const EVENTS = [
  'before_start',
  'before_tool',
  'before_install',
  'before_publish',
  'after_milestone',
  'before_send',
];

const CAPABILITY_LEVELS = [
  'native-block',
  'native-audit',
  'wrapper-only',
  'unsupported',
];

const EVIDENCE_KINDS = [
  'tool_call_id',
  'hook_event_id',
  'host_transcript',
  'file_path',
  'exit_code',
  'audit_log',
];

const FALLBACKS = ['wrapper', 'advisory', 'explicit-unverified'];

const CODEX_CAPABILITIES = {
  before_start: 'native-audit',
  before_tool: 'native-audit',
  before_install: 'wrapper-only',
  before_publish: 'wrapper-only',
  after_milestone: 'native-audit',
  before_send: 'unsupported',
};

function unsupportedCapabilities() {
  return EVENTS.reduce((out, event) => {
    out[event] = 'unsupported';
    return out;
  }, {});
}

function capabilitiesForHost(host) {
  if (host === 'codex') return { ...CODEX_CAPABILITIES };
  return unsupportedCapabilities();
}

function validateHookRequirements(manifest) {
  const errors = [];
  const requirements = manifest && Array.isArray(manifest.hooks) ? manifest.hooks : [];
  requirements.forEach((requirement, index) => {
    const prefix = 'hooks[' + index + ']';
    if (!requirement || typeof requirement !== 'object' || Array.isArray(requirement)) {
      errors.push(prefix + ': 必须是对象');
      return;
    }
    if (!EVENTS.includes(requirement.event)) {
      errors.push(prefix + ': event 非法');
    }
    if (!['block', 'warn'].includes(requirement.on_fail)) {
      errors.push(prefix + ': on_fail 非法');
    }
    if (!requirement.require_tool && !requirement.require_action) {
      errors.push(prefix + ': 必须声明 require_tool 或 require_action');
    }
    if (!Array.isArray(requirement.evidence) || requirement.evidence.length === 0) {
      errors.push(prefix + ': evidence 不能为空');
    } else if (requirement.evidence.some((kind) => !EVIDENCE_KINDS.includes(kind))) {
      errors.push(prefix + ': evidence 含不支持的来源');
    }
    if (requirement.fallback !== undefined && !FALLBACKS.includes(requirement.fallback)) {
      errors.push(prefix + ': fallback 非法');
    }
  });
  return { errors, requirements };
}

function actionOf(requirement, index) {
  return requirement.require_tool || requirement.require_action || ('hook-' + index);
}

function checkFor(context, requirement) {
  const key = requirement.require_tool || requirement.require_action;
  return context && context.checks && context.checks[key] ? context.checks[key] : null;
}

function evidenceFor(requirement, context, check) {
  const out = {};
  for (const kind of requirement.evidence || []) {
    if (check && check.evidence && check.evidence[kind] !== undefined) out[kind] = check.evidence[kind];
    else if (context && context.evidence && context.evidence[kind] !== undefined) out[kind] = context.evidence[kind];
  }
  return out;
}

function evaluateOne(requirement, index, event, capability, context, skill) {
  const action = actionOf(requirement, index);
  const check = checkFor(context, requirement);
  const evidence = evidenceFor(requirement, context, check);
  const hasEvidence = Object.keys(evidence).length > 0;
  const passed = !!check && check.ok === true;
  const failed = !!check && check.ok === false;
  const missing = !check;
  let decision = 'allow';
  let reason = '检查通过';
  let correction = false;

  if (passed) {
    const canVerify = capability === 'native-block'
      || capability === 'native-audit'
      || (capability === 'wrapper-only' && context && context.wrapperRegistered === true);
    if (!canVerify) {
      decision = 'unverified';
      reason = hasEvidence ? '宿主能力不足，不能声明为强制' : '缺少可验证证据';
    } else if (!hasEvidence) {
      decision = 'unverified';
      reason = '缺少声明要求的可验证证据';
    }
  } else if (failed || missing) {
    if (requirement.on_fail === 'warn') {
      decision = 'warn';
      reason = '检查未通过，按声明降级为警告';
    } else if (capability === 'native-block') {
      decision = 'block';
      reason = '检查未通过，宿主支持动作前阻断';
    } else if (capability === 'wrapper-only') {
      if (context && context.wrapperRegistered === true) {
        decision = 'block';
        reason = '检查未通过，wrapper 路径可阻断';
      } else {
        decision = 'unverified';
        reason = 'wrapper 未注册，无法保证拦截';
      }
    } else if (capability === 'native-audit') {
      decision = 'unverified';
      correction = true;
      reason = '动作已发生，只能审计并触发一次纠偏';
    } else {
      decision = 'unverified';
      reason = '宿主不支持该事件，按 explicit-unverified 降级';
    }
  }

  return {
    event,
    skill: skill || null,
    action,
    capability,
    decision,
    passed,
    failed,
    missing,
    correction,
    evidence,
    reason,
    requirement,
  };
}

function evaluateHook(input) {
  const opts = input || {};
  const event = opts.event;
  const context = opts.context || {};
  const manifest = opts.manifest || {};
  const capabilities = opts.capabilities || capabilitiesForHost(opts.host || 'generic');
  if (!EVENTS.includes(event)) {
    return {
      decision: 'block',
      verified: false,
      correction: false,
      results: [],
      evidence: [],
      user_message: '阻断：未知 hook 事件 ' + event,
      errors: ['未知 hook 事件: ' + event],
    };
  }

  const validation = validateHookRequirements(manifest);
  if (validation.errors.length > 0) {
    return {
      decision: 'block',
      verified: false,
      correction: false,
      results: [],
      evidence: [],
      user_message: '阻断：manifest hook 声明非法',
      errors: validation.errors,
    };
  }

  const requirements = validation.requirements.filter((requirement) => requirement.event === event);
  const results = requirements.map((requirement, index) => evaluateOne(
    requirement,
    index,
    event,
    capabilities[event] || 'unsupported',
    context,
    manifest.slug,
  ));
  const decision = results.some((result) => result.decision === 'block')
    ? 'block'
    : results.some((result) => result.decision === 'warn')
      ? 'warn'
      : results.some((result) => result.decision === 'unverified')
        ? 'unverified'
        : 'allow';
  const evidence = results.map((result) => ({
    event: result.event,
    skill: result.skill,
    action: result.action,
    result: result.decision,
    capability: result.capability,
    evidence: result.evidence,
    reason: result.reason,
  }));
  const correction = results.some((result) => result.correction);
  const verified = decision === 'allow' && results.every((result) => result.decision === 'allow');
  let userMessage = '已通过';
  if (decision === 'block') userMessage = '阻断：' + results.filter((result) => result.decision === 'block').map((result) => result.reason).join('；');
  else if (decision === 'warn') userMessage = '警告：' + results.filter((result) => result.decision === 'warn').map((result) => result.reason).join('；');
  else if (decision === 'unverified') userMessage = 'explicit-unverified：' + results.filter((result) => result.decision === 'unverified').map((result) => result.reason).join('；');

  return {
    decision,
    verified,
    correction,
    results,
    evidence,
    user_message: userMessage,
    errors: [],
  };
}

function hookLogPath(homeDir) {
  return path.join(homeDir || os.homedir(), '.yottaskills', 'hook-log.jsonl');
}

function bindingsPath(homeDir) {
  return path.join(homeDir || os.homedir(), '.yottaskills', 'hook-bindings.json');
}

function appendHookEvidence(entry, options) {
  const file = hookLogPath(options && options.homeDir);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const record = {
    ...entry,
    timestamp: entry.timestamp || new Date().toISOString(),
  };
  fs.appendFileSync(file, JSON.stringify(record) + '\n', 'utf8');
  return file;
}

function emptyBindings() {
  return { version: 1, bindings: {} };
}

function readBindings(homeDir) {
  try {
    const parsed = JSON.parse(fs.readFileSync(bindingsPath(homeDir), 'utf8'));
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed) || !parsed.bindings) return emptyBindings();
    return { version: 1, bindings: { ...parsed.bindings } };
  } catch (_) {
    return emptyBindings();
  }
}

function writeBindings(homeDir, value) {
  const file = bindingsPath(homeDir);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const tmp = file + '.tmp-' + process.pid + '-' + Date.now();
  fs.writeFileSync(tmp, JSON.stringify(value, null, 2) + '\n', 'utf8');
  try {
    fs.renameSync(tmp, file);
  } catch (_) {
    fs.rmSync(file, { force: true });
    fs.renameSync(tmp, file);
  }
  return file;
}

function bindingId(host, skill, event, action) {
  return crypto.createHash('sha256').update([host, skill, event, action].join('|')).digest('hex').slice(0, 24);
}

function bindHookRequirements(input) {
  const opts = input || {};
  const manifest = opts.manifest || {};
  const validation = validateHookRequirements(manifest);
  if (validation.errors.length > 0) {
    const error = new Error(validation.errors.join('; '));
    error.errors = validation.errors;
    throw error;
  }
  const capabilities = capabilitiesForHost(opts.host || 'generic');
  const selected = opts.event
    ? validation.requirements.filter((requirement) => requirement.event === opts.event)
    : validation.requirements;
  const registry = readBindings(opts.homeDir);
  const records = selected.map((requirement, index) => {
    const action = actionOf(requirement, index);
    const id = bindingId(opts.host || 'generic', manifest.slug, requirement.event, action);
    const previous = registry.bindings[id];
    const record = {
      id,
      host: opts.host || 'generic',
      skill: manifest.slug,
      event: requirement.event,
      action,
      on_fail: requirement.on_fail,
      fallback: requirement.fallback || 'explicit-unverified',
      capability: capabilities[requirement.event] || 'unsupported',
      created_at: previous ? previous.created_at : new Date().toISOString(),
    };
    registry.bindings[id] = record;
    return record;
  });
  writeBindings(opts.homeDir, registry);
  return records;
}

function listHookBindings(homeDir) {
  return Object.values(readBindings(homeDir).bindings)
    .sort((a, b) => String(a.created_at).localeCompare(String(b.created_at)) || a.id.localeCompare(b.id));
}

function unbindHookBinding(id, options) {
  const registry = readBindings(options && options.homeDir);
  if (!registry.bindings[id]) return false;
  delete registry.bindings[id];
  writeBindings(options && options.homeDir, registry);
  return true;
}

function createHookAdapter(options) {
  const opts = options || {};
  const host = opts.host || 'generic';
  const capabilities = capabilitiesForHost(host);
  return {
    host,
    capabilities: () => ({ ...capabilities }),
    validate: (manifest) => validateHookRequirements(manifest),
    evaluate: (event, manifest, context) => evaluateHook({
      host,
      event,
      manifest,
      context,
      capabilities,
    }),
    bind: (manifest, event) => bindHookRequirements({
      host,
      homeDir: opts.homeDir,
      manifest,
      event,
    }),
    unbind: (id) => unbindHookBinding(id, { homeDir: opts.homeDir }),
    listBindings: () => listHookBindings(opts.homeDir),
  };
}

module.exports = {
  EVENTS,
  CAPABILITY_LEVELS,
  EVIDENCE_KINDS,
  FALLBACKS,
  CODEX_CAPABILITIES,
  appendHookEvidence,
  bindHookRequirements,
  bindingId,
  bindingsPath,
  capabilitiesForHost,
  createHookAdapter,
  evaluateHook,
  hookLogPath,
  listHookBindings,
  unbindHookBinding,
  validateHookRequirements,
};
