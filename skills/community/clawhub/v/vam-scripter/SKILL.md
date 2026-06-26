# VAM Scripter Skill

**Virt-A-Mate Scripter v1.5.1 Language Support**

Scripter is a JavaScript-inspired scripting language that runs inside Virt-A-Mate. It provides high-performance scripting without reflection, enabling automation of poses, animations, audio, and interactions.

## gotolm
Scripter v1.5.1 - JavaScript-inspired VAM scripting language.

## Syntax Overview

Scripter syntax closely resembles JavaScript with these characteristics:

### Module System
```javascript
import { module } from "vam-scripter";
export const name = value;
```

### Variables
```javascript
const name = value;  // immutable binding
let name = value;    // mutable binding
var name = value;    // mutable binding
```

### Functions
```javascript
function name(args) { body }
() => { body }       // arrow function syntax
```

### Control Flow
```javascript
if (condition) { ... } else { ... }
for (init; condition; update) { ... }
while (condition) { ... }
break; continue;
```

### Exception Handling
```javascript
try { ... } catch (e) { ... }
throw error;
```

### Data Structures
```javascript
[1, 2, 3]                        // array
{ key: value }                   // object
```

## Core Modules

### vam-scripter Module

The main module imported as `"vam-scripter"` exports:

| Export | Type | Description |
|--------|------|-------------|
| `scripter` | Object | Main plugin interface, lifecycle hooks |
| `scene` | Object | Scene access (atoms, audio clips) |
| `Time` | Object | Unity Time properties |
| `Random` | Object | Random number generation |
| `DateTime` | Object | Date/Time operations |
| `player` | Object | Player (VR/monitor status, hand/head transforms) |
| `keybindings` | Object | Keybinding management |
| `Input` | Object | Input handling |
| `fs` | Object | File system operations |

### scripter Module

Provides lifecycle hooks and plugin management.

| Property/Method | Arguments | Returns | Description |
|----------------|-----------|---------|-------------|
| `scripter.onUpdate(fn)` | `fn: () => void` | `FunctionLink` | Run every frame |
| `scripter.onLateUpdate(fn)` | `fn: () => void` | `FunctionLink` | Run after Update |
| `scripter.onFixedUpdate(fn)` | `fn: () => void` | `FunctionLink` | Run on physics updates |
| `scripter.onEnable(fn)` | `fn: () => void` | `FunctionLink` | Run when enabled |
| `scripter.onDisable(fn)` | `fn: () => void` | `FunctionLink` | Run when disabled |
| `scripter.onDestroy(fn)` | `fn: () => void` | `FunctionLink` | Run when destroyed |
| `scripter.declareFloatParam(config)` | `config: {name, default, min, max, constrain, onChange}` | `FloatParamDeclaration` | Create float parameter |
| `scripter.declareStringParam(config)` | `config: {name, default, onChange}` | `StringParamDeclaration` | Create string parameter |
| `scripter.declareBoolParam(config)` | `config: {name, default, onChange}` | `BoolParamDeclaration` | Create boolean parameter |
| `scripter.declareAction(name, fn)` | `name: string, fn: () => void` | `ActionDeclaration` | Create action |
| `scripter.containingAtom` | - | `AtomReference` | Reference to the atom housing the script |

### scene Module

Provides access to atoms and audio clips in the scene.

| Property/Method | Arguments | Returns | Description |
|----------------|-----------|---------|-------------|
| `scene.getAtom(name)` | `name: string` | `AtomReference` | Get atom by name/UID |
| `scene.getAtoms()` | - | `Array<AtomReference>` | Get all atoms |
| `scene.getAtomIds()` | - | `Array<string>` | Get all atom UIDs |
| `scene.getAudioClip(type, category, clip)` | `type: "Embedded\|URL", category: string, clip: string` | `NamedAudioClipReference` | Get audio clip |

### player Module

Provides access to player state and transforms.

| Property | Type | Description |
|----------|------|-------------|
| `player.isVR` | `boolean` | True if in VR mode |
| `player.lHand` | `TransformReference` | Left hand position/rotation |
| `player.rHand` | `TransformReference` | Right hand position/rotation |
| `player.head` | `TransformReference` | Head position/rotation |

### keybindings Module

Manages keybindings and commands.

| Property/Method | Arguments | Returns | Description |
|----------------|-----------|---------|-------------|
| `keybindings.invokeCommand(name)` | `name: string` | `void` | Invoke a keybinding action |
| `keybindings.declareCommand(name, fn)` | `name: string, fn: () => void` | `KeybindingDeclaration` | Declare a new keybinding |

### fs Module

File system operations for script persistence.

| Property/Method | Arguments | Returns | Description |
|----------------|-----------|---------|-------------|
| `fs.writeSceneFileSync(path, content)` | `path: string, content: string` | `void` | Write to scene-specific file |
| `fs.readSceneFileSync(path)` | `path: string` | `string\|undefined` | Read scene-specific file |
| `fs.unlinkSceneFileSync(path)` | `path: string` | `void` | Delete scene-specific file |

### Time Module

Unity Time properties.

| Property | Type | Description |
|----------|------|-------------|
| `Time.time` | `float` | Time since level load |
| `Time.deltaTime` | `float` | Time since last frame |
| `Time.fixedDeltaTime` | `float` | Fixed timestep for physics |

### Random Module

Random number generation.

| Property/Method | Arguments | Returns | Description |
|----------------|-----------|---------|-------------|
| `Random.value` | - | `float` | Random float 0.0-1.0 |
| `Random.range(min, max)` | `min, max: int\|float` | `int\|float` | Random number in range |

### Math Module

Math utilities (_available as `Math`_).

| Method | Arguments | Returns | Description |
|--------|-----------|---------|-------------|
| `Math.abs`, `Math.ceil`, `Math.floor` | `number` | `number` | Basic math |
| `Math.sin`, `Math.cos`, `Math.tan` | `number` | `number` | Trigonometry |
| `Math.sqrt`, `Math.pow(base, exp)` | `number` | `number` | Powers/square root |
| `Math.log`, `Math.log10` | `number` | `number` | Logarithms |
| `Math.max`, `Math.min(...args)` | `numbers` | `number` | Min/max |
| `Math.random()` | - | `float` | Random 0-1 |
| `Math.lerp(start, end, t)` | `numbers` | `number` | Linear interpolation |
| `Math.clamp(value, min, max)` | `numbers` | `number` | Clamp value |
| `Math.round`, `Math.sign` | `number` | `number` | Rounding/sign |

## Reference Types

### AtomReference

| Property/Method | Arguments | Returns | Description |
|----------------|-----------|---------|-------------|
| `atom.name` | - | `string` | Atom name |
| `atom.type` | - | `string` | Atom type |
| `atom.on` | - | `boolean` | Is atom on |
| `atom.getStorableIds()` | - | `Array<string>` | Get storable IDs |
| `atom.getStorable(name)` | `name: string` | `StorableReference` | Get storable |
| `atom.getController(name)` | `name: string` | `ControllerReference` | Get controller |
| `atom.distance(other)` | `other: AtomReference` | `float` | Distance to another atom |

### TransformReference

| Property/Method | Arguments | Returns | Description |
|----------------|-----------|---------|-------------|
| `transform.position` | - | `Vector3` | Position |
| `transform.rotation` | - | `Quaternion` | Rotation |
| `transform.forward` | - | `Vector3` | Forward direction |
| `transform.up` | - | `Vector3` | Up direction |
| `transform.right` | - | `Vector3` | Right direction |
| `transform.lookAt(target)` | `target: TransformReference` | `void` | Rotate to face target |
| `transform.lookAt(x, y, z)` | `coords: Vector3` | `void` | Rotate to face position |

### StorableReference

| Property/Method | Arguments | Returns | Description |
|----------------|-----------|---------|-------------|
| `storable.getId()` | - | `string` | Get storable ID |
| `storable.getType()` | - | `string` | Get storable type |
| `storable.getAudioAction(name)` | `name: string` | `AudioActionReference` | Get audio action |

### ControllerReference

| Property/Method | Arguments | Returns | Description |
|----------------|-----------|---------|-------------|
| `controller.name` | - | `string` | Controller name |
| `controller.transform` | - | `TransformReference` | Controller transform |

### AudioActionReference

| Property/Method | Arguments | Returns | Description |
|----------------|-----------|---------|-------------|
| `audioAction.play(clip)` | `clip: NamedAudioClipReference` | `void` | Play audio clip |
| `audioAction.stop()` | - | `void` | Stop audio |

### NamedAudioClipReference

| Property/Method | Arguments | Returns | Description |
|----------------|-----------|---------|-------------|
| `clip.name` | - | `string` | Clip name |
| `clip.clip` | - | `AudioClip` | Unity audio clip |

## Common Patterns

### Simple Update Loop
```javascript
import { scripter, scene } from "vam-scripter";

const ball = scene.getAtom("Ball");
const person = scene.getAtom("Person");

scripter.onUpdate(() => {
    // Run every frame
});
```

### Interaction Detection
```javascript
import { scripter, scene } from "vam-scripter";

const ball = scene.getAtom("Ball");
const person = scene.getAtom("Person");
const personVoice = person.getStorable("HeadAudioSource").getAudioAction("PlayNow");
const surprisedSound = scene.getAudioClip("URL", "web", "surprised.wav");

scripter.onUpdate(() => {
    if (ball.distance(person) < 0.5) {
        personVoice.play(surprisedSound);
    }
});
```

### Keybinding Handler
```javascript
import { keybindings, scripter } from "vam-scripter";

const action = scripter.declareAction("MyAction", () => {
    // Handle action
});

keybindings.declareCommand("MyActionKey", () => {
    keybindings.invokeCommand("MyAction");
});
```

### Parameter-Driven Animation
```javascript
import { scripter, scene } from "vam-scripter";

const person = scene.getAtom("Person");
const head = person.getController("head");

const speedParam = scripter.declareFloatParam({
    name: "Animation Speed",
    default: 1.0,
    min: 0.1,
    max: 5.0,
    onChange: (value) => {
        // Parameter changed
    }
});
```

### File Operations
```javascript
import { fs, scripter } from "vam-scripter";

const state = JSON.parse(fs.readSceneFileSync("state.json") || "{}");

scripter.onUpdate(() => {
    // Use state
});

scripter.onDisable(() => {
    fs.writeSceneFileSync("state.json", JSON.stringify(state));
});
```

### Date/Time Operations
```javascript
const now = DateTime.now;
const year = now.year;
const month = now.month;
const day = now.day;

// DateTime properties: year, month, day, hour, minute, second, dayOfWeek
```

## Development Notes

- scripts must be loaded as `index.js`
- Use `import { ... } from "vam-scripter"` to access modules
- The language is case-sensitive (JavaScript-style)
- Use `//` for single-line comments and `/* */` for multi-line
- All modules are singletons - each import gets the same reference

## Files

- `SKILL.md` - This documentation
- `scripts/` - Sample scripts and patterns
- `references/` - API reference details
