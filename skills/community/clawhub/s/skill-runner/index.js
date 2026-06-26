import { fileURLToPath } from 'url';
import path from 'path';
import fs from 'fs';

// Helper to get skill path relative to workspace
function getSkillPath(skillName) {
  return path.join('/home/bosunjung/.openclaw/workspace/skills', skillName, 'index.js');
}

// Main skill entry point
export async function skill(args, context) {
  const message = args.message; // Message from cron or another agent (e.g., "run memory-enhancer")

  if (!message || typeof message !== 'string' || !message.startsWith('run ')) {
    console.warn('[Skill Runner] Invalid message format. Expected "run <skill-name>".');
    return { status: 'error', reason: 'invalid_message_format' };
  }

  const skillToRun = message.substring(4).trim(); // Extract "memory-enhancer"
  const skillFilePath = getSkillPath(skillToRun);

  if (!fs.existsSync(skillFilePath)) {
    console.error(`[Skill Runner] Target skill "${skillToRun}" not found at ${skillFilePath}.`);
    return { status: 'error', reason: 'skill_not_found', skill: skillToRun };
  }

  try {
    // Dynamically import the target skill's module
    // Note: 'fileURLToPath' is needed for dynamic imports of local files
    const skillModule = await import(fileURLToPath(`file://${skillFilePath}`));

    if (typeof skillModule.skill !== 'function') {
      console.error(`[Skill Runner] Target skill "${skillToRun}" does not export a 'skill' function.`);
      return { status: 'error', reason: 'invalid_skill_export', skill: skillToRun };
    }

    console.log(`[Skill Runner] Executing target skill "${skillToRun}"...`);
    // Execute the target skill's 'skill' function, passing our context
    const result = await skillModule.skill(args, context);
    console.log(`[Skill Runner] Target skill "${skillToRun}" completed. Result:`, result);
    return { status: 'completed', skill: skillToRun, result: result };

  } catch (error) {
    console.error(`[Skill Runner] Error executing target skill "${skillToRun}":`, error);
    return { status: 'error', reason: 'skill_execution_failed', skill: skillToRun, error: error.message };
  }
}