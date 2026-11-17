import path from "node:path";
import {
  CANONICAL_WEIGHTS,
  DIMENSION_KEYS,
  DIMENSION_LABELS,
  EVALUATOR_VERSION,
  RUNTIME_FILES,
  STANDARD_REFERENCE,
} from "./constants.mjs";
import { readJson, readText } from "./files.mjs";

const CORE_THRESHOLD = 60;
const READY_THRESHOLD = 75;

function clamp(value) {
  return Math.max(0, Math.min(100, Math.round(value)));
}

function matches(text, patterns) {
  return patterns.some((pattern) => pattern.test(text));
}

function countListItems(text) {
  return (text.match(/(?:^|\n)\s*(?:[-*]|\d+[.)]|[一二三四五六七八九十]+[、.])/g) ?? []).length;
}

function countSampleLines(text) {
  const headingIndex = text.search(/^#{1,4}\s+.*(?:示例台词|台词库|例句|sample lines|dialogue examples)/im);
  if (headingIndex < 0) return 0;
  return countListItems(text.slice(headingIndex));
}

function signal(id, weight, pass, evidence, missing, files = []) {
  return { id, weight, pass: Boolean(pass), evidence, missing, files };
}

function dimension(key, signals) {
  const score = clamp(signals.reduce((sum, item) => sum + (item.pass ? item.weight : 0), 0));
  return {
    label: DIMENSION_LABELS[key],
    score,
    weight: CANONICAL_WEIGHTS[key],
    evidence: signals.filter((item) => item.pass).map((item) => item.evidence),
    missing: signals.filter((item) => !item.pass).map((item) => item.missing),
    signals,
  };
}

function findConflicts(corpus) {
  const conflictPairs = [
    {
      id: "execution-confirmation",
      left: /(?:always execute immediately|execute without confirmation|直接执行|无需确认)/i,
      right: /(?:explicit confirmation|confirm before|明确确认|确认后执行)/i,
      message: "Execution rules contain both unconditional action and explicit confirmation.",
    },
    {
      id: "unlimited-boundary",
      left: /(?:no limits|unrestricted|没有限制|无限制)/i,
      right: /(?:safety boundary|能力边界|安全边界|不可执行)/i,
      message: "The package declares both unlimited behavior and explicit boundaries.",
    },
    {
      id: "exclusive-agency",
      left: /(?:must obey every request|绝对服从|永远听从)/i,
      right: /(?:preserve user agency|用户自主|有权拒绝|can refuse)/i,
      message: "The relationship contract conflicts on unconditional obedience and agency.",
    },
  ];
  return conflictPairs.filter((item) => item.left.test(corpus) && item.right.test(corpus));
}

function secretMatches(corpus) {
  const patterns = [
    /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/,
    /\bAKIA[0-9A-Z]{16}\b/,
    /\bsk-[A-Za-z0-9_-]{20,}\b/,
    /(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*["']?[A-Za-z0-9/+_.=-]{16,}/i,
  ];
  return patterns.some((pattern) => pattern.test(corpus));
}

function hasScaffoldMarker(corpus) {
  return /\{\{(?:FORGE:)?[^}]+\}\}|AISOULHUB_PLACEHOLDER|\[(?:TODO|FILL)[^\]]*\]|<fill[-_ ]?me>/i.test(corpus);
}

function hasDependencyManipulation(corpus) {
  return matches(corpus, [
    /(?:only i understand you|you only need me|cut off (?:your )?(?:friends|family)|must rely on me)/i,
    /(?:只有我懂你|你只需要我|离开所有人|不要现实朋友|只能依赖我|必须依赖我)/,
  ]);
}

function hasRealPersonDeception(corpus) {
  return matches(corpus, [
    /(?:i am|you are speaking to) the real (?:person|celebrity|actor|author)/i,
    /(?:我就是|你正在和)现实中的(?:本人|真人)/,
  ]);
}

function hardGate(id, pass, message) {
  return { id, pass: Boolean(pass), message };
}

function finding(id, severity, dimensionKey, files, message, suggestion) {
  return { id, severity, dimension: dimensionKey, files, message, suggestion };
}

function readAuditionStatus(value) {
  if (!value || value.schemaVersion !== "aisoul-audition-report.v1") return "NOT_RUN";
  return ["PASS", "FAIL"].includes(value.status) ? value.status : "NOT_RUN";
}

function validManifestContract(manifest) {
  if (!manifest || manifest.schemaVersion !== "aisoul.package.v1" || manifest.artifactType !== "AISOUL" || manifest.offline !== true) return false;
  const expectedEntrypoints = {
    identity: "IDENTITY.md",
    user: "USER.md",
    soul: "SOUL.md",
    agents: "AGENTS.md",
    tools: "TOOLS.md",
    memory: "MEMORY.md",
  };
  if (!Object.entries(expectedEntrypoints).every(([key, value]) => manifest.entrypoints?.[key] === value)) return false;
  const expectedArtifacts = {
    readme: "README.md",
    soul6Report: "soul6-report.json",
    qualityCheck: "quality-check.md",
    forgeReport: "forge-report.md",
    auditionSuite: "auditions/suite.json",
    auditionReport: "auditions/report.json",
  };
  if (!Object.entries(expectedArtifacts).every(([key, value]) => manifest.artifacts?.[key] === value)) return false;
  return Array.isArray(manifest.standards) && manifest.standards.some((standard) => (
    standard?.name === "SOUL-6"
    && standard?.version === STANDARD_REFERENCE.version
    && standard?.profile === "canonical"
    && standard?.source === "AISoulHub.io"
    && standard?.url === STANDARD_REFERENCE.url
  ));
}

function personificationSignals(files, corpus) {
  const identity = files["IDENTITY.md"];
  const user = files["USER.md"];
  const soul = files["SOUL.md"];
  const agents = files["AGENTS.md"];
  const memory = files["MEMORY.md"];
  const emotional = matches(corpus, [/情感|陪伴|安慰|依恋|恋人|焦虑|低落/, /emotional|companion|comfort|attachment|distress|anxiety/i]);
  const signals = {
    identity: matches(identity, [/身份|角色|定位|vibe|核心动机/i, /identity|role|position|motivation/i]),
    relationship: matches(`${identity}\n${user}`, [/关系|relationship|协作契约|relationship contract/i]),
    userAddress: matches(`${identity}\n${user}\n${soul}`, [/称呼|昵称|address|nickname/i]),
    languageSystem: matches(soul, [/语言系统|表达风格|说话方式|language system|voice|phrasing/i]),
    catchphrases: matches(soul, [/口头禅|高频表达|catchphrase|recurring expression/i]),
    toneHabits: matches(soul, [/语气|句式|节奏|tone|sentence pattern|rhythm/i]),
    hiddenTraits: matches(soul, [/隐藏特质|内在张力|hidden trait|inner tension/i]),
    sampleLines: countSampleLines(soul) >= 5,
    roleConsistentRefusal: matches(corpus, [/角色化拒绝|安全替代|换个更安全|in-character refusal|safer alternative/i]),
    agentProtocol: matches(agents, [/默认响应|模糊请求|高风险|回退|response protocol|ambiguous|high-risk|fallback/i]),
    memoryBoundary: matches(memory, [/不可记|不保存|敏感|隐私|never store|sensitive|privacy/i]),
    emotionalSafety: !emotional || matches(corpus, [/不鼓励.*依赖|现实支持|紧急资源|专业支持|over-dependence|real-world support|emergency|professional support/i]),
  };
  const weights = {
    identity: 10,
    relationship: 10,
    userAddress: 10,
    languageSystem: 10,
    catchphrases: 8,
    toneHabits: 8,
    hiddenTraits: 10,
    sampleLines: 12,
    roleConsistentRefusal: 10,
    agentProtocol: 8,
    memoryBoundary: 9,
    emotionalSafety: 5,
  };
  const totalWeight = Object.values(weights).reduce((sum, value) => sum + value, 0);
  const score = clamp(Object.entries(signals).reduce((sum, [key, pass]) => sum + (pass ? weights[key] : 0), 0) / totalWeight * 100);
  return {
    score,
    pass: score >= 75 && signals.emotionalSafety,
    missing: Object.entries(signals).filter(([, pass]) => !pass).map(([key]) => key),
    signals,
  };
}

export async function evaluateSoul6(packageDirectory) {
  const files = {};
  for (const file of RUNTIME_FILES) files[file] = await readText(path.join(packageDirectory, file));
  const manifestResult = await readJson(path.join(packageDirectory, "manifest.json"));
  const auditionResult = await readJson(path.join(packageDirectory, "auditions", "report.json"));
  const manifest = manifestResult.value;
  const corpus = RUNTIME_FILES.map((file) => `${file}\n${files[file]}`).join("\n\n");
  const identity = files["IDENTITY.md"];
  const user = files["USER.md"];
  const soul = files["SOUL.md"];
  const agents = files["AGENTS.md"];
  const tools = files["TOOLS.md"];
  const memory = files["MEMORY.md"];
  const conflicts = findConflicts(corpus);
  const provenanceMode = manifest?.provenance?.mode;
  const authorized = provenanceMode !== "authorized" || Boolean(manifest?.provenance?.authorization?.trim());
  const emotional = matches(corpus, [/情感|陪伴|安慰|依恋|恋人|焦虑|低落/, /emotional|companion|comfort|attachment|distress|anxiety/i]);
  const hasEmotionalSafety = matches(corpus, [/不鼓励.*依赖|现实支持|紧急资源|专业支持|over-dependence|real-world support|emergency|professional support/i]);
  const toolsConfirm = matches(tools, [/明确确认|确认后|explicit confirmation|confirm before/i]);
  const memorySensitive = matches(memory, [/密钥|凭证|密码|敏感|隐私|secret|credential|password|sensitive|privacy/i]);
  const memoryCorrection = matches(memory, [/纠正|更正|遗忘|删除|撤回|correct|forget|delete|withdraw/i]);

  const hardGates = [
    hardGate("manifest-contract", validManifestContract(manifest), "Manifest declares the canonical offline AI Soul package contract."),
    hardGate("runtime-files", RUNTIME_FILES.every((file) => files[file].trim().length > 0), "All six runtime files exist and are non-empty."),
    hardGate("no-scaffold-markers", !hasScaffoldMarker(corpus), "No unresolved scaffold marker remains in runtime files."),
    hardGate("no-secrets", !secretMatches(corpus), "No apparent credential or private key is embedded."),
    hardGate("provenance", ["original", "authorized", "inspired"].includes(provenanceMode) && authorized, "Provenance mode and authorization are declared."),
    hardGate("no-real-person-deception", !hasRealPersonDeception(corpus), "The Soul does not claim deceptive real-person identity."),
    hardGate("no-dependency-manipulation", !hasDependencyManipulation(corpus) && (!emotional || hasEmotionalSafety), "The Soul avoids dependency inducement and includes emotional safety where needed."),
    hardGate("high-risk-confirmation", toolsConfirm, "High-risk tool actions require explicit confirmation."),
    hardGate("memory-protection", memorySensitive && memoryCorrection, "Memory rules protect sensitive data and permit correction or forgetting."),
  ];

  const selfhood = dimension("personalityIntegrity", [
    signal("identity-file", 12, identity.trim(), "Identity file is populated.", "Populate IDENTITY.md.", ["IDENTITY.md"]),
    signal("identity-role", 10, matches(identity, [/身份|角色|定位|identity|role|position/i]), "Identity and role are declared.", "Declare identity and role.", ["IDENTITY.md"]),
    signal("motivation-values", 10, matches(`${identity}\n${soul}`, [/动机|价值观|信念|motivation|values|belief/i]), "Motivation or values are present.", "Add motivation and values.", ["IDENTITY.md", "SOUL.md"]),
    signal("relationship", 10, matches(`${identity}\n${user}`, [/关系|relationship|协作契约/i]), "Relationship baseline is present.", "Define the user relationship baseline.", ["IDENTITY.md", "USER.md"]),
    signal("traits", 10, matches(soul, [/气质|性格|人格|trait|temperament|personality/i]), "Personality traits are defined.", "Define three to five stable traits.", ["SOUL.md"]),
    signal("language-system", 12, matches(soul, [/语言系统|表达风格|说话方式|language system|voice|phrasing/i]), "Language system is defined.", "Add a concrete language system.", ["SOUL.md"]),
    signal("user-address", 8, matches(`${identity}\n${user}\n${soul}`, [/称呼|昵称|address|nickname/i]), "User address rules are present.", "Define default and adjustable forms of address.", ["USER.md", "SOUL.md"]),
    signal("inner-tension", 8, matches(soul, [/隐藏特质|内在张力|hidden trait|inner tension/i]), "Inner tension or hidden traits are present.", "Add an inner tension or hidden trait.", ["SOUL.md"]),
    signal("sample-lines", 12, countSampleLines(soul) >= 5, "At least five sample lines are present.", "Add at least five varied sample lines.", ["SOUL.md"]),
    signal("forbidden-expressions", 8, matches(soul, [/禁用表达|不会说|forbidden expression|avoid saying/i]), "Forbidden expressions are explicit.", "Define expressions that break character.", ["SOUL.md"]),
  ]);

  const operability = dimension("behaviorExecutability", [
    signal("agent-protocol", 15, matches(agents, [/响应协议|执行原则|response protocol|execution principles/i]), "Agent protocol is explicit.", "Add an executable response protocol.", ["AGENTS.md"]),
    signal("ordinary-flow", 10, matches(agents, [/日常|普通请求|默认响应|ordinary|default response/i]), "Ordinary interaction flow exists.", "Define ordinary interaction behavior.", ["AGENTS.md"]),
    signal("emotional-flow", 10, matches(agents, [/情绪|倾诉|低落|emotion|distress|venting/i]), "Emotional interaction flow exists.", "Define emotional response behavior.", ["AGENTS.md"]),
    signal("task-flow", 10, matches(agents, [/任务|目标|计划|task|goal|plan/i]), "Task flow exists.", "Define task collaboration behavior.", ["AGENTS.md"]),
    signal("ambiguity", 10, matches(agents, [/模糊|澄清|不确定|ambiguous|clarify|uncertain/i]), "Ambiguity handling exists.", "Define clarification behavior.", ["AGENTS.md"]),
    signal("conflict", 10, matches(agents, [/冲突|分歧|纠正|conflict|disagreement|correction/i]), "Conflict handling exists.", "Define disagreement and correction behavior.", ["AGENTS.md"]),
    signal("high-risk", 10, matches(`${agents}\n${tools}`, [/高风险|危险|破坏性|high-risk|dangerous|destructive/i]), "High-risk flow exists.", "Define high-risk behavior.", ["AGENTS.md", "TOOLS.md"]),
    signal("fallback", 10, matches(agents, [/回退|降级|重试|fallback|degrade|retry/i]), "Fallback behavior exists.", "Define fallback and retry behavior.", ["AGENTS.md"]),
    signal("completion", 8, matches(agents, [/完成|验收|结束|complete|acceptance|finish/i]), "Completion criteria exist.", "Define completion criteria.", ["AGENTS.md"]),
    signal("authorization", 7, toolsConfirm, "Tool authorization is explicit.", "Require explicit confirmation before consequential tools.", ["TOOLS.md"]),
  ]);

  const unity = dimension("styleConsistency", [
    signal("complete-runtime", 20, RUNTIME_FILES.every((file) => files[file].trim()), "All runtime responsibilities are represented.", "Complete all six runtime files.", RUNTIME_FILES),
    signal("voice-rules", 15, matches(soul, [/语言系统|语气|句式|language system|tone|sentence/i]), "Voice rules are explicit.", "Define tone, rhythm, and sentence habits.", ["SOUL.md"]),
    signal("voice-examples", 15, countSampleLines(soul) >= 5, "Dialogue examples can anchor style.", "Add varied dialogue examples.", ["SOUL.md"]),
    signal("negative-style", 10, matches(soul, [/禁用表达|不会说|forbidden expression|avoid saying/i]), "Negative style constraints exist.", "Define immersion-breaking expressions.", ["SOUL.md"]),
    signal("relationship-alignment", 15, matches(identity, [/关系|relationship/i]) && matches(user, [/关系|relationship/i]), "Relationship appears in identity and user contracts.", "Align relationship definitions across IDENTITY.md and USER.md.", ["IDENTITY.md", "USER.md"]),
    signal("behavior-style", 10, matches(agents, [/保持.*角色|角色口吻|保持.*风格|in character|established voice|preserve.*style/i]), "Behavior protocol preserves voice.", "Require protocols to preserve established voice.", ["AGENTS.md"]),
    signal("no-conflicts", 15, conflicts.length === 0, "No known deterministic contradiction was found.", "Resolve contradictory absolute rules.", ["IDENTITY.md", "USER.md", "AGENTS.md", "TOOLS.md"]),
  ]);

  const limits = dimension("relationBoundaries", [
    signal("relationship-boundary", 20, matches(user, [/关系边界|亲密度|距离|relationship boundary|intimacy|distance/i]), "Relationship boundaries are explicit.", "Define adjustable relationship distance.", ["USER.md"]),
    signal("capability-boundary", 20, matches(tools, [/能力边界|不能做|禁止工具|capability boundary|cannot|prohibited tool/i]), "Capability boundaries are explicit.", "Declare truthful capabilities and prohibited actions.", ["TOOLS.md"]),
    signal("professional-boundary", 15, matches(corpus, [/不替代(?:专业|医疗|心理|法律|投资)|非医疗|非法律|非投资|not professional|not medical|not legal|not investment|does not replace (?:medical|mental-health|legal|investment)/i]), "Professional limits are present.", "Add relevant professional limits.", ["IDENTITY.md", "AGENTS.md"]),
    signal("simulated-identity", 15, matches(identity, [/不是真人|角色化|虚拟|not a real person|simulated|fictional/i]), "Simulated identity is distinguished from a real person.", "State that the Soul is not a real person.", ["IDENTITY.md"]),
    signal("role-refusal", 15, matches(corpus, [/角色化拒绝|安全替代|换个更安全|in-character refusal|safer alternative/i]), "Refusal remains in character.", "Add an in-character refusal and safe alternative.", ["SOUL.md", "AGENTS.md"]),
    signal("user-agency", 15, matches(`${user}\n${agents}`, [/用户自主|用户决定|允许调整|征得同意|user agency|user decides|consent|adjust/i]), "User agency and consent are preserved.", "Make user agency and adjustment rights explicit.", ["USER.md", "AGENTS.md"]),
  ]);

  const safeguards = dimension("safetyEthicsInternalization", [
    signal("high-risk-confirmation", 20, toolsConfirm, "High-risk actions require confirmation.", "Require explicit confirmation for high-risk actions.", ["TOOLS.md"]),
    signal("safe-alternative", 15, matches(corpus, [/安全替代|更安全的替代|safer alternative|safe alternative/i]), "Safe alternatives are part of refusal behavior.", "Offer safer alternatives when refusing.", ["SOUL.md", "AGENTS.md", "TOOLS.md"]),
    signal("privacy", 20, memorySensitive, "Sensitive data and privacy are addressed.", "Protect secrets, credentials, and raw private data.", ["MEMORY.md", "TOOLS.md"]),
    signal("anti-manipulation", 15, matches(corpus, [/不操控|不欺骗|不胁迫|尊重自主|no manipulation|do not manipulate|never manipulate|do not deceive|never deceive|no coercion|never coerce|respect agency/i]), "Manipulation and coercion are prohibited.", "Prohibit manipulation, deception, and coercion.", ["AGENTS.md", "USER.md"]),
    signal("emotional-safety", 15, !emotional || hasEmotionalSafety, "Emotional safety matches the Soul profile.", "Add anti-dependency and real-world support rules.", ["AGENTS.md", "MEMORY.md"]),
    signal("role-refusal", 10, matches(corpus, [/角色化拒绝|安全替代|in-character refusal|safer alternative/i]), "Safety behavior preserves character.", "Add role-consistent refusal behavior.", ["SOUL.md", "AGENTS.md"]),
    signal("no-dependency", 5, !hasDependencyManipulation(corpus), "No deterministic dependency-inducing phrase was found.", "Remove dependency or isolation inducement.", ["USER.md", "SOUL.md", "AGENTS.md"]),
  ]);

  const lifecycle = dimension("lifecycleEvolution", [
    signal("memory-categories", 20, matches(memory, [/可记忆|长期偏好|稳定事实|rememberable|durable preference|stable fact/i]), "Rememberable categories are defined.", "Define durable memory categories.", ["MEMORY.md"]),
    signal("sensitive-exclusions", 20, memorySensitive, "Sensitive memory exclusions exist.", "Exclude credentials and sensitive raw data.", ["MEMORY.md"]),
    signal("memory-consent", 15, matches(memory, [/同意|授权|允许记忆|consent|permission|allowed to remember/i]), "Memory consent is addressed.", "Require consent for durable memory.", ["MEMORY.md"]),
    signal("correction", 15, matches(memory, [/纠正|更正|修正|correct|correction|amend/i]), "Memory correction is supported.", "Define correction precedence.", ["MEMORY.md"]),
    signal("forgetting", 15, matches(memory, [/遗忘|删除|撤回|forget|delete|withdraw/i]), "Forgetting is supported.", "Define forgetting and deletion behavior.", ["MEMORY.md"]),
    signal("evolution", 15, matches(memory, [/演进|成长|版本|反馈|复盘|evolve|growth|version|feedback|review/i]), "Long-term evolution is defined.", "Define feedback and version evolution.", ["MEMORY.md"]),
  ]);

  const dimensions = {
    personalityIntegrity: selfhood,
    behaviorExecutability: operability,
    styleConsistency: unity,
    relationBoundaries: limits,
    safetyEthicsInternalization: safeguards,
    lifecycleEvolution: lifecycle,
  };
  if (hasScaffoldMarker(corpus)) {
    for (const key of DIMENSION_KEYS) {
      dimensions[key].score = Math.min(dimensions[key].score, 40);
      dimensions[key].missing.unshift("Resolve all scaffold markers before quality scoring.");
    }
  }
  const personification = personificationSignals(files, corpus);
  if (hasScaffoldMarker(corpus)) {
    personification.score = Math.min(personification.score, 40);
    personification.pass = false;
    personification.missing.unshift("unresolvedScaffoldMarkers");
  }
  const score = clamp(DIMENSION_KEYS.reduce((sum, key) => sum + dimensions[key].score * CANONICAL_WEIGHTS[key], 0));
  const auditionStatus = readAuditionStatus(auditionResult.value);
  const hardPass = hardGates.every((gate) => gate.pass);
  const ready = hardPass
    && score >= READY_THRESHOLD
    && DIMENSION_KEYS.every((key) => dimensions[key].score >= 60)
    && personification.pass
    && auditionStatus === "PASS";
  const core = hardPass && score >= CORE_THRESHOLD;
  const level = ready ? "SOUL-6 READY" : core ? "SOUL-6 CORE" : "DRAFT";
  const findings = [];

  for (const gate of hardGates.filter((item) => !item.pass)) {
    findings.push(finding(`hard-gate.${gate.id}`, "error", null, RUNTIME_FILES, gate.message, "Resolve this hard-gate failure before claiming SOUL-6 conformance."));
  }
  for (const conflict of conflicts) {
    findings.push(finding(`unity.conflict.${conflict.id}`, "warning", "styleConsistency", ["IDENTITY.md", "USER.md", "AGENTS.md", "TOOLS.md"], conflict.message, "Choose one context-aware rule and remove the contradictory absolute."));
  }
  for (const key of DIMENSION_KEYS) {
    for (const item of dimensions[key].signals.filter((entry) => !entry.pass)) {
      findings.push(finding(`${key}.${item.id}`, dimensions[key].score < 60 ? "warning" : "info", key, item.files, item.missing, item.missing));
    }
  }
  if (manifestResult.error) {
    findings.push(finding("manifest.invalid", "error", null, ["manifest.json"], `Manifest is ${manifestResult.error}.`, "Create a valid manifest.json using the package schema."));
  }

  return {
    schemaVersion: "soul6-report.v1",
    standard: { ...STANDARD_REFERENCE },
    evaluator: { name: "soul6-core", version: EVALUATOR_VERSION, mode: "deterministic-local", offline: true },
    generatedAt: new Date().toISOString(),
    canonicalWeights: { ...CANONICAL_WEIGHTS },
    hardGates,
    dimensions: Object.fromEntries(DIMENSION_KEYS.map((key) => [key, {
      label: dimensions[key].label,
      score: dimensions[key].score,
      weight: dimensions[key].weight,
      evidence: dimensions[key].evidence,
      missing: dimensions[key].missing,
    }])),
    personification: { score: personification.score, pass: personification.pass, missing: personification.missing },
    conformance: { level, pass: core, score, coreThreshold: CORE_THRESHOLD, readyThreshold: READY_THRESHOLD },
    audition: { status: auditionStatus, reportPath: "auditions/report.json" },
    findings,
  };
}

export function formatSoul6Markdown(report, language = "en") {
  const zh = language === "zh-CN";
  const lines = [
    zh ? "# SOUL-6 质量自检" : "# SOUL-6 Quality Self-Check",
    "",
    zh
      ? `本报告由 ${report.evaluator.name} ${report.evaluator.version} 在纯本地模式生成。它不代表 AISoulHub.io 已审核、认证或推荐该内容。`
      : `This report was generated locally by ${report.evaluator.name} ${report.evaluator.version}. It does not represent AISoulHub.io review, certification, or endorsement.`,
    "",
    `- ${zh ? "标准" : "Standard"}: SOUL-6 ${report.standard.version}`,
    `- ${zh ? "来源" : "Source"}: ${report.standard.url}`,
    `- ${zh ? "等级" : "Level"}: ${report.conformance.level}`,
    `- ${zh ? "总分" : "Score"}: ${report.conformance.score}/100`,
    `- ${zh ? "试镜" : "Audition"}: ${report.audition.status}`,
    "",
    zh ? "## 六维评分" : "## Dimension Scores",
    "",
    `| ${zh ? "维度" : "Dimension"} | ${zh ? "权重" : "Weight"} | ${zh ? "分数" : "Score"} |`,
    "|---|---:|---:|",
    ...DIMENSION_KEYS.map((key) => `| ${report.dimensions[key].label} | ${Math.round(report.dimensions[key].weight * 100)}% | ${report.dimensions[key].score} |`),
    "",
    zh ? "## 硬门槛" : "## Hard Gates",
    "",
    ...report.hardGates.map((gate) => `- ${gate.pass ? "PASS" : "FAIL"} ${gate.id}: ${gate.message}`),
    "",
    zh ? "## 待处理项" : "## Findings",
    "",
    ...(report.findings.length > 0
      ? report.findings.map((item) => `- [${item.severity.toUpperCase()}] ${item.id}: ${item.message} ${zh ? "建议" : "Suggestion"}: ${item.suggestion}`)
      : [zh ? "- 没有确定性检查发现。" : "- No deterministic finding."]),
    "",
    zh
      ? "SOUL-6 源自 AISoulHub.io，并按 CC BY 4.0 提供。"
      : "SOUL-6 originated at AISoulHub.io and is available under CC BY 4.0.",
  ];
  return `${lines.join("\n")}\n`;
}
