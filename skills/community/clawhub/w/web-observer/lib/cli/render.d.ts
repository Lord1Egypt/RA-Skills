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
export type Streams = {
    out: (text: string) => void;
    err: (text: string) => void;
};
/** The real streams, used by the built entry point. */
export declare const processStreams: Streams;
/** Collects output instead of writing it, for tests. */
export declare function captureStreams(): Streams & {
    stdout: () => string;
    stderr: () => string;
};
/** Write one line to stdout. */
export declare function line(streams: Streams, text?: string): void;
/** Write one line to stderr. */
export declare function note(streams: Streams, text: string): void;
/**
 * Lay out a table with aligned columns.
 *
 * @param headers Column headings.
 * @param rows One array of cells per row. A cell is rendered as given.
 * @returns The table as lines, headings first, then a rule, then the rows.
 */
export declare function table(headers: readonly string[], rows: readonly (readonly string[])[]): string[];
