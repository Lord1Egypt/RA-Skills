import { z } from 'zod';

export const CLIInputSchema = z.object({
  name: z.string().min(1).max(100).regex(/^[a-zA-Z0-9_-]+$/, 'Project name must be alphanumeric, hyphens, or underscores'),
  path: z.string().min(1).optional(),
});

export const AttestConfigSchema = z.object({
  ledgerPath: z.string().min(1, 'Ledger path is required'),
});

export const PolicyRuleSchema = z.object({
  pattern: z.string().min(1, 'Pattern is required'),
  level: z.enum(['safe', 'risky', 'dangerous']),
  action: z.enum(['allow', 'warn', 'block']),
  reason: z.string().min(1, 'Reason is required'),
});

export const PolicySchema = z.object({
  rules: z.array(PolicyRuleSchema).min(1, 'At least one rule is required'),
});

export const WBTTaskSchema = z.object({
  id: z.string().min(1),
  workPackage: z.string().min(1, 'Work package description required'),
  dependencies: z.array(z.string()).default([]),
  status: z.enum(['todo', 'doing', 'done', 'blocked', 'skipped']).default('todo'),
  contextBrief: z.string().optional(),
  exitCriteria: z.string().optional(),
  evidence: z.string().optional(),
});

export const EventSchema = z.object({
  type: z.string().min(1, 'Event type is required'),
  domain: z.enum(['audit', 'integrity', 'quality']),
  timestamp: z.string().or(z.number()).optional(),
  data: z.record(z.any()).default({}),
});