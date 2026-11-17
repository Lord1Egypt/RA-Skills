/** @jest-environment node */
import { parseArgs } from "../args.js";

describe("parseArgs", () => {
  it("reads the command as the first positional", () => {
    expect(parseArgs(["me"])).toEqual({
      command: "me",
      positionals: [],
      flags: {},
    });
  });

  it("collects positionals after the command", () => {
    expect(parseArgs(["pages:get", "abc-123"])).toEqual({
      command: "pages:get",
      positionals: ["abc-123"],
      flags: {},
    });
  });

  it("parses `--flag value` pairs", () => {
    const parsed = parseArgs(["pages:list", "--status", "active", "--per-page", "10"]);
    expect(parsed.command).toBe("pages:list");
    expect(parsed.flags).toEqual({ status: "active", "per-page": "10" });
  });

  it("parses `--flag=value` pairs", () => {
    const parsed = parseArgs(["pages:list", "--status=active"]);
    expect(parsed.flags).toEqual({ status: "active" });
  });

  it("treats a trailing flag with no value as an empty string", () => {
    const parsed = parseArgs(["entries:list", "id", "--email"]);
    expect(parsed.flags).toEqual({ email: "" });
    expect(parsed.positionals).toEqual(["id"]);
  });

  it("records --help and --version as flags with no command", () => {
    expect(parseArgs(["--help"])).toEqual({
      command: undefined,
      positionals: [],
      flags: { help: "" },
    });
    expect(parseArgs(["--version"]).flags).toEqual({ version: "" });
  });

  it("maps the -v short flag to version", () => {
    expect(parseArgs(["-v"]).flags).toEqual({ v: "" });
  });

  it("returns an undefined command for empty argv", () => {
    expect(parseArgs([])).toEqual({
      command: undefined,
      positionals: [],
      flags: {},
    });
  });
});
