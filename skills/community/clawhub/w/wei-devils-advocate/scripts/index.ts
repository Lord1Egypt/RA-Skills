#!/usr/bin/env bun
// Entry point for multi-model-researcher skill.
// Requires Bun (https://bun.sh) for native TypeScript execution.

import { readFileSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

/**
 * Multi-Model Researcher - Main Entry Point
 *
 * Provides a clean API interface for the multi-model researcher skill.
 * Handles input/output validation and provides both programmatic and CLI interfaces.
 */

import { createResearchAgent } from './agent.js';
import { BailianClient, OpenRouterClient } from './clients/index.js';
import type {
  ResearchRequest,
  ResearchResponse,
  ModelName,
} from './agent.js';

/** Query type classification - must match routing keys in config.json */
export type QueryType =
  | 'financial'
  | 'technical'
  | 'social'
  | 'current_events'
  | 'scientific'
  | 'creative'
  | 'general';

// Re-export types
export type {
  ResearchRequest,
  ResearchResponse,
  ModelName,
  NormalizedResponse,
  FailedModel,
} from './agent.js';

export { ResearchAgent, createResearchAgent } from './agent.js';
export { BailianClient, OpenRouterClient, BAILIAN_MODELS, OPENROUTER_MODELS } from './clients/index.js';

/** Load configuration from config.json */
function loadConfig(): ConfigFile {
  const __dirname = dirname(fileURLToPath(import.meta.url));
  const configPath = join(__dirname, '..', 'config.json');
  const raw = readFileSync(configPath, 'utf-8');
  return JSON.parse(raw);
}

/** Configuration file structure */
interface ConfigFile {
  judge_model: string;
  max_models: number;
  max_tokens: number;
  max_tokens_judge: number;
  depth: string;
  models: Record<string, {
    provider: string;
    model_id: string;
    api_base: string;
    api_key_env: string;
    timeout: number;
    roles?: string[];
  }>;
  routing?: Record<string, {
    models?: string[];
    judge_prompt?: string;
    keywords?: string[];
  }>;
}

const appConfig = loadConfig();

/**
 * Select models based on query type using config.json routing configuration
 * Returns models from the routing config, limited to maxModels
 */
function selectModelsByDomain(
  queryType: QueryType,
  maxModels: number
): ModelName[] {
  const routingConfig = appConfig.routing?.[queryType];
  const allModels = Object.keys(appConfig.models);

  if (routingConfig?.models && routingConfig.models.length > 0) {
    // Filter to only include models that exist in config
    const validModels = routingConfig.models.filter(
      (m): m is ModelName => allModels.includes(m)
    );
    return validModels.slice(0, maxModels);
  }

  // Fallback: use general routing or first available models
  const generalModels = appConfig.routing?.['general']?.models
    || Object.keys(appConfig.models).slice(0, maxModels);

  return generalModels.slice(0, maxModels) as ModelName[];
}

/** Client configuration options */
export interface ClientConfig {
  bailianApiKey?: string;
  bailianBaseUrl?: string;
  openrouterApiKey?: string;
  openrouterBaseUrl?: string;
}

/** Research options */
export interface ResearchOptions {
  /** Force specific models (bypasses auto-selection) */
  models?: ModelName[];
  /** Maximum number of models to query (default: 2) */
  maxModels?: number;
  /** Depth mode: 'simple' or 'tree' (default: 'simple') */
  depth?: 'simple' | 'tree';
  /** Judge model to use for synthesis (default: 'glm-5') */
  judgeModel?: ModelName;
  /** Query type for model selection - must match domains in config.json (default: 'general') */
  queryType?: QueryType;
}

/**
 * Main research function - query multiple models and synthesize responses
 *
 * @param query - The research question to analyze
 * @param options - Optional configuration
 * @returns Research response with synthesized answer
 *
 * @example
 * ```typescript
 * const result = await research('What are the economic impacts of AI agents?');
 * console.log(result.finalAnswer);
 * console.log(`Confidence: ${result.confidence}`);
 * ```
 */
export async function research(
  query: string,
  options?: ResearchOptions
): Promise<ResearchResponse> {
  // Validate input
  if (!query || typeof query !== 'string') {
    throw new ResearchError('Query is required and must be a string', 'INVALID_INPUT');
  }

  if (query.trim().length === 0) {
    throw new ResearchError('Query cannot be empty', 'INVALID_INPUT');
  }

  // Determine models based on queryType (default: 'general')
  let selectedModels: ModelName[] | undefined = options?.models;
  const queryType = options?.queryType ?? 'general';
  const maxModels = options?.maxModels ?? appConfig.max_models ?? 2;

  if (!selectedModels) {
    selectedModels = selectModelsByDomain(queryType, maxModels);
  }

  // Map queryType to domain for judge prompt selection
  // 'financial' queryType uses 'financial' domain judge prompt
  const domain = queryType === 'financial' ? 'financial' : undefined;

  // Build request
  const request: ResearchRequest = {
    query: query.trim(),
    models: selectedModels,
    maxModels: maxModels,
    depth: options?.depth ?? 'simple',
    domain: domain,
  };

  // Create agent with optional client configuration
  const agent = createResearchAgent({
    judgeModel: options?.judgeModel,
  });

  // Execute research
  return await agent.research(request);
}

/**
 * Research with custom clients - use when you need to configure API keys or endpoints
 *
 * @param query - The research question
 * @param clientConfig - Client configuration for Bailian and OpenRouter
 * @param options - Optional research options
 * @returns Research response
 *
 * @example
 * ```typescript
 * const result = await researchWithClients(
 *   'What are the latest AI breakthroughs?',
 *   {
 *     bailianApiKey: 'your-bailian-key',
 *     openrouterApiKey: 'your-openrouter-key',
 *   }
 * );
 * ```
 */
export async function researchWithClients(
  query: string,
  clientConfig: ClientConfig,
  options?: ResearchOptions
): Promise<ResearchResponse> {
  // Validate input
  if (!query || typeof query !== 'string') {
    throw new ResearchError('Query is required and must be a string', 'INVALID_INPUT');
  }

  // Create custom clients
  const bailianClient = clientConfig.bailianApiKey
    ? new BailianClient({
        apiKey: clientConfig.bailianApiKey,
        baseUrl: clientConfig.bailianBaseUrl,
      })
    : new BailianClient();

  const openrouterClient = clientConfig.openrouterApiKey
    ? new OpenRouterClient({
        apiKey: clientConfig.openrouterApiKey,
        baseUrl: clientConfig.openrouterBaseUrl,
      })
    : new OpenRouterClient();

  // Determine models based on queryType (default: 'general')
  let selectedModels: ModelName[] | undefined = options?.models;
  const queryType = options?.queryType ?? 'general';
  const maxModels = options?.maxModels ?? appConfig.max_models ?? 2;

  if (!selectedModels) {
    selectedModels = selectModelsByDomain(queryType, maxModels);
  }

  // Map queryType to domain for judge prompt selection
  const domain = queryType === 'financial' ? 'financial' : undefined;

  // Build request
  const request: ResearchRequest = {
    query: query.trim(),
    models: selectedModels,
    maxModels: maxModels,
    depth: options?.depth ?? 'simple',
    domain: domain,
  };

  // Create agent with custom clients
  const agent = createResearchAgent({
    bailianClient,
    openrouterClient,
    judgeModel: options?.judgeModel,
  });

  // Execute research
  return await agent.research(request);
}

/**
 * Quick research - simplified interface for simple queries
 *
 * @param query - The research question
 * @returns The synthesized answer string
 *
 * @example
 * ```typescript
 * const answer = await quickResearch('What is quantum computing?');
 * console.log(answer);
 * ```
 */
export async function quickResearch(query: string): Promise<string> {
  const result = await research(query);
  return result.finalAnswer;
}

/**
 * Research with specific models - bypass router and use specified models
 *
 * @param query - The research question
 * @param models - Array of model names to use
 * @returns Research response
 *
 * @example
 * ```typescript
 * const result = await researchWithModels(
 *   'Explain neural networks',
 *   ['glm-5', 'kimi-k2.5']
 * );
 * ```
 */
export async function researchWithModels(
  query: string,
  models: ModelName[]
): Promise<ResearchResponse> {
  if (!models || models.length === 0) {
    throw new ResearchError('At least one model must be specified', 'INVALID_INPUT');
  }

  return await research(query, { models });
}

/**
 * Custom error class for research operations
 */
export class ResearchError extends Error {
  code: string;

  constructor(message: string, code: string) {
    super(message);
    this.name = 'ResearchError';
    this.code = code;
  }
}

/**
 * Format research response for display
 *
 * @param response - Research response object
 * @returns Formatted string
 */
export function formatResearchResponse(response: ResearchResponse): string {
  const lines: string[] = [];

  lines.push('='.repeat(60));
  lines.push('MULTI-MODEL RESEARCH RESULT');
  lines.push('='.repeat(60));
  lines.push('');
  lines.push(`Query: ${response.query}`);
  lines.push('');

  if (response.modelSummaries && response.modelSummaries.length > 0) {
    lines.push('-'.repeat(60));
    lines.push('MODEL SUMMARIES');
    lines.push('-'.repeat(60));
    response.modelSummaries.forEach(s => {
      lines.push(`• ${s}`);
    });
    lines.push('');
  }

  lines.push('-'.repeat(60));
  lines.push('FINAL ANSWER');
  lines.push('-'.repeat(60));
  lines.push(response.finalAnswer);
  lines.push('');

  if (response.consensus && response.consensus.length > 0) {
    lines.push('-'.repeat(60));
    lines.push('CONSENSUS POINTS');
    lines.push('-'.repeat(60));
    response.consensus.forEach(point => {
      lines.push(`• ${point}`);
    });
    lines.push('');
  }

  if (response.disagreements && response.disagreements.length > 0) {
    lines.push('-'.repeat(60));
    lines.push('DISAGREEMENTS');
    lines.push('-'.repeat(60));
    response.disagreements.forEach(d => {
      lines.push(`• ${d}`);
    });
    lines.push('');
  }

  lines.push('-'.repeat(60));
  lines.push(`Confidence: ${(response.confidence * 100).toFixed(1)}%`);
  lines.push(`Models Used: ${response.modelsUsed.join(', ')}`);

  if (response.modelsFailed && response.modelsFailed.length > 0) {
    lines.push(`Models Failed: ${response.modelsFailed.map(m => `${m.model} (${m.reason})`).join(', ')}`);
  }

  if (response.warning) {
    lines.push('');
    lines.push(`⚠️  Warning: ${response.warning}`);
  }

  if (response.reasoning) {
    lines.push('');
    lines.push('-'.repeat(60));
    lines.push('REASONING');
    lines.push('-'.repeat(60));
    lines.push(response.reasoning);
  }

  lines.push('');
  lines.push('='.repeat(60));

  return lines.join('\n');
}

/**
 * Export individual model answers
 *
 * @param response - Research response object
 * @returns Array of individual model responses
 */
export function getIndividualAnswers(response: ResearchResponse): Array<{
  model: ModelName;
  summary: string;
  keyPoints: string[];
  confidence: number;
}> {
  return response.answers.map(answer => ({
    model: answer.model,
    summary: answer.summary,
    keyPoints: answer.keyPoints,
    confidence: answer.confidence,
  }));
}

// CLI entry point - only run if executed directly
const isMainModule = process.argv[1]?.includes('index.ts') ||
                     process.argv[1]?.includes('index.js') ||
                     process.argv[1]?.includes('dist/index');

if (isMainModule) {
  (async () => {
    const args = process.argv.slice(2);

    // Show help
    if (args.includes('--help') || args.includes('-h')) {
      console.log(`
Multi-Model Researcher CLI

Usage:
  bun run scripts/index.ts [options] "Your research question"

Options:
  -h, --help              Show this help message
  -m, --models <models>   Comma-separated list of models (e.g., glm-5,kimi-k2.5)
  -t, --type <type>       Query type for model selection: financial, technical, social,
                          current_events, analysis, creative, factual, general (default: general)
  -j, --json              Output as JSON
  -v, --verbose           Show detailed output including individual model responses

Examples:
  bun run scripts/index.ts "What are the economic impacts of AI?"
  bun run scripts/index.ts -m glm-5,gpt-5.4 "Explain quantum computing"
  bun run scripts/index.ts -t financial "Will the Fed cut rates in 2026?"
  bun run scripts/index.ts -t technical "How do I implement a distributed transaction?"
  bun run scripts/index.ts --json "Latest AI breakthroughs"
`);
      process.exit(0);
    }

    // Parse arguments
    let query = '';
    let models: ModelName[] | undefined;
    let queryType: QueryType = 'general';
    let outputJson = false;
    let verbose = false;

    for (let i = 0; i < args.length; i++) {
      const arg = args[i];

      if (arg === '-m' || arg === '--models') {
        const modelStr = args[++i];
        if (modelStr) {
          models = modelStr.split(',') as ModelName[];
        }
      } else if (arg === '-t' || arg === '--type') {
        const typeStr = args[++i];
        if (typeStr) {
          queryType = typeStr as QueryType;
        }
      } else if (arg === '-j' || arg === '--json') {
        outputJson = true;
      } else if (arg === '-v' || arg === '--verbose') {
        verbose = true;
      } else if (!arg.startsWith('-') && !query) {
        query = arg;
      }
    }

    // Collect remaining args as query if not set
    if (!query && args.length > 0) {
      const lastArg = args[args.length - 1];
      if (!lastArg.startsWith('-')) {
        query = lastArg;
      }
    }

    if (!query) {
      console.error('Error: No query provided. Use --help for usage information.');
      process.exit(1);
    }

    try {
      console.log(`Researching: "${query}"`);
      if (models) {
        console.log(`Using models: ${models.join(', ')}`);
      } else {
        console.log(`Query type: ${queryType}`);
      }
      console.log('');

      const result = await research(query, { models, queryType });

      if (outputJson) {
        console.log(JSON.stringify(result, null, 2));
      } else if (verbose) {
        console.log(formatResearchResponse(result));
      } else if (result.reportPath) {
        // Output report content directly (format defined in judge.txt)
        console.log(readFileSync(result.reportPath, 'utf-8'));
      } else {
        console.log(result.finalAnswer);
      }

      process.exit(0);
    } catch (error) {
      console.error('Error:', error instanceof Error ? error.message : error);
      process.exit(1);
    }
  })();
}

// Default export
export default {
  research,
  researchWithClients,
  quickResearch,
  researchWithModels,
  formatResearchResponse,
  getIndividualAnswers,
  ResearchError,
  selectModelsByDomain,
};
