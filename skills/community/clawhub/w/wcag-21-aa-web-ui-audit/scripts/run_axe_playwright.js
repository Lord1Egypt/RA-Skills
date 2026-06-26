#!/usr/bin/env node
"use strict";

const fs = require("fs/promises");
const path = require("path");

function printUsage() {
  console.log(
    "Usage: node scripts/run_axe_playwright.js --url <https://example.com> [--url <https://example2.com>] [--urls-file <./urls.txt>] [--timeout-ms <20000>]"
  );
}

function parseArgs(argv) {
  const args = {
    urls: [],
    urlsFile: null,
    timeoutMs: 20000,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (token === "--url") {
      const value = argv[i + 1];
      if (!value) {
        throw new Error("Missing value for --url");
      }
      args.urls.push(value);
      i += 1;
      continue;
    }

    if (token === "--urls-file") {
      const value = argv[i + 1];
      if (!value) {
        throw new Error("Missing value for --urls-file");
      }
      args.urlsFile = value;
      i += 1;
      continue;
    }

    if (token === "--timeout-ms") {
      const value = argv[i + 1];
      if (!value) {
        throw new Error("Missing value for --timeout-ms");
      }
      const parsed = Number(value);
      if (!Number.isFinite(parsed) || parsed <= 0) {
        throw new Error("--timeout-ms must be a positive number");
      }
      args.timeoutMs = Math.floor(parsed);
      i += 1;
      continue;
    }

    if (token === "--help" || token === "-h") {
      args.help = true;
      continue;
    }

    throw new Error(`Unknown argument: ${token}`);
  }

  return args;
}

function normalizeUrl(raw) {
  if (!raw) {
    return null;
  }

  const value = String(raw).trim();
  if (!value) {
    return null;
  }

  try {
    const url = new URL(value);
    if (url.protocol !== "http:" && url.protocol !== "https:") {
      return null;
    }
    return url.toString();
  } catch (_error) {
    return null;
  }
}

async function loadUrlsFromFile(filePath) {
  const content = await fs.readFile(filePath, "utf8");
  return content
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line.length > 0 && !line.startsWith("#"));
}

async function resolveDependencyModules() {
  try {
    const playwrightModule = await import("playwright");
    const axeModule = await import("@axe-core/playwright");

    const playwrightExport = playwrightModule.default || playwrightModule;
    const chromium = playwrightExport.chromium;
    const AxeBuilder = axeModule.default || axeModule.AxeBuilder;

    if (!chromium || !AxeBuilder) {
      throw new Error("Imported modules did not expose expected APIs");
    }

    return { chromium, AxeBuilder };
  } catch (_error) {
    return null;
  }
}

function toSerializableViolations(violations) {
  return violations.map((violation) => ({
    id: violation.id,
    impact: violation.impact || "unknown",
    description: violation.description,
    help: violation.help,
    helpUrl: violation.helpUrl,
    tags: Array.isArray(violation.tags) ? violation.tags : [],
    nodes: (violation.nodes || []).map((node) => ({
      target: Array.isArray(node.target) ? node.target : [],
      html: node.html || "",
      failureSummary: node.failureSummary || "",
      impact: node.impact || violation.impact || "unknown",
    })),
  }));
}

function dedupeFindings(pages) {
  const map = new Map();

  for (const pageResult of pages) {
    for (const violation of pageResult.violations) {
      for (const node of violation.nodes) {
        const targetSelector = node.target.join(" | ");
        const key = `${violation.id}::${targetSelector}::${pageResult.url}`;
        if (!map.has(key)) {
          map.set(key, {
            key,
            ruleId: violation.id,
            impact: violation.impact,
            description: violation.description,
            help: violation.help,
            helpUrl: violation.helpUrl,
            page: pageResult.url,
            target: targetSelector,
            failureSummary: node.failureSummary,
            tags: violation.tags,
          });
        }
      }
    }
  }

  return Array.from(map.values());
}

function buildImpactCounts(findings) {
  const counts = {
    critical: 0,
    serious: 0,
    moderate: 0,
    minor: 0,
    unknown: 0,
  };

  for (const finding of findings) {
    const key = Object.prototype.hasOwnProperty.call(counts, finding.impact)
      ? finding.impact
      : "unknown";
    counts[key] += 1;
  }

  return counts;
}

function buildRuleSummary(findings) {
  const byRule = new Map();

  for (const finding of findings) {
    const existing = byRule.get(finding.ruleId) || {
      ruleId: finding.ruleId,
      impact: finding.impact,
      description: finding.description,
      pages: new Set(),
      targets: new Set(),
      occurrences: 0,
    };

    existing.pages.add(finding.page);
    existing.targets.add(finding.target);
    existing.occurrences += 1;
    byRule.set(finding.ruleId, existing);
  }

  return Array.from(byRule.values())
    .map((entry) => ({
      ruleId: entry.ruleId,
      impact: entry.impact,
      description: entry.description,
      pageCount: entry.pages.size,
      targetCount: entry.targets.size,
      occurrences: entry.occurrences,
    }))
    .sort((a, b) => b.occurrences - a.occurrences || a.ruleId.localeCompare(b.ruleId));
}

function escapeCell(value) {
  return String(value).replace(/\|/g, "\\|").replace(/\n/g, " ");
}

function buildMarkdownSummary(payload) {
  const impactCounts = buildImpactCounts(payload.dedupedFindings);
  const ruleSummary = buildRuleSummary(payload.dedupedFindings);

  const lines = [];
  lines.push("# axe + Playwright Summary");
  lines.push("");
  lines.push(`Generated: ${payload.generatedAt}`);
  lines.push(`Total input URLs: ${payload.inputUrls.length}`);
  lines.push(`Scanned pages: ${payload.pages.length}`);
  lines.push(`Page failures: ${payload.pageErrors.length}`);
  lines.push(`Unique findings (rule + target + page): ${payload.dedupedFindings.length}`);
  lines.push("");
  lines.push("## Impact Counts");
  lines.push(`- critical: ${impactCounts.critical}`);
  lines.push(`- serious: ${impactCounts.serious}`);
  lines.push(`- moderate: ${impactCounts.moderate}`);
  lines.push(`- minor: ${impactCounts.minor}`);
  lines.push(`- unknown: ${impactCounts.unknown}`);
  lines.push("");

  if (payload.pageErrors.length > 0) {
    lines.push("## Page Failures");
    for (const failure of payload.pageErrors) {
      lines.push(`- ${failure.url}: ${failure.error}`);
    }
    lines.push("");
  }

  lines.push("## Rule Summary");
  lines.push("");
  lines.push("| Rule ID | Impact | Occurrences | Pages | Targets | Description |");
  lines.push("| --- | --- | ---: | ---: | ---: | --- |");

  if (ruleSummary.length === 0) {
    lines.push("| none | n/a | 0 | 0 | 0 | No violations reported by axe for scanned pages. |");
  } else {
    for (const row of ruleSummary) {
      lines.push(
        `| ${escapeCell(row.ruleId)} | ${escapeCell(row.impact)} | ${row.occurrences} | ${row.pageCount} | ${row.targetCount} | ${escapeCell(row.description)} |`
      );
    }
  }

  lines.push("");
  lines.push("## Notes");
  lines.push("- This is an automated baseline only; manual WCAG checks are still required.");
  lines.push("- Deduplication key: (rule id + target selector + page).");

  return `${lines.join("\n")}\n`;
}

async function writeOutputs(payload) {
  const outputsDir = path.resolve(process.cwd(), "outputs");
  await fs.mkdir(outputsDir, { recursive: true });

  const jsonPath = path.join(outputsDir, "axe-results.json");
  const markdownPath = path.join(outputsDir, "axe-summary.md");

  await fs.writeFile(jsonPath, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  await fs.writeFile(markdownPath, buildMarkdownSummary(payload), "utf8");

  console.log(`[wcag-21-aa-web-ui-audit] Wrote ${jsonPath}`);
  console.log(`[wcag-21-aa-web-ui-audit] Wrote ${markdownPath}`);
}

async function scanUrls({ urls, timeoutMs, chromium, AxeBuilder }) {
  const browser = await chromium.launch({ headless: true });
  const pages = [];
  const pageErrors = [];

  try {
    for (const url of urls) {
      const context = await browser.newContext();
      const page = await context.newPage();
      page.setDefaultTimeout(timeoutMs);

      try {
        await page.goto(url, { waitUntil: "domcontentloaded", timeout: timeoutMs });
        const axeResults = await new AxeBuilder({ page }).analyze();
        pages.push({
          url,
          scannedAt: new Date().toISOString(),
          violations: toSerializableViolations(axeResults.violations || []),
        });
        console.log(`[wcag-21-aa-web-ui-audit] Scanned ${url}`);
      } catch (error) {
        const message = error && error.message ? error.message : String(error);
        pageErrors.push({ url, error: message });
        console.log(`[wcag-21-aa-web-ui-audit] Failed ${url}: ${message}`);
      } finally {
        await context.close();
      }
    }
  } finally {
    await browser.close();
  }

  return { pages, pageErrors };
}

async function main() {
  let args;
  try {
    args = parseArgs(process.argv.slice(2));
  } catch (error) {
    console.log(`[wcag-21-aa-web-ui-audit] ${error.message}`);
    printUsage();
    process.exit(1);
    return;
  }

  if (args.help) {
    printUsage();
    process.exit(0);
    return;
  }

  let urls = [...args.urls];
  if (args.urlsFile) {
    try {
      const fromFile = await loadUrlsFromFile(args.urlsFile);
      urls = urls.concat(fromFile);
    } catch (error) {
      console.log(`[wcag-21-aa-web-ui-audit] Failed to read --urls-file: ${error.message}`);
      process.exit(1);
      return;
    }
  }

  const normalizedUniqueUrls = Array.from(
    new Set(
      urls
        .map((item) => normalizeUrl(item))
        .filter((item) => item !== null)
    )
  );

  if (normalizedUniqueUrls.length === 0) {
    console.log("[wcag-21-aa-web-ui-audit] No valid URLs provided.");
    printUsage();
    process.exit(1);
    return;
  }

  const deps = await resolveDependencyModules();
  if (!deps) {
    console.log("[wcag-21-aa-web-ui-audit] Optional dependencies are missing.");
    console.log("[wcag-21-aa-web-ui-audit] Install with: npm install -D playwright @axe-core/playwright");
    console.log("[wcag-21-aa-web-ui-audit] Skipping automated scan and exiting without failure.");
    process.exit(0);
    return;
  }

  const { pages, pageErrors } = await scanUrls({
    urls: normalizedUniqueUrls,
    timeoutMs: args.timeoutMs,
    chromium: deps.chromium,
    AxeBuilder: deps.AxeBuilder,
  });

  const dedupedFindings = dedupeFindings(pages);

  const payload = {
    generatedAt: new Date().toISOString(),
    inputUrls: normalizedUniqueUrls,
    timeoutMs: args.timeoutMs,
    pages,
    pageErrors,
    dedupedFindings,
    notes: {
      dedupeKey: "rule id + target selector + page",
      mode: "automated baseline",
    },
  };

  await writeOutputs(payload);
}

main().catch((error) => {
  const message = error && error.stack ? error.stack : String(error);
  console.error(`[wcag-21-aa-web-ui-audit] Unexpected failure:\n${message}`);
  process.exit(1);
});
