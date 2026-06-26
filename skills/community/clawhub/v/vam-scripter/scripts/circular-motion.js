// VAM Scripter Example: Circular Motion
// Demonstrates using Math and Time for animation

import { scripter, scene, Math, Time } from "vam-scripter";

// Get reference to the object we'll animate
const objectToAnimate = scene.getAtom("Object");
const centerObject = scene.getAtom("Center");

// Configuration
const rotationRadius = 2.0;
const rotationSpeed = 1.0;

// Run every frame
scripter.onUpdate(() => {
    // Calculate angle based on time and speed
    const angle = Time.time * rotationSpeed;
    
    // Calculate position on circle
    const x = Math.cos(angle) * rotationRadius;
    const z = Math.sin(angle) * rotationRadius;
    
    // Set position
    objectToAnimate.transform.position = {
        x: centerObject.transform.position.x + x,
        y: centerObject.transform.position.y,
        z: centerObject.transform.position.z + z
    };
    
    // Make object face the center
    objectToAnimate.transform.lookAt(centerObject.transform);
});