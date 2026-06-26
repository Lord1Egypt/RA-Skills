const test = require("node:test");
const assert = require("node:assert/strict");
const { execFileSync } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");

const { generateScript } = require("../dist/services/generateScript.js");
const { generateTopics } = require("../dist/services/generateTopics.js");
const { checkCompliance } = require("../dist/services/checkCompliance.js");
const { rewriteStyle } = require("../dist/services/rewriteStyle.js");
const { runOpenClawSkill, validateOpenClawSkillRequest, getSupportedActions } = require("../dist/index.js");
const { resolveScriptOutputFields } = require("../dist/lib/scriptOutput.js");
const { resolveTopicOutputFields } = require("../dist/lib/topicOutput.js");
const { resolveComplianceOutputFields } = require("../dist/lib/complianceOutput.js");
const { resolveRewriteProfile } = require("../dist/lib/rewriteOutput.js");
const { validateAllConfigs } = require("../dist/validate-config.js");

test("generateScript returns parsed structured content with a mock model", async () => {
  const mockInvokeModel = async (prompt) => {
    assert.match(prompt, /# System/);
    assert.match(prompt, /# Persona/);
    assert.match(prompt, /# Task/);

    return JSON.stringify({
      positioning: "面向医美老板，讲清价值表达为什么决定成交。",
      titles: ["客户不是嫌贵，是你没讲清价值"],
      hook: "客户一说贵，你就降价，这才是最大的问题。",
      script: "开头钩子：客户一说贵，你就降价，这才是最大的问题。\n问题展开：你总在讲活动，不在讲价值。\n核心观点：客户不是嫌贵，是你没讲清价值。\n解决方案：第一，先讲客户在意什么；第二，讲你方案为什么不一样。\n结尾引导：如果你也有这个问题，先把表达改掉。",
      shotList: ["镜头1：正面口播", "镜头2：举错误案例"],
      coverText: "不是嫌贵，是没讲清价值",
      publishCaption: "内容能不能转化，先看你会不会讲价值。",
      commentCTA: "你遇到过一开口就被说贵吗？",
    });
  };

  const result = await generateScript(
    {
      topic: "客户不是嫌贵，是你没讲清价值",
      style: "老板表达型",
      scriptStructure: "boss_point_v1",
    },
    mockInvokeModel,
  );

  assert.equal(result.titles[0], "客户不是嫌贵，是你没讲清价值");
  assert.equal(result.coverText, "不是嫌贵，是没讲清价值");
  assert.match(result.script, /核心观点：客户不是嫌贵，是你没讲清价值。/);
  assert.equal(result.publishCaption, "内容能不能转化，先看你会不会讲价值。");
});

test("generateScript injects configured script structure into prompt", async () => {
  let capturedPrompt = "";
  const mockInvokeModel = async (prompt) => {
    capturedPrompt = prompt;
    return "{}";
  };

  await generateScript(
    {
      topic: "老板为什么总觉得内容没用",
      scriptStructure: "boss_point_v1",
    },
    mockInvokeModel,
  );

  assert.match(capturedPrompt, /脚本结构：boss_point_v1/);
  assert.match(capturedPrompt, /输出包配置：full_publish_pack/);
  assert.match(capturedPrompt, /输出字段：positioning/);
  assert.match(capturedPrompt, /scriptStructuresConfig/);
  assert.match(capturedPrompt, /scriptOutputProfilesConfig/);
  assert.match(capturedPrompt, /老板观点表达式/);
});

test("generateScript supports output profile pruning", async () => {
  const result = await generateScript(
    {
      topic: "老板为什么总觉得内容没用",
      outputProfile: "lite_publish_pack",
      includeShotList: false,
      includePublishCaption: false,
      includeCommentCTA: false,
    },
    async () => JSON.stringify({
      titles: ["内容没效果，不是因为你发少了"],
      hook: "你以为是发少了，其实是内容根本没打中。",
      script: "开头钩子：你以为是发少了，其实不是。\n问题展开：你一直在发，但没观点。\n核心观点：不是发少了，是没打中。\n解决方案：第一，先讲判断；第二，再讲方法。\n结尾引导：留言说说你卡在哪。",
      coverText: "不是发少了，是没打中",
      publishCaption: "这条应该被裁掉",
      commentCTA: "这条也应该被裁掉",
      shotList: ["这条也应该被裁掉"],
    }),
  );

  assert.deepEqual(Object.keys(result).sort(), ["coverText", "hook", "script", "titles"]);
  assert.equal(result.coverText, "不是发少了，是没打中");
});

test("resolveScriptOutputFields respects output profile and include flags", () => {
  const fields = resolveScriptOutputFields({
    outputProfile: "full_publish_pack",
    includeShotList: false,
    includePublishCaption: false,
  });

  assert.deepEqual(fields, [
    "positioning",
    "titles",
    "hook",
    "script",
    "coverText",
    "commentCTA",
  ]);
});

test("generateTopics injects output profile into prompt", async () => {
  let capturedPrompt = "";
  await generateTopics(
    {
      direction: "机构经营",
      targetAudience: "医美老板",
    },
    async (prompt) => {
      capturedPrompt = prompt;
      return "[]";
    },
  );

  assert.match(capturedPrompt, /输出包配置：default_topics/);
  assert.match(capturedPrompt, /输出字段：title/);
  assert.match(capturedPrompt, /topicOutputProfilesConfig/);
});

test("checkCompliance supports issues_only output profile", async () => {
  const result = await checkCompliance(
    {
      script: "这个项目百分百有效，谁做谁变年轻。",
      outputProfile: "issues_only",
    },
    async () => JSON.stringify({
      issues: [
        {
          originalText: "百分百有效",
          riskType: "绝对化表达",
          reason: "保证性表述",
          suggestion: "改成个体化表达",
        },
      ],
      revisedVersion: "这条应该被裁掉",
      safeCaption: "这条也应该被裁掉",
    }),
  );

  assert.deepEqual(Object.keys(result), ["issues"]);
  assert.equal(result.issues[0].riskType, "绝对化表达");
});

test("resolveTopicOutputFields and resolveComplianceOutputFields read configured profiles", () => {
  assert.deepEqual(resolveTopicOutputFields(), ["title", "category", "angle", "targetAudience"]);
  assert.deepEqual(resolveComplianceOutputFields("issues_only"), ["issues"]);
});

test("rewriteStyle injects rewrite profile into prompt", async () => {
  let capturedPrompt = "";
  const result = await rewriteStyle(
    {
      originalScript: "客户不是嫌贵，是你不会讲价值。",
      rewriteProfile: "boss_only",
    },
    async (prompt) => {
      capturedPrompt = prompt;
      return "[]";
    },
  );

  assert.match(capturedPrompt, /改写配置：/);
  assert.match(capturedPrompt, /boss_only/);
  assert.match(capturedPrompt, /rewriteProfilesConfig/);
  assert.equal(result[0].style, "老板表达型");
});

test("resolveRewriteProfile reads configured style sets", () => {
  const profile = resolveRewriteProfile("boss_only");
  assert.deepEqual(profile.styles, ["老板表达型"]);
  assert.deepEqual(profile.fields, ["style", "content"]);
});

test("validateAllConfigs passes for current config set", () => {
  const files = validateAllConfigs();
  assert(files.includes("rewrite-profiles.json"));
  assert.equal(files.length, 8);
});

test("runOpenClawSkill dispatches script action with injected invoker", async () => {
  const mockInvoker = async () => JSON.stringify({
    positioning: "这是定位",
    titles: ["这是标题"],
    hook: "这是钩子",
    script: "开头钩子：这是钩子。\n问题展开：这是问题。\n核心观点：这是核心。\n解决方案：第一，先说人话；第二，再说价值。\n结尾引导：欢迎留言。",
    shotList: ["镜头1：口播"],
    coverText: "这是封面",
    publishCaption: "这是发布文案",
    commentCTA: "这是评论引导",
  });

  const result = await runOpenClawSkill(
    {
      action: "script",
      payload: { topic: "测试主题" },
    },
    { invoker: mockInvoker },
  );

  assert.equal(result.titles[0], "这是标题");
  assert.equal(result.commentCTA, "这是评论引导");
});

test("validateOpenClawSkillRequest rejects invalid payloads", () => {
  assert.throws(
    () => validateOpenClawSkillRequest({ action: "script", payload: {} }),
    /"topic" must be a non-empty string/,
  );

  assert.throws(
    () => validateOpenClawSkillRequest({ action: "unknown", payload: {} }),
    /Invalid action/,
  );
});

test("runOpenClawSkill dispatches topics action", async () => {
  const result = await runOpenClawSkill(
    {
      action: "topics",
      payload: { direction: "机构经营", targetAudience: "医美老板" },
    },
    {
      invoker: async () => JSON.stringify([
        {
          title: "为什么内容做了很多，咨询还是没起色",
          category: "痛点",
          angle: "从信任缺失切入",
          targetAudience: "医美老板",
        },
      ]),
    },
  );

  assert.equal(result[0].category, "痛点");
  assert.equal(result[0].targetAudience, "医美老板");
});

test("runOpenClawSkill dispatches rewrite action", async () => {
  const result = await runOpenClawSkill(
    {
      action: "rewrite",
      payload: { originalScript: "客户不是嫌贵，是你不会讲价值。" },
    },
    {
      invoker: async () => JSON.stringify([
        {
          style: "犀利观点型",
          content: "客户不是嫌贵，是你根本没把价值说到点上。",
        },
      ]),
    },
  );

  assert.equal(result[0].style, "犀利观点型");
  assert.match(result[0].content, /价值/);
});

test("runOpenClawSkill dispatches compliance action", async () => {
  const result = await runOpenClawSkill(
    {
      action: "compliance",
      payload: { script: "这个项目百分百有效，谁做谁变年轻。" },
    },
    {
      invoker: async () => JSON.stringify({
        issues: [
          {
            originalText: "百分百有效",
            riskType: "绝对化表达",
            reason: "属于保证性表述",
            suggestion: "改为更克制的个体化表达",
          },
        ],
        revisedVersion: "建议先评估个人情况，再选择合适方案。",
        safeTitles: ["做项目前，先看自己适不适合"],
        safeCaption: "内容表达要克制，决策前先评估。",
      }),
    },
  );

  assert.equal(result.issues[0].riskType, "绝对化表达");
  assert.match(result.revisedVersion, /评估/);
});

test("cli shows help text", () => {
  const output = execFileSync("node", ["dist/openclaw.js", "--help"], {
    cwd: path.resolve(__dirname, ".."),
    encoding: "utf8",
  });

  assert.match(output, /Usage:/);
  assert.match(output, /--action <name>/);
  assert.deepEqual(getSupportedActions(), ["topics", "script", "rewrite", "compliance"]);
});

test("cli accepts action with payload-file", () => {
  const fixturePath = path.resolve(__dirname, "fixtures", "script-request.json");
  const mockResponse = JSON.stringify({
    positioning: "围绕主题输出一个核心观点。",
    titles: ["客户不是嫌贵，是你不会讲价值"],
    hook: "你以为客户在嫌贵，其实不是。",
    script: "开头钩子：你以为客户在嫌贵，其实不是。\n问题展开：很多内容只会讲活动。\n核心观点：客户不是嫌贵，是你不会讲价值。\n解决方案：第一，先讲需求；第二，再讲差异。\n结尾引导：把价值先讲明白。",
    shotList: ["镜头1：口播"],
    coverText: "客户不是嫌贵，是你不会讲价值",
    publishCaption: "价值讲清楚，转化才会起来。",
    commentCTA: "你会先讲价格还是先讲价值？",
  });

  const output = execFileSync(
    "node",
    ["dist/openclaw.js", "--action", "script", "--payload-file", fixturePath],
    {
      cwd: path.resolve(__dirname, ".."),
      encoding: "utf8",
      env: {
        ...process.env,
        MODEL_MOCK_RESPONSE: mockResponse,
      },
    },
  );

  const parsed = JSON.parse(output);
  assert.equal(parsed.coverText, "客户不是嫌贵，是你不会讲价值");
  assert.match(parsed.script, /核心观点：客户不是嫌贵，是你不会讲价值。/);
});

test("examples request files are valid skill requests", () => {
  const requestsDir = path.resolve(__dirname, "..", "examples", "requests");
  const fileNames = fs.readdirSync(requestsDir).filter((name) => name.endsWith(".json")).sort();

  assert.deepEqual(fileNames, ["compliance.json", "rewrite.json", "script.json", "topics.json"]);

  for (const fileName of fileNames) {
    const content = JSON.parse(fs.readFileSync(path.join(requestsDir, fileName), "utf8"));
    const validated = validateOpenClawSkillRequest(content);
    assert.equal(typeof validated.action, "string");
    assert.equal(typeof validated.payload, "object");
  }
});

test("package.json exposes check and validate-config scripts", () => {
  const packageJson = JSON.parse(
    fs.readFileSync(path.resolve(__dirname, "..", "package.json"), "utf8"),
  );

  assert.equal(packageJson.scripts.check, "npm run build && npm run validate-config && npm test");
  assert.equal(packageJson.scripts["validate-config"], "npm run build && node dist/validate-config.js");
});

test("package and skill versions stay aligned for publishing", () => {
  const packageJson = JSON.parse(
    fs.readFileSync(path.resolve(__dirname, "..", "package.json"), "utf8"),
  );
  const skillMd = fs.readFileSync(path.resolve(__dirname, "..", "SKILL.md"), "utf8");
  const skillVersionMatch = skillMd.match(/^version:\s*(.+)$/m);

  assert(skillVersionMatch);
  assert.equal(skillVersionMatch[1].trim(), packageJson.version);
});
