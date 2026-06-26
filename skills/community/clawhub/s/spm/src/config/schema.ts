import { z } from 'zod';

// Project execution configuration
const ProjectSchema = z.object({
  project_type: z.enum(['code', 'docs', 'config']).default('code'),
  execution_mode: z.enum(['subagent', 'inline']).default('subagent'),
  parallel_subagents: z.boolean().default(true),
  max_parallel_subagents: z.number().positive().default(4),
});

// Quality gates configuration
const QualitySchema = z.object({
  gates_enabled: z.boolean().default(true),
  auto_checkpoint: z.boolean().default(true),
  coverage_target: z.number().min(0).max(100).default(80),
});

// Tracking configuration
const TrackingSchema = z.object({
  wbs_ledger_path: z.string().default('docs/spm/ledger.md'),
  heartbeat_interval: z.string().default('10m'),
  auto_update_ledger: z.boolean().default(true),
});

// Review configuration
const ReviewSchema = z.object({
  spec_reviewer: z.boolean().default(true),
  quality_reviewer: z.boolean().default(true),
  plan_reviewer: z.boolean().default(true),
  reviewer_model: z.string().default(''),
});

// Model tier routing — maps task complexity to model/provider
const ModelTierSchema = z.object({
  model: z.string(),
  description: z.string(),
});

const ModelRoutingSchema = z.object({
  fast: ModelTierSchema,
  standard: ModelTierSchema,
  strong: ModelTierSchema,
});

// Deployment configuration
const DeploymentSchema = z.object({
  enabled: z.boolean().default(false),
  environment: z.enum(['development', 'staging', 'production']).default('development'),
});

// Logging
const LoggingSchema = z.object({
  level: z.enum(['debug', 'info', 'warn', 'error']).default('info'),
  format: z.enum(['json', 'text']).default('json'),
});

// Root schema
export const ConfigSchema = z.object({
  project: ProjectSchema.optional().default({}),
  quality: QualitySchema.optional().default({}),
  tracking: TrackingSchema.optional().default({}),
  review: ReviewSchema.optional().default({}),
  model_routing: ModelRoutingSchema,
  deployment: DeploymentSchema.optional().default({}),
  logging: LoggingSchema.optional().default({}),
});

export type Config = z.infer<typeof ConfigSchema>;
