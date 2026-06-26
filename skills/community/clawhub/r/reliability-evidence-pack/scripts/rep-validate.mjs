#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

// v1.0 Required Artifacts (per rep-spec-v1.0.md)
const REQUIRED_TYPES = [
  'decision_rejection_log',
  'memory_reconstruction_audit',
  'handoff_acceptance_packet',
  'near_miss_reliability_trailer',
  'signed_divergence_violation_record',
];

// v1.0 Recommended Artifacts (optional but supported in v1.0)
const RECOMMENDED_TYPES = [
  'agent_heartbeat_record',
  'context_snapshot',
  'claim_file',
  // v1.0 additions (previously in LEGACY, now promoted)
  'error_recovery_log',
  'performance_baseline',
  'model_switch_event',
];

// Legacy v0.x types (supported for backward compatibility, not required in v1.0)
const LEGACY_TYPES = [
  // v0.5 types
  'session_context_loss_record',
  'tool_execution_failure_record',
  'security_policy_violation',
  // v0.6 types (Capability Evolution) - NOT promoted to v1.0
  'capability_degradation_record',
  'evolution_recommendation_accepted',
  'evolution_cycle_record',
];

// All supported types (union of v1.0 + legacy)
const ALL_SUPPORTED_TYPES = [...REQUIRED_TYPES, ...RECOMMENDED_TYPES, ...LEGACY_TYPES];

const TYPE_ALIASES = {
  decision_rejection_log: [
    'decision_rejection_log',
    'decision_log',
    'rejection_log',
    'decision_rejection',
  ],
  memory_reconstruction_audit: [
    'memory_reconstruction_audit',
    'memory_audit',
    'reconstruction_audit',
    'memory_recon_audit',
  ],
  handoff_acceptance_packet: [
    'handoff_acceptance_packet',
    'handoff_packet',
    'handoff_acceptance',
    'handoff',
  ],
  near_miss_reliability_trailer: [
    'near_miss_reliability_trailer',
    'near_miss',
    'incident',
    'incident_report',
  ],
  signed_divergence_violation_record: [
    'signed_divergence_violation_record',
    'signed_divergence_record',
    'divergence_violation_record',
    'violation_record',
    'signed_divergence',
  ],
  // Claim-File Pattern - production safety documentation
  claim_file: [
    'claim_file',
    'claim',
    'safety_claim',
    'change_claim',
  ],
  // v0.2: Agent heartbeat for long-running agents
  agent_heartbeat_record: [
    'agent_heartbeat_record',
    'heartbeat',
    'hb',
    'agent_hb',
    'health_check',
  ],
  // v0.2: Context snapshot at decision points
  context_snapshot: [
    'context_snapshot',
    'ctx_snapshot',
    'context',
    'snapshot',
    'state_capture',
  ],
  // v1.0: Error recovery log (promoted from v0.3)
  error_recovery_log: [
    'error_recovery_log',
    'error_recovery',
    'recovery_log',
    'err_rec',
  ],
  // v1.0: Performance baseline (promoted from v0.3)
  performance_baseline: [
    'performance_baseline',
    'perf_baseline',
    'baseline',
    'perf',
  ],
  // v1.0: Model switch event (promoted from v0.4)
  model_switch_event: [
    'model_switch_event',
    'model_switch',
    'switch_event',
    'model_change',
  ],
  // v0.5: Session context loss record
  session_context_loss_record: [
    'session_context_loss_record',
    'context_loss',
    'scl',
  ],
  // v0.5: Tool execution failure record
  tool_execution_failure_record: [
    'tool_execution_failure_record',
    'tool_failure',
    'tef',
  ],
  // v0.5: Security policy violation
  security_policy_violation: [
    'security_policy_violation',
    'security_violation',
    'spv',
  ],
  // v0.6: Capability Degradation Record
  capability_degradation_record: [
    'capability_degradation_record',
    'degradation',
    'cap_degradation',
    'cdr',
  ],
  // v0.6: Evolution Recommendation Accepted
  evolution_recommendation_accepted: [
    'evolution_recommendation_accepted',
    'evo_rec_accept',
    'era',
  ],
  // v0.6: Evolution Cycle Record
  evolution_cycle_record: [
    'evolution_cycle_record',
    'evo_cycle',
    'ecr',
  ],
};

const SHA256_RE = /^sha256:[a-f0-9]{8,}$/i;

function usage() {
  console.log(`REP validator (v0.1 schemas)\n\nUsage:\n  node scripts/rep-validate.mjs <input.json|input.jsonl|-> [options]\n\nOptions:\n  --type <artifact_type>   Force artifact type for all records\n  --json                   Emit JSON output\n  --jsonl                  Parse input as JSONL\n  --require-pack           Fail if one or more required REP artifact types are missing\n  --check-chain            Validate prev_hash chain across input order
  --schema-only            Only validate JSON schema (no chain, xref, or pack validation)
  --xref                   Validate cross-artifact references exist in bundle
  --verify-hash            Verify content_hash matches computed SHA256
  --dedup                  Check for duplicate artifact_id values\n\nExamples:\n  node scripts/rep-validate.mjs artifacts/decision_rejection_log.jsonl --jsonl\n  node scripts/rep-validate.mjs rep-bundle.json --require-pack --check-chain --xref\n  cat artifacts.jsonl | node scripts/rep-validate.mjs - --jsonl --json\n`);
}

function parseArgs(argv) {
  const args = {
    input: null,
    forcedType: null,
    json: false,
    jsonl: false,
    schemaOnly: false,
    requirePack: false,
    checkChain: false,
    xref: false,
    verifyHash: false,
    dedup: false,
  };

  for (let i = 2; i < argv.length; i += 1) {
    const token = argv[i];

    if (!args.input && !token.startsWith('--')) {
      args.input = token;
      continue;
    }

    if (token === '--type') {
      args.forcedType = argv[i + 1];
      i += 1;
      continue;
    }
    if (token === '--json') {
      args.json = true;
      continue;
    }
    if (token === '--jsonl') {
      args.jsonl = true;
      continue;
    }
    if (token === '--schema-only') {
      args.schemaOnly = true;
      continue;
    }
    if (token === '--require-pack') {
      args.requirePack = true;
      continue;
    }
    if (token === '--check-chain') {
      args.checkChain = true;
      continue;
    }
    if (token === '--xref') {
      args.xref = true;
      continue;
    }
    if (token === '--verify-hash') {
      args.verifyHash = true;
      continue;
    }
    if (token === '--dedup') {
      args.dedup = true;
      continue;
    }
    if (token === '-h' || token === '--help') {
      usage();
      process.exit(0);
    }

    throw new Error(`Unknown argument: ${token}`);
  }

  if (!args.input) {
    usage();
    process.exit(2);
  }

  return args;
}

function readInput(inputPath) {
  if (inputPath === '-') return fs.readFileSync(0, 'utf8');
  return fs.readFileSync(path.resolve(inputPath), 'utf8');
}

function parseInput(raw, args) {
  const parseAsJsonl = args.jsonl || (args.input !== '-' && args.input.toLowerCase().endsWith('.jsonl'));
  if (parseAsJsonl) {
    const items = [];
    const errors = [];
    const lines = raw.split(/\r?\n/);
    lines.forEach((line, idx) => {
      const trimmed = line.trim();
      if (!trimmed) return;
      try {
        items.push(JSON.parse(trimmed));
      } catch (err) {
        errors.push({ line: idx + 1, message: err.message });
      }
    });
    return { items, parseErrors: errors, sourceFormat: 'jsonl' };
  }

  const parsed = JSON.parse(raw);
  return {
    items: Array.isArray(parsed) ? parsed : [parsed],
    parseErrors: [],
    sourceFormat: 'json',
  };
}

function isObject(v) {
  return typeof v === 'object' && v !== null && !Array.isArray(v);
}

function asString(v) {
  return typeof v === 'string' ? v.trim() : '';
}

function hasValue(v) {
  return !(v === undefined || v === null || (typeof v === 'string' && v.trim() === ''));
}

function get(obj, keys) {
  for (const k of keys) {
    if (Object.hasOwn(obj, k) && obj[k] !== undefined) return obj[k];
  }
  return undefined;
}

/**
 * Get value from either top-level or content wrapper.
 * This handles both flat schemas (v1.0) and content-wrapped schemas.
 * Returns { value, found, source } where source is 'top' or 'content'.
 */
function getFromContent(obj, ...keys) {
  // First check top-level
  for (const k of keys) {
    if (Object.hasOwn(obj, k) && obj[k] !== undefined) {
      return { value: obj[k], found: true, source: 'top' };
    }
  }
  // Then check content wrapper
  if (obj.content && typeof obj.content === 'object') {
    for (const k of keys) {
      if (Object.hasOwn(obj.content, k) && obj.content[k] !== undefined) {
        return { value: obj.content[k], found: true, source: 'content' };
      }
    }
  }
  return { value: undefined, found: false, source: 'none' };
}

/**
 * Add a reason with optional hint about content wrapper format.
 */
function pushWithHint(reasons, fieldName, message, foundInContent = false) {
  if (foundInContent) {
    reasons.push(`${message} (hint: found in 'content.${fieldName}', validator expects top-level or v1.0 flat schema)`);
  } else {
    reasons.push(message);
  }
}

function isValidTimestamp(v) {
  return hasValue(v) && !Number.isNaN(Date.parse(String(v)));
}

function normalizeType(rawType) {
  const t = asString(rawType).toLowerCase();
  if (!t) return { normalized: '', canonical: false };

  for (const [canonical, aliases] of Object.entries(TYPE_ALIASES)) {
    if (aliases.includes(t)) {
      return { normalized: canonical, canonical: t === canonical };
    }
  }

  return { normalized: t, canonical: false };
}

const VALID_VERSIONS = ['1.0'];

function validateEnvelope(obj, reasons, warnings) {
  const repVersion = get(obj, ['rep_version']);
  const artifactType = get(obj, ['artifact_type', 'type', 'artifactType']);
  const artifactId = get(obj, ['artifact_id', 'id', 'event_id']);
  const sessionId = get(obj, ['session_id']);
  const interactionId = get(obj, ['interaction_id']);
  const createdAt = get(obj, ['created_at', 'timestamp', 'ts', 'occurred_at', 'time']);
  const actor = get(obj, ['actor']);
  const contentHash = get(obj, ['content_hash']);
  const prevHash = get(obj, ['prev_hash']);

  if (!hasValue(repVersion)) {
    reasons.push('Missing required field: rep_version');
  } else if (!VALID_VERSIONS.includes(String(repVersion))) {
    warnings.push(`Non-standard rep_version: ${String(repVersion)} (expected ${VALID_VERSIONS.join(' or ')})`);
  }

  if (!asString(artifactType)) reasons.push('Missing required field: artifact_type');
  if (!asString(artifactId)) reasons.push('Missing required field: artifact_id');
  if (!asString(sessionId)) reasons.push('Missing required field: session_id');
  if (!asString(interactionId)) reasons.push('Missing required field: interaction_id');

  if (!isValidTimestamp(createdAt)) {
    reasons.push('created_at must be a valid RFC3339 timestamp');
  }

  if (!isObject(actor)) {
    reasons.push('actor must be an object with {id, role}');
  } else {
    if (!asString(actor.id)) reasons.push('actor.id is required');
    const role = asString(actor.role);
    if (!['agent', 'human', 'system'].includes(role)) {
      reasons.push('actor.role must be one of: agent|human|system');
    }
  }

  if (!asString(contentHash) || !SHA256_RE.test(String(contentHash))) {
    reasons.push('content_hash must match /^sha256:[a-f0-9]{8,}$/');
  }

  if (!(prevHash === null || (typeof prevHash === 'string' && SHA256_RE.test(prevHash)))) {
    reasons.push('prev_hash must be null or match /^sha256:[a-f0-9]{8,}$/');
  }

  return normalizeType(artifactType);
}

function validateDecisionRejectionLog(obj, reasons) {
  // Use getFromContent to check both top-level and content wrapper
  const decisionResult = getFromContent(obj, 'decision');
  const actionClassResult = getFromContent(obj, 'action_class', 'action');
  const targetRefResult = getFromContent(obj, 'target_ref', 'target');
  const criteriaResult = getFromContent(obj, 'criteria');
  const rejectionCodesResult = getFromContent(obj, 'rejection_codes');
  const rationaleResult = getFromContent(obj, 'rationale');
  const reviewerResult = getFromContent(obj, 'reviewer');
  const finalizedAtResult = getFromContent(obj, 'finalized_at');

  const decision = asString(decisionResult.value);
  const actionClass = asString(actionClassResult.value);
  const targetRef = asString(targetRefResult.value);
  const criteria = criteriaResult.found && Array.isArray(criteriaResult.value) ? criteriaResult.value : [];
  const rejectionCodes = rejectionCodesResult.found && Array.isArray(rejectionCodesResult.value) ? rejectionCodesResult.value : [];
  const rationale = asString(rationaleResult.value);

  if (!decisionResult.found) {
    pushWithHint(reasons, 'decision', 'decision is required', decisionResult.source === 'content');
  } else if (!['approve', 'reject', 'defer'].includes(decision)) {
    reasons.push('decision must be one of: approve|reject|defer');
  }
  
  if (!actionClassResult.found) {
    pushWithHint(reasons, 'action_class', 'action_class is required', actionClassResult.source === 'content');
  } else if (!['post', 'reply', 'memory_write', 'external_call', 'handoff'].includes(actionClass)) {
    reasons.push('action_class must be one of: post|reply|memory_write|external_call|handoff');
  }
  
  if (!targetRefResult.found) {
    pushWithHint(reasons, 'target_ref', 'target_ref is required', targetRefResult.source === 'content');
  }

  if (!criteriaResult.found || !Array.isArray(criteriaResult.value) || criteria.length === 0) {
    pushWithHint(reasons, 'criteria', 'criteria must be a non-empty array', criteriaResult.source === 'content');
  } else {
    criteria.forEach((c, idx) => {
      if (!isObject(c)) {
        reasons.push(`criteria[${idx}] must be an object`);
        return;
      }
      if (!asString(c.name)) reasons.push(`criteria[${idx}].name is required`);
      if (!['pass', 'fail'].includes(asString(c.result))) {
        reasons.push(`criteria[${idx}].result must be pass|fail`);
      }
    });
  }

  if (['external_call', 'post'].includes(actionClass) && criteria.length < 2) {
    reasons.push('criteria must contain at least 2 items for external_call or post');
  }

  if (decision === 'reject' && rejectionCodes.length < 1) {
    reasons.push('rejection_codes must include at least one code when decision=reject');
  }

  if (!rationaleResult.found) {
    pushWithHint(reasons, 'rationale', 'rationale is required', rationaleResult.source === 'content');
  } else if (rationale.length > 500) {
    reasons.push('rationale exceeds 500 characters');
  }

  if (!reviewerResult.found) {
    pushWithHint(reasons, 'reviewer', 'reviewer is required', reviewerResult.source === 'content');
  }
  
  if (!finalizedAtResult.found) {
    pushWithHint(reasons, 'finalized_at', 'finalized_at is required', finalizedAtResult.source === 'content');
  } else if (!isValidTimestamp(finalizedAtResult.value)) {
    reasons.push('finalized_at must be a valid timestamp');
  }
}

function validateMemoryReconstructionAudit(obj, reasons) {
  // Check both top-level and content wrapper
  const claimRefResult = getFromContent(obj, 'claim_ref');
  if (!claimRefResult.found) reasons.push('claim_ref is required');

  // source_items - can be simple strings or objects
  let sourceItems = [];
  const sourceItemsResult = getFromContent(obj, 'source_items');
  if (sourceItemsResult.found && Array.isArray(sourceItemsResult.value)) {
    sourceItems = sourceItemsResult.value;
  }
  if (sourceItems.length < 1) {
    reasons.push('source_items must contain at least one item');
  } else {
    // Allow both string items and object items
    sourceItems.forEach((item, idx) => {
      if (typeof item === 'string') {
        // Simple string format is OK - just log as info
        return;
      }
      if (!isObject(item)) {
        reasons.push(`source_items[${idx}] must be a string or object`);
        return;
      }
      // Object format validation (optional fields)
      if (item.source_id && !asString(item.source_id)) {
        reasons.push(`source_items[${idx}].source_id must be a string`);
      }
      if (item.hash && !SHA256_RE.test(String(item.hash))) {
        reasons.push(`source_items[${idx}].hash should match sha256: prefix`);
      }
    });
  }

  // reconstruction_steps - can be simple strings or objects
  let steps = [];
  const stepsResult = getFromContent(obj, 'reconstruction_steps');
  if (stepsResult.found && Array.isArray(stepsResult.value)) {
    steps = stepsResult.value;
  }
  if (steps.length < 1) {
    reasons.push('reconstruction_steps must contain at least one step');
  } else {
    const allowedOps = new Set(['retrieve', 'filter', 'summarize', 'compare', 'search', 'verify']);
    steps.forEach((step, idx) => {
      if (typeof step === 'string') {
        // Simple string format is OK
        return;
      }
      if (!isObject(step)) {
        reasons.push(`reconstruction_steps[${idx}] must be a string or object`);
        return;
      }
      // Object format validation (optional)
      if (step.step !== undefined && (!Number.isInteger(step.step) || step.step < 1)) {
        reasons.push(`reconstruction_steps[${idx}].step should be integer >= 1`);
      }
      if (step.operation && !allowedOps.has(asString(step.operation))) {
        reasons.push(`reconstruction_steps[${idx}].operation should be retrieve|filter|summarize|compare|search|verify`);
      }
    });
  }

  // consistency_score
  const scoreResult = getFromContent(obj, 'consistency_score');
  let score = 0;
  if (!scoreResult.found) {
    reasons.push('consistency_score is required');
  } else {
    score = Number(scoreResult.value);
    if (!Number.isFinite(score) || score < 0 || score > 1) {
      reasons.push('consistency_score must be numeric in [0,1]');
    }
  }

  // missing_context - can be array or string
  let missingContext = [];
  const missingContextResult = getFromContent(obj, 'missing_context');
  if (missingContextResult.found) {
    if (Array.isArray(missingContextResult.value)) {
      missingContext = missingContextResult.value;
    } else if (typeof missingContextResult.value === 'string' && missingContextResult.value.trim()) {
      missingContext = [missingContextResult.value]; // Convert single string to array
    }
  }

  // audit_outcome - also accept verified_with_notes
  const outcomeResult = getFromContent(obj, 'audit_outcome');
  if (!outcomeResult.found) {
    reasons.push('audit_outcome is required');
  } else if (!['verified', 'partially_verified', 'failed', 'verified_with_notes'].includes(outcomeResult.value)) {
    reasons.push('audit_outcome must be verified|partially_verified|failed|verified_with_notes');
  }

  // auditor
  const auditorResult = getFromContent(obj, 'auditor');
  if (!auditorResult.found) reasons.push('auditor is required');

  // audited_at
  const auditedAtResult = getFromContent(obj, 'audited_at', 'created_at', 'timestamp');
  if (!auditedAtResult.found) {
    reasons.push('audited_at is required');
  } else if (!isValidTimestamp(auditedAtResult.value)) {
    reasons.push('audited_at must be a valid timestamp');
  }

  if (outcomeResult.value === 'verified' && scoreResult.found) {
    if (!(Number.isFinite(score) && score >= 0.85)) {
      reasons.push('audit_outcome=verified requires consistency_score >= 0.85');
    }
    if (missingContext.length > 0) {
      reasons.push('audit_outcome=verified requires missing_context to be empty');
    }
  }
}

function validateHandoffAcceptancePacket(obj, reasons) {
  // Check both top-level and content wrapper
  const handoffIdResult = getFromContent(obj, 'handoff_id');
  if (!handoffIdResult.found) reasons.push('handoff_id is required');

  const fromActorResult = getFromContent(obj, 'from_actor');
  if (!fromActorResult.found) reasons.push('from_actor is required');

  const toActorResult = getFromContent(obj, 'to_actor');
  if (!toActorResult.found) reasons.push('to_actor is required');

  const taskSummaryResult = getFromContent(obj, 'task_summary');
  if (!taskSummaryResult.found) {
    reasons.push('task_summary is required');
  } else if (taskSummaryResult.value.length > 300) {
    reasons.push('task_summary exceeds 300 characters');
  }

  // acceptance_criteria - check both locations
  let criteria = [];
  const criteriaResult = getFromContent(obj, 'acceptance_criteria');
  if (criteriaResult.found && Array.isArray(criteriaResult.value)) {
    criteria = criteriaResult.value;
  }
  if (criteria.length < 1) reasons.push('acceptance_criteria must contain at least one item');

  // SLA - can be object or simple string duration
  const slaResult = getFromContent(obj, 'sla');
  let sla = null;
  let slaObj = null;
  
  if (slaResult.found) {
    if (typeof slaResult.value === 'object' && slaResult.value !== null) {
      slaObj = slaResult.value; // Full SLA object
    } else if (typeof slaResult.value === 'string') {
      // Simple string like "5m" - convert to object format for compatibility
      slaObj = { duration: slaResult.value }; // Accept as valid shorthand
    }
  }
  
  if (!slaObj) {
    reasons.push('sla object is required (or string duration like "5m")');
  } else if (typeof slaObj === 'object') {
    // Only validate object fields if it's actually an object
    const ackBy = slaObj.ack_by;
    const firstUpdateBy = slaObj.first_update_by;
    const deliverBy = slaObj.deliver_by;

    if (ackBy && !isValidTimestamp(ackBy)) reasons.push('sla.ack_by must be a valid timestamp');
    if (firstUpdateBy && !isValidTimestamp(firstUpdateBy)) reasons.push('sla.first_update_by must be a valid timestamp');
    if (deliverBy && !isValidTimestamp(deliverBy)) reasons.push('sla.deliver_by must be a valid timestamp');

    if (ackBy && firstUpdateBy && deliverBy && isValidTimestamp(ackBy) && isValidTimestamp(firstUpdateBy) && isValidTimestamp(deliverBy)) {
      const a = Date.parse(String(ackBy));
      const f = Date.parse(String(firstUpdateBy));
      const d = Date.parse(String(deliverBy));
      if (!(a <= f && f <= d)) {
        reasons.push('SLA timestamps must satisfy ack_by <= first_update_by <= deliver_by');
      }
    }

    if (slaObj.severity && !['low', 'med', 'high', 'critical'].includes(asString(slaObj.severity))) {
      reasons.push('sla.severity must be low|med|high|critical');
    }
  }

  const acceptanceStatusResult = getFromContent(obj, 'acceptance_status');
  if (!acceptanceStatusResult.found) {
    reasons.push('acceptance_status is required');
  } else if (!['accepted', 'rejected', 'accepted_with_conditions'].includes(acceptanceStatusResult.value)) {
    reasons.push('acceptance_status must be accepted|rejected|accepted_with_conditions');
  }

  const acceptedAtResult = getFromContent(obj, 'accepted_at');
  if (acceptanceStatusResult.value !== 'rejected' && !acceptedAtResult.found) {
    reasons.push('accepted_at is required unless acceptance_status=rejected');
  } else if (acceptedAtResult.found && !isValidTimestamp(acceptedAtResult.value)) {
    reasons.push('accepted_at must be a valid timestamp');
  }
}

function validateNearMissReliabilityTrailer(obj, reasons) {
  if (!asString(obj.incident_id)) reasons.push('incident_id is required');
  if (!asString(obj.trigger)) reasons.push('trigger is required');
  if (!['misinfo', 'policy_breach', 'privacy_leak', 'operational_delay', 'other'].includes(asString(obj.potential_impact))) {
    reasons.push('potential_impact must be misinfo|policy_breach|privacy_leak|operational_delay|other');
  }
  if (!['rule', 'human_review', 'self_check'].includes(asString(obj.detected_by))) {
    reasons.push('detected_by must be rule|human_review|self_check');
  }

  const ttd = Number(obj.time_to_detect_sec);
  if (!Number.isFinite(ttd) || ttd < 0) reasons.push('time_to_detect_sec must be >= 0');

  if (!asString(obj.containment_action)) reasons.push('containment_action is required');

  const residualRisk = asString(obj.residual_risk);
  if (!['low', 'med', 'high'].includes(residualRisk)) reasons.push('residual_risk must be low|med|high');

  const corrective = Array.isArray(obj.corrective_actions) ? obj.corrective_actions : [];
  if (corrective.length < 1) reasons.push('corrective_actions must contain at least one item');

  if (!asString(obj.owner)) reasons.push('owner is required');

  if (residualRisk === 'low' && !isValidTimestamp(obj.closed_at)) {
    reasons.push('closed_at is required when residual_risk=low');
  }

  if (obj.closed_at !== null && obj.closed_at !== undefined && !isValidTimestamp(obj.closed_at)) {
    reasons.push('closed_at must be null or a valid timestamp');
  }
}

function validateSignedDivergenceViolationRecord(obj, reasons) {
  if (!asString(obj.record_id)) reasons.push('record_id is required');
  if (!asString(obj.baseline_ref)) reasons.push('baseline_ref is required');
  if (!asString(obj.observed_behavior)) reasons.push('observed_behavior is required');

  if (!['process', 'safety', 'security', 'sla', 'data_integrity'].includes(asString(obj.divergence_class))) {
    reasons.push('divergence_class must be process|safety|security|sla|data_integrity');
  }

  const severity = asString(obj.severity);
  if (!['S1', 'S2', 'S3', 'S4'].includes(severity)) reasons.push('severity must be S1|S2|S3|S4');

  const evidenceRefs = Array.isArray(obj.evidence_refs) ? obj.evidence_refs : [];
  if (evidenceRefs.length < 1) reasons.push('evidence_refs must contain at least one item');

  const disposition = asString(obj.disposition);
  if (!['waived', 'remediated', 'open'].includes(disposition)) {
    reasons.push('disposition must be waived|remediated|open');
  }

  if (disposition === 'remediated' && !asString(obj.remediation_plan)) {
    reasons.push('remediation_plan is required when disposition=remediated');
  }

  const signatures = Array.isArray(obj.signatures) ? obj.signatures : [];
  if (signatures.length < 1) reasons.push('signatures must contain at least one signature');

  let hasReviewer = false;
  signatures.forEach((sig, idx) => {
    if (!isObject(sig)) {
      reasons.push(`signatures[${idx}] must be an object`);
      return;
    }
    if (!asString(sig.signer_id)) reasons.push(`signatures[${idx}].signer_id is required`);
    const role = asString(sig.role);
    if (!['owner', 'reviewer'].includes(role)) {
      reasons.push(`signatures[${idx}].role must be owner|reviewer`);
    }
    if (role === 'reviewer') hasReviewer = true;
    if (!isValidTimestamp(sig.signed_at)) reasons.push(`signatures[${idx}].signed_at must be valid timestamp`);
    if (!asString(sig.sig)) reasons.push(`signatures[${idx}].sig is required`);
  });

  if (['S1', 'S2'].includes(severity)) {
    if (signatures.length < 2) reasons.push(`severity=${severity} requires at least 2 signatures`);
    if (!hasReviewer) reasons.push(`severity=${severity} requires at least one reviewer signature`);
  }
}

function validateClaimFile(obj, reasons) {
  // Claim-File Pattern - production safety documentation
  // Note: claim_id is optional; artifact_id serves as the primary identifier
  
  // Check both top-level and content wrapper
  const claimSummaryResult = getFromContent(obj, 'change_summary');
  if (!claimSummaryResult.found) {
    reasons.push('change_summary is required');
  } else if (claimSummaryResult.value.length > 500) {
    reasons.push('change_summary exceeds 500 characters');
  }

  let expectedFiles = [];
  const expectedFilesResult = getFromContent(obj, 'expected_files');
  if (expectedFilesResult.found && Array.isArray(expectedFilesResult.value)) {
    expectedFiles = expectedFilesResult.value;
  }
  if (expectedFiles.length < 1) reasons.push('expected_files must contain at least one item');

  let nonExpectedAreas = [];
  const nonExpectedAreasResult = getFromContent(obj, 'non_expected_areas');
  if (nonExpectedAreasResult.found && Array.isArray(nonExpectedAreasResult.value)) {
    nonExpectedAreas = nonExpectedAreasResult.value;
  }
  if (nonExpectedAreas.length < 1) reasons.push('non_expected_areas must contain at least one item');

  const rollbackMethodResult = getFromContent(obj, 'rollback_method');
  if (!rollbackMethodResult.found) reasons.push('rollback_method is required');

  // Status - also accept 'completed' as alias for 'verified'
  const statusResult = getFromContent(obj, 'status');
  if (!statusResult.found) {
    reasons.push('status is required');
  } else if (!['pending_review', 'approved', 'rejected', 'verified', 'failed', 'completed'].includes(statusResult.value)) {
    reasons.push('status must be pending_review|approved|rejected|verified|failed|completed');
  }

  // Risk level
  const riskLevelResult = getFromContent(obj, 'risk_level');
  if (!riskLevelResult.found) {
    reasons.push('risk_level is required');
  } else if (!['low', 'medium', 'high', 'critical'].includes(riskLevelResult.value)) {
    reasons.push('risk_level must be low|medium|high|critical');
  }

  // PR number is optional but if present should be valid format
  const prNumberResult = getFromContent(obj, 'pr_number');
  if (prNumberResult.found && !/^#?\d+$/.test(String(prNumberResult.value))) {
    reasons.push('pr_number must be numeric');
  }

  // verified_at is required if status is verified
  if (statusResult.value === 'verified' && !isValidTimestamp(getFromContent(obj, 'verified_at').value)) {
    reasons.push('verified_at is required when status=verified');
  }
}

// v0.2: Agent heartbeat for long-running agents
function validateAgentHeartbeatRecord(obj, reasons) {
  // Use helper to check both top-level and content wrapper
  const statusResult = getFromContent(obj, 'status', 'agent_status');
  if (!statusResult.found) {
    reasons.push('status is required (top-level or in content.status)');
  } else if (!['healthy', 'degraded', 'unhealthy', 'restarting', 'stopped'].includes(statusResult.value)) {
    reasons.push('status must be healthy|degraded|unhealthy|restarting|stopped');
  }

  // Check session_id (should be at envelope level, but check content too for compatibility)
  if (!asString(obj.session_id) && !getFromContent(obj, 'session_id').found) {
    reasons.push('session_id is required (envelope level or content.session_id)');
  }
  
  // Actor can be string or object with id
  if (!obj.actor) reasons.push('actor is required');

  // heartbeat_seq - check both locations
  const hbSeqResult = getFromContent(obj, 'heartbeat_seq');
  if (!hbSeqResult.found) reasons.push('heartbeat_seq is required');
  else if (typeof hbSeqResult.value !== 'number') reasons.push('heartbeat_seq must be a number');

  // Accept various memory field formats - check both locations
  const memResult = getFromContent(obj, 'memory_usage_mb');
  if (memResult.found && typeof memResult.value !== 'number') {
    reasons.push('memory_usage_mb must be a number');
  }
  const memUsedResult = getFromContent(obj, 'memory_used_mb');
  if (memUsedResult.found && typeof memUsedResult.value !== 'number') {
    reasons.push('memory_used_mb must be a number');
  }

  // CPU metrics - check both locations
  const cpuResult = getFromContent(obj, 'cpu_percent');
  if (cpuResult.found && (typeof cpuResult.value !== 'number' || cpuResult.value < 0 || cpuResult.value > 100)) {
    reasons.push('cpu_percent must be a number 0-100');
  }

  // Accept various activity timestamp formats - check both locations
  const lastActivityResult = getFromContent(obj, 'last_activity', 'last_activity_at');
  if (!lastActivityResult.found) {
    reasons.push('last_activity is required (top-level or content.last_activity)');
  } else if (!isValidTimestamp(lastActivityResult.value)) {
    reasons.push('last_activity must be valid ISO 8601');
  }

  // Uptime can be uptime_sec or uptime_seconds - check both locations
  const uptimeResult = getFromContent(obj, 'uptime_sec', 'uptime_seconds');
  if (uptimeResult.found && typeof uptimeResult.value !== 'number') {
    reasons.push('uptime_sec must be a number');
  }

  // Tasks arrays - check both locations
  const tasksActiveResult = getFromContent(obj, 'tasks_active');
  if (tasksActiveResult.found && !Array.isArray(tasksActiveResult.value)) {
    reasons.push('tasks_active must be an array');
  }
  const tasksCompletedResult = getFromContent(obj, 'tasks_completed');
  if (tasksCompletedResult.found && typeof tasksCompletedResult.value !== 'number') {
    reasons.push('tasks_completed must be a number');
  }

  // Errors/checks arrays - check both locations
  const errorsResult = getFromContent(obj, 'errors');
  if (errorsResult.found && !Array.isArray(errorsResult.value)) {
    reasons.push('errors must be an array');
  }
  const checksResult = getFromContent(obj, 'checks');
  if (checksResult.found && !Array.isArray(checksResult.value)) {
    reasons.push('checks must be an array');
  }
}

// v0.2: Context snapshot at decision points
function validateContextSnapshot(obj, reasons) {
  // Accept both snapshot_type and trigger field names
  const snapshotType = asString(obj.snapshot_type) || asString(obj.trigger);
  if (!snapshotType) reasons.push('snapshot_type (or trigger) is required');
  
  if (snapshotType && !['pre_decision', 'post_decision', 'handoff', 'checkpoint', 'failure'].includes(snapshotType)) {
    reasons.push('snapshot_type/trigger must be pre_decision|post_decision|handoff|checkpoint|failure');
  }

  // snapshot_id is optional but recommended
  if (!asString(obj.snapshot_id)) reasons.push('snapshot_id is recommended');

  // context_version is optional but recommended for versioning
  if (!asString(obj.context_version)) reasons.push('context_version is recommended');

  // Active memory - core context state
  const activeMemory = obj.active_memory;
  if (!activeMemory) {
    reasons.push('active_memory is required');
  } else if (typeof activeMemory !== 'object') {
    reasons.push('active_memory must be an object');
  } else {
    // Validate active_memory contents
    if (activeMemory.messages_count !== undefined && (!Number.isInteger(activeMemory.messages_count) || activeMemory.messages_count < 0)) {
      reasons.push('active_memory.messages_count must be a non-negative integer');
    }
    if (activeMemory.tokens_approx !== undefined && (!Number.isInteger(activeMemory.tokens_approx) || activeMemory.tokens_approx < 0)) {
      reasons.push('active_memory.tokens_approx must be a non-negative integer');
    }
    if (activeMemory.key_topics !== undefined && !Array.isArray(activeMemory.key_topics)) {
      reasons.push('active_memory.key_topics must be an array');
    }
    if (activeMemory.oldest_message !== undefined && !isValidTimestamp(activeMemory.oldest_message)) {
      reasons.push('active_memory.oldest_message must be a valid timestamp');
    }
  }

  // Decision context - present for decision-related snapshots
  if (snapshotType === 'pre_decision' || snapshotType === 'post_decision') {
    const decisionContext = obj.decision_context;
    if (!decisionContext) {
      reasons.push('decision_context is required for pre_decision/post_decision snapshots');
    } else if (typeof decisionContext !== 'object') {
      reasons.push('decision_context must be an object');
    }
  }

  // Variables - session state variables
  if (obj.variables !== undefined && typeof obj.variables !== 'object') {
    reasons.push('variables must be an object');
  }

  // Attached artifacts - references to related REP artifacts
  if (obj.attached_artifacts !== undefined) {
    if (!Array.isArray(obj.attached_artifacts)) {
      reasons.push('attached_artifacts must be an array');
    } else {
      obj.attached_artifacts.forEach((ref, idx) => {
        if (typeof ref !== 'string') {
          reasons.push(`attached_artifacts[${idx}] must be a string reference`);
        }
      });
    }
  }

  // Snapshot hash for integrity
  if (!asString(obj.snapshot_hash)) reasons.push('snapshot_hash is recommended for integrity');
}

// v0.3: Error recovery log
// Allowed error types (expanded to include common patterns)
const ALLOWED_ERROR_TYPES = [
  'timeout', 'api_error', 'validation_error', 'permission_denied', 'rate_limit', 
  'network_error', 'internal_error', 'unknown',
  // Extended types
  'tool_execution_failure', 'memory_recall_failure', 'execution_error', 
  'resource_exhausted', 'service_unavailable'
];

// Allowed recovery strategies (expanded)
const ALLOWED_RECOVERY_STRATEGIES = [
  'retry', 'fallback', 'skip', 'abort', 'manual_intervention',
  // Extended strategies
  'retry_with_timeout', 'fallback_to_memfile', 'requeue', 'ignore'
];

// Allowed recovery statuses (expanded)
const ALLOWED_RECOVERY_STATUSES = [
  'success', 'failed', 'partial', 'pending',
  // Extended statuses
  'recovered', 'completed', 'abandoned'
];

function validateErrorRecoveryLog(obj, reasons) {
  // Check both top-level and content wrapper
  const errorTypeResult = getFromContent(obj, 'error_type');
  if (!errorTypeResult.found) {
    reasons.push('error_type is required (top-level or content.error_type)');
  } else if (!ALLOWED_ERROR_TYPES.includes(errorTypeResult.value)) {
    reasons.push(`error_type must be one of: ${ALLOWED_ERROR_TYPES.join('|')}`);
  }

  const errorMsgResult = getFromContent(obj, 'error_message');
  if (!errorMsgResult.found) reasons.push('error_message is required (top-level or content.error_message)');

  const recoveryStrategyResult = getFromContent(obj, 'recovery_strategy');
  if (!recoveryStrategyResult.found) {
    reasons.push('recovery_strategy is required (top-level or content.recovery_strategy)');
  } else if (!ALLOWED_RECOVERY_STRATEGIES.includes(recoveryStrategyResult.value)) {
    reasons.push(`recovery_strategy must be one of: ${ALLOWED_RECOVERY_STRATEGIES.join('|')}`);
  }

  const recoveryStatusResult = getFromContent(obj, 'recovery_status');
  if (!recoveryStatusResult.found) {
    reasons.push('recovery_status is required (top-level or content.recovery_status)');
  } else if (!ALLOWED_RECOVERY_STATUSES.includes(recoveryStatusResult.value)) {
    reasons.push(`recovery_status must be one of: ${ALLOWED_RECOVERY_STATUSES.join('|')}`);
  }

  const errorOccurredResult = getFromContent(obj, 'error_occurred_at', 'occurred_at', 'timestamp');
  if (!errorOccurredResult.found) {
    reasons.push('error_occurred_at is required (top-level or content.error_occurred_at)');
  } else if (!isValidTimestamp(errorOccurredResult.value)) {
    reasons.push('error_occurred_at must be a valid ISO 8601 timestamp');
  }
  
  const recoveryAttemptedResult = getFromContent(obj, 'recovery_attempted_at');
  if (recoveryAttemptedResult.found && !isValidTimestamp(recoveryAttemptedResult.value)) {
    reasons.push('recovery_attempted_at must be a valid timestamp');
  }

  const recoveredResult = getFromContent(obj, 'recovered_at');
  if (recoveredResult.found && !isValidTimestamp(recoveredResult.value)) {
    reasons.push('recovered_at must be a valid timestamp');
  }

  // Retry count if retry strategy
  if (recoveryStrategyResult.value === 'retry') {
    const retryCountResult = getFromContent(obj, 'retry_count');
    if (!retryCountResult.found) {
      reasons.push('retry_count is required when recovery_strategy=retry');
    } else {
      const retryCount = Number(retryCountResult.value);
      if (!Number.isInteger(retryCount) || retryCount < 0) {
        reasons.push('retry_count must be a non-negative integer');
      }
    }
  }

  // Error context
  const errorContextResult = getFromContent(obj, 'error_context');
  if (errorContextResult.found && typeof errorContextResult.value !== 'object') {
    reasons.push('error_context must be an object');
  }
}

// v0.3: Performance baseline
function validatePerformanceBaseline(obj, reasons) {
  const baselineType = asString(obj.baseline_type);
  if (!baselineType) reasons.push('baseline_type is required');
  
  if (baselineType && !['cpu', 'memory', 'latency', 'throughput', 'error_rate', 'composite'].includes(baselineType)) {
    reasons.push('baseline_type must be cpu|memory|latency|throughput|error_rate|composite');
  }

  const baselineValue = obj.baseline_value;
  if (baselineValue === undefined) reasons.push('baseline_value is required');
  
  if (baselineValue !== undefined && typeof baselineValue !== 'number') {
    reasons.push('baseline_value must be a number');
  }

  if (!asString(obj.measurement_window)) reasons.push('measurement_window is required');

  const metrics = obj.metrics;
  if (!metrics) {
    reasons.push('metrics object is required');
  } else if (typeof metrics !== 'object') {
    reasons.push('metrics must be an object');
  } else {
    // Validate common metric fields
    if (metrics.sample_count !== undefined && (!Number.isInteger(metrics.sample_count) || metrics.sample_count < 1)) {
      reasons.push('metrics.sample_count must be a positive integer');
    }
    if (metrics.p50 !== undefined && typeof metrics.p50 !== 'number') {
      reasons.push('metrics.p50 must be a number');
    }
    if (metrics.p95 !== undefined && typeof metrics.p95 !== 'number') {
      reasons.push('metrics.p95 must be a number');
    }
    if (metrics.p99 !== undefined && typeof metrics.p99 !== 'number') {
      reasons.push('metrics.p99 must be a number');
    }
  }

  if (!isValidTimestamp(obj.baseline_measured_at)) reasons.push('baseline_measured_at must be a valid timestamp');

  const status = asString(obj.status);
  if (!status) reasons.push('status is required');
  
  if (status && !['active', 'deprecated', 'calibrating'].includes(status)) {
    reasons.push('status must be active|deprecated|calibrating');
  }
}

// v0.4: Model switch event
function validateModelSwitchEvent(obj, reasons) {
  // Check both top-level and content wrapper
  const prevModelResult = getFromContent(obj, 'previous_model', 'from_model');
  if (!prevModelResult.found) reasons.push('previous_model (or from_model) is required');

  const newModelResult = getFromContent(obj, 'new_model', 'to_model');
  if (!newModelResult.found) reasons.push('new_model (or to_model) is required');

  const switchReasonResult = getFromContent(obj, 'switch_reason', 'trigger_reason');
  if (!switchReasonResult.found) {
    reasons.push('switch_reason (or trigger_reason) is required');
  } else if (!['performance', 'cost', 'availability', 'capability', 'manual', 'error_recovery', 'scheduled', 'latency_threshold_exceeded'].includes(switchReasonResult.value)) {
    reasons.push('switch_reason must be performance|cost|availability|capability|manual|error_recovery|scheduled|latency_threshold_exceeded');
  }

  const switchStatusResult = getFromContent(obj, 'switch_status');
  if (!switchStatusResult.found) {
    reasons.push('switch_status is required');
  } else if (!['initiated', 'completed', 'failed', 'rolled_back'].includes(switchStatusResult.value)) {
    reasons.push('switch_status must be initiated|completed|failed|rolled_back');
  }

  const switchInitiatedAtResult = getFromContent(obj, 'switch_initiated_at', 'initiated_at');
  if (!switchInitiatedAtResult.found) {
    reasons.push('switch_initiated_at is required');
  } else if (!isValidTimestamp(switchInitiatedAtResult.value)) {
    reasons.push('switch_initiated_at must be a valid timestamp');
  }

  const switchCompletedAtResult = getFromContent(obj, 'switch_completed_at', 'completed_at');
  if (switchCompletedAtResult.found && !isValidTimestamp(switchCompletedAtResult.value)) {
    reasons.push('switch_completed_at must be a valid timestamp');
  }

  // switch_overhead_ms is optional but if present should be a number
  const switchOverheadResult = getFromContent(obj, 'switch_overhead_ms', 'overhead_ms');
  if (switchOverheadResult.found && typeof switchOverheadResult.value !== 'number') {
    reasons.push('switch_overhead_ms must be a number');
  }

  // context_preserved is optional
  const contextPreservedResult = getFromContent(obj, 'context_preserved');
  if (contextPreservedResult.found && typeof contextPreservedResult.value !== 'boolean') {
    reasons.push('context_preserved must be a boolean');
  }

  // fallback_enabled is optional
  const fallbackEnabledResult = getFromContent(obj, 'fallback_enabled');
  if (fallbackEnabledResult.found && typeof fallbackEnabledResult.value !== 'boolean') {
    reasons.push('fallback_enabled must be a boolean');
  }
}

// v0.5: Session context loss record
function validateSessionContextLossRecord(obj, reasons) {
  // Check both top-level and content wrapper
  const lossIdResult = getFromContent(obj, 'loss_id');
  if (!lossIdResult.found) reasons.push('loss_id is required');

  let lostFields = [];
  const lostFieldsResult = getFromContent(obj, 'lost_fields');
  if (lostFieldsResult.found && Array.isArray(lostFieldsResult.value)) {
    lostFields = lostFieldsResult.value;
  }
  if (lostFields.length < 1) reasons.push('lost_fields must contain at least one field');

  const lossReasonResult = getFromContent(obj, 'loss_reason', 'trigger_reason');
  if (!lossReasonResult.found) {
    reasons.push('loss_reason is required');
  } else if (!['timeout', 'session_expired', 'memory_overflow', 'system_error', 'manual_clear', 'migration', 'truncation', 'max_tokens'].includes(lossReasonResult.value)) {
    reasons.push('loss_reason must be timeout|session_expired|memory_overflow|system_error|manual_clear|migration|truncation|max_tokens');
  }

  const lossOccurredAtResult = getFromContent(obj, 'loss_occurred_at', 'occurred_at', 'timestamp');
  if (!lossOccurredAtResult.found) {
    reasons.push('loss_occurred_at is required');
  } else if (!isValidTimestamp(lossOccurredAtResult.value)) {
    reasons.push('loss_occurred_at must be a valid timestamp');
  }

  const recoveryAttemptedResult = getFromContent(obj, 'recovery_attempted');
  if (!recoveryAttemptedResult.found) {
    reasons.push('recovery_attempted is required');
  } else if (typeof recoveryAttemptedResult.value !== 'boolean') {
    reasons.push('recovery_attempted must be a boolean');
  }

  const impactLevelResult = getFromContent(obj, 'impact_level');
  if (!impactLevelResult.found) {
    reasons.push('impact_level is required');
  } else if (!['low', 'medium', 'high', 'critical'].includes(impactLevelResult.value)) {
    reasons.push('impact_level must be low|medium|high|critical');
  }

  // Recovery result if attempted
  if (recoveryAttemptedResult.value === true) {
    const recoveryResultResult = getFromContent(obj, 'recovery_result', 'recovery_action');
    if (!recoveryResultResult.found) {
      reasons.push('recovery_result is required when recovery_attempted=true');
    }
  }
}

// v0.5: Tool execution failure record
function validateToolExecutionFailureRecord(obj, reasons) {
  // Check both top-level and content wrapper
  const toolNameResult = getFromContent(obj, 'tool_name');
  if (!toolNameResult.found) reasons.push('tool_name is required');

  const errorTypeResult = getFromContent(obj, 'error_type');
  if (!errorTypeResult.found) {
    reasons.push('error_type is required');
  } else if (!['timeout', 'permission_denied', 'invalid_input', 'resource_not_found', 'rate_limit', 'network_error', 'internal_error', 'unknown', 'tool_execution_failure'].includes(errorTypeResult.value)) {
    reasons.push('error_type must be timeout|permission_denied|invalid_input|resource_not_found|rate_limit|network_error|internal_error|unknown|tool_execution_failure');
  }

  const errorMessageResult = getFromContent(obj, 'error_message');
  if (!errorMessageResult.found) reasons.push('error_message is required');

  const failureStatusResult = getFromContent(obj, 'failure_status');
  if (!failureStatusResult.found) {
    reasons.push('failure_status is required');
  } else if (!['failed', 'retry_exhausted', 'aborted', 'fallback_used'].includes(failureStatusResult.value)) {
    reasons.push('failure_status must be failed|retry_exhausted|aborted|fallback_used');
  }

  const executionStartedAtResult = getFromContent(obj, 'execution_started_at', 'started_at', 'initiated_at');
  if (!executionStartedAtResult.found) {
    reasons.push('execution_started_at is required');
  } else if (!isValidTimestamp(executionStartedAtResult.value)) {
    reasons.push('execution_started_at must be a valid timestamp');
  }
  
  const executionFailedAtResult = getFromContent(obj, 'execution_failed_at', 'failed_at', 'timestamp');
  if (!executionFailedAtResult.found) {
    reasons.push('execution_failed_at is required');
  } else if (!isValidTimestamp(executionFailedAtResult.value)) {
    reasons.push('execution_failed_at must be a valid timestamp');
  }

  // Retry count is optional
  const retryCountResult = getFromContent(obj, 'retry_count', 'attempt_count');
  if (retryCountResult.found) {
    const retryCount = Number(retryCountResult.value);
    if (!Number.isInteger(retryCount) || retryCount < 0) {
      reasons.push('retry_count must be a non-negative integer');
    }
  }
}

// v0.5: Security policy violation
function validateSecurityPolicyViolation(obj, reasons) {
  // Check both top-level and content wrapper
  const violationIdResult = getFromContent(obj, 'violation_id');
  if (!violationIdResult.found) reasons.push('violation_id is required');

  const policyNameResult = getFromContent(obj, 'policy_name');
  if (!policyNameResult.found) reasons.push('policy_name is required');

  const severityResult = getFromContent(obj, 'severity');
  if (!severityResult.found) {
    reasons.push('severity is required');
  } else if (!['low', 'medium', 'high', 'critical'].includes(severityResult.value)) {
    reasons.push('severity must be low|medium|high|critical');
  }

  const violationDetailsResult = getFromContent(obj, 'violation_details');
  if (!violationDetailsResult.found) reasons.push('violation_details is required');

  const actionTakenResult = getFromContent(obj, 'action_taken');
  if (!actionTakenResult.found) {
    reasons.push('action_taken is required');
  } else if (!['blocked', 'logged', 'warned', 'quarantined', 'escalated'].includes(actionTakenResult.value)) {
    reasons.push('action_taken must be blocked|logged|warned|quarantined|escalated');
  }

  const violationDetectedAtResult = getFromContent(obj, 'violation_detected_at', 'detected_at', 'timestamp');
  if (!violationDetectedAtResult.found) {
    reasons.push('violation_detected_at is required');
  } else if (!isValidTimestamp(violationDetectedAtResult.value)) {
    reasons.push('violation_detected_at must be a valid timestamp');
  }

  // Source of the violation - also accept 'moltguard'
  const sourceTypeResult = getFromContent(obj, 'source_type');
  if (!sourceTypeResult.found) {
    reasons.push('source_type is required');
  } else if (!['user_input', 'api_call', 'file_access', 'network_request', 'internal', 'moltguard'].includes(sourceTypeResult.value)) {
    reasons.push('source_type must be user_input|api_call|file_access|network_request|internal|moltguard');
  }

  // Violation category/type - also accept command_injection
  const violationTypeResult = getFromContent(obj, 'violation_type', 'category');
  if (violationTypeResult.found && !['data_leak', 'credential_theft', 'command_injection', 'privilege_escalation', 'policy_breach', 'other'].includes(violationTypeResult.value)) {
    reasons.push('violation_type must be data_leak|credential_theft|command_injection|privilege_escalation|policy_breach|other');
  }

  // Remediation - can be string or object
  const remediationResult = getFromContent(obj, 'remediation');
  if (remediationResult.found && typeof remediationResult.value === 'string') {
    // String format is OK - it's the remediation action
  } else if (remediationResult.found && typeof remediationResult.value !== 'object') {
    reasons.push('remediation must be a string or object');
  }
}

// v0.6: Capability degradation record
function validateCapabilityDegradationRecord(obj, reasons) {
  // Check both top-level and content wrapper
  const degradationIdResult = getFromContent(obj, 'degradation_id');
  if (!degradationIdResult.found) reasons.push('degradation_id is required');

  const capabilityNameResult = getFromContent(obj, 'capability_name', 'metric_name');
  if (!capabilityNameResult.found) reasons.push('capability_name (or metric_name) is required');

  // degradation_level can be string (minor/moderate/severe/complete) or number (percentage)
  const degradationLevelResult = getFromContent(obj, 'degradation_level');
  if (!degradationLevelResult.found) {
    reasons.push('degradation_level is required');
  } else {
    const level = degradationLevelResult.value;
    const isStringLevel = typeof level === 'string';
    const isNumberLevel = typeof level === 'number';
    
    if (isStringLevel && !['minor', 'moderate', 'severe', 'complete'].includes(level)) {
      reasons.push('degradation_level must be minor|moderate|severe|complete (or a percentage number)');
    } else if (isNumberLevel && (level < 0 || level > 100)) {
      reasons.push('degradation_level as percentage must be 0-100');
    } else if (!isStringLevel && !isNumberLevel) {
      reasons.push('degradation_level must be string or number');
    }
  }

  const detectedAtResult = getFromContent(obj, 'detected_at', 'created_at', 'timestamp');
  if (!detectedAtResult.found) {
    reasons.push('detected_at is required');
  } else if (!isValidTimestamp(detectedAtResult.value)) {
    reasons.push('detected_at must be a valid timestamp');
  }

  // Affected metrics - check both locations
  let affectedMetrics = [];
  const affectedMetricsResult = getFromContent(obj, 'affected_metrics');
  if (affectedMetricsResult.found && Array.isArray(affectedMetricsResult.value)) {
    affectedMetrics = affectedMetricsResult.value;
  }
  if (affectedMetrics.length < 1) reasons.push('affected_metrics must contain at least one metric');

  // Trend
  const trendResult = getFromContent(obj, 'trend');
  if (trendResult.found && !['improving', 'stable', 'degrading', 'unknown'].includes(trendResult.value)) {
    reasons.push('trend must be improving|stable|degrading|unknown');
  }

  // Recommended action
  const recommendedActionResult = getFromContent(obj, 'recommended_action');
  if (!recommendedActionResult.found) reasons.push('recommended_action is required');

  // Status
  const statusResult = getFromContent(obj, 'status');
  if (!statusResult.found) {
    reasons.push('status is required');
  } else if (!['detected', 'investigating', 'remediating', 'resolved', 'monitoring', 'low', 'medium', 'high', 'critical'].includes(statusResult.value)) {
    reasons.push('status must be detected|investigating|remediating|resolved|monitoring (or low|medium|high|critical)');
  }
}

// v0.6: Evolution recommendation accepted
function validateEvolutionRecommendationAccepted(obj, reasons) {
  if (!asString(obj.recommendation_id)) reasons.push('recommendation_id is required');

  const recommendationType = asString(obj.recommendation_type);
  if (!recommendationType) reasons.push('recommendation_type is required');
  
  if (recommendationType && !['capability_add', 'capability_remove', 'capability_modify', 'parameter_tune', 'model_change', 'workflow_change'].includes(recommendationType)) {
    reasons.push('recommendation_type must be capability_add|capability_remove|capability_modify|parameter_tune|model_change|workflow_change');
  }

  if (!asString(obj.accepted_by)) reasons.push('accepted_by is required');

  if (!isValidTimestamp(obj.accepted_at)) reasons.push('accepted_at must be a valid timestamp');

  // Acceptance rationale
  if (!asString(obj.acceptance_rationale)) reasons.push('acceptance_rationale is required');

  // Priority
  const priority = asString(obj.priority);
  if (priority && !['low', 'medium', 'high', 'critical'].includes(priority)) {
    reasons.push('priority must be low|medium|high|critical');
  }

  // Target timeline
  if (obj.target_implementation_at && !isValidTimestamp(obj.target_implementation_at)) {
    reasons.push('target_implementation_at must be a valid timestamp');
  }

  // Dependencies
  if (obj.dependencies !== undefined && !Array.isArray(obj.dependencies)) {
    reasons.push('dependencies must be an array');
  }

  // Expected impact
  if (obj.expected_impact !== undefined && typeof obj.expected_impact !== 'object') {
    reasons.push('expected_impact must be an object');
  }
}

// v0.6: Evolution cycle record
function validateEvolutionCycleRecord(obj, reasons) {
  if (!asString(obj.cycle_id)) reasons.push('cycle_id is required');

  const cycleType = asString(obj.cycle_type);
  if (!cycleType) reasons.push('cycle_type is required');
  
  if (cycleType && !['capability_assessment', 'parameter_optimization', 'model_evaluation', 'integration_test', 'full_evolution'].includes(cycleType)) {
    reasons.push('cycle_type must be capability_assessment|parameter_optimization|model_evaluation|integration_test|full_evolution');
  }

  const cycleStatus = asString(obj.cycle_status);
  if (!cycleStatus) reasons.push('cycle_status is required');
  
  if (cycleStatus && !['planned', 'running', 'completed', 'failed', 'cancelled'].includes(cycleStatus)) {
    reasons.push('cycle_status must be planned|running|completed|failed|cancelled');
  }

  if (!isValidTimestamp(obj.cycle_started_at)) reasons.push('cycle_started_at is required');

  if (obj.cycle_completed_at && !isValidTimestamp(obj.cycle_completed_at)) {
    reasons.push('cycle_completed_at must be a valid timestamp');
  }

  // Phase information
  const phases = Array.isArray(obj.phases) ? obj.phases : [];
  phases.forEach((phase, idx) => {
    if (!isObject(phase)) {
      reasons.push(`phases[${idx}] must be an object`);
      return;
    }
    if (!asString(phase.name)) reasons.push(`phases[${idx}].name is required`);
    if (!asString(phase.status)) reasons.push(`phases[${idx}].status is required`);
  });

  // Results summary
  if (obj.results_summary !== undefined && typeof obj.results_summary !== 'object') {
    reasons.push('results_summary must be an object');
  }

  // Recommendations generated
  if (obj.recommendations !== undefined && !Array.isArray(obj.recommendations)) {
    reasons.push('recommendations must be an array');
  }

  // Performance delta
  if (obj.performance_delta !== undefined && typeof obj.performance_delta !== 'object') {
    reasons.push('performance_delta must be an object');
  }
}

const VALIDATORS = {
  decision_rejection_log: validateDecisionRejectionLog,
  memory_reconstruction_audit: validateMemoryReconstructionAudit,
  handoff_acceptance_packet: validateHandoffAcceptancePacket,
  near_miss_reliability_trailer: validateNearMissReliabilityTrailer,
  signed_divergence_violation_record: validateSignedDivergenceViolationRecord,
  claim_file: validateClaimFile,
  // v1.0 types
  agent_heartbeat_record: validateAgentHeartbeatRecord,
  context_snapshot: validateContextSnapshot,
  // types (promoted v1.0 from v0.x)
  error_recovery_log: validateErrorRecoveryLog,
  performance_baseline: validatePerformanceBaseline,
  model_switch_event: validateModelSwitchEvent,
  // v0.5 legacy types
  session_context_loss_record: validateSessionContextLossRecord,
  tool_execution_failure_record: validateToolExecutionFailureRecord,
  security_policy_violation: validateSecurityPolicyViolation,
  // v0.6 legacy types (Capability Evolution)
  capability_degradation_record: validateCapabilityDegradationRecord,
  evolution_recommendation_accepted: validateEvolutionRecommendationAccepted,
  evolution_cycle_record: validateEvolutionCycleRecord,
};

function validateItem(item, forcedType) {
  const reasons = [];
  const warnings = [];

  if (!isObject(item)) {
    return {
      ok: false,
      status: 'fail',
      artifact_type: '',
      reasons: ['Item is not a JSON object'],
      warnings,
      content_hash: '',
      prev_hash: null,
    };
  }

  const envelopeType = validateEnvelope(item, reasons, warnings);
  const forced = normalizeType(forcedType);
  const normalized = forced.normalized || envelopeType.normalized;

  if (!normalized || !Object.hasOwn(VALIDATORS, normalized)) {
    reasons.push(
      `Unsupported artifact_type "${forcedType || item.artifact_type || item.type || ''}". Supported: ${Object.keys(VALIDATORS).join(', ')}`
    );
  } else {
    if (!envelopeType.canonical && !forcedType) {
      warnings.push(`Non-canonical artifact_type alias used: ${String(item.artifact_type || item.type || '')}`);
    }
    VALIDATORS[normalized](item, reasons);
  }

  const status = reasons.length > 0 ? 'fail' : warnings.length > 0 ? 'pass_with_warnings' : 'pass';

  return {
    ok: reasons.length === 0,
    status,
    artifact_type: normalized,
    reasons,
    warnings,
    content_hash: item.content_hash,
    prev_hash: item.prev_hash,
    created_at: item.created_at || item.timestamp || item.ts || item.occurred_at || item.time,
  };
}

function validatePackCompleteness(results) {
  const present = new Set(results.filter((r) => r.ok).map((r) => r.artifact_type));
  return REQUIRED_TYPES.filter((t) => !present.has(t));
}

function validateChain(results) {
  const issues = [];
  for (let i = 0; i < results.length; i += 1) {
    const r = results[i];
    if (!r.ok) continue;
    if (i === 0) continue;

    const prev = results[i - 1];
    if (!prev.ok) continue;

    if (r.prev_hash !== prev.content_hash) {
      issues.push(`Chain mismatch at index ${i}: prev_hash=${String(r.prev_hash)} expected ${String(prev.content_hash)}`);
    }
  }
  return issues;
}

// Compute SHA256 hex string from canonical JSON (sorted keys)
function computeHash(obj) {
  const canonical = JSON.stringify(obj, Object.keys(obj).sort());
  const crypto = require('node:crypto');
  return 'sha256:' + crypto.createHash('sha256').update(canonical).digest('hex').substring(0, 64);
}

function validateXref(items) {
  const issues = [];
  // Build index of all valid artifact_ids
  const validIds = new Set(items.map((item) => item.artifact_id).filter(Boolean));
  
  items.forEach((item, idx) => {
    if (!item.ok) return;
    
    // Check evidence_refs in signed_divergence_violation_record
    if (item.artifact_type === 'signed_divergence_violation_record' && Array.isArray(item.evidence_refs)) {
      item.evidence_refs.forEach((ref) => {
        if (!validIds.has(ref)) {
          issues.push(`XREF at index ${idx}: evidence_ref "${ref}" not found in bundle`);
        }
      });
    }
    
    // Check target_ref in decision_rejection_log
    if (item.artifact_type === 'decision_rejection_log' && item.target_ref) {
      // target_ref can be URLs, message IDs, etc. - only flag if it looks like an artifact ref
      const refMatch = String(item.target_ref).match(/^(artifact|dec|mem|ho|nm|div)-/);
      if (refMatch && !validIds.has(item.target_ref)) {
        // Not necessarily an error - target_ref might be external
      }
    }
    
    // Check artifacts_provided in handoff_acceptance_packet
    if (item.artifact_type === 'handoff_acceptance_packet' && Array.isArray(item.artifacts_provided)) {
      item.artifacts_provided.forEach((ref) => {
        // Format: "decision:dec-001" or just artifact_id
        const actualRef = ref.includes(':') ? ref.split(':')[1] : ref;
        if (!validIds.has(actualRef)) {
          issues.push(`XREF at index ${idx}: artifacts_provided "${ref}" not found in bundle`);
        }
      });
    }
  });
  
  return issues;
}

function validateHash(items) {
  const issues = [];
  items.forEach((item, idx) => {
    if (!item.ok) return;
    if (!item.content_hash || !item.content_hash.startsWith('sha256:')) return;
    
    const computed = computeHash(item);
    // Remove computed hash from comparison (it's based on content_hash field being present)
    const itemCopy = { ...item };
    delete itemCopy.content_hash;
    const computedClean = computeHash(itemCopy);
    
    // The stored hash is supposed to be hash of content without the hash field itself
    // For now, we verify the hash format is correct; actual content verification requires
    // storing the hash of the content separately or computing it before adding content_hash
    if (item.content_hash !== computed && item.content_hash !== computedClean) {
      // For v0.1, we just warn - actual hash verification requires workflow changes
      issues.push(`HASH_VERIFY at index ${idx}: content_hash "${item.content_hash}" does not match computed hash (format check only in v0.1)`);
    }
  });
  return issues;
}

function validateDedup(items) {
  const issues = [];
  const idCounts = {};
  
  items.forEach((item) => {
    if (!item.artifact_id) return;
    idCounts[item.artifact_id] = (idCounts[item.artifact_id] || 0) + 1;
  });
  
  Object.entries(idCounts).forEach(([id, count]) => {
    if (count > 1) {
      issues.push(`DUPLICATE artifact_id: "${id}" appears ${count} times`);
    }
  });
  
  return issues;
}

function printTextReport(results, summary, parseErrors, packMissing, chainIssues, xrefIssues, hashIssues, dedupIssues) {
  if (parseErrors.length > 0) {
    parseErrors.forEach((e) => {
      console.log(`PARSE_ERROR line=${e.line} ${e.message}`);
    });
  }

  results.forEach((r, idx) => {
    console.log(`${r.status.toUpperCase()} [${idx}] type=${r.artifact_type || 'unknown'}`);
    r.reasons.forEach((reason) => console.log(`  - ${reason}`));
    r.warnings.forEach((warning) => console.log(`  * ${warning}`));
  });

  if (packMissing.length > 0) {
    console.log('PACK_MISSING:');
    packMissing.forEach((t) => console.log(`  - ${t}`));
  }
  if (chainIssues.length > 0) {
    console.log('CHAIN_ISSUES:');
    chainIssues.forEach((issue) => console.log(`  - ${issue}`));
  }
  if (xrefIssues && xrefIssues.length > 0) {
    console.log('XREF_ISSUES:');
    xrefIssues.forEach((issue) => console.log(`  - ${issue}`));
  }
  if (hashIssues && hashIssues.length > 0) {
    console.log('HASH_ISSUES:');
    hashIssues.forEach((issue) => console.log(`  - ${issue}`));
  }
  if (dedupIssues && dedupIssues.length > 0) {
    console.log('DEDUP_ISSUES:');
    dedupIssues.forEach((issue) => console.log(`  - ${issue}`));
  }

  console.log(`\nSummary: ${summary.passed}/${summary.total} passed (${summary.passWithWarnings} with warnings), ${summary.failed} failed`);
}

function main() {
  try {
    const args = parseArgs(process.argv);
    const raw = readInput(args.input);
    const parsed = parseInput(raw, args);

    const results = parsed.items.map((item) => validateItem(item, args.forcedType));

    const summary = {
      total: results.length,
      passed: results.filter((r) => r.status === 'pass').length,
      passWithWarnings: results.filter((r) => r.status === 'pass_with_warnings').length,
      failed: results.filter((r) => r.status === 'fail').length,
      parseErrors: parsed.parseErrors.length,
    };

    // schema-only mode: skip pack, chain, xref, hash, and dedup validation
    const isSchemaOnly = args.schemaOnly;
    const packMissing = isSchemaOnly ? [] : (args.requirePack ? validatePackCompleteness(results) : []);
    const chainIssues = isSchemaOnly ? [] : (args.checkChain ? validateChain(results) : []);
    const xrefIssues = isSchemaOnly ? [] : (args.xref ? validateXref(parsed.items) : []);
    const hashIssues = isSchemaOnly ? [] : (args.verifyHash ? validateHash(parsed.items) : []);
    const dedupIssues = isSchemaOnly ? [] : (args.dedup ? validateDedup(parsed.items) : []);

    const failed = summary.failed > 0 || summary.parseErrors > 0 || packMissing.length > 0 || chainIssues.length > 0 || xrefIssues.length > 0 || hashIssues.length > 0 || dedupIssues.length > 0;

    if (args.json) {
      console.log(
        JSON.stringify(
          {
            sourceFormat: parsed.sourceFormat,
            summary,
            requiredTypes: REQUIRED_TYPES,
            packMissing,
            chainIssues,
            xrefIssues,
            hashIssues,
            dedupIssues,
            parseErrors: parsed.parseErrors,
            results,
          },
          null,
          2
        )
      );
    } else {
      printTextReport(results, summary, parsed.parseErrors, packMissing, chainIssues, xrefIssues, hashIssues, dedupIssues);
    }

    process.exit(failed ? 1 : 0);
  } catch (err) {
    console.error(`ERROR: ${err.message}`);
    process.exit(2);
  }
}

main();
