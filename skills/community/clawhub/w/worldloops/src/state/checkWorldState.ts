import * as fs from 'node:fs';
import * as path from 'node:path';

const VALID_BOUNDARY_CROSSED = new Set<string>(['read_only', 'local_commit', 'external_write']);

export interface IntegrityIssue {
  code: string;
  severity: 'error' | 'warning' | 'info';
  file: string;
  message: string;
  referenceId?: string;
}

export interface IntegrityResult {
  ok: boolean;
  status: 'passed' | 'failed';
  summary: {
    filesChecked: number;
    issues: number;
    warnings: number;
    repaired: number;
  };
  issues: IntegrityIssue[];
  safety: {
    externalWrite: false;
  };
}

export interface CheckOptions {
  worldloopsDir?: string;
}

function resolveDir(options?: CheckOptions): string {
  return options?.worldloopsDir ?? process.env.WORLDLOOPS_DIR ?? path.join(process.cwd(), '.worldloops');
}

function tryReadJsonArray(filePath: string, issues: IntegrityIssue[]): unknown[] | null {
  if (!fs.existsSync(filePath)) return null;

  let raw: string;
  try {
    raw = fs.readFileSync(filePath, 'utf8');
  } catch (err) {
    issues.push({
      code: 'FILE_READ_ERROR',
      severity: 'error',
      file: filePath,
      message: `Failed to read file: ${err instanceof Error ? err.message : String(err)}`,
    });
    return null;
  }

  let parsed: unknown;
  try {
    parsed = JSON.parse(raw);
  } catch (err) {
    issues.push({
      code: 'MALFORMED_JSON',
      severity: 'error',
      file: filePath,
      message: `Malformed JSON: ${err instanceof Error ? err.message : String(err)}`,
    });
    return null;
  }

  if (!Array.isArray(parsed)) {
    issues.push({
      code: 'INVALID_FILE_SHAPE',
      severity: 'error',
      file: filePath,
      message: `Expected a JSON array but found ${typeof parsed}`,
    });
    return null;
  }

  return parsed as unknown[];
}

function tryReadJsonObject(
  filePath: string,
  issues: IntegrityIssue[]
): Record<string, unknown> | null {
  if (!fs.existsSync(filePath)) return null;

  let raw: string;
  try {
    raw = fs.readFileSync(filePath, 'utf8');
  } catch (err) {
    issues.push({
      code: 'FILE_READ_ERROR',
      severity: 'error',
      file: filePath,
      message: `Failed to read file: ${err instanceof Error ? err.message : String(err)}`,
    });
    return null;
  }

  let parsed: unknown;
  try {
    parsed = JSON.parse(raw);
  } catch (err) {
    issues.push({
      code: 'MALFORMED_JSON',
      severity: 'error',
      file: filePath,
      message: `Malformed JSON: ${err instanceof Error ? err.message : String(err)}`,
    });
    return null;
  }

  if (typeof parsed !== 'object' || parsed === null || Array.isArray(parsed)) {
    issues.push({
      code: 'INVALID_FILE_SHAPE',
      severity: 'error',
      file: filePath,
      message: `Expected a JSON object but found ${Array.isArray(parsed) ? 'array' : typeof parsed}`,
    });
    return null;
  }

  return parsed as Record<string, unknown>;
}

function checkDuplicateField(
  items: unknown[],
  field: string,
  code: string,
  file: string,
  issues: IntegrityIssue[]
): void {
  const seen = new Map<string, number>();
  for (const item of items) {
    if (typeof item !== 'object' || item === null) continue;
    const val = (item as Record<string, unknown>)[field];
    if (typeof val !== 'string' || val === '') continue;
    seen.set(val, (seen.get(val) ?? 0) + 1);
  }
  for (const [value, count] of seen) {
    if (count > 1) {
      issues.push({
        code,
        severity: 'error',
        file,
        message: `Duplicate ${field} "${value}" found ${count} times`,
        referenceId: value,
      });
    }
  }
}

function checkExternalWriteField(items: unknown[], file: string, issues: IntegrityIssue[]): void {
  for (const item of items) {
    if (typeof item !== 'object' || item === null) continue;
    const obj = item as Record<string, unknown>;
    if (obj['externalWrite'] !== false) {
      issues.push({
        code: 'EXTERNAL_WRITE_VIOLATION',
        severity: 'error',
        file,
        message: `Item "${String(obj['id'] ?? 'unknown')}" has externalWrite: ${JSON.stringify(obj['externalWrite'])} (must be false)`,
        referenceId: typeof obj['id'] === 'string' ? obj['id'] : undefined,
      });
    }
  }
}

function checkBoundaryCrossedField(items: unknown[], file: string, issues: IntegrityIssue[]): void {
  for (const item of items) {
    if (typeof item !== 'object' || item === null) continue;
    const obj = item as Record<string, unknown>;
    const bc = obj['boundaryCrossed'];
    if (bc !== undefined && !VALID_BOUNDARY_CROSSED.has(String(bc))) {
      issues.push({
        code: 'INVALID_BOUNDARY_CROSSED',
        severity: 'error',
        file,
        message: `Item "${String(obj['id'] ?? 'unknown')}" has invalid boundaryCrossed: "${String(bc)}"`,
        referenceId: typeof obj['id'] === 'string' ? obj['id'] : undefined,
      });
    }
  }
}

function idSet(items: unknown[] | null): Set<string> {
  const s = new Set<string>();
  if (!items) return s;
  for (const item of items) {
    if (typeof item === 'object' && item !== null) {
      const id = (item as Record<string, unknown>)['id'];
      if (typeof id === 'string') s.add(id);
    }
  }
  return s;
}

// Builds a lookup set of proposal references (id + idempotencyKey) for receipt verification.
function proposalLookupSet(proposals: unknown[] | null): Set<string> {
  const s = new Set<string>();
  if (!proposals) return s;
  for (const item of proposals) {
    if (typeof item !== 'object' || item === null) continue;
    const obj = item as Record<string, unknown>;
    if (typeof obj['id'] === 'string') s.add(obj['id']);
    if (typeof obj['idempotencyKey'] === 'string') s.add(obj['idempotencyKey']);
  }
  return s;
}

function buildResult(issues: IntegrityIssue[], filesChecked: number): IntegrityResult {
  const errorCount = issues.filter((i) => i.severity === 'error').length;
  const warningCount = issues.filter((i) => i.severity === 'warning').length;
  const repairedCount = issues.filter((i) => i.severity === 'info').length;
  const ok = errorCount === 0;
  return {
    ok,
    status: ok ? 'passed' : 'failed',
    summary: { filesChecked, issues: errorCount, warnings: warningCount, repaired: repairedCount },
    issues,
    safety: { externalWrite: false },
  };
}

export function checkWorldState(options?: CheckOptions): IntegrityResult {
  const dir = resolveDir(options);
  const issues: IntegrityIssue[] = [];
  let filesChecked = 0;

  const fp = (name: string): string => path.join(dir, name);

  // ── open_loop_states.json ────────────────────────────────────────────────────
  const loopsFile = fp('open_loop_states.json');
  const loopsFileExists = fs.existsSync(loopsFile);
  const loops = tryReadJsonArray(loopsFile, issues);
  if (loops !== null) {
    filesChecked++;
    checkDuplicateField(loops, 'id', 'DUPLICATE_LOOP_ID', loopsFile, issues);
    for (const item of loops) {
      if (typeof item !== 'object' || item === null) continue;
      const obj = item as Record<string, unknown>;
      const safety = obj['safety'];
      if (typeof safety === 'object' && safety !== null) {
        if ((safety as Record<string, unknown>)['externalWrite'] !== false) {
          issues.push({
            code: 'EXTERNAL_WRITE_VIOLATION',
            severity: 'error',
            file: loopsFile,
            message: `Loop "${String(obj['id'] ?? 'unknown')}" has safety.externalWrite: ${JSON.stringify((safety as Record<string, unknown>)['externalWrite'])} (must be false)`,
            referenceId: typeof obj['id'] === 'string' ? obj['id'] : undefined,
          });
        }
      }
    }
  } else if (loopsFileExists) {
    filesChecked++;
  }

  const loopIds = idSet(loops);
  void loopIds; // reserved for future receipt→loop cross-checks

  // ── proposals.json ───────────────────────────────────────────────────────────
  const proposalsFile = fp('proposals.json');
  const proposalsFileExists = fs.existsSync(proposalsFile);
  const proposals = tryReadJsonArray(proposalsFile, issues);
  if (proposals !== null) {
    filesChecked++;
    checkDuplicateField(proposals, 'id', 'DUPLICATE_PROPOSAL_ID', proposalsFile, issues);
    checkDuplicateField(
      proposals,
      'idempotencyKey',
      'DUPLICATE_PROPOSAL_IDEMPOTENCY_KEY',
      proposalsFile,
      issues
    );
    checkExternalWriteField(proposals, proposalsFile, issues);
  } else if (proposalsFileExists) {
    filesChecked++;
  }

  const proposalIds = idSet(proposals);
  const proposalLookup = proposalLookupSet(proposals);

  // ── execution_plans.json ─────────────────────────────────────────────────────
  const plansFile = fp('execution_plans.json');
  const plansFileExists = fs.existsSync(plansFile);
  const plans = tryReadJsonArray(plansFile, issues);
  if (plans !== null) {
    filesChecked++;
    checkDuplicateField(plans, 'id', 'DUPLICATE_PLAN_ID', plansFile, issues);
    checkExternalWriteField(plans, plansFile, issues);
    if (proposalsFileExists) {
      for (const item of plans) {
        if (typeof item !== 'object' || item === null) continue;
        const obj = item as Record<string, unknown>;
        const pid = obj['proposalId'];
        if (typeof pid === 'string' && pid !== '' && !proposalIds.has(pid)) {
          issues.push({
            code: 'PLAN_MISSING_PROPOSAL',
            severity: 'error',
            file: plansFile,
            message: `Plan "${String(obj['id'] ?? 'unknown')}" references missing proposal "${pid}"`,
            referenceId: pid,
          });
        }
      }
    }
  } else if (plansFileExists) {
    filesChecked++;
  }

  const planIds = idSet(plans);

  // ── execution_contracts.json ─────────────────────────────────────────────────
  const contractsFile = fp('execution_contracts.json');
  const contractsFileExists = fs.existsSync(contractsFile);
  const contracts = tryReadJsonArray(contractsFile, issues);
  if (contracts !== null) {
    filesChecked++;
    checkDuplicateField(contracts, 'id', 'DUPLICATE_CONTRACT_ID', contractsFile, issues);
    checkExternalWriteField(contracts, contractsFile, issues);
    if (plansFileExists) {
      for (const item of contracts) {
        if (typeof item !== 'object' || item === null) continue;
        const obj = item as Record<string, unknown>;
        const pid = obj['planId'];
        if (typeof pid === 'string' && pid !== '' && !planIds.has(pid)) {
          issues.push({
            code: 'CONTRACT_MISSING_PLAN',
            severity: 'error',
            file: contractsFile,
            message: `Contract "${String(obj['id'] ?? 'unknown')}" references missing plan "${pid}"`,
            referenceId: pid,
          });
        }
      }
    }
  } else if (contractsFileExists) {
    filesChecked++;
  }

  // ── transition_receipts.json ─────────────────────────────────────────────────
  const transReceiptsFile = fp('transition_receipts.json');
  const transReceiptsFileExists = fs.existsSync(transReceiptsFile);
  const transReceipts = tryReadJsonArray(transReceiptsFile, issues);
  if (transReceipts !== null) {
    filesChecked++;
    checkDuplicateField(transReceipts, 'id', 'DUPLICATE_RECEIPT_ID', transReceiptsFile, issues);
    checkExternalWriteField(transReceipts, transReceiptsFile, issues);
    checkBoundaryCrossedField(transReceipts, transReceiptsFile, issues);
    if (proposalsFileExists) {
      for (const item of transReceipts) {
        if (typeof item !== 'object' || item === null) continue;
        const obj = item as Record<string, unknown>;
        const pid = obj['proposalId'];
        if (typeof pid === 'string' && pid !== '' && !proposalLookup.has(pid)) {
          const alreadyRepaired = typeof obj['_worldloopsRepair'] === 'object' && obj['_worldloopsRepair'] !== null;
          if (alreadyRepaired) {
            issues.push({
              code: 'REPAIRED_ORPHAN_RECEIPT',
              severity: 'info',
              file: transReceiptsFile,
              message: `Transition receipt "${String(obj['id'] ?? 'unknown')}" references missing proposal "${pid}" but has been marked orphaned by state:repair`,
              referenceId: typeof obj['id'] === 'string' ? obj['id'] : undefined,
            });
          } else {
            issues.push({
              code: 'RECEIPT_MISSING_PROPOSAL',
              severity: 'warning',
              file: transReceiptsFile,
              message: `Transition receipt "${String(obj['id'] ?? 'unknown')}" references proposal "${pid}" which was not found`,
              referenceId: pid,
            });
          }
        }
      }
    }
  } else if (transReceiptsFileExists) {
    filesChecked++;
  }

  // ── proposal_decision_receipts.json ──────────────────────────────────────────
  const decReceiptsFile = fp('proposal_decision_receipts.json');
  const decReceiptsFileExists = fs.existsSync(decReceiptsFile);
  const decReceipts = tryReadJsonArray(decReceiptsFile, issues);
  if (decReceipts !== null) {
    filesChecked++;
    checkDuplicateField(decReceipts, 'id', 'DUPLICATE_RECEIPT_ID', decReceiptsFile, issues);
    checkExternalWriteField(decReceipts, decReceiptsFile, issues);
    checkBoundaryCrossedField(decReceipts, decReceiptsFile, issues);
    if (proposalsFileExists) {
      for (const item of decReceipts) {
        if (typeof item !== 'object' || item === null) continue;
        const obj = item as Record<string, unknown>;
        const pid = obj['proposalId'];
        if (typeof pid === 'string' && pid !== '' && !proposalLookup.has(pid)) {
          const alreadyRepaired = typeof obj['_worldloopsRepair'] === 'object' && obj['_worldloopsRepair'] !== null;
          if (alreadyRepaired) {
            issues.push({
              code: 'REPAIRED_ORPHAN_RECEIPT',
              severity: 'info',
              file: decReceiptsFile,
              message: `Decision receipt "${String(obj['id'] ?? 'unknown')}" references missing proposal "${pid}" but has been marked orphaned by state:repair`,
              referenceId: typeof obj['id'] === 'string' ? obj['id'] : undefined,
            });
          } else {
            issues.push({
              code: 'RECEIPT_MISSING_PROPOSAL',
              severity: 'error',
              file: decReceiptsFile,
              message: `Decision receipt "${String(obj['id'] ?? 'unknown')}" references missing proposal "${pid}"`,
              referenceId: pid,
            });
          }
        }
      }
    }
  } else if (decReceiptsFileExists) {
    filesChecked++;
  }

  // ── notification_prefs.json ──────────────────────────────────────────────────
  const prefsFile = fp('notification_prefs.json');
  const prefsFileExists = fs.existsSync(prefsFile);
  const prefs = tryReadJsonObject(prefsFile, issues);
  if (prefs !== null) {
    filesChecked++;
    if (!('dailyBrief' in prefs) || !('channels' in prefs)) {
      issues.push({
        code: 'INVALID_FILE_SHAPE',
        severity: 'warning',
        file: prefsFile,
        message: 'notification_prefs.json is missing expected top-level fields (dailyBrief, channels)',
      });
    }
  } else if (prefsFileExists) {
    filesChecked++;
  }

  // ── notification_state.json ──────────────────────────────────────────────────
  const notifStateFile = fp('notification_state.json');
  const notifStateFileExists = fs.existsSync(notifStateFile);
  const notifState = tryReadJsonObject(notifStateFile, issues);
  if (notifState !== null) {
    filesChecked++;
  } else if (notifStateFileExists) {
    filesChecked++;
  }

  return buildResult(issues, filesChecked);
}

export function checkReceipts(options?: CheckOptions): IntegrityResult {
  const dir = resolveDir(options);
  const issues: IntegrityIssue[] = [];
  let filesChecked = 0;

  const fp = (name: string): string => path.join(dir, name);

  // Load proposals for reference checks (silent errors; not counted in filesChecked)
  const proposalsFileExists = fs.existsSync(fp('proposals.json'));
  const proposalsRaw = tryReadJsonArray(fp('proposals.json'), []);
  const proposalLookup = proposalLookupSet(proposalsRaw);

  // ── transition_receipts.json ─────────────────────────────────────────────────
  const transFile = fp('transition_receipts.json');
  const transFileExists = fs.existsSync(transFile);
  const transReceipts = tryReadJsonArray(transFile, issues);
  if (transReceipts !== null) {
    filesChecked++;
    checkDuplicateField(transReceipts, 'id', 'DUPLICATE_RECEIPT_ID', transFile, issues);
    checkExternalWriteField(transReceipts, transFile, issues);
    checkBoundaryCrossedField(transReceipts, transFile, issues);
    if (proposalsFileExists) {
      for (const item of transReceipts) {
        if (typeof item !== 'object' || item === null) continue;
        const obj = item as Record<string, unknown>;
        const pid = obj['proposalId'];
        if (typeof pid === 'string' && pid !== '' && !proposalLookup.has(pid)) {
          const alreadyRepaired = typeof obj['_worldloopsRepair'] === 'object' && obj['_worldloopsRepair'] !== null;
          if (alreadyRepaired) {
            issues.push({
              code: 'REPAIRED_ORPHAN_RECEIPT',
              severity: 'info',
              file: transFile,
              message: `Transition receipt "${String(obj['id'] ?? 'unknown')}" references missing proposal "${pid}" but has been marked orphaned by state:repair`,
              referenceId: typeof obj['id'] === 'string' ? obj['id'] : undefined,
            });
          } else {
            issues.push({
              code: 'RECEIPT_MISSING_PROPOSAL',
              severity: 'warning',
              file: transFile,
              message: `Transition receipt "${String(obj['id'] ?? 'unknown')}" references proposal "${pid}" which was not found`,
              referenceId: pid,
            });
          }
        }
      }
    }
  } else if (transFileExists) {
    filesChecked++;
  }

  // ── proposal_decision_receipts.json ──────────────────────────────────────────
  const decFile = fp('proposal_decision_receipts.json');
  const decFileExists = fs.existsSync(decFile);
  const decReceipts = tryReadJsonArray(decFile, issues);
  if (decReceipts !== null) {
    filesChecked++;
    checkDuplicateField(decReceipts, 'id', 'DUPLICATE_RECEIPT_ID', decFile, issues);
    checkExternalWriteField(decReceipts, decFile, issues);
    checkBoundaryCrossedField(decReceipts, decFile, issues);
    if (proposalsFileExists) {
      for (const item of decReceipts) {
        if (typeof item !== 'object' || item === null) continue;
        const obj = item as Record<string, unknown>;
        const pid = obj['proposalId'];
        if (typeof pid === 'string' && pid !== '' && !proposalLookup.has(pid)) {
          const alreadyRepaired = typeof obj['_worldloopsRepair'] === 'object' && obj['_worldloopsRepair'] !== null;
          if (alreadyRepaired) {
            issues.push({
              code: 'REPAIRED_ORPHAN_RECEIPT',
              severity: 'info',
              file: decFile,
              message: `Decision receipt "${String(obj['id'] ?? 'unknown')}" references missing proposal "${pid}" but has been marked orphaned by state:repair`,
              referenceId: typeof obj['id'] === 'string' ? obj['id'] : undefined,
            });
          } else {
            issues.push({
              code: 'RECEIPT_MISSING_PROPOSAL',
              severity: 'error',
              file: decFile,
              message: `Decision receipt "${String(obj['id'] ?? 'unknown')}" references missing proposal "${pid}"`,
              referenceId: pid,
            });
          }
        }
      }
    }
  } else if (decFileExists) {
    filesChecked++;
  }

  return buildResult(issues, filesChecked);
}
