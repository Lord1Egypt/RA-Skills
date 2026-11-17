declare const _default: Omit<{
    id: string;
    name: string;
    description: string;
    kind?: import("openclaw/plugin-sdk/plugin-entry").OpenClawPluginDefinition["kind"];
    configSchema?: import("openclaw/plugin-sdk/plugin-entry").OpenClawPluginConfigSchema | (() => import("openclaw/plugin-sdk/plugin-entry").OpenClawPluginConfigSchema);
    reload?: import("openclaw/plugin-sdk/plugin-entry").OpenClawPluginDefinition["reload"];
    nodeHostCommands?: import("openclaw/plugin-sdk/plugin-entry").OpenClawPluginDefinition["nodeHostCommands"];
    securityAuditCollectors?: import("openclaw/plugin-sdk/plugin-entry").OpenClawPluginDefinition["securityAuditCollectors"];
    register: NonNullable<import("openclaw/plugin-sdk/plugin-entry").OpenClawPluginDefinition["register"]>;
}, "configSchema"> & {
    configSchema: import("openclaw/plugin-sdk/plugin-entry").OpenClawPluginConfigSchema;
};
export default _default;
