# Tilemaps Reference

Comprehensive guide for Phaser 3 tilemap integration with Tiled.

## Tiled Setup Best Practices

### Tileset Configuration

1. Use embedded tilesets (File > Export Tileset if external)
2. Set consistent tile size (16x16, 32x32, 64x64)
3. Add custom properties to tiles for collision, damage, etc.
4. Use tile collision editor for precise hitboxes

### Layer Organization

```
Recommended layer structure (top to bottom in Tiled):
- Foreground (renders above player)
- Objects (spawn points, triggers)
- Player (reference layer, not exported)
- Enemies (object layer)
- Collectibles (object layer)
- Ground (collision layer)
- Background (decoration)
```

## Loading Tilemaps

### JSON Format (Recommended)

```javascript
preload() {
  // Load tilemap JSON (exported from Tiled)
  this.load.tilemapTiledJSON('level1', 'assets/tilemaps/level1.json');

  // Load tileset image(s)
  this.load.image('tiles', 'assets/tilesets/tileset.png');

  // For multiple tilesets
  this.load.image('terrain', 'assets/tilesets/terrain.png');
  this.load.image('props', 'assets/tilesets/props.png');
}
```

### Tileset with Margins/Spacing

```javascript
// If tileset has margin (border) or spacing (between tiles)
this.load.image('tiles', 'assets/tileset.png');

// Later, specify margin and spacing
const tileset = map.addTilesetImage('tileset-name', 'tiles',
  tileWidth, tileHeight, margin, spacing);

// Example: 32x32 tiles with 1px margin and 2px spacing
const tileset = map.addTilesetImage('my-tiles', 'tiles', 32, 32, 1, 2);
```

## Creating the Map

### Basic Setup

```javascript
create() {
  // Create tilemap from loaded JSON
  const map = this.make.tilemap({ key: 'level1' });

  // Add tileset image (name must match Tiled tileset name)
  const tileset = map.addTilesetImage('tileset-name-in-tiled', 'tiles');

  // Create layers (names must match Tiled layer names)
  const bgLayer = map.createLayer('Background', tileset, 0, 0);
  const groundLayer = map.createLayer('Ground', tileset, 0, 0);
  const fgLayer = map.createLayer('Foreground', tileset, 0, 0);

  // Foreground renders above player
  fgLayer.setDepth(10);
}
```

### Multiple Tilesets

```javascript
const terrainTileset = map.addTilesetImage('terrain', 'terrain-img');
const propsTileset = map.addTilesetImage('props', 'props-img');

// Layer can use multiple tilesets
const groundLayer = map.createLayer('Ground', [terrainTileset, propsTileset]);
```

## Collision Setup

### By Tile Index

```javascript
// Single tile
groundLayer.setCollision(1);

// Multiple tiles
groundLayer.setCollision([1, 2, 3, 4, 5]);

// Range of tiles
groundLayer.setCollisionBetween(1, 100);

// Exclude tiles
groundLayer.setCollisionByExclusion([-1]); // All except empty
```

### By Custom Property

Set properties in Tiled (Tileset > Edit Tileset > Select tile > Add property)

```javascript
// Collide tiles with "collides: true" property
groundLayer.setCollisionByProperty({ collides: true });

// Multiple properties
groundLayer.setCollisionByProperty({ solid: true, type: 'wall' });
```

### Physics Collider

```javascript
// Add physics collision
this.physics.add.collider(player, groundLayer);

// With callback
this.physics.add.collider(player, hazardLayer, onHazardHit, null, this);

function onHazardHit(player, tile) {
  console.log('Hit hazard at', tile.x, tile.y);
  player.damage(10);
}
```

## Object Layers

### Reading Objects

```javascript
// Get all objects from layer
const objectLayer = map.getObjectLayer('Objects');
const objects = objectLayer.objects;

objects.forEach(obj => {
  console.log(obj.name, obj.x, obj.y, obj.properties);
});

// Find specific object
const spawnPoint = map.findObject('Objects', obj => obj.name === 'spawn');
player.setPosition(spawnPoint.x, spawnPoint.y);

// Filter objects
const enemies = map.filterObjects('Objects', obj => obj.type === 'enemy');
```

### Creating Sprites from Objects

```javascript
// Create sprites from object layer
const coins = map.createFromObjects('Collectibles', {
  name: 'coin',         // Object name in Tiled
  key: 'coin'           // Texture key
});

// Add physics to all coins
this.physics.world.enable(coins);
coins.forEach(coin => {
  coin.body.setAllowGravity(false);
});

// With custom class
const enemies = map.createFromObjects('Enemies', {
  name: 'goblin',
  classType: Goblin     // Custom class extending Sprite
});
```

### Custom Properties on Objects

In Tiled, add custom properties to objects. Access in Phaser:

```javascript
const obj = map.findObject('Objects', o => o.name === 'door');

// Access properties
const isLocked = obj.properties.find(p => p.name === 'locked').value;
const requiredKey = obj.properties.find(p => p.name === 'keyType').value;

// Helper function
function getProperty(obj, name) {
  const prop = obj.properties?.find(p => p.name === name);
  return prop ? prop.value : undefined;
}
```

## Tile Manipulation

### Get/Set Tiles

```javascript
// Get tile at world position
const tile = groundLayer.getTileAtWorldXY(pointer.x, pointer.y);

// Get tile at tile coordinates
const tile = groundLayer.getTileAt(tileX, tileY);

// Set tile
groundLayer.putTileAt(tileIndex, tileX, tileY);

// Remove tile
groundLayer.removeTileAt(tileX, tileY);

// Replace tiles
groundLayer.replaceByIndex(oldIndex, newIndex);
```

### Tile Properties

```javascript
if (tile) {
  console.log(tile.index);         // Tile index
  console.log(tile.x, tile.y);     // Tile coordinates
  console.log(tile.pixelX, tile.pixelY);  // World position
  console.log(tile.properties);    // Custom properties

  // Check collision
  if (tile.collides) {
    // This tile has collision
  }
}
```

### Iterate Tiles

```javascript
// Process each tile in layer
groundLayer.forEachTile(tile => {
  if (tile.index === 77) {  // Spike tile
    // Replace with sprite
    const spike = this.add.sprite(tile.getCenterX(), tile.getCenterY(), 'spike');
    groundLayer.removeTileAt(tile.x, tile.y);
  }
});

// With bounds
groundLayer.forEachTile(callback, context,
  startX, startY, width, height, filteringOptions);
```

## Camera and World Bounds

```javascript
// Set world bounds to map size
this.physics.world.setBounds(0, 0, map.widthInPixels, map.heightInPixels);

// Camera bounds
this.cameras.main.setBounds(0, 0, map.widthInPixels, map.heightInPixels);

// Follow player
this.cameras.main.startFollow(player, true, 0.1, 0.1);

// Dead zones (player can move in center without camera moving)
this.cameras.main.setDeadzone(200, 100);
```

## Advanced Techniques

### Parallax Scrolling

```javascript
// Create layers with different scroll factors
const skyLayer = map.createLayer('Sky', tileset);
const cloudsLayer = map.createLayer('Clouds', tileset);
const mountainsLayer = map.createLayer('Mountains', tileset);
const groundLayer = map.createLayer('Ground', tileset);

// Closer layers scroll faster (1 = normal, <1 = slower)
skyLayer.setScrollFactor(0);        // Fixed background
cloudsLayer.setScrollFactor(0.2);
mountainsLayer.setScrollFactor(0.5);
groundLayer.setScrollFactor(1);     // Normal scrolling
```

### Animated Tiles

Phaser doesn't natively animate tilemap tiles. Use plugin or manual approach:

```javascript
// Manual approach: swap tile indices on timer
this.time.addEvent({
  delay: 200,
  callback: () => {
    waterLayer.forEachTile(tile => {
      if (tile.index >= 10 && tile.index <= 13) {
        tile.index = 10 + ((tile.index - 10 + 1) % 4);
      }
    });
  },
  loop: true
});
```

### Procedural Tilemap

```javascript
// Create blank tilemap
const map = this.make.tilemap({
  tileWidth: 32,
  tileHeight: 32,
  width: 100,
  height: 50
});

const tileset = map.addTilesetImage('tiles');
const layer = map.createBlankLayer('Ground', tileset);

// Fill programmatically
for (let x = 0; x < map.width; x++) {
  for (let y = 0; y < map.height; y++) {
    if (y === map.height - 1) {
      layer.putTileAt(1, x, y);  // Ground
    } else if (Math.random() < 0.1) {
      layer.putTileAt(2, x, y);  // Random obstacle
    }
  }
}

layer.setCollision([1, 2]);
```

### Weighted Random Tiles

```javascript
function getWeightedTile() {
  const tiles = [
    { index: 1, weight: 10 },   // Grass (common)
    { index: 2, weight: 3 },    // Flower (uncommon)
    { index: 3, weight: 1 }     // Mushroom (rare)
  ];

  const total = tiles.reduce((sum, t) => sum + t.weight, 0);
  let random = Math.random() * total;

  for (const tile of tiles) {
    random -= tile.weight;
    if (random <= 0) return tile.index;
  }
  return tiles[0].index;
}
```

## Debugging Tilemaps

```javascript
// Render tile coordinates
groundLayer.forEachTile(tile => {
  if (tile.index !== -1) {
    this.add.text(tile.pixelX, tile.pixelY, `${tile.x},${tile.y}`, {
      fontSize: '10px'
    }).setOrigin(0);
  }
});

// Debug collision tiles
groundLayer.renderDebug(this.add.graphics(), {
  tileColor: null,
  collidingTileColor: new Phaser.Display.Color(255, 0, 0, 100),
  faceColor: new Phaser.Display.Color(0, 255, 0, 255)
});
```
