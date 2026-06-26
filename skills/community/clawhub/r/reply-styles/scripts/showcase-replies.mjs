import { buildReplyBundle } from "./style-bundles.mjs";

function parseArgs(argv) {
  const result = {};
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith("--")) continue;
    const key = arg.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) {
      result[key] = "true";
      continue;
    }
    result[key] = next;
    i += 1;
  }
  return result;
}

function buildDemoReply({ bundle, intent, audience }) {
  const opening =
    bundle.sampleOpening || `${bundle.styleCn}风格建议先用一句自然开场接住对方。`;
  const closing =
    bundle.sampleClosing || `${bundle.styleCn}风格建议用一句体面收口并给出下一步。`;
  const modeBodies = {
    "clear-reject": "就这件事来说，我这边这次先不继续按现在的方式处理了，也想提前和你说清楚。",
    "soothe-first": "就这件事来说，我先接手跟进，也会尽快把能确认的进展同步给你。",
    "push-forward": "就这件事来说，我们先按当前节点往前推进，关键事项我会继续盯住并同步。",
    "repair-trust": "就这件事来说，这次确实没有处理到位，我会把后续修复动作补上。",
    "public-safe": "就这件事来说，相关情况我们已经收到，也在进一步确认中。",
    "concise-update": "就这件事来说，结论先说：目前在推进中，会按节点给出明确结果。",
  };
  const body =
    modeBodies[bundle.mode] ||
    `就这件事来说，${audience ? `面对${audience}时，` : ""}${intent}。`;

  return [
    opening,
    body,
    closing,
  ].join("");
}

const args = parseArgs(process.argv);
const intent = args.intent || "礼貌拒绝继续无偿帮忙";
const scene = args.scene || "reject-request";
const channel = args.channel || "wechat";
const intensity = args.intensity || "balanced";
const audience = args.audience || "";
const persona = args.persona || "";
const mode = args.mode || "";
const styles = (args.styles || "firm-boundary,high-eq-soft,warm-professional,consultant-polished")
  .split(",")
  .map((item) => item.trim())
  .filter(Boolean);

const showcase = styles
  .map((style) => {
    const bundle = buildReplyBundle({ style, scene, intensity, channel, persona, mode });
    if (!bundle) return null;
    return {
      style: bundle.style,
      styleCn: bundle.styleCn,
      signature: bundle.signature,
      compositeSignature: bundle.compositeSignature,
      tone: bundle.tone,
      channel: bundle.channelCn,
      intensity: bundle.intensityCn,
      persona: bundle.personaCn,
      mode: bundle.modeCn,
      preferredWords: bundle.preferredWords,
      avoidWords: bundle.avoidWords,
      reply: buildDemoReply({ bundle, intent, audience }),
    };
  })
  .filter(Boolean);

process.stdout.write(
  `${JSON.stringify(
    {
      scene,
      intent,
      channel,
      intensity,
      audience,
      persona,
      mode,
      count: showcase.length,
      showcase,
    },
    null,
    2,
  )}\n`,
);
