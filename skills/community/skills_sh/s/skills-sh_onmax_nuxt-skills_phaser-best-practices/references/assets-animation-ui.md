# Assets, Animations, and UI Panels

## Contents

- Asset pipeline defaults
- Images vs spritesheets vs atlases
- Loader measurement protocol
- Animation patterns
- Aseprite support
- UI slicing strategy
- Built-in NineSlice / ThreeSlice
- Custom fallback for difficult art
- Asset-key conventions
- Common mistakes

## Asset pipeline defaults

Use stable keys, predictable folders, and measured loader configs.

Recommended categories:

```text
public/assets/
├── images/
├── sprites/
├── atlases/
├── maps/
├── audio/
├── ui/
└── fonts/
```

Keep file naming boring and consistent. Prefer `kebab-case` or `snake_case`, but use one style consistently.

## Images vs spritesheets vs atlases

Choose the asset container deliberately.

### Use an image when

- the art is static
- there is only one frame
- no animation or slicing is required

```ts
this.load.image('background-forest', 'assets/images/background-forest.png');
```

### Use a spritesheet when

- frames are a uniform grid
- frame width and height are constant
- the asset is animation-first or grid-sliced UI art

```ts
this.load.spritesheet('player-run', 'assets/sprites/player-run.png', {
  frameWidth: 32,
  frameHeight: 32
});
```

### Use an atlas when

- frames are irregular sizes
- many sprites should share one texture for batching
- export tooling already produces a texture atlas

```ts
this.load.atlas('game-atlas', 'assets/atlases/game.png', 'assets/atlases/game.json');
```

Rule of thumb:

- **spritesheet** for measured uniform grids
- **atlas** for production sprite packs and batched mixed assets

## Loader measurement protocol

Never guess spritesheet metrics.

Before writing loader code:

1. inspect the source image
2. record total width and height
3. count rows and columns
4. measure actual frame width and height
5. check for spacing between cells
6. check for margin around the whole sheet
7. verify the math closes exactly

### Example with spacing

```ts
this.load.spritesheet('wood-panel', 'assets/ui/wood-panel.png', {
  frameWidth: 144,
  frameHeight: 144,
  spacing: 8
});
```

### Example with margin and spacing

```ts
this.load.spritesheet('icons', 'assets/ui/icons.png', {
  frameWidth: 32,
  frameHeight: 32,
  margin: 4,
  spacing: 2
});
```

If the sheet dimensions do not divide cleanly, stop and re-measure.

## Animation patterns

### Prefer global animations for shared motion

```ts
if (!this.anims.exists('player-run')) {
  this.anims.create({
    key: 'player-run',
    frames: this.anims.generateFrameNumbers('player-run', { start: 0, end: 5 }),
    frameRate: 12,
    repeat: -1
  });
}
```

Use global animations when multiple instances share the same data.

### Use local animations only for one-off behavior

Local animations are appropriate when:

- a single sprite needs unique frame timing
- a cutscene prop has custom animation data
- you explicitly do not want other sprites to reuse the animation

### Animation switching rule

Only switch animations when the state changed. Do not spam `.play()` with different keys every frame unless required.

```ts
if (this.player.body!.velocity.x !== 0) {
  this.player.anims.play('player-run', true);
} else {
  this.player.anims.play('player-idle', true);
}
```

### Completion handling

```ts
this.player.on(Phaser.Animations.Events.ANIMATION_COMPLETE, (anim) => {
  if (anim.key === 'enemy-die') {
    this.player.destroy();
  }
});
```

## Aseprite support

If the asset pipeline uses Aseprite JSON exports, create animations from the exported data instead of hand-writing every frame list.

```ts
this.load.aseprite(
  'hero',
  'assets/sprites/hero.png',
  'assets/sprites/hero.json'
);

this.anims.createFromAseprite('hero');
```

Use Aseprite-driven animations when the animation tags in the art tool already describe the desired behavior.

## UI slicing strategy

Use the simplest UI scaling technique that preserves the art.

### Use plain images when

- the panel size is fixed
- the art does not need to scale

### Use ThreeSlice when

- the UI element stretches horizontally only
- the source art is really left-cap / center / right-cap

### Use NineSlice when

- the source art is a regular 3x3 layout
- corners must stay fixed
- edges stretch on one axis
- center stretches freely

### Use custom composition when

- frames contain large transparent padding
- the art has discontinuous gaps or gutters
- built-in slicing produces visible side bars or broken seams

## Built-in NineSlice / ThreeSlice

Prefer the built-in game object first.

### NineSlice

```ts
const panel = this.add.nineslice(
  320,
  180,
  'ui-panels',
  'paper-panel',
  420,
  260,
  24,
  24,
  24,
  24
);
panel.setOrigin(0.5);
```

### ThreeSlice

Create a 3-slice by setting top and bottom slice heights to zero:

```ts
const ribbon = this.add.nineslice(
  320,
  80,
  'ui-panels',
  'banner',
  300,
  48,
  18,
  18,
  0,
  0
);
```

Use built-in slicing when the art is genuinely slice-friendly. Do not jump to custom canvas composition first.

## Custom fallback for difficult art

Some asset packs look like nine-slice art but are not actually safe to stretch directly.

Use a custom fallback when you observe:

- opaque side bars just inside edges
- stretched transparent gutters
- seams between stitched slices
- later slices drifting because spacing or margins were mis-measured

Fallback strategy:

1. measure the real painted bounds in each source frame
2. trim away large transparent padding
3. render the slices into a composed texture at the target size
4. add tiny overlap to hide seams
5. disable smoothing for pixel-art UI

This is a fallback, not the default.

## Asset-key conventions

Centralize keys in one place:

```ts
export const SCENES = {
  Boot: 'BootScene',
  Menu: 'MenuScene',
  Game: 'GameScene',
  UI: 'UIScene'
} as const;

export const TEX = {
  Player: 'player',
  Atlas: 'game-atlas',
  PaperPanel: 'paper-panel'
} as const;

export const ANIMS = {
  PlayerIdle: 'player-idle',
  PlayerRun: 'player-run'
} as const;
```

This reduces typo bugs and improves refactor safety.

## Common mistakes

- guessing frame width or spacing
- putting every animated frame set into a separate PNG when an atlas would batch better
- re-creating global animations every scene start without checking `this.anims.exists()`
- forcing custom nine-slice composition when the built-in NineSlice already works
- using built-in NineSlice on art with large transparent padding and assuming the result is trustworthy
- scattering asset keys as raw strings across dozens of files
