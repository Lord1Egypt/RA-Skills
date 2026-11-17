'use strict';

const path = require('path');
const { familyById } = require('./capabilities');

function round(value) {
  return Math.round(value * 100);
}

function skillSummary(skill) {
  return {
    name: skill.name,
    description: skill.description,
    path: skill.path,
    agent: skill.agent,
    scope: skill.scope,
    origins: skill.origins,
  };
}

function evidenceAssessment(comparison) {
  const evidence = comparison.evidence;
  const curated = Boolean(evidence.sharedCapabilities?.length || evidence.behavioralInterference);
  return {
    source: curated ? 'curated' : 'automatic',
    reviewLevel: comparison.kind === 'name-shadow' ? 'automatic-decision' : 'manual-review-required',
    confidence: Number(Math.max(
      evidence.capabilitySimilarity || 0,
      evidence.behavioralInterference?.confidence || 0,
      comparison.score || 0,
    ).toFixed(3)),
  };
}

function comparisonSummary(comparison, options = {}) {
  const evidence = comparison.evidence;
  const interference = evidence.behavioralInterference;
  const assessment = evidenceAssessment(comparison);
  return {
    candidate: skillSummary(comparison.left),
    installed: skillSummary(comparison.right),
    kind: comparison.kind,
    severity: comparison.severity,
    score: Number(comparison.score.toFixed(3)),
    evidence: {
      sameName: evidence.sameName,
      nameSimilarity: Number(evidence.nameSimilarity.toFixed(3)),
      descriptionSimilarity: Number(evidence.descriptionSimilarity.toFixed(3)),
      bodySimilarity: Number(evidence.bodySimilarity.toFixed(3)),
      capabilitySimilarity: Number((evidence.capabilitySimilarity || 0).toFixed(3)),
      sharedCapabilities: (evidence.sharedCapabilities || []).map((item) => ({
        id: item.id,
        label: item.label,
        confidence: item.confidence,
        facets: item.facets,
        candidateMatchedBy: item.left.matchedBy,
        installedMatchedBy: item.right.matchedBy,
      })),
      behavioralInterference: interference ? {
        confidence: interference.confidence,
        overlay: {
          name: interference.overlay.name,
          scope: interference.overlay.scope,
          mode: interference.overlay.mode,
          persistent: interference.overlay.persistent,
        },
        target: interference.target,
        affectedCapabilities: interference.affectedCapabilities,
        reason: interference.reason,
      } : null,
      classificationSource: assessment.source,
      reviewLevel: assessment.reviewLevel,
      confidence: assessment.confidence,
      policyConflicts: evidence.policyConflicts,
    },
    recommendation: recommendation(comparison, options.sessionId, options.context),
  };
}

function recommendation(comparison, sessionId = '<session-id>', context = 'general') {
  const candidate = comparison.left;
  const old = comparison.right;
  if (comparison.evidence.behavioralInterference) {
    const interference = comparison.evidence.behavioralInterference;
    const overlay = interference.overlay;
    const target = interference.target;
    const side = overlay.path === candidate.path ? 'candidate' : 'installed';
    const prefix = context === 'install' ? 'Confirmation required before installation. ' : '';
    return `${prefix}Keep fixed workflow '${target.name}' authoritative; suppress ${side} '${overlay.name}' for this session when they overlap: skill-guard suppress "${overlay.name}" --session "${sessionId}"`;
  }
  if (comparison.kind === 'complementary') {
    return `Keep both; run '${comparison.left.name}' and '${comparison.right.name}' as separate review passes.`;
  }
  if (context === 'install' && ['critical', 'high'].includes(comparison.severity)) {
    if (old.scope === 'system') {
      return `Skip candidate '${candidate.name}' to keep system skill '${old.name}'; or choose the candidate and cooperatively suppress system skill '${old.name}' for this session: skill-guard suppress "${old.path}" --session "${sessionId}"`;
    }
    return `Skip candidate '${candidate.name}' to keep installed '${old.name}'; or, after explicit user approval, remove installed '${old.name}' permanently or suppress installed '${old.name}' for this session: skill-guard suppress "${old.path}" --session "${sessionId}"`;
  }
  if (comparison.kind === 'name-shadow') {
    return `Keep only one '${old.name}', or temporarily run: skill-guard suppress "${old.path}" --session "${sessionId}"`;
  }
  if (comparison.kind === 'policy-conflict') {
    return `Choose the policy needed for this task; suppress '${old.name}' for this session before continuing.`;
  }
  if (comparison.kind === 'probable-duplicate' || comparison.kind === 'capability-collision') {
    return `Prefer the narrower skill and, after explicit user approval, remove the duplicate, or suppress '${old.name}' for this session.`;
  }
  if (comparison.kind === 'capability-conflict') {
    return `Choose one behavior for this capability; suppress '${old.name}' for this session before continuing.`;
  }
  return `These skills may coexist, but make their descriptions more explicit if both trigger for the same prompt.`;
}

function formatComparisons(comparisons, options = {}) {
  if (!comparisons.length) {
    return 'No automated skill relationships found. The curated capability taxonomy is not exhaustive; manual review is still required for broad or high-risk instructions before installation.';
  }
  const lines = [`Found ${comparisons.length} skill relationship${comparisons.length === 1 ? '' : 's'}:`];
  for (const item of comparisons) {
    const assessment = evidenceAssessment(item);
    lines.push(
      '',
      `[${item.severity.toUpperCase()}] ${item.left.name} <-> ${item.right.name}`,
      `  type: ${item.kind}; similarity: ${round(item.score)}%`,
      `  candidate: ${item.left.path}`,
      `  installed: ${item.right.path}`,
    );
    if (item.evidence.sharedCapabilities?.length) {
      const capabilities = item.evidence.sharedCapabilities.map((capability) => {
        const facets = capability.facets.length > 1 ? ` (${capability.facets.join(' vs ')})` : '';
        return `${capability.label}${facets}`;
      });
      lines.push(`  shared capabilities: ${capabilities.join(', ')}`);
    }
    if (item.evidence.behavioralInterference) {
      const interference = item.evidence.behavioralInterference;
      const persistence = interference.overlay.persistent ? ', persistent' : '';
      const affected = interference.affectedCapabilities
        .map((id) => familyById(id)?.label || id);
      lines.push(
        `  behavioral overlay: ${interference.overlay.name} (${interference.overlay.scope}, ${interference.overlay.mode}${persistence})`,
        `  affected workflows: ${affected.join(', ')}`,
        `  evidence source: curated capability taxonomy; confidence: ${round(interference.confidence)}%`,
      );
    } else {
      const source = assessment.source === 'curated' ? 'curated capability taxonomy' : 'automatic lexical/policy heuristic';
      lines.push(`  evidence source: ${source}; confidence: ${round(assessment.confidence)}%`);
    }
    if (assessment.reviewLevel === 'manual-review-required') lines.push('  review level: manual review required');
    if (item.evidence.policyConflicts.length) lines.push(`  opposing policies: ${item.evidence.policyConflicts.join(', ')}`);
    lines.push(`  recommendation: ${recommendation(item, options.sessionId, options.context)}`);
  }
  return lines.join('\n');
}

function formatInventory(skills) {
  if (!skills.length) return 'No installed skills found in known coding-agent directories.';
  const lines = [`Found ${skills.length} installed skill${skills.length === 1 ? '' : 's'}:`];
  for (const skill of skills) {
    const origins = (skill.origins || [{ agent: skill.agent, scope: skill.scope }])
      .map((item) => `${item.agent}:${item.scope}`).join(', ');
    lines.push(`- ${skill.name} [${origins}] ${path.normalize(skill.path)}`);
  }
  return lines.join('\n');
}

module.exports = { comparisonSummary, evidenceAssessment, formatComparisons, formatInventory, recommendation, skillSummary };
