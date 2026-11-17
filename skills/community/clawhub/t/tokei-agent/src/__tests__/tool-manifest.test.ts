/** @jest-environment node */
import { readFileSync } from "node:fs";
import { join } from "node:path";
import manifest from "../tool-manifest.json";
import { buildToolRequest, readManifest, resolvePath } from "../tool-dispatch.js";
import { TOOLS } from "../mcp.js";
import { main } from "../index.js";
import type { Io } from "../index.js";

const specs = readManifest(manifest);

describe("tool-manifest.json", () => {
  it("is the source of the MCP tool list", () => {
    expect(TOOLS).toEqual(specs.map((s) => s.def));
  });

  it("has unique tool names and CLI command names", () => {
    const names = specs.map((s) => s.def.name);
    expect(new Set(names).size).toBe(names.length);
    const commands = specs.flatMap((s) => (s.cli ? [s.cli.command] : []));
    expect(new Set(commands).size).toBe(commands.length);
  });

  it("gives every tool either a CLI command or a handler", () => {
    for (const spec of specs) {
      expect([spec.def.name, spec.cli !== undefined || spec.handler !== undefined]).toEqual([
        spec.def.name,
        true,
      ]);
    }
    expect(specs.filter((s) => s.handler !== undefined).map((s) => s.def.name)).toEqual([
      "media_upload",
    ]);
  });

  it.each(specs.map((s) => [s.def.name, s] as const))("%s is internally consistent", (_name, spec) => {
    const props = spec.def.inputSchema.properties;
    const required = spec.def.inputSchema.required ?? [];
    const placeholders = [...spec.path.matchAll(/\{([^}]+)\}/g)].map((m) => m[1]);

    expect(spec.path.startsWith("/")).toBe(true);
    if (spec.pathParam === undefined) {
      expect(placeholders).toEqual([]);
    } else {
      expect(placeholders).toEqual([spec.pathParam]);
      expect(props).toHaveProperty([spec.pathParam]);
      expect(required).toContain(spec.pathParam);
      expect(spec.cli === undefined || spec.cli.positional !== undefined).toBe(true);
    }
    for (const name of spec.queryParams ?? []) expect(props).toHaveProperty([name]);
    for (const name of required) expect(props).toHaveProperty([name]);

    const cli = spec.cli;
    if (cli) {
      expect(cli.positional === undefined).toBe(spec.pathParam === undefined);
      for (const field of cli.bodyFlags ?? []) expect(props).toHaveProperty([field]);
      expect(cli.bodyFlags === undefined || spec.hasBody === true).toBe(true);
      for (const field of Object.keys(cli.flagNames ?? {})) {
        expect([...(cli.bodyFlags ?? []), ...(spec.queryParams ?? [])]).toContain(field);
      }
    }
  });
});

describe("tool-dispatch.ts", () => {
  it("imports nothing, so the Next.js route can load it by relative path", () => {
    const source = readFileSync(join(__dirname, "..", "tool-dispatch.ts"), "utf8");
    expect(source).not.toMatch(/^\s*(import|export\s.*\sfrom)\s/m);
    expect(source).not.toMatch(/\brequire\(/);
  });

  it("percent-encodes the path value into one segment", () => {
    const spec = specs.find((s) => s.def.name === "pages_get")!;
    expect(resolvePath(spec, "../a/b?c=$&")).toBe("/contests/..%2Fa%2Fb%3Fc%3D%24%26");
  });

  it("drops undeclared arguments from the body and reports them", () => {
    const spec = specs.find((s) => s.def.name === "pages_publish")!;
    expect(buildToolRequest(spec, { contest_id: "c 1", prizes: [], end_date: "2030-01-01" })).toEqual({
      method: "PATCH",
      path: "/contests/c%201",
      query: undefined,
      body: { status: "active", end_date: "2030-01-01" },
      dropped: ["prizes"],
    });
  });
});

describe("CLI command lookup", () => {
  it.each(["toString", "constructor", "__proto__", "hasOwnProperty"])(
    "%s is an unknown command, not a crash",
    async (command) => {
      const err: string[] = [];
      const io = {
        env: { TOKEI_API_KEY: "k" },
        fetchImpl: async () => {
          throw new Error("no network in this test");
        },
        stdout: () => {},
        stderr: (line: string) => err.push(line),
      } as unknown as Io;
      expect(await main([command], io)).toBe(2);
      expect(JSON.parse(err[0]).error.message).toMatch(new RegExp(`^Unknown command "${command}"`));
    },
  );
});
