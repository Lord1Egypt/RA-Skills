# VAM Scripter Module API Reference

## Module Export: `vam-scripter`

The `vam-scripter` module is the primary interface for Scripter scripts. It provides access to all major VAM functionality.

```javascript
import { scripter, scene, player, keybindings, fs, Time, Random, DateTime, Input, Math } from "vam-scripter";
```

## scripter - Plugin Lifecycle & Parameters

### Lifecycle Hooks

These methods register callback functions that execute at specific times in the plugin's lifecycle.

#### scripter.onUpdate(callback)

Registers a function to run every frame (Update phase).

```javascript
scripter.onUpdate(() => {
    // Runs once per frame
    // Use for animations, state checks
});
```

**Returns:** `FunctionLink` - Use to dispose the callback

**Example:**
```javascript
const onUpdateLink = scripter.onUpdate(() => {
    // Your code here
});

// To remove the callback:
onUpdateLink.dispose();
```

#### scripter.onLateUpdate(callback)

Registers a function to run after all Update callbacks complete.

```javascript
scripter.onLateUpdate(() => {
    // Runs after onUpdate
    // Use for post-processing
});
```

#### scripter.onFixedUpdate(callback)

Registers a function to run on physics updates (FixedUpdate phase).

```javascript
scripter.onFixedUpdate(() => {
    // Runs at fixed timestep
    // Use for physics calculations
});
```

#### scripter.onEnable(callback)

Registers a function to run when the plugin is enabled.

```javascript
scripter.onEnable(() => {
    // Plugin enabled
});
```

#### scripter.onDisable(callback)

Registers a function to run when the plugin is disabled.

```javascript
scripter.onDisable(() => {
    // Plugin disabled
});
```

#### scripter.onDestroy(callback)

Registers a function to run when the plugin is destroyed.

```javascript
scripter.onDestroy(() => {
    // Cleanup
});
```

### Parameter Declarations

These methods create editable parameters in the VAM UI.

#### scripter.declareFloatParam(config)

Creates a float slider parameter.

```javascript
const param = scripter.declareFloatParam({
    name: "Moving Speed",
    default: 1.0,
    min: 0.1,
    max: 5.0,
    constrain: true,
    onChange: (value) => {
        console.log("Speed changed to:", value);
    }
});

// Use the parameter value
const speed = param.value;
```

**Parameters:**
- `name: string` - Parameter display name
- `default: float` - Initial value
- `min: float` - Minimum value
- `max: float` - Maximum value
- `constrain: boolean` - Whether to constrain to min/max
- `onChange: function` - Optional callback when value changes

#### scripter.declareStringParam(config)

Creates a string input parameter.

```javascript
const param = scripter.declareStringParam({
    name: "Target Name",
    default: "Person",
    onChange: (value) => {
        console.log("Target is now:", value);
    }
});
```

#### scripter.declareBoolParam(config)

Creates a boolean (checkbox) parameter.

```javascript
const param = scripter.declareBoolParam({
    name: "Enable Animation",
    default: true,
    onChange: (value) => {
        console.log("Animation enabled:", value);
    }
});
```

#### scripter.declareAction(name, callback)

Creates an action button in the VAM UI.

```javascript
const action = scripter.declareAction("Trigger Animation", () => {
    // Action triggered
    console.log("Action clicked!");
});
```

### Properties

#### scripter.containingAtom

Reference to the atom that contains this script plugin.

```javascript
const atom = scripter.containingAtom;
console.log(atom.name);
console.log(atom.type);
```

## scene - Scene Access

#### scene.getAtom(name)

Retrieves an atom by name or UID.

```javascript
const person = scene.getAtom("Person");
const ball = scene.getAtom("Ball");
```

**Returns:** `AtomReference`

**Throws:** `ScripterPluginException` if atom not found

#### scene.getAtoms()

Retrieves all atoms in the scene.

```javascript
const allAtoms = scene.getAtoms();
for (const atom of allAtoms) {
    console.log(atom.name);
}
```

**Returns:** `Array<AtomReference>`

#### scene.getAtomIds()

Retrieves all atom UIDs in the scene.

```javascript
const ids = scene.getAtomIds();
// ["Person", "Ball", ...]
```

**Returns:** `Array<string>`

#### scene.getAudioClip(type, category, clip)

Retrieves an audio clip by type, category, and name.

```javascript
const sound = scene.getAudioClip("URL", "web", "surprised.wav");
const embedded = scene.getAudioClip("Embedded", "Human", "Scream");
```

**Parameters:**
- `type: "Embedded" | "URL"` - Clipsource type
- `category: string` - Category name
- `clip: string` - Clip name

**Returns:** `NamedAudioClipReference`

**Throws:** `ScripterRuntimeException` for invalid type or missing clip

## player - Player Information

Accesses player state and body part positions.

#### player.isVR

```javascript
if (player.isVR) {
    console.log("VR mode active");
}
```

**Returns:** `boolean`

#### player.lHand

Left hand transform reference.

```javascript
const leftHandPos = player.lHand.position;
const leftHandRot = player.lHand.rotation;
```

**Returns:** `TransformReference`

#### player.rHand

Right hand transform reference.

**Returns:** `TransformReference`

#### player.head

Head/center camera transform reference.

**Returns:** `TransformReference`

## keybindings - Keybinding Management

#### keybindings.invokeCommand(name)

Triggers a named keybinding action.

```javascript
keybindings.invokeCommand("SomeNamedAction");
```

#### keybindings.declareCommand(name, callback)

Declares a new keybinding that can be mapped by the user.

```javascript
keybindings.declareCommand("MyToggle", () => {
    // User pressed their mapped key
});
```

**Returns:** `KeybindingDeclaration`

## fs - File System Operations

Operations for reading and writing files within the Scripter directory.

#### fs.writeSceneFileSync(path, content)

Writes content to a file in the scene-specific Scripter directory.

```javascript
fs.writeSceneFileSync("state.json", JSON.stringify(state));
```

**Parameters:**
- `path: string` - File path (must end with .txt or .json)
- `content: string` - Content to write

**Throws:** `ScripterRuntimeException` for invalid paths

#### fs.readSceneFileSync(path)

Reads content from a file.

```javascript
const content = fs.readSceneFileSync("state.json");
if (content !== undefined) {
    const state = JSON.parse(content);
}
```

**Parameters:**
- `path: string` - File path

**Returns:** `string | undefined` - Content or undefined if not found

**Throws:** `ScripterRuntimeException` for invalid paths

#### fs.unlinkSceneFileSync(path)

Deletes a file.

```javascript
fs.unlinkSceneFileSync("state.json");
```

**Parameters:**
- `path: string` - File path

**Throws:** `ScripterRuntimeException` for invalid paths

## Time - Unity Time Properties

#### Time.time

Time since the level was loaded (in seconds).

```javascript
const elapsedTime = Time.time;
```

**Returns:** `float`

#### Time.deltaTime

Time in seconds it took to complete the last frame.

```javascript
const frameTime = Time.deltaTime;
```

**Returns:** `float`

#### Time.fixedDeltaTime

The interval in seconds at which physics will be processed.

```javascript
const physicsInterval = Time.fixedDeltaTime;
```

**Returns:** `float`

## Random - Random Number Generation

#### Random.value

A random number between 0.0 and 1.0 (inclusive).

```javascript
const rand = Random.value;
```

**Returns:** `float`

#### Random.range(min, max)

Returns a random number between min and max.

```javascript
const intRand = Random.range(0, 10);  // 0-10
const floatRand = Random.range(0.0, 1.0);  // 0.0-1.0
```

**Returns:** `int | float`

## DateTime - Date and Time

Accesses the current date and time.

```javascript
const now = DateTime.now;
console.log(now.year);
console.log(now.month);
console.log(now.day);
console.log(now.hour);
console.log(now.minute);
console.log(now.second);
console.log(now.dayOfWeek);
```

**Properties:**
- `year: int`
- `month: int` (1-12)
- `day: int` (1-31)
- `hour: int` (0-23)
- `minute: int` (0-59)
- `second: int` (0-59)
- `dayOfWeek: int` (0-6, Sunday=0)

## Math - Mathematical Functions

The Math object provides mathematical constants and functions.

### Trigonometry
- `Math.abs(number)` - Absolute value
- `Math.sin(number)` - Sine
- `Math.cos(number)` - Cosine
- `Math.tan(number)` - Tangent
- `Math.asin(number)` - Arcsine
- `Math.acos(number)` - Arccosine
- `Math.atan(number)` - Arctangent
- `Math.atan2(y, x)` - Arctangent of y/x

### Powers and Roots
- `Math.sqrt(number)` - Square root
- `Math.pow(base, exponent)` - Power
- `Math.exp(number)` - Exponential
- `Math.log(number)` - Natural logarithm
- `Math.log10(number)` - Base-10 logarithm

### Rounding
- `Math.ceil(number)` - Ceiling
- `Math.floor(number)` - Floor
- `Math.round(number)` - Round to nearest

### Sign and Value
- `Math.sign(number)` - Sign (-1, 0, or 1)
- `Math.abs(number)` - Absolute value

### Min/Max
- `Math.max(a, b, ...)` - Maximum value
- `Math.min(a, b, ...)` - Minimum value

### Interpolation
- `Math.lerp(start, end, t)` - Linear interpolation
- `Math.lerpAngle(start, end, t)` - Angle interpolation
- `Math.clamp(value, min, max)` - Clamp value
- `Math.clamp01(value)` - Clamp to 0-1
- `Math.inverseLerp(a, b, value)` - Inverse linear interpolation
- `Math.pingPong(t, length)` - Ping pong between 0 and length

### Constants
- `Math.random()` - Random 0-1 (same as `Random.value`)