#!/usr/bin/env node
import { install, validateInstallPlan } from "./installer.mjs";

const [mode, directory, ...argumentsAfterDirectory] = process.argv.slice(2);
const isDryRun = mode === "--dry-run";
const installDirectory = isDryRun ? directory : mode;

if (
  !installDirectory ||
  argumentsAfterDirectory.length ||
  (!isDryRun && directory)
) {
  console.error(
    "Usage: install.mjs <new-absolute-install-directory>\n       install.mjs --dry-run <new-absolute-install-directory>",
  );
  process.exitCode = 2;
} else {
  try {
    if (isDryRun) {
      const plan = await validateInstallPlan(installDirectory, process.env);
      console.log(
        `Dry-run installation plan:\n${JSON.stringify(plan, null, 2)}`,
      );
    } else {
      const plan = await install(installDirectory, process.env);
      console.log(
        `Installed Proxmox MCP ${plan.releaseVersion} in ${plan.installDirectory}.`,
      );
    }
  } catch (error) {
    console.error(
      error instanceof Error ? error.message : "Installation failed",
    );
    process.exitCode = 1;
  }
}
