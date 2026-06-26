# Tilemaps, Camera, Input, and Audio

## Contents

- Tilemap defaults
- Tiled layer organization
- Loading maps and tilesets
- Collision setup
- Object layers and spawn data
- Camera patterns
- Input mapping
- Gamepad support
- Audio patterns
- Timers and tweens
- Common mistakes

## Tilemap defaults

Use Tiled JSON unless the user explicitly needs procedural-only map generation.

Good reasons to use tilemaps:

- authored platformer levels
- collision-heavy overworlds
- spawn data in object layers
- reusable environment art
- parallax or foreground / background separation

## Tiled layer organization

A practical layer order:

```text
Foreground
UI markers / debug helpers (dev only)
Objects
Enemies
Collectibles
Ground
Background
```

For complex maps, split object layers by purpose:

- `SpawnPoints`
- `Enemies`
- `Collectibles`
- `Triggers`
- `Doors`
- `NPCs`

Do not overload one giant object layer with unrelated semantics.

## Loading maps and tilesets

```ts
preload() {
  this.load.tilemapTiledJSON('level-1', 'assets/maps/level-1.json');
  this.load.image('terrain', 'assets/maps/terrain.png');
  this.load.image('props', 'assets/maps/props.png');
}
```

```ts
create() {
  const map = this.make.tilemap({ key: 'level-1' });

  const terrain = map.addTilesetImage('terrain', 'terrain');
  const props = map.addTilesetImage('props', 'props');

  const background = map.createLayer('Background', [terrain, props], 0, 0);
  const ground = map.createLayer('Ground', [terrain, props], 0, 0);
  const foreground = map.createLayer('Foreground', [terrain, props], 0, 0);

  foreground.setDepth(100);
}
```

If the tileset uses spacing or margin, pass those values in `addTilesetImage`.

```ts
const terrain = map.addTilesetImage('terrain', 'terrain', 32, 32, 1, 2);
```

## Collision setup

Prefer collision by tile property where possible. It survives art changes better than raw index ranges.

```ts
ground.setCollisionByProperty({ collides: true });
this.physics.add.collider(this.player, ground);
```

Use index-based collision when the map export or tileset metadata is too simple for properties:

```ts
ground.setCollisionBetween(1, 64);
```

Use tile callbacks for hazards or triggers when that reads better than large collider callbacks.

## Object layers and spawn data

Use object layers for spawn points and designer-authored metadata.

```ts
const spawn = map.findObject('SpawnPoints', (obj) => obj.name === 'player-start');
this.player = this.physics.add.sprite(spawn!.x!, spawn!.y!, 'player');
```

Read custom properties from Tiled objects with a helper:

```ts
function getObjectProp<T>(obj: { properties?: Array<{ name: string; value: unknown }> }, name: string): T | undefined {
  return obj.properties?.find((p) => p.name === name)?.value as T | undefined;
}
```

Use object layers for:

- spawn locations
- patrol points
- scene exits
- chest or switch metadata
- checkpoint positions

## Camera patterns

### Follow camera

```ts
this.cameras.main.startFollow(this.player, true, 0.12, 0.12);
this.cameras.main.setBounds(0, 0, map.widthInPixels, map.heightInPixels);
this.physics.world.setBounds(0, 0, map.widthInPixels, map.heightInPixels);
```

### Deadzone for larger worlds

```ts
this.cameras.main.setDeadzone(160, 90);
```

### Pixel-art camera rounding

```ts
this.cameras.main.roundPixels = true;
```

Use this when pixel art shimmers during follow movement.

### HUD separation

Use a UI scene for HUD instead of `setScrollFactor(0)` on everything. Reserve `setScrollFactor(0)` for a few world-attached elements that truly should ignore camera scroll.

## Input mapping

Keep input scene-owned and expose an input state object.

```ts
type InputState = {
  left: boolean;
  right: boolean;
  up: boolean;
  down: boolean;
  jumpPressed: boolean;
  firePressed: boolean;
};

create() {
  const cursors = this.input.keyboard!.createCursorKeys();
  const fire = this.input.keyboard!.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);

  this.inputState = {
    left: false,
    right: false,
    up: false,
    down: false,
    jumpPressed: false,
    firePressed: false
  };

  this.updateInputState = () => {
    this.inputState.left = cursors.left.isDown;
    this.inputState.right = cursors.right.isDown;
    this.inputState.up = cursors.up.isDown;
    this.inputState.down = cursors.down.isDown;
    this.inputState.jumpPressed = Phaser.Input.Keyboard.JustDown(cursors.up);
    this.inputState.firePressed = Phaser.Input.Keyboard.JustDown(fire);
  };
}

update() {
  this.updateInputState();
  this.playerController.update(this.inputState);
}
```

This makes remapping, replay systems, AI takeover, and mobile control injection easier.

## Pointer and touch

Use Phaser's unified pointer system for mouse and touch.

```ts
this.input.on('pointerdown', (pointer: Phaser.Input.Pointer) => {
  this.spawnPing(pointer.worldX, pointer.worldY);
});
```

Touch-friendly patterns:

- enlarge hit areas
- avoid placing important controls against unsafe screen edges
- use drag or tap consistently
- test with one pointer first; only add multi-touch if the game truly needs it

## Gamepad support

Add gamepad support when the game fits it, but keep it optional.

```ts
create() {
  this.input.gamepad?.once('connected', (pad: Phaser.Input.Gamepad.Gamepad) => {
    this.pad = pad;
  });
}

update() {
  if (this.pad) {
    this.inputState.left ||= this.pad.left;
    this.inputState.right ||= this.pad.right;
    this.inputState.jumpPressed ||= this.pad.A;
  }
}
```

Do not hard-require a gamepad mapping in a browser game unless the user asked for it.

## Audio patterns

Use two channels of intent:

- **BGM**: longer loops, scene or mode ownership
- **SFX**: short one-shots, event-driven

### Loading with format fallbacks

```ts
preload() {
  this.load.audio('bgm-forest', [
    'assets/audio/bgm-forest.ogg',
    'assets/audio/bgm-forest.mp3'
  ]);

  this.load.audio('pickup', [
    'assets/audio/pickup.ogg',
    'assets/audio/pickup.mp3'
  ]);
}
```

### Basic usage

```ts
create() {
  this.music = this.sound.add('bgm-forest', { loop: true, volume: 0.5 });
  this.music.play();
}

collectCoin() {
  this.sound.play('pickup', { volume: 0.8 });
}
```

Centralize user settings such as music mute and SFX mute in the registry or a dedicated audio service.

## Timers and tweens

Prefer Phaser timers and tweens over ad hoc `setTimeout`.

### Timer example

```ts
this.time.delayedCall(1200, () => {
  this.spawnWave();
});
```

### Tween example

```ts
this.tweens.add({
  targets: this.promptText,
  alpha: 0.2,
  duration: 400,
  yoyo: true,
  repeat: -1
});
```

Track timers or tweens that must be canceled on scene shutdown.

## Common mistakes

- storing essential spawn logic only in hand-written code when Tiled objects would be clearer
- forgetting to match the Tiled tileset name in `addTilesetImage`
- not setting camera and physics bounds to the map size
- mixing scene-owned input with entity-owned listeners
- assuming `pointer.x` / `pointer.y` are world coordinates when the camera moved
- starting multiple music tracks because a scene restart did not stop or reuse the old one
- using browser `setTimeout` instead of Phaser's clock for gameplay timing
