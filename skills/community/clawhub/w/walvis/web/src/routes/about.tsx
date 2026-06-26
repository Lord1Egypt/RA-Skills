import { createFileRoute, useNavigate } from '@tanstack/react-router';

export const Route = createFileRoute('/about')({
  component: AboutPage,
});

function AboutPage() {
  const navigate = useNavigate();

  return (
    <div style={{
      position: 'relative',
      zIndex: 1,
      animation: 'float-up 0.7s ease forwards',
      maxWidth: 800,
      margin: '0 auto',
    }}>
      {/* Back button */}
      <button
        onClick={() => navigate({ to: '/' })}
        style={{
          background: 'none',
          border: 'none',
          color: 'var(--text-muted)',
          fontSize: 11,
          letterSpacing: '0.15em',
          cursor: 'pointer',
          marginBottom: 32,
          display: 'flex',
          alignItems: 'center',
          gap: 6,
        }}
      >
        ← Back
      </button>

      {/* Banner */}
      <div style={{ marginBottom: 40 }}>
        <img
          src="/shark-banner.png"
          alt="WALVIS Banner"
          style={{
            width: '100%',
            height: 'auto',
            borderRadius: 12,
            border: '1px solid var(--rim)',
            boxShadow: '0 8px 32px rgba(0,200,255,0.12)',
          }}
        />
      </div>

      {/* Title */}
      <h1 style={{
        fontFamily: 'var(--font-display)',
        fontWeight: 800,
        fontSize: 'clamp(32px, 6vw, 56px)',
        letterSpacing: '-0.02em',
        lineHeight: 1,
        background: 'linear-gradient(135deg, #fff 20%, var(--glow) 60%, #0066ff)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
        backgroundClip: 'text',
        marginBottom: 8,
      }}>
        W.A.L.V.I.S.
      </h1>
      <p style={{
        fontSize: 11,
        letterSpacing: '0.3em',
        textTransform: 'uppercase',
        color: 'var(--text-muted)',
        marginBottom: 40,
      }}>
        Walrus Autonomous Learning &amp; Vibe Intelligence System
      </p>

      {/* Vision */}
      <Section title="Vision">
        <p>
          WALVIS is your AI-powered knowledge vault that lives in Telegram.
          Send a link, a snippet of text, or an image — WALVIS analyzes, tags,
          and stores it on <Highlight>Walrus decentralized storage</Highlight>.
          Your knowledge is yours: censorship-resistant, always available, and
          browsable through a web UI hosted on Walrus Sites.
        </p>
        <p style={{ marginTop: 12 }}>
          Not just links — save anything. Articles, ideas, screenshots, references.
          WALVIS is your second brain on the decentralized web.
        </p>
      </Section>

      {/* How it works */}
      <Section title="How It Works">
        <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
          <Step number="1" title="Save">
            Send anything to <Code>/walvis</Code> in Telegram — links, text, or images.
            The AI analyzes content, generates a summary, and assigns tags automatically.
          </Step>
          <Step number="2" title="Organize">
            Group items into spaces (like folders). Search across everything with full-text search,
            or filter by tags. Edit tags and notes inline.
          </Step>
          <Step number="3" title="Sync">
            Run <Code>/walvis sync</Code> to upload your spaces to Walrus.
            Data is stored as decentralized blobs — no central server, no single point of failure.
          </Step>
          <Step number="4" title="Browse">
            Open the web UI on Walrus Sites, enter your manifest blob ID, and explore
            your entire knowledge vault from any device.
          </Step>
        </div>
      </Section>

      {/* Tech stack */}
      <Section title="Built With">
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
          gap: 12,
        }}>
          <StackCard name="Walrus" desc="Decentralized blob storage on Sui" />
          <StackCard name="Walrus Sites" desc="Static site hosting on-chain" />
          <StackCard name="OpenClaw" desc="AI agent framework for Telegram" />
          <StackCard name="Sui" desc="Wallet connect via @mysten/dapp-kit" />
          <StackCard name="React 19" desc="UI with TanStack Router + Vite" />
          <StackCard name="AI Tagging" desc="OpenAI-compatible LLM analysis" />
        </div>
      </Section>

      {/* Footer spacer */}
      <div style={{ height: 60 }} />
    </div>
  );
}

// --- Sub-components ---

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div style={{ marginBottom: 40 }}>
      <h2 style={{
        fontFamily: 'var(--font-display)',
        fontWeight: 700,
        fontSize: 20,
        letterSpacing: '-0.01em',
        color: 'var(--walrus-mint)',
        marginBottom: 16,
      }}>
        {title}
      </h2>
      <div style={{
        fontSize: 13,
        lineHeight: 1.8,
        color: 'var(--text-muted)',
      }}>
        {children}
      </div>
    </div>
  );
}

function Step({ number, title, children }: { number: string; title: string; children: React.ReactNode }) {
  return (
    <div style={{ display: 'flex', gap: 16, alignItems: 'flex-start' }}>
      <div style={{
        width: 32,
        height: 32,
        borderRadius: 8,
        background: 'var(--walrus-mint-faint)',
        border: '1px solid var(--walrus-mint-dim)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontFamily: 'var(--font-display)',
        fontWeight: 800,
        fontSize: 14,
        color: 'var(--walrus-mint)',
        flexShrink: 0,
      }}>
        {number}
      </div>
      <div>
        <div style={{
          fontFamily: 'var(--font-display)',
          fontWeight: 600,
          fontSize: 14,
          color: 'var(--text)',
          marginBottom: 4,
        }}>
          {title}
        </div>
        <div style={{ fontSize: 12, lineHeight: 1.7, color: 'var(--text-muted)' }}>
          {children}
        </div>
      </div>
    </div>
  );
}

function StackCard({ name, desc }: { name: string; desc: string }) {
  return (
    <div style={{
      padding: '14px 16px',
      background: 'var(--layer)',
      border: '1px solid var(--rim)',
      borderRadius: 8,
    }}>
      <div style={{
        fontFamily: 'var(--font-display)',
        fontWeight: 600,
        fontSize: 13,
        color: 'var(--text)',
        marginBottom: 4,
      }}>
        {name}
      </div>
      <div style={{
        fontSize: 11,
        color: 'var(--text-dim)',
        lineHeight: 1.4,
      }}>
        {desc}
      </div>
    </div>
  );
}

function Highlight({ children }: { children: React.ReactNode }) {
  return (
    <span style={{ color: 'var(--walrus-mint)' }}>{children}</span>
  );
}

function Code({ children }: { children: React.ReactNode }) {
  return (
    <code style={{
      color: 'var(--walrus-mint)',
      fontSize: 11,
      background: 'var(--walrus-mint-faint)',
      padding: '2px 6px',
      borderRadius: 3,
    }}>
      {children}
    </code>
  );
}
