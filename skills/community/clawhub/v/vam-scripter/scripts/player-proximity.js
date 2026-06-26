// VAM Scripter Example: Player Proximity
// Reacts to player presence

import { scripter, scene, player, Time } from "vam-scripter";

// Get target object
const target = scene.getAtom("Target");
const nearSound = scene.getAudioClip("URL", "web", "close.wav");
const farSound = scene.getAudioClip("URL", "web", "far.wav");

// Get audio action
const voice = target.getStorable("HeadAudioSource").getAudioAction("PlayNow");

// Configuration
const nearDistance = 1.0;
const farDistance = 5.0;

let lastState = "unknown";
let timer = 0;

scripter.onUpdate(() => {
    // Get distance to player
    const distance = target.distance(player.head);
    
    // Determine state based on distance
    let currentState;
    
    if (distance < nearDistance) {
        currentState = "very_close";
    } else if (distance < farDistance) {
        currentState = "near";
    } else {
        currentState = "far";
    }
    
    // Trigger behavior based on state changes
    if (currentState !== lastState) {
        console.log(`State changed: ${lastState} -> ${currentState}`);
        
        switch (currentState) {
            case "very_close":
                voice.play(nearSound);
                timer = 0;
                break;
            case "near":
                voice.play(nearSound);
                break;
            case "far":
                voice.play(farSound);
                break;
        }
        
        lastState = currentState;
    }
    
    // Continuous timer when near
    if (currentState === "near") {
        timer += Time.deltaTime;
        if (timer > 3) {
            console.log("Player has been near for 3+ seconds");
        }
    }
});