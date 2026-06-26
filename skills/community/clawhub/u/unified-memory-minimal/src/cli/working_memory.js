/**
 * cli/working_memory.js - CLI Commands for Working Memory
 * 
 * Usage:
 *   node cli/index.js working --start "task description"
 *   node cli/index.js working --list
 *   node cli/index.js working --hold <id>
 *   node cli/index.js working --resume <id>
 *   node cli/index.js working --clear <id>
 *   node cli/index.js working --extend <id> --duration 3600000
 *   node cli/index.js working --tree
 */

import { parseArgs } from 'util';
import {
  create,
  hold,
  resume,
  clear,
  extend,
  getActive,
  get,
} from '../working_memory_manager.js';
import {
  visualizeTaskTree,
  getDescendants,
  getAncestry,
} from '../task_hierarchy.js';

/**
 * Main entry point for working memory CLI
 * Accepts args object from CLI (extracts subcommand from args._ or args.command)
 * @param {object} args - CLI args (can include command in various forms)
 */
export async function cmdWorkingMemory(args) {
  // Extract subcommand from various possible locations
  // Allow: memory working start "task"
  //        memory working --start "task"
  //        memory working --list
  let command = args.command || args._?.[0];
  
  // Map flag-based commands
  if (args.start) command = 'start';
  else if (args.list) command = 'list';
  else if (args.hold) command = 'hold';
  else if (args.resume) command = 'resume';
  else if (args.clear) command = 'clear';
  else if (args.extend) command = 'extend';
  else if (args.tree) command = 'tree';
  else if (args.get) command = 'get';
  
  // Default to list if no subcommand
  if (!command) command = 'list';

  switch (command) {
    case 'start':
      return cmdStart(args);
    case 'list':
      return cmdList(args);
    case 'hold':
      return cmdHold(args);
    case 'resume':
      return cmdResume(args);
    case 'clear':
      return cmdClear(args);
    case 'extend':
      return cmdExtend(args);
    case 'tree':
      return cmdTree(args);
    case 'get':
      return cmdGet(args);
    default:
      console.log(`Unknown working memory command: ${command}`);
      return cmdHelp();
  }
}

async function cmdStart(args) {
  const task = args._[0] || args.task || args.t;
  if (!task) {
    console.log('Usage: memory working --start "task description" [--context "details"] [--ttl 7200000]');
    return;
  }

  const result = create({
    taskDescription: task,
    contextWindow: args.context || '',
    ttlMs: args.ttl ? parseInt(args.ttl) : null,
    taskId: args.taskId || args.id || null,
  });

  if (result.success) {
    const wm = result.workingMemory;
    console.log(`\n✅ Working memory created:`);
    console.log(`   ID: ${wm.id}`);
    console.log(`   Task: ${wm.description}`);
    console.log(`   Status: ${wm.status}`);
    console.log(`   Expires: ${wm.expiresAt}`);
    if (result.archived) {
      console.log(`   ⚠️ Note: Oldest working memory auto-archived (max limit: 5)`);
    }
  } else {
    console.log(`❌ Failed: ${result.error}`);
  }
}

async function cmdList(args) {
  const { active, held, counts } = getActive();

  console.log(`\n🧠 Working Memories (Active: ${counts.active}/${counts.maxActive}, Held: ${counts.held})\n`);

  if (active.length === 0 && held.length === 0) {
    console.log('   No active working memories.\n');
    return;
  }

  for (const wm of active) {
    const remainingMin = Math.round(wm.remainingMs / 60000);
    console.log(`● [ACTIVE] ${wm.description}`);
    console.log(`  ID: ${wm.id} | Expires in: ${remainingMin}min`);
    if (wm.contextWindow) {
      console.log(`  Context: ${wm.contextWindow.slice(0, 60)}...`);
    }
    console.log('');
  }

  for (const wm of held) {
    console.log(`○ [HELD] ${wm.description}`);
    console.log(`  ID: ${wm.id}`);
    console.log('');
  }
}

async function cmdHold(args) {
  const id = args._[0] || args.id || args.i;
  if (!id) {
    console.log('Usage: memory working --hold <id>');
    return;
  }

  const result = hold(id);
  if (result.success) {
    console.log(`\n⏸️ Working memory held: ${result.workingMemory.description}`);
  } else {
    console.log(`❌ Failed: ${result.error}`);
  }
}

async function cmdResume(args) {
  const id = args._[0] || args.id || args.i;
  if (!id) {
    console.log('Usage: memory working --resume <id> [--duration 3600000]');
    return;
  }

  const durationMs = args.duration ? parseInt(args.duration) : null;
  const result = resume(id, durationMs);

  if (result.success) {
    console.log(`\n▶️ Working memory resumed: ${result.workingMemory.description}`);
  } else {
    console.log(`❌ Failed: ${result.error}`);
  }
}

async function cmdClear(args) {
  const id = args._[0] || args.id || args.i;
  if (!id) {
    console.log('Usage: memory working --clear <id>');
    return;
  }

  const reason = args.reason || 'cli_clear';
  const result = clear(id, reason);

  if (result.success) {
    console.log(`\n✅ Working memory cleared: ${result.workingMemory.description}`);
  } else {
    console.log(`❌ Failed: ${result.error}`);
  }
}

async function cmdExtend(args) {
  const id = args._[0] || args.id || args.i;
  const duration = args._[1] || args.duration || args.d;

  if (!id || !duration) {
    console.log('Usage: memory working --extend <id> --duration <ms>');
    console.log('Example: --duration 3600000 (1 hour)');
    return;
  }

  const durationMs = parseInt(duration);
  const result = extend(id, durationMs);

  if (result.success) {
    const extendedMin = Math.round(durationMs / 60000);
    console.log(`\n⏰ Extended by ${extendedMin}min: ${result.workingMemory.description}`);
    console.log(`   New expiry: ${result.workingMemory.expiresAt}`);
  } else {
    console.log(`❌ Failed: ${result.error}`);
  }
}

async function cmdTree(args) {
  const id = args._[0] || args.id || null;

  if (id) {
    const ancestry = getAncestry(id);
    const descendants = getDescendants(id);

    console.log(`\n📋 Task Tree for ${id}\n`);
    console.log(`Ancestry (${ancestry.length} levels):`);
    for (const wm of ancestry) {
      console.log(`  › ${wm.taskId}: ${wm.description}`);
    }
    console.log(`\nSubtasks (${descendants.length}):`);
    for (const wm of descendants) {
      console.log(`  › ${wm.taskId}: ${wm.description}`);
    }
    return;
  }

  const tree = visualizeTaskTree();
  console.log(`\n${tree}\n`);
}

async function cmdGet(args) {
  const id = args._[0] || args.id || args.i;
  if (!id) {
    console.log('Usage: memory working --get <id>');
    return;
  }

  const wm = get(id);
  if (!wm) {
    console.log(`\n❌ Working memory not found: ${id}`);
    return;
  }

  const remainingMin = Math.round(wm.remainingMs / 60000);
  console.log(`\n🧠 Working Memory:`);
  console.log(`   ID: ${wm.id}`);
  console.log(`   Task: ${wm.description}`);
  console.log(`   Status: ${wm.status}`);
  console.log(`   Created: ${wm.createdAt}`);
  console.log(`   Expires: in ${remainingMin}min`);
  if (wm.contextWindow) {
    console.log(`   Context: ${wm.contextWindow}`);
  }
  if (wm.episodeId) {
    console.log(`   Episode: ${wm.episodeId}`);
  }
  if (wm.parentTaskId) {
    console.log(`   Parent: ${wm.parentTaskId}`);
  }
  if (wm.subtaskCount > 0) {
    console.log(`   Subtasks: ${wm.subtaskCount}`);
  }
}

function cmdHelp() {
  console.log(`
🧠 Working Memory CLI

Usage: memory working <command> [options]

Commands:
  --start "task"     Create a new working memory
  --list             List all active working memories
  --hold <id>        Hold (pause) a working memory
  --resume <id>      Resume a held working memory
  --clear <id>       Clear a working memory
  --extend <id>      Extend TTL (requires --duration)
  --tree [id]        Show task hierarchy
  --get <id>         Get working memory details

Options:
  --context "text"   Context/details for the task
  --duration <ms>    Duration in milliseconds (e.g., 3600000)
  --ttl <ms>         Custom TTL in milliseconds
  --reason "text"    Reason for clearing

Examples:
  memory working --start "Implementing login feature"
  memory working --list
  memory working --hold wm_abc123
  memory working --extend wm_abc123 --duration 3600000
`);
}

export default cmdWorkingMemory;
