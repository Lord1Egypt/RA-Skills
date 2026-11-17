'use strict';

const { classifyCapabilities, familyById } = require('./capabilities');

const GLOBAL_SCOPE = [
  /\b(?:any|all|every) coding tasks?\b/i,
  /\bactive (?:on |for )?every response\b/i,
  /\b(?:all|every) (?:implementation|coding|development) (?:work|request|task)\b/i,
  /(?:任何|所有|每个).{0,8}(?:编码|开发|实现)(?:任务|工作)?/,
];

const ONE_SHOT_SCOPE = [
  /\bone[- ]shot\b/i,
  /\b(?:display|report) only\b/i,
  /(?:一次性|单次).{0,8}(?:报告|展示|检查)/,
];

const REPORT_ONLY_MODE = [
  /\b(?:does not|doesn't|do not) (?:apply fixes|edit|change|modify)\b/i,
  /\bchanges nothing\b/i,
  /\bone[- ]shot (?:report|display)\b/i,
  /(?:仅|只).{0,6}(?:报告|展示)|不(?:修改|应用修复)/,
];

const REVIEW_ONLY_MODE = [
  /\b(?:code |diff )?review\b/i,
  /\baudit\b/i,
  /(?:代码|变更|差异).{0,5}(?:审查|评审)|审计/,
];

function matchesAny(patterns, text) {
  return patterns.some((pattern) => pattern.test(text));
}

function classifyBehavior(skill) {
  const text = `${skill.name}\n${skill.description}\n${skill.body || ''}`;
  const capabilities = classifyCapabilities(skill);
  const minimalism = capabilities.find((item) => item.id === 'minimalism-yagni');
  const scope = matchesAny(ONE_SHOT_SCOPE, text)
    ? 'one-shot'
    : (matchesAny(GLOBAL_SCOPE, text) ? 'global' : 'workflow');
  let mode = 'write';
  if (scope === 'one-shot' && matchesAny(REPORT_ONLY_MODE, text)) mode = 'report-only';
  else if (matchesAny(REVIEW_ONLY_MODE, text)) mode = 'review-only';
  else if (matchesAny(REPORT_ONLY_MODE, text)) mode = 'report-only';
  return {
    name: skill.name,
    path: skill.path,
    scope,
    mode,
    persistent: scope === 'global' && /\b(?:active|persist|until|session end)\b/i.test(text),
    policy: minimalism?.facet === 'implementation-policy' ? minimalism : null,
  };
}

function behavioralInterference(left, right) {
  const pairs = [
    { overlaySkill: left, targetSkill: right },
    { overlaySkill: right, targetSkill: left },
  ];
  for (const pair of pairs) {
    const overlay = classifyBehavior(pair.overlaySkill);
    if (!overlay.policy || overlay.scope !== 'global' || overlay.mode !== 'write') continue;
    const affected = classifyCapabilities(pair.targetSkill)
      .filter((item) => familyById(item.id)?.fixedWorkflow);
    if (!affected.length) continue;
    return {
      confidence: Math.min(overlay.policy.confidence, ...affected.map((item) => item.confidence)),
      overlay,
      target: {
        name: pair.targetSkill.name,
        capabilities: affected.map((item) => item.id),
      },
      affectedCapabilities: affected.map((item) => item.id),
      reason: 'A global write policy can alter decisions inside a fixed workflow.',
    };
  }
  return null;
}

module.exports = { behavioralInterference, classifyBehavior };
