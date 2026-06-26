// VAM Scripter Example: State Persistence
// Saves and loads state across sessions

import { fs, scripter } from "vam-scripter";

// Initialize or load state
const statePath = "app-state.json";
const defaultState = {
    clickCount: 0,
    lastOpened: "unknown",
    settings: {
        volume: 50,
        enabled: true
    }
};

// Load existing state or use defaults
let appState;
const savedState = fs.readSceneFileSync(statePath);

if (savedState === undefined) {
    console.log("No saved state found, using defaults");
    appState = JSON.parse(JSON.stringify(defaultState));
} else {
    try {
        appState = JSON.parse(savedState);
        console.log("State loaded:", JSON.stringify(appState));
    } catch (e) {
        console.log("Failed to load state:", e.message);
        appState = JSON.parse(JSON.stringify(defaultState));
    }
}

// Update last opened time
appState.lastOpened = new Date().toISOString();

// Declare an action to increment counter
scripter.declareAction("Increment Counter", () => {
    appState.clickCount++;
    console.log(`Click count: ${appState.clickCount}`);
    saveState();
});

// Declare a toggle
const enabledParam = scripter.declareBoolParam({
    name: "Feature Enabled",
    default: appState.settings.enabled,
    onChange: (value) => {
        appState.settings.enabled = value;
        console.log(`Feature enabled: ${value}`);
        saveState();
    }
});

// Declare a volume slider
const volumeParam = scripter.declareFloatParam({
    name: "Volume Level",
    default: appState.settings.volume,
    min: 0,
    max: 100,
    onChange: (value) => {
        appState.settings.volume = value;
        console.log(`Volume: ${value}`);
        saveState();
    }
});

// Save state to file
function saveState() {
    try {
        fs.writeSceneFileSync(statePath, JSON.stringify(appState, null, 2));
        console.log("State saved");
    } catch (e) {
        console.log("Failed to save state:", e.message);
    }
}

// Cleanup on disable
scripter.onDisable(() => {
    saveState();
    console.log("Plugin disabled, state saved");
});