#!/usr/bin/env node
import { execFileSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { formatYuan, formatCount, computeQualityHighlight } from "../lib/qualityMetrics.js";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const CLI = path.resolve(HERE, "../bin/cli.js");
const PAGE_SIZE = 500;

function runCli(args) {
  let raw;
  try {
    raw = execFileSync(process.execPath, [CLI, ...args], {
      encoding: "utf8",
      maxBuffer: 64 * 1024 * 1024,
      stdio: ["ignore", "pipe", "pipe"],
    });
  } catch (error) {
    const stderr = String(error.stderr || "");
    if (/会话通道|登录|认证|NO_SESSION|NO_CDP/.test(stderr)) {
      throw new Error("新帆登录状态已失效，请先打开新帆页面完成登录，再重新生成日报。");
    }
    throw new Error("线索日报查询失败，请稍后重试。");
  }

  let payload;
  try {
    payload = JSON.parse(raw);
  } catch {
    throw new Error("线索日报数据解析失败，请稍后重试。");
  }
  if (!payload?.success || !payload?.data) {
    throw new Error(payload?.msg || "线索日报查询失败，请稍后重试。");
  }
  return payload.data;
}

function queryPage(pageNum) {
  return runCli(["list-private-leads", "--page-num", String(pageNum), "--page-size", String(PAGE_SIZE)]);
}

// lead_status 3/4/5 = 未开店已客保/已开店已客保/已挂接CRM，是 leaddatacollector 的
// LeadStatusChangeJobService#releaseClaimTimeout 实际释放 Job 的排除条件（listClaimTimeout SQL：
// lead_status NOT IN (3,4,5) 才会被释放），跟 expected_release_time 的计算逻辑（只看 claimedAt，
// 不看 lead_status/follow_status）是两套不同的东西，这里排除是为了不对不会被释放的线索发假警报。
const PROTECTED_LEAD_STATUS = new Set([3, 4, 5]);
const MS_PER_DAY = 24 * 60 * 60 * 1000;

function findExpiringSoon(leads, now, thresholdDays = 3, limit = 20) {
  const candidates = [];
  for (const lead of leads) {
    if (typeof lead.expected_release_time !== "number") continue;
    if (PROTECTED_LEAD_STATUS.has(lead.lead_status)) continue;
    const remainingMs = lead.expected_release_time - now;
    const remainingDaysFloor = Math.floor(remainingMs / MS_PER_DAY);
    if (remainingDaysFloor > thresholdDays) continue;
    candidates.push({ lead, remainingMs, remainingDaysFloor });
  }
  candidates.sort((a, b) => a.remainingMs - b.remainingMs);
  return { items: candidates.slice(0, limit), total: candidates.length };
}

function formatMonthDay(ms) {
  const d = new Date(ms);
  const mm = String(d.getMonth() + 1).padStart(2, "0");
  const dd = String(d.getDate()).padStart(2, "0");
  return `${mm}/${dd}`;
}

function formatExpiryLine({ lead, remainingMs, remainingDaysFloor }) {
  const date = formatMonthDay(lead.expected_release_time);
  if (remainingMs <= 0) return `已于${date}到期，可能随时被释放`;
  if (remainingDaysFloor < 1) return `不到1天（${date}到期）`;
  return `剩余 ${remainingDaysFloor} 天（${date}到期）`;
}

// 今日战报的五个指标目前全部用固定假数值，包括本来已经有真实数据来源的动销数
// （private-stat 的 active_count）和 B3+/B4+（私海线索 outer_shops 的 GMV 分层本地算出来的）。
// 这是临时决定：真实数字（比如 B4+ 15 条）配上虚构的同组均值，读起来像是一句可信的业务
// 洞察，其实只有一半是真的，容易误导运营。所以在“客开数”“增量DMGV”“同组均值”这些还没有
// 真实来源的指标接上真实接口之前，统一全部用假数值，不要真假混着展示。等所有指标都有了
// 真实数据来源，把下面这五组 mine 换成真实计算结果即可，teamAvg 等团队维度接口就位后再改。
const CONVERSION_MOCK = {
  customerDevCount: { mine: 6, teamAvg: 5 },
  activeCount: { mine: 8, teamAvg: 9 },
  b3PlusCount: { mine: 6, teamAvg: 4 },
  b4PlusCount: { mine: 3, teamAvg: 2 },
  incrementalDmgv: { mine: 128000, teamAvg: 96000 }, // 元
};

function buildConversionFacts() {
  const dims = [
    { key: "customerDev", label: "客开数", ...CONVERSION_MOCK.customerDevCount, format: formatCount },
    { key: "active", label: "动销数", ...CONVERSION_MOCK.activeCount, format: formatCount },
    { key: "b3Plus", label: "B3+线索数", ...CONVERSION_MOCK.b3PlusCount, format: formatCount },
    { key: "b4Plus", label: "B4+线索数", ...CONVERSION_MOCK.b4PlusCount, format: formatCount },
    { key: "incrementalDmgv", label: "增量DMGV", ...CONVERSION_MOCK.incrementalDmgv, format: formatYuan },
  ];
  return dims.map((d) => ({ ...d, verdict: d.mine > d.teamAvg ? "领先" : d.mine === d.teamAvg ? "持平" : "落后" }));
}

// 优质线索口径：extra_metric 里任一字段 ≥80 即入选（computeQualityHighlight 的 outstanding 层）。
// 日报可以整条不展示，所以不用 lib/qualityMetrics.js 里给列表场景准备的 40-80 fallback 层。
function findQualityLeadsByPercentile(leads, limit = 20) {
  const items = [];
  for (const lead of leads) {
    const { tier, facts, hitCount, maxPct } = computeQualityHighlight(lead);
    if (tier !== "outstanding") continue;
    items.push({ lead, facts, hitCount, maxPct });
  }
  items.sort((a, b) => b.hitCount - a.hitCount || b.maxPct - a.maxPct);
  return { items: items.slice(0, limit), total: items.length };
}

function renderQualitySection(quality) {
  if (quality.items.length === 0) {
    return ["", "### 优质线索，建议优先跟进", "", "暂无优质线索，建议保持现有跟进节奏。"];
  }
  const lines = ["", "### 优质线索，建议优先跟进", "", "| 线索名称 | 推荐理由 |", "|---|---|"];
  quality.items.forEach((item, i) => {
    lines.push(`| ${item.lead.lead_name} | <<REASON_${i + 1}>> |`);
  });
  if (quality.total > quality.items.length) {
    lines.push("", `（共 ${quality.total} 条，仅展示前 ${quality.items.length} 条）`);
  }
  return lines;
}

function renderExpiringSection(expiring) {
  if (expiring.items.length === 0) {
    return ["", "### 即将到期，请及时跟进", "", "暂无即将到期的线索。"];
  }
  const lines = ["", "### 即将到期，请及时跟进", "", "| 线索名称 | 剩余时间 |", "|---|---|"];
  for (const item of expiring.items) {
    lines.push(`| ${item.lead.lead_name} | ${formatExpiryLine(item)} |`);
  }
  if (expiring.total > expiring.items.length) {
    lines.push("", `（共 ${expiring.total} 条，仅展示最紧急的 ${expiring.items.length} 条）`);
  }
  return lines;
}

function renderAgentFactsBlock(conversionDims, quality) {
  const lines = [
    "",
    "<!-- AGENT-FACTS-START：仅供你生成上面的占位符使用，替换完所有占位符后必须整段删除，不要发给用户 -->",
    "### 转化数据参考（写 <<SUMMARY>> 用，写成 2~4 句连贯自然语言，禁止逐字段罗列；多数指标领先→鼓励语气，多数落后→督促语气，持平→中性鼓励；只挑 1~2 个最突出的对比点展开，不要五个指标全列一遍）",
    ...conversionDims.map((d) => `- ${d.label}：我 ${d.format(d.mine)} ｜ 同组均值 ${d.format(d.teamAvg)} ｜ ${d.verdict}`),
  ];
  if (quality.items.length > 0) {
    lines.push(
      "",
      "### 优质线索参考（写 <<REASON_n>> 用，每条一句自然语言，挑2~3个最有代表性的事实融合表达，禁止用“｜”分隔罗列字段，禁止出现字段英文名或百分位数字本身）"
    );
    quality.items.forEach((item, i) => {
      lines.push(`- <<REASON_${i + 1}>>（${item.lead.lead_name}）：${item.facts.join(" ｜ ")}`);
    });
  }
  lines.push("<!-- AGENT-FACTS-END -->");
  return lines;
}

function render(conversionDims, quality, expiring) {
  return [
    "## 私海线索日报",
    "",
    "### 今日战报",
    "<<SUMMARY>>",
    ...renderQualitySection(quality),
    ...renderExpiringSection(expiring),
    ...renderAgentFactsBlock(conversionDims, quality),
  ].join("\n");
}

try {
  const first = queryPage(1);
  const total = Number(first.total || 0);
  const leads = [...(first.leads || [])];
  const pages = Math.ceil(total / PAGE_SIZE);
  for (let page = 2; page <= pages; page += 1) {
    const data = queryPage(page);
    leads.push(...(data.leads || []));
  }
  const conversionDims = buildConversionFacts();
  const now = Date.now();
  const expiring = findExpiringSoon(leads, now);
  const quality = findQualityLeadsByPercentile(leads);
  process.stdout.write(render(conversionDims, quality, expiring) + "\n");
} catch (error) {
  process.stderr.write(`${error.message}\n`);
  process.exit(1);
}
