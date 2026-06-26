#!/usr/bin/env python3
"""Patch OpenClaw dist JS bundles to append a Telegram private-chat footer.

Safety notes:
- This script modifies files under the OpenClaw installation directory.
- Always run with --dry-run first to see which files would be touched.
- The script creates timestamped backups (*.bak.telegram-footer.*) before writing.
- If anything fails, it restores from backup automatically.

This version handles two layers:
- runner/finalPayload candidate bundles
- Telegram delivery/live outbound layer bundles

Important boundary:
- patch/verify success only proves candidate bundle patching + syntax validity
- final acceptance still requires a real Telegram private-chat reply showing the footer
- if you only hot-refresh and never load a new process, treat it as unverified
"""

import argparse
import datetime as dt
import os
import pathlib
import re
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True

MARKER_START = "/* OPENCLAW_TELEGRAM_STATUS_FOOTER_START */"
MARKER_END = "/* OPENCLAW_TELEGRAM_STATUS_FOOTER_END */"

RUNNER_SNIPPET_TEMPLATE = r'''
__MARKER_START__
const __ocSessionLooksTelegramDirect =
  typeof sessionKey === "string" && sessionKey.includes(":telegram:direct:");
const __ocReplyProvider =
  sessionCtx?.Surface || sessionCtx?.Provider || activeSessionEntry?.lastChannel || activeSessionEntry?.channel || "";
const __ocReplyChatType =
  sessionCtx?.ChatType || activeSessionEntry?.chatType || "";
const __ocShouldAppendStatusFooter =
  (__ocSessionLooksTelegramDirect || __ocReplyProvider === "telegram") &&
  __ocReplyChatType !== "group" &&
  __ocReplyChatType !== "channel";

const __ocEscapeHtml = (str) => String(str)
  .replace(/&/g, "&amp;")
  .replace(/</g, "&lt;")
  .replace(/>/g, "&gt;")
  .replace(/\"/g, "&quot;")
  .replace(/'/g, "&#39;");

const __ocFormatTokens = (value) => {
  if (typeof value !== "number" || !Number.isFinite(value) || value <= 0) return "?";
  if (value >= 1000000) return `${(value / 1000000).toFixed(value >= 10000000 ? 0 : 1).replace(/\.0$/, "")}M`;
  if (value >= 1000) return `${(value / 1000).toFixed(value >= 100000 ? 0 : 1).replace(/\.0$/, "")}k`;
  return String(Math.round(value));
};

const __ocBuildTokenUsage = (used, limit) => {
  const usedLabel = __ocFormatTokens(used);
  const limitLabel = __ocFormatTokens(limit);
  return limitLabel === "?" ? usedLabel : `${usedLabel}/${limitLabel}`;
};

const __ocAppendFooter = (payloads, footerText, footerHtml) => {
  let index = -1;
  for (let i = payloads.length - 1; i >= 0; i -= 1) {
    if (payloads[i]?.html || payloads[i]?.text) {
      index = i;
      break;
    }
  }

  if (index === -1) return [...payloads, { text: footerText }];

  const existing = payloads[index];
  const existingText = existing?.text ?? "";
  const existingHtml = existing?.html ?? "";
  const textSep = existingText.endsWith("\n") ? "" : "\n";
  const htmlSep = existingHtml.endsWith("<br>") ? "" : "<br>";
  const next = {
    ...existing,
    text: existingText ? `${existingText}${textSep}${footerText}` : footerText,
    html: existingHtml ? `${existingHtml}${htmlSep}${footerHtml}` : void 0
  };
  const updated = payloads.slice();
  updated[index] = next;
  return updated;
};

if (__ocShouldAppendStatusFooter) {
  const __ocTotalTokens = resolveFreshSessionTotalTokens(activeSessionEntry);
  const __ocThinkingLevel = activeSessionEntry?.thinkingLevel || "default";
  const __ocContextLimit = contextTokensUsed ?? activeSessionEntry?.contextTokens ?? null;

  const __ocStatusFooter = [
    `🧠 ${providerUsed && modelUsed ? `${providerUsed}/${modelUsed}` : modelUsed || "unknown"}`,
    `💭 Think: ${__ocThinkingLevel}`,
    `📊 ${__ocBuildTokenUsage(__ocTotalTokens, __ocContextLimit)}`
  ].join(" ");

  const __ocFooterText = `──────────\n${__ocStatusFooter}`;
  const __ocFooterHtml = `──────────<br>${__ocEscapeHtml(__ocStatusFooter)}`;

  finalPayloads = __ocAppendFooter(finalPayloads, __ocFooterText, __ocFooterHtml);
}
__MARKER_END__
'''.strip("\n")

DELIVERY_HELPERS_TEMPLATE = r'''
__MARKER_START__
function __ocFooterAlreadyPresent(text) {
	return typeof text === "string" && text.includes("🧠 ") && text.includes("💭 Think:") && text.includes("📊 ");
}
function __ocFormatFooterTokens(value) {
	if (typeof value !== "number" || !Number.isFinite(value) || value <= 0) return "?";
	if (value >= 1e6) return `${(value / 1e6).toFixed(value >= 1e7 ? 0 : 1).replace(/\.0$/, "")}M`;
	if (value >= 1e3) return `${(value / 1e3).toFixed(value >= 1e5 ? 0 : 1).replace(/\.0$/, "")}k`;
	return String(Math.round(value));
}
function __ocBuildFooterTokenUsage(used, limit) {
	const usedLabel = __ocFormatFooterTokens(used);
	const limitLabel = __ocFormatFooterTokens(limit);
	return limitLabel === "?" ? usedLabel : `${usedLabel}/${limitLabel}`;
}
async function __ocReadSessionEntryForFooter(sessionKey) {
	if (!sessionKey) return null;
	try {
		const fs = await import("node:fs/promises");
		const homeDir = typeof process !== "undefined" && process?.env?.HOME ? process.env.HOME : "/root";
		const raw = await fs.readFile(`${homeDir}/.openclaw/agents/main/sessions/sessions.json`, "utf8");
		const parsed = JSON.parse(raw);
		const entry = parsed && typeof parsed === "object" ? parsed[sessionKey] : null;
		return entry && typeof entry === "object" ? entry : null;
	} catch {
		return null;
	}
}
async function __ocMaybeAppendTelegramStatusFooter(text, params) {
	if (typeof text !== "string" || !text.trim()) return text;
	if (__ocFooterAlreadyPresent(text)) return text;
	const sessionKey = typeof params?.sessionKeyForInternalHooks === "string" ? params.sessionKeyForInternalHooks : "";
	const chatIdText = typeof params?.chatId === "string" ? params.chatId : String(params?.chatId ?? "");
	const looksTelegramDirect = sessionKey.includes(":telegram:direct:") || (!!chatIdText && !chatIdText.startsWith("-") && sessionKey.includes(":telegram:"));
	if (!looksTelegramDirect) return text;
	const entry = await __ocReadSessionEntryForFooter(sessionKey);
	if (!entry) return text;
	const provider = typeof entry.modelProvider === "string" && entry.modelProvider ? entry.modelProvider : "unknown";
	const model = typeof entry.model === "string" && entry.model ? entry.model : "unknown";
	const thinkingLevel = typeof entry.thinkingLevel === "string" && entry.thinkingLevel ? entry.thinkingLevel : "default";
	const totalTokens = typeof entry.totalTokens === "number" ? entry.totalTokens : null;
	const contextTokens = typeof entry.contextTokens === "number" ? entry.contextTokens : null;
	const statusFooter = [
		`🧠 ${provider}/${model}`,
		`💭 Think: ${thinkingLevel}`,
		`📊 ${__ocBuildFooterTokenUsage(totalTokens, contextTokens)}`
	].join(" ");
	const separator = text.endsWith("\n") ? "" : "\n";
	return `${text}${separator}\n──────────\n${statusFooter}`;
}
__MARKER_END__
'''.strip("\n")

RUNNER_SNIPPET = RUNNER_SNIPPET_TEMPLATE.replace("__MARKER_START__", MARKER_START).replace("__MARKER_END__", MARKER_END)
DELIVERY_HELPERS = DELIVERY_HELPERS_TEMPLATE.replace("__MARKER_START__", MARKER_START).replace("__MARKER_END__", MARKER_END)

RUNNER_PATTERN = re.compile(
    r"(if\s*\(\s*responseUsageLine\s*\)\s*finalPayloads\s*=\s*appendUsageLine\(\s*finalPayloads\s*,\s*responseUsageLine\s*\);)",
    flags=re.M,
)
RUNNER_NEEDLE_SUBSTR = "appendUsageLine(finalPayloads, responseUsageLine)"
DELIVERY_FN_ANCHOR = "async function deliverReplies(params) {"
DELIVERY_LOOP_ANCHOR = "\t\tlet reply = originalReply;"
DELIVERY_LOOP_INSERT = (
    "\t\tif (typeof reply?.text === \"string\" && reply.text) reply = {\n"
    "\t\t\t...reply,\n"
    "\t\t\ttext: await __ocMaybeAppendTelegramStatusFooter(reply.text, params)\n"
    "\t\t};"
)
DELIVERY_INLINE_NEEDLE = "__ocMaybeAppendTelegramStatusFooter(reply.text, params)"
DELIVERY_HELPER_NEEDLE = "async function __ocMaybeAppendTelegramStatusFooter(text, params)"
MARKER_BLOCK_RE = re.compile(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), flags=re.S)
TARGET_GLOBS = [
    "agent-runner.runtime-*.js",
    "reply-*.js",
    "compact-*.js",
    "pi-embedded-*.js",
    "plugin-sdk/thread-bindings-*.js",
    "model-selection-*.js",
    "auth-profiles-*.js",
    "delivery-*.js",
]
LEGACY_BLOCK_RE = re.compile(
    r"\n?\s*const shouldAppendStatusFooter = activeSessionEntry\?\.chatType !== \"group\" && activeSessionEntry\?\.chatType !== \"channel\" && \(activeSessionEntry\?\.lastChannel === \"telegram\" \|\| activeSessionEntry\?\.channel === \"telegram\"\);\s*"
    r"if \(shouldAppendStatusFooter\) \{\s*"
    r"const totalTokens = resolveFreshSessionTotalTokens\(activeSessionEntry\);\s*"
    r"const statusFooter = \[\s*"
    r"`🧠 Model: \$\{providerUsed && modelUsed \? `\$\{providerUsed\}/\$\{modelUsed\}` : modelUsed \|\| \"unknown\"\}`\s*,\s*"
    r"`📊 Context: \$\{formatTokens\(typeof totalTokens === \"number\" && Number\.isFinite\(totalTokens\) && totalTokens > 0 \? totalTokens : null, contextTokensUsed \?\? activeSessionEntry\?\.contextTokens \?\? null\)\}`\s*"
    r"\]\.join\(\"  \"\);\s*"
    r"finalPayloads = appendUsageLine\(finalPayloads, statusFooter\);\s*"
    r"\}\s*",
    flags=re.S,
)


def verify_node_syntax(path: pathlib.Path):
    result = subprocess.run(["node", "--check", str(path)], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        details = (result.stderr or result.stdout or "node --check failed").strip()
        raise RuntimeError(details)


def _is_backup_path(path: pathlib.Path) -> bool:
    return ".bak.telegram-footer." in path.name


def _read_text(path: pathlib.Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def _detect_kind(path: pathlib.Path, text: str) -> str | None:
    if (
        DELIVERY_FN_ANCHOR in text
        and "for (const originalReply of params.replies) {" in text
        and "emitTelegramMessageSentHooks" in text
    ):
        return "delivery"
    if RUNNER_NEEDLE_SUBSTR in text and RUNNER_PATTERN.search(text):
        return "runner"
    return None


def _looks_like_target_by_content(path: pathlib.Path) -> bool:
    text = _read_text(path)
    return _detect_kind(path, text) is not None


def iter_target_files(dist: pathlib.Path, auto_discover: bool = False) -> list[pathlib.Path]:
    files: set[pathlib.Path] = set()
    for pattern in TARGET_GLOBS:
        for fp in dist.glob(pattern):
            if fp.is_file() and not _is_backup_path(fp):
                files.add(fp)

    if auto_discover:
        for fp in dist.rglob("*.js"):
            if not fp.is_file() or _is_backup_path(fp):
                continue
            try:
                if _looks_like_target_by_content(fp):
                    files.add(fp)
            except OSError:
                continue

    return sorted(files)


def analyze_file(path: pathlib.Path) -> dict:
    content = _read_text(path)
    kind = _detect_kind(path, content)
    has_marker = MARKER_START in content
    has_runner_pattern = RUNNER_PATTERN.search(content) is not None
    has_legacy = LEGACY_BLOCK_RE.search(content) is not None
    has_delivery_inline = DELIVERY_INLINE_NEEDLE in content
    has_delivery_helper = DELIVERY_HELPER_NEEDLE in content
    is_candidate = kind is not None or has_marker or has_legacy
    fully_patched = False
    if kind == "runner":
        fully_patched = has_marker
    elif kind == "delivery":
        fully_patched = has_delivery_inline and (has_marker or has_delivery_helper)
    return {
        "path": path,
        "content": content,
        "kind": kind,
        "has_marker": has_marker,
        "has_runner_pattern": has_runner_pattern,
        "has_legacy": has_legacy,
        "has_delivery_inline": has_delivery_inline,
        "has_delivery_helper": has_delivery_helper,
        "is_candidate": is_candidate,
        "fully_patched": fully_patched,
    }


def _patch_runner_content(content: str) -> tuple[str, int]:
    updated = content
    legacy_removed = 0
    if LEGACY_BLOCK_RE.search(updated):
        updated, legacy_removed = LEGACY_BLOCK_RE.subn("\n", updated)

    if MARKER_START in updated:
        updated, count = MARKER_BLOCK_RE.subn(lambda _m: RUNNER_SNIPPET, updated, count=1)
        if count == 0:
            raise RuntimeError("runner marker block found but could not be replaced")
        return updated, legacy_removed

    match = RUNNER_PATTERN.search(updated)
    if not match:
        raise RuntimeError("runner insertion needle not found in candidate dist bundle")
    replacement = match.group(1) + "\n\n" + RUNNER_SNIPPET
    updated = updated[: match.start()] + replacement + updated[match.end() :]
    return updated, legacy_removed


def _patch_delivery_content(content: str) -> str:
    updated = content
    if MARKER_START in updated:
        updated, count = MARKER_BLOCK_RE.subn(lambda _m: DELIVERY_HELPERS, updated, count=1)
        if count == 0:
            raise RuntimeError("delivery marker block found but could not be replaced")
    elif DELIVERY_HELPER_NEEDLE not in updated:
        if DELIVERY_FN_ANCHOR not in updated:
            raise RuntimeError("delivery function anchor not found")
        updated = updated.replace(DELIVERY_FN_ANCHOR, DELIVERY_HELPERS + "\n" + DELIVERY_FN_ANCHOR, 1)

    if DELIVERY_INLINE_NEEDLE not in updated:
        if DELIVERY_LOOP_ANCHOR not in updated:
            raise RuntimeError("delivery loop anchor not found")
        updated = updated.replace(DELIVERY_LOOP_ANCHOR, DELIVERY_LOOP_ANCHOR + "\n" + DELIVERY_LOOP_INSERT, 1)

    return updated


def patch_file(path: pathlib.Path, dry_run: bool):
    info = analyze_file(path)
    content = info["content"]
    kind = info["kind"]
    if not info["is_candidate"] or not kind:
        print(f"[skip] non-target dist bundle: {path}")
        return {"status": "skip", "candidate": False, "changed": False}

    try:
        if kind == "runner":
            updated, legacy_removed = _patch_runner_content(content)
            extra = f" (legacy cleaned: {legacy_removed})" if legacy_removed else ""
        else:
            updated = _patch_delivery_content(content)
            extra = ""
    except Exception as exc:
        print(f"[err] patch planning failed: {path}", file=sys.stderr)
        print(f"[err] reason: {exc}", file=sys.stderr)
        return {"status": "error", "candidate": True, "changed": False}

    changed = updated != content
    if not changed:
        print(f"[skip] already up to date: {path}")
        return {"status": "ok", "candidate": True, "changed": False}

    action = "update patch" if info["has_marker"] else "patch"
    if dry_run:
        print(f"[dry-run] would {action}: {path}{extra}")
        return {"status": "ok", "candidate": True, "changed": True}

    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = path.with_suffix(path.suffix + f".bak.telegram-footer.{ts}")
    shutil.copy2(path, backup)
    try:
        path.write_text(updated, encoding="utf-8")
        verify_node_syntax(path)
    except Exception as exc:
        shutil.copy2(backup, path)
        print(f"[err] patch failed, restored backup: {path}", file=sys.stderr)
        print(f"[err] reason: {exc}", file=sys.stderr)
        return {"status": "error", "candidate": True, "changed": False}

    print(f"[ok] {action}ed: {path}{extra}")
    print(f"[ok] backup      : {backup}")
    print(f"[ok] syntax check: node --check passed")
    return {"status": "ok", "candidate": True, "changed": True}


def preflight(dist: pathlib.Path, dry_run: bool) -> int:
    print("[warn] This tool patches OpenClaw installation files (dist JS bundles).")
    print("[warn] Recommended: run --dry-run first and review the candidate files.")
    node_path = shutil.which("node")
    if not node_path:
        print("[err] node not found in PATH (required for syntax validation via node --check)", file=sys.stderr)
        return 2
    if not dist.exists() or not dist.is_dir():
        print(f"[err] dist directory not found: {dist}", file=sys.stderr)
        return 2
    if not dry_run:
        if not os.access(dist, os.W_OK):
            print(f"[err] no write permission for dist directory: {dist} (try sudo or adjust permissions)", file=sys.stderr)
            return 2
    else:
        if not os.access(dist, os.R_OK):
            print(f"[err] no read permission for dist directory: {dist}", file=sys.stderr)
            return 2
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Patch OpenClaw dist files to append Telegram status footer.")
    parser.add_argument("--dist", default="/usr/lib/node_modules/openclaw/dist", help="OpenClaw dist directory")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, do not write")
    parser.add_argument("--auto-discover", action="store_true", help="Also scan dist/**/*.js for supported runner/delivery anchors")
    parser.add_argument("--list-targets", action="store_true", help="Print resolved target file list, then exit")
    parser.add_argument("--verify", action="store_true", help="Exit non-zero if any real candidate file lacks the patch")
    args = parser.parse_args()

    dist = pathlib.Path(args.dist)
    rc = preflight(dist, dry_run=args.dry_run)
    if rc != 0:
        return rc

    files = iter_target_files(dist, auto_discover=args.auto_discover)
    if not files:
        print("[err] no target dist files found", file=sys.stderr)
        return 2

    if args.list_targets:
        for fp in files:
            info = analyze_file(fp)
            print(
                f"{fp}  candidate={str(info['is_candidate']).lower()}  kind={info['kind'] or '-'}  marker={str(info['has_marker']).lower()}  fully_patched={str(info['fully_patched']).lower()}  legacy={str(info['has_legacy']).lower()}"
            )
        return 0

    if args.verify:
        missing: list[pathlib.Path] = []
        candidate_count = 0
        for fp in files:
            info = analyze_file(fp)
            if not info["is_candidate"] or not info["kind"]:
                continue
            candidate_count += 1
            if not info["fully_patched"]:
                missing.append(fp)
        if missing:
            for fp in missing:
                print(f"[err] patch missing/incomplete in candidate: {fp}", file=sys.stderr)
            return 1
        print(f"[ok] patch present in {candidate_count} candidate target(s)")
        return 0

    changed = 0
    errors = 0
    for fp in files:
        result = patch_file(fp, dry_run=args.dry_run)
        if result.get("status") == "error":
            errors += 1
        if result.get("changed"):
            changed += 1

    if errors:
        print(f"[done] errors: {errors}", file=sys.stderr)
        return 1

    if args.dry_run:
        print(f"[done] changed files: {changed}" if changed else "[done] no files changed")
        return 0

    print(f"[done] changed files: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
