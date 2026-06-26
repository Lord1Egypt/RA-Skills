# SpriteKit Patterns

Advanced SpriteKit patterns for tile maps, texture atlases, shader effects,
scene transitions, game loop architecture, audio, and SceneKit embedding.

## Contents

- [Tile Maps](#tile-maps)
- [Texture Atlases](#texture-atlases)
- [Scene Transitions](#scene-transitions)
- [Game Loop Patterns](#game-loop-patterns)
- [Audio](#audio)
- [Lighting](#lighting)
- [Custom Shaders](#custom-shaders)
- [Constraints](#constraints)
- [Physics Joints](#physics-joints)
- [Physics Fields](#physics-fields)
- [Crop and Effect Nodes](#crop-and-effect-nodes)
- [SceneKit in SpriteKit](#scenekit-in-spritekit)
- [Performance Optimization](#performance-optimization)

## Tile Maps

`SKTileMapNode` renders a grid of tile images. Define tile sets in Xcode's
SpriteKit scene editor or build them programmatically. Tile maps support
square, hexagonal, and isometric grids.

### Programmatic Tile Map

```swift
func createTileMap() -> SKTileMapNode {
    // Create tile definitions
    let grassTexture = SKTexture(imageNamed: "grass")
    let grassDef = SKTileDefinition(texture: grassTexture, size: CGSize(width: 32, height: 32))

    let dirtTexture = SKTexture(imageNamed: "dirt")
    let dirtDef = SKTileDefinition(texture: dirtTexture, size: CGSize(width: 32, height: 32))

    // Create tile groups
    let grassGroup = SKTileGroup(tileDefinition: grassDef)
    let dirtGroup = SKTileGroup(tileDefinition: dirtDef)

    // Create tile set
    let tileSet = SKTileSet(tileGroups: [grassGroup, dirtGroup])

    // Create tile map
    let tileMap = SKTileMapNode(
        tileSet: tileSet,
        columns: 20,
        rows: 15,
        tileSize: CGSize(width: 32, height: 32)
    )
    tileMap.fill(with: grassGroup)
    return tileMap
}
```

### Setting Individual Tiles

```swift
// Set a specific tile
tileMap.setTileGroup(dirtGroup, forColumn: 5, row: 3)

// Set tile with a specific definition (for adjacency rules)
tileMap.setTileGroup(dirtGroup, andTileDefinition: dirtDef, forColumn: 5, row: 3)
```

### Coordinate Conversion

Convert between tile grid coordinates and scene positions:

```swift
// Scene position to tile coordinate
let column = tileMap.tileColumnIndex(fromPosition: touchLocation)
let row = tileMap.tileRowIndex(fromPosition: touchLocation)

// Tile coordinate to scene position
let center = tileMap.centerOfTile(atColumn: column, row: row)
```

### Adding Physics to Tiles

Tile maps do not expose individual tiles as nodes. Overlay invisible
`SKNode` objects for physics:

```swift
func addPhysicsToTileMap(_ tileMap: SKTileMapNode) {
    let tileSize = tileMap.tileSize

    for column in 0..<tileMap.numberOfColumns {
        for row in 0..<tileMap.numberOfRows {
            guard let def = tileMap.tileDefinition(atColumn: column, row: row),
                  def.userData?["isWall"] as? Bool == true else { continue }

            let center = tileMap.centerOfTile(atColumn: column, row: row)
            let wall = SKNode()
            wall.position = center
            wall.physicsBody = SKPhysicsBody(rectangleOf: tileSize)
            wall.physicsBody?.isDynamic = false
            wall.physicsBody?.categoryBitMask = PhysicsCategory.wall
            tileMap.addChild(wall)
        }
    }
}
```

### Adjacency Rules

Use `SKTileGroupRule` with adjacency masks for auto-tiling (e.g., terrain
edges that blend into neighboring terrain):

```swift
let centerRule = SKTileGroupRule(
    adjacency: .adjacencyAll,
    tileDefinitions: [centerDef]
)
let topEdgeRule = SKTileGroupRule(
    adjacency: .adjacencyUpEdge,
    tileDefinitions: [topEdgeDef]
)
let tileGroup = SKTileGroup(rules: [centerRule, topEdgeRule])
```

Enable auto-fill by using `tileMap.enableAutomapping = true` in the scene
editor. The tile map picks the correct definition based on neighboring tiles.

## Texture Atlases

Texture atlases pack multiple images into a single texture, reducing draw
calls and improving GPU performance.

### Creating an Atlas in Xcode

1. Add a folder with the `.atlas` extension to the asset catalog.
2. Place individual images inside the folder.
3. SpriteKit compiles them into a single texture sheet at build time.

### Loading Textures from an Atlas

```swift
let atlas = SKTextureAtlas(named: "Characters")
let textures = atlas.textureNames.sorted().map { atlas.textureNamed($0) }

let animation = SKAction.animate(with: textures, timePerFrame: 0.1)
sprite.run(SKAction.repeatForever(animation))
```

### Preloading Atlases

Preload atlases before presenting a scene to avoid frame drops during
first use:

```swift
SKTextureAtlas.preloadTextureAtlasesNamed(["Characters", "Environment"]) {
    error, atlases in
    // Atlases are now in GPU memory; present the scene.
    presentGameScene()
}
```

Alternatively, use SpriteKit's async preload APIs:

```swift
func preloadAssets() async throws {
    _ = try await SKTextureAtlas.preloadTextureAtlasesNamed([
        "Characters",
        "Environment"
    ])

    await SKTextureAtlas.preloadTextureAtlases([
        SKTextureAtlas(named: "Effects")
    ])
}
```

### Texture Filtering

```swift
let texture = SKTexture(imageNamed: "pixel_art")
texture.filteringMode = .nearest  // Sharp pixels for pixel art
// .linear (default) for smooth scaling
```

## Scene Transitions

`SKTransition` provides animated transitions between scenes. Present the
new scene with a transition through the view:

```swift
func goToGameOver() {
    let gameOverScene = GameOverScene(size: size)
    gameOverScene.scaleMode = scaleMode
    let transition = SKTransition.fade(withDuration: 1.0)
    view?.presentScene(gameOverScene, transition: transition)
}
```

### Transition Types

```swift
// Fade
SKTransition.fade(withDuration: 1.0)
SKTransition.fade(with: .black, duration: 1.0)

// Slide
SKTransition.push(with: .left, duration: 0.5)
SKTransition.moveIn(with: .right, duration: 0.5)
SKTransition.reveal(with: .down, duration: 0.5)

// Dissolve effects
SKTransition.crossFade(withDuration: 1.0)
SKTransition.flipHorizontal(withDuration: 0.5)
SKTransition.flipVertical(withDuration: 0.5)

// Doors
SKTransition.doorway(withDuration: 1.0)
SKTransition.doorsOpenHorizontal(withDuration: 0.5)
SKTransition.doorsOpenVertical(withDuration: 0.5)
SKTransition.doorsCloseHorizontal(withDuration: 0.5)
SKTransition.doorsCloseVertical(withDuration: 0.5)
```

### Pausing During Transition

By default, both the outgoing and incoming scenes run during a transition.
Pause the outgoing scene if needed:

```swift
let transition = SKTransition.fade(withDuration: 1.0)
transition.pausesOutgoingScene = true
transition.pausesIncomingScene = false
```

## Game Loop Patterns

### Delta Time Tracking

Frame-rate-independent movement requires delta time calculation:

```swift
final class GameScene: SKScene {

    private var lastUpdateTime: TimeInterval = 0

    override func update(_ currentTime: TimeInterval) {
        let deltaTime: TimeInterval
        if lastUpdateTime == 0 {
            deltaTime = 0
        } else {
            deltaTime = currentTime - lastUpdateTime
        }
        lastUpdateTime = currentTime

        updateEntities(deltaTime: deltaTime)
    }
}
```

### Entity-Component Pattern

Organize game objects using a simple entity-component structure. For complex
games, consider GameplayKit's `GKEntity` and `GKComponent`.

```swift
protocol GameComponent {
    func update(deltaTime: TimeInterval)
}

final class HealthComponent: GameComponent {
    var hitPoints: Int
    var maxHitPoints: Int

    init(hitPoints: Int) {
        self.hitPoints = hitPoints
        self.maxHitPoints = hitPoints
    }

    func update(deltaTime: TimeInterval) { }

    func takeDamage(_ amount: Int) {
        hitPoints = max(0, hitPoints - amount)
    }
}

final class MovementComponent: GameComponent {
    weak var node: SKNode?
    var velocity: CGVector = .zero

    func update(deltaTime: TimeInterval) {
        guard let node else { return }
        node.position.x += velocity.dx * deltaTime
        node.position.y += velocity.dy * deltaTime
    }
}
```

### Spawn Timer Pattern

Use `SKAction` for timed spawning rather than manual timer tracking:

```swift
func startSpawning() {
    let spawn = SKAction.run { [weak self] in
        self?.spawnEnemy()
    }
    let delay = SKAction.wait(forDuration: 2.0, withRange: 1.0) // 1.5-2.5s
    run(SKAction.repeatForever(SKAction.sequence([spawn, delay])), withKey: "spawning")
}

func stopSpawning() {
    removeAction(forKey: "spawning")
}
```

### Scene Delegate Pattern

Use `SKSceneDelegate` to share update logic across scenes without
subclassing:

```swift
final class GameController: SKSceneDelegate {

    func update(_ currentTime: TimeInterval, for scene: SKScene) {
        // Shared game logic applied to any scene
    }

    func didEvaluateActions(for scene: SKScene) { }
    func didSimulatePhysics(for scene: SKScene) { }
}

// Usage
let scene = SKScene(fileNamed: "Level1")!
scene.delegate = gameController
```

## Audio

### SKAudioNode

`SKAudioNode` provides positional audio tied to a node's position in the
scene. Set the scene's `listener` property for spatial audio.

```swift
// Background music
let music = SKAudioNode(fileNamed: "background.mp3")
music.autoplayLooped = true
music.isPositional = false
addChild(music)

// Positional sound effect
let engineSound = SKAudioNode(fileNamed: "engine.wav")
engineSound.isPositional = true
engineSound.autoplayLooped = true
spaceship.addChild(engineSound)

// Set the listener for positional audio
listener = cameraNode
```

### Sound Effects with SKAction

For short, non-positional sound effects:

```swift
let playSound = SKAction.playSoundFileNamed("explosion.wav", waitForCompletion: false)
run(playSound)
```

This is simple but offers no volume or positional control. Use `SKAudioNode`
for sounds that need spatial positioning or dynamic volume.

### Stopping Audio

```swift
// Stop a specific audio node
music.run(SKAction.changeVolume(to: 0, duration: 1.0)) {
    music.removeFromParent()
}

// Or immediately
music.removeFromParent()
```

## Lighting

`SKLightNode` adds 2D lighting with shadows to a scene. Light affects
sprites that have matching `lightingBitMask` values.

```swift
let light = SKLightNode()
light.categoryBitMask = 0b0001
light.falloff = 1.5
light.ambientColor = UIColor(white: 0.3, alpha: 1.0)
light.lightColor = .white
light.shadowColor = UIColor(white: 0.0, alpha: 0.5)
light.position = player.position
addChild(light)

// Enable lighting on a sprite
wall.lightingBitMask = 0b0001
wall.shadowCastBitMask = 0b0001   // This sprite casts shadows
wall.shadowedBitMask = 0b0001     // This sprite receives shadows
```

### Normal Maps for Depth

Apply a normal map texture to a sprite for per-pixel lighting detail:

```swift
let sprite = SKSpriteNode(imageNamed: "stone_wall")
sprite.normalTexture = SKTexture(imageNamed: "stone_wall_normal")
sprite.lightingBitMask = 0b0001
```

## Custom Shaders

`SKShader` applies custom GLSL fragment shaders to sprites, shape nodes,
emitters, and tile maps.

```swift
let shader = SKShader(source: """
    void main() {
        vec2 uv = v_tex_coord;
        vec4 color = texture2D(u_texture, uv);
        float gray = dot(color.rgb, vec3(0.299, 0.587, 0.114));
        gl_FragColor = vec4(vec3(gray), color.a) * v_color_mix;
    }
""")
sprite.shader = shader
```

### Uniform Variables

Pass values from Swift to the shader:

```swift
let shader = SKShader(fileNamed: "dissolve.fsh")
shader.uniforms = [
    SKUniform(name: "u_threshold", float: 0.5)
]
sprite.shader = shader

// Update at runtime
shader.uniformNamed("u_threshold")?.floatValue = newValue
```

### Built-in Shader Symbols

| Symbol | Type | Description |
|----------|------|-------------|
| `u_texture` | `sampler2D` | The node's texture |
| `u_time` | `float` | Time since shader attached |
| `u_path_length` | `float` | Path length (shape nodes) |
| `v_tex_coord` | `vec2` | Texture coordinate |
| `v_color_mix` | `vec4` | Node's blend color |
| `v_path_distance` | `float` | Distance along a shape-node stroke path |
| `SKDefaultShading()` | function | Default SpriteKit shading behavior |

Values such as `u_sprite_size` are app-defined uniforms or attributes, not
SpriteKit-provided built-ins.

### Attribute Values

Pass per-node values through attributes when multiple nodes share a shader
but need different parameters:

```swift
let shader = SKShader(fileNamed: "tint.fsh")
shader.attributes = [
    SKAttribute(name: "a_tintColor", type: .vectorFloat4)
]

sprite.setValue(
    SKAttributeValue(vectorFloat4: vector_float4(1, 0, 0, 1)),
    forAttribute: "a_tintColor"
)
```

## Constraints

`SKConstraint` limits a node's position or rotation automatically each frame.

```swift
// Keep node oriented toward a target
let orient = SKConstraint.orient(to: targetNode, offset: SKRange(constantValue: 0))
turret.constraints = [orient]

// Keep node within a rectangular boundary
let xRange = SKRange(lowerLimit: 50, upperLimit: frame.width - 50)
let yRange = SKRange(lowerLimit: 50, upperLimit: frame.height - 50)
let boundary = SKConstraint.positionX(xRange, y: yRange)
player.constraints = [boundary]

// Keep distance from another node
let distance = SKConstraint.distance(SKRange(lowerLimit: 50, upperLimit: 200), to: leader)
follower.constraints = [distance]
```

## Physics Joints

Joints connect two physics bodies. Both bodies must exist in the scene before
creating a joint.

```swift
// Pin joint: bodies rotate around a shared anchor
let pin = SKPhysicsJointPin.joint(
    withBodyA: wheelBody,
    bodyB: chassisBody,
    anchor: wheelNode.position
)
physicsWorld.add(pin)

// Spring joint: elastic connection
let spring = SKPhysicsJointSpring.joint(
    withBodyA: bodyA.physicsBody!,
    bodyB: bodyB.physicsBody!,
    anchorA: bodyA.position,
    anchorB: bodyB.position
)
spring.frequency = 1.0
spring.damping = 0.5
physicsWorld.add(spring)

// Fixed joint: rigid connection
let fixed = SKPhysicsJointFixed.joint(
    withBodyA: partA.physicsBody!,
    bodyB: partB.physicsBody!,
    anchor: CGPoint(x: 0, y: 0)
)
physicsWorld.add(fixed)

// Sliding joint: constrained to an axis
let slide = SKPhysicsJointSliding.joint(
    withBodyA: slider.physicsBody!,
    bodyB: track.physicsBody!,
    anchor: slider.position,
    axis: CGVector(dx: 1, dy: 0)
)
physicsWorld.add(slide)

// Limit joint: maximum distance between anchors
let limit = SKPhysicsJointLimit.joint(
    withBodyA: chainLink1.physicsBody!,
    bodyB: chainLink2.physicsBody!,
    anchorA: chainLink1.position,
    anchorB: chainLink2.position
)
physicsWorld.add(limit)
```

Remove joints with `physicsWorld.remove(joint)`.

## Physics Fields

`SKFieldNode` applies forces to physics bodies within a region. Bodies opt
in through `fieldBitMask`.

```swift
// Radial gravity (black hole effect)
let gravity = SKFieldNode.radialGravityField()
gravity.strength = 5.0
gravity.falloff = 1.0
gravity.position = CGPoint(x: frame.midX, y: frame.midY)
gravity.region = SKRegion(radius: 200)
addChild(gravity)

// Vortex (swirling)
let vortex = SKFieldNode.vortexField()
vortex.strength = 2.0

// Turbulence (random jitter)
let turbulence = SKFieldNode.turbulenceField(withSmoothness: 0.5, animationSpeed: 1.0)

// Linear gravity (wind)
let wind = SKFieldNode.linearGravityField(withVector: vector_float3(2, 0, 0))
wind.strength = 3.0

// Electric field (attracts/repels based on charge)
let electric = SKFieldNode.electricField()
// Set physicsBody.charge on affected bodies
```

Bodies interact with fields when their `fieldBitMask` matches the field
node's `categoryBitMask`.

## Crop and Effect Nodes

### SKCropNode

Masks child content using another node as a mask shape:

```swift
let cropNode = SKCropNode()
let maskShape = SKSpriteNode(imageNamed: "circle_mask")
cropNode.maskNode = maskShape
cropNode.addChild(contentSprite)
addChild(cropNode)
```

Only the portions of children that overlap the mask's non-transparent pixels
are rendered.

### SKEffectNode

Applies a Core Image filter to its child subtree:

```swift
let effectNode = SKEffectNode()
effectNode.shouldRasterize = true  // Cache the result for performance
effectNode.filter = CIFilter(name: "CIGaussianBlur", parameters: [
    "inputRadius": 10.0
])
effectNode.addChild(backgroundSprite)
addChild(effectNode)
```

Use `shouldRasterize = true` when children do not change frequently.

## SceneKit in SpriteKit

`SK3DNode` embeds a SceneKit scene within a SpriteKit scene:

```swift
let node3D = SK3DNode(viewportSize: CGSize(width: 200, height: 200))

let scnScene = SCNScene(named: "model.scn")!
node3D.scnScene = scnScene

// Set a camera for the 3D viewport
let scnCamera = SCNCamera()
let cameraNode = SCNNode()
cameraNode.camera = scnCamera
cameraNode.position = SCNVector3(x: 0, y: 2, z: 5)
scnScene.rootNode.addChild(cameraNode)
node3D.pointOfView = cameraNode

node3D.position = CGPoint(x: frame.midX, y: frame.midY)
addChild(node3D)
```

The 3D node participates in the 2D scene's draw order like any other node.

## Performance Optimization

### Draw Call Reduction

- Use texture atlases to batch sprites sharing the same atlas into a single
  draw call.
- Set `ignoresSiblingOrder = true` on `SKView` to enable automatic batching.
- Avoid `SKShapeNode` for repeated elements; convert shapes to textures using
  `SKView.texture(from:)`.

### Node Count Management

- Remove offscreen nodes. Use `SKCameraNode.containedNodeSet()` or manual
  bounds checking to cull nodes that leave the viewport.
- Pool and reuse nodes instead of creating and destroying them each frame.
- Use `SKAction.removeFromParent()` in action sequences for projectiles and
  effects that leave the screen.

```swift
final class NodePool<T: SKNode> {
    private var available: [T] = []

    func acquire() -> T {
        if let node = available.popLast() {
            return node
        }
        return T()
    }

    func release(_ node: T) {
        node.removeAllActions()
        node.removeFromParent()
        available.append(node)
    }
}
```

### Physics Optimization

- Use simple shapes (`circleOfRadius`, `rectangleOf`) over `texture:size:`
  bodies when possible.
- Set `usesPreciseCollisionDetection = true` only on fast-moving small bodies
  that tunnel through thin obstacles.
- Set `isDynamic = false` on static scenery.
- Limit the number of active physics bodies; disable physics on offscreen
  nodes.

### Emitter Performance

- Limit `particleBirthRate` and `particleLifetime` to the minimum needed.
- Set `numParticlesToEmit` for finite effects and remove the emitter after
  completion.
- Use `advanceSimulationTime(_:)` to pre-warm emitters that should appear
  mid-effect when added to the scene.
- Set `targetNode` to the scene when particles should detach from a moving
  emitter, but be aware this prevents batching.

### Texture Memory

- Use the smallest texture size that looks acceptable at the rendered size.
- Provide @2x and @3x variants only when necessary.
- Call `SKTextureAtlas.preloadTextureAtlases` to load textures before the
  scene appears, avoiding mid-game stalls.

### Profiling

Enable debug overlays on `SKView` during development:

```swift
skView.showsFPS = true
skView.showsNodeCount = true
skView.showsDrawCount = true
skView.showsPhysics = true
```

Use Instruments with the SpriteKit template to profile frame time, draw
calls, and node count over time. The Core Animation instrument helps
identify GPU bottlenecks.
