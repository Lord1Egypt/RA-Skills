import { api } from "../api";

interface CompleteOptions {
  json?: boolean;
}

export async function completeCommand(taskId: string, options: CompleteOptions): Promise<void> {
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

    await api.completeTask(projectId, task.id);

    if (options.json) {
      console.log(
        JSON.stringify(
          {
            success: true,
            task: {
              id: task.id,
              title: task.title,
              projectId: projectId,
              status: "completed",
            },
          },
          null,
          2
        )
      );
      return;
    }

    console.log(`✓ Completed: "${task.title}"`);
  } catch (error) {
    console.error(`❌ Error: ${error instanceof Error ? error.message : String(error)}`);
    process.exit(1);
  }
}
