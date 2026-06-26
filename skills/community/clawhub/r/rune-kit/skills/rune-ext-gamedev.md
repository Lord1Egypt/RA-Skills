# rune-ext-gamedev

> Rune L4 Skill | extension


# @rune/gamedev

> **RUNE COMPLIANCE**: Before ANY code response, you MUST:
> 1. Classify this request (CODE_CHANGE | QUESTION | DEBUG | REVIEW | EXPLORE)
> 2. Route through the correct Rune skill (see skill-router routing table)
> 3. Follow the skill's workflow — do NOT freelance or skip steps
> Violation: writing code without skill routing = incorrect behavior.

## Platform Constraints

- SHOULD: Monitor your context usage. If working on a long task, summarize progress before context fills up.
- MUST: Before summarizing/compacting context, save important decisions and progress to project files.
- SHOULD: Before ending, save architectural decisions and progress to .rune/ directory for future sessions.

## Purpose

Web game development hits performance walls that traditional web apps never encounter: 60fps render loops that stutter on garbage collection, physics simulations that diverge between clients, shaders that work on desktop but fail on mobile GPUs, and asset loading that blocks the first frame for 10 seconds. This pack provides patterns for the full web game stack — rendering, simulation, physics, assets, multiplayer, audio, input, ECS, particles, camera, and scene management — each optimized for the unique constraints of real-time interactive applications running in a browser.

## Triggers

- Auto-trigger: when `three`, `@react-three/fiber`, `pixi.js`, `phaser`, `cannon`, `rapier`, `*.glsl`, `*.wgsl` detected
- `/rune threejs-patterns` — audit or optimize Three.js scene
- `/rune webgl` — raw WebGL/shader development
- `/rune game-loops` — implement or audit game loop architecture
- `/rune physics-engine` — set up or optimize physics simulation
- `/rune asset-pipeline` — optimize asset loading and management
- `/rune multiplayer` — WebSocket game server and client prediction
- `/rune audio-system` — Web Audio API, spatial audio, SFX management
- `/rune input-system` — keyboard/mouse/gamepad/touch input handling
- `/rune ecs` — Entity Component System architecture
- `/rune particles` — GPU particle system with WebGL
- `/rune camera-system` — follow camera, screen shake, zoom
- `/rune scene-management` — scene transitions, preloading, serialization
- Called by `cook` (L1) when game development task detected

## Skills Included

| Skill | Model | Description |
|-------|-------|-------------|
| [threejs-patterns](skills/threejs-patterns.md) | sonnet | Three.js scene, React Three Fiber, PBR materials, LOD, post-processing, instanced rendering, and disposal patterns. |
| [webgl](skills/webgl.md) | sonnet | Raw WebGL2, GLSL shaders, VAO buffer management, instanced rendering, and texture handling. |
| [game-loops](skills/game-loops.md) | sonnet | Fixed timestep with accumulator, interpolation for smooth rendering, decoupled input handler, and frame budget monitoring. |
| [physics-engine](skills/physics-engine.md) | sonnet | Rapier.js (WASM) setup with collision groups, sleep thresholds, event-driven collision callbacks, and raycasting. |
| [asset-pipeline](skills/asset-pipeline.md) | sonnet | glTF/Draco loading, KTX2 texture compression, typed asset manifest, preloader with progress tracking. |
| [multiplayer](skills/multiplayer.md) | sonnet | Authoritative WebSocket game server, client-side prediction, reconciliation, entity interpolation, and lag compensation. |
| [audio-system](skills/audio-system.md) | sonnet | Web Audio API AudioManager — spatial audio, music crossfade, SFX pooling, browser autoplay policy handling. |
| [input-system](skills/input-system.md) | sonnet | Unified keyboard/mouse/gamepad/touch input with action mapping, input buffering, coyote time, and virtual joystick. |
| [ecs](skills/ecs.md) | sonnet | Lightweight archetype-based ECS — dense component storage, query-based entity iteration, and pure system functions. |
| [particles](skills/particles.md) | sonnet | Object-pooled CPU particle system with WebGL instancing path for 10k+ particles and emitter presets. |
| [camera-system](skills/camera-system.md) | sonnet | 2D camera with smooth lerp follow, dead zone, screen shake decay, and zoom-to target. |
| [scene-management](skills/scene-management.md) | sonnet | Stack-based SceneManager with fade transitions, asset preloading before enter, and level JSON serialization. |

## Common Workflows

| Workflow | Skills Involved | Typical Trigger |
|----------|----------------|----------------|
| 2D platformer bootstrap | game-loops → physics-engine → input-system → camera-system | new Phaser/PixiJS project |
| 3D world with NPCs | threejs-patterns → ecs → physics-engine → camera-system | Three.js/R3F project |
| Multiplayer action game | game-loops → multiplayer → physics-engine → input-system | real-time PvP feature |
| Mobile game port | asset-pipeline → input-system → camera-system → game-loops | add touch controls |
| VFX & atmosphere | particles → webgl → threejs-patterns → audio-system | visual polish sprint |
| Game level editor | scene-management → asset-pipeline → ecs → camera-system | tooling sprint |
| Performance audit | game-loops → webgl → particles → asset-pipeline | frame rate complaints |

## Cross-Pack Connections

| Target Pack | Connection | Use Case |
|-------------|-----------|----------|
| **@rune/ui** | HUD components, inventory screens, pause menus, leaderboard overlays | Health bars, minimap, skill cooldowns, settings modal |
| **@rune/backend** | REST/WebSocket API for leaderboards, save data, player accounts, matchmaking | POST `/scores`, GET `/leaderboard`, save game state to DB |
| **@rune/analytics** | Player telemetry — session length, death locations, skill usage heatmaps | `analytics.track('player_died', { x, y, cause })` |
| **@rune/ai-ml** | NPC behavior trees, pathfinding ML, procedural content, cheat detection | A* pathfinding, trained NPC models, PCG level generation |

## Connections

```
Calls → perf (L2): frame budget and rendering performance audit
Calls → asset-creator (L3): generate placeholder assets and sprites
Calls → @rune/ui: HUD, inventory, menus, overlays
Calls → @rune/backend: leaderboards, save data, player accounts, matchmaking
Calls → @rune/analytics: player telemetry and session tracking
Calls → @rune/ai-ml: NPC behavior, procedural content, cheat detection
Called By ← cook (L1): when game development task detected
Called By ← review (L2): when game code under review
```

## Tech Stack Support

| Engine | Rendering | Physics | ECS |
|--------|-----------|---------|-----|
| Three.js | WebGL2 / WebGPU | Rapier.js (WASM) | bitECS |
| React Three Fiber | Three.js (declarative) | @react-three/rapier | Custom |
| PixiJS | WebGL2 (2D) | Matter.js | Custom |
| Phaser 3 | WebGL / Canvas | Arcade / Matter | Built-in |
| Babylon.js | WebGL2 / WebGPU | Havok (WASM) | Built-in |

## Constraints

1. MUST use fixed timestep for physics — variable timestep causes non-deterministic simulation.
2. MUST dispose all GPU resources (geometries, textures, materials) on scene teardown — GPU memory leaks crash tabs.
3. MUST NOT create objects inside the render loop — allocate outside, reuse inside.
4. MUST test on target minimum hardware (mobile GPU) not just development machine.
5. MUST use compressed asset formats (Draco for geometry, KTX2/Basis for textures) — raw assets cause unacceptable load times.
6. MUST use authoritative server model for multiplayer — never trust client position data.
7. MUST resume AudioContext on user gesture — browsers block autoplay audio.
8. MUST call `input.flush()` at end of each fixed tick — prevents justPressed persisting across frames.

## Sharp Edges

| Failure Mode | Severity | Mitigation |
|---|---|---|
| Objects created in useFrame/render loop cause GC stutters at 60fps | CRITICAL | Pre-allocate all vectors, quaternions, matrices outside the loop; reuse with `.set()` |
| GPU memory leak from undisposed textures/geometries (tab crashes after 5 minutes) | CRITICAL | Implement disposal manager; call `.dispose()` on every Three.js resource on unmount |
| Physics spiral of death: update takes longer than frame, accumulator grows unbounded | HIGH | Cap accumulator at 250ms (skip frames); reduce physics complexity if consistent |
| Shader compiles on first use causing frame drop (shader cache miss) | MEDIUM | Pre-warm shaders during loading screen; use `renderer.compile(scene, camera)` |
| Asset loading blocks first frame (white screen for 5+ seconds) | HIGH | Implement progressive loading with preloader UI; prioritize visible assets |
| Mobile GPU fails on desktop-quality shaders (WebGL context lost) | HIGH | Detect GPU tier with `detect-gpu`; provide shader LOD variants |
| Multiplayer client trusts own position — speed hack trivial | CRITICAL | Server is authoritative; client sends inputs only, reconciles with server state |
| AudioContext locked until user gesture — no music on load | MEDIUM | Resume AudioContext in first click/keydown handler; show muted indicator |
| Gamepad axes not zeroed when gamepad disconnects | LOW | Set axes to 0 in gamepaddisconnected handler |
| Input justPressed persists to next frame if flush() skipped | HIGH | Always flush at end of fixed update, not render |

## Done When

- Scene renders at stable 60fps on target hardware
- Physics simulation is deterministic with fixed timestep
- All GPU resources properly disposed on cleanup
- Assets compressed and preloaded with progress indicator
- Game loop decouples update from render with interpolation
- Multiplayer: server authoritative, client predicts + reconciles
- Audio: spatial SFX + crossfade music, resumable after user gesture
- Input: keyboard/mouse/gamepad/touch unified, buffered, rebindable
- ECS: entities/components/systems cleanly separated, query-based
- Particles: pooled, no GC spikes, emitter presets for common FX
- Camera: smooth follow, dead zone, screen shake on impact
- Scenes: transition with fade, preload assets before enter
- Performance: quadtree spatial queries, frame budget monitoring active
- Structured report emitted for each skill invoked

## Cost Profile

~10,000–20,000 tokens per full pack run (all skills). Individual skill: ~2,000–4,000 tokens. Sonnet default. Use haiku for asset detection scans and grep passes; sonnet for physics config, shader optimization, and multiplayer architecture; escalate to opus for full game architecture decisions spanning multiple systems.

# asset-pipeline

Game asset pipeline — glTF loading, texture compression, audio management, asset manifest, preloading.

#### Workflow

**Step 1 — Detect asset strategy**
Use Glob to find asset files: `*.gltf`, `*.glb`, `*.ktx2`, `*.basis`, `*.png` in `assets/` or `public/`. Use Grep to find loaders: `GLTFLoader`, `TextureLoader`, `KTX2Loader`, `Howler`, `Audio`. Read the loading code to understand: preloading strategy, compression, and caching.

**Step 2 — Audit asset efficiency**
Check for: uncompressed textures (PNG/JPG instead of KTX2/Basis), glTF without Draco compression, no asset manifest (scattered inline paths), missing preloader (assets load mid-gameplay causing stutters), audio files in WAV format (use OGG/MP3), and no LOD variants for 3D models.

**Step 3 — Emit asset pipeline**
Emit: asset manifest with typed entries, preloader with progress tracking, glTF loader with Draco decoder, KTX2 texture loader, and audio manager with Howler.js.

#### Example

```typescript
// Asset manifest + preloader with progress tracking
interface AssetManifest {
  models: Record<string, { url: string; draco?: boolean }>;
  textures: Record<string, { url: string; format: 'ktx2' | 'png' }>;
  audio: Record<string, { url: string; volume?: number; loop?: boolean }>;
}

const MANIFEST: AssetManifest = {
  models: {
    player: { url: '/assets/player.glb', draco: true },
    level1: { url: '/assets/level1.glb', draco: true },
  },
  textures: {
    terrain: { url: '/assets/terrain.ktx2', format: 'ktx2' },
  },
  audio: {
    bgm: { url: '/assets/bgm.ogg', volume: 0.5, loop: true },
    jump: { url: '/assets/jump.ogg', volume: 0.8 },
  },
};

class AssetLoader {
  private loaded = 0;
  private total = 0;
  private cache = new Map<string, unknown>();

  async loadAll(manifest: AssetManifest, onProgress: (pct: number) => void) {
    const entries = [
      ...Object.entries(manifest.models).map(([k, v]) => ({ key: k, ...v, type: 'model' })),
      ...Object.entries(manifest.textures).map(([k, v]) => ({ key: k, ...v, type: 'texture' })),
      ...Object.entries(manifest.audio).map(([k, v]) => ({ key: k, ...v, type: 'audio' })),
    ];
    this.total = entries.length;

    await Promise.all(entries.map(async (entry) => {
      await fetch(entry.url); // preload into browser cache
      this.loaded++;
      onProgress(this.loaded / this.total);
    }));
  }

  get<T>(key: string): T {
    const asset = this.cache.get(key);
    if (!asset) throw new Error(`Asset not loaded: ${key}`);
    return asset as T;
  }
}
```

---

# audio-system

Web Audio API, spatial audio, SFX management — AudioManager with spatial audio, music crossfade, and SFX pooling.

#### Workflow

**Step 1 — Detect audio setup**
Use Grep to find audio code: `AudioContext`, `Howler`, `Audio`, `createBufferSource`, `createGain`. Read the audio initialization to understand: context management, volume controls, and loading strategy.

**Step 2 — Audit audio configuration**
Check for: AudioContext not resumed on user gesture (browser autoplay policy), SFX creating new nodes on every play (memory pressure), no volume normalization (clipping), missing cleanup on scene exit.

**Step 3 — Emit AudioManager**
Emit: AudioManager class with master/music/sfx gain chain, music crossfade, spatial (3D) audio via PannerNode, and SFX pooling.

#### Web Audio API — Full Audio Manager

```typescript
// AudioManager — spatial audio, music crossfade, SFX pooling
class AudioManager {
  private ctx: AudioContext;
  private masterGain: GainNode;
  private musicGain: GainNode;
  private sfxGain: GainNode;
  private buffers = new Map<string, AudioBuffer>();
  private sfxPool = new Map<string, AudioBufferSourceNode[]>();
  private currentMusic: AudioBufferSourceNode | null = null;

  constructor() {
    this.ctx = new AudioContext();
    this.masterGain = this.ctx.createGain();
    this.musicGain = this.ctx.createGain();
    this.sfxGain = this.ctx.createGain();

    this.musicGain.connect(this.masterGain);
    this.sfxGain.connect(this.masterGain);
    this.masterGain.connect(this.ctx.destination);

    this.musicGain.gain.value = 0.6;
    this.sfxGain.gain.value = 1.0;
  }

  async load(id: string, url: string) {
    const response = await fetch(url);
    const arrayBuffer = await response.arrayBuffer();
    this.buffers.set(id, await this.ctx.decodeAudioData(arrayBuffer));
  }

  playSfx(id: string, options: { volume?: number; detune?: number } = {}) {
    const buffer = this.buffers.get(id);
    if (!buffer) return;

    // Resume context if suspended (browser autoplay policy)
    if (this.ctx.state === 'suspended') this.ctx.resume();

    const source = this.ctx.createBufferSource();
    const gain = this.ctx.createGain();
    source.buffer = buffer;
    source.detune.value = options.detune ?? 0;
    gain.gain.value = options.volume ?? 1;

    source.connect(gain).connect(this.sfxGain);
    source.start();
  }

  // Music crossfade — smooth transition between tracks
  async crossfadeTo(id: string, fadeDuration = 2) {
    const buffer = this.buffers.get(id);
    if (!buffer) return;
    if (this.ctx.state === 'suspended') await this.ctx.resume();

    const newSource = this.ctx.createBufferSource();
    newSource.buffer = buffer;
    newSource.loop = true;

    const newGain = this.ctx.createGain();
    newGain.gain.setValueAtTime(0, this.ctx.currentTime);
    newGain.gain.linearRampToValueAtTime(1, this.ctx.currentTime + fadeDuration);

    newSource.connect(newGain).connect(this.musicGain);
    newSource.start();

    if (this.currentMusic) {
      const oldGain = this.ctx.createGain();
      oldGain.gain.setValueAtTime(1, this.ctx.currentTime);
      oldGain.gain.linearRampToValueAtTime(0, this.ctx.currentTime + fadeDuration);
      this.currentMusic.connect(oldGain).connect(this.musicGain);
      const old = this.currentMusic;
      setTimeout(() => old.stop(), fadeDuration * 1000);
    }

    this.currentMusic = newSource;
  }

  // Spatial (3D) audio — attenuate by distance from listener
  playSpatial(id: string, x: number, y: number, z: number) {
    const buffer = this.buffers.get(id);
    if (!buffer) return;

    const source = this.ctx.createBufferSource();
    const panner = this.ctx.createPanner();
    source.buffer = buffer;

    panner.panningModel = 'HRTF';
    panner.distanceModel = 'inverse';
    panner.refDistance = 1;
    panner.maxDistance = 100;
    panner.rolloffFactor = 1;
    panner.positionX.value = x;
    panner.positionY.value = y;
    panner.positionZ.value = z;

    source.connect(panner).connect(this.sfxGain);
    source.start();
  }

  setMasterVolume(v: number) { this.masterGain.gain.value = Math.max(0, Math.min(1, v)); }
  setMusicVolume(v: number) { this.musicGain.gain.value = Math.max(0, Math.min(1, v)); }
  setSfxVolume(v: number) { this.sfxGain.gain.value = Math.max(0, Math.min(1, v)); }
}
```

---

# camera-system

Follow camera, screen shake, zoom — 2D camera with smooth lerp follow, dead zone, screen shake on impact, and zoom-to target.

#### Workflow

**Step 1 — Detect camera usage**
Use Grep to find camera code: `Camera`, `follow`, `viewport`, `ctx.translate`, `ctx.setTransform`. Read to understand: follow strategy, any existing shake/zoom, and how transform is applied to canvas.

**Step 2 — Audit camera configuration**
Check for: camera snapping to target each frame (no lerp = no smoothness), no dead zone (camera moves even for tiny player motion), screen shake with random offset not decaying.

**Step 3 — Emit Camera2D**
Emit: Camera2D with smooth lerp, configurable dead zone, screen shake with intensity decay, zoom-to target, and `applyToContext` helper.

#### Smooth Follow, Screen Shake, Dead Zone

```typescript
// 2D camera system — smooth follow, screen shake, zoom, dead zone
class Camera2D {
  x = 0; y = 0;
  zoom = 1;
  private targetX = 0; private targetY = 0;
  private shakeIntensity = 0; private shakeDuration = 0;
  lerpSpeed = 5;

  // Dead zone — camera only moves when target leaves this box
  private deadZone = { w: 80, h: 60 };

  follow(targetX: number, targetY: number, dt: number) {
    const dx = targetX - this.targetX;
    const dy = targetY - this.targetY;

    // Only move camera when target exits dead zone
    if (Math.abs(dx) > this.deadZone.w / 2) this.targetX += dx - Math.sign(dx) * this.deadZone.w / 2;
    if (Math.abs(dy) > this.deadZone.h / 2) this.targetY += dy - Math.sign(dy) * this.deadZone.h / 2;

    // Smooth lerp
    this.x += (this.targetX - this.x) * this.lerpSpeed * dt;
    this.y += (this.targetY - this.y) * this.lerpSpeed * dt;
  }

  shake(intensity: number, duration: number) {
    this.shakeIntensity = intensity;
    this.shakeDuration = duration;
  }

  zoomTo(target: number, dt: number, speed = 3) {
    this.zoom += (target - this.zoom) * speed * dt;
  }

  update(dt: number): { x: number; y: number; zoom: number } {
    let sx = 0; let sy = 0;
    if (this.shakeDuration > 0) {
      this.shakeDuration -= dt;
      const t = Math.max(0, this.shakeDuration);
      sx = (Math.random() * 2 - 1) * this.shakeIntensity * t;
      sy = (Math.random() * 2 - 1) * this.shakeIntensity * t;
    }
    return { x: this.x + sx, y: this.y + sy, zoom: this.zoom };
  }

  // Apply to Canvas 2D context
  applyToContext(ctx: CanvasRenderingContext2D, screenW: number, screenH: number) {
    const { x, y, zoom } = this.update(1 / 60);
    ctx.setTransform(zoom, 0, 0, zoom, screenW / 2 - x * zoom, screenH / 2 - y * zoom);
  }
}

// Usage
const camera = new Camera2D();
camera.lerpSpeed = 8;

// In game loop render:
// camera.follow(player.x, player.y, dt);
// camera.applyToContext(ctx, canvas.width, canvas.height);
// ... draw scene ...
// ctx.setTransform(1, 0, 0, 1, 0, 0); // reset for HUD
```

---

# ecs

Entity Component System architecture — archetype-based ECS with dense array storage for cache efficiency, pure system functions, and query-based entity iteration.

#### Workflow

**Step 1 — Detect ECS usage**
Use Grep to find ECS patterns: `Entity`, `Component`, `System`, `World`, `bitECS`, `createWorld`. Read entity management code to understand: component storage, system execution order, and query patterns.

**Step 2 — Audit ECS architecture**
Check for: logic mixed into components (components should be pure data), O(n²) entity iteration without spatial partitioning, components stored as objects (prefer flat arrays for cache efficiency), and missing entity cleanup on destroy.

**Step 3 — Emit ECS scaffold**
Emit: World class with entity registry + component storage, query-based entity iteration, pure system functions, and proper cleanup.

#### Lightweight ECS — Archetype-Based

```typescript
// Minimal ECS — dense array storage per archetype for cache efficiency
type EntityId = number;
type ComponentType<T> = { new(...args: unknown[]): T; readonly typeName: string; };

// Components are plain data, no logic
class Position { static typeName = 'Position'; constructor(public x = 0, public y = 0) {} }
class Velocity { static typeName = 'Velocity'; constructor(public vx = 0, public vy = 0) {} }
class Sprite   { static typeName = 'Sprite';   constructor(public textureId = '') {} }
class Health   { static typeName = 'Health';   constructor(public hp = 100, public max = 100) {} }

// World — entity registry + component storage
class World {
  private nextId = 1;
  private components = new Map<string, Map<EntityId, unknown>>();

  createEntity(): EntityId { return this.nextId++; }

  addComponent<T extends object>(entity: EntityId, component: T & { constructor: { typeName: string } }) {
    const name = component.constructor.typeName;
    if (!this.components.has(name)) this.components.set(name, new Map());
    this.components.get(name)!.set(entity, component);
  }

  getComponent<T>(entity: EntityId, type: ComponentType<T>): T | undefined {
    return this.components.get(type.typeName)?.get(entity) as T | undefined;
  }

  removeComponent<T>(entity: EntityId, type: ComponentType<T>) {
    this.components.get(type.typeName)?.delete(entity);
  }

  // Query — iterate entities that have ALL specified components
  query<T extends object[]>(...types: { [K in keyof T]: ComponentType<T[K]> }): EntityId[] {
    if (types.length === 0) return [];
    const [first, ...rest] = types;
    const candidates = Array.from(this.components.get(first.typeName)?.keys() ?? []);
    return candidates.filter(id => rest.every(t => this.components.get(t.typeName)?.has(id)));
  }

  destroyEntity(entity: EntityId) {
    this.components.forEach(store => store.delete(entity));
  }
}

// Systems — pure functions over component queries
const movementSystem = (world: World, dt: number) => {
  for (const id of world.query(Position, Velocity)) {
    const pos = world.getComponent(id, Position)!;
    const vel = world.getComponent(id, Velocity)!;
    pos.x += vel.vx * dt;
    pos.y += vel.vy * dt;
  }
};

const healthSystem = (world: World) => {
  for (const id of world.query(Health)) {
    const hp = world.getComponent(id, Health)!;
    if (hp.hp <= 0) world.destroyEntity(id);
  }
};

// Usage
const world = new World();
const player = world.createEntity();
world.addComponent(player, new Position(100, 100));
world.addComponent(player, new Velocity(0, 0));
world.addComponent(player, new Health(100, 100));

// In fixed update:
// movementSystem(world, dt);
// healthSystem(world);
```

---

# game-loops

Game loop architecture — fixed timestep, interpolation, input handling, state machines, ECS.

#### Workflow

**Step 1 — Detect game loop pattern**
Use Grep to find loop code: `requestAnimationFrame`, `setInterval.*16`, `update`, `fixedUpdate`, `deltaTime`, `gameLoop`. Read the main loop to understand: timestep strategy, update/render separation, and input handling.

**Step 2 — Audit loop correctness**
Check for: variable timestep physics (non-deterministic), no accumulator for fixed update (physics tied to framerate), input polled inside render (inconsistent), missing interpolation between fixed steps (visual stuttering), and no frame budget monitoring.

**Step 3 — Emit fixed timestep loop**
Emit: fixed timestep (60Hz) with accumulator, interpolation for smooth rendering, decoupled input handler, and frame budget monitoring.

#### Example

```typescript
// Fixed timestep game loop with interpolation
const TICK_RATE = 60;
const TICK_DURATION = 1000 / TICK_RATE;

class GameLoop {
  private accumulator = 0;
  private previousTime = 0;
  private running = false;

  constructor(
    private update: (dt: number) => void,     // fixed timestep logic
    private render: (alpha: number) => void,   // interpolated rendering
  ) {}

  start() {
    this.running = true;
    this.previousTime = performance.now();
    requestAnimationFrame(this.tick);
  }

  private tick = (currentTime: number) => {
    if (!this.running) return;
    const elapsed = Math.min(currentTime - this.previousTime, 250); // cap spiral of death
    this.previousTime = currentTime;
    this.accumulator += elapsed;

    while (this.accumulator >= TICK_DURATION) {
      this.update(TICK_DURATION / 1000); // dt in seconds
      this.accumulator -= TICK_DURATION;
    }

    const alpha = this.accumulator / TICK_DURATION; // interpolation factor [0, 1)
    this.render(alpha);
    requestAnimationFrame(this.tick);
  };

  stop() { this.running = false; }
}

// Usage
const loop = new GameLoop(
  (dt) => { world.step(dt); entities.forEach(e => e.update(dt)); },
  (alpha) => { renderer.render(scene, camera, alpha); },
);
loop.start();
```

---

# input-system

Keyboard/mouse/gamepad/touch input handling — unified InputManager with action mapping, input buffering, coyote time, and touch virtual joystick.

#### Workflow

**Step 1 — Detect input handling**
Use Grep to find input code: `addEventListener.*keydown`, `addEventListener.*gamepad`, `onMouseMove`, `ontouchstart`. Read input handlers to understand: action mapping strategy, polling vs event-driven, and platform support.

**Step 2 — Audit input correctness**
Check for: input polled inside render loop (should be in fixed update), no gamepad support, missing touch controls for mobile, hardcoded key bindings, and no input buffering (missed jump inputs).

**Step 3 — Emit InputManager**
Emit: unified InputManager with keyboard/mouse/gamepad/touch, action-based API, justPressed/wasReleased one-frame flags, and runtime rebinding. Always call `flush()` at end of each fixed tick.

#### Unified Input Handler — Keyboard, Mouse, Gamepad, Touch

```typescript
// InputManager — supports keyboard, mouse, gamepad, touch with action mapping
type ActionMap = Record<string, string[]>; // action → [key1, key2, ...]

const DEFAULT_ACTIONS: ActionMap = {
  moveUp:    ['KeyW', 'ArrowUp'],
  moveDown:  ['KeyS', 'ArrowDown'],
  moveLeft:  ['KeyA', 'ArrowLeft'],
  moveRight: ['KeyD', 'ArrowRight'],
  jump:      ['Space'],
  attack:    ['Mouse0'],
  pause:     ['Escape'],
};

class InputManager {
  private held = new Set<string>();
  private justPressed = new Set<string>();
  private justReleased = new Set<string>();
  private axes = { x: 0, y: 0 };
  private gamepad: Gamepad | null = null;
  private bindings: ActionMap;

  constructor(bindings = DEFAULT_ACTIONS) {
    this.bindings = { ...bindings };
    window.addEventListener('keydown', e => { this.held.add(e.code); this.justPressed.add(e.code); });
    window.addEventListener('keyup', e => { this.held.delete(e.code); this.justReleased.add(e.code); });
    window.addEventListener('mousedown', e => this.held.add(`Mouse${e.button}`));
    window.addEventListener('mouseup', e => this.held.delete(`Mouse${e.button}`));
    window.addEventListener('gamepaddisconnected', () => { this.gamepad = null; });
  }

  // Call at the START of each fixed update tick, not inside render
  pollGamepad() {
    const pads = navigator.getGamepads();
    this.gamepad = pads[0] ?? null;
    if (this.gamepad) {
      this.axes.x = this.gamepad.axes[0];
      this.axes.y = this.gamepad.axes[1];
    }
  }

  // Call at END of each fixed update tick to clear one-frame flags
  flush() {
    this.justPressed.clear();
    this.justReleased.clear();
  }

  isDown(action: string): boolean {
    return (this.bindings[action] ?? []).some(key => this.held.has(key));
  }

  wasPressed(action: string): boolean {
    return (this.bindings[action] ?? []).some(key => this.justPressed.has(key));
  }

  wasReleased(action: string): boolean {
    return (this.bindings[action] ?? []).some(key => this.justReleased.has(key));
  }

  getAxes() { return { ...this.axes }; }

  // Rebind at runtime (save to localStorage)
  rebind(action: string, keys: string[]) {
    this.bindings[action] = keys;
    localStorage.setItem('inputBindings', JSON.stringify(this.bindings));
  }

  loadSavedBindings() {
    const saved = localStorage.getItem('inputBindings');
    if (saved) this.bindings = { ...this.bindings, ...JSON.parse(saved) };
  }
}
```

#### Input Buffering (Coyote Time + Jump Buffering)

```typescript
// Input buffer — remember button press for N frames to forgive missed timing
class InputBuffer {
  private buffer: Map<string, number> = new Map(); // action → frames remaining

  bufferAction(action: string, frames = 6) { this.buffer.set(action, frames); }

  consume(action: string): boolean {
    if ((this.buffer.get(action) ?? 0) > 0) {
      this.buffer.set(action, 0);
      return true;
    }
    return false;
  }

  tick() {
    this.buffer.forEach((frames, action) => {
      if (frames > 0) this.buffer.set(action, frames - 1);
    });
  }
}

// Coyote time — allow jump for N frames after walking off a ledge
class CoyoteTime {
  private grounded = false;
  private coyoteFrames = 0;
  private readonly maxFrames = 6;

  update(isGrounded: boolean) {
    if (isGrounded) {
      this.grounded = true;
      this.coyoteFrames = this.maxFrames;
    } else {
      this.grounded = false;
      this.coyoteFrames = Math.max(0, this.coyoteFrames - 1);
    }
  }

  canJump(): boolean { return this.coyoteFrames > 0; }
}
```

#### Touch Virtual Joystick (Mobile)

```typescript
// Canvas-rendered virtual joystick for mobile
class VirtualJoystick {
  private origin: { x: number; y: number } | null = null;
  private current: { x: number; y: number } | null = null;
  private touchId: number | null = null;
  readonly radius = 60;

  constructor(private canvas: HTMLCanvasElement) {
    canvas.addEventListener('touchstart', this.onStart, { passive: false });
    canvas.addEventListener('touchmove', this.onMove, { passive: false });
    canvas.addEventListener('touchend', this.onEnd);
  }

  private onStart = (e: TouchEvent) => {
    e.preventDefault();
    if (this.touchId !== null) return;
    const t = e.changedTouches[0];
    this.touchId = t.identifier;
    this.origin = { x: t.clientX, y: t.clientY };
    this.current = { ...this.origin };
  };

  private onMove = (e: TouchEvent) => {
    e.preventDefault();
    const t = Array.from(e.changedTouches).find(t => t.identifier === this.touchId);
    if (!t || !this.origin) return;
    const dx = t.clientX - this.origin.x;
    const dy = t.clientY - this.origin.y;
    const len = Math.hypot(dx, dy);
    const clamped = Math.min(len, this.radius);
    const angle = Math.atan2(dy, dx);
    this.current = {
      x: this.origin.x + Math.cos(angle) * clamped,
      y: this.origin.y + Math.sin(angle) * clamped,
    };
  };

  private onEnd = (e: TouchEvent) => {
    if (Array.from(e.changedTouches).some(t => t.identifier === this.touchId)) {
      this.origin = this.current = null;
      this.touchId = null;
    }
  };

  getAxes(): { x: number; y: number } {
    if (!this.origin || !this.current) return { x: 0, y: 0 };
    return {
      x: (this.current.x - this.origin.x) / this.radius,
      y: (this.current.y - this.origin.y) / this.radius,
    };
  }
}
```

---

# multiplayer

WebSocket game server and client prediction — authoritative server model, client-side prediction, reconciliation, entity interpolation, and lag compensation.

Authoritative server model: server owns game state, clients send inputs only. Never trust client position.

#### Workflow

**Step 1 — Assess multiplayer architecture**
Use Grep to find existing WebSocket code: `WebSocket`, `socket.io`, `ws`, `onmessage`, `postMessage`. Determine: is there a server or is this client-only? What is the tick rate?

**Step 2 — Implement authoritative server**
Emit: Node.js WebSocket server with fixed-tick update (20Hz sufficient), input queue per player, server-side physics/movement, state broadcast.

**Step 3 — Implement client prediction**
Emit: local input application before server confirmation, pending input buffer, reconciliation on server update, smooth interpolation for remote entities.

**Step 4 — Add lag compensation**
Emit: snapshot buffer for entity interpolation (render ~100ms behind server), client prediction with rollback on desync.

#### WebSocket Game Server Pattern

```typescript
// Server (Node.js + ws) — authoritative game server
import { WebSocketServer, WebSocket } from 'ws';

interface PlayerInput { seq: number; keys: { up: boolean; down: boolean; left: boolean; right: boolean }; }
interface PlayerState { id: string; x: number; y: number; vx: number; vy: number; }

const wss = new WebSocketServer({ port: 3001 });
const players = new Map<string, PlayerState>();
const inputQueues = new Map<string, PlayerInput[]>();

wss.on('connection', (ws: WebSocket, req) => {
  const id = crypto.randomUUID();
  players.set(id, { id, x: 0, y: 0, vx: 0, vy: 0 });
  inputQueues.set(id, []);

  ws.send(JSON.stringify({ type: 'init', id, state: Object.fromEntries(players) }));
  broadcast({ type: 'player_joined', id });

  ws.on('message', (raw) => {
    const msg = JSON.parse(raw.toString());
    if (msg.type === 'input') {
      inputQueues.get(id)?.push(msg.input);
    }
  });

  ws.on('close', () => {
    players.delete(id);
    inputQueues.delete(id);
    broadcast({ type: 'player_left', id });
  });
});

// Fixed-tick server update (20Hz is sufficient for authoritative server)
const TICK_MS = 50;
setInterval(() => {
  inputQueues.forEach((queue, id) => {
    const player = players.get(id)!;
    const input = queue.shift(); // process one input per tick
    if (input) applyInput(player, input);
    integratePhysics(player);
  });

  broadcast({ type: 'state_update', tick: Date.now(), players: Object.fromEntries(players) });
}, TICK_MS);

function broadcast(msg: object) {
  const data = JSON.stringify(msg);
  wss.clients.forEach(c => c.readyState === WebSocket.OPEN && c.send(data));
}

function applyInput(p: PlayerState, input: PlayerInput) {
  const speed = 200;
  p.vx = (input.keys.right ? 1 : 0) - (input.keys.left ? 1 : 0);
  p.vy = (input.keys.down ? 1 : 0) - (input.keys.up ? 1 : 0);
  const len = Math.hypot(p.vx, p.vy);
  if (len > 0) { p.vx = (p.vx / len) * speed; p.vy = (p.vy / len) * speed; }
}

function integratePhysics(p: PlayerState) {
  p.x += p.vx * (TICK_MS / 1000);
  p.y += p.vy * (TICK_MS / 1000);
}
```

#### Client Prediction & Reconciliation

```typescript
// Client — predict locally, reconcile on server update
class NetworkedPlayer {
  private pendingInputs: { seq: number; input: PlayerInput; }[] = [];
  private seq = 0;
  localState: PlayerState;
  serverState: PlayerState;

  constructor(initial: PlayerState) {
    this.localState = { ...initial };
    this.serverState = { ...initial };
  }

  sendInput(keys: PlayerInput['keys'], ws: WebSocket) {
    const input: PlayerInput = { seq: ++this.seq, keys };
    this.pendingInputs.push({ seq: this.seq, input });
    ws.send(JSON.stringify({ type: 'input', input }));

    // Apply immediately (client prediction)
    applyInputToState(this.localState, keys);
  }

  reconcile(serverUpdate: PlayerState & { lastProcessedSeq: number }) {
    this.serverState = serverUpdate;

    // Remove acknowledged inputs
    this.pendingInputs = this.pendingInputs.filter(p => p.seq > serverUpdate.lastProcessedSeq);

    // Reapply unacknowledged inputs on top of server state
    this.localState = { ...serverUpdate };
    for (const { input } of this.pendingInputs) {
      applyInputToState(this.localState, input.keys);
    }
  }
}

function applyInputToState(state: PlayerState, keys: PlayerInput['keys']) {
  const dt = 1 / 60;
  const speed = 200;
  state.x += ((keys.right ? 1 : 0) - (keys.left ? 1 : 0)) * speed * dt;
  state.y += ((keys.down ? 1 : 0) - (keys.up ? 1 : 0)) * speed * dt;
}
```

#### Lag Compensation & Entity Interpolation

```typescript
// Interpolate remote entities between server snapshots (smooth movement, ~100ms behind)
interface Snapshot { tick: number; timestamp: number; entities: Map<string, PlayerState>; }

class EntityInterpolator {
  private buffer: Snapshot[] = [];
  private readonly delay = 100; // ms behind server

  addSnapshot(snapshot: Snapshot) {
    this.buffer.push(snapshot);
    // Keep only last 1 second of snapshots
    const cutoff = Date.now() - 1000;
    this.buffer = this.buffer.filter(s => s.timestamp > cutoff);
  }

  getInterpolatedState(entityId: string): PlayerState | null {
    const renderTime = Date.now() - this.delay;

    // Find the two snapshots bracketing renderTime
    const newer = this.buffer.find(s => s.timestamp >= renderTime);
    const older = this.buffer.slice().reverse().find(s => s.timestamp < renderTime);

    if (!older || !newer) return newer?.entities.get(entityId) ?? null;

    const t = (renderTime - older.timestamp) / (newer.timestamp - older.timestamp);
    const a = older.entities.get(entityId);
    const b = newer.entities.get(entityId);
    if (!a || !b) return null;

    return {
      ...a,
      x: a.x + (b.x - a.x) * t,
      y: a.y + (b.y - a.y) * t,
    };
  }
}
```

---

# particles

GPU particle system with WebGL instancing — object-pooled particles, emission presets, and performance-safe rendering for 10k+ particles.

#### Workflow

**Step 1 — Detect particle usage**
Use Grep to find particle code: `particles`, `emitter`, `ParticleSystem`, `createBufferSource`. Understand current implementation: CPU vs GPU, pooling strategy, and draw call count.

**Step 2 — Audit particle performance**
Check for: new particle objects created on emit (GC pressure), no object pool, drawing each particle as a separate draw call, no life/alpha fade.

**Step 3 — Emit particle system**
Emit: ParticleSystem with pre-allocated pool, update/render separation, emitter presets for common effects (explosion, sparks, smoke).

#### GPU Particles with WebGL Instancing

```typescript
// GPU particle system — update on CPU, render 10k+ particles via instancing
interface Particle {
  x: number; y: number;
  vx: number; vy: number;
  life: number; maxLife: number;
  size: number;
  r: number; g: number; b: number; a: number;
}

class ParticleSystem {
  private particles: Particle[] = [];
  private pool: Particle[] = [];
  private readonly maxParticles: number;

  constructor(maxParticles = 5000) {
    this.maxParticles = maxParticles;
    // Pre-allocate pool
    for (let i = 0; i < maxParticles; i++) {
      this.pool.push({ x:0,y:0,vx:0,vy:0,life:0,maxLife:1,size:4,r:1,g:1,b:1,a:1 });
    }
  }

  emit(x: number, y: number, count: number, config: Partial<Particle> = {}) {
    for (let i = 0; i < count && this.particles.length < this.maxParticles; i++) {
      const p = this.pool.pop() ?? { x:0,y:0,vx:0,vy:0,life:0,maxLife:1,size:4,r:1,g:1,b:1,a:1 };
      const angle = Math.random() * Math.PI * 2;
      const speed = 50 + Math.random() * 150;
      Object.assign(p, {
        x, y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        life: 1, maxLife: 0.5 + Math.random() * 1.5,
        size: 3 + Math.random() * 5,
        r: 1, g: 0.5, b: 0.1, a: 1,
        ...config,
      });
      this.particles.push(p);
    }
  }

  update(dt: number) {
    const gravity = 200;
    for (let i = this.particles.length - 1; i >= 0; i--) {
      const p = this.particles[i];
      p.x += p.vx * dt;
      p.y += p.vy * dt;
      p.vy += gravity * dt;
      p.life -= dt / p.maxLife;
      p.a = Math.max(0, p.life);
      if (p.life <= 0) {
        this.pool.push(p);
        this.particles.splice(i, 1);
      }
    }
  }

  // Render with Canvas 2D (swap with WebGL instancing for >10k particles)
  render(ctx: CanvasRenderingContext2D) {
    for (const p of this.particles) {
      ctx.globalAlpha = p.a;
      ctx.fillStyle = `rgb(${p.r * 255 | 0},${p.g * 255 | 0},${p.b * 255 | 0})`;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size * p.life, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.globalAlpha = 1;
  }
}

// Emitter presets
const EMITTER_PRESETS = {
  explosion: (x: number, y: number, sys: ParticleSystem) =>
    sys.emit(x, y, 80, { r: 1, g: 0.4, b: 0 }),
  sparks: (x: number, y: number, sys: ParticleSystem) =>
    sys.emit(x, y, 20, { r: 1, g: 0.9, b: 0.2, size: 2, maxLife: 0.8 }),
  smoke: (x: number, y: number, sys: ParticleSystem) =>
    sys.emit(x, y, 10, { r: 0.5, g: 0.5, b: 0.5, size: 12, maxLife: 3, vx: 0, vy: -30 }),
};
```

---

# physics-engine

Physics integration — Rapier.js, rigid bodies, constraints, raycasting, collision callbacks, deterministic simulation.

#### Workflow

**Step 1 — Detect physics setup**
Use Grep to find physics libraries: `rapier`, `cannon`, `ammo`, `@dimforge/rapier3d`, `RigidBody`, `Collider`. Read physics initialization and body creation to understand: engine choice, world configuration, and collision handling.

**Step 2 — Audit physics configuration**
Check for: physics step tied to render frame (non-deterministic), missing collision groups (everything collides with everything), no sleep threshold (wasted CPU on static objects), raycasts without max distance (expensive), and missing body cleanup on entity destroy.

**Step 3 — Emit optimized physics**
Emit: Rapier.js (WASM, deterministic) setup with proper collision groups, sleep thresholds, event-driven collision callbacks, and raycasting utility.

#### Example

```typescript
// Rapier.js (WASM) — setup with collision groups and raycasting
import RAPIER from '@dimforge/rapier3d-compat';

await RAPIER.init();
const world = new RAPIER.World({ x: 0, y: -9.81, z: 0 });

// Collision groups: player=0x0001, enemy=0x0002, ground=0x0004, projectile=0x0008
const GROUPS = { PLAYER: 0x0001, ENEMY: 0x0002, GROUND: 0x0004, PROJECTILE: 0x0008 };

// Ground — static, collides with everything
const groundBody = world.createRigidBody(RAPIER.RigidBodyDesc.fixed().setTranslation(0, 0, 0));
world.createCollider(
  RAPIER.ColliderDesc.cuboid(50, 0.1, 50)
    .setCollisionGroups((GROUPS.GROUND << 16) | 0xFFFF),
  groundBody,
);

// Player — dynamic, collides with ground + enemy (not own projectiles)
const playerBody = world.createRigidBody(RAPIER.RigidBodyDesc.dynamic().setTranslation(0, 5, 0));
world.createCollider(
  RAPIER.ColliderDesc.capsule(0.5, 0.3)
    .setCollisionGroups((GROUPS.PLAYER << 16) | (GROUPS.GROUND | GROUPS.ENEMY))
    .setActiveEvents(RAPIER.ActiveEvents.COLLISION_EVENTS),
  playerBody,
);

// Raycast utility
function raycast(origin: RAPIER.Vector3, direction: RAPIER.Vector3, maxDist = 100) {
  const ray = new RAPIER.Ray(origin, direction);
  const hit = world.castRay(ray, maxDist, true);
  if (hit) {
    const point = ray.pointAt(hit.timeOfImpact);
    return { point, normal: hit.normal, collider: hit.collider };
  }
  return null;
}
```

#### Collision Event Handling

```typescript
// Event-driven collision callbacks — no polling
const eventQueue = new RAPIER.EventQueue(true);

// In fixed update step:
world.step(eventQueue);

eventQueue.drainCollisionEvents((handle1, handle2, started) => {
  const body1 = world.getRigidBody(world.getCollider(handle1).parent()!);
  const body2 = world.getRigidBody(world.getCollider(handle2).parent()!);

  const entity1 = entityMap.get(body1.handle);
  const entity2 = entityMap.get(body2.handle);

  if (started) {
    entity1?.onCollisionEnter(entity2);
    entity2?.onCollisionEnter(entity1);
  } else {
    entity1?.onCollisionExit(entity2);
    entity2?.onCollisionExit(entity1);
  }
});
```

---

# scene-management

Scene transitions, preloading, serialization — stack-based SceneManager with fade transitions, asset preloading before enter, and level JSON serialization.

#### Workflow

**Step 1 — Detect scene structure**
Use Grep to find scene code: `Scene`, `GameState`, `StateMachine`, `push`, `pop`, `replace`. Read to understand: how scenes transition, whether assets are preloaded, and how scene data is persisted.

**Step 2 — Audit scene management**
Check for: abrupt scene switches with no transition (jarring UX), assets loaded mid-scene causing stutters, no scene stack (can't return to previous state), missing cleanup on exit.

**Step 3 — Emit SceneManager**
Emit: stack-based SceneManager with fade in/out, asset preloading tied to scene.assets[], push/pop/replace operations, and level serialization/deserialization.

#### Scene Stack with Transitions and Preloading

```typescript
// Scene manager — stack-based, asset preloading, fade transitions
interface Scene {
  name: string;
  assets: string[]; // asset keys to preload before entering
  onEnter(data?: unknown): void;
  onExit(): void;
  update(dt: number): void;
  render(ctx: CanvasRenderingContext2D): void;
}

class SceneManager {
  private stack: Scene[] = [];
  private loader: AssetLoader;
  private transitioning = false;
  private fadeAlpha = 0;
  private fadeDir: 1 | -1 = 1;

  constructor(loader: AssetLoader) { this.loader = loader; }

  get current(): Scene | undefined { return this.stack[this.stack.length - 1]; }

  async push(scene: Scene, data?: unknown) {
    if (this.transitioning) return;
    this.transitioning = true;

    await this.fadeOut();
    await this.preloadScene(scene);
    this.stack.push(scene);
    scene.onEnter(data);
    await this.fadeIn();

    this.transitioning = false;
  }

  async pop() {
    if (this.transitioning || this.stack.length <= 1) return;
    this.transitioning = true;

    await this.fadeOut();
    this.current?.onExit();
    this.stack.pop();
    await this.fadeIn();

    this.transitioning = false;
  }

  async replace(scene: Scene, data?: unknown) {
    if (this.transitioning) return;
    this.transitioning = true;

    await this.fadeOut();
    this.current?.onExit();
    this.stack.pop();
    await this.preloadScene(scene);
    this.stack.push(scene);
    scene.onEnter(data);
    await this.fadeIn();

    this.transitioning = false;
  }

  private async preloadScene(scene: Scene) {
    // Preload only assets not already cached
    await Promise.all(scene.assets.map(key => this.loader.load(key, `/assets/${key}`)));
  }

  renderTransition(ctx: CanvasRenderingContext2D, w: number, h: number) {
    if (this.fadeAlpha > 0) {
      ctx.save();
      ctx.globalAlpha = this.fadeAlpha;
      ctx.fillStyle = '#000';
      ctx.fillRect(0, 0, w, h);
      ctx.restore();
    }
  }

  private fadeOut(): Promise<void> {
    return new Promise(resolve => {
      this.fadeDir = 1;
      const interval = setInterval(() => {
        this.fadeAlpha = Math.min(1, this.fadeAlpha + 0.05);
        if (this.fadeAlpha >= 1) { clearInterval(interval); resolve(); }
      }, 16);
    });
  }

  private fadeIn(): Promise<void> {
    return new Promise(resolve => {
      this.fadeDir = -1;
      const interval = setInterval(() => {
        this.fadeAlpha = Math.max(0, this.fadeAlpha - 0.05);
        if (this.fadeAlpha <= 0) { clearInterval(interval); resolve(); }
      }, 16);
    });
  }
}

// Level serialization — save/load level state as JSON
interface LevelData {
  name: string;
  entities: Array<{ type: string; x: number; y: number; props: Record<string, unknown> }>;
  tilemap: number[][];
}

function serializeLevel(world: World): LevelData {
  const entities: LevelData['entities'] = [];
  for (const id of world.query(Position)) {
    const pos = world.getComponent(id, Position)!;
    entities.push({ type: 'generic', x: pos.x, y: pos.y, props: {} });
  }
  return { name: 'level1', entities, tilemap: [] };
}

function deserializeLevel(data: LevelData, world: World) {
  for (const e of data.entities) {
    const id = world.createEntity();
    world.addComponent(id, new Position(e.x, e.y));
  }
}
```

---

# threejs-patterns

Three.js patterns — scene setup, React Three Fiber integration, PBR materials, post-processing, performance optimization.

#### Workflow

**Step 1 — Detect Three.js setup**
Use Grep to find Three.js usage: `THREE.`, `useThree`, `useFrame`, `Canvas`, `@react-three/fiber`, `@react-three/drei`. Read the main scene file to understand: renderer setup, scene graph structure, camera type, and lighting model.

**Step 2 — Audit performance**
Check for: objects created inside `useFrame` (GC pressure), missing `dispose()` on unmount (memory leak), no frustum culling on large scenes, textures without power-of-two dimensions, unoptimized geometry (too many draw calls), and missing LOD for distant objects.

**Step 3 — Emit optimized scene**
Emit: properly structured R3F scene with declarative lights, memoized geometries, disposal on unmount, instanced meshes for repeated objects, and post-processing pipeline.

#### Example

```tsx
// React Three Fiber — optimized scene with instancing and post-processing
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Environment, useGLTF, Instances, Instance } from '@react-three/drei';
import { EffectComposer, Bloom, Vignette } from '@react-three/postprocessing';
import { useRef, useMemo } from 'react';

function InstancedTrees({ count = 500 }) {
  const positions = useMemo(() =>
    Array.from({ length: count }, () => [
      (Math.random() - 0.5) * 100,
      0,
      (Math.random() - 0.5) * 100,
    ] as [number, number, number]),
  [count]);

  return (
    <Instances limit={count}>
      <cylinderGeometry args={[0.2, 0.4, 3]} />
      <meshStandardMaterial color="#4a7c59" />
      {positions.map((pos, i) => <Instance key={i} position={pos} />)}
    </Instances>
  );
}

function GameScene() {
  return (
    <Canvas camera={{ position: [0, 10, 20], fov: 60 }} gl={{ antialias: true }}>
      <ambientLight intensity={0.3} />
      <directionalLight position={[10, 20, 10]} intensity={1} castShadow />
      <Environment preset="sunset" />
      <InstancedTrees count={500} />
      <OrbitControls maxPolarAngle={Math.PI / 2.2} />
      <EffectComposer>
        <Bloom intensity={0.3} luminanceThreshold={0.8} />
        <Vignette offset={0.3} darkness={0.6} />
      </EffectComposer>
    </Canvas>
  );
}
```

#### LOD (Level of Detail) Pattern

```typescript
import * as THREE from 'three';

// Swap geometry based on camera distance
function buildLODMesh(
  highGeo: THREE.BufferGeometry,
  midGeo: THREE.BufferGeometry,
  lowGeo: THREE.BufferGeometry,
  material: THREE.Material,
): THREE.LOD {
  const lod = new THREE.LOD();
  lod.addLevel(new THREE.Mesh(highGeo, material), 0);    // < 20 units
  lod.addLevel(new THREE.Mesh(midGeo, material), 20);    // 20–80 units
  lod.addLevel(new THREE.Mesh(lowGeo, material), 80);    // > 80 units
  return lod;
}

// In render loop — LOD auto-updates based on camera distance
// scene.add(buildLODMesh(highGeo, midGeo, lowGeo, mat));
// lod.update(camera); // call once per frame
```

---

# webgl

WebGL patterns — shader programming, GLSL, buffer management, texture handling, instanced rendering.

#### Workflow

**Step 1 — Detect WebGL usage**
Use Grep to find WebGL code: `getContext('webgl`, `gl.createShader`, `gl.createProgram`, `*.glsl`, `*.vert`, `*.frag`. Read shader files and GL initialization to understand: WebGL version, shader complexity, and buffer strategy.

**Step 2 — Audit shader and buffer efficiency**
Check for: uniforms set every frame that don't change (use UBO), separate draw calls for identical geometry (use instancing), textures not using mipmaps, missing `gl.deleteBuffer`/`gl.deleteTexture` cleanup, and shaders with expensive per-fragment branching.

**Step 3 — Emit optimized WebGL code**
Emit: WebGL2 setup with proper context attributes, VAO-based buffer management, instanced rendering for repeated geometry, and GLSL shaders with documented inputs/outputs.

#### Example

```glsl
// Vertex shader — instanced rendering with per-instance transform
#version 300 es
layout(location = 0) in vec3 aPosition;
layout(location = 1) in vec3 aNormal;
layout(location = 2) in mat4 aInstanceMatrix; // per-instance (locations 2-5)

uniform mat4 uViewProjection;

out vec3 vNormal;
out vec3 vWorldPos;

void main() {
  vec4 worldPos = aInstanceMatrix * vec4(aPosition, 1.0);
  vWorldPos = worldPos.xyz;
  vNormal = mat3(transpose(inverse(aInstanceMatrix))) * aNormal;
  gl_Position = uViewProjection * worldPos;
}
```

```glsl
// Fragment shader — PBR-lite with single directional light
#version 300 es
precision highp float;

in vec3 vNormal;
in vec3 vWorldPos;
out vec4 fragColor;

uniform vec3 uLightDir;
uniform vec3 uCameraPos;
uniform vec3 uBaseColor;

void main() {
  vec3 N = normalize(vNormal);
  vec3 L = normalize(uLightDir);
  vec3 V = normalize(uCameraPos - vWorldPos);
  vec3 H = normalize(L + V);

  float diffuse = max(dot(N, L), 0.0);
  float specular = pow(max(dot(N, H), 0.0), 32.0);
  vec3 ambient = uBaseColor * 0.15;

  fragColor = vec4(ambient + uBaseColor * diffuse + vec3(specular * 0.5), 1.0);
}
```

---
> **Rune Skill Mesh** — 64 skills, 203 connections + 40 signals, 14 extension packs
> [Landing Page](https://rune-kit.github.io/rune) · [Source](https://github.com/rune-kit/rune) (MIT)
> **Rune Pro** ($49 lifetime) — product, sales, data-science, support packs → [rune-kit/rune-pro](https://github.com/rune-kit/rune-pro)
> **Rune Business** ($149 lifetime) — finance, legal, HR, enterprise-search packs → [rune-kit/rune-business](https://github.com/rune-kit/rune-business)