'use strict';

// Capability matching is intentionally multilingual. English and Chinese
// phrases are recognition signals for a skill's declared scope, not forced
// locale triggers and not instructions that the agent must follow.
const CAPABILITY_FAMILIES = [
  {
    id: 'test-driven-development',
    label: 'test-driven development',
    fixedWorkflow: true,
    namePatterns: [/(?:^|-)tdd(?:$|-)/, /test-driven-development/],
    descriptionPatterns: [
      /\btest[- ]driven development\b/i,
      /\b(?:write|writing) (?:a |the )?failing test first\b/i,
      /\bred[- ]green[- ]refactor\b/i,
      /测试驱动|先写(?:失败|会失败)?的?测试/,
    ],
  },
  {
    id: 'debugging',
    label: 'systematic bug diagnosis',
    fixedWorkflow: true,
    namePatterns: [/(?:^|-)(?:debug|debugging|diagnose|diagnosing|diagnosis|troubleshoot|troubleshooting)(?:$|-)/],
    descriptionPatterns: [
      /\b(?:diagnosis|debugging) (?:loop|workflow|process)\b/i,
      /\b(?:bug|failure|unexpected behavior).{0,60}\broot cause\b/i,
      /\broot cause.{0,60}\b(?:bug|failure|unexpected behavior)\b/i,
      /(?:排查.{0,12}(?:故障|问题|错误|根因)|(?:故障|问题|错误).{0,12}排查|根因.{0,12}(?:故障|问题|错误))/,
    ],
  },
  {
    id: 'skill-authoring',
    label: 'skill authoring',
    fixedWorkflow: true,
    namePatterns: [
      /(?:^|-)skill-(?:creator|authoring|writer)(?:$|-)/,
      /(?:^|-)writing-(?:great-)?skills(?:$|-)/,
      /(?:^|-)create-(?:.+-)?skill(?:$|-)/,
    ],
    descriptionPatterns: [
      /\b(?:create|creating|write|writing|edit|editing|author|authoring)\b.{0,45}\bskills?\b/i,
      /\bskills?\b.{0,45}\b(?:create|creating|write|writing|edit|editing|author|authoring)\b/i,
      /(?:创建|编写|编辑).{0,12}(?:技能|skill)/i,
    ],
    facet(skill) {
      const name = normalize(skill.name);
      return /^create-.+-skill$/.test(name) && name !== 'skill-creator' ? 'specialized-generator' : 'general';
    },
    differentFacetSeverity: 'medium',
  },
  {
    id: 'code-review',
    label: 'code review',
    fixedWorkflow: true,
    namePatterns: [/(?:^|-)(?:code-review|reviewing-code|pr-review|pull-request-review)(?:$|-)/, /代码(?:审查|评审)/],
    descriptionPatterns: [/\bcode review\b/i, /代码(?:审查|评审)/],
    facet(skill) {
      const name = normalize(skill.name);
      const description = String(skill.description || '').toLowerCase();
      if (/(?:^|-)requesting(?:-|$)/.test(name) || /\brequest(?:ing)? (?:a )?(?:code )?review\b/.test(description)) return 'requesting';
      if (/(?:^|-)receiving(?:-|$)/.test(name) || /\breceiv(?:e|ing) (?:code )?review (?:feedback|comments)\b/.test(description)) return 'receiving';
      if (/over[- ]engineering|unnecessary (?:complexity|abstractions)|过度工程/.test(`${name} ${description}`)) return 'complexity';
      return 'performing';
    },
    facetRelations: [
      { facets: ['complexity', 'performing'], kind: 'complementary', severity: 'info' },
    ],
    differentFacetSeverity: 'medium',
    descriptionOnlySeverity: 'medium',
  },
  {
    id: 'minimalism-yagni',
    label: 'minimal implementation and YAGNI',
    namePatterns: [/(?:^|-)(?:minimal(?:ist|ism)?|yagni)(?:-|$)/, /over[-]?engineering-(?:review|audit)/],
    descriptionPatterns: [
      /\byagni\b/i,
      /\b(?:simplest|minimal|shortest) (?:working )?(?:solution|implementation|diff|code)\b/i,
      /\b(?:standard library|stdlib) (?:first|before)\b/i,
      /(?:最小|最简|最少).{0,12}(?:实现|方案|代码)|避免过度工程|标准库优先/,
    ],
    facet(skill) {
      const text = `${skill.name} ${skill.description}`.toLowerCase();
      if (/\baudit\b|审计/.test(text)) return 'audit';
      if (/\breview\b|审查|评审/.test(text)) return 'review';
      return 'implementation-policy';
    },
    differentFacetSeverity: 'info',
  },
  {
    id: 'codebase-architecture',
    label: 'codebase architecture assessment',
    fixedWorkflow: true,
    namePatterns: [/(?:^|-)improv(?:e|ing)-codebase-architecture(?:$|-)/, /over[-]?engineering-audit/],
    descriptionPatterns: [
      /\bwhole[- ]repo audit for over[- ]engineering\b/i,
      /\b(?:scan|audit).{0,35}\bcodebase\b.{0,35}\b(?:architecture|deepening|over[- ]engineering)\b/i,
      /\bcodebase\b.{0,35}\b(?:architecture|deepening) (?:opportunities|improvements?)\b/i,
      /(?:全仓|整个代码库).{0,12}(?:过度工程|架构)|代码库.{0,12}(?:架构|深化机会)/,
    ],
    facet(skill) {
      const text = `${skill.name} ${skill.description}`.toLowerCase();
      return /\baudit\b|over[- ]engineering|审计|过度工程/.test(text)
        ? 'simplification-audit'
        : 'architecture-improvement';
    },
    differentFacetSeverity: 'medium',
    descriptionOnlySeverity: 'medium',
  },
  {
    id: 'skill-routing',
    label: 'skill discovery and routing',
    namePatterns: [/^(?:using-superpowers|ask-matt)$/],
    descriptionPatterns: [
      /\brouter over (?:the )?skills\b/i,
      /\bwhich skill (?:or flow )?fits\b/i,
      /\bestablishes how to find and use skills\b/i,
      /\brequiring skill invocation before\b/i,
      /(?:技能|skill).{0,12}(?:路由|选择|发现)/i,
    ],
    facet(skill) {
      const text = `${skill.name} ${skill.description} ${skill.body}`.toLowerCase();
      return /\b(?:any conversation|any response|every response|1% chance)\b/.test(text)
        ? 'global-enforcement'
        : 'routing';
    },
    differentFacetSeverity: 'high',
  },
];

function normalize(value) {
  return String(value || '').toLowerCase().replace(/[^\p{L}\p{N}]+/gu, '-').replace(/^-|-$/g, '');
}

function classifyCapabilities(skill) {
  const name = normalize(skill.name);
  const description = String(skill.description || '');
  const results = [];
  for (const family of CAPABILITY_FAMILIES) {
    const nameMatch = family.namePatterns.some((pattern) => pattern.test(name));
    const descriptionMatch = family.descriptionPatterns.some((pattern) => pattern.test(description));
    if (!nameMatch && !descriptionMatch) continue;
    results.push({
      id: family.id,
      label: family.label,
      confidence: nameMatch ? 1 : 0.78,
      facet: family.facet ? family.facet(skill) : 'default',
      matchedBy: nameMatch && descriptionMatch ? 'name+description' : (nameMatch ? 'name' : 'description'),
    });
  }
  return results.sort((left, right) => right.confidence - left.confidence || left.id.localeCompare(right.id));
}

function sharedCapabilities(left, right) {
  const leftById = new Map(classifyCapabilities(left).map((item) => [item.id, item]));
  const shared = [];
  for (const rightCapability of classifyCapabilities(right)) {
    const leftCapability = leftById.get(rightCapability.id);
    if (!leftCapability) continue;
    shared.push({
      id: rightCapability.id,
      label: rightCapability.label,
      confidence: Math.min(leftCapability.confidence, rightCapability.confidence),
      facets: [...new Set([leftCapability.facet, rightCapability.facet])],
      descriptionOnly: leftCapability.matchedBy === 'description' || rightCapability.matchedBy === 'description',
      left: leftCapability,
      right: rightCapability,
    });
  }
  return shared.sort((left, right) => right.confidence - left.confidence || left.id.localeCompare(right.id));
}

function familyById(id) {
  return CAPABILITY_FAMILIES.find((family) => family.id === id);
}

function facetRelation(family, facets) {
  return family?.facetRelations?.find((relation) =>
    relation.facets.length === facets.length && relation.facets.every((facet) => facets.includes(facet)));
}

module.exports = { CAPABILITY_FAMILIES, classifyCapabilities, facetRelation, familyById, sharedCapabilities };
