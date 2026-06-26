import React from "react";
import { AbsoluteFill } from "remotion";
import { AppleBg, ToolGrid, SceneTag, TagGroup } from "../components/AppleShared";

const TOOLS = [
  "file/read", "bash", "grab", "glob",
  "web/search", "web/fetch", "file/edit", "file/write",
  "grep", "ls", "cd", "mv",
  "mkdir", "rm", "cp", "cat",
  "git/status", "git/diff", "git/log", "git/commit",
  "npm/install", "npm/run", "node", "python",
  "curl", "wget", "ssh", "scp",
  "docker/ps", "docker/exec", "docker/logs", "docker/build",
  "kubectl", "helm", "terraform", "ansible",
  "gh/issue", "gh/pr", "gh/run", "gh/api",
];

export const 工具系统: React.FC = () => {
  return (
    <AppleBg>
      <SceneTag text="工具系统" startFrame={0} color="#64D2FF" />
      <div style={{
        position: "absolute",
        top: "10%",
        left: 0,
        right: 0,
        textAlign: "center",
      }}>
        <div style={{
          fontSize: 22,
          color: "#FFFFFF",
          fontWeight: 700,
          fontFamily: "Inter, -apple-system, sans-serif",
        }}>
          80+ 工具 · 按需加载 · Zod Schema 验证
        </div>
      </div>
      <div style={{
        position: "absolute",
        top: "24%",
        left: 0,
        right: 0,
        display: "flex",
        justifyContent: "center",
      }}>
        <ToolGrid tools={TOOLS} startFrame={8} />
      </div>
      <div style={{ position: "absolute", bottom: 70, left: 0, right: 0 }}>
        <TagGroup
          startFrame={62}
          tags={[
            { text: "核心工具启动时加载", color: "#64D2FF" },
            { text: "扩展工具 tool search 按需发现", color: "#64D2FF" },
            { text: "输出大时存外部 storage", color: "#64D2FF" },
            { text: "模型按需取用，摘要+指针", color: "#64D2FF" },
          ]}
        />
      </div>
    </AppleBg>
  );
};
