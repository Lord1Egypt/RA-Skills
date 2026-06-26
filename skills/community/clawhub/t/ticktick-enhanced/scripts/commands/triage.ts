import { api } from "../api";

interface TriageOptions {
  urgent?: boolean;
  quickWins?: boolean;
  meetings?: boolean;
  highPriority?: boolean;
  all?: boolean;
  format?: "plain" | "rich" | "json";
  verbose?: boolean;
}

function isMeetingTask(title: string, content?: string): boolean {
  const text = (title + " " + (content || "")).toLowerCase();
  return /\b(meeting|call|sync|standup|zoom|teams|conference)\b/.test(text);
}

function isQuickWin(task: any): boolean {
  const title = task.title || "";
  const priority = task.priority || 0;
  const hasDue = !!task.dueDate;
  const content = (task.content || "").toLowerCase();

  if (title.length < 40 && priority <= 1 && !hasDue) return true;
  if (/\b(quick|review|check|5\s*min|ten\s*min|quickly)\b/.test(content)) return true;
  return false;
}

export async function triageCommand(options: TriageOptions): Promise<void> {
  try {
    // Fetch all pending tasks from all projects
    const projects = await api.listProjects();
    let allTasks: any[] = [];

    for (const project of projects) {
      try {
        const data = await api.getProjectData(project.id);
        if (data.tasks) {
          for (const task of data.tasks) {
            if (task.status !== 2) { // pending only
              allTasks.push({ ...task, projectName: project.name });
            }
          }
        }
      } catch (err) {
        if (options.verbose) console.error(`Warning: Could not fetch project ${project.name}: ${err}`);
      }
    }

    // Categorize
    const categories: Record<string, any[]> = {
      urgent: [],
      quickWins: [],
      meetings: [],
      highPriority: [],
      others: [],
    };

    const now = new Date();
    for (const task of allTasks) {
      const dueSoon = task.dueDate && new Date(task.dueDate) <= now;
      if (dueSoon) {
        categories.urgent.push(task);
      } else if (isQuickWin(task)) {
        categories.quickWins.push(task);
      } else if (isMeetingTask(task.title, task.content)) {
        categories.meetings.push(task);
      } else if (task.priority === 5) {
        categories.highPriority.push(task);
      } else {
        categories.others.push(task);
      }
    }

    // Determine which categories to display
    const showUrgent = options.urgent || options.all;
    const showQuick = options.quickWins || options.all;
    const showMeetings = options.meetings || options.all;
    const showHigh = options.highPriority || options.all;
    const showOthers = options.all;

    const fmt = options.format || "plain";

    if (fmt === "json") {
      console.log(JSON.stringify({ categories, total: allTasks.length }, null, 2));
      return;
    }

    // Plain/rich output
    let output = "\n📋 Task Triage\n" + "=".repeat(40) + `\nTotal pending: ${allTasks.length}\n`;

    function section(title: string, tasks: any[], key: string, emoji: string): string {
      if (tasks.length === 0) return "";
      const lines = [`${emoji} ${title} (${tasks.length})`];
      for (const t of tasks.slice(0, 10)) {
        const due = t.dueDate ? ` 📅 ${new Date(t.dueDate).toLocaleDateString('en-US', {month:'short', day:'numeric'})}` : '';
        const proj = t.projectName ? ` (${t.projectName})` : '';
        lines.push(`  - ${t.title}${due}${proj}`);
      }
      if (tasks.length > 10) lines.push(`  ...and ${tasks.length - 10} more`);
      return lines.join("\n") + "\n";
    }

    if (showUrgent) output += section("🔥 Urgent & Overdue", categories.urgent, "urgent", "🔥");
    if (showHigh) output += section("🎯 High Priority (no due)", categories.highPriority, "highPriority", "🎯");
    if (showQuick) output += section("⚡ Quick Wins", categories.quickWins, "quickWins", "⚡");
    if (showMeetings) output += section("📞 Meetings & Calls", categories.meetings, "meetings", "📞");
    if (showOthers && options.all) output += section("📦 Other Tasks", categories.others, "others", "📦");

    output += "\n---\nFocus: Start with one 🔥 task, then tackle at least 2 ⚡ quick wins.\n";
    console.log(output);

  } catch (error) {
    console.error(`❌ Error: ${error instanceof Error ? error.message : String(error)}`);
    if (options.verbose && error instanceof Error && error.stack) {
      console.error(error.stack);
    }
    process.exit(1);
  }
}
