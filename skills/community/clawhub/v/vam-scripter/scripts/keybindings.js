// VAM Scripter Example: Keybindings
// Demonstrates keybinding management

import { scripter, keybindings } from "vam-scripter";

// Create an action that can be assigned to a key
scripter.declareAction("Toggle Light", () => {
    console.log("Light toggled!");
    // Add your toggle logic here
});

scripter.declareAction("Play Sound", () => {
    console.log("Sound played!");
    // Add your sound logic here
});

scripter.declareAction("Reset Scene", () => {
    console.log("Scene reset!");
    // Add your reset logic here
});

// Declare keybindings that map to actions
keybindings.declareCommand("ToggleKey", () => {
    keybindings.invokeCommand("Toggle Light");
});

keybindings.declareCommand("SoundKey", () => {
    keybindings.invokeCommand("Play Sound");
});

keybindings.declareCommand("ResetKey", () => {
    keybindings.invokeCommand("Reset Scene");
});

console.log("Keybindings registered!");
console.log("Assignment: ToggleKey -> Toggle Light");
console.log("Assignment: SoundKey -> Play Sound");
console.log("Assignment: ResetKey -> Reset Scene");