#!/usr/bin/env node

const builtins = [
  ["iTime", "Elapsed time in seconds."],
  ["iResolution", "Viewport resolution; use `.xy` for width and height."],
  ["iMouse", "Mouse state packed into a vec4."],
  ["iFrame", "Current frame count."],
  ["iTimeDelta", "Time between frames."],
  ["iChannel0..3", "Texture or buffer sampler inputs."],
  ["fragCoord", "Current pixel coordinate passed into mainImage."],
];

const channels = [
  "iChannel0..3 can be textures, videos, cubemaps, microphones, webcams, or buffer outputs.",
  "If the effect depends on a prior pass, say that it is multi-pass before porting.",
  "Procedural single-pass effects are the easiest ShaderToy exports.",
];

const porting = {
  webgl: [
    "Replace mainImage with main.",
    "Map iTime -> uTime and iResolution -> uResolution.",
    "Derive uv from gl_FragCoord.xy / uResolution.",
    "Create a fullscreen quad and pass uniforms manually.",
    "Replace channel dependencies with bound textures or remove them temporarily.",
  ],
  three: [
    "Wrap the fragment logic in a ShaderMaterial or fullscreen pass host.",
    "Map iTime -> uTime and iResolution -> uResolution.",
    "Preserve screen-space math if the shader is a fullscreen effect.",
    "For mesh materials, decide whether the effect truly belongs in screen space or material UV space.",
    "Handle channel samplers as Three.js textures or render targets.",
  ],
  r3f: [
    "Port the shader into a shaderMaterial inside a minimal R3F component.",
    "Update uTime in useFrame.",
    "Pass uResolution from canvas size when needed.",
    "If the effect is really fullscreen, consider a screen quad instead of a mesh material.",
    "Treat channels and feedback passes explicitly; do not hide them in React state.",
  ],
};

const debugLists = {
  "black-screen": [
    "Replace mainImage output with a constant visible color.",
    "Visualize fragCoord / iResolution.xy as color.",
    "Remove channel sampling temporarily.",
    "Check whether the shader actually depends on a missing Buffer A/B/C/D pass.",
    "Port only after the ShaderToy version is visibly correct.",
  ],
  channels: [
    "Check which iChannel slots are used.",
    "Identify whether each channel is a texture, video, cubemap, or buffer feedback input.",
    "Temporarily replace each sampled channel with a constant if the effect is broken.",
    "Do not treat a buffer-dependent effect as single-pass during porting.",
  ],
  buffers: [
    "List every Image / Buffer pass first.",
    "Check whether Buffer A output is sampled by Image or another buffer.",
    "Verify feedback order and whether the effect relies on previous frames.",
    "Explain clearly if the target runtime needs render targets or ping-pong buffers.",
  ],
};

const demos = {
  "single-pass": {
    title: "Demo: single-pass",
    items: [
      "Start from: assets/shadertoy-single-pass-demo/index.html",
      "Use when the ShaderToy effect is a single Image pass with no buffer feedback.",
      "Best first export target for uv, noise, gradient, ripple, and most procedural effects.",
    ],
  },
  feedback: {
    title: "Demo: feedback",
    items: [
      "Start from: assets/shadertoy-feedback-notes.txt",
      "Use when the ShaderToy effect relies on Buffer A/B/C/D or previous-frame feedback.",
      "Treat this as a multi-pass export plan, not a drop-in single-pass fragment shader.",
    ],
  },
};

function buildScaffold(target, effectShape) {
  const demoKey = effectShape === "feedback" ? "feedback" : "single-pass";
  const portTarget = ["webgl", "three", "r3f"].includes(target) ? target : "webgl";
  const portList = porting[portTarget];
  const demo = demos[demoKey];

  return {
    title: `Scaffold: ${target} + ${effectShape}`,
    items: [
      demo.items[0],
      `Porting target: ${portTarget}`,
      demo.items[1],
      "First confirm whether the original ShaderToy uses only Image or also Buffer A/B/C/D.",
      `Then follow the ${portTarget} porting checklist one item at a time.`,
      effectShape === "feedback"
        ? "Do not flatten feedback into single-pass code; plan render targets or ping-pong buffers explicitly."
        : "Keep the fragment logic close to ShaderToy form until the host renders correctly.",
    ],
  };
}

function usage() {
  console.log(`ShaderToy helper

Usage:
  node shadertoy.js builtins [--json]
  node shadertoy.js channels [--json]
  node shadertoy.js port <webgl|three|r3f> [--json]
  node shadertoy.js debug <black-screen|channels|buffers> [--json]
  node shadertoy.js intake <request> [--json]
  node shadertoy.js demo <single-pass|feedback> [--json]
  node shadertoy.js scaffold <webgl|three|r3f> <single-pass|feedback> [--json]
`);
}

function wantsJson(args) {
  return args.includes("--json");
}

function output(value, json) {
  if (json) {
    console.log(JSON.stringify(value, null, 2));
    return;
  }
  if (Array.isArray(value)) {
    value.forEach((item, index) => {
      if (Array.isArray(item)) {
        console.log(`${item[0]}: ${item[1]}`);
      } else {
        console.log(`${index + 1}. ${item}`);
      }
    });
    return;
  }
  console.log(value.title);
  value.items.forEach((item, index) => {
    console.log(`${index + 1}. ${item}`);
  });
}

function buildIntake(request) {
  const lower = String(request || "").toLowerCase();
  const target = lower.includes("r3f")
    ? "React Three Fiber"
    : lower.includes("three")
      ? "Three.js"
      : lower.includes("webgl")
        ? "raw WebGL"
        : "unknown: clarify target runtime";

  return {
    title: `ShaderToy intake: ${request}`,
    items: [
      `Target runtime: ${target}`,
      "Check whether the original effect is single-pass Image or uses Buffer A/B/C/D.",
      "List every ShaderToy builtin in use: iTime, iResolution, iMouse, iChannel0..3, iFrame.",
      "Identify whether the effect is purely procedural or depends on textures / feedback buffers.",
      "Keep the original ShaderToy structure visible until the effect works.",
      "Port built-ins to explicit host uniforms only after the logic is understood.",
    ],
  };
}

const args = process.argv.slice(2);
const command = args[0];
const json = wantsJson(args);

if (!command || command === "help" || command === "--help" || command === "-h") {
  usage();
  process.exit(0);
}

if (command === "builtins") {
  output(builtins, json);
  process.exit(0);
}

if (command === "channels") {
  output(channels, json);
  process.exit(0);
}

if (command === "port") {
  const target = args[1];
  const checklist = porting[target];
  if (!checklist) {
    console.error("Unknown port target.");
    process.exit(1);
  }
  output({ title: `Porting checklist: ${target}`, items: checklist }, json);
  process.exit(0);
}

if (command === "debug") {
  const kind = args[1];
  const checklist = debugLists[kind];
  if (!checklist) {
    console.error("Unknown debug type.");
    process.exit(1);
  }
  output({ title: `Debug checklist: ${kind}`, items: checklist }, json);
  process.exit(0);
}

if (command === "intake") {
  const request = args.filter((arg, index) => index > 0 && arg !== "--json").join(" ").trim();
  if (!request) {
    console.error("Please provide a ShaderToy task.");
    process.exit(1);
  }
  output(buildIntake(request), json);
  process.exit(0);
}

if (command === "demo") {
  const kind = args[1];
  const demo = demos[kind];
  if (!demo) {
    console.error("Unknown demo type.");
    process.exit(1);
  }
  output(demo, json);
  process.exit(0);
}

if (command === "scaffold") {
  const target = args[1];
  const effectShape = args[2];
  if (!target || !effectShape) {
    console.error("Please provide a target and effect shape.");
    process.exit(1);
  }
  output(buildScaffold(target, effectShape), json);
  process.exit(0);
}

console.error("Unknown command.");
process.exit(1);
