import { describe, expect, test } from "bun:test";
import { sendEmailViaGog } from "../../src/delivery/email";
import type { SpawnFn } from "../../src/delivery/email";

describe("sendEmailViaGog", () => {
  test("returns ok=true on exit code 0", async () => {
    const spawner: SpawnFn = async (_cmd, _opts) => ({ exitCode: 0, stderr: "" });
    const result = await sendEmailViaGog(
      { to: "test@example.com", subject: "Test", body: "Hello" },
      spawner,
    );
    expect(result.ok).toBe(true);
    expect(result.error).toBeUndefined();
  });

  test("returns ok=false on non-zero exit", async () => {
    const spawner: SpawnFn = async (_cmd, _opts) => ({ exitCode: 1, stderr: "delivery failed" });
    const result = await sendEmailViaGog(
      { to: "test@example.com", subject: "Test", body: "Hello" },
      spawner,
    );
    expect(result.ok).toBe(false);
    expect(result.error).toContain("delivery failed");
  });

  test("returns ok=false with helpful message on ENOENT", async () => {
    const spawner: SpawnFn = async () => {
      const err = new Error("ENOENT") as NodeJS.ErrnoException;
      err.code = "ENOENT";
      throw err;
    };
    const result = await sendEmailViaGog(
      { to: "test@example.com", subject: "Test", body: "Hello" },
      spawner,
    );
    expect(result.ok).toBe(false);
    expect(result.error).toContain("gog not found in PATH");
  });

  test("spawner receives correct command args", async () => {
    let capturedCmd: string[] = [];
    let capturedStdin = "";

    const spawner: SpawnFn = async (cmd, opts) => {
      capturedCmd = cmd;
      capturedStdin = opts.stdin;
      return { exitCode: 0, stderr: "" };
    };

    await sendEmailViaGog(
      { to: "addr@example.com", subject: "My Subject", body: "My Body" },
      spawner,
    );

    expect(capturedCmd).toContain("gog");
    expect(capturedCmd).toContain("addr@example.com");
    expect(capturedCmd).toContain("My Subject");
    expect(capturedStdin).toBe("My Body");
  });
});
