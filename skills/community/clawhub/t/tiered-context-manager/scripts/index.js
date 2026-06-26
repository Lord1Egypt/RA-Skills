// tiered-compactor/index.js — OpenClaw plugin entry point
// Registers TieredContextEngine via the plugin API.

/**
 * Plugin manifest — must export these properties.
 * @type {{ id: string, name: string, version: string, description: string, register: function }}
 */
const manifest = {
  id: "tiered-compactor",
  name: "Tiered Compactor",
  version: "1.0.0",
  description: "Tiered context compaction engine with version-aware fallback.",

  /**
   * register — called by OpenClaw when the plugin is loaded.
   * @param {object} api - Plugin API object built by buildPluginApi().
   * @param {object} api.registerContextEngine - (id: string, factory: () => ContextEngine) => void
   * @param {object} api.logger - Logger instance
   * @param {object} api.config - Resolved plugin config (package.json openclaw.config)
   * @param {object} api.runtime - Runtime info (version, agent, subagent, etc.)
   */
  register(api) {
    const logger = api.logger ?? console;

    // Locate the openclaw dist directory to dynamically import the runtime compaction module.
    // In an ESM context (openclaw's bundler), require.resolve works because openclaw
    // is installed as a proper npm package. We use require.resolve to get a stable
    // absolute path to the openclaw package, then navigate to dist/.
    let compactEmbeddedPiSessionDirect;
    try {
      const path = require("path");
      // Resolve openclaw's package.json to get the package root, then go to dist/
      const openclawPkgPath = require.resolve("openclaw/package.json");
      const openclawDistDir = path.dirname(openclawPkgPath);
      const compactRuntimePath = path.join(openclawDistDir, "dist", "compact.runtime-C0J2-J-T.js");
      // eslint-disable-next-line global-require
      const mod = require(compactRuntimePath);
      compactEmbeddedPiSessionDirect = mod.compactEmbeddedPiSessionDirect;
    } catch (err) {
      logger.error(
        "[tiered-compactor] Failed to resolve compactEmbeddedPiSessionDirect from openclaw dist. " +
        `Error: ${err.message}. Plugin will not be registered.`
      );
      return;
    }

    if (typeof compactEmbeddedPiSessionDirect !== "function") {
      logger.error(
        "[tiered-compactor] compactEmbeddedPiSessionDirect is not a function. Plugin will not be registered."
      );
      return;
    }

    const openclawVersion = api.runtime?.version ?? "0.0.0";

    // Lazily instantiate the engine so construction errors are caught
    // before the registration call returns.
    const engineFactory = () => {
      // eslint-disable-next-line global-require
      const { TieredContextEngine } = require("./tiered-engine.js");
      return new TieredContextEngine({
        openclawVersion,
        compactEmbeddedPiSessionDirect,
        logger
      });
    };

    api.registerContextEngine("tiered-compactor", engineFactory);

    logger.info(
      `[tiered-compactor] Registered context engine "tiered-compactor" for OpenClaw ${openclawVersion}. ` +
      "NOTE: Set plugins.slots.contextEngine to \"tiered-compactor\" in openclaw config to activate."
    );
  }
};

module.exports = manifest;
module.exports.default = manifest;
