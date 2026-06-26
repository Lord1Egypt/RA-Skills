import { api } from "../api";

interface AbandonOptions {
  json?: boolean;
}

export async function abandonCommand(taskId: string, options: AbandonOptions): Promise<void> {
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
      process.exit(1);
    }

    const { task, projectId } = found;

    const result = await api.updateTask({
      id: task.id,
      projectId: projectId,
      status: -1,
    });

    if (options.json) {
      console.log(JSON.stringify(result, null, 2));
      return;
    }

    console.log(`✓ Abandoned: "${task.title}"`);
  } catch (error) {
    console.error(`❌ Error: ${error instanceof Error ? error.message : String(error)}`);
    process.exit(1);
  }
}
