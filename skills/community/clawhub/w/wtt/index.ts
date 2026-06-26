import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { wttPlugin } from "./dist/channel.js";

export { processWTTCommandText } from "./dist/channel.js";

const plugin = {
  id: "wtt",
  name: "WTT",
  description: "WTT channel plugin",
  configSchema: {
    type: "object",
    additionalProperties: false,
    properties: {},
  },
  register(api: any) {
    api.registerChannel({ plugin: wttPlugin });

    // Provide a built-in CLI command so npm/plugin install is immediately usable
    // without manually installing a global `openclaw-wtt-bootstrap` binary.
    api.registerCli(
      ({ program }: { program: any }) => {
        program
          .command("wtt-bootstrap")
          .description("Bootstrap WTT plugin account/config")
          .requiredOption("--agent-id <agent_id>", "WTT agent id")
          .requiredOption("--token <token>", "WTT agent token")
          .option("--cloud-url <url>", "WTT API base", "https://www.waxbyte.com")
          .action((opts: { agentId: string; token: string; cloudUrl?: string }) => {
            const script = fileURLToPath(new URL("./bin/openclaw-wtt-bootstrap.mjs", import.meta.url));
            const args = [
              script,
              "--agent-id",
              String(opts.agentId || ""),
              "--token",
              String(opts.token || ""),
              "--cloud-url",
              String(opts.cloudUrl || "https://www.waxbyte.com"),
            ];
            const res = spawnSync(process.execPath, args, {
              stdio: "inherit",
              env: process.env,
            });
            if (typeof res.status === "number" && res.status !== 0) {
              process.exitCode = res.status;
            }
          });
      },
      { commands: ["wtt-bootstrap"] },
    );
  },
};

export default plugin;
