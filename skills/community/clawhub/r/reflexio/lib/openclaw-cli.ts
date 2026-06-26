/**
 * Abstraction over command execution.
 * Plugin runtime injects api.runtime.system.runCommandWithTimeout.
 * Tests inject a mock.
 */
export type CommandRunner = (
  argv: string[],
  opts: { timeoutMs: number; input?: string }
) => Promise<{ stdout: string; stderr: string; code: number | null }>;

export interface MemorySearchResult {
  path: string;
  startLine: number;
  endLine: number;
  score: number;
  snippet: string;
  source: string;
}

export interface MemorySearchResponse {
  results: MemorySearchResult[];
}

/**
 * Call `openclaw memory search` via the injected runner.
 * Returns empty array on any failure (graceful degradation).
 */
export async function memorySearch(
  query: string,
  maxResults: number,
  runner: CommandRunner
): Promise<MemorySearchResult[]> {
  try {
    const result = await runner(
      ["openclaw", "memory", "search", query, "--json", "--max-results", String(maxResults)],
      { timeoutMs: 30_000 }
    );
    const parsed: MemorySearchResponse = JSON.parse(result.stdout.trim());
    return parsed.results || [];
  } catch (err) {
    console.error(`[reflexio] openclaw memory search failed: ${err}`);
    return [];
  }
}

/**
 * Call `openclaw memory index --force` to rebuild the search index.
 * Necessary after bulk file deletions (e.g. consolidation) so that
 * deleted files are dropped from search results.
 */
export async function reindexMemory(runner: CommandRunner): Promise<void> {
  try {
    await runner(
      ["openclaw", "memory", "index", "--force"],
      { timeoutMs: 60_000 }
    );
  } catch (err) {
    console.error(`[reflexio] openclaw memory index --force failed: ${err}`);
  }
}

/**
 * Abstraction over LLM inference.
 * Plugin runtime creates this from the SDK simple completion API.
 * Tests inject a mock.
 */
export type InferFn = (prompt: string) => Promise<string | null>;
