import { api, PRIORITY_MAP, type UpdateTaskInput } from "../api";

interface EditOptions {
  title?: string;
  content?: string;
  due?: string;
  priority?: string;
  tags?: string[];
  json?: boolean;
  verbose?: boolean;
}

function parseDueDate(dueStr: string): string {
  const now = new Date();
  const lowerDue = dueStr.toLowerCase();

  const toEndOfDay = (d: Date): string => {
    d.setHours(23, 59, 59, 0);
    return d.toISOString().replace("Z", "+0000");
  };

  if (lowerDue === "today") return toEndOfDay(now);
  if (lowerDue === "tomorrow") {
    now.setDate(now.getDate() + 1);
    return toEndOfDay(now);
  }
  if (lowerDue.match(/^in (\d+) days?$/i)) {
    const match = lowerDue.match(/^in (\d+) days?$/i);
    if (match) {
      now.setDate(now.getDate() + parseInt(match[1], 10));
      return toEndOfDay(now);
    }
  }
  if (lowerDue.match(/^next (monday|tuesday|wednesday|thursday|friday|saturday|sunday)$/i)) {
    const match = lowerDue.match(/^next (monday|tuesday|wednesday|thursday|friday|saturday|sunday)$/i);
    if (match) {
      const days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"];
      const targetDay = days.indexOf(match[1].toLowerCase());
      const currentDay = now.getDay();
      let daysUntil = targetDay - currentDay;
      if (daysUntil <= 0) daysUntil += 7;
      now.setDate(now.getDate() + daysUntil);
      return toEndOfDay(now);
    }
  }

  const parsed = new Date(dueStr);
  if (!isNaN(parsed.getTime())) {
    return parsed.toISOString().replace("Z", "+0000");
  }

  throw new Error(`Invalid date format: ${dueStr}. Try 'today', 'tomorrow', 'in 3 days', or ISO date.`);
}

export async function editCommand(taskId: string, options: EditOptions): Promise<void> {
  try {
    // Require 24-char hex ID
    if (!/^[a-f0-9]{24}$/i.test(taskId)) {
      console.error(`❌ Invalid task ID: ${taskId}`);
      console.error(`   Task ID must be a 24-character hex string (e.g., 65a54fce2026ccc8b729349b)`);
      console.error(`   Obtain IDs from: /tasks --json`);
      process.exit(1);
    }

    const found = await api.findTaskById(taskId);

    if (!found) {
      console.error(`❌ Task not found with ID: ${taskId}`);
      console.error(`   Verify the ID is correct and the task exists.`);
      process.exit(1);
    }

    const { task, projectId } = found;
    const input: UpdateTaskInput = { id: task.id, projectId };

    let changedFields: string[] = [];

    if (options.title !== undefined) {
      input.title = options.title;
      changedFields.push("title");
    }
    if (options.content !== undefined) {
      input.content = options.content;
      changedFields.push("content");
    }
    if (options.due) {
      input.dueDate = parseDueDate(options.due);
      changedFields.push("due");
    }
    if (options.priority) {
      const priority = PRIORITY_MAP[options.priority.toLowerCase()];
      if (priority === undefined) {
        console.error(`❌ Invalid priority: ${options.priority}. Use none, low, medium, or high.`);
        process.exit(1);
      }
      input.priority = priority;
      changedFields.push("priority");
    }
    if (options.tags && options.tags.length > 0) {
      input.tags = options.tags;
      changedFields.push("tags");
    }

    if (Object.keys(input).length <= 2) {
      console.error("❌ No changes specified. Use --title, --content, --due, --priority, or --tags.");
      process.exit(1);
    }

    const updated = await api.updateTask(input);

    if (options.json) {
      console.log(JSON.stringify(updated, null, 2));
      return;
    }

    console.log(`✓ Task updated: "${updated.title}"`);
    console.log(`  ID: ${updated.id}`);
    if (changedFields.length > 0) {
      console.log(`  Changed: ${changedFields.join(", ")}`);
    }
    if (options.verbose) {
      console.log(`  Project: ${projectId}`);
      if (updated.dueDate) {
        console.log(`  Due: ${new Date(updated.dueDate).toLocaleDateString()}`);
      }
      if (updated.priority !== undefined) {
        const prioNames: Record<number, string> = {0: "none", 1: "low", 3: "medium", 5: "high"};
        console.log(`  Priority: ${prioNames[updated.priority] ?? updated.priority}`);
      }
    }
  } catch (error) {
    console.error(`❌ Error: ${error instanceof Error ? error.message : String(error)}`);
    if (options.verbose && error instanceof Error && error.stack) {
      console.error(error.stack);
    }
    process.exit(1);
  }
}
