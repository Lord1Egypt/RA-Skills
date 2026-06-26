/**
 * Curated database of startup accelerators, fellowships, and incubators.
 *
 * Data lives in src/data/programs.json — hand-maintained, ships with npm.
 * Deadline status is computed at runtime by comparing dates to today.
 */

import programsData from "../data/programs.json" with { type: "json" };

// --- Types ---

export type ProgramType = "accelerator" | "fellowship" | "incubator" | "community";

export interface Deadline {
  batch: string;
  opens?: string;
  closes?: string;
  status?: "upcoming" | "open" | "closed";
  notes?: string;
}

export interface Program {
  slug: string;
  name: string;
  organization?: string;
  type: ProgramType;
  tier: 1 | 2 | 3;

  investment?: string;
  equity?: string;
  duration?: string;

  cycle: "cohort" | "rolling" | "annual";
  deadlines: Deadline[];
  applicationUrl?: string;

  description: string;
  focus?: string[];
  stage?: string[];
  location?: string;
  remote?: boolean;

  website: string;

  lastVerified: string;
  notes?: string;
}

// --- Load & Enrich ---

function computeDeadlineStatus(d: Deadline): Deadline["status"] {
  const today = new Date().toISOString().slice(0, 10);
  if (d.closes && d.closes < today) return "closed";
  if (d.opens && d.opens > today) return "upcoming";
  if (!d.closes) return "open"; // rolling
  return "open";
}

function enrichProgram(p: Program): Program {
  return {
    ...p,
    deadlines: p.deadlines.map((d) => ({
      ...d,
      status: computeDeadlineStatus(d),
    })),
  };
}

/** Load all programs with computed deadline statuses. */
export function loadPrograms(): Program[] {
  return (programsData as unknown as Program[]).map(enrichProgram);
}

// --- Query Functions ---

export interface FilterOptions {
  type?: ProgramType;
  stage?: string;
  focus?: string;
  tier?: number;
}

/** Filter programs by type, stage, focus area, or tier. */
export function filterPrograms(programs: Program[], opts: FilterOptions): Program[] {
  let result = programs;

  if (opts.type) {
    result = result.filter((p) => p.type === opts.type);
  }
  if (opts.tier) {
    result = result.filter((p) => p.tier === opts.tier);
  }
  if (opts.stage) {
    const s = opts.stage.toLowerCase();
    result = result.filter(
      (p) => p.stage?.some((st) => st.toLowerCase().includes(s)),
    );
  }
  if (opts.focus) {
    const f = opts.focus.toLowerCase();
    result = result.filter(
      (p) => p.focus?.some((fc) => fc.toLowerCase().includes(f)),
    );
  }

  return result;
}

/** Get all upcoming/open deadlines across all programs, sorted by close date. */
export function getUpcomingDeadlines(
  programs: Program[],
): Array<{ program: Program; deadline: Deadline }> {
  const results: Array<{ program: Program; deadline: Deadline }> = [];

  for (const p of programs) {
    for (const d of p.deadlines) {
      if (d.status === "open" || d.status === "upcoming") {
        results.push({ program: p, deadline: d });
      }
    }
  }

  return results.sort((a, b) => {
    const aDate = a.deadline.closes || "9999-12-31";
    const bDate = b.deadline.closes || "9999-12-31";
    return aDate.localeCompare(bDate);
  });
}

/** Search programs by name, description, focus, or slug. */
export function searchPrograms(programs: Program[], query: string): Program[] {
  const q = query.toLowerCase();
  return programs.filter(
    (p) =>
      p.name.toLowerCase().includes(q) ||
      p.slug.toLowerCase().includes(q) ||
      p.description.toLowerCase().includes(q) ||
      p.organization?.toLowerCase().includes(q) ||
      p.focus?.some((f) => f.toLowerCase().includes(q)) ||
      p.stage?.some((s) => s.toLowerCase().includes(q)),
  );
}
