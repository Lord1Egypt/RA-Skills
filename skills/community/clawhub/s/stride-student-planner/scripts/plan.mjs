import { readFileSync } from "node:fs";

const inputPath = process.argv[2] ?? "data/seed/student-state.json";
const data = JSON.parse(readFileSync(inputPath, "utf8"));

const format = new Intl.DateTimeFormat("en-US", {
  timeZone: data.timezone,
  weekday: "long",
  year: "numeric",
  month: "long",
  day: "numeric",
  hour: "numeric",
  minute: "2-digit",
  timeZoneName: "short"
});

const now = new Date();

const tasks = data.tasks
  .filter(task => task.status === "todo")
  .map(task => {
    const deadline = new Date(task.due_at);

    if (Number.isNaN(deadline.getTime())) {
      throw new Error(`Invalid deadline for ${task.id}`);
    }

    return {
      ...task,
      deadline_display: format.format(deadline),
      overdue: deadline.getTime() < now.getTime()
    };
  })
  .sort((a, b) => Date.parse(a.due_at) - Date.parse(b.due_at));

console.log(JSON.stringify({
  generated_at: now.toISOString(),
  current_time_display: format.format(now),
  timezone: data.timezone,
  tasks
}, null, 2));