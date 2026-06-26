import { api } from "../api";

interface DetailsOptions {
  json?: boolean;
  verbose?: boolean;
}

function formatDate(dateStr: string): string {
  const date = new Date(dateStr);
  return date.toLocaleString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
    timeZoneName: "short",
  });
}

function priorityLabel(p: number): string {
  const map: Record<number, string> = {0: "none", 1: "low", 3: "medium", 5: "high"};
  return map[p] ?? "unknown";
}

export async function detailsCommand(taskId: string, options: DetailsOptions): Promise<void> {
  try {
    if (!/^[a-f0-9]{24}$/i.test(taskId)) {
      console.error(`❌ Invalid task ID: ${taskId}`);
      console.error(`   Task ID must be a 24-character hex string.`);
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

    if (options.json) {
      console.log(JSON.stringify({ task, projectId }, null, 2));
      return;
    }

    console.log(`\n📄 Task Details\n${"=".repeat(40)}`);
    console.log(`Title:   ${task.title}`);
    console.log(`ID:      ${task.id}`);
    console.log(`Project: ${projectId}`);
    console.log(`Status:  ${task.status === 2 ? "✅ Completed" : task.status === -1 ? "🗑️ Abandoned" : "⏳ Pending"}`);

    if (task.priority !== undefined && task.priority !== 0) {
      console.log(`Priority: ${priorityLabel(task.priority)}`);
    }

    if (task.dueDate) {
      console.log(`Due:     ${formatDate(task.dueDate)}`);
    }

    if (task.tags && task.tags.length > 0) {
      console.log(`Tags:    ${task.tags.join(", ")}`);
    }

    if (task.content) {
      console.log(`\nDescription/Notes:`);
      console.log(`${"-".repeat(40)}`);
      console.log(task.content);
      console.log(`${"-".repeat(40)}`);
    }

    if (task.items && task.items.length > 0) {
      console.log(`\nChecklist Items:`);
      task.items.forEach((item: any, idx: number) => {
        const status = item.status === 2 ? "✅" : "⬜";
        console.log(`  ${idx + 1}. ${status} ${item.title}`);
      });
    }

    console.log(`\nCreated:  ${formatDate(task.createdTime)}`);
    console.log(`Modified: ${formatDate(task.modifiedTime)}`);

    if (options.verbose) {
      console.log(`\n[verbose] Full task object:`);
      console.log(JSON.stringify(task, null, 2));
    }
  } catch (error) {
    console.error(`❌ Error: ${error instanceof Error ? error.message : String(error)}`);
    if (options.verbose && error instanceof Error && error.stack) {
      console.error(error.stack);
    }
    process.exit(1);
  }
}
