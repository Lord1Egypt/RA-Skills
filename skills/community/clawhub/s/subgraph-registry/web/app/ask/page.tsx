import { AmpChat } from "./AmpChat";
import { Panel } from "@/components/Panel";
import { SUGGESTED_QUESTIONS } from "@/lib/ampSchema";

export const dynamic = "force-dynamic";

export default function AmpPage() {
  return (
    <>
      <header className="mb-6">
        <h1 className="text-3xl font-semibold tracking-tight text-ink sm:text-4xl">
          Ask <span className="text-accent">x402</span>
        </h1>
        <p className="mt-1 text-sm text-muted">
          Natural-language SQL over every x402 settlement event on Base
          (May 2025 → June 2026). Pre-baked answers are in the{" "}
          <a href="/" className="text-muted underline decoration-accent/40 underline-offset-2 hover:text-accent">
            Watch view
          </a>{" "}
          — this page is for the questions you didn&apos;t pre-encode.
        </p>
      </header>

      <Panel title="Conversation" caption="powered by DuckDB + parquet">
        <AmpChat suggestions={SUGGESTED_QUESTIONS} />
      </Panel>

      <p className="mt-4 text-center text-[11px] text-dim">
        Backend: DuckDB over a parquet dataset of Base x402 settlements
        (configured via <code className="font-mono text-muted">AMP_PARQUET_GLOB</code>).
      </p>
    </>
  );
}
