import type { OpenClawPluginApi } from "openclaw/plugin-sdk/plugin-runtime";
export declare function createZap1Tools(api: OpenClawPluginApi): {
    name: string;
    label: string;
    description: string;
    parameters: import("@sinclair/typebox").TObject<{}>;
    execute: (_toolCallId: string, _rawParams: Record<string, unknown>) => Promise<import("@mariozechner/pi-agent-core").AgentToolResult<unknown>>;
}[];
