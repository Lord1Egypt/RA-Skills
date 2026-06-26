# RealityKit + ARKit Extended Patterns

Overflow reference for the `realitykit` skill. Contains advanced patterns that exceed the main skill file's scope.

## Contents

- [Physics Simulation](#physics-simulation)
- [Entity Animations](#entity-animations)
- [Custom Materials and Lighting](#custom-materials-and-lighting)
- [Entity Component System](#entity-component-system)
- [Occlusion and Environment](#occlusion-and-environment)
- [RealityKit + SwiftUI Integration](#realitykit--swiftui-integration)
- [Performance Tips](#performance-tips)

## Physics Simulation

### Rigid Body Physics

```swift
import RealityKit

func createPhysicsScene(content: RealityViewCameraContent) {
    // Ground plane (static body)
    let ground = ModelEntity(
        mesh: .generatePlane(width: 2, depth: 2),
        materials: [SimpleMaterial(color: .gray, isMetallic: false)]
    )
    ground.components.set(PhysicsBodyComponent(
        massProperties: .default,
        material: .default,
        mode: .static
    ))
    ground.components.set(CollisionComponent(
        shapes: [.generateBox(size: [2, 0.01, 2])]
    ))
    ground.position = [0, -0.5, -1]
    content.add(ground)

    // Falling box (dynamic body)
    let box = ModelEntity(
        mesh: .generateBox(size: 0.1),
        materials: [SimpleMaterial(color: .red, isMetallic: true)]
    )
    box.components.set(PhysicsBodyComponent(
        massProperties: .init(mass: 1.0),
        material: PhysicsMaterialResource.generate(
            staticFriction: 0.5,
            dynamicFriction: 0.5,
            restitution: 0.7
        ),
        mode: .dynamic
    ))
    box.components.set(CollisionComponent(
        shapes: [.generateBox(size: [0.1, 0.1, 0.1])]
    ))
    box.position = [0, 0.5, -1]
    content.add(box)
}
```

### Applying Forces and Impulses

```swift
// Apply a continuous force (in Newtons)
if var physics = entity.components[PhysicsBodyComponent.self] {
    // Forces are applied per-frame via the physics simulation
}

// Apply an instantaneous impulse
if let physicsEntity = entity as? HasPhysicsBody {
    physicsEntity.addForce([0, 10, 0], relativeTo: nil)
    physicsEntity.applyLinearImpulse([5, 0, 0], relativeTo: nil)
}
```

### Collision Detection

```swift
RealityView { content in
    // Setup entities...

    _ = content.subscribe(to: CollisionEvents.Began.self) { event in
        print("Collision between \(event.entityA.name) and \(event.entityB.name)")
    }

    _ = content.subscribe(to: CollisionEvents.Ended.self) { event in
        print("Collision ended between \(event.entityA.name) and \(event.entityB.name)")
    }
}
```

## Entity Animations

### Transform Animation

```swift
func animateEntity(_ entity: Entity) {
    // Move to a new position over 2 seconds
    var transform = entity.transform
    transform.translation = [0.5, 0, -0.5]

    entity.move(
        to: transform,
        relativeTo: entity.parent,
        duration: 2.0,
        timingFunction: .easeInOut
    )
}
```

### Orbit Animation

```swift
func orbitAnimation(
    entity: Entity,
    content: RealityViewCameraContent
) {
    var angle: Float = 0
    let radius: Float = 0.3
    let center = SIMD3<Float>(0, 0, -0.8)

    _ = content.subscribe(to: SceneEvents.Update.self) { event in
        angle += Float(event.deltaTime) * 1.5
        entity.position = center + SIMD3<Float>(
            cos(angle) * radius,
            0,
            sin(angle) * radius
        )
    }
}
```

### Playing USDZ Animations

```swift
RealityView { content in
    if let character = try? await ModelEntity(named: "character") {
        content.add(character)

        // Play all available animations
        if let animation = character.availableAnimations.first {
            character.playAnimation(
                animation.repeat(duration: .infinity),
                transitionDuration: 0.5,
                startsPaused: false
            )
        }
    }
}
```

## Custom Materials and Lighting

### SimpleMaterial Variations

```swift
// Metallic material
let metallic = SimpleMaterial(
    color: .init(tint: .gray, texture: nil),
    roughness: .float(0.1),
    isMetallic: true
)

// Transparent material
var transparent = SimpleMaterial()
transparent.color = .init(
    tint: UIColor.blue.withAlphaComponent(0.5),
    texture: nil
)
transparent.blending = .transparent(opacity: 0.5)

// Textured material
if let texture = try? await TextureResource(named: "wood") {
    var textured = SimpleMaterial()
    textured.color = .init(
        tint: .white,
        texture: .init(texture)
    )
}
```

### Environment Lighting

```swift
RealityView { content in
    // Use image-based lighting
    if let resource = try? await EnvironmentResource(named: "studio") {
        content.environment.lighting.resource = resource
        content.environment.lighting.intensityExponent = 1.0
    }
}
```

## Entity Component System

### Custom Components

Define custom components to attach data to entities:

```swift
import RealityKit

struct HealthComponent: Component {
    var currentHealth: Float
    var maxHealth: Float

    var healthPercentage: Float {
        currentHealth / maxHealth
    }
}

// Register the component (once, at app launch)
HealthComponent.registerComponent()

// Attach to an entity
let enemy = ModelEntity(
    mesh: .generateBox(size: 0.1),
    materials: [SimpleMaterial(color: .red, isMetallic: false)]
)
enemy.components.set(HealthComponent(
    currentHealth: 100,
    maxHealth: 100
))
```

### Custom Systems

Systems process entities with matching components each frame:

```swift
struct HealthColorSystem: System {
    static let query = EntityQuery(where: .has(HealthComponent.self))

    init(scene: Scene) { }

    func update(context: SceneUpdateContext) {
        for entity in context.entities(
            matching: Self.query,
            updatingSystemWhen: .rendering
        ) {
            guard let health = entity.components[HealthComponent.self],
                  var model = entity.components[ModelComponent.self]
            else { continue }

            let ratio = health.healthPercentage
            let color = UIColor(
                red: CGFloat(1 - ratio),
                green: CGFloat(ratio),
                blue: 0,
                alpha: 1
            )
            model.materials = [SimpleMaterial(
                color: color,
                isMetallic: false
            )]
            entity.components.set(model)
        }
    }
}

// Register the system
HealthColorSystem.registerSystem()
```

## Occlusion and Environment

### Occlusion Material

Use occlusion materials to hide virtual content behind real-world surfaces:

```swift
let occlusionPlane = ModelEntity(
    mesh: .generatePlane(width: 1, depth: 1),
    materials: [OcclusionMaterial()]
)
occlusionPlane.position = [0, -0.5, -1]
content.add(occlusionPlane)
```

This makes virtual objects appear to go behind real-world surfaces.

### Environment Configuration

```swift
RealityView { content in
    // Configure the background
    content.environment.background = .color(.clear)  // AR camera passthrough

    // Adjust lighting intensity
    content.environment.lighting.intensityExponent = 1.2
}
```

## RealityKit + SwiftUI Integration

### AR Model Viewer with Controls

```swift
import SwiftUI
import RealityKit
import AVFoundation

@Observable
@MainActor
final class ARViewModel {
    var selectedModelName: String = "robot"
    var modelScale: Float = 0.01
    var isPlaced = false

    private var currentEntity: ModelEntity?

    func loadModel(into content: RealityViewCameraContent) async {
        // Remove existing model
        currentEntity?.removeFromParent()

        guard let model = try? await ModelEntity(
            named: selectedModelName
        ) else { return }

        model.scale = [modelScale, modelScale, modelScale]
        model.position = [0, -0.2, -0.8]
        model.name = "currentModel"

        // Enable interaction
        model.generateCollisionShapes(recursive: true)
        model.components.set(InputTargetComponent())

        content.add(model)
        currentEntity = model
        isPlaced = true
    }
}

struct ARModelViewer: View {
    @State private var viewModel = ARViewModel()
    @State private var cameraAuthorized = false

    var body: some View {
        ZStack {
            if cameraAuthorized {
                RealityView { content in
                    await viewModel.loadModel(into: content)
                } update: { content in
                    if let model = content.entities.first(
                        where: { $0.name == "currentModel" }
                    ) {
                        let s = viewModel.modelScale
                        model.scale = [s, s, s]
                    }
                }
                .gesture(
                    DragGesture()
                        .targetedToAnyEntity()
                        .onChanged { value in
                            value.entity.position = value.convert(
                                value.location3D,
                                from: .local,
                                to: value.entity.parent!
                            )
                        }
                )
            } else {
                ContentUnavailableView(
                    "Camera Required",
                    systemImage: "camera.fill",
                    description: Text("Allow camera access for AR.")
                )
            }

            VStack {
                Spacer()
                controlsPanel
            }
        }
        .task {
            let status = AVCaptureDevice.authorizationStatus(for: .video)
            if status == .authorized {
                cameraAuthorized = true
            } else if status == .notDetermined {
                cameraAuthorized = await AVCaptureDevice
                    .requestAccess(for: .video)
            }
        }
    }

    private var controlsPanel: some View {
        VStack {
            Picker("Model", selection: $viewModel.selectedModelName) {
                Text("Robot").tag("robot")
                Text("Chair").tag("chair")
                Text("Lamp").tag("lamp")
            }
            .pickerStyle(.segmented)

            Slider(
                value: $viewModel.modelScale,
                in: 0.001...0.05,
                step: 0.001
            ) {
                Text("Scale")
            }
        }
        .padding()
        .background(.ultraThinMaterial)
        .clipShape(.rect(cornerRadius: 16))
        .padding()
    }
}
```

### Entity Accessibility

Make AR content accessible to assistive technologies:

```swift
let model = ModelEntity(
    mesh: .generateBox(size: 0.1),
    materials: [SimpleMaterial(color: .blue, isMetallic: false)]
)
var accessibility = AccessibilityComponent()
accessibility.isAccessibilityElement = true
accessibility.label = "Blue cube"
accessibility.value = "Interactive 3D object"
accessibility.traits = [.button]
accessibility.systemActions = [.activate]
model.components.set(accessibility)
```

## Performance Tips

### Entity Pooling

Reuse entities instead of creating and destroying them repeatedly:

```swift
@MainActor
final class EntityPool {
    private var available: [ModelEntity] = []
    private let mesh: MeshResource
    private let materials: [any Material]

    init(mesh: MeshResource, materials: [any Material], initialCount: Int) {
        self.mesh = mesh
        self.materials = materials
        for _ in 0..<initialCount {
            let entity = ModelEntity(mesh: mesh, materials: materials)
            entity.isEnabled = false
            available.append(entity)
        }
    }

    func acquire() -> ModelEntity {
        if let entity = available.popLast() {
            entity.isEnabled = true
            return entity
        }
        return ModelEntity(mesh: mesh, materials: materials)
    }

    func release(_ entity: ModelEntity) {
        entity.isEnabled = false
        entity.removeFromParent()
        available.append(entity)
    }
}
```

### Reducing Draw Calls

- Merge static entities into a single entity when possible
- Use instancing for repeated identical geometry
- Limit the number of unique materials in a scene
- Use LOD (level of detail) models for objects at varying distances

### Memory Management

- Unload entities that are no longer visible
- Use `ModelEntity(named:in:)` with a specific bundle to control resource loading
- Monitor memory with Instruments (RealityKit Trace template)
- Set `entity.isEnabled = false` instead of removing entities you will reuse
