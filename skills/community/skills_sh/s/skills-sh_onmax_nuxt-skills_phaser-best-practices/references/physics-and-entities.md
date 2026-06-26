# Physics and Entities

## Contents

- Choosing Arcade vs Matter
- Arcade patterns
- Matter patterns
- Entity composition
- Finite state machines
- Groups and pooling
- Collision handling
- Pooled object reset checklist
- Common mistakes

## Choosing Arcade vs Matter

Use this matrix:

| Need                                                             | Use    |
| ---------------------------------------------------------------- | ------ |
| Platformer, top-down action, shooter, pickup collection          | Arcade |
| Simple overlap checks and fast iteration                         | Arcade |
| Compound bodies, constraints, realistic stacking, heavy rotation | Matter |
| Physics puzzle with body shapes beyond simple AABB / circles     | Matter |
| No real physics, mostly menus / cards / visual novel             | None   |

Default to **Arcade** when the answer is not obvious.

## Arcade patterns

Arcade is the workhorse for most Phaser 3 gameplay.

### Standard player setup

```ts
this.player = this.physics.add.sprite(96, 96, 'player');
this.player.setCollideWorldBounds(true);
this.player.setDrag(1200, 0);
this.player.setMaxVelocity(220, 500);
```

### Colliders and overlaps

```ts
this.physics.add.collider(this.player, this.groundLayer);
this.physics.add.collider(this.player, this.enemies, this.onPlayerHitEnemy, undefined, this);
this.physics.add.overlap(this.player, this.coins, this.onPlayerCollectCoin, undefined, this);
```

Use:

- **collider** for physical separation
- **overlap** for triggers, pickups, hurtboxes, checkpoints, sensors

### Platformer movement baseline

```ts
update() {
  const speed = 180;
  const jumpSpeed = 360;

  if (this.cursors.left.isDown) {
    this.player.setVelocityX(-speed);
    this.player.setFlipX(true);
  } else if (this.cursors.right.isDown) {
    this.player.setVelocityX(speed);
    this.player.setFlipX(false);
  } else {
    this.player.setVelocityX(0);
  }

  if (Phaser.Input.Keyboard.JustDown(this.cursors.up) && this.player.body!.blocked.down) {
    this.player.setVelocityY(-jumpSpeed);
  }
}
```

### Body sizing

Match bodies to gameplay, not to raw sprite dimensions:

```ts
this.player.body!.setSize(18, 28, true);
this.player.body!.setOffset(7, 4);
```

Tight bodies usually feel better than full-sprite hitboxes.

## Matter patterns

Use Matter when the simulation itself is part of the design.

### Minimal sprite setup

```ts
this.player = this.matter.add.sprite(200, 120, 'player');
this.player.setFixedRotation();
this.player.setFriction(0.05);
this.player.setBounce(0);
```

### Bodies and constraints

```ts
const crate = this.matter.add.rectangle(400, 300, 48, 48);
const anchor = this.matter.add.circle(400, 80, 10, { isStatic: true });

this.matter.add.constraint(anchor, crate, 180, 0.8);
```

Use Matter for:

- swinging bodies
- push / topple puzzles
- unusual body shapes
- rotation-sensitive collisions

Do not use Matter just because it sounds more advanced.

## Entity composition

Prefer composition over inheritance for most gameplay objects.

```ts
class Health {
  constructor(public hp: number, public maxHp: number) {}
  damage(amount: number) {
    this.hp = Math.max(0, this.hp - amount);
  }
  get dead() {
    return this.hp <= 0;
  }
}

class ArcadeMover {
  constructor(
    private readonly sprite: Phaser.Physics.Arcade.Sprite,
    private readonly speed: number
  ) {}

  moveX(dir: -1 | 0 | 1) {
    this.sprite.setVelocityX(dir * this.speed);
  }
}

class Enemy {
  readonly health = new Health(30, 30);
  readonly mover: ArcadeMover;

  constructor(readonly sprite: Phaser.Physics.Arcade.Sprite) {
    this.mover = new ArcadeMover(sprite, 70);
  }
}
```

Use composition when:

- multiple entity types share only some behaviors
- you want reusable health, movement, attack, patrol, or loot logic
- deep subclass hierarchies would mostly duplicate state handling

## Finite state machines

Use a state machine when entity behavior is becoming branch-heavy.

```ts
type EnemyState = 'idle' | 'patrol' | 'chase' | 'stunned' | 'dead';

class EnemyBrain {
  private state: EnemyState = 'idle';

  constructor(private readonly enemy: Phaser.Physics.Arcade.Sprite) {}

  update(player: Phaser.Physics.Arcade.Sprite) {
    switch (this.state) {
      case 'idle':
        if (Phaser.Math.Distance.Between(this.enemy.x, this.enemy.y, player.x, player.y) < 180) {
          this.state = 'chase';
        }
        break;
      case 'chase':
        this.enemy.setVelocityX(player.x < this.enemy.x ? -80 : 80);
        break;
      case 'stunned':
      case 'dead':
        this.enemy.setVelocityX(0);
        break;
    }
  }

  stun() {
    this.state = 'stunned';
  }

  die() {
    this.state = 'dead';
  }
}
```

Use an FSM for:

- player locomotion states
- enemy AI states
- boss phases
- run / pause / dialogue state transitions

## Groups and pooling

Pool objects that spawn and despawn often:

- bullets
- slash effects
- enemy projectiles
- damage numbers
- temporary pickups
- frequently recycled enemies

### Arcade pool example

```ts
this.bullets = this.physics.add.group({
  classType: Phaser.Physics.Arcade.Image,
  maxSize: 64,
  runChildUpdate: false
});

fireBullet(x: number, y: number, vx: number, vy: number) {
  const bullet = this.bullets.get(x, y, 'bullet') as Phaser.Physics.Arcade.Image | null;
  if (!bullet) return;

  bullet.setActive(true).setVisible(true);
  bullet.body!.enable = true;
  bullet.body!.reset(x, y);
  bullet.setVelocity(vx, vy);
}
```

### Return to pool

```ts
despawnBullet(bullet: Phaser.Physics.Arcade.Image) {
  bullet.setActive(false).setVisible(false);
  bullet.body!.stop();
  bullet.body!.enable = false;
}
```

Pool only what is frequent enough to matter.

## Collision handling

Keep collision callbacks small and intentional.

### Good overlap callback

```ts
private onPlayerCollectCoin(
  _player: Phaser.GameObjects.GameObject,
  coin: Phaser.GameObjects.GameObject
) {
  const sprite = coin as Phaser.Physics.Arcade.Sprite;
  sprite.disableBody(true, true);
  this.registry.set('coins', (this.registry.get('coins') ?? 0) + 1);
}
```

### Process callback for conditional collision

```ts
private shouldCollidePlayerPlatform(
  player: Phaser.Types.Physics.Arcade.GameObjectWithBody,
  platform: Phaser.Types.Physics.Arcade.GameObjectWithBody
) {
  return player.body.velocity.y >= 0 && player.body.bottom <= platform.body.top + 8;
}

this.physics.add.collider(
  this.player,
  this.oneWayPlatforms,
  undefined,
  this.shouldCollidePlayerPlatform,
  this
);
```

## Pooled object reset checklist

Whenever a pooled object is reused, reset all state that can leak from a previous life:

- position and velocity
- visibility and active flag
- body enabled state
- alpha, scale, tint, rotation, flip
- animation state
- timers or delayed calls tied to the object
- tweens targeting the object
- data values or custom fields such as damage, owner, lifetime, faction

If a pooled object behaves randomly, assume reset state is incomplete until proven otherwise.

## Common mistakes

- using Matter for a simple platformer or shooter
- never resizing Arcade bodies away from full-sprite bounds
- putting AI, movement, attacks, and animation switching directly in the scene `update()`
- destroying bullets instead of pooling them in a bullet-heavy game
- forgetting to stop tweens or timers before returning pooled objects
- assuming `touching.down` and `blocked.down` mean the same thing in every situation
- creating physics bodies for decorative sprites or UI art
