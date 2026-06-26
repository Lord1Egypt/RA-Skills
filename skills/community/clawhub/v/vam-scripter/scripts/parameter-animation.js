// VAM Scripter Example: Parameter-Driven Animation
// Shows how to use scripter parameters in animations

import { scripter, scene, Time } from "vam-scripter";

// Get references
const person = scene.getAtom("Person");
const head = person.getController("head");

// Declare parameters
const speedParam = scripter.declareFloatParam({
    name: "Wave Speed",
    default: 1.0,
    min: 0.1,
    max: 5.0,
    onChange: (value) => {
        console.log("Speed changed to:", value);
    }
});

const amplitudeParam = scripter.declareFloatParam({
    name: "Wave Amplitude",
    default: 0.1,
    min: 0.01,
    max: 0.5,
    onChange: (value) => {
        console.log("Amplitude changed to:", value);
    }
});

// Store initial rotation
let baseRotation = head.transform.rotation;

// Run every frame
scripter.onUpdate(() => {
    // Calculate rotation using parameters
    const yRotation = Math.sin(Time.time * speedParam.value) * amplitudeParam.value;
    
    // Apply rotation
    head.transform.rotation = {
        x: baseRotation.x,
        y: baseRotation.y + yRotation,
        z: baseRotation.z,
        w: baseRotation.w
    };
});