import type { AgentCapabilityDescriptor, AgentProviderManifest } from "./contracts";

const buildCapabilityMap = (
  catalog: ReadonlyArray<AgentCapabilityDescriptor>,
): Map<string, AgentCapabilityDescriptor> => {
  const capabilityMap = new Map<string, AgentCapabilityDescriptor>();

  for (const capability of catalog) {
    if (capabilityMap.has(capability.key)) {
      throw new Error(`Duplicate capability key: ${capability.key}`);
    }
    capabilityMap.set(capability.key, capability);
  }

  return capabilityMap;
};

export const defineCapabilityCatalog = <T extends ReadonlyArray<AgentCapabilityDescriptor>>(catalog: T): T => {
  buildCapabilityMap(catalog);
  return catalog;
};

export const defineProviderManifest = <T extends AgentProviderManifest>(
  manifest: T,
  catalog: ReadonlyArray<AgentCapabilityDescriptor>,
): T => {
  const capabilityMap = buildCapabilityMap(catalog);

  for (const capabilityKey of manifest.capabilities) {
    if (!capabilityMap.has(capabilityKey)) {
      throw new Error(
        `Provider "${manifest.providerId}" references unknown capability "${capabilityKey}"`,
      );
    }
  }

  if (manifest.auth.primaryStrategy === "session_handoff") {
    if (!manifest.auth.sessionBrokerPath) {
      throw new Error(
        `Provider "${manifest.providerId}" must define auth.sessionBrokerPath for session handoff`,
      );
    }
    if (!manifest.auth.bridgeTokenTtlSeconds || manifest.auth.bridgeTokenTtlSeconds <= 0) {
      throw new Error(
        `Provider "${manifest.providerId}" must define a positive auth.bridgeTokenTtlSeconds for session handoff`,
      );
    }
  }

  if (manifest.transport === "redirect" && !manifest.ui.callbackPath && !manifest.auth.callback?.path) {
    throw new Error(
      `Provider "${manifest.providerId}" must define a callback path for redirect transport`,
    );
  }

  return manifest;
};

export const pickCapabilities = (
  catalog: ReadonlyArray<AgentCapabilityDescriptor>,
  capabilityKeys: ReadonlyArray<string>,
): AgentCapabilityDescriptor[] => {
  const capabilityMap = buildCapabilityMap(catalog);

  return capabilityKeys.map((key) => {
    const capability = capabilityMap.get(key);
    if (!capability) {
      throw new Error(`Unknown capability requested: ${key}`);
    }
    return capability;
  });
};

export const summarizeCapabilities = (
  catalog: ReadonlyArray<AgentCapabilityDescriptor>,
): Record<string, number> => {
  return catalog.reduce<Record<string, number>>((summary, capability) => {
    summary[capability.status] = (summary[capability.status] ?? 0) + 1;
    return summary;
  }, {});
};
