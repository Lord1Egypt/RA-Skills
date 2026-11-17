'use strict';

const { classifyCapabilities, facetRelation, familyById, sharedCapabilities } = require('./capabilities');
const { behavioralInterference } = require('./behavior');

const STOP_WORDS = new Set([
  'a', 'an', 'and', 'are', 'as', 'at', 'be', 'before', 'by', 'can', 'code', 'codex',
  'do', 'does', 'for', 'from', 'how', 'if', 'in', 'into', 'is', 'it', 'of', 'on',
  'or', 'should', 'skill', 'that', 'the', 'this', 'to', 'use', 'user', 'when', 'with',
  'work', 'you', 'your'
]);

// These expressions classify instructions found in skills. They are evidence
// for a human review, never permissions or commands for the guard to execute.
// Approval-related phrases describe a candidate skill's policy and must not
// disable the guard's own human approval boundary.
const POLICY_PAIRS = [
  ['dependency policy', /\b(no|avoid|without)\s+(new\s+)?dependenc|\bstdlib\s+first|standard library first/i,
    /\b(?:proven|third[- ]party|external)\s+(?:library|dependenc|package)|\binstall\s+(?:a\s+)?(?:library|dependenc|package)|do not hand[- ]roll/i],
  ['response detail', /\b(concise|brief|minimal|shortest|terse)\b/i,
    /\b(detailed|thorough|comprehensive|maximally|long[- ]form)\b/i],
  ['write policy', /\b(read[- ]only|do not (edit|implement|modify)|no code changes)\b/i,
    /\b(implement|edit files|make the change|write the code)\b/i],
  ['approval policy', /\b(ask|confirm|approval).{0,30}\b(before|first)\b/i,
    /\b(do not ask|without asking|proceed autonomously|no confirmation)\b/i],
  ['test policy', /\b(skip|do not (run|write)|without)\s+(the\s+)?tests?\b/i,
    /\b(test[- ]driven|run (the )?tests|write tests|red[- ]green[- ]refactor)\b/i],
];

const COMPLEMENTARY_ACTIONS = [
  ['save', 'restore'], ['freeze', 'unfreeze'], ['install', 'uninstall'],
  ['enable', 'disable'], ['start', 'stop'], ['encode', 'decode'],
];
const PROFILE_CACHE = new WeakMap();

function normalizeName(name) {
  return String(name || '').toLowerCase().replace(/[^\p{L}\p{N}]+/gu, '-').replace(/^-|-$/g, '');
}

function tokens(value) {
  const parts = String(value || '').toLowerCase().match(/[a-z][a-z0-9-]*|\p{Script=Han}+/gu) || [];
  const result = [];
  for (const part of parts) {
    if (/^\p{Script=Han}+$/u.test(part)) {
      if (part.length === 1) result.push(part);
      else for (let index = 0; index < part.length - 1; index += 1) result.push(part.slice(index, index + 2));
    } else {
      const normalized = part.replace(/^-|-$/g, '');
      if (normalized.length > 1 && !STOP_WORDS.has(normalized)) result.push(normalized);
    }
  }
  return new Set(result);
}

function jaccard(left, right) {
  if (!left.size || !right.size) return 0;
  let intersection = 0;
  for (const item of left) if (right.has(item)) intersection += 1;
  return intersection / (left.size + right.size - intersection);
}

function bigrams(value) {
  const normalized = normalizeName(value).replace(/-/g, '');
  if (normalized.length < 2) return new Set(normalized ? [normalized] : []);
  const result = new Set();
  for (let index = 0; index < normalized.length - 1; index += 1) result.add(normalized.slice(index, index + 2));
  return result;
}

function findPolicyConflicts(left, right) {
  const leftText = profile(left).text;
  const rightText = profile(right).text;
  const conflicts = [];
  for (const [label, first, second] of POLICY_PAIRS) {
    if ((first.test(leftText) && second.test(rightText)) || (second.test(leftText) && first.test(rightText))) {
      conflicts.push(label);
    }
  }
  return conflicts;
}

function profile(skill) {
  if (PROFILE_CACHE.has(skill)) return PROFILE_CACHE.get(skill);
  const value = {
    name: normalizeName(skill.name),
    nameBigrams: bigrams(skill.name),
    nameParts: new Set(normalizeName(skill.name).split('-').filter(Boolean)),
    descriptionTokens: tokens(skill.description),
    bodyTokens: tokens(String(skill.body || '').slice(0, 12000)),
    text: `${skill.description}\n${skill.body}`,
  };
  PROFILE_CACHE.set(skill, value);
  return value;
}

function declaresSeparation(left, right) {
  const mentions = (source, target) => {
    const description = String(source.description || '').toLowerCase();
    const escaped = normalizeName(target.name).replace(/[.*+?^${}()|[\]\\]/g, '\\$&').replace(/-/g, '[- ]');
    return new RegExp(`(?:separate|different|distinct)\\s+from\\s+[/@$]?${escaped}\\b`, 'i').test(description);
  };
  return mentions(left, right) || mentions(right, left);
}

function complementaryNames(left, right) {
  const leftParts = profile(left).nameParts;
  const rightParts = profile(right).nameParts;
  return COMPLEMENTARY_ACTIONS.some(([a, b]) =>
    (leftParts.has(a) && rightParts.has(b)) || (leftParts.has(b) && rightParts.has(a)));
}

function compareSkills(left, right) {
  const leftProfile = profile(left);
  const rightProfile = profile(right);
  const sameName = leftProfile.name === rightProfile.name;
  const nameSimilarity = jaccard(leftProfile.nameBigrams, rightProfile.nameBigrams);
  const descriptionSimilarity = jaccard(leftProfile.descriptionTokens, rightProfile.descriptionTokens);
  const bodySimilarity = jaccard(leftProfile.bodyTokens, rightProfile.bodyTokens);
  const policyConflicts = findPolicyConflicts(left, right);
  const shared = sharedCapabilities(left, right);
  const interference = behavioralInterference(left, right);
  const capabilitySimilarity = shared[0]?.confidence || 0;
  // Descriptions define invocation scope. Bodies often share templates and host
  // boilerplate, so body overlap is evidence for humans but not a routing score.
  const lexicalScore = nameSimilarity * 0.45 + descriptionSimilarity * 0.55;
  const score = sameName ? 1 : Math.min(1, Math.max(
    lexicalScore,
    capabilitySimilarity,
    interference?.confidence || 0,
  ));

  let kind = 'distinct';
  let severity = 'none';
  if (sameName) {
    kind = 'name-shadow';
    severity = 'critical';
  } else if (declaresSeparation(left, right) || complementaryNames(left, right)) {
    kind = 'distinct';
    severity = 'none';
  } else if (policyConflicts.length && descriptionSimilarity >= 0.24) {
    kind = 'policy-conflict';
    severity = 'high';
  } else if (shared.length) {
    const strongest = shared[0];
    const family = familyById(strongest.id);
    const differentFacets = strongest.facets.length > 1;
    const relation = facetRelation(family, strongest.facets);
    if (relation) {
      kind = relation.kind;
      severity = relation.severity;
    } else {
      severity = differentFacets
        ? (family.differentFacetSeverity || 'medium')
        : (strongest.descriptionOnly ? (family.descriptionOnlySeverity || 'high') : 'high');
      kind = differentFacets
        ? (severity === 'high' ? 'capability-conflict' : 'capability-overlap')
        : (severity === 'high' ? 'capability-collision' : 'capability-overlap');
    }
  } else if (interference) {
    kind = policyConflicts.length ? 'policy-conflict' : 'behavioral-interference';
    severity = policyConflicts.length ? 'high' : 'medium';
  } else if (policyConflicts.length &&
      (descriptionSimilarity >= 0.24 || (nameSimilarity >= 0.65 && descriptionSimilarity >= 0.14))) {
    kind = 'policy-conflict';
    severity = 'high';
  } else if (score >= 0.68) {
    kind = 'probable-duplicate';
    severity = 'high';
  } else if (score >= 0.42 || (descriptionSimilarity >= 0.32 && nameSimilarity >= 0.2)) {
    kind = 'overlap';
    severity = 'medium';
  }

  return {
    left,
    right,
    kind,
    severity,
    score,
    evidence: {
      sameName,
      nameSimilarity,
      descriptionSimilarity,
      bodySimilarity,
      capabilitySimilarity,
      sharedCapabilities: shared,
      behavioralInterference: interference,
      policyConflicts,
    },
  };
}

function analyzeCandidates(candidates, installed, options = {}) {
  const ignored = new Set((options.ignorePaths || []).map(String));
  const results = [];
  for (const candidate of candidates) {
    for (const existing of installed) {
      if (candidate.path === existing.path || ignored.has(existing.path) || ignored.has(existing.name)) continue;
      const comparison = compareSkills(candidate, existing);
      if (comparison.severity !== 'none') results.push(comparison);
    }
  }
  const rank = { critical: 4, high: 3, medium: 2, info: 1, none: 0 };
  return results.sort((a, b) => rank[b.severity] - rank[a.severity] || b.score - a.score);
}

function requiresInstallDecision(comparison) {
  return comparison.severity === 'critical' || comparison.severity === 'high' ||
    comparison.kind === 'behavioral-interference';
}

function clusters(skills) {
  const results = [];
  for (let left = 0; left < skills.length; left += 1) {
    for (let right = left + 1; right < skills.length; right += 1) {
      const comparison = compareSkills(skills[left], skills[right]);
      if (comparison.severity !== 'none') results.push(comparison);
    }
  }
  return results;
}

function matchPrompt(prompt, skills) {
  const explicit = new Set();
  for (const match of String(prompt || '').matchAll(/(?:^|\s)[$@/]([a-z0-9][a-z0-9._-]*)/gi)) explicit.add(normalizeName(match[1]));
  const promptTokens = tokens(prompt);
  return skills.map((skill) => {
    const name = normalizeName(skill.name);
    const explicitMatch = explicit.has(name) || explicit.has(name.split(':').pop());
    const intent = jaccard(promptTokens, tokens(`${skill.name} ${skill.description}`));
    return { skill, explicit: explicitMatch, intent };
  }).filter((item) => item.explicit || item.intent >= 0.16)
    .sort((a, b) => Number(b.explicit) - Number(a.explicit) || b.intent - a.intent);
}

module.exports = {
  analyzeCandidates,
  clusters,
  compareSkills,
  classifyCapabilities,
  behavioralInterference,
  complementaryNames,
  declaresSeparation,
  findPolicyConflicts,
  jaccard,
  matchPrompt,
  normalizeName,
  requiresInstallDecision,
  tokens,
};
