import { describe, test, expect } from 'bun:test';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const CLI_PATH = join(__dirname, '..', 'cli.ts');

async function runCli(
  args: string[],
  envOverrides: Record<string, string | undefined> = {}
): Promise<{ stdout: string; stderr: string; exitCode: number }> {
  const env = { ...process.env, ...envOverrides };
  
  for (const [key, value] of Object.entries(envOverrides)) {
    if (value === undefined) {
      delete env[key];
    }
  }

  const proc = Bun.spawn(['bun', CLI_PATH, ...args], {
    env,
    stdout: 'pipe',
    stderr: 'pipe',
  });

  const stdout = await new Response(proc.stdout).text();
  const stderr = await new Response(proc.stderr).text();
  const exitCode = await proc.exited;

  return { stdout, stderr, exitCode };
}

describe('CLI', () => {
  describe('--help', () => {
    test('shows help text with --help flag', async () => {
      const { stdout, exitCode } = await runCli(['--help'], { ROBLOX_API_KEY: 'test' });

      expect(exitCode).toBe(0);
      expect(stdout).toContain('roblox-cli');
      expect(stdout).toContain('games list');
      expect(stdout).toContain('passes list');
      expect(stdout).toContain('products list');
      expect(stdout).toContain('ROBLOX_API_KEY');
    });

    test('shows help text with -h flag', async () => {
      const { stdout, exitCode } = await runCli(['-h'], { ROBLOX_API_KEY: 'test' });

      expect(exitCode).toBe(0);
      expect(stdout).toContain('roblox-cli');
    });

    test('shows help text with no arguments', async () => {
      const { stdout, exitCode } = await runCli([], { ROBLOX_API_KEY: 'test' });

      expect(exitCode).toBe(0);
      expect(stdout).toContain('roblox-cli');
    });
  });

  describe('MISSING_API_KEY', () => {
    test('returns MISSING_API_KEY error when env var not set', async () => {
      const { stdout, exitCode } = await runCli(['games', 'list'], { ROBLOX_API_KEY: undefined });

      expect(exitCode).toBe(1);
      const result = JSON.parse(stdout);
      expect(result.success).toBe(false);
      expect(result.error.code).toBe('MISSING_API_KEY');
      expect(result.error.message).toContain('ROBLOX_API_KEY');
    });
  });

  describe('INVALID_API_KEY', () => {
    test('returns INVALID_API_KEY for short/invalid key on games list', async () => {
      const { stdout, exitCode } = await runCli(['games', 'list'], { ROBLOX_API_KEY: 'invalid_short_key' });

      expect(exitCode).toBe(1);
      const result = JSON.parse(stdout);
      expect(result.success).toBe(false);
      expect(result.error.code).toBe('INVALID_API_KEY');
    });
  });

  describe('INVALID_ARGS', () => {
    test('returns INVALID_ARGS for unknown command', async () => {
      const { stdout, exitCode } = await runCli(['unknown'], { ROBLOX_API_KEY: 'test-key' });

      expect(exitCode).toBe(1);
      const result = JSON.parse(stdout);
      expect(result.success).toBe(false);
      expect(result.error.code).toBe('INVALID_ARGS');
      expect(result.error.message).toContain('Unknown command');
    });

    test('returns INVALID_ARGS for unknown games subcommand', async () => {
      const { stdout, exitCode } = await runCli(['games', 'unknown'], { ROBLOX_API_KEY: 'test-key' });

      expect(exitCode).toBe(1);
      const result = JSON.parse(stdout);
      expect(result.success).toBe(false);
      expect(result.error.code).toBe('INVALID_ARGS');
    });

    test('returns INVALID_ARGS for passes create without required flags', async () => {
      const { stdout, exitCode } = await runCli(['passes', 'create', '12345'], { ROBLOX_API_KEY: 'test-key' });

      expect(exitCode).toBe(1);
      const result = JSON.parse(stdout);
      expect(result.success).toBe(false);
      expect(result.error.code).toBe('INVALID_ARGS');
      expect(result.error.message).toContain('--name');
      expect(result.error.message).toContain('--price');
    });

    test('returns INVALID_ARGS for products create without required flags', async () => {
      const { stdout, exitCode } = await runCli(['products', 'create', '12345'], { ROBLOX_API_KEY: 'test-key' });

      expect(exitCode).toBe(1);
      const result = JSON.parse(stdout);
      expect(result.success).toBe(false);
      expect(result.error.code).toBe('INVALID_ARGS');
      expect(result.error.message).toContain('--name');
      expect(result.error.message).toContain('--price');
    });

    test('returns INVALID_ARGS for passes update without any flags', async () => {
      const { stdout, exitCode } = await runCli(['passes', 'update', '12345', '67890'], { ROBLOX_API_KEY: 'test-key' });

      expect(exitCode).toBe(1);
      const result = JSON.parse(stdout);
      expect(result.success).toBe(false);
      expect(result.error.code).toBe('INVALID_ARGS');
    });

    test('returns INVALID_ARGS for missing universeId', async () => {
      const { stdout, exitCode } = await runCli(['passes', 'list'], { ROBLOX_API_KEY: 'test-key' });

      expect(exitCode).toBe(1);
      const result = JSON.parse(stdout);
      expect(result.success).toBe(false);
      expect(result.error.code).toBe('INVALID_ARGS');
      expect(result.error.message).toContain('universeId');
    });

    test('returns INVALID_ARGS for missing passId on get', async () => {
      const { stdout, exitCode } = await runCli(['passes', 'get', '12345'], { ROBLOX_API_KEY: 'test-key' });

      expect(exitCode).toBe(1);
      const result = JSON.parse(stdout);
      expect(result.success).toBe(false);
      expect(result.error.code).toBe('INVALID_ARGS');
      expect(result.error.message).toContain('passId');
    });

    test('returns INVALID_ARGS for missing productId on get', async () => {
      const { stdout, exitCode } = await runCli(['products', 'get', '12345'], { ROBLOX_API_KEY: 'test-key' });

      expect(exitCode).toBe(1);
      const result = JSON.parse(stdout);
      expect(result.success).toBe(false);
      expect(result.error.code).toBe('INVALID_ARGS');
      expect(result.error.message).toContain('productId');
    });
  });

  describe('JSON output format', () => {
    test('outputs valid JSON for errors', async () => {
      const { stdout } = await runCli(['games', 'list'], { ROBLOX_API_KEY: undefined });

      expect(() => JSON.parse(stdout)).not.toThrow();
      const result = JSON.parse(stdout);
      expect(result).toHaveProperty('success');
      expect(result).toHaveProperty('error');
      expect(result.error).toHaveProperty('code');
      expect(result.error).toHaveProperty('message');
    });

    test('help output is plain text, not JSON', async () => {
      const { stdout } = await runCli(['--help'], { ROBLOX_API_KEY: 'test' });

      expect(() => JSON.parse(stdout)).toThrow();
      expect(stdout).toContain('Usage:');
    });
  });

  describe('exit codes', () => {
    test('exits with 0 for help', async () => {
      const { exitCode } = await runCli(['--help'], { ROBLOX_API_KEY: 'test' });
      expect(exitCode).toBe(0);
    });

    test('exits with 1 for missing API key', async () => {
      const { exitCode } = await runCli(['games', 'list'], { ROBLOX_API_KEY: undefined });
      expect(exitCode).toBe(1);
    });

    test('exits with 1 for invalid command', async () => {
      const { exitCode } = await runCli(['invalid'], { ROBLOX_API_KEY: 'test' });
      expect(exitCode).toBe(1);
    });
  });
});
