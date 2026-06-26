/**
 * StoryTime — Interactive Fiction Engine
 * @author @TheShadowRose
 * @license MIT
 */
const fs = require('fs');

class StoryTime {
  constructor(options = {}) {
    this.saveFile = options.saveFile || './story-save.json';
    this.state = { scene: 'start', history: [], inventory: [], stats: { choices: 0 } };
  }

  loadScenario(scenario) {
    this.scenario = scenario;
    this.state = { scene: 'start', history: [], inventory: scenario.startInventory || [], stats: { choices: 0 } };
    return this.getCurrentScene();
  }

  getCurrentScene() {
    const scene = this.scenario.scenes[this.state.scene];
    if (!scene) return { error: 'Scene not found: ' + this.state.scene };
    return {
      text: scene.text,
      choices: (scene.choices || []).map((c, i) => ({ id: i + 1, text: c.text })),
      inventory: this.state.inventory,
      sceneId: this.state.scene
    };
  }

  choose(choiceId) {
    const scene = this.scenario.scenes[this.state.scene];
    if (!scene || !scene.choices) return { error: 'No choices available' };
    const choice = scene.choices[choiceId - 1];
    if (!choice) return { error: 'Invalid choice' };

    this.state.history.push({ scene: this.state.scene, choice: choiceId });
    this.state.stats.choices++;

    if (choice.addItem) this.state.inventory.push(choice.addItem);
    if (choice.removeItem) this.state.inventory = this.state.inventory.filter(i => i !== choice.removeItem);

    this.state.scene = choice.goto || 'end';
    return this.getCurrentScene();
  }

  save() { fs.writeFileSync(this.saveFile, JSON.stringify({ state: this.state, scenario: this.scenario }, null, 2)); return true; }
  load() {
    try {
      const saved = JSON.parse(fs.readFileSync(this.saveFile, 'utf8'));
      if (saved.scenario) this.scenario = saved.scenario;
      this.state = saved.state || saved;
      if (!this.scenario) return { error: 'No scenario loaded. Call loadScenario() first.' };
      return this.getCurrentScene();
    } catch { return { error: 'No save found' }; }
  }
}

// Example scenario
StoryTime.EXAMPLE_SCENARIO = {
  title: "The Ancient Library",
  genre: "fantasy",
  startInventory: ["torch"],
  scenes: {
    start: {
      text: "You stand at the entrance of an ancient library. Dust motes float in shafts of light from cracked windows. A spiral staircase descends into darkness. Ahead, rows of shelves stretch into shadow. A faint humming comes from above.",
      choices: [
        { text: "Descend the spiral staircase", goto: "basement" },
        { text: "Explore the shelves", goto: "shelves" },
        { text: "Follow the humming upward", goto: "attic" }
      ]
    },
    basement: {
      text: "The staircase winds down into cool darkness. Your torch reveals stone walls covered in strange symbols. At the bottom, a heavy iron door stands ajar. Beyond it, you hear dripping water.",
      choices: [
        { text: "Push through the iron door", goto: "vault" },
        { text: "Study the symbols on the walls", goto: "symbols", addItem: "symbol knowledge" },
        { text: "Go back up", goto: "start" }
      ]
    },
    shelves: {
      text: "You move between towering shelves. The books here are old — leather bindings cracked, pages yellowed. One book on a reading stand is open, its pages glowing faintly blue. Another shelf holds glass jars with something moving inside.",
      choices: [
        { text: "Read the glowing book", goto: "glowing_book", addItem: "blue spell" },
        { text: "Examine the glass jars", goto: "jars" },
        { text: "Keep walking deeper", goto: "deep_library" }
      ]
    },
    attic: { text: "You climb creaking stairs to the attic. The humming grows louder. A crystal orb floats in the center of the room, pulsing with light. It seems to be calling to you.", choices: [{ text: "Touch the orb", goto: "end_good" }, { text: "Back away", goto: "start" }] },
    end_good: { text: "The orb fills you with ancient knowledge. You are now the library's guardian. Congratulations!", choices: [] },
    vault: { text: "A treasure vault! Gold coins and ancient artifacts fill the room. But the door is closing behind you...", choices: [{ text: "Grab what you can and run", goto: "end_good" }, { text: "Look for another exit", goto: "end_good" }] },
    symbols: { text: "The symbols are a map of the library's hidden rooms. You've gained valuable knowledge.", choices: [{ text: "Continue down", goto: "vault" }, { text: "Go back up", goto: "start" }] },
    glowing_book: { text: "The book teaches you a spell of illumination. The library's secrets begin to reveal themselves.", choices: [{ text: "Continue exploring", goto: "deep_library" }] },
    jars: { text: "The jars contain tiny elementals — fire, water, earth, air. They gesture excitedly at you.", choices: [{ text: "Free them", goto: "end_good" }, { text: "Leave them", goto: "deep_library" }] },
    deep_library: { text: "Deep in the library, you find a door marked 'Restricted'. It requires a key... or perhaps knowledge.", choices: [{ text: "Try to open it", goto: "end_good" }] }
  }
};

module.exports = { StoryTime };
