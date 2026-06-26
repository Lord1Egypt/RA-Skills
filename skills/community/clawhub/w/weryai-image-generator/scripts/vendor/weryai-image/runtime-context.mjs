import path from "node:path";
import process from "node:process";

function normalizedString(value) {
  return typeof value === "string" ? value.trim() : "";
}

function resolvePath(value) {
  const normalized = normalizedString(value);
  return normalized ? path.resolve(normalized) : "";
}

export function parseProjectArg(argv = process.argv.slice(2)) {
  for (let i = 0; i < argv.length; i++) {
    const current = argv[i];
    if (current === "--project") {
      const value = argv[i + 1];
      return value && !value.startsWith("-") ? path.resolve(value) : "";
    }
    if (current?.startsWith("--project=")) {
      return path.resolve(current.slice("--project=".length));
    }
  }
  return "";
}

export function resolveSkillNamespace(options = {}) {
  const explicit = normalizedString(options.explicitSkillNamespace ?? process.env.IMAGE_SKILL_NAMESPACE);
  if (explicit) return explicit;

  const skillDir = resolvePath(options.skillDir ?? process.env.IMAGE_SKILL_DIR);
  if (skillDir) return path.basename(skillDir);

  const packageJsonPath = resolvePath(options.packageJsonPath ?? process.env.npm_package_json);
  if (packageJsonPath) return path.basename(path.dirname(packageJsonPath));

  const cwd = resolvePath(options.cwd ?? process.cwd());
  if (cwd) return path.basename(cwd);

  const packageName = normalizedString(options.packageName ?? process.env.npm_package_name);
  if (packageName) return packageName;

  return normalizedString(options.fallbackSkillNamespace) || "image-generation-2";
}

export function hasProjectScopedConfig() {
  return false;
}

export function resolveProjectRoot(options = {}) {
  const argv = options.argv ?? process.argv.slice(2);
  return (
    resolvePath(options.explicitProjectRoot || parseProjectArg(argv)) ||
    resolvePath(options.envProjectRoot ?? process.env.IMAGE_PROJECT_ROOT) ||
    resolvePath(options.initCwd ?? process.env.INIT_CWD) ||
    resolvePath(options.cwd ?? process.cwd()) ||
    process.cwd()
  );
}

export function resolveRuntimeContext(options = {}) {
  const skillDir = resolvePath(options.skillDir ?? process.env.IMAGE_SKILL_DIR ?? options.cwd ?? process.cwd());
  const skillNamespace = resolveSkillNamespace({
    ...options,
    skillDir: skillDir || options.skillDir,
  });
  const projectRoot = resolveProjectRoot({
    ...options,
    skillDir: skillDir || options.skillDir,
    explicitSkillNamespace: skillNamespace,
  });
  return {
    skillDir: skillDir || resolvePath(process.cwd()) || process.cwd(),
    skillNamespace,
    projectRoot,
  };
}
