import type { Tool } from "@modelcontextprotocol/sdk/types.js";
import { callRemoteTool, listRemoteTools } from "./remote-client.js";
import { UPLOAD_TOOL } from "./tool-specs.js";
import type { RemoteConfig, ToolInvocationResult } from "./types.js";
import { uploadLocalFile } from "./upload-file.js";

function asError(error: unknown): ToolInvocationResult {
  const message = error instanceof Error ? error.message : String(error);
  return {
    content: [{ type: "text", text: `Error: ${message}` }],
    isError: true,
  };
}

export async function listExposedTools(config?: RemoteConfig): Promise<Tool[]> {
  const remoteTools = await listRemoteTools(config);
  return [...remoteTools, UPLOAD_TOOL as Tool];
}

export async function invokeExposedTool(
  name: string,
  args: Record<string, unknown> | undefined,
  config?: RemoteConfig,
): Promise<ToolInvocationResult> {
  try {
    if (name === "uploadFile") {
      const filePath = typeof args?.filePath === "string" ? args.filePath : "";
      if (!filePath) {
        throw new Error("filePath is required");
      }

      const fileName = typeof args?.fileName === "string" ? args.fileName : undefined;
      const cdnUrl = await uploadLocalFile(filePath, fileName, config);
      return {
        content: [{ type: "text", text: cdnUrl }],
      };
    }

    return await callRemoteTool(name, args, config) as ToolInvocationResult;
  } catch (error) {
    return asError(error);
  }
}
