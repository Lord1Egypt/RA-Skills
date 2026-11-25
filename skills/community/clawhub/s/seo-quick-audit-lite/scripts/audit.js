#!/usr/bin/env node
// seo-quick-audit-lite — offline on-page SEO check for a local HTML file.
// Reads the file, never touches the network. JSON report on stdout.
// Exit 0 = all pass, 1 = warns/fails, 2 = usage/read error.
import fs from "node:fs";

const tagAttr = (html, re) => {
  const m = html.match(re);
  return m ? (m[1] ?? m[0]).trim() : null;
};
const count = (html, re) => (html.match(re) || []).length;

export function auditHtml(html) {
  const checks = [];
  const c = (id, status, detail) => checks.push({ id, status, detail });

  const title = tagAttr(html, /<title[^>]*>([^<]*)<\/title>/i);
  if (!title) c("title", "fail", "No <title> element.");
  else if (title.length < 20 || title.length > 65)
    c("title", "warn", `Title length ${title.length} (aim ~30-65 chars): "${title.slice(0, 80)}"`);
  else c("title", "pass", `Title ok (${title.length} chars).`);

  const desc =
    tagAttr(html, /<meta[^>]+name=["']description["'][^>]+content=["']([^"']*)["']/i) ??
    tagAttr(html, /<meta[^>]+content=["']([^"']*)["'][^>]+name=["']description["']/i);
  if (!desc) c("meta-description", "fail", "Missing meta description.");
  else if (desc.length < 50 || desc.length > 160)
    c("meta-description", "warn", `Description length ${desc.length} (aim 50-160).`);
  else c("meta-description", "pass", `Description ok (${desc.length} chars).`);

  const canonical = tagAttr(html, /<link[^>]+rel=["']canonical["'][^>]+href=["']([^"']+)["']/i);
  c("canonical", canonical ? "pass" : "warn",
    canonical ? `Canonical: ${canonical}` : "No canonical link tag.");

  const robotsMeta = tagAttr(html, /<meta[^>]+name=["']robots["'][^>]+content=["']([^"']+)["']/i);
  c("robots-meta",
    robotsMeta && /noindex/i.test(robotsMeta) ? "warn" : "pass",
    robotsMeta ? `robots meta: "${robotsMeta}"` : "No robots meta (defaults to index,follow).");

  c("viewport", /<meta[^>]+name=["']viewport["']/i.test(html) ? "pass" : "warn",
    "viewport meta for mobile rendering.");

  const ogTags = count(html, /<meta[^>]+property=["']og:/gi);
  c("open-graph", ogTags >= 3 ? "pass" : "warn",
    `${ogTags} og:* tags${ogTags < 3 ? " — og:title/og:description/og:image expected" : ""}.`);

  const h1 = count(html, /<h1[\s>]/gi);
  c("h1", h1 === 1 ? "pass" : h1 === 0 ? "fail" : "warn",
    h1 === 1 ? "Exactly one <h1>." : `${h1} <h1> elements.`);

  const imgs = count(html, /<img\b/gi);
  const imgsWithAlt = count(html, /<img[^>]+alt=["'][^"']*["']/gi);
  c("img-alt",
    imgs === 0 ? "info" : imgsWithAlt === imgs ? "pass" : "warn",
    imgs === 0 ? "No <img> elements." : `${imgsWithAlt}/${imgs} images have alt attributes.`);

  c("lang", /<html[^>]+lang=["'][^"']+["']/i.test(html) ? "pass" : "warn",
    "html lang attribute.");
  c("charset",
    /<meta[^>]+charset/i.test(html) || /<meta[^>]+content=["'][^"']*charset=/i.test(html)
      ? "pass" : "warn",
    "charset declaration.");

  return checks;
}

const isMain = process.argv[1] && import.meta.url === new URL(`file:///${process.argv[1].replace(/\\/g, "/")}`).href;
if (isMain || process.argv[1]?.endsWith("audit.js")) {
  const file = process.argv[2];
  if (!file) {
    console.error("usage: node audit.js <page.html>");
    process.exit(2);
  }
  let html;
  try {
    html = fs.readFileSync(file, "utf8");
  } catch {
    console.error(`cannot read ${file}`);
    process.exit(2);
  }
  const checks = auditHtml(html);
  const summary = {
    pass: checks.filter((x) => x.status === "pass").length,
    warn: checks.filter((x) => x.status === "warn").length,
    fail: checks.filter((x) => x.status === "fail").length,
    info: checks.filter((x) => x.status === "info").length,
  };
  const reasons = [];
  if (
    tagAttr(html, /<link[^>]+rel=["']canonical["'][^>]+href=["']https?:\/\//i) ||
    tagAttr(html, /<meta[^>]+property=["']og:url["'][^>]+content=["']https?:\/\//i)
  )
    reasons.push(
      "page references a live canonical/og:url — the full version fetches live URLs including /robots.txt and /sitemap.xml status",
    );
  const twitterTags = count(html, /<meta[^>]+(?:name|property)=["']twitter:/gi);
  if (twitterTags)
    reasons.push(
      `${twitterTags} twitter:* meta tag(s) present — the dedicated twitter-card check is only in the full version`,
    );
  const report = { file, summary, checks };
  if (reasons.length) report.upgrade = { skill: "seo-quick-audit", reasons };
  console.log(JSON.stringify(report, null, 2));
  process.exit(summary.fail + summary.warn ? 1 : 0);
}
