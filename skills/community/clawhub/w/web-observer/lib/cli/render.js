/**
 * Output: where it goes, and how a table is laid out.
 *
 * Streams are injected everywhere rather than written to directly, so a test can
 * assert on exactly what a scheduled run would have delivered. That matters more
 * here than in most tools: on a scheduled run, stdout **is** the message sent to
 * the user, so a stray line is a notification.
 *
 * The division is strict. Anything a person is meant to read goes to stdout only
 * when it is the answer. Diagnostics, warnings and progress go to stderr. A
 * scheduled run holds them back and, when it succeeds, writes them to the run log
 * instead (see runlog.ts), because OpenClaw delivers stderr alongside stdout.
 */
/** The real streams, used by the built entry point. */
export const processStreams = {
    out: (text) => process.stdout.write(text),
    err: (text) => process.stderr.write(text),
};
/** Collects output instead of writing it, for tests. */
export function captureStreams() {
    const out = [];
    const err = [];
    return {
        out: (text) => out.push(text),
        err: (text) => err.push(text),
        stdout: () => out.join(""),
        stderr: () => err.join(""),
    };
}
/** Write one line to stdout. */
export function line(streams, text = "") {
    streams.out(`${text}\n`);
}
/** Write one line to stderr. */
export function note(streams, text) {
    streams.err(`${text}\n`);
}
/**
 * Lay out a table with aligned columns.
 *
 * @param headers Column headings.
 * @param rows One array of cells per row. A cell is rendered as given.
 * @returns The table as lines, headings first, then a rule, then the rows.
 */
export function table(headers, rows) {
    const widths = headers.map((header, column) => Math.max(header.length, ...rows.map((row) => (row[column] ?? "").length)));
    const render = (cells) => cells
        .map((cell, column) => cell.padEnd(widths[column] ?? 0))
        .join("  ")
        .trimEnd();
    return [render(headers), render(widths.map((width) => "-".repeat(width))), ...rows.map(render)];
}
