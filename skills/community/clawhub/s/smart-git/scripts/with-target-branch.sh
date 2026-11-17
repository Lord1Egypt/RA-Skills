#!/usr/bin/env bash
# Build an ephemeral config that sets pullRequestCreation.targetBranch.
# smart-commit-host-agent has no --target-branch CLI flag; use this overlay instead.
#
# If pullRequestCreation.configFilePath is set, this script merges that creation
# overlay (same first-existing-file rule as the CLI, resolved against <repo-dir>),
# then writes targetBranch last and clears configFilePath so the CLI does not
# reload the overlay and override the conversation-specified target.
#
# Usage: with-target-branch.sh <base-config-path> <target-branch> [repo-dir]
# stdout: absolute path to temp config; stderr: notes; exit 0 on success.

set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: with-target-branch.sh <base-config-path> <target-branch> [repo-dir]" >&2
  exit 1
fi

base_config="$1"
target_branch="$2"
repo_dir="${3:-}"

if [[ ! -f "${base_config}" ]]; then
  echo "Base config does not exist: ${base_config}" >&2
  exit 1
fi

if [[ -n "${repo_dir}" && ! -d "${repo_dir}" ]]; then
  echo "Repo directory does not exist: ${repo_dir}" >&2
  exit 1
fi

# Normalize: strip quotes and origin/ prefix
target_branch="${target_branch%\"}"
target_branch="${target_branch#\"}"
target_branch="${target_branch%\'}"
target_branch="${target_branch#\'}"
target_branch="${target_branch#origin/}"
target_branch="$(printf '%s' "${target_branch}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"

if [[ -z "${target_branch}" ]]; then
  echo "target-branch is empty" >&2
  exit 1
fi

if [[ -z "${repo_dir}" ]]; then
  repo_dir="$(pwd)"
fi
repo_dir="$(cd "${repo_dir}" && pwd)"

tmp_dir="${TMPDIR:-/tmp}/scha-config-overlays"
mkdir -p "${tmp_dir}"
# macOS mktemp requires the XXXXXX suffix at the end (no extension after it).
out_path="$(mktemp "${tmp_dir}/scha-cfg.XXXXXX")"
mv "${out_path}" "${out_path}.json"
out_path="${out_path}.json"

node -e '
const fs = require("fs");
const path = require("path");
const basePath = process.argv[1];
const targetBranch = process.argv[2];
const outPath = process.argv[3];
const repoDir = process.argv[4];

function parseObject(value, label) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new Error(label + " must be a JSON object.");
  }
  return value;
}

function parseConfigFilePathList(value) {
  return String(value || "")
    .split(",")
    .map((part) => part.trim())
    .filter((part) => part.length > 0);
}

function resolveFirstExisting(configuredPaths, baseDirectory) {
  const attempted = [];
  for (const configuredPath of configuredPaths) {
    const resolvedPath = path.isAbsolute(configuredPath)
      ? path.normalize(configuredPath)
      : path.resolve(baseDirectory, configuredPath);
    attempted.push({ configuredPath, resolvedPath });
    try {
      if (fs.existsSync(resolvedPath) && fs.statSync(resolvedPath).isFile()) {
        return resolvedPath;
      }
    } catch {
      // keep looking
    }
  }
  const tried = attempted
    .map((item) => item.configuredPath + " (resolved to " + item.resolvedPath + ")")
    .join("; ");
  throw new Error("Configured pullRequestCreation.configFilePath not found. Tried: " + tried);
}

function loadCreationOverlay(configuredValue, baseDirectory) {
  const configuredPaths = parseConfigFilePathList(configuredValue);
  if (configuredPaths.length === 0) {
    return {};
  }
  const overlayPath = resolveFirstExisting(configuredPaths, baseDirectory);
  const content = fs.readFileSync(overlayPath, "utf8");
  if (!content.trim()) {
    throw new Error("pull request creation config file must not be empty: " + overlayPath);
  }
  let parsed;
  try {
    parsed = JSON.parse(content);
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    throw new Error("pull request creation config file is not valid JSON: " + overlayPath + ". " + message);
  }
  const root = parseObject(parsed, "pull request creation config file " + overlayPath);
  const extraRoot = Object.keys(root).find((key) => key !== "smartCommitHostAgent");
  if (extraRoot) {
    throw new Error(
      "pull request creation config file " + overlayPath +
      " only supports the smartCommitHostAgent config object; unsupported key: " + extraRoot + "."
    );
  }
  if (!Object.hasOwn(root, "smartCommitHostAgent")) {
    return {};
  }
  const canonical = parseObject(root.smartCommitHostAgent, overlayPath + ":smartCommitHostAgent");
  const extraKey = Object.keys(canonical).find((key) => key !== "pullRequestCreation");
  if (extraKey) {
    throw new Error(
      overlayPath + ":smartCommitHostAgent only supports pullRequestCreation settings; unsupported key: " + extraKey + "."
    );
  }
  if (!Object.hasOwn(canonical, "pullRequestCreation")) {
    return {};
  }
  const section = parseObject(
    canonical.pullRequestCreation,
    overlayPath + ":smartCommitHostAgent.pullRequestCreation"
  );
  for (const forbidden of ["autoCreateAfterPush", "configFilePath"]) {
    if (Object.hasOwn(section, forbidden)) {
      throw new Error(
        overlayPath + ":smartCommitHostAgent.pullRequestCreation." + forbidden +
        " is not supported inside a pull request creation config file."
      );
    }
  }
  return section;
}

try {
  const raw = JSON.parse(fs.readFileSync(basePath, "utf8"));
  if (!raw.smartCommitHostAgent || typeof raw.smartCommitHostAgent !== "object") {
    throw new Error("Config is missing the smartCommitHostAgent root key");
  }
  const root = { ...raw.smartCommitHostAgent };
  const creation = { ...(root.pullRequestCreation || {}) };
  const overlay = loadCreationOverlay(creation.configFilePath, repoDir);
  root.pullRequestCreation = {
    ...creation,
    ...overlay,
    targetBranch,
    configFilePath: ""
  };
  raw.smartCommitHostAgent = root;
  fs.writeFileSync(outPath, JSON.stringify(raw, null, 2) + "\n", "utf8");
} catch (error) {
  const message = error instanceof Error ? error.message : String(error);
  console.error(message);
  process.exit(1);
}
' "${base_config}" "${target_branch}" "${out_path}" "${repo_dir}"

echo "Wrote ephemeral config with targetBranch=${target_branch}: ${out_path}" >&2
echo "${out_path}"
