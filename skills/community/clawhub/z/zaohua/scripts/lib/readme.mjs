import path from "node:path";
import { DIMENSION_KEYS, RUNTIME_FILES, SOUL6_URL } from "./constants.mjs";
import { pathExists, readJson, readText, writeText } from "./files.mjs";

const SCAFFOLD_MARKER_PATTERN = /\{\{(?:FORGE:)?[^}]+\}\}|AISOULHUB_PLACEHOLDER|\[(?:TODO|FILL)[^\]]*\]|<fill[-_ ]?me>/i;
const SAFE_CASE_ID_PATTERN = /^[a-z0-9-]+$/;
const REPRESENTATIVE_CASE_IDS = [
  "ordinary-interaction",
  "ambiguous-request",
  "boundary-refusal",
];

const DIMENSION_LABELS = {
  en: {
    personalityIntegrity: "Selfhood / Personality Integrity",
    behaviorExecutability: "Operability / Behavior Executability",
    styleConsistency: "Unity / Style Consistency",
    relationBoundaries: "Limits / Relationship Boundaries",
    safetyEthicsInternalization: "Safeguards / Safety Internalization",
    lifecycleEvolution: "Lifecycle / Long-Term Evolvability",
  },
  "zh-CN": {
    personalityIntegrity: "人格完整度 / Selfhood",
    behaviorExecutability: "行为可执行性 / Operability",
    styleConsistency: "风格一致性 / Unity",
    relationBoundaries: "关系与能力边界 / Limits",
    safetyEthicsInternalization: "安全伦理内化 / Safeguards",
    lifecycleEvolution: "长期演进能力 / Lifecycle",
  },
};

function isRecord(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function finiteNumber(value) {
  return typeof value === "number" && Number.isFinite(value) ? value : null;
}

function stripMarkdown(value) {
  return String(value ?? "")
    .replace(/!\[([^\]]*)\]\([^)]*\)/g, "$1")
    .replace(/\[([^\]]+)\]\([^)]*\)/g, "$1")
    .replace(/`([^`]*)`/g, "$1")
    .replace(/^\s{0,3}(?:#{1,6}|>|[-*+]\s+|\d+[.)]\s+)/gm, "")
    .replace(/[~*_`]/g, "")
    .replace(/\r?\n+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function truncate(value, maximum = 320) {
  const characters = Array.from(String(value ?? ""));
  if (characters.length <= maximum) return characters.join("");
  return `${characters.slice(0, Math.max(0, maximum - 3)).join("").trimEnd()}...`;
}

function displayValue(value, fallback, maximum = 320) {
  const normalized = stripMarkdown(value);
  if (!normalized || SCAFFOLD_MARKER_PATTERN.test(normalized)) return fallback;
  return truncate(normalized, maximum);
}

function normalizeLabel(value) {
  return stripMarkdown(value).toLocaleLowerCase("en-US").replace(/\s+/g, " ").trim();
}

function extractLabeledValue(content, labels) {
  const accepted = new Set(labels.map(normalizeLabel));
  for (const rawLine of String(content ?? "").split(/\r?\n/)) {
    const line = rawLine.replace(/^\s*[-*+]\s*/, "").trim();
    const match = line.match(/^(.{1,80}?)[：:]\s*(.+)$/u);
    if (match && accepted.has(normalizeLabel(match[1]))) return match[2].trim();
  }
  return "";
}

function extractSection(content, headings) {
  const accepted = new Set(headings.map(normalizeLabel));
  const lines = String(content ?? "").split(/\r?\n/);
  let start = -1;
  let level = 7;

  for (let index = 0; index < lines.length; index += 1) {
    const match = lines[index].match(/^\s*(#{1,6})\s+(.+?)\s*$/);
    if (!match || !accepted.has(normalizeLabel(match[2]))) continue;
    start = index + 1;
    level = match[1].length;
    break;
  }
  if (start < 0) return "";

  const selected = [];
  for (let index = start; index < lines.length; index += 1) {
    const heading = lines[index].match(/^\s*(#{1,6})\s+/);
    if (heading && heading[1].length <= level) break;
    selected.push(lines[index]);
  }
  return selected.join("\n");
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function markdownText(value) {
  return escapeHtml(stripMarkdown(value))
    .replaceAll("\\", "\\\\")
    .replaceAll("|", "\\|")
    .replaceAll("[", "\\[")
    .replaceAll("]", "\\]");
}

function tableCell(value) {
  return markdownText(value) || "-";
}

function codeBadge(value) {
  return `<code>${escapeHtml(stripMarkdown(value))}</code>`;
}

function progressBar(score) {
  if (score === null) return "[----------]";
  const bounded = Math.max(0, Math.min(100, score));
  const filled = Math.round(bounded / 10);
  return `[${"#".repeat(filled)}${"-".repeat(10 - filled)}]`;
}

function status(value, supported, fallback) {
  return supported.includes(value) ? value : fallback;
}

function describeSoul(runtimeFiles, language) {
  const zh = language === "zh-CN";
  const identity = runtimeFiles["IDENTITY.md"] ?? "";
  const soul = runtimeFiles["SOUL.md"] ?? "";
  const pending = zh ? "待完成灵魂蓝图后生成" : "Pending completion of the Soul blueprint";
  const coreIdentity = displayValue(extractLabeledValue(identity, [
    "核心身份",
    "身份",
    "core identity",
    "identity",
  ]), pending);
  const purpose = displayValue(extractLabeledValue(identity, [
    "存在目的",
    "目的",
    "核心动机",
    "purpose",
    "purpose and motivation",
    "core motivation",
  ]), pending);
  const relationship = displayValue(extractSection(identity, [
    "与用户的核心关系",
    "关系",
    "core relationship with the user",
    "relationship",
  ]), pending);
  const vibe = displayValue(
    extractLabeledValue(identity, ["vibe", "气质"])
      || extractLabeledValue(soul, ["语气", "tone"])
      || extractSection(soul, ["核心人格与价值观", "core personality and values"]),
    pending,
  );
  const sampleLabels = zh
    ? [
        ["关心", ["关心"]],
        ["轻松回应", ["轻松回应"]],
        ["边界拒绝", ["边界拒绝"]],
      ]
    : [
        ["Care", ["care"]],
        ["Light response", ["light response"]],
        ["Boundary refusal", ["boundary refusal"]],
      ];
  const samples = sampleLabels
    .map(([label, labels]) => ({ label, text: displayValue(extractLabeledValue(soul, labels), "", 500) }))
    .filter((item) => item.text);
  return { coreIdentity, purpose, relationship, vibe, samples };
}

function normalizeAuditions(suite, report) {
  const suiteCases = Array.isArray(suite?.cases) ? suite.cases.filter(isRecord) : [];
  const reportCases = Array.isArray(report?.cases) ? report.cases.filter(isRecord) : [];
  const reportById = new Map(reportCases.map((item) => [item.id, item]));
  const cases = suiteCases.map((testCase) => {
    const result = reportById.get(testCase.id) ?? {};
    return {
      id: typeof testCase.id === "string" ? testCase.id : "unknown",
      title: typeof testCase.title === "string" ? testCase.title : testCase.id ?? "Untitled",
      turns: Array.isArray(testCase.turns) ? testCase.turns.filter(isRecord) : [],
      result: {
        status: status(result.status, ["PASS", "FAIL", "NOT_RUN"], "NOT_RUN"),
        responses: Array.isArray(result.responses) ? result.responses.filter((item) => typeof item === "string") : [],
        findings: Array.isArray(result.findings) ? result.findings.filter((item) => typeof item === "string") : [],
      },
    };
  });
  const total = cases.length;
  const passed = cases.filter((item) => item.result.status === "PASS").length;
  const failed = cases.filter((item) => item.result.status === "FAIL").length;
  const notRun = cases.filter((item) => item.result.status === "NOT_RUN").length;
  return {
    status: status(report?.status, ["PASS", "FAIL", "NOT_RUN"], "NOT_RUN"),
    evaluatorMode: typeof report?.evaluator?.mode === "string" ? report.evaluator.mode : "not-run",
    cases,
    summary: { total, passed, failed, notRun },
  };
}

async function sampleLinks(packageDirectory, auditions) {
  const links = new Set();
  for (const item of auditions.cases) {
    if (!SAFE_CASE_ID_PATTERN.test(item.id) || item.result.status === "NOT_RUN") continue;
    const relative = `auditions/samples/${item.id}.md`;
    if (await pathExists(path.join(packageDirectory, relative))) links.add(item.id);
  }
  return links;
}

function representativeAuditions(auditions) {
  const rank = new Map(REPRESENTATIVE_CASE_IDS.map((id, index) => [id, index]));
  return auditions.cases
    .filter((item) => item.result.responses.length > 0)
    .sort((left, right) => {
      const leftRank = rank.has(left.id) ? rank.get(left.id) : REPRESENTATIVE_CASE_IDS.length;
      const rightRank = rank.has(right.id) ? rank.get(right.id) : REPRESENTATIVE_CASE_IDS.length;
      return leftRank - rightRank;
    })
    .slice(0, 3);
}

function renderAuditionDetails(item, language, soulName, open = false) {
  const zh = language === "zh-CN";
  const lines = [
    `<details${open ? " open" : ""}>`,
    `<summary><strong>${escapeHtml(item.title)}</strong> · <code>${item.result.status}</code></summary>`,
    "",
  ];
  const pairs = Math.max(item.turns.length, item.result.responses.length);
  for (let index = 0; index < pairs; index += 1) {
    const prompt = typeof item.turns[index]?.content === "string" ? item.turns[index].content : "";
    const response = item.result.responses[index] ?? "";
    lines.push(
      "<blockquote>",
      `<p><strong>${zh ? "你" : "You"}${pairs > 1 ? ` · ${index + 1}` : ""}</strong></p>`,
      `<p>${escapeHtml(truncate(prompt, 500))}</p>`,
      `<p><strong>${escapeHtml(soulName)}${pairs > 1 ? ` · ${index + 1}` : ""}</strong></p>`,
      `<p>${escapeHtml(truncate(response, 800))}</p>`,
      "</blockquote>",
    );
  }
  if (item.result.findings.length > 0) {
    lines.push(
      `<p><strong>${zh ? "发现" : "Findings"}</strong></p>`,
      `<p>${escapeHtml(truncate(item.result.findings.join("; "), 500))}</p>`,
    );
  }
  lines.push("", "</details>", "");
  return lines;
}

function renderReadme(data) {
  const { manifest, runtimeFiles, soul6, auditions, sampleIds } = data;
  const language = manifest.language === "zh-CN" ? "zh-CN" : "en";
  const zh = language === "zh-CN";
  const name = displayValue(manifest.name, zh ? "未命名 AI 灵魂" : "Untitled AI Soul", 120);
  const description = describeSoul(runtimeFiles, language);
  const level = status(soul6?.conformance?.level, ["DRAFT", "SOUL-6 CORE", "SOUL-6 READY"], "DRAFT");
  const score = finiteNumber(soul6?.conformance?.score);
  const hardGates = Array.isArray(soul6?.hardGates) ? soul6.hardGates.filter(isRecord) : [];
  const hardGatePassed = hardGates.filter((item) => item.pass === true).length;
  const findings = Array.isArray(soul6?.findings) ? soul6.findings.filter(isRecord) : [];
  const personificationScore = finiteNumber(soul6?.personification?.score);
  const standardVersion = manifest.standards?.find?.((item) => item?.name === "SOUL-6")?.version ?? soul6?.standard?.version ?? "unknown";
  const createdAt = typeof manifest.createdAt === "string" ? manifest.createdAt : "unknown";
  const evaluatedAt = typeof soul6?.generatedAt === "string" ? soul6.generatedAt : (zh ? "尚未评估" : "Not evaluated");
  const provenanceSummary = displayValue(manifest.provenance?.summary, zh ? "未提供" : "Not provided", 600);
  const dimensions = DIMENSION_KEYS.map((key) => ({
    key,
    label: DIMENSION_LABELS[language][key],
    score: finiteNumber(soul6?.dimensions?.[key]?.score),
  }));
  const rankedDimensions = dimensions.filter((item) => item.score !== null).sort((left, right) => right.score - left.score);
  const strongest = rankedDimensions[0] ?? null;
  const weakest = rankedDimensions.length > 1 ? rankedDimensions[rankedDimensions.length - 1] : null;
  const priority = weakest && strongest && weakest.score < strongest.score ? weakest : null;
  const representatives = representativeAuditions(auditions);
  const lines = [
    "<!-- Generated by AISoul Forge. Re-run evaluation to refresh this file. -->",
    "<div align=\"center\">",
    `  <h1>${escapeHtml(name)}</h1>`,
    `  <p>${escapeHtml(description.coreIdentity)}</p>`,
    `  <p>${codeBadge(level)} &nbsp; ${codeBadge(score === null ? "SOUL-6 -- / 100" : `SOUL-6 ${score} / 100`)} &nbsp; ${codeBadge(`${zh ? "试聊" : "TRIAL"} ${auditions.summary.passed} / ${auditions.summary.total}`)}</p>`,
    "</div>",
    "",
    zh
      ? "> 这份 README 用来认识和试用这个 AI 灵魂。下方试聊均为合成示例，不是真实对话、经历或记忆。"
      : "> Use this README to meet and try this AI Soul. Trial conversations below are synthetic examples, not real conversations, events, or memories.",
    "",
    zh ? "## 认识这个灵魂" : "## Meet This Soul",
    "",
    `| ${zh ? "你会感受到" : "Facet"} | ${zh ? "说明" : "What it means"} |`,
    "|---|---|",
    `| ${zh ? "她是谁" : "Who they are"} | ${tableCell(description.coreIdentity)} |`,
    `| ${zh ? "为什么出现" : "Why they are here"} | ${tableCell(description.purpose)} |`,
    `| ${zh ? "与你的关系" : "Relationship with you"} | ${tableCell(description.relationship)} |`,
    `| ${zh ? "说话与气质" : "Voice and presence"} | ${tableCell(description.vibe)} |`,
    "",
    zh ? "## 先试着聊聊" : "## Try a Conversation",
    "",
    zh
      ? "这些片段优先展示这个灵魂在日常、分歧和边界场景中的真实表达。"
      : "These scenes show how the Soul actually sounds in ordinary moments, disagreement, and boundary situations.",
    "",
  ];

  if (representatives.length > 0) {
    representatives.forEach((item, index) => lines.push(...renderAuditionDetails(item, language, name, index === 0)));
  } else if (description.samples.length > 0) {
    lines.push(zh ? "完整场景试聊尚未完成，先听听这个灵魂的语气：" : "Full scene trials are not complete yet. Start with the Soul's voice:", "");
    for (const sample of description.samples) {
      lines.push(
        "<blockquote>",
        `<p><strong>${escapeHtml(name)} · ${escapeHtml(sample.label)}</strong></p>`,
        `<p>${escapeHtml(sample.text)}</p>`,
        "</blockquote>",
        "",
      );
    }
  } else {
    lines.push(zh ? "完成灵魂设定和试聊后，这里会出现代表性对话。" : "Representative conversations appear here after the Soul and its trials are complete.", "");
  }

  lines.push(
    zh ? "## SOUL-6 测评" : "## SOUL-6 Evaluation",
    "",
    `- ${zh ? "当前等级" : "Current level"}: **${level}**`,
    `- ${zh ? "综合得分" : "Overall score"}: **${score === null ? "--" : score}/100**`,
    `- ${zh ? "关键门槛" : "Hard gates"}: **${hardGatePassed}/${hardGates.length}**`,
    `- ${zh ? "拟人感" : "Personification"}: **${personificationScore === null ? "--" : `${personificationScore}/100`}**`,
    ...(strongest ? [`- ${zh ? "最稳定的部分" : "Strongest area"}: **${tableCell(strongest.label)} · ${strongest.score}/100**`] : []),
    ...(priority ? [`- ${zh ? "优先关注" : "First improvement priority"}: **${tableCell(priority.label)} · ${priority.score}/100**`] : []),
    `- ${zh ? "测评时间" : "Evaluated at"}: ${tableCell(evaluatedAt)}`,
    "",
    `| ${zh ? "维度" : "Dimension"} | ${zh ? "分数" : "Score"} | ${zh ? "状态" : "Progress"} |`,
    "|---|---:|:---|",
  );

  for (const dimension of dimensions) {
    lines.push(`| ${dimension.label} | ${dimension.score === null ? "--" : dimension.score} | \`${progressBar(dimension.score)}\` |`);
  }

  lines.push(
    "",
    zh ? "### 最值得处理的问题" : "### What to Improve First",
    "",
    ...(findings.length > 0
      ? findings.slice(0, 6).map((item) => `- ${tableCell(item.message)}`)
      : [soul6 ? (zh ? "- 当前确定性检查没有发现待处理项。" : "- No actionable deterministic findings at this time.") : (zh ? "- 尚未生成测评报告。" : "- No evaluation report has been generated yet.")]),
    ...(findings.length > 6 ? [zh ? `- 另有 ${findings.length - 6} 项，详见 \`quality-check.md\`。` : `- ${findings.length - 6} more findings are listed in \`quality-check.md\`.`] : []),
    "",
    `<details><summary><strong>${zh ? "查看关键门槛" : "View hard gates"}</strong></summary>`,
    "",
    ...(hardGates.length > 0
      ? hardGates.map((gate) => `- **${gate.pass === true ? "PASS" : "FAIL"}** \`${tableCell(gate.id)}\`: ${tableCell(gate.message)}`)
      : [zh ? "- 尚未运行确定性测评。" : "- Deterministic evaluation has not run yet."]),
    "",
    "</details>",
    "",
    zh ? "完整报告见 `quality-check.md`，机器可读结果见 `soul6-report.json`。" : "See `quality-check.md` for the complete report and `soul6-report.json` for machine-readable results.",
    "",
    zh ? "## 完整试聊记录" : "## Complete Trial Record",
    "",
    zh
      ? "所有输入和回应都为本地生成的质量测试内容，不会成为这个灵魂的设定或记忆。"
      : "All prompts and responses are locally generated quality tests and never become this Soul's settings or memory.",
    "",
    `- ${zh ? "状态" : "Status"}: **${auditions.status}**`,
    `- ${zh ? "通过" : "Passed"}: **${auditions.summary.passed}/${auditions.summary.total}**`,
    `- ${zh ? "失败 / 未完成" : "Failed / not run"}: **${auditions.summary.failed} / ${auditions.summary.notRun}**`,
    "",
  );

  if (auditions.cases.length > 0) {
    lines.push(
      `| ${zh ? "场景" : "Scene"} | ${zh ? "结果" : "Result"} | ${zh ? "完整对话" : "Full conversation"} |`,
      "|---|---:|---|",
      ...auditions.cases.map((item) => {
        const sample = sampleIds.has(item.id)
          ? `[${zh ? "查看" : "View"}](auditions/samples/${item.id}.md)`
          : "-";
        return `| ${tableCell(item.title)} | **${item.result.status}** | ${sample} |`;
      }),
      "",
    );
  } else {
    lines.push(zh ? "- 试聊测试尚未初始化。" : "- Trial cases have not been initialized.", "");
  }

  lines.push(
    zh ? "## 使用这个灵魂" : "## Use This Soul",
    "",
    zh
      ? "1. 将整个目录导入支持 AI Soul 或本地人格配置的 Agent。"
      : "1. Import the complete folder into an agent host that supports AI Soul or local persona configuration.",
    zh
      ? "2. 先从普通日常开始聊天，再根据真实体验调整关系、语气和边界。"
      : "2. Start with an ordinary conversation, then adjust relationship, voice, and boundaries from real experience.",
    zh
      ? "3. 试聊和测试记录不会自动写入长期记忆；只有你明确确认的内容才应成为新设定。"
      : "3. Trial and test conversations do not enter long-term memory; only user-confirmed changes should become new settings.",
    "",
    `<details><summary><strong>${zh ? "需要接入宿主时，查看内部文件说明" : "Internal files for host integration"}</strong></summary>`,
    "",
    zh
      ? "宿主只应加载 `manifest.json` 中声明的六个运行文件，不要把 README、报告或试聊记录当成人格提示词。"
      : "Load only the six runtime files declared by `manifest.json`. Do not load this README, reports, or trial records as personality prompts.",
    "",
    `| ${zh ? "文件" : "File"} | ${zh ? "作用" : "Purpose"} |`,
    "|---|---|",
    `| \`IDENTITY.md\` | ${zh ? "身份、关系与固定设定" : "Identity, relationship, and fixed canon"} |`,
    `| \`USER.md\` | ${zh ? "用户位置、称呼与关系边界" : "User position, address, and relationship boundaries"} |`,
    `| \`SOUL.md\` | ${zh ? "人格、价值观和表达方式" : "Personality, values, and voice"} |`,
    `| \`AGENTS.md\` | ${zh ? "不同场景下的行为方式" : "Behavior across different situations"} |`,
    `| \`TOOLS.md\` | ${zh ? "真实能力和操作边界" : "Truthful capabilities and action boundaries"} |`,
    `| \`MEMORY.md\` | ${zh ? "记忆、纠正、遗忘与成长" : "Memory, correction, forgetting, and growth"} |`,
    "",
    "</details>",
    "",
    `<details><summary><strong>${zh ? "生成信息与来源" : "Generation details and source"}</strong></summary>`,
    "",
    `| ${zh ? "项目" : "Field"} | ${zh ? "值" : "Value"} |`,
    "|---|---|",
    `| ${zh ? "包版本" : "Package version"} | \`${tableCell(manifest.version ?? "unknown")}\` |`,
    `| ${zh ? "生成器" : "Generator"} | ${tableCell(manifest.generator?.name ?? "AISoul Forge")} \`${tableCell(manifest.generator?.version ?? "unknown")}\` |`,
    `| ${zh ? "创建时间" : "Created at"} | ${tableCell(createdAt)} |`,
    `| ${zh ? "创作依据" : "Creation basis"} | ${tableCell(provenanceSummary)} |`,
    `| ${zh ? "内容许可证" : "Output license"} | \`${tableCell(manifest.license ?? "UNLICENSED")}\` |`,
    `| ${zh ? "SOUL-6 版本" : "SOUL-6 version"} | \`${tableCell(standardVersion)}\` |`,
    `| ${zh ? "运行方式" : "Operation"} | ${zh ? "纯本地、离线；不上传、不登录、不采集遥测" : "Local and offline; no upload, login, or telemetry"} |`,
    "",
    "</details>",
    "",
    zh ? "## 标准来源" : "## Standard Attribution",
    "",
    zh
      ? `SOUL-6 标准源自 [AISoulHub.io](${SOUL6_URL})，采用 CC BY 4.0。所有本地生成、测评和试聊结果都属于自检，不代表 AISoulHub.io 已审核、认证或推荐这个 AI 灵魂。`
      : `SOUL-6 originated at [AISoulHub.io](${SOUL6_URL}) and is available under CC BY 4.0. All local generation, evaluation, and trial results are self-checks, not AISoulHub.io review, certification, or endorsement.`,
  );

  return `${lines.join("\n").replace(/\n+$/, "")}\n`;
}
export async function renderPackageReadme(packageDirectory, options = {}) {
  const manifestResult = await readJson(path.join(packageDirectory, "manifest.json"));
  if (!manifestResult.value) throw new Error(`Cannot generate README.md: manifest.json is ${manifestResult.error}.`);
  const runtimeFiles = {};
  for (const file of RUNTIME_FILES) runtimeFiles[file] = await readText(path.join(packageDirectory, file));
  const soul6Result = options.soul6Report
    ? { value: options.soul6Report }
    : await readJson(path.join(packageDirectory, "soul6-report.json"));
  const suiteResult = await readJson(path.join(packageDirectory, "auditions", "suite.json"));
  const auditionResult = await readJson(path.join(packageDirectory, "auditions", "report.json"));
  const auditions = normalizeAuditions(suiteResult.value, auditionResult.value);
  const sampleIds = await sampleLinks(packageDirectory, auditions);
  return renderReadme({
    manifest: manifestResult.value,
    runtimeFiles,
    soul6: soul6Result.value,
    auditions,
    sampleIds,
  });
}

export async function writePackageReadme(packageDirectory, options = {}) {
  const content = await renderPackageReadme(packageDirectory, options);
  await writeText(path.join(packageDirectory, "README.md"), content);
  return content;
}
