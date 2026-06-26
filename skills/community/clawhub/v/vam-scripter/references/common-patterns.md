# VAM Scripter Common Patterns & Examples

This document provides实用 patterns and examples for common scripting scenarios in VAM Scripter.

## File Organization

Store scripts in `index.js` format:

```
Custom/Scripts/
  AcidBubbles/
    Scripter/
      script-name.js
```

Or import modules:
```javascript
import { scripter, scene } from "vam-scripter";
import { helper } from "./helpers.js";
```

## 1. Basic Update Loop

```javascript
import { scripter } from "vam-scripter";

scripter.onUpdate(() => {
    console.log("Running every frame");
});
```

## 2. Interaction Detection

```javascript
import { scripter, scene } from "vam-scripter";

const ball = scene.getAtom("Ball");
const person = scene.getAtom("Person");
const voice = person.getStorable("HeadAudioSource").getAudioAction("PlayNow");
const sound = scene.getAudioClip("URL", "web", "surprised.wav");

scripter.onUpdate(() => {
    if (ball.distance(person) < 0.5) {
        voice.play(sound);
    }
});
```

## 3. Parameter-Driven Animation

```javascript
import { scripter, scene } from "vam-scripter";

const ball = scene.getAtom("Ball");

const speed = scripter.declareFloatParam({
    name: "Animation Speed",
    default: 1.0,
    min: 0.1,
    max: 5.0
});

const direction = scripter.declareBoolParam({
    name: "Change Direction",
    default: false
});

scripter.onUpdate(() => {
    const currentSpeed = speed.value;
    const dir = direction.value ? 1 : -1;
    
    // Use params in your logic
    console.log(`Speed: ${currentSpeed}, Direction: ${dir}`);
});
```

## 4. Keybinding Management

```javascript
import { scripter, keybindings } from "vam-scripter";

// Create an action
const toggleAction = scripter.declareAction("Toggle Light", () => {
    console.log("Toggle action triggered!");
});

// Map it to a key
keybindings.declareCommand("ToggleKey", () => {
    keybindings.invokeCommand("Toggle Light");
});

// Or check if a key is pressed
scripter.onUpdate(() => {
    if (Input.GetKeyDown("space")) {
        console.log("Space pressed");
    }
});
```

## 5. State Persistence

```javascript
import { fs, scripter } from "vam-scripter";

// Load state on start
const state = JSON.parse(fs.readSceneFileSync("state.json") || "{}");

if (!state.counter) {
    state.counter = 0;
}

scripter.onUpdate(() => {
    // Use state
});

scripter.onDisable(() => {
    // Save state on disable
    fs.writeSceneFileSync("state.json", JSON.stringify(state));
});
```

## 6. Player Distance Checker

```javascript
import { scripter, scene, player } from "vam-scripter";

const target = scene.getAtom("Target");
constDetectionRadius = 2.0;

scripter.onUpdate(() => {
    const distance = target.distance(player.head);
    
    if (distance < detectionRadius) {
        console.log(`Target is close! ${distance.toFixed(2)}m`);
    }
});
```

## 7. Timed Events

```javascript
import { scripter, Time } from "vam-scripter";

let timer = 0;
const interval = 5.0; // 5 seconds

scripter.onUpdate(() => {
    timer += Time.deltaTime;
    
    if (timer >= interval) {
        timer = 0;
        console.log("Timer fired!");
    }
});
```

## 8. Random Behavior

```javascript
import { scripter, Random } from "vam-scripter";

scripter.onUpdate(() => {
    const rand = Random.value;
    
    if (rand < 0.1) {
        console.log("10% chance action");
    } else if (rand < 0.3) {
        console.log("20% chance action");
    }
});
```

## 9. Audio Trigger

```javascript
import { scripter, scene } from "vam-scripter";

const person = scene.getAtom("Person");
const voice = person.getStorable("HeadAudioSource").getAudioAction("PlayNow");
const sound = scene.getAudioClip("URL", "web", "surprised.wav");
let triggered = false;

scripter.onUpdate(() => {
    if (!triggered && someCondition()) {
        voice.play(sound);
        triggered = true;
    }
});
```

## 10. Multiple Atoms Loop

```javascript
import { scripter, scene } from "vam-scripter";

const ball = scene.getAtom("Ball");

scripter.onUpdate(() => {
    const atoms = scene.getAtoms();
    
    for (const atom of atoms) {
        if (atom.name !== ball.name) {
            const dist = atom.distance(ball);
            console.log(`${atom.name} is ${dist.toFixed(2)}m away`);
        }
    }
});
```

## 11. Date/Time Display

```javascript
import { DateTime } from "vam-scripter";

scripter.onUpdate(() => {
    const now = DateTime.now;
    const timeString = `${now.hour}:${now.minute.toString().padLeft(2, '0')}:${now.second.toString().padLeft(2, '0')}`;
    
    console.log(`Current time: ${timeString}`);
});
```

## 12. Math Operations

```javascript
import { scripter, scene, Math } from "vam-scripter";

const obj = scene.getAtom("Object");
const startScale = 1.0;
const maxScale = 5.0;

scripter.onUpdate(() => {
    const t = (Math.sin(Time.time) + 1) / 2; // 0 to 1
    const scale = Math.lerp(startScale, maxScale, t);
    
    // Apply scaling
    obj.transform.localScale = { x: scale, y: scale, z: scale };
});
```

## 13. Complex State Machine

```javascript
import { scripter, scene } from "vam-scripter";

const person = scene.getAtom("Person");
const voice = person.getStorable("HeadAudioSource").getAudioAction("PlayNow");
const sounds = {
    happy: scene.getAudioClip("URL", "web", "laugh.wav"),
    sad: scene.getAudioClip("URL", "web", "sad.wav"),
    surprised: scene.getAudioClip("URL", "web", "surprised.wav")
};

let state = "idle";
let timer = 0;

scripter.onUpdate(() => {
    timer += Time.deltaTime;
    
    switch (state) {
        case "idle":
            if (timer > 5) {
                state = "happy";
                voice.play(sounds.happy);
                timer = 0;
            }
            break;
        case "happy":
            if (timer > 3) {
                state = "idle";
                timer = 0;
            }
            break;
        case "sad":
            if (timer > 4) {
                state = "idle";
                timer = 0;
            }
            break;
    }
});
```

## 14. Input Monitoring

```javascript
import { scripter, Input } from "vam-scripter";

scripter.onUpdate(() => {
    if (Input.GetKeyDown("space")) {
        console.log("Space pressed");
    }
    
    if (Input.GetKey("shift")) {
        console.log("Shift held");
    }
    
    if (Input.GetKeyUp("space")) {
        console.log("Space released");
    }
});
```

## 15. Transform Manipulation

```javascript
import { scripter, scene, Math } from "vam-scripter";

const obj = scene.getAtom("Object");
const center = scene.getAtom("Center");

const radius = 2.0;
const speed = 1.0;

scripter.onUpdate(() => {
    const angle = Time.time * speed;
    const x = Math.cos(angle) * radius;
    const z = Math.sin(angle) * radius;
    
    obj.transform.position = {
        x: center.transform.position.x + x,
        y: center.transform.position.y,
        z: center.transform.position.z + z
    };
    
    obj.transform.lookAt(center.transform);
});
```

## 16. Event Debouncing

```javascript
import { scripter } from "vam-scripter";

let lastTriggerTime = 0;
const cooldown = 2.0;

function triggerAction() {
    const now = Time.time;
    
    if (now - lastTriggerTime > cooldown) {
        console.log("Action triggered!");
        lastTriggerTime = now;
    }
}

scripter.onUpdate(() => {
    if (someCondition()) {
        triggerAction();
    }
});
```

## 17. Animation with Parameters

```javascript
import { scripter, scene, Math } from "vam-scripter";

const person = scene.getAtom("Person");
const head = person.getController("head");

const amplitude = scripter.declareFloatParam({
    name: "Wave Amplitude",
    default: 0.1,
    min: 0.01,
    max: 0.5
});

const frequency = scripter.declareFloatParam({
    name: "Wave Frequency",
    default: 1.0,
    min: 0.1,
    max: 5.0
});

let baseRotation = head.transform.rotation;

scripter.onUpdate(() => {
    const yRotation = Math.sin(Time.time * frequency.value) * amplitude.value;
    
    head.transform.rotation = {
        x: baseRotation.x,
        y: baseRotation.y + yRotation,
        z: baseRotation.z,
        w: baseRotation.w
    };
});
```

## 18. Conditional Actions

```javascript
import { scripter, scene } from "vam-scripter";

const person = scene.getAtom("Person");
const voice = person.getStorable("HeadAudioSource").getAudioAction("PlayNow");
const sounds = {
    yes: scene.getAudioClip("Embedded", "Human", "Yes"),
    no: scene.getAudioClip("Embedded", "Human", "No")
};

let triggerCount = 0;

scripter.onUpdate(() => {
    if (someCondition()) {
        triggerCount++;
        
        if (triggerCount % 2 === 0) {
            voice.play(sounds.yes);
        } else {
            voice.play(sounds.no);
        }
    }
});
```

## 19. Performance Optimization

```javascript
import { scripter, scene } from "vam-scripter";

// Cache references
const person = scene.getAtom("Person");
const voice = person.getStorable("HeadAudioSource").getAudioAction("PlayNow");
const sound = scene.getAudioClip("URL", "web", "surprised.wav");

// Use flag to avoid expensive operations
let hasPlayed = false;

scripter.onUpdate(() => {
    if (someCondition() && !hasPlayed) {
        voice.play(sound);
        hasPlayed = true;
    }
    
    if (!someCondition()) {
        hasPlayed = false;
    }
});
```

## 20. Clear Cleanup Pattern

```javascript
import { scripter } from "vam-scripter";

const updates = [];
const lates = [];
const fixeds = [];

// Register callbacks
updates.push(scripter.onUpdate(() => { /* ... */ }));
updates.push(scripter.onUpdate(() => { /* ... */ }));

// Cleanup on disable
scripter.onDisable(() => {
    for (const link of updates) {
        link.dispose();
    }
    for (const link of lates) {
        link.dispose();
    }
    for (const link of fixeds) {
        link.dispose();
    }
});
```