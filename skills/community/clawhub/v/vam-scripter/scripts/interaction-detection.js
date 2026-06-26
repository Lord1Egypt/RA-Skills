// VAM Scripter Example: Interaction Detection
// Import the main module
import { scripter, scene } from "vam-scripter";

// Get references to objects we'll use
const ball = scene.getAtom("Ball");
const person = scene.getAtom("Person");

// Get the audio action we'll trigger
const personVoice = person.getStorable("HeadAudioSource").getAudioAction("PlayNow");

// Get a sound clip
const surprisedSound = scene.getAudioClip("URL", "web", "surprised.wav");

// Run this code every frame
scripter.onUpdate(() => {
    // Check if ball is within 0.5m of person
    if (ball.distance(person) < 0.5) {
        // Play the sound if collision detected
        personVoice.play(surprisedSound);
    }
});