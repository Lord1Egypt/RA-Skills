import type { OpenClawRuntime } from "openclaw/plugin-sdk";

let runtime: OpenClawRuntime | null = null;

export function setXiaozhiRuntime(r: OpenClawRuntime) {
  runtime = r;
}

export function getXiaozhiRuntime(): OpenClawRuntime {
  if (!runtime) {
    throw new Error("XiaoZhi runtime not initialized");
  }
  return runtime;
}
