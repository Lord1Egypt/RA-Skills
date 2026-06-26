# Setup and Build

## Contents

- New-project defaults
- Recommended folder layouts
- Game configuration patterns
- Scale and renderer decisions
- Pixel-art settings
- Loader timing and asset strategy
- Vite / static asset handling
- Example bootstrap
- Validation checklist

## New-project defaults

For a new Phaser 3 project, prefer a modern browser build setup with TypeScript unless the repository already uses plain JavaScript.

Use this as the default stack:

- Phaser 3
- Vite for local dev and production builds
- TypeScript for scene keys, asset keys, and physics object typing
- `public/assets` for static runtime files, or module imports for bundled art files
- `src/game` (or `src/`) as the game code root

If the user already has a Webpack, Parcel, Bun, or plain HTML setup, stay consistent unless they asked for a migration.

## Recommended folder layouts

### Small game / prototype

```text
src/
├── main.ts
├── game/
│   ├── config.ts
│   ├── constants.ts
│   └── scenes/
│       ├── BootScene.ts
│       ├── GameScene.ts
│       └── UIScene.ts
public/
└── assets/
```

### Mid-size game

```text
src/
├── main.ts
├── game/
│   ├── config/
│   │   ├── game-config.ts
│   │   └── keys.ts
│   ├── scenes/
│   ├── entities/
│   ├── systems/
│   ├── services/
│   └── ui/
public/
└── assets/
```

### Content-heavy game

```text
src/
├── main.ts
├── game/
│   ├── config/
│   ├── scenes/
│   ├── entities/
│   ├── systems/
│   ├── services/
│   ├── ui/
│   ├── data/
│   └── utils/
public/
└── assets/
```

Use the smallest structure that cleanly supports the current scope.

## Game configuration patterns

### Baseline Arcade config

```ts
import Phaser from 'phaser';

export const gameConfig: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  width: 960,
  height: 540,
  backgroundColor: '#101418',
  parent: 'game-root',
  scene: [],
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { y: 0 },
      debug: false
    }
  },
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH
  }
};
```

### Matter config

```ts
export const gameConfig: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  width: 1280,
  height: 720,
  scene: [],
  physics: {
    default: 'matter',
    matter: {
      gravity: { y: 1 },
      debug: false
    }
  },
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH
  }
};
```

### Pixel-art config

```ts
export const gameConfig: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  width: 320,
  height: 180,
  pixelArt: true,
  roundPixels: true,
  autoRound: true,
  scene: [],
  physics: {
    default: 'arcade',
    arcade: { debug: false }
  },
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH
  }
};
```

## Scale and renderer decisions

Use this decision table:

| Need                                                     | Recommendation                                     |
| -------------------------------------------------------- | -------------------------------------------------- |
| Standard responsive game                                 | `Phaser.Scale.FIT`                                 |
| UI-heavy app or layout that should resize to the browser | `Phaser.Scale.RESIZE`                              |
| Manually controlled canvas size                          | `Phaser.Scale.NONE`                                |
| Unsure about renderer                                    | `Phaser.AUTO`                                      |
| Pixel art                                                | `pixelArt: true`, integer-friendly base resolution |
| Heavy post-processing or filters                         | prefer WebGL / `AUTO`                              |

Important host-page rules:

- Put the game inside a parent container you control
- Do not add padding directly to the Phaser parent element
- Put borders, padding, or layout chrome on a wrapper outside the Phaser parent
- Let Phaser manage the canvas display size; avoid overriding canvas width / height with ad hoc CSS

## Pixel-art settings

Use all of these together when the art style is pixel art:

- `pixelArt: true`
- `roundPixels: true`
- low native resolution with `FIT`
- camera `roundPixels = true` if camera follow produces shimmer
- integer zoom if possible

Avoid:

- high native resolution plus CSS downscaling
- sub-pixel camera scroll on crisp pixel art
- mixing linear-scaled UI art and pixel-art gameplay without deliberate separation

## Loader timing and asset strategy

### Use `preload()` for assets needed when the scene starts

```ts
preload() {
  this.load.image('logo', 'assets/ui/logo.png');
  this.load.audio('confirm', [
    'assets/audio/confirm.ogg',
    'assets/audio/confirm.mp3'
  ]);
}
```

### Lazy-load later when it improves startup time

If assets are loaded outside `preload()`, remember to start the loader manually:

```ts
queueLevelTwoAssets() {
  this.load.image('boss', 'assets/enemies/boss.png');
  this.load.tilemapTiledJSON('level2', 'assets/maps/level2.json');
  this.load.start();
}
```

Use lazy loading for:

- later levels
- cosmetic-only content
- optional menu art
- large boss or cutscene assets

Do not lazy-load assets that are required immediately on scene start.

## Boot scene guidance

Use a Boot scene for:

- a loading bar or splash
- startup-critical assets
- decoding or preparing data needed before the first menu / game scene

Do **not** turn Boot into a mandatory "load the whole game forever" scene unless the game is tiny.

## Vite / static asset handling

Two safe patterns:

### 1. Static assets in `public/assets`

Use this for larger asset libraries or files referenced by string paths:

```ts
this.load.image('player', 'assets/player.png');
this.load.audio('bgm', ['assets/music.ogg', 'assets/music.mp3']);
```

### 2. Imported bundled assets

Use this for a few assets that belong tightly to one module:

```ts
import logoImg from '../assets/logo.png';

preload() {
  this.load.image('logo', logoImg);
}
```

Choose one approach consistently per asset family.

## Example bootstrap

```ts
// src/main.ts
import Phaser from 'phaser';
import { gameConfig } from './game/config/game-config';
import { BootScene } from './game/scenes/BootScene';
import { MenuScene } from './game/scenes/MenuScene';
import { GameScene } from './game/scenes/GameScene';
import { UIScene } from './game/scenes/UIScene';

new Phaser.Game({
  ...gameConfig,
  scene: [BootScene, MenuScene, GameScene, UIScene]
});
```

## Validation checklist

Before finishing a setup task, verify:

- the scene array contains the expected startup order
- the chosen scale mode fits the target platform
- the physics default matches the actual gameplay needs
- pixel-art projects use pixel-art-friendly settings
- asset paths align with the repository's bundler strategy
- startup scenes only preload what they truly need
