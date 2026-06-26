export interface EmailOptions {
  to: string;
  subject: string;
  body: string;
}

export type SpawnFn = (cmd: string[], opts: { stdin: string }) => Promise<{ exitCode: number; stderr: string }>;

async function defaultSpawner(cmd: string[], opts: { stdin: string }): Promise<{ exitCode: number; stderr: string }> {
  try {
    const proc = Bun.spawn(cmd, {
      stdin: "pipe",
      stdout: "ignore",
      stderr: "pipe",
    });

    proc.stdin.write(opts.stdin);
    proc.stdin.end();

    const exitCode = await proc.exited;
    const stderrBytes = await new Response(proc.stderr).text();

    return { exitCode, stderr: stderrBytes };
  } catch (error) {
    if (error instanceof Error && (error as NodeJS.ErrnoException).code === "ENOENT") {
      throw Object.assign(new Error("ENOENT"), { code: "ENOENT" });
    }
    throw error;
  }
}

export async function sendEmailViaGog(
  options: EmailOptions,
  spawner: SpawnFn = defaultSpawner,
): Promise<{ ok: boolean; error?: string }> {
  const cmd = ["gog", "send", "--to", options.to, "--subject", options.subject];

  try {
    const { exitCode, stderr } = await spawner(cmd, { stdin: options.body });
    if (exitCode === 0) {
      return { ok: true };
    }
    return { ok: false, error: stderr || `gog exited with code ${exitCode}` };
  } catch (error) {
    if (error instanceof Error && (error as NodeJS.ErrnoException).code === "ENOENT") {
      return { ok: false, error: "gog not found in PATH. Install: https://github.com/googleapis/google-auth-library-python" };
    }
    return { ok: false, error: error instanceof Error ? error.message : String(error) };
  }
}
