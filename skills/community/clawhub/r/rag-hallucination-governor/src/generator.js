#!/usr/bin/env node

const readline = require('readline');

function parseArgs(argv) {
  const args = { symptom: null, scenario: null, retrieval: null, impact: null, quick: false };
  for (let i = 2; i < argv.length; i += 1) {
    switch (argv[i]) {
      case '--symptom': args.symptom = argv[++i]; break;
      case '--scenario': args.scenario = argv[++i]; break;
      case '--retrieval': args.retrieval = argv[++i]; break;
      case '--impact': args.impact = argv[++i]; break;
      case '--quick': args.quick = true; break;
      case '--help':
      case '-h': printHelp(); process.exit(0); break;
      default: break;
    }
  }
  return args;
}

function printHelp() {
  console.log(`
RAG hallucination governor

Usage:
  node generator.js --symptom "Top1相似度很高但答案经常错"
  node generator.js --symptom "引用错误政策" --scenario "制度问答" --retrieval "Top1=0.86 Top2=0.83 来源冲突"
  node generator.js --symptom "query rewrite 后把门店退款问题扩成了通用财务制度"

Options:
  --symptom     Production symptom, required
  --scenario    Business scenario
  --retrieval   Retrieval/rerank/citation log summary
  --impact      Business impact
  --quick       Print compact card
`);
}

const RULES = [
  {
    key: 'top1_pollution',
    name: 'Top1 pollution',
    trigger: /top\s*1|top1|第一条|相似度.*高|高相似|召回.*错|错文档|错误文档/i,
    failure: 'High-similarity wrong evidence suppresses better lower-ranked evidence.',
    controls: [
      'Add Top1 pollution detection: if Top1 conflicts with Top2/Top3 by source, version, or subject, do not directly generate.',
      'Use rerank plus evidence-consistency checks instead of vector score alone.',
      'Create a high-score conflict reject band that routes to clarification or human review.',
    ],
    metrics: ['Top1 adoption rate', 'Top1/Top2 conflict rate', 'high-score reject rate', 'human-review hit rate'],
    handoff: 'Refuse or route to human when high-scoring evidence conflicts on conclusion, version, or subject.',
  },
  {
    key: 'citation_gap',
    name: 'Citation coverage gap',
    trigger: /引用|出处|citation|cite|来源|编造|无依据|依据不足/i,
    failure: 'The answer contains key claims that cannot be traced to retrieved evidence.',
    controls: [
      'Add sentence-level citation coverage checks for key facts.',
      'Remove or downgrade claims that cannot be bound to evidence.',
      'Enable strict citation mode for policy, amount, date, ownership, and compliance answers.',
    ],
    metrics: ['key-claim citation coverage', 'unsupported fact count', 'citation hit rate', 'post-answer correction rate'],
    handoff: 'Refuse or route to human when key facts cannot be bound to evidence.',
  },
  {
    key: 'conflict',
    name: 'Evidence conflict',
    trigger: /冲突|矛盾|多个答案|不一致|版本|新旧|政策.*不同|制度.*不同/i,
    failure: 'The model blends conflicting evidence into a synthetic answer that no source supports.',
    controls: [
      'Add dual-hit conflict checks before generation.',
      'Resolve by version, publish time, scope, and organization level.',
      'Expose unresolved conflicts and ask the user to choose the applicable scope.',
    ],
    metrics: ['conflict detection rate', 'version-resolution rate', 'clarification completion rate', 'conflict miss reports'],
    handoff: 'Route to human when conflicts cannot be resolved by version or scope.',
  },
  {
    key: 'rewrite_drift',
    name: 'Query rewrite drift',
    trigger: /rewrite|改写|扩写|重写|泛化|范围扩大|scope|漂移|门店.*通用|问题.*扩/i,
    failure: 'Query rewrite changes the business scope, so retrieval answers a broader or different question than the user asked.',
    controls: [
      'Log pre-rewrite and post-rewrite queries, then compare their TopK evidence overlap.',
      'Add a rewrite drift guard: if rewritten scope changes entity, department, product, or policy domain, ask for clarification.',
      'Route narrow operational questions away from broad policy retrieval unless the user explicitly asks for policy background.',
    ],
    metrics: ['rewrite drift rate', 'pre/post rewrite TopK overlap', 'clarification rate after rewrite', 'wrong-scope correction rate'],
    handoff: 'Clarify or hand off when rewrite changes the entity, department, product, tenant, or policy scope.',
  },
  {
    key: 'scope_mismatch',
    name: 'Permission or scope mismatch',
    trigger: /权限|租户|tenant|部门|ACL|scope|串库|跨库|别的部门|知识库串|数据域/i,
    failure: 'The answer is grounded in evidence from the wrong tenant, department, permission scope, or knowledge slice.',
    controls: [
      'Add ACL and tenant-scope filters before retrieval, not only after generation.',
      'Log evidence scope fields with every cited chunk: tenant, department, role, version, and visibility.',
      'Block answer generation when cited evidence scope does not match the user context.',
    ],
    metrics: ['scope-filter miss rate', 'cross-tenant retrieval count', 'ACL-blocked answer count', 'wrong-scope user reports'],
    handoff: 'Refuse and escalate when evidence comes from a different tenant, department, role, or restricted corpus.',
  },
  {
    key: 'low_confidence',
    name: 'Low-confidence hard answer',
    trigger: /低置信|阈值|threshold|分数低|不确定|兜底|硬答|拒答/i,
    failure: 'The system produces a confident answer despite weak or scattered evidence.',
    controls: [
      'Use three bands: answer, clarify, refuse.',
      'Allow conservative answers only when low-score evidence is still mutually consistent.',
      'Replace guess-style fallback with missing-condition clarification.',
    ],
    metrics: ['refusal rate', 'clarification success rate', 'low-score correction rate', 'threshold band distribution'],
    handoff: 'Route to human when evidence is below the minimum threshold or scattered across unrelated chunks.',
  },
];

function pickRule(input) {
  const text = [input.symptom, input.retrieval, input.impact].filter(Boolean).join(' ');
  const priority = ['scope_mismatch', 'rewrite_drift', 'top1_pollution', 'conflict', 'citation_gap', 'low_confidence'];
  for (const key of priority) {
    const rule = RULES.find((item) => item.key === key);
    if (rule && rule.trigger.test(text)) return rule;
  }
  return RULES[RULES.length - 1];
}

function matchedRules(input) {
  const text = [input.symptom, input.retrieval, input.impact].filter(Boolean).join(' ');
  const priority = ['scope_mismatch', 'rewrite_drift', 'top1_pollution', 'conflict', 'citation_gap', 'low_confidence'];
  return priority
    .map((key) => RULES.find((item) => item.key === key))
    .filter((rule) => rule && rule.trigger.test(text));
}

function requiredLogs(rule) {
  const common = [
    'TopK chunks with source, version, tenant, department, role, and visibility',
    'vector score and rerank score',
    'cited spans mapped to final answer claims',
    'final answer, refusal, clarification, or human-handoff decision',
  ];

  const byRule = {
    top1_pollution: [
      'Top1/Top2/Top3 subject, source, version, and conclusion comparison',
      'rerank score and evidence-consistency check result',
    ],
    citation_gap: [
      'key answer claims and their cited evidence spans',
      'unsupported claim count after citation coverage check',
    ],
    conflict: [
      'conflicting chunk versions, publish times, and organization scopes',
      'version-resolution decision or unresolved-conflict marker',
    ],
    rewrite_drift: [
      'query before rewrite',
      'query after rewrite',
      'pre/post rewrite TopK overlap and scope change result',
    ],
    scope_mismatch: [
      'user tenant, department, role, and permission context',
      'evidence tenant, department, role, and visibility fields',
      'ACL filter decision before retrieval',
    ],
    low_confidence: [
      'threshold band distribution for TopK evidence',
      'rerank score distribution',
      'threshold pass rate and clarification/refusal decision',
    ],
  };

  return [...(byRule[rule.key] || []), ...common];
}

function generateCard(input) {
  const rule = pickRule(input);
  const matches = matchedRules(input);
  const scenario = input.scenario || 'not specified';
  const symptom = input.symptom || 'not specified';
  const retrieval = input.retrieval || 'retrieval logs not provided';
  const impact = input.impact || 'impact not provided';

  const lines = [
    '# RAG Hallucination Triage Note',
    '',
    `- Scenario: ${scenario}`,
    `- Symptom: ${symptom}`,
    `- Retrieval evidence: ${retrieval}`,
    `- Business impact: ${impact}`,
    `- Risk type: ${rule.name}`,
  ];

  if (matches.length > 1) {
    lines.push(
      `- Additional risk types: ${matches.slice(1).map((item) => item.name).join(', ')}`,
      '- Mixed-risk note: this input matches multiple production failure patterns. Use this CLI result as triage, then load the full skill for deeper analysis.',
    );
  }

  lines.push(
    '',
    '## Field Diagnosis',
    '',
    `- Trigger signal: ${symptom}`,
    `- Production failure mode: ${rule.failure}`,
    `- Immediate stance: do not treat this as a prompt-only issue; verify retrieval, scope, citation, and handoff controls first.`,
    '',
    '## Control Changes',
    '',
  );

  rule.controls.forEach((control, index) => lines.push(`${index + 1}. ${control}`));

  lines.push(
    '',
    '## Metrics To Watch',
    '',
    ...rule.metrics.map((metric) => `- ${metric}`),
    '',
    '## Refuse, Clarify, Or Handoff',
    '',
    `- ${rule.handoff}`,
    '',
    '## Required Logs',
    '',
    ...requiredLogs(rule).map((item) => `- ${item}`),
  );

  if (!input.quick) {
    lines.push(
      '',
      '## Smoke Cases',
      '',
      '- Correct evidence appears at Top2/Top3 while wrong evidence appears at Top1.',
      '- Two policy versions conflict and require scope or version resolution.',
      '- Evidence supports background context but not the final answer claim.',
      '',
      '## Review Note',
      '',
      '- This output is a triage note. Do not claim exact incident root cause without the required logs.',
    );
  }

  return lines.join('\n');
}

function interactiveMode() {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  const ask = (question) => new Promise((resolve) => rl.question(question, resolve));

  (async () => {
    const symptom = await ask('Symptom: ');
    if (!symptom.trim()) {
      console.log('Symptom is required');
      rl.close();
      return;
    }
    const scenario = await ask('Scenario: ');
    const retrieval = await ask('Retrieval summary: ');
    const impact = await ask('Impact: ');
    console.log('\n' + generateCard({
      symptom: symptom.trim(),
      scenario: scenario.trim() || null,
      retrieval: retrieval.trim() || null,
      impact: impact.trim() || null,
    }));
    rl.close();
  })();
}

if (require.main === module) {
  const args = parseArgs(process.argv);
  if (!args.symptom) interactiveMode();
  else console.log(generateCard(args));
}

module.exports = { detectRules: matchedRules, generateCard, matchedRules, parseArgs, requiredLogs };
