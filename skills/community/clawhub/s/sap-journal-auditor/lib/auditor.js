/**
 * SAP Journal Auditor - Audit Engine
 * Runs all SAP FI/CO audit checks against normalized journal entries.
 *
 * @author Daryoosh Dehestani (https://github.com/dda-oo)
 * @organization RadarRoster (https://radarroster.com)
 * @license CC-BY-4.0
 *
 * Audit checks implemented:
 *   1. Duplicate Postings - Same amount/account/cost center within ±2 days
 *   2. Round Amount Anomalies - Round figures on accrual accounts at period-end
 *   3. Cost Center Mismatch - Account outside typical range for cost center
 *   4. Approval Bypass - Missing documentation, backdated postings
 *   5. Intercompany/GR-IR - IC postings without reference, open clearing items
 *   6. User Patterns - High-volume users, unusually large postings
 */

"use strict";

let findingCounter = 0;
function nextId() {
  return `FND-${String(++findingCounter).padStart(4, "0")}`;
}

// ── Helpers ──────────────────────────────────────────────────────────────────

/** Absolute difference in days between two Date objects */
function daysDiff(a, b) {
  if (!a || !b) return 999;
  return Math.abs((a.getTime() - b.getTime()) / 86400000);
}

/** Returns the day-of-month for a Date */
function dayOfMonth(d) {
  if (!d) return 0;
  return d.getDate();
}

/** Returns total days in a given month */
function daysInMonth(d) {
  if (!d) return 30;
  return new Date(d.getFullYear(), d.getMonth() + 1, 0).getDate();
}

/** Is the posting in the last N days of its month? */
function isEndOfPeriod(date, lastNDays = 3) {
  if (!date) return false;
  const total = daysInMonth(date);
  return dayOfMonth(date) >= total - lastNDays + 1;
}

/** SAP accrual/deferral account range: 480000–499999 (standard German chart of accounts SKR03/SKR04) */
function isAccrualAccount(account) {
  const num = parseInt(account, 10);
  return num >= 480000 && num <= 499999;
}

/** Intercompany accounts: typically 180000–199999 */
function isIntercompanyAccount(account) {
  const num = parseInt(account, 10);
  return num >= 180000 && num <= 199999;
}

/** GR/IR clearing: typically 191100 or 191200 in SKR04 */
function isGRIRAccount(account) {
  const num = parseInt(account, 10);
  return num === 191100 || num === 191200 || (num >= 190000 && num <= 192999);
}

/** Is amount exactly round? (no cents) */
function isRoundAmount(amount) {
  return Math.abs(amount) > 0 && Math.abs(amount) % 100 === 0;
}

// ── Check 1: Duplicate Postings ───────────────────────────────────────────────

function checkDuplicates(entries, threshold) {
  const findings = [];

  for (let i = 0; i < entries.length; i++) {
    for (let j = i + 1; j < entries.length; j++) {
      const a = entries[i];
      const b = entries[j];

      const sameAmount = Math.abs(Math.abs(a.amount) - Math.abs(b.amount)) < 0.01;
      const sameAccount = a.account && b.account && a.account === b.account;
      const sameCostCenter = a.costCenter && b.costCenter && a.costCenter === b.costCenter;
      const withinTwoDays = daysDiff(a.postingDate, b.postingDate) <= 2;
      const differentDoc = a.docNumber !== b.docNumber;

      if (!differentDoc) continue;
      if (Math.abs(a.amount) < threshold) continue;

      // HIGH: same amount + account + cost center within 2 days
      if (sameAmount && sameAccount && sameCostCenter && withinTwoDays) {
        findings.push({
          id: nextId(),
          checkType: "Duplicate Posting",
          risk: "HIGH",
          docNumbers: [a.docNumber, b.docNumber],
          amount: a.amount,
          currency: a.currency,
          account: a.account,
          costCenter: a.costCenter,
          postingDate: a.postingDate,
          user: a.user,
          description: `Potential duplicate: Doc ${a.docNumber} and ${b.docNumber} — same amount (${a.amount} ${a.currency}), account ${a.account}, cost center ${a.costCenter}, posted within ${daysDiff(a.postingDate, b.postingDate).toFixed(0)} day(s).`,
          recommendation: "Verify both documents are not double-posted. Check FBL3N for open items.",
        });
      }

      // MEDIUM: same amount + same vendor/customer within period
      const sameVendor = a.vendor && b.vendor && a.vendor === b.vendor;
      const sameCustomer = a.customer && b.customer && a.customer === b.customer;
      const samePeriod =
        a.postingDate &&
        b.postingDate &&
        a.postingDate.getFullYear() === b.postingDate.getFullYear() &&
        a.postingDate.getMonth() === b.postingDate.getMonth();

      if (sameAmount && (sameVendor || sameCustomer) && samePeriod && !sameCostCenter) {
        findings.push({
          id: nextId(),
          checkType: "Duplicate Posting (Vendor/Customer)",
          risk: "MEDIUM",
          docNumbers: [a.docNumber, b.docNumber],
          amount: a.amount,
          currency: a.currency,
          account: a.account,
          costCenter: a.costCenter,
          postingDate: a.postingDate,
          user: a.user,
          description: `Possible duplicate invoice: Doc ${a.docNumber} and ${b.docNumber} — same amount for ${sameVendor ? "vendor " + a.vendor : "customer " + a.customer} in same period.`,
          recommendation: "Check for double invoice payment. Review MIR4 / FBL1N.",
        });
      }
    }
  }

  return findings;
}

// ── Check 2: Round-Amount + Period-End Postings ───────────────────────────────

function checkRoundAmounts(entries, threshold) {
  const findings = [];

  for (const e of entries) {
    if (Math.abs(e.amount) < threshold) continue;
    if (!isRoundAmount(e.amount)) continue;

    const endOfPeriod = isEndOfPeriod(e.postingDate);
    const accrualAcc = isAccrualAccount(e.account);

    if (endOfPeriod && accrualAcc) {
      findings.push({
        id: nextId(),
        checkType: "Round Amount — Period-End Accrual",
        risk: "HIGH",
        docNumbers: [e.docNumber],
        amount: e.amount,
        currency: e.currency,
        account: e.account,
        costCenter: e.costCenter,
        postingDate: e.postingDate,
        user: e.user,
        description: `Round amount of ${e.amount} ${e.currency} posted on ${e.postingDate?.toISOString().slice(0, 10)} (end of period) to accrual/deferral account ${e.account}. High risk of unsupported estimate.`,
        recommendation: "Request supporting calculation for accrual. Verify reversal is scheduled.",
      });
    } else if (endOfPeriod) {
      findings.push({
        id: nextId(),
        checkType: "Round Amount — Period-End",
        risk: "MEDIUM",
        docNumbers: [e.docNumber],
        amount: e.amount,
        currency: e.currency,
        account: e.account,
        costCenter: e.costCenter,
        postingDate: e.postingDate,
        user: e.user,
        description: `Round amount of ${e.amount} ${e.currency} posted in last days of period to account ${e.account}.`,
        recommendation: "Verify posting is based on actual document, not estimate.",
      });
    } else if (accrualAcc) {
      findings.push({
        id: nextId(),
        checkType: "Round Amount — Accrual Account",
        risk: "LOW",
        docNumbers: [e.docNumber],
        amount: e.amount,
        currency: e.currency,
        account: e.account,
        costCenter: e.costCenter,
        postingDate: e.postingDate,
        user: e.user,
        description: `Round amount of ${e.amount} ${e.currency} on accrual account ${e.account}. Verify against accrual schedule.`,
        recommendation: "Cross-check with accruals register.",
      });
    }
  }

  return findings;
}

// ── Check 3: Unusual Cost Center Assignments ──────────────────────────────────

function checkCostCenterMismatch(entries) {
  const findings = [];

  // Build a profile: for each cost center, what accounts does it normally use?
  const ccProfile = {};
  for (const e of entries) {
    if (!e.costCenter || !e.account) continue;
    const accNum = parseInt(e.account, 10);
    if (!ccProfile[e.costCenter]) ccProfile[e.costCenter] = { accounts: [], ranges: { min: accNum, max: accNum } };
    ccProfile[e.costCenter].accounts.push(accNum);
    if (accNum < ccProfile[e.costCenter].ranges.min) ccProfile[e.costCenter].ranges.min = accNum;
    if (accNum > ccProfile[e.costCenter].ranges.max) ccProfile[e.costCenter].ranges.max = accNum;
  }

  // Compute median account range per cost center
  for (const cc of Object.keys(ccProfile)) {
    const accs = ccProfile[cc].accounts.sort((a, b) => a - b);
    const p10 = accs[Math.floor(accs.length * 0.1)];
    const p90 = accs[Math.floor(accs.length * 0.9)];
    ccProfile[cc].p10 = p10;
    ccProfile[cc].p90 = p90;
  }

  // Flag entries outside 10th-90th percentile account range for their cost center
  for (const e of entries) {
    if (!e.costCenter || !e.account) continue;
    const profile = ccProfile[e.costCenter];
    if (!profile || profile.accounts.length < 5) continue; // need enough data

    const accNum = parseInt(e.account, 10);
    if (accNum < profile.p10 || accNum > profile.p90) {
      findings.push({
        id: nextId(),
        checkType: "Unusual Cost Center Assignment",
        risk: "MEDIUM",
        docNumbers: [e.docNumber],
        amount: e.amount,
        currency: e.currency,
        account: e.account,
        costCenter: e.costCenter,
        postingDate: e.postingDate,
        user: e.user,
        description: `Account ${e.account} is outside the typical range for cost center ${e.costCenter} (usual range: ${profile.p10}–${profile.p90}). May indicate wrong cost assignment.`,
        recommendation: "Verify account assignment is intentional. Check with responsible controller.",
      });
    }
  }

  return findings;
}

// ── Check 4: Approval Bypass Indicators ──────────────────────────────────────

function checkApprovalBypass(entries, threshold) {
  const findings = [];

  for (const e of entries) {
    // Missing document text AND no reference number above threshold
    if (Math.abs(e.amount) >= threshold && !e.docText && !e.reference) {
      findings.push({
        id: nextId(),
        checkType: "Missing Documentation",
        risk: "MEDIUM",
        docNumbers: [e.docNumber],
        amount: e.amount,
        currency: e.currency,
        account: e.account,
        costCenter: e.costCenter,
        postingDate: e.postingDate,
        user: e.user,
        description: `Document ${e.docNumber} of ${e.amount} ${e.currency} has no document text (BKTXT) and no reference number. Lacks audit trail.`,
        recommendation: "Request posting documentation from responsible user.",
      });
    }

    // Large manual posting: above 10x threshold with no vendor/customer reference (likely manual journal)
    if (
      Math.abs(e.amount) >= threshold * 10 &&
      !e.vendor &&
      !e.customer &&
      !e.reference &&
      !isAccrualAccount(e.account)
    ) {
      findings.push({
        id: nextId(),
        checkType: "Missing Documentation",
        risk: "HIGH",
        docNumbers: [e.docNumber],
        amount: e.amount,
        currency: e.currency,
        account: e.account,
        costCenter: e.costCenter,
        postingDate: e.postingDate,
        user: e.user,
        description: `Large manual posting ${e.docNumber} of ${e.amount} ${e.currency} has no vendor, customer, or reference document. Manual journal entry above threshold with no traceable source document.`,
        recommendation: "Verify supporting documentation. Check if posting requires dual control.",
      });
    }

    // Backdated posting: posting date more than 7 days before entry date
    if (e.postingDate && e.entryDate) {
      const diff = (e.entryDate.getTime() - e.postingDate.getTime()) / 86400000;
      if (diff > 7) {
        findings.push({
          id: nextId(),
          checkType: "Backdated Posting",
          risk: "HIGH",
          docNumbers: [e.docNumber],
          amount: e.amount,
          currency: e.currency,
          account: e.account,
          costCenter: e.costCenter,
          postingDate: e.postingDate,
          user: e.user,
          description: `Document ${e.docNumber} was entered on ${e.entryDate.toISOString().slice(0, 10)} but backdated to ${e.postingDate.toISOString().slice(0, 10)} (${diff.toFixed(0)} days earlier).`,
          recommendation: "Verify business justification for backdating. Check period-lock settings.",
        });
      }
    }
  }

  return findings;
}

// ── Check 5: Intercompany / Clearing Anomalies ────────────────────────────────

function checkIntercompanyClearing(entries) {
  const findings = [];

  // GR/IR open items: flag if there are GR/IR account postings with no matching clearing
  const grirEntries = entries.filter((e) => isGRIRAccount(e.account));
  const grirByRef = {};
  for (const e of grirEntries) {
    const key = e.reference || e.docNumber;
    if (!grirByRef[key]) grirByRef[key] = [];
    grirByRef[key].push(e);
  }

  for (const [ref, group] of Object.entries(grirByRef)) {
    const totalAmount = group.reduce((sum, e) => {
      const sign = e.debitCredit === "H" ? -1 : 1;
      return sum + sign * Math.abs(e.amount);
    }, 0);

    // If net is non-zero, potentially open item
    if (Math.abs(totalAmount) > 0.01 && group.length > 0) {
      const oldestDate = group
        .filter((e) => e.postingDate)
        .sort((a, b) => a.postingDate - b.postingDate)[0]?.postingDate;
      const ageInDays = oldestDate ? (Date.now() - oldestDate.getTime()) / 86400000 : 0;

      if (ageInDays > 60) {
        findings.push({
          id: nextId(),
          checkType: "GR/IR Open Item",
          risk: "MEDIUM",
          docNumbers: group.map((e) => e.docNumber),
          amount: totalAmount,
          currency: group[0].currency,
          account: group[0].account,
          costCenter: "",
          postingDate: oldestDate,
          user: group[0].user,
          description: `GR/IR account ${group[0].account} shows uncleared balance of ${Math.abs(totalAmount).toFixed(2)} ${group[0].currency} for reference ${ref}, open for ${ageInDays.toFixed(0)} days.`,
          recommendation: "Review GRIR clearing account. Post missing goods receipt or invoice.",
        });
      }
    }
  }

  // Intercompany without reference document (cross-company reference is mandatory)
  const icEntries = entries.filter((e) => isIntercompanyAccount(e.account));
  for (const e of icEntries) {
    if (!e.reference) {
      findings.push({
        id: nextId(),
        checkType: "Intercompany — No Reference",
        risk: "HIGH",
        docNumbers: [e.docNumber],
        amount: e.amount,
        currency: e.currency,
        account: e.account,
        costCenter: e.costCenter,
        postingDate: e.postingDate,
        user: e.user,
        description: `Intercompany posting ${e.docNumber} of ${e.amount} ${e.currency} on account ${e.account} has no reference or partner company indicator.`,
        recommendation: "Verify corresponding entry in partner company code. Use F.13 for reconciliation.",
      });
    }
  }

  return findings;
}

// ── Check 6: Suspicious User Patterns ────────────────────────────────────────

function checkUserPatterns(entries, threshold) {
  const findings = [];

  // Users with unusually high posting volume
  const userVolume = {};
  for (const e of entries) {
    if (!e.user) continue;
    userVolume[e.user] = (userVolume[e.user] || 0) + 1;
  }

  const avgVolume = Object.values(userVolume).reduce((a, b) => a + b, 0) / Object.keys(userVolume).length || 0;
  const highVolumeThreshold = avgVolume * 3;

  for (const [user, count] of Object.entries(userVolume)) {
    if (count > highVolumeThreshold && count > 20) {
      const userEntries = entries.filter((e) => e.user === user);
      const totalAmount = userEntries.reduce((s, e) => s + Math.abs(e.amount), 0);
      findings.push({
        id: nextId(),
        checkType: "High-Volume User",
        risk: "LOW",
        docNumbers: userEntries.slice(0, 3).map((e) => e.docNumber),
        amount: totalAmount,
        currency: userEntries[0]?.currency || "EUR",
        account: "",
        costCenter: "",
        postingDate: null,
        user,
        description: `User ${user} posted ${count} documents (${(count / avgVolume).toFixed(1)}x average), total volume: ${totalAmount.toFixed(2)}. Verify this aligns with their role.`,
        recommendation: "Cross-check user authorization profile in SU01. Verify SoD compliance.",
      });
    }
  }

  // Large single-user postings: one user posting above 3x the average single transaction
  const amounts = entries.map((e) => Math.abs(e.amount)).filter((a) => a > 0).sort((a, b) => a - b);
  const p95Amount = amounts[Math.floor(amounts.length * 0.95)] || threshold;

  for (const e of entries) {
    if (Math.abs(e.amount) > p95Amount * 2 && Math.abs(e.amount) > threshold * 10) {
      findings.push({
        id: nextId(),
        checkType: "Unusually Large Posting",
        risk: "MEDIUM",
        docNumbers: [e.docNumber],
        amount: e.amount,
        currency: e.currency,
        account: e.account,
        costCenter: e.costCenter,
        postingDate: e.postingDate,
        user: e.user,
        description: `Document ${e.docNumber} amount of ${e.amount} ${e.currency} is in the top 5% of all postings in this dataset. Posted by ${e.user || "unknown"}.`,
        recommendation: "Request supporting documentation. Verify approval chain.",
      });
    }
  }

  return findings;
}

// ── Overall Risk Calculator ───────────────────────────────────────────────────

function calcOverallRisk(findings) {
  if (findings.some((f) => f.risk === "CRITICAL")) return "CRITICAL";
  const highCount = findings.filter((f) => f.risk === "HIGH").length;
  if (highCount >= 3) return "CRITICAL";
  if (highCount >= 1) return "HIGH";
  if (findings.some((f) => f.risk === "MEDIUM")) return "MEDIUM";
  if (findings.length > 0) return "LOW";
  return "CLEAN";
}

// ── Main Export ───────────────────────────────────────────────────────────────

function runAllChecks(entries, options = {}) {
  const { duplicateThreshold = 1000 } = options;
  findingCounter = 0; // reset for each run

  const allFindings = [
    ...checkDuplicates(entries, duplicateThreshold),
    ...checkRoundAmounts(entries, duplicateThreshold),
    ...checkCostCenterMismatch(entries),
    ...checkApprovalBypass(entries, duplicateThreshold),
    ...checkIntercompanyClearing(entries),
    ...checkUserPatterns(entries, duplicateThreshold),
  ];

  // Sort by risk severity
  const riskOrder = { CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3 };
  allFindings.sort((a, b) => (riskOrder[a.risk] || 9) - (riskOrder[b.risk] || 9));

  return {
    findings: allFindings,
    overallRisk: calcOverallRisk(allFindings),
    checksSummary: {
      duplicates: allFindings.filter((f) => f.checkType.startsWith("Duplicate")).length,
      roundAmounts: allFindings.filter((f) => f.checkType.startsWith("Round")).length,
      costCenterMismatch: allFindings.filter((f) => f.checkType === "Unusual Cost Center Assignment").length,
      approvalBypass: allFindings.filter((f) => ["Missing Documentation", "Backdated Posting"].includes(f.checkType)).length,
      intercompany: allFindings.filter((f) => f.checkType.startsWith("GR/IR") || f.checkType.startsWith("Intercompany")).length,
      userPatterns: allFindings.filter((f) => ["High-Volume User", "Unusually Large Posting"].includes(f.checkType)).length,
    },
  };
}

module.exports = { runAllChecks };
