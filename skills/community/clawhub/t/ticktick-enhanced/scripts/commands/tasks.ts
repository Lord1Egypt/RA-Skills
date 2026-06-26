import { api, PRIORITY_REVERSE, type Task } from "../api";

interface TaskWithProject extends Task {
  projectName?: string;
}

interface TasksOptions {
  list?: string;
  status?: "pending" | "completed";
  due?: "today" | "overdue" | "none" | "unspecified";
  priority?: "high" | "medium" | "low" | "none";
  sort?: "due" | "priority" | "title" | "created";
  limit?: number;
  offset?: number;
  group?: boolean;
  format?: "plain" | "rich" | "json" | "yaml";
  verbose?: boolean;
  json?: boolean; // legacy alias for format=json
  focus?: "today" | "overdue" | "upcoming";
}

// Color utilities for rich output
const colors = {
  reset: "\x1b[0m",
  red: "\x1b[31m",
  yellow: "\x1b[33m",
  magenta: "\x1b[35m",
  cyan: "\x1b[36m",
  dim: "\x1b[2m",
  bold: "\x1b[1m",
};

function colorize(text: string, color: keyof typeof colors): string {
  if (process.env.NO_COLOR || !color) return text;
  return `${colors[color]}${text}${colors.reset}`;
}

function formatDueDate(dateStr: string): string {
  const date = new Date(dateStr);
  const now = new Date();
  const tomorrow = new Date(now);
  tomorrow.setDate(tomorrow.getDate() + 1);

  if (date.toDateString() === now.toDateString()) return "today";
  if (date.toDateString() === tomorrow.toDateString()) return "tomorrow";
  return date.toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

function formatTask(task: TaskWithProject, showProject = false, format: TasksOptions["format"] = "plain"): string {
  const isCompleted = task.status === 2;
  const status = isCompleted ? colorize("✓", "green") : colorize("○", "cyan");
  const priorityMap: Record<number, {label: string; color: keyof typeof colors}> = {
    5: {label: "!!!", color: "magenta"},
    3: {label: "!!", color: "yellow"},
    1: {label: "!", color: "cyan"},
    0: {label: "", color: "reset"},
  };
  const pri = priorityMap[task.priority ?? 0] ?? {label: "", color: "reset"};
  const priorityStr = task.priority ? colorize(pri.label, pri.color) : "";

  const dueStr = (() => {
    if (!task.dueDate) return "";
    const formatted = formatDueDate(task.dueDate);
    const isOverdue = new Date(task.dueDate) < new Date() && !isCompleted;
    const color = isOverdue ? "red" : isCompleted ? "dim" : "yellow";
    return ` ${colorize(`due ${formatted}`, color)}`;
  })();

  const projectPart = showProject && task.projectName ? colorize(` (${task.projectName})`, "cyan") : "";
  const idPart = colorize(`[${task.id.slice(0, 8)}]`, "dim");

  const titleColor = isCompleted ? "dim" : "reset";
  const title = colorize(task.title, titleColor);

  return `${status} ${idPart} ${priorityStr}${title}${projectPart}${dueStr}`;
}

function isToday(dateStr: string): boolean {
  const date = new Date(dateStr);
  const today = new Date();
  return date.toDateString() === today.toDateString();
}

function isOverdue(dateStr: string): boolean {
  const date = new Date(dateStr);
  return date < new Date();
}

export async function tasksCommand(options: TasksOptions): Promise<void> {
  try {
    const projects = await api.listProjects();
    const projectMap = new Map(projects.map((p) => [p.id, p.name]));

    let searchProjects = projects;
    if (options.list) {
      const project = await api.findProjectByName(options.list);
      if (!project) {
        console.error(`❌ Project not found: ${options.list}`);
        process.exit(1);
      }
      searchProjects = [project];
    }

    // Fetch all tasks from selected projects
    const tasksWithProjects: TaskWithProject[] = [];
    for (const project of searchProjects) {
      try {
        const data = await api.getProjectData(project.id);
        if (data.tasks) {
          for (const task of data.tasks) {
            tasksWithProjects.push({
              ...task,
              projectName: projectMap.get(task.projectId) || task.projectId,
            });
          }
        }
      } catch (err) {
        if (options.verbose) console.error(`Warning: Could not fetch project ${project.name}: ${err}`);
        continue;
      }
    }

    // Apply filters
    let filtered = tasksWithProjects;

    if (options.status === "pending") {
      filtered = filtered.filter((t) => t.status !== 2);
    } else if (options.status === "completed") {
      filtered = filtered.filter((t) => t.status === 2);
    }

    if (options.due === "today") {
      filtered = filtered.filter((t) => t.dueDate && isToday(t.dueDate));
    } else if (options.due === "overdue") {
      filtered = filtered.filter((t) => t.dueDate && isOverdue(t.dueDate) && t.status !== 2);
    } else if (options.due === "none") {
      filtered = filtered.filter((t) => !t.dueDate);
    } else if (options.due === "unspecified") {
      filtered = filtered.filter((t) => !t.dueDate || t.dueDate === "");
    }

    if (options.priority === "high") {
      filtered = filtered.filter((t) => t.priority === 5);
    } else if (options.priority === "medium") {
      filtered = filtered.filter((t) => t.priority === 3);
    } else if (options.priority === "low") {
      filtered = filtered.filter((t) => t.priority === 1);
    } else if (options.priority === "none") {
      filtered = filtered.filter((t) => t.priority === 0 || t.priority === undefined);
    }

    // Focus mode
    if (options.focus) {
      const now = new Date();
      const weekFromNow = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000);
      if (options.focus === "today") {
        filtered = filtered.filter((t) => t.dueDate && isToday(t.dueDate));
      } else if (options.focus === "overdue") {
        filtered = filtered.filter((t) => t.dueDate && isOverdue(t.dueDate) && t.status !== 2);
      } else if (options.focus === "upcoming") {
        filtered = filtered.filter((t) => t.dueDate && (() => {
            const d = new Date(t.dueDate);
            return d >= now && d <= weekFromNow;
          })());
      }
    }

    // Sorting
    const sortField = options.sort || (options.status !== "completed" ? "due" : "created");
    filtered.sort((a, b) => {
      // Completed tasks sort by modified desc by default
      if (sortField === "created" || sortField === "modified") {
        const dateA = new Date(a[sortField as keyof Task] as string || a.modifiedTime).getTime();
        const dateB = new Date(b[sortField as keyof Task] as string || b.modifiedTime).getTime();
        return dateB - dateA; // newest first
      }
      if (sortField === "due") {
        const aDue = a.dueDate ? new Date(a.dueDate).getTime() : Infinity;
        const bDue = b.dueDate ? new Date(b.dueDate).getTime() : Infinity;
        // Incomplete tasks: overdue first, then nearest due
        if (a.status !== 2 && b.status !== 2) {
          return aDue - bDue;
        }
        return 0;
      }
      if (sortField === "priority") {
        return (b.priority || 0) - (a.priority || 0);
      }
      if (sortField === "title") {
        return (a.title || "").localeCompare(b.title || "");
      }
      return 0;
    });

    // Pagination
    if (options.offset && options.offset > 0) {
      filtered = filtered.slice(Number(options.offset));
    }
    if (options.limit && options.limit > 0) {
      filtered = filtered.slice(0, Number(options.limit));
    }

    // JSON output
    if (options.json || options.format === "json") {
      console.log(JSON.stringify(filtered, null, 2));
      return;
    }

    if (options.format === "yaml") {
      console.log(require('js-yaml').dump(filtered));
      return;
    }

    if (filtered.length === 0) {
      console.log("No tasks found matching filters.");
      return;
    }

    // Grouped output
    if (options.group && !options.list) {
      const groups = new Map<string, TaskWithProject[]>();
      for (const task of filtered) {
        const proj = task.projectName || "Unknown";
        if (!groups.has(proj)) groups.set(proj, []);
        groups.get(proj)!.push(task);
      }

      console.log(`\nTasks (${filtered.length}) grouped by project:\n`);
      for (const [proj, tasks] of Array.from(groups.entries()).sort((a, b) => a[0].localeCompare(b[0]))) {
        console.log(colorize(`:: ${proj} (${tasks.length})`, "bold"));
        for (const task of tasks) {
          console.log("  " + formatTask(task, false, options.format));
        }
        console.log();
      }
      return;
    }

    // Plain/rich list
    const showProject = !!options.list;
    console.log(`\nTasks (${filtered.length}):\n`);
    for (const task of filtered) {
      console.log(formatTask(task, showProject, options.format));
    }

    // Pagination notice
    if ((options.limit && options.limit < tasksWithProjects.length) || options.offset) {
      const shown = filtered.length;
      const total = tasksWithProjects.length;
      console.log(colorize(`\n  ...showing ${shown} of ${total} tasks`, "dim"));
    }

  } catch (error) {
    console.error(`❌ Error: ${error instanceof Error ? error.message : String(error)}`);
    if (options.verbose && error instanceof Error && error.stack) {
      console.error(error.stack);
    }
    process.exit(1);
  }
}
