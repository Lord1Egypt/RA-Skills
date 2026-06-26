import fs from "node:fs/promises";
import path from "node:path";

import { CONFIG_FILE_NAME, DEFAULT_BASE_URL, DEFAULT_CONFIG } from "./constants.js";
import { exitWithError, findOption, hasFlag, maskSecret, printJson, sanitizeForOutput } from "./utils.js";

export function configFilePath(configDir) {
  return path.join(configDir, CONFIG_FILE_NAME);
}

export async function loadConfig(configDir) {
  try {
    const contents = await fs.readFile(configFilePath(configDir), "utf8");
    const parsed = JSON.parse(contents);
    return {
      ...structuredClone(DEFAULT_CONFIG),
      ...parsed,
      apps: parsed.apps || {},
      profiles: parsed.profiles || {},
    };
  } catch (error) {
    if (error.code === "ENOENT") {
      return structuredClone(DEFAULT_CONFIG);
    }
    exitWithError("Failed to load config.", error.message);
  }
}

export async function saveConfig(configDir, config) {
  await fs.mkdir(configDir, { recursive: true });
  await fs.writeFile(configFilePath(configDir), `${JSON.stringify(config, null, 2)}\n`, "utf8");
}

export function printConfigSummary(configDir, config) {
  const display = {
    configDir,
    currentApp: config.currentApp || null,
    currentProfile: config.currentProfile || null,
    apps: Object.fromEntries(
      Object.entries(config.apps).map(([name, app]) => [
        name,
        {
          baseUrl: app.baseUrl,
          apiKey: maskSecret(app.apiKey),
        },
      ]),
    ),
    profiles: Object.fromEntries(
      Object.entries(config.profiles).map(([name, profile]) => [
        name,
        {
          cookie: profile.cookie ? maskSecret(profile.cookie) : "",
          authToken: profile.authToken ? maskSecret(profile.authToken) : "",
          ct0: profile.ct0 ? maskSecret(profile.ct0) : "",
        },
      ]),
    ),
  };

  printJson(display);
}

export function resolveAppState(state, config) {
  const configuredApp = state.appName
    ? config.apps[state.appName]
    : config.currentApp
      ? config.apps[config.currentApp]
      : null;

  if (state.appName && !configuredApp) {
    exitWithError(`Unknown app profile: ${state.appName}`);
  }

  return {
    appName: state.appName || config.currentApp || "",
    apiKey: state.apiKey || process.env.TWEXAPI_KEY || configuredApp?.apiKey || "",
    baseUrl: (
      state.baseUrl ||
      process.env.TWEXAPI_BASE_URL ||
      configuredApp?.baseUrl ||
      DEFAULT_BASE_URL
    ).replace(/\/+$/, ""),
  };
}

export function resolveProfile(config, preferredName) {
  const profileName = preferredName || config.currentProfile || "";
  if (!profileName) {
    return { profileName: "", profile: null };
  }

  const profile = config.profiles[profileName];
  if (!profile) {
    exitWithError(`Unknown profile: ${profileName}`);
  }

  return { profileName, profile };
}

export function profileCredential(profile) {
  if (!profile) {
    return "";
  }
  if (profile.cookie) {
    return profile.cookie;
  }
  if (profile.authToken && profile.ct0) {
    return `ct0=${profile.ct0}; auth_token=${profile.authToken}`;
  }
  if (profile.authToken) {
    return profile.authToken;
  }
  return "";
}

export function resolveCookieArg(args, state, config, required = true) {
  const explicitCookie = findOption(args, "--cookie");
  if (explicitCookie) {
    return explicitCookie;
  }

  const explicitProfile = findOption(args, "--profile") || state.profileName;
  const { profile } = resolveProfile(config, explicitProfile);
  const savedValue = profileCredential(profile);
  if (savedValue) {
    return savedValue;
  }

  if (required && !state.dryRun) {
    exitWithError("Missing cookie/auth token.", "Pass --cookie or configure a saved profile.");
  }
  return "";
}

export async function handleConfigCommand(state, config, args) {
  const action = args[1] || "show";
  if (action === "show") {
    printConfigSummary(state.configDir, config);
    return;
  }

  if (action === "path") {
    console.log(configFilePath(state.configDir));
    return;
  }

  exitWithError("Unknown config command.", "Use: config show | config path");
}

export async function handleAuthAppsCommand(state, config, args) {
  const action = args[2];

  if (action === "add") {
    const name = findOption(args, "--name");
    const apiKey = findOption(args, "--api-key");
    if (!name || !apiKey) {
      exitWithError("Usage: twexapi auth apps add --name <name> --api-key <key> [--base-url <url>]");
    }

    const baseUrl = (findOption(args, "--base-url") || DEFAULT_BASE_URL).replace(/\/+$/, "");
    config.apps[name] = { apiKey, baseUrl };
    if (!config.currentApp || hasFlag(args, "--use")) {
      config.currentApp = name;
    }
    await saveConfig(state.configDir, config);

    printJson({
      saved: name,
      currentApp: config.currentApp,
      app: {
        baseUrl,
        apiKey: maskSecret(apiKey),
      },
    });
    return;
  }

  if (action === "list") {
    printJson({
      currentApp: config.currentApp || null,
      apps: Object.entries(config.apps).map(([name, app]) => ({
        name,
        isCurrent: name === config.currentApp,
        baseUrl: app.baseUrl,
        apiKey: maskSecret(app.apiKey),
      })),
    });
    return;
  }

  if (action === "use") {
    const name = args[3];
    if (!name) {
      exitWithError("Usage: twexapi auth apps use <name>");
    }
    if (!config.apps[name]) {
      exitWithError(`Unknown app profile: ${name}`);
    }
    config.currentApp = name;
    await saveConfig(state.configDir, config);
    printJson({ currentApp: name });
    return;
  }

  if (action === "remove") {
    const name = args[3];
    if (!name) {
      exitWithError("Usage: twexapi auth apps remove <name>");
    }
    if (!config.apps[name]) {
      exitWithError(`Unknown app profile: ${name}`);
    }
    delete config.apps[name];
    if (config.currentApp === name) {
      config.currentApp = "";
    }
    await saveConfig(state.configDir, config);
    printJson({ removed: name, currentApp: config.currentApp || null });
    return;
  }

  exitWithError("Unknown auth apps command.", "Use: add | list | use | remove");
}

export async function handleAuthProfilesCommand(state, config, args) {
  const action = args[2];

  if (action === "add") {
    const name = findOption(args, "--name");
    const cookie = findOption(args, "--cookie");
    const authToken = findOption(args, "--auth-token");
    const ct0 = findOption(args, "--ct0");
    if (!name || (!cookie && !authToken)) {
      exitWithError("Usage: twexapi auth profiles add --name <name> [--cookie <value> | --auth-token <value>] [--ct0 <value>]");
    }

    config.profiles[name] = {
      ...(cookie ? { cookie } : {}),
      ...(authToken ? { authToken } : {}),
      ...(ct0 ? { ct0 } : {}),
    };
    if (!config.currentProfile || hasFlag(args, "--use")) {
      config.currentProfile = name;
    }
    await saveConfig(state.configDir, config);

    printJson({
      saved: name,
      currentProfile: config.currentProfile,
      profile: sanitizeForOutput(config.profiles[name]),
    });
    return;
  }

  if (action === "list") {
    printJson({
      currentProfile: config.currentProfile || null,
      profiles: Object.entries(config.profiles).map(([name, profile]) => ({
        name,
        isCurrent: name === config.currentProfile,
        hasCookie: Boolean(profile.cookie),
        hasAuthToken: Boolean(profile.authToken),
        hasCt0: Boolean(profile.ct0),
      })),
    });
    return;
  }

  if (action === "use") {
    const name = args[3];
    if (!name) {
      exitWithError("Usage: twexapi auth profiles use <name>");
    }
    if (!config.profiles[name]) {
      exitWithError(`Unknown profile: ${name}`);
    }
    config.currentProfile = name;
    await saveConfig(state.configDir, config);
    printJson({ currentProfile: name });
    return;
  }

  if (action === "remove") {
    const name = args[3];
    if (!name) {
      exitWithError("Usage: twexapi auth profiles remove <name>");
    }
    if (!config.profiles[name]) {
      exitWithError(`Unknown profile: ${name}`);
    }
    delete config.profiles[name];
    if (config.currentProfile === name) {
      config.currentProfile = "";
    }
    await saveConfig(state.configDir, config);
    printJson({ removed: name, currentProfile: config.currentProfile || null });
    return;
  }

  exitWithError("Unknown auth profiles command.", "Use: add | list | use | remove");
}
