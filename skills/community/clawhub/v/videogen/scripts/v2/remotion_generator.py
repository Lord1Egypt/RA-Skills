#!/usr/bin/env python3
"""
videogen v2 — Remotion 视频代码生成器

用法：
    python remotion_generator.py gen \
        --scene-names "开场|Agent Loop|MCP" \
        --timings "20|50|35" \
        --narrations "旁白1||旁白2" \
        --visuals "terminal|ring|hub" \
        --output /path/to/project/
"""

import argparse
import re
import shutil
import subprocess
from pathlib import Path


# ═══════════════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════════════

class Scene:
    def __init__(self, name: str, label: str, duration_sec: int,
                 narration: str, visual_type: str):
        self.name = name          # 英文驼峰
        self.label = label        # 中文标签
        self.duration_sec = duration_sec
        self.narration = narration
        self.visual_type = visual_type


# ═══════════════════════════════════════════════════════
# 工具
# ═══════════════════════════════════════════════════════

def to_pascal(name: str) -> str:
    """中文/空格分隔的名称转 PascalCase"""
    cleaned = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]", "", name)
    return cleaned[:1].upper() + cleaned[1:] if cleaned else "Scene"


def sh(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


# ═══════════════════════════════════════════════════════
# 场景组件生成
# ═══════════════════════════════════════════════════════

# 每个场景类型的组件代码（不使用 f-string，避免 {} 冲突）
COMPONENT_TEMPLATES = {

    "terminal": """\
import React from "react";
import { AbsoluteFill } from "remotion";
import { Terminal } from "../components/Terminal";

export const SCENE_NAME: React.FC<{ narration: string }> = ({ narration }) => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <Terminal text="NARRATION" startFrame={5} />
    </AbsoluteFill>
  );
};
""",

    "architecture": """\
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";

export const SCENE_NAME: React.FC<{ narration: string }> = ({ narration }) => {
  const frame = useCurrentFrame();
  const nodes = [
    { label: "AI Model", sublabel: "大脑", x: 0.5, y: 0.05 },
    { label: "Tools", sublabel: "工具层", x: 0.92, y: 0.5 },
    { label: "Session", sublabel: "状态管理", x: 0.5, y: 0.92 },
    { label: "Permissions", sublabel: "权限控制", x: 0.08, y: 0.5 },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0e17", justifyContent: "center" }}>
      <svg width={1080} height={1080} viewBox="0 0 1080 1080">
        {[0,1,2,3].map((i) => {
          const sources = [
            { x: 540, y: 54 },
            { x: 995, y: 540 },
            { x: 540, y: 995 },
            { x: 85, y: 540 },
          ];
          const progress = Math.min(1, Math.max(0, (frame - i * 8) / 30));
          return (
            <line
              key={i}
              x1={sources[i].x} y1={sources[i].y}
              x2={540 + (540 - sources[i].x) * progress}
              y2={540 + (540 - sources[i].y) * progress}
              stroke="#00d4ff"
              strokeWidth={3}
              opacity={0.8}
            />
          );
        })}
        {[0,1,2,3].map((i) => {
          const pos = [
            { x: 540, y: 54 },
            { x: 995, y: 540 },
            { x: 540, y: 995 },
            { x: 85, y: 540 },
          ];
          const p = Math.min(1, Math.max(0, (frame - 30 - i * 10) / 20));
          return (
            <g key={i} opacity={p}>
              <circle cx={pos[i].x} cy={pos[i].y} r={90} fill="#141922" stroke="#00d4ff" strokeWidth={2} />
              <text x={pos[i].x} y={pos[i].y - 5} textAnchor="middle" fill="#00d4ff" fontSize={72} fontWeight="bold" fontFamily="system-ui, sans-serif">{nodes[i].label}</text>
              <text x={pos[i].x} y={pos[i].y + 14} textAnchor="middle" fill="#666" fontSize={22} fontFamily="system-ui, sans-serif">{nodes[i].sublabel}</text>
            </g>
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};
""",

    "ring": """\
import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { RingDiagram } from "../components/FlowChart";

export const SCENE_NAME: React.FC<{ narration: string }> = ({ narration }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const DURATION = DURATION_SEC;
  const nodes = ["计划", "选工具", "执行", "评估"];
  const nodeDetails = [
    ["接收任务", "用户给出目标，如：把API改成支持流式输出"],
    ["规划步骤", "AI分析需要改哪些文件，按什么顺序执行"],
    ["调用工具", "Harness接收请求，校验权限，执行命令"],
    ["评估结果", "AI判断：成功？报错？需要修复？"],
  ];
  const nodeDuration = (DURATION * fps) / nodes.length;
  const currentNode = Math.min(nodes.length - 1, Math.floor(frame / nodeDuration));

  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0e17", justifyContent: "center" }}>
      <RingDiagram nodes={nodes} centerText="Agent Loop" color="#00d4ff" activeIndex={currentNode} />
      <div style={{ position: "absolute", bottom: 120, left: "50%", transform: "translateX(-50%)", textAlign: "center" }}>
        <div style={{ color: "#00d4ff", fontSize: 32, fontWeight: "bold", marginBottom: 12 }}>{nodeDetails[currentNode][0]}</div>
        <div style={{ color: "#888", fontSize: 18 }}>{nodeDetails[currentNode][1]}</div>
      </div>
    </AbsoluteFill>
  );
};
""",

    "layers": """\
import React from "react";
import { AbsoluteFill } from "remotion";
import { LayerDiagram } from "../components/Diagrams";

export const SCENE_NAME: React.FC<{ narration: string }> = ({ narration }) => {
  const layers = [
    { label: "Session", sublabel: "会话历史 · 跨会话持久化", color: "#ff6b6b" },
    { label: "Context Window", sublabel: "Token 上限 · 自动 Compact 压缩", color: "#ffd93d" },
    { label: "CLAUDE.md", sublabel: "项目级记忆 · 项目专属规则", color: "#6bcb77" },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0e17", justifyContent: "center" }}>
      <LayerDiagram layers={layers} direction="top-down" />
    </AbsoluteFill>
  );
};
""",

    "toggles": """\
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";

export const SCENE_NAME: React.FC<{ narration: string }> = ({ narration }) => {
  const frame = useCurrentFrame();
  const modes = [
    { label: "Read-only", desc: "只读 · 禁止任何写入", color: "#ff6b6b", active: frame > 20 },
    { label: "Workspace-write", desc: "工作区写入 · 禁止高危命令", color: "#ffd93d", active: frame > 60 },
    { label: "Danger-full-access", desc: "完全信任 · 可执行任意操作", color: "#27C93F", active: frame > 100 },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0e17", justifyContent: "center" }}>
      <svg width={1080} height={800} viewBox="0 0 1080 800">
        <text x={540} y={60} textAnchor="middle" fill="#888" fontSize={72} fontFamily="system-ui, sans-serif">Permission Mode · 权限模式</text>
        {modes.map((mode, i) => {
          const delay = i * 40;
          const progress = Math.min(1, Math.max(0, (frame - delay) / 20));
          const y = 160 + i * 160;
          return (
            <g key={i} opacity={progress}>
              <rect x={250} y={y} width={580} height={100} rx={12} fill="#141922" stroke={mode.active ? mode.color : "#333"} strokeWidth={2} />
              <text x={280} y={y + 40} fill={mode.active ? mode.color : "#666"} fontSize={48} fontWeight="bold" fontFamily="system-ui, sans-serif">{mode.label}</text>
              <text x={280} y={y + 68} fill="#555" fontSize={28} fontFamily="system-ui, sans-serif">{mode.desc}</text>
              <rect x={720} y={y + 25} width={80} height={50} rx={25} fill={mode.active ? mode.color : "#333"} opacity={mode.active ? 1 : 0.5} />
              <circle cx={mode.active ? 775 : 745} cy={y + 50} r={20} fill="#fff" />
            </g>
          );
        })}
        {frame > 140 && (
          <g opacity={Math.min(1, (frame - 140) / 20)}>
            <rect x={250} y={620} width={580} height={80} rx={8} fill="#1a1a2e" stroke="#00d4ff" strokeWidth={1} strokeDasharray="4 2" />
            <text x={540} y={655} textAnchor="middle" fill="#00d4ff" fontSize={72} fontFamily="system-ui, sans-serif">PreToolUse Hook · 工具执行前置拦截点</text>
            <text x={540} y={680} textAnchor="middle" fill="#555" fontSize={26} fontFamily="system-ui, sans-serif">检查参数 · 拒绝执行 · 附加逻辑</text>
          </g>
        )}
      </svg>
    </AbsoluteFill>
  );
};
""",

    "hub": """\
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";

export const SCENE_NAME: React.FC<{ narration: string }> = ({ narration }) => {
  const frame = useCurrentFrame();
  const nodes = [
    { label: "Claude Code", sublabel: "核心系统", x: 0.2, y: 0.5, color: "#6bcb77" },
    { label: "MCP Hub", sublabel: "协议接口", x: 0.5, y: 0.5, color: "#00d4ff" },
    { label: "Database", sublabel: "数据库", x: 0.8, y: 0.25, color: "#ffd93d" },
    { label: "GitHub", sublabel: "代码托管", x: 0.8, y: 0.5, color: "#ffd93d" },
    { label: "Custom", sublabel: "定制工具", x: 0.8, y: 0.75, color: "#ffd93d" },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0e17", justifyContent: "center" }}>
      <svg width={1080} height={1080} viewBox="0 0 1080 1080">
        {nodes.map((node, i) => {
          const progress = Math.min(1, Math.max(0, (frame - i * 10) / 20));
          const x = node.x * 1080;
          const y = node.y * 1080;
          const isHub = i === 1;
          return (
            <g key={i} opacity={progress}>
              <circle cx={x} cy={y} r={isHub ? 70 : 50} fill={isHub ? "#00d4ff20" : "#141922"} stroke={node.color} strokeWidth={isHub ? 3 : 2} />
              <text x={x} y={y} textAnchor="middle" dominantBaseline="middle" fill={node.color} fontSize={isHub ? 16 : 14} fontWeight="bold" fontFamily="system-ui, sans-serif">{node.label}</text>
              <text x={x} y={y + 25} textAnchor="middle" fill="#555" fontSize={24} fontFamily="system-ui, sans-serif">{node.sublabel}</text>
            </g>
          );
        })}
        <line x1={216} y1={540} x2={540} y2={540} stroke="#00d4ff" strokeWidth={3} opacity={0.7} />
        <line x1={540} y1={540} x2={864} y2={270} stroke="#00d4ff" strokeWidth={2} opacity={0.6} strokeDasharray="6 3" />
        <line x1={540} y1={540} x2={864} y2={540} stroke="#00d4ff" strokeWidth={2} opacity={0.6} strokeDasharray="6 3" />
        <line x1={540} y1={540} x2={864} y2={810} stroke="#00d4ff" strokeWidth={2} opacity={0.6} strokeDasharray="6 3" />
      </svg>
      <div style={{ position: "absolute", bottom: 60, left: "50%", transform: "translateX(-50%)", color: "#555", fontSize: 14, fontFamily: "system-ui, sans-serif" }}>
        MCP = Model Context Protocol · 开放标准接口
      </div>
    </AbsoluteFill>
  );
};
""",

    "closing": """\
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { TypewriterText } from "../components/Typography";

export const SCENE_NAME: React.FC<{ narration: string }> = ({ narration }) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <TypewriterText
        text="NARRATION"
        fontSize={72}
        color="#ffffff"
        fontFamily="system-ui, sans-serif"
        startFrame={5}
        charsPerFrame={2}
        x={0.5}
        y={0.45}
        anchor="center"
      />
      {frame > 80 && (
        <div style={{ position: "absolute", bottom: 120, left: "50%", transform: "translateX(-50%)", color: "#444", fontSize: 16, fontFamily: "system-ui, sans-serif", letterSpacing: 2 }}>
          关注我，继续拆解 AI 时代的工程能力
        </div>
      )}
    </AbsoluteFill>
  );
};
""",

    "generic": """\
import React from "react";
import { AbsoluteFill } from "remotion";

export const SCENE_NAME: React.FC<{ narration: string }> = ({ narration }) => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0e17", justifyContent: "center", alignItems: "center" }}>
      <div style={{ color: "#00d4ff", fontSize: 36, fontWeight: "bold", textAlign: "center" }}>
        SCENE_LABEL
      </div>
      <div style={{ color: "#666", fontSize: 18, marginTop: 20, textAlign: "center", maxWidth: 700 }}>
        SCENE_NARRATION
      </div>
    </AbsoluteFill>
  );
};
""",
}


def generate_scene_file(scene: Scene) -> str:
    """生成单个场景的 TSX 文件"""
    template = COMPONENT_TEMPLATES.get(scene.visual_type, COMPONENT_TEMPLATES["generic"])

    # 替换占位符
    content = template
    content = content.replace("SCENE_NAME", scene.name)
    content = content.replace("SCENE_LABEL", scene.label)
    content = content.replace("DURATION_SEC", str(scene.duration_sec))

    # 旁白文本：截取合适长度，避免特殊字符问题
    narration = scene.narration[:80].replace("`", "\\`").replace("\\", "\\\\")
    content = content.replace("NARRATION", narration)
    content = content.replace("SCENE_NARRATION", scene.narration[:60])

    return content


# ═══════════════════════════════════════════════════════
# Video.tsx 生成（使用 JS 模板，避免 Python f-string 问题）
# ═══════════════════════════════════════════════════════

VIDEO_TSX_TEMPLATE = """\
import React from "react";
import {
  AbsoluteFill,
  Sequence,
  useVideoConfig,
} from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
SCENE_IMPORT_STATEMENTS

// 场景定义
const SCENES = [
SCENE_ARRAY
];

// 旁白文本
const NARRATIONS = {
SCENE_NARRATIONS_OBJECT
};

export const Video: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <TransitionSeries>
        {SCENES.map((scene) => {
          const narration = NARRATIONS[scene.name] || "";
          return (
            <TransitionSeries.Sequence
              key={scene.name}
              durationInFrames={scene.durationInFrames}
            >
              <TransitionSeries.Transition
                presentation={fade()}
                timing={linearTiming({ durationInFrames: 15 })}
              />
              <SceneWrapper name={scene.name} narration={narration} />
            </TransitionSeries.Sequence>
          );
        })}
      </TransitionSeries>
    </AbsoluteFill>
  );
};

// 场景渲染分发
const SceneWrapper: React.FC<{ name: string; narration: string }> = ({ name, narration }) => {
  switch (name) {
// SCENE_CASES
    default: return <div style={{ color: "#fff" }}>Unknown: {name}</div>;
  }
};
"""


def generate_video_tsx(scenes: list[Scene]) -> str:
    fps = 30

    # Import 语句
    imports = "\n".join(
        f'import {{ {s.name} }} from "./scenes/{s.name}";'
        for s in scenes
    )

    # SCENES 定义（需包装在数组里）
    scene_defs = ",\n".join(
        f'        {{ name: "{s.name}", durationInFrames: {s.duration_sec * fps}, fps: {fps} }}'
        for s in scenes
    )

    # NARRATIONS 对象
    narrations = ",\n".join(
        f'  {s.name}: `{s.narration.replace("`", "\\`")}`'
        for s in scenes
    )

    # Switch cases
    cases = "\n".join(
        f'    case "{s.name}": return <{s.name} narration={{narration}} />;'
        for s in scenes
    )

    content = VIDEO_TSX_TEMPLATE
    content = content.replace("SCENE_IMPORT_STATEMENTS", imports)
    content = content.replace("SCENE_ARRAY", scene_defs)
    content = content.replace("SCENE_NARRATIONS_OBJECT", narrations)
    content = content.replace("// SCENE_CASES", cases)

    return content


# ═══════════════════════════════════════════════════════
# Root.tsx 生成
# ═══════════════════════════════════════════════════════

def generate_root_tsx(scenes: list[Scene], fps: int = 30) -> str:
    total = sum(s.duration_sec for s in scenes) * fps
    return f"""\
import {{ Composition }} from "remotion";
import {{ Video }} from "./Video";

export const RemotionRoot: React.FC = () => {{
  return (
    <>
      <Composition
        id="Video"
        component={{Video}}
        durationInFrames={{{total}}}
        fps={{{fps}}}
        width={{1080}}
        height={{1920}}
      />
    </>
  );
}};
"""


# ═══════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════

def main():
    import sys

    parser = argparse.ArgumentParser(description="Remotion 视频代码生成器")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("gen", help="生成 Remotion 项目代码")
    p.add_argument("--scene-names", required=True,
                   help="场景名称，用 | 分隔")
    p.add_argument("--timings", default="",
                   help="各场景时长（秒），用 | 分隔")
    p.add_argument("--narrations", default="",
                   help="各场景旁白，用 || 分隔（注意：||是分隔符本身）")
    p.add_argument("--visuals", default="",
                   help="视觉类型，用 | 分隔")
    p.add_argument("--output", required=True, help="项目目录")
    p.add_argument("--fps", type=int, default=30)

    args = parser.parse_args()

    # 解析
    names = args.scene_names.split("|")
    timings = [int(x) for x in args.timings.split("|")] if args.timings else []
    narrations = args.narrations.split("||") if args.narrations else [""]
    visuals = args.visuals.split("|") if args.visuals else []

    scenes = []
    for i, name in enumerate(names):
        scenes.append(Scene(
            name=to_pascal(name),
            label=name,
            duration_sec=timings[i] if i < len(timings) else 30,
            narration=narrations[i] if i < len(narrations) else "",
            visual_type=visuals[i] if i < len(visuals) else "generic",
        ))

    output_dir = Path(args.output)
    scenes_dir = output_dir / "src" / "scenes"
    scenes_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "src").mkdir(exist_ok=True)

    print(f"🎬 生成 Remotion 项目: {len(scenes)} 场景, {sum(s.duration_sec for s in scenes)} 秒")

    # 复制项目配置文件
    template_dir = Path(__file__).parent.parent.parent / "remotion-template"
    for cfg in ["package.json", "tsconfig.json", "remotion.config.ts"]:
        src = template_dir / cfg
        if src.exists():
            shutil.copy2(src, output_dir / cfg)
    # 复制 public/ 目录
    pub_src = template_dir / "public"
    if pub_src.exists():
        shutil.copytree(pub_src, output_dir / "public", dirs_exist_ok=True)
    # 复制 src/index.ts
    idx_src = template_dir / "src" / "index.ts"
    if idx_src.exists():
        shutil.copy2(idx_src, output_dir / "src" / "index.ts")

    # 复制组件库
    components_dir = template_dir / "src" / "components"
    if components_dir.exists():
        components_dest = output_dir / "src" / "components"
        components_dest.mkdir(parents=True, exist_ok=True)
        for f in components_dir.glob("*.tsx"):
            shutil.copy2(f, components_dest / f.name)
        print(f"  ✅ 组件库: {len(list(components_dir.glob('*.tsx')))} 个文件")

    # 生成场景文件
    print("\n  生成场景组件...")
    for s in scenes:
        code = generate_scene_file(s)
        path = scenes_dir / f"{s.name}.tsx"
        path.write_text(code)
        print(f"    ✅ {s.name}.tsx ({s.visual_type})")

    # 生成 Video.tsx
    print("\n  生成 Video.tsx...")
    video_code = generate_video_tsx(scenes)
    (output_dir / "src" / "Video.tsx").write_text(video_code)
    print(f"    ✅ Video.tsx")

    # 生成 Root.tsx
    print("\n  生成 Root.tsx...")
    root_code = generate_root_tsx(scenes, args.fps)
    (output_dir / "src" / "Root.tsx").write_text(root_code)
    print(f"    ✅ Root.tsx")

    print(f"\n{'='*50}")
    print(f"✅ 项目生成完成: {output_dir}")
    print(f"\n下一步（推荐两阶段渲染，防止 timeout 中断）：")
    print(f"  1. cd {output_dir} && npm install")
    print(f"  2. 阶段1 — 渲染帧序列（Remotion 输出 PNG/JPG）：")
    print(f"     npx remotion render Video --output=out/frames --sequence Justice")
    print(f"  3. 阶段2 — ffmpeg 独立编码（不被 timeout 中断）：")
    print(f"     ffmpeg -framerate 30 -i out/frames/element-%04d.png \\")
    print(f"            -c:v libx264 -crf 23 -preset fast \\")
    print(f"            -pix_fmt yuv420p -r 30 out/video_raw.mp4")
    print(f"  4. 合并配音：")
    print(f"     ffmpeg -y -i out/video_raw.mp4 -i voiceover.mp3 \\")
    print(f"            -map 0:v -map 1:a -c:v copy \\")
    print(f"            -c:a aac -b:a 128k -shortest out/video_final.mp4")
    print(f"")
    print(f"  备选（单命令，timeout 可能中断）：")
    print(f"     timeout 600 npx remotion render Video \\")
    print(f"            --codec=h264 --crf=23 --preset=ultrafast \\")
    print(f"            --output=out/video_raw.mp4")


if __name__ == "__main__":
    main()
