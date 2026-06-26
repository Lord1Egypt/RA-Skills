import type { ComplianceOutput, ScriptOutput, TopicItem } from "../schemas/output-schema";

export function applyTopicFallback(items: Partial<TopicItem>[], targetAudience = "泛人群"): TopicItem[] {
  if (items.length === 0) {
    return [
      {
        title: "为什么你发了很多内容，还是没人来咨询",
        category: "痛点",
        angle: "从内容不等于信任切入",
        targetAudience,
      },
    ];
  }

  return items.map((item, index) => ({
    title: item.title?.trim() || `待优化选题 ${index + 1}`,
    category: (item.category as TopicItem["category"]) || "观点",
    angle: item.angle?.trim() || "从用户痛点切入",
    targetAudience: item.targetAudience?.trim() || targetAudience,
  }));
}

export function applyScriptFallback(output: Partial<ScriptOutput>, topic: string): ScriptOutput {
  return {
    positioning: output.positioning?.trim() || `围绕“${topic}”输出一个适合视频号口播的核心观点。`,
    titles: output.titles && output.titles.length > 0 ? output.titles : [
      `${topic}`,
      `很多人没看懂：${topic}`,
      `真正的问题不是贵，而是你不会讲`,
      `为什么同样的项目，别人更容易成交`,
      `把价值讲明白，客户才愿意买单`,
    ],
    hook: output.hook?.trim() || `你以为客户是在嫌贵，其实很多时候，是你根本没把价值讲明白。`,
    script: output.script?.trim() || [
      `开头钩子：你以为客户是在嫌贵，其实不是。`,
      `问题展开：很多机构一讲项目，就只会讲价格和活动，客户当然没有感觉。`,
      `核心观点：客户不是嫌贵，是你不会讲价值。`,
      `解决方案：第一，先讲客户为什么需要；第二，讲清和普通方案的差别；第三，讲结果预期时要真实、克制。`,
      `结尾引导：如果你也在做内容获客，先把价值表达练好。`,
    ].join("\n"),
    shotList: output.shotList && output.shotList.length > 0 ? output.shotList : [
      "镜头1：正面口播，直接抛出反常识观点",
      "镜头2：插入机构常见错误表达示例",
      "镜头3：回到正面口播，给出3点方法",
      "镜头4：结尾收口，引导评论互动",
    ],
    coverText: output.coverText?.trim() || "客户不是嫌贵，是你不会讲价值",
    publishCaption: output.publishCaption?.trim() || `很多机构不是产品有问题，而是表达有问题。把价值讲明白，内容才有转化。`,
    commentCTA: output.commentCTA?.trim() || "你觉得客户更在意价格，还是更在意你有没有把价值讲清楚？",
  };
}

export function applyComplianceFallback(output: Partial<ComplianceOutput>): ComplianceOutput {
  return {
    issues: output.issues && output.issues.length > 0 ? output.issues : [
      {
        originalText: "内容中可能存在绝对化或效果承诺表达。",
        riskType: "绝对化表达",
        reason: "平台与医美内容通常不适合使用保证性、唯一性、绝对有效等说法。",
        suggestion: "改为更克制、基于个体差异的描述，并增加评估前置表达。",
      },
    ],
    revisedVersion: output.revisedVersion?.trim() || "建议改为：先做专业评估，再根据个人情况选择更合适的方案，效果呈现也会因人而异。",
    safeTitles: output.safeTitles && output.safeTitles.length > 0 ? output.safeTitles : [
      "做项目之前，先把适合不适合讲清楚",
      "内容想有吸引力，也要先过合规这一关",
    ],
    safeCaption: output.safeCaption?.trim() || "表达可以有吸引力，但更重要的是真实、克制、可公开传播。",
  };
}
