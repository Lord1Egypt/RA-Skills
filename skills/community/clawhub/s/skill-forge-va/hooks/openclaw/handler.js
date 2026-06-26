// Skill Creator Hook Handler

const REMINDER_INTERVAL = 10; // minutes
const REMINDERS = {
  sessionStart: "Remember to follow skill creation best practices from skill-creator",
  postToolUse: "Check skill structure and documentation quality",
  error: "Use skill-creator check to identify and fix issues"
};

// Session start handler
function onSessionStart(session) {
  console.log(REMINDERS.sessionStart);
  // Schedule periodic reminders
  setInterval(() => {
    console.log(REMINDERS.postToolUse);
  }, REMINDER_INTERVAL * 60 * 1000);
}

// Post tool use handler
function onPostToolUse(toolResult) {
  if (toolResult.error) {
    console.log(REMINDERS.error);
  }
  // Check if skill creation command was used
  if (toolResult.command && toolResult.command.includes('skill-creator')) {
    console.log("Skill creation command detected. Remember to run quality check.");
  }
}

// Export handlers
module.exports = {
  onSessionStart,
  onPostToolUse
};