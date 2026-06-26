# Performance and Debugging

## Contents

- Performance mindset
- Biggest wins first
- Pooling patterns
- Update-loop hygiene
- Rendering and asset strategy
- Physics workload control
- Scene-safe cleanup
- Debug tooling
- TestScene pattern
- Shipping checklist

## Performance mindset

Profile before optimizing. Phaser performance problems usually come from a small number of recurring causes:

- too many active objects
- too many physics bodies or unnecessary collision pairs
- allocation churn inside `update()`
- oversized particle systems
- expensive AI or pathfinding every frame
- unnecessary scene overlap
- leaking listeners, timers, or tweens across restarts

Start with the simplest explanation and verify it.

## Biggest wins first

Tackle these before micro-optimizations:

1. pool frequently spawned objects
2. reduce active physics bodies and collision pairs
3. stop off-screen or inactive systems from updating
4. throttle expensive AI / pathfinding / scanning work
5. trim particles, post-processing, and unnecessary overdraw
6. simplify scene responsibilities if multiple scenes are running at once

## Pooling patterns

Pool when spawn / despawn is frequent enough to create churn.

### Bullet pool

```ts
this.bullets = this.physics.add.group({
  classType: Phaser.Physics.Arcade.Image,
  maxSize: 100
});
```

```ts
fireBullet(x: number, y: number, vx: number, vy: number) {
  const bullet = this.bullets.get(x, y, 'bullet') as Phaser.Physics.Arcade.Image | null;
  if (!bullet) return;

  bullet.setActive(true).setVisible(true);
  bullet.body!.enable = true;
  bullet.body!.reset(x, y);
  bullet.setVelocity(vx, vy);
}
```

```ts
killBullet(bullet: Phaser.Physics.Arcade.Image) {
  this.tweens.killTweensOf(bullet);
  bullet.body!.stop();
  bullet.body!.enable = false;
  bullet.setActive(false).setVisible(false);
}
```

Pool only what matters. Premature pooling of rare objects adds complexity for little gain.

## Update-loop hygiene

### Good habits

- reuse vectors or temp objects
- use primitive values when possible
- throttle logic that does not need 60 Hz updates
- keep `update()` short and orchestration-focused

### Bad pattern

```ts
update() {
  const target = { x: this.player.x + 10, y: this.player.y }; // allocates every frame
  this.enemy.body!.velocity.x = target.x - this.enemy.x;
}
```

### Better pattern

```ts
update(time: number) {
  if (time - this.lastAiTick > 100) {
    this.updateEnemyAi();
    this.lastAiTick = time;
  }
}
```

Use `delta` or elapsed time for framerate-independent movement and throttling decisions.

## Rendering and asset strategy

### Use atlases when it helps batching

When many related sprites can share a texture, prefer atlases over dozens of separate files.

### Keep backgrounds simple

Good options:

- large static image
- tile sprite
- one or two parallax layers

Be careful with:

- many translucent full-screen layers
- large particle fields over the entire screen
- stacked blend modes everywhere

### Pixel art

For crisp pixel art:

- use `pixelArt: true`
- favor integer-friendly zoom
- avoid sub-pixel camera drift
- test actual device/browser output, not just desktop Chrome

## Physics workload control

### Reduce collision pairs

Only add the collisions the game needs.

Good:

```ts
this.physics.add.collider(this.player, this.groundLayer);
this.physics.add.collider(this.enemies, this.groundLayer);
this.physics.add.overlap(this.player, this.pickups, this.onPickup, undefined, this);
```

Bad:

```ts
this.physics.add.collider(this.enemies, this.enemies);
this.physics.add.collider(this.pickups, this.pickups);
```

Only enable broad collision matrices when the mechanic genuinely needs them.

### Disable or recycle inactive bodies

```ts
enemy.body!.enable = false;
enemy.setActive(false).setVisible(false);
```

For projectile-heavy games, disable bodies immediately when the object leaves play.

## Scene-safe cleanup

A surprising amount of "performance" trouble is actually leaked state after scene restarts.

On shutdown, clean:

- timers
- tweens
- global or foreign-scene listeners
- debug overlays
- DOM nodes added during debugging
- stale references in services or caches

Example:

```ts
create() {
  this.events.once(Phaser.Scenes.Events.SHUTDOWN, this.onShutdown, this);
}

private onShutdown() {
  this.time.removeAllEvents();
  this.tweens.killAll();
  // destroy any colliders or debug helpers you created and tracked explicitly
}
```

Only destroy colliders or managers you own; be careful not to tear down shared systems accidentally.

## Debug tooling

### Physics debug

Enable during diagnosis, not by default in shipping builds.

```ts
physics: {
  default: 'arcade',
  arcade: {
    debug: true
  }
}
```

### Tile collision debug

```ts
groundLayer.renderDebug(this.add.graphics(), {
  tileColor: null,
  collidingTileColor: new Phaser.Display.Color(255, 0, 0, 100),
  faceColor: new Phaser.Display.Color(0, 255, 0, 255)
});
```

### Runtime inspection

Useful things to inspect:

- active scenes
- world bounds
- camera bounds and follow target
- texture cache keys
- whether a pooled object was truly reset

### Debug overlays

If you add DOM-based FPS meters or debug widgets, remember to remove them on shutdown.

## TestScene pattern

Use a dedicated sandbox scene for isolated mechanics.

A good `TestScene` can quickly answer:

- are sprite bounds correct?
- did the body size / offset match the art?
- are animations valid?
- does a projectile pool reset correctly?
- does a new tileset align with the map?

Keep `TestScene` out of production scene lists when shipping.

## Shipping checklist

Before declaring a Phaser task done, verify:

- the game still restarts the affected scene cleanly
- no duplicate listeners were introduced
- pooled objects reset fully
- scene transitions do not leave music or overlays behind
- tile collisions match the visual art
- pixel-art projects are still crisp after the change
- performance-sensitive changes were tested with representative object counts
- debug flags and test helpers are removed or gated
