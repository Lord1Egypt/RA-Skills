import { defineModel } from "@cargo-ai/cdk";

import { modelsFolder } from "../folders";

// The ledger: one row per domain per week.
//
// Ora keeps only the latest scan of a domain, so this is the history. Last
// week's row is what "regressed", "fixed" and "competitor moved" are measured
// against, and it is also the idempotency key:
//   - `scan_id` is the ISO week plus the domain. A re-run the same week finds
//     the row and does not scan that domain again.
//   - `fix_pr_url` is set on our row once the fix pull request is open, so a
//     re-run opens no second one.
//   - `digest_ts` is set on our row after the digest posted, so a re-run posts
//     nothing.
//
// A row stores the failing check ids, not every check. Ora runs about 150; the
// ones that pass and the ones that do not apply say nothing week to week, and
// the full report is one link away.
export const websiteAudits = defineModel("website_audits", {
  kind: "native",
  extractSlug: "defineCustom",
  config: {
    columns: [
      // <ISO week>:<domain>, e.g. 2026-W42:www.example.com
      { slug: "scan_id", type: "string" },
      { slug: "week", type: "string" },
      { slug: "domain", type: "string" },
      { slug: "is_ours", type: "boolean" },
      // False when the bare domain, which is what Ora scans, does not land on
      // the site: no scan, no score, and next week counts from a baseline.
      { slug: "reached", type: "boolean" },
      { slug: "score", type: "number" },
      { slug: "grade", type: "string" },
      // Ora's scannedAt: when Ora ran the scan, not when this row was written.
      { slug: "scanned_at", type: "string" },
      { slug: "report_url", type: "string" },
      // Check ids with status fail or warning, sorted, comma separated.
      { slug: "failing_checks", type: "string" },
      { slug: "fix_pr_url", type: "string" },
      { slug: "digest_ts", type: "string" },
    ],
  },
  folder: modelsFolder,
});
