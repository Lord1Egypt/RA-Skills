import { createHash, randomUUID } from "node:crypto";

export function sha256(value: string): string {
  return createHash("sha256").update(value).digest("hex");
}

export function deterministicId(prefix: string, seed: string): string {
  return `${prefix}_${sha256(seed).slice(0, 20)}`;
}

export function createId(prefix: string): string {
  return `${prefix}_${randomUUID().replace(/-/g, "")}`;
}
