#!/usr/bin/env node
/**
 * REP v0.1 Bundle Generator
 * Generates realistic REP artifact bundles for testing and demos
 * 
 * Usage: node scripts/rep-generate-bundle.mjs [options]
 * 
 * Options:
 *   --count <n>      Number of artifact sets to generate (default: 1)
 *   --valid-only     Only generate valid artifacts
 *   --invalid-only   Only generate invalid artifacts (for testing validators)
 *   --mixed          Generate mix of valid/invalid (default)
 *   --output <path>  Output file path (default: stdout as JSONL)
 *   --json           Output as JSON array
 */

import { writeFileSync } from 'node:fs';

const ARTIFACT_TYPES = [
  'decision_rejection_log',
  'memory_reconstruction_audit', 
  'handoff_acceptance_packet',
  'near_miss_reliability_trailer',
  'signed_divergence_violation_record'
];

function generateUUID() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
    const r = Math.random() * 16 | 0;
    return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
  });
}

function generateHash() {
  return 'sha256:' + Array.from({ length: 64 }, () => 
    Math.floor(Math.random() * 16).toString(16)
  ).join('');
}

function randomChoice(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function generateEnvelope(sessionId, interactionId, artifactType) {
  return {
    rep_version: '0.1',
    artifact_type: artifactType,
    artifact_id: generateUUID(),
    session_id: sessionId,
    interaction_id: interactionId,
    created_at: new Date().toISOString(),
    actor: {
      id: `agent:${randomChoice(['ops', 'writer', 'reviewer', 'auditor'])}`,
      role: 'agent'
    },
    content_hash: generateHash(),
    prev_hash: null // Caller should chain this
  };
}

function generateDecision(valid = true) {
  const sessionId = generateUUID();
  const interactionId = generateUUID();
  const base = generateEnvelope(sessionId, interactionId, 'decision_rejection_log');
  
  const decision = valid ? randomChoice(['approve', 'reject']) : 'reject';
  const criteria = [
    { name: 'safety', result: 'pass', note: 'no policy hit' },
    { name: 'evidence', result: 'pass', note: 'sources present' }
  ];
  
  const artifact = {
    ...base,
    decision,
    action_class: randomChoice(['post', 'reply', 'external_call', 'handoff']),
    target_ref: `msg:${Math.floor(Math.random() * 100000)}`,
    criteria,
    rejection_codes: decision === 'reject' ? [randomChoice(['POLICY_RISK', 'EVIDENCE_GAP', 'SAFETY_CONCERN'])] : [],
    rationale: 'Standard review completed.',
    reviewer: 'agent:reviewer',
    finalized_at: new Date().toISOString()
  };
  
  // Make invalid: missing rejection codes on reject
  if (!valid && decision === 'reject') {
    artifact.rejection_codes = [];
  }
  
  return artifact;
}

function generateMemoryAudit(valid = true) {
  const sessionId = generateUUID();
  const interactionId = generateUUID();
  const base = generateEnvelope(sessionId, interactionId, 'memory_reconstruction_audit');
  
  const score = valid ? 0.92 : 0.65;
  
  const artifact = {
    ...base,
    claim_ref: `claim-${Math.floor(Math.random() * 1000)}`,
    source_items: [
      { source_id: `doc:spec-${Math.floor(Math.random() * 10)}`, hash: generateHash() }
    ],
    reconstruction_steps: [
      { step: 1, operation: 'retrieve', output_ref: 'out-1' }
    ],
    consistency_score: score,
    missing_context: valid ? [] : ['prior_conversation'],
    audit_outcome: valid ? 'verified' : 'partially_verified',
    auditor: 'agent:auditor',
    audited_at: new Date().toISOString()
  };
  
  return artifact;
}

function generateHandoff(valid = true) {
  const sessionId = generateUUID();
  const interactionId = generateUUID();
  const base = generateEnvelope(sessionId, interactionId, 'handoff_acceptance_packet');
  
  const now = new Date();
  const ackBy = new Date(now.getTime() + 5 * 60000);
  const firstUpdateBy = new Date(now.getTime() + 15 * 60000);
  const deliverBy = new Date(now.getTime() + 60 * 60000);
  
  const artifact = {
    ...base,
    handoff_id: `ho-${Date.now()}`,
    from_actor: 'agent:writer',
    to_actor: 'agent:reviewer',
    task_summary: 'Validate REP evidence completeness for campaign thread.',
    acceptance_criteria: ['All 5 artifacts present', 'Hashes verify'],
    artifacts_provided: ['decision:dec-001', 'audit:mem-001'],
    risks: [{ risk: 'late ack', mitigation: 'page on-call' }],
    sla: {
      ack_by: ackBy.toISOString(),
      first_update_by: firstUpdateBy.toISOString(),
      deliver_by: deliverBy.toISOString(),
      severity: 'high'
    },
    acceptance_status: 'accepted',
    acceptance_note: 'Ready',
    accepted_at: new Date().toISOString()
  };
  
  // Make invalid: broken SLA monotonicity
  if (!valid) {
    artifact.sla.first_update_by = new Date(now.getTime() + 2 * 60000).toISOString(); // Before ack_by
  }
  
  return artifact;
}

function generateNearMiss(valid = true) {
  const sessionId = generateUUID();
  const interactionId = generateUUID();
  const base = generateEnvelope(sessionId, interactionId, 'near_miss_reliability_trailer');
  
  const artifact = {
    ...base,
    incident_id: `inc-${Math.floor(Math.random() * 1000)}`,
    trigger: 'missing source detected pre-send',
    potential_impact: 'misinfo',
    detected_by: randomChoice(['rule', 'human_review', 'self_check']),
    time_to_detect_sec: Math.floor(Math.random() * 30),
    containment_action: 'blocked send',
    residual_risk: valid ? 'low' : 'med',
    corrective_actions: valid ? ['add source gate'] : [],
    owner: 'agent:ops',
    closed_at: valid ? new Date().toISOString() : null
  };
  
  return artifact;
}

function generateDivergence(valid = true) {
  const sessionId = generateUUID();
  const interactionId = generateUUID();
  const base = generateEnvelope(sessionId, interactionId, 'signed_divergence_violation_record');
  
  const now = new Date();
  const severity = valid ? 'S2' : 'S1';
  
  const signatures = [
    { signer_id: 'agent:owner', role: 'owner', signed_at: now.toISOString(), sig: 'sig:abc' }
  ];
  
  // Make invalid: S1 requires reviewer signature
  if (!valid && severity === 'S1') {
    // Only owner signature, missing reviewer
  } else {
    signatures.push({ signer_id: 'human:kailong', role: 'reviewer', signed_at: now.toISOString(), sig: 'sig:def' });
  }
  
  const artifact = {
    ...base,
    record_id: `div-${Math.floor(Math.random() * 1000)}`,
    baseline_ref: 'policy:review-required',
    observed_behavior: 'Draft posted before reviewer sign-off.',
    divergence_class: 'process',
    severity,
    evidence_refs: ['dec-001', 'nm-001'],
    disposition: 'remediated',
    remediation_plan: 'Enforce publish lock until signature.',
    signatures
  };
  
  return artifact;
}

function generateArtifactSet(valid = true) {
  return [
    generateDecision(valid),
    generateMemoryAudit(valid),
    generateHandoff(valid),
    generateNearMiss(valid),
    generateDivergence(valid)
  ];
}

// CLI
const args = process.argv.slice(2);
let count = 1;
let mode = 'mixed';
let outputPath = null;
let jsonOutput = false;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--count' && args[i + 1]) {
    count = parseInt(args[i + 1], 10);
    i++;
  } else if (args[i] === '--valid-only') {
    mode = 'valid';
  } else if (args[i] === '--invalid-only') {
    mode = 'invalid';
  } else if (args[i] === '--mixed') {
    mode = 'mixed';
  } else if (args[i] === '--output' && args[i + 1]) {
    outputPath = args[i + 1];
    i++;
  } else if (args[i] === '--json') {
    jsonOutput = true;
  }
}

const artifacts = [];
for (let i = 0; i < count; i++) {
  let isValid = true;
  if (mode === 'mixed') {
    isValid = Math.random() > 0.3;
  } else if (mode === 'invalid') {
    isValid = false;
  }
  artifacts.push(...generateArtifactSet(isValid));
}

// Chain prev_hash
for (let i = 1; i < artifacts.length; i++) {
  artifacts[i].prev_hash = artifacts[i - 1].content_hash;
}

const output = jsonOutput ? JSON.stringify(artifacts, null, 2) : artifacts.map(a => JSON.stringify(a)).join('\n');

if (outputPath) {
  writeFileSync(outputPath, output);
  console.error(`Wrote ${artifacts.length} artifacts to ${outputPath}`);
} else {
  console.log(output);
}
