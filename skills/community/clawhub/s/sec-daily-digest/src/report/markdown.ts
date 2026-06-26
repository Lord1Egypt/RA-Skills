import type { VulnerabilityEvent } from "../merge/vuln";
import type { CategoryId } from "../pipeline/types";
import type { TweetMetrics } from "../twitter/types";

export interface DigestArticle {
  titleZh: string;
  title: string;
  link: string;
  summaryZh: string;
  reasonZh: string;
  category: CategoryId;
  keywords: string[];
  score: number;
  sourceName: string;
}

export interface KolEntry {
  displayName: string;
  handle: string;
  text: string;
  link: string;
  tweetId: string;
  metrics: TweetMetrics;
}

export interface DigestRenderInput {
  date: string;
  highlights: string;
  ai: DigestArticle[];
  security: DigestArticle[];
  vulnerabilities: VulnerabilityEvent[];
  kols?: KolEntry[];
  healthWarnings?: string[];
}

export function formatMetric(n: number): string {
  if (n >= 1000) {
    return `${(n / 1000).toFixed(1)}K`;
  }
  return String(n);
}

function renderArticleList(items: DigestArticle[]): string {
  if (items.length === 0) {
    return "_暂无条目_\n";
  }

  return items
    .map((item, index) => {
      let block = `### ${index + 1}. ${item.titleZh}\n\n`;
      block += `[${item.title}](${item.link}) · ${item.sourceName} · ${item.category} · 🔥${Math.round(item.score)}\n\n`;
      block += `${item.summaryZh}\n`;
      if (item.reasonZh) {
        block += `\n- 推荐理由: ${item.reasonZh}\n`;
      }
      if (item.keywords.length > 0) {
        block += `- 关键词: ${item.keywords.join(", ")}\n`;
      }
      return block;
    })
    .join("\n");
}

function renderVulnEvents(events: VulnerabilityEvent[]): string {
  if (events.length === 0) {
    return "_暂无漏洞事件_\n";
  }

  return events
    .map((event, index) => {
      let block = `### ${index + 1}. ${event.title}\n\n`;
      if (event.cves.length > 0) {
        block += `- CVE: ${event.cves.join(", ")}\n`;
      }
      block += `- 摘要: ${event.summary}\n`;
      block += "- 参考链接:\n";
      for (const ref of event.references) {
        block += `  - ${ref.source}: ${ref.link}\n`;
      }
      return block;
    })
    .join("\n");
}

export function renderKolSection(kols: KolEntry[]): string {
  if (!kols || kols.length === 0) return "";

  const lines = kols.map((kol) => {
    const m = kol.metrics;
    const metrics = `👁 ${formatMetric(m.impression_count)} | 💬 ${formatMetric(m.reply_count)} | 🔁 ${formatMetric(m.retweet_count)} | ❤️ ${formatMetric(m.like_count)}`;
    return `- **${kol.displayName}** (@${kol.handle}) — ${kol.text} \`${metrics}\`\n  <${kol.link}>`;
  });

  return `## 🔐 Security KOL Updates\n\n${lines.join("\n\n")}\n`;
}

export function renderDigest(input: DigestRenderInput): string {
  let out = `# sec-daily-digest ${input.date}\n\n`;
  out += "面向网络空间安全研究员的每日精选：平衡追踪 AI 发展与安全动态。\n\n";

  if (input.highlights.trim().length > 0) {
    out += "## 📝 今日趋势\n\n";
    out += `${input.highlights.trim()}\n\n`;
  }

  const kolSection = renderKolSection(input.kols ?? []);
  if (kolSection) {
    out += kolSection;
    out += "\n";
  }

  out += "## AI发展\n\n";
  out += renderArticleList(input.ai);
  out += "\n";

  out += "## 安全动态\n\n";
  out += renderArticleList(input.security);
  out += "\n";

  out += "## 漏洞专报\n\n";
  out += renderVulnEvents(input.vulnerabilities);
  out += "\n";

  const healthSection = formatHealthWarnings(input.healthWarnings ?? []);
  if (healthSection) {
    out += healthSection;
    out += "\n";
  }

  return out;
}

function formatHealthWarnings(names: string[]): string {
  if (names.length === 0) return "";
  const lines = names.map((n) => `- ${n}`).join("\n");
  return `## ⚠️ Source Health Warnings\n\n${lines}\n`;
}
