import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
declare const sessionArchivePlugin: {
    id: string;
    name: string;
    description: string;
    configSchema: {
        parse(value: unknown): {
            dbPath: string | undefined;
        };
    };
    register(api: OpenClawPluginApi): void;
};
export default sessionArchivePlugin;
