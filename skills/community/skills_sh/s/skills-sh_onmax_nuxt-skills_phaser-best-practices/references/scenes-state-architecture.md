# Scenes, State, and Architecture

## Contents

- Scene lifecycle essentials
- Scene responsibilities
- Pause vs sleep vs stop vs remove
- Cross-scene state patterns
- Architecture sizes
- UI overlay pattern
- Lifecycle-safe cleanup
- Scene restart pitfalls
- Example scene skeleton
- Architecture anti-patterns

## Scene lifecycle essentials

A Phaser scene is booted once, started zero or more times, and can be shut down and started again until it is removed.

Use the lifecycle like this:

- `init(data)`: receive start parameters and reset scene-local state
- `preload()`: queue assets required at scene start
- `create()`: create objects, input bindings, colliders, timers, UI
- `update(time, delta)`: orchestrate per-frame behavior

Important nuance:

- **shutdown** means the scene stopped running and may start again later
- **destroy** means the scene was removed and cannot be used again

Write code that survives scene restarts cleanly.

## Scene responsibilities

Use scenes as top-level game modes, not as random code buckets.

Typical split:

- **BootScene**: startup-critical loading, splash, data priming
- **MenuScene**: title, difficulty, save-slot choice, options entry
- **GameScene**: core simulation and world logic
- **UIScene**: HUD, counters, health bars, crosshairs, inventory overlays
- **PauseScene**: pause menu or modal overlay
- **GameOverScene**: run summary, restart flow, progression summary

Keep HUD and gameplay separate unless the game is tiny.

## Pause vs sleep vs stop vs remove

Use the right scene transition operation:

- `scene.pause(key)`: scene still renders, but does not update
- `scene.sleep(key)`: scene neither updates nor renders
- `scene.stop(key)`: scene shuts down and can be started again later
- `scene.remove(key)`: scene is destroyed and removed from the manager

Practical guidance:

- use **pause** for gameplay under a visible pause overlay
- use **sleep** for background scenes you want to wake later
- use **stop** for scenes that should fully reset on next start
- use **remove** only when the scene should never be reused or is dynamically created

## Cross-scene state patterns

Choose the smallest state-sharing mechanism that fits.

### 1. Scene start data

Use for one-time transitions:

```ts
this.scene.start('GameOverScene', { score: this.score, timeMs: this.elapsedMs });
```

Best for:

- score / result handoff
- selected level or seed
- checkpoint data
- modal scene parameters

### 2. Global registry

Use for small game-wide state:

```ts
this.registry.set('musicEnabled', true);
this.registry.set('coins', 42);

const coins = this.registry.get('coins');
```

Best for:

- settings
- meta progression
- currently selected profile or seed
- small shared counters

Do not turn the registry into an unstructured dumping ground.

### 3. Services / managers

Use for medium or large shared systems:

- `AudioService`
- `SaveService`
- `RunState`
- `InventoryService`
- `LevelDirector`

These can be plain modules, classes owned by bootstrap code, or scene-attached services.

Use services when:

- multiple scenes read and write the same domain state
- invariants matter
- the state has behavior, not just values

### 4. Events between scenes

Use events for decoupled notifications:

```ts
// UIScene
this.game.events.emit('hud:toggle-minimap', true);

// GameScene
this.game.events.on('hud:toggle-minimap', this.onToggleMinimap, this);
```

If you attach cross-scene listeners, add cleanup on shutdown / destroy.

## Architecture sizes

### Small / jam game

Use:

- 2-4 scenes
- constants file
- a few entity classes
- minimal services

Avoid building a full ECS or data layer unless the user asked for it.

### Mid-size action game

Use:

- scenes
- entity classes
- systems for combat, spawning, AI, pickups
- constants / content config
- one or two shared services

This is the default architecture for many production Phaser games.

### Large content-heavy game

Use:

- scenes as shells for game modes
- data-driven content tables / JSON
- reusable services for save, progression, encounter generation
- UI layer separate from world simulation
- typed content schemas if the project uses TypeScript

## UI overlay pattern

A dedicated UI scene usually scales better than baking HUD into the gameplay scene.

```ts
// In GameScene.create()
this.scene.launch('UIScene', { ownerScene: 'GameScene' });

// In UIScene.create(data)
this.ownerSceneKey = data.ownerScene;
this.game.events.on('score:changed', this.onScoreChanged, this);
```

Use a UI scene when you need:

- HUD independent of camera scroll
- pause overlays
- inventory or modal panels
- cross-scene UI that survives game scene resets

Keep the UI scene thin; it should render and react, not own the game simulation.

## Lifecycle-safe cleanup

Do not invent a `shutdown()` scene method and assume Phaser will call it. Register cleanup with scene events.

```ts
export class GameScene extends Phaser.Scene {
  private onResizeBound?: () => void;

  create() {
    this.events.once(Phaser.Scenes.Events.SHUTDOWN, this.onShutdown, this);
    this.events.once(Phaser.Scenes.Events.DESTROY, this.onDestroy, this);

    this.onResizeBound = () => {
      // layout logic
    };

    this.scale.on(Phaser.Scale.Events.RESIZE, this.onResizeBound);
  }

  private onShutdown() {
    if (this.onResizeBound) {
      this.scale.off(Phaser.Scale.Events.RESIZE, this.onResizeBound);
    }

    this.time.removeAllEvents();
    this.tweens.killAll();
  }

  private onDestroy() {
    // final teardown for permanently removed scenes
  }
}
```

At shutdown, clean up:

- event listeners attached to global emitters, `game.events`, `scale`, `registry`, or foreign scenes
- long-lived timers
- tweens that should not survive a restart
- cached references to scene objects that will be recreated

## Scene restart pitfalls

These are common sources of bugs:

- registering keyboard or resize listeners every `create()` without removing them
- keeping pooled objects in module scope after the scene stops
- storing references to destroyed sprites in services
- relying on constructor initialization instead of resetting state in `init()` / `create()`
- launching UI or pause scenes multiple times without checking whether they already exist

## Example scene skeleton

```ts
export class GameScene extends Phaser.Scene {
  private cursors!: Phaser.Types.Input.Keyboard.CursorKeys;
  private player!: Phaser.Physics.Arcade.Sprite;
  private level = 1;

  constructor() {
    super('GameScene');
  }

  init(data: { level?: number }) {
    this.level = data.level ?? 1;
  }

  preload() {
    this.load.image('player', 'assets/player.png');
  }

  create() {
    this.events.once(Phaser.Scenes.Events.SHUTDOWN, this.onShutdown, this);

    this.player = this.physics.add.sprite(64, 64, 'player');
    this.cursors = this.input.keyboard!.createCursorKeys();
  }

  update(_: number, delta: number) {
    const speed = 180;
    this.player.setVelocity(0);

    if (this.cursors.left.isDown) this.player.setVelocityX(-speed);
    else if (this.cursors.right.isDown) this.player.setVelocityX(speed);

    // Delegate deeper logic elsewhere once the scene grows
    this.updateWorld(delta);
  }

  private updateWorld(delta: number) {
    // systems / entity orchestration
  }

  private onShutdown() {
    // remove cross-scene listeners, timers, etc
  }
}
```

## Architecture anti-patterns

Avoid these unless the game is truly trivial:

- one mega-scene that owns gameplay, HUD, menus, save logic, and audio policy
- using the registry for every piece of state
- keeping all entities as anonymous sprites with logic in `update()`
- attaching input listeners inside every entity constructor
- carrying game objects across scenes with `ignoreDestroy` unless you have a very deliberate ownership model
- deep inheritance trees for enemy variants when configuration + composition would work better

## Rule of thumb

If a scene is hard to restart safely, its responsibilities are probably too broad.
