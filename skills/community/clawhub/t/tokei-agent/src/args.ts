// Zero-dependency argument parser for the tokei-agent CLI.
//
// The first bare token is the command; remaining bare tokens are positionals.
// Flags may be written as `--name value`, `--name=value`, or a bare `--name`
// (recorded as an empty string). The single-dash `-v` short flag is supported.

export interface ParsedArgs {
  command: string | undefined;
  positionals: string[];
  flags: Record<string, string>;
}

export function parseArgs(argv: string[]): ParsedArgs {
  let command: string | undefined;
  const positionals: string[] = [];
  const flags: Record<string, string> = {};

  for (let i = 0; i < argv.length; i++) {
    const token = argv[i];

    if (token.startsWith("--")) {
      const body = token.slice(2);
      const eq = body.indexOf("=");
      if (eq !== -1) {
        flags[body.slice(0, eq)] = body.slice(eq + 1);
      } else {
        const next = argv[i + 1];
        if (next !== undefined && !next.startsWith("-")) {
          flags[body] = next;
          i++;
        } else {
          flags[body] = "";
        }
      }
      continue;
    }

    if (token.startsWith("-") && token.length > 1) {
      flags[token.slice(1)] = "";
      continue;
    }

    if (command === undefined) {
      command = token;
    } else {
      positionals.push(token);
    }
  }

  return { command, positionals, flags };
}
