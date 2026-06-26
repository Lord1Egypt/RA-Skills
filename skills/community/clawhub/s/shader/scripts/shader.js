#!/usr/bin/env node

const effectStarters = [
  ["gradient", "Start from UV remapping and color mixing."],
  ["noise", "Use hash/value noise for simple breakup or motion."],
  ["fbm", "Layer noise octaves for clouds, terrain, or flowing texture."],
  ["fresnel", "Use view direction dot normal for edge glow or rim light."],
  ["dissolve", "Use noise + threshold + edge band coloring."],
  ["ripple", "Use radial distance and sin(time - dist * k)."],
  ["scanline", "Use repeated screen-space bands with time modulation."],
  ["pixelate", "Quantize UVs or screen coordinates before sampling."],
];

const boilerplates = {
  fresnel: {
    title: "Boilerplate: fresnel",
    items: [
      "Recommended shape: vertex + fragment shader for material effects.",
      "Uniforms: rimColor, intensity, optional uTime.",
      "Varyings: vNormal plus enough data to compute or pass view direction.",
      "Build order: prove normal visualization first, then add the fresnel term, then add emission or color shaping.",
      "Common bug: normals and view direction are compared in different spaces.",
    ],
  },
  dissolve: {
    title: "Boilerplate: dissolve",
    items: [
      "Recommended shape: fragment-heavy material shader.",
      "Uniforms: uProgress, edgeWidth, edgeColor, optional uTexture.",
      "Varyings: vUv at minimum.",
      "Build order: base color -> noise mask -> threshold -> colored edge band -> optional discard/alpha handling.",
      "Common bug: alpha or discard logic hides the whole mesh too early.",
    ],
  },
  ripple: {
    title: "Boilerplate: ripple",
    items: [
      "Recommended shape: fragment-only for full-screen, vertex + fragment for material-space ripple surfaces.",
      "Uniforms: uTime, uResolution or explicit center/radius controls.",
      "Varyings: vUv for material-space ripple effects.",
      "Build order: radial distance -> sine wave -> ring mask -> color blend.",
      "Common bug: missing aspect-ratio correction makes circles become ellipses.",
    ],
  },
  scanline: {
    title: "Boilerplate: scanline",
    items: [
      "Recommended shape: fragment overlay.",
      "Uniforms: uTime, lineDensity, strength.",
      "Varyings: none for screen-space; vUv for material-space overlays.",
      "Build order: base color -> stripe mask -> animate -> blend lightly.",
      "Common bug: overlay strength is too high and crushes the base image.",
    ],
  },
  "vertex-wobble": {
    title: "Boilerplate: vertex-wobble",
    items: [
      "Recommended shape: vertex + fragment shader.",
      "Uniforms: uTime, amplitude, frequency.",
      "Varyings: optional vUv; keep fragment simple until deformation is correct.",
      "Build order: one-axis displacement -> multi-axis modulation -> fragment styling.",
      "Common bug: debugging color and displacement at the same time hides the real fault.",
    ],
  },
};

const snippets = {
  fresnel: {
    title: "Snippet: fresnel",
    items: [
      "File: assets/snippets/fresnel.md",
      "Use for rim light, shield glow, hologram edge emphasis.",
      "Needs: view direction and normal in the same space.",
      "Typical pairing: material fragment shader with vNormal and viewDir.",
    ],
  },
  dissolve: {
    title: "Snippet: dissolve",
    items: [
      "File: assets/snippets/dissolve.md",
      "Use for dissolve, burn-away, transition threshold masks.",
      "Needs: a noise value plus progress and edge width.",
      "Typical pairing: fragment shader with vUv and a noise function or texture.",
    ],
  },
  ripple: {
    title: "Snippet: ripple",
    items: [
      "File: assets/snippets/ripple.md",
      "Use for radial wave, pulse ring, click feedback, sci-fi HUD.",
      "Needs: UV and time; aspect-ratio correction may still be required.",
      "Typical pairing: full-screen fragment shader or plane material fragment shader.",
    ],
  },
  scanline: {
    title: "Snippet: scanline",
    items: [
      "File: assets/snippets/scanline.md",
      "Use for CRT lines, HUD overlays, monitor effects.",
      "Needs: screen-space coordinates or gl_FragCoord plus time.",
      "Typical pairing: post-process pass or fragment overlay.",
    ],
  },
  pixelate: {
    title: "Snippet: pixelate",
    items: [
      "File: assets/snippets/pixelate.md",
      "Use for mosaic, retro rendering, censorship, transition blocks.",
      "Needs: UV plus a texture sampler or other sampled source.",
      "Typical pairing: texture fragment shader or post-process pass.",
    ],
  },
  "vertex-wobble": {
    title: "Snippet: vertex-wobble",
    items: [
      "File: assets/snippets/vertex-wobble.md",
      "Use for soft deformation, water-ish planes, flags, breathing surfaces.",
      "Needs: position plus uTime, amplitude, and frequency controls.",
      "Typical pairing: vertex shader before projection.",
    ],
  },
};

function buildDemoPlan(target, effect) {
  const normalizedTarget = String(target || "").toLowerCase();
  const normalizedEffect = String(effect || "").toLowerCase();

  const isScreenEffect = ["ripple", "scanline", "pixelate", "noise", "fbm", "gradient"].includes(
    normalizedEffect,
  );
  const isMaterialEffect = ["fresnel", "dissolve", "vertex-wobble"].includes(normalizedEffect);

  let file = "assets/webgl-fullscreen-demo/index.html";
  let why = "Good default for browser-native fullscreen fragment shader work.";

  if (normalizedTarget === "three" || normalizedTarget === "threejs") {
    file = "assets/threejs-material-demo/index.html";
    why = "Best fit for Three.js ShaderMaterial and mesh-bound effects.";
  } else if (normalizedTarget === "r3f" || normalizedTarget === "react-three-fiber") {
    file = "assets/r3f-demo/App.jsx";
    why = "Best fit for React Three Fiber projects that already use JSX and useFrame.";
  } else if (normalizedTarget === "postprocess" || normalizedTarget === "screen") {
    file = "assets/postprocess-demo/index.html";
    why = "Best fit for full-screen screen-space effects and post-style passes.";
  } else if (isScreenEffect) {
    file = "assets/postprocess-demo/index.html";
    why = "The requested effect reads like a screen-space effect, so a postprocess-style template is the fastest start.";
  } else if (isMaterialEffect) {
    file =
      normalizedTarget === "webgl"
        ? "assets/threejs-material-demo/index.html"
        : "assets/threejs-material-demo/index.html";
    why = "The requested effect reads like a mesh/material effect, so the material demo is the closest bundled fit.";
  }

  return {
    title: `Demo plan: ${target} + ${effect}`,
    items: [
      `Start from: ${file}`,
      `Why: ${why}`,
      "First step: make the bundled demo run unchanged before swapping shader logic.",
      "Second step: replace only the fragment or vertex section that matches the effect.",
      "Third step: add uniforms one at a time and keep a visible fallback color while integrating.",
    ],
  };
}

function snippetPathForEffect(effect) {
  const normalizedEffect = String(effect || "").toLowerCase();
  if (snippets[normalizedEffect]) {
    return snippets[normalizedEffect].items[0].replace("File: ", "");
  }
  return "No direct bundled snippet; start from the closest boilerplate.";
}

function boilerplateKeyForEffect(effect) {
  const normalizedEffect = String(effect || "").toLowerCase();
  if (boilerplates[normalizedEffect]) {
    return normalizedEffect;
  }
  if (normalizedEffect === "pixelate") {
    return "scanline";
  }
  return "ripple";
}

function buildScaffoldPlan(target, effect) {
  const demo = buildDemoPlan(target, effect);
  const boilerplateKey = boilerplateKeyForEffect(effect);
  const boilerplate = boilerplates[boilerplateKey];
  const snippetFile = snippetPathForEffect(effect);

  return {
    title: `Scaffold: ${target} + ${effect}`,
    items: [
      demo.items[0],
      `Closest boilerplate: ${boilerplateKey}`,
      `Closest snippet: ${snippetFile}`,
      "Start by running the demo unchanged and confirm the render path works.",
      "Then splice in the snippet or follow the boilerplate build order, one term at a time.",
      "Keep a visible fallback color until the effect renders correctly end-to-end.",
    ],
  };
}

const debugChecklists = {
  "black-screen": [
    "Replace shader body with a constant visible color like pure magenta.",
    "Verify the mesh or full-screen quad is actually being drawn.",
    "Check that required uniforms exist and are updated every frame.",
    "Reduce math until only UV mapping remains; then re-add features one by one.",
    "Look for divide-by-zero, normalize(vec3(0.0)), invalid texture reads, or discarded fragments.",
    "Confirm the host runtime expects the same GLSL version and output convention.",
  ],
  compile: [
    "Read the first compile error line carefully; later lines are often cascade failures.",
    "Check missing semicolons, precision qualifiers, and mismatched vector sizes.",
    "Verify varyings/in-out names match between vertex and fragment stages.",
    "Check that built-ins and texture functions match the GLSL version in use.",
    "Remove custom helper functions until the file compiles, then add them back incrementally.",
  ],
  uniform: [
    "Confirm each uniform is declared in GLSL and also passed from the host code.",
    "Check naming matches exactly, including case.",
    "Verify time and resolution values are non-zero and updated when expected.",
    "For textures, ensure the sampler uniform points to a bound texture.",
    "Temporarily output uniform-driven debug colors to prove the data path is alive.",
  ],
  varyings: [
    "Make vertex shader output a simple varying like UV or normal visualization.",
    "Confirm names and types match exactly across stages.",
    "Check that geometry actually contains the expected attributes.",
    "If a value seems broken, write it directly to fragment color before doing more math.",
  ],
  uv: [
    "Render raw UVs as color to verify orientation and continuity.",
    "Check for flipped Y, tiled wrapping, or geometry without UV attributes.",
    "For screen shaders, derive UV from fragment coordinates and resolution explicitly.",
    "Clamp or inspect out-of-range UVs before sampling textures.",
  ],
};

function printUsage() {
  console.log(`Shader helper

Usage:
  node shader.js intake <request> [--json]
  node shader.js debug <black-screen|compile|uniform|varyings|uv> [--json]
  node shader.js effects [--json]
  node shader.js boilerplate <fresnel|dissolve|ripple|scanline|vertex-wobble> [--json]
  node shader.js snippet <fresnel|dissolve|ripple|scanline|pixelate|vertex-wobble> [--json]
  node shader.js demo <webgl|three|r3f|postprocess|screen> <effect> [--json]
  node shader.js scaffold <webgl|three|r3f|postprocess|screen> <effect> [--json]
`);
}

function asJson(args) {
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
  const runtime = lower.includes("shadertoy")
    ? "ShaderToy-style fragment shader"
    : lower.includes("r3f") || lower.includes("react three")
      ? "React Three Fiber"
      : lower.includes("three")
        ? "Three.js ShaderMaterial"
        : lower.includes("webgl")
          ? "raw WebGL / GLSL ES"
          : "unknown: ask user or default to Three.js / browser GLSL";

  const shape =
    lower.includes("vertex") || lower.includes("deform") || lower.includes("displace")
      ? "vertex + fragment"
      : "fragment-first";

  const items = [
    `Runtime: ${runtime}`,
    `Stage shape: ${shape}`,
    "Confirm required uniforms: uTime, uResolution, uMouse, uTexture as needed.",
    "Decide whether the effect is screen-space, material-space, or post-processing.",
    "Start with a visible baseline color or UV gradient before adding complexity.",
    "If porting existing code, map all source-specific built-ins to host uniforms and varyings.",
  ];

  return {
    title: `Shader intake for: ${request}`,
    items,
  };
}

const args = process.argv.slice(2);
const command = args[0];
const json = asJson(args);

if (!command || command === "-h" || command === "--help" || command === "help") {
  printUsage();
  process.exit(0);
}

if (command === "effects") {
  output(effectStarters, json);
  process.exit(0);
}

if (command === "boilerplate") {
  const kind = args[1];
  const plan = boilerplates[kind];
  if (!plan) {
    console.error("Unknown boilerplate type.");
    process.exit(1);
  }
  output(plan, json);
  process.exit(0);
}

if (command === "snippet") {
  const kind = args[1];
  const snippet = snippets[kind];
  if (!snippet) {
    console.error("Unknown snippet type.");
    process.exit(1);
  }
  output(snippet, json);
  process.exit(0);
}

if (command === "demo") {
  const target = args[1];
  const effect = args[2];
  if (!target || !effect) {
    console.error("Please provide both a target and an effect.");
    process.exit(1);
  }
  output(buildDemoPlan(target, effect), json);
  process.exit(0);
}

if (command === "scaffold") {
  const target = args[1];
  const effect = args[2];
  if (!target || !effect) {
    console.error("Please provide both a target and an effect.");
    process.exit(1);
  }
  output(buildScaffoldPlan(target, effect), json);
  process.exit(0);
}

if (command === "debug") {
  const kind = args[1];
  const checklist = debugChecklists[kind];
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
    console.error("Please provide a shader request.");
    process.exit(1);
  }
  output(buildIntake(request), json);
  process.exit(0);
}

console.error("Unknown command.");
process.exit(1);
