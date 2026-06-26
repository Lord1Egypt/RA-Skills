import { createRootRoute, Outlet, useNavigate } from '@tanstack/react-router';
import { ConnectButton } from '@mysten/dapp-kit';
import { NavProvider, useNavContext } from '../lib/nav-context';

export const Route = createRootRoute({
  component: RootLayout,
});

function Logo({ onClick }: { onClick: () => void }) {
  return (
    <button onClick={onClick} style={{
      background: 'none',
      border: 'none',
      display: 'flex',
      alignItems: 'center',
      gap: 10,
      cursor: 'pointer',
      padding: 0,
    }}>
      <div style={{
        position: 'relative',
        width: 36,
        height: 36,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        borderRadius: 8,
        background: 'var(--walrus-mint-faint)',
        border: '1px solid var(--walrus-mint-dim)',
      }}>
        <img src="/shark-icon.png" alt="WALVIS" style={{ width: 28, height: 28, objectFit: 'contain' }} />
      </div>
      <div style={{
        fontFamily: 'var(--font-display)',
        fontWeight: 800,
        fontSize: 15,
        letterSpacing: '0.1em',
        color: 'var(--walrus-mint)',
        lineHeight: 1,
      }}>W.A.L.V.I.S.</div>
    </button>
  );
}

function CenterLabel() {
  const { centerLabel } = useNavContext();
  if (!centerLabel) return null;
  return (
    <span style={{
      fontFamily: 'var(--font-data)',
      fontSize: 11,
      letterSpacing: '0.15em',
      textTransform: 'uppercase',
      color: 'var(--text-muted)',
    }}>
      {centerLabel}
    </span>
  );
}

function RootLayout() {
  const navigate = useNavigate();

  return (
    <NavProvider>
      <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
        {/* Header */}
        <header style={{
          position: 'sticky',
          top: 0,
          zIndex: 100,
          background: 'rgba(8,14,27,0.88)',
          backdropFilter: 'blur(16px)',
          borderBottom: '1px solid var(--rim)',
          padding: '0 24px',
          height: 56,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: 20,
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 20 }}>
            <Logo onClick={() => navigate({ to: '/' })} />
            <button
              onClick={() => navigate({ to: '/about' })}
              style={{
                background: 'none',
                border: 'none',
                color: 'var(--text-dim)',
                fontSize: 11,
                letterSpacing: '0.12em',
                textTransform: 'uppercase',
                cursor: 'pointer',
                padding: '4px 0',
                transition: 'color 0.2s',
              }}
              onMouseEnter={(e) => e.currentTarget.style.color = 'var(--walrus-mint)'}
              onMouseLeave={(e) => e.currentTarget.style.color = 'var(--text-dim)'}
            >
              About
            </button>
          </div>

          <CenterLabel />

          <ConnectButton />
        </header>

        {/* Content */}
        <main style={{ flex: 1, padding: '32px 24px', maxWidth: 1200, margin: '0 auto', width: '100%' }}>
          <Outlet />
        </main>

        {/* Footer */}
        <footer style={{
          borderTop: '1px solid var(--rim)',
          padding: '16px 24px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          color: 'var(--text-dim)',
          fontSize: 10,
          letterSpacing: '0.12em',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <img src="/shark-icon.png" alt="WALVIS" style={{ width: 14, height: 14, objectFit: 'contain' }} />
            <span>W.A.L.V.I.S. // WALRUS TESTNET</span>
          </div>
          <a href="https://clawhub.ai/Kuuga-0/walvis" target="_blank" rel="noopener noreferrer" style={{ color: 'var(--text-dim)', transition: 'color 0.2s' }}>OPENCLAW SKILL v0.2.0</a>
        </footer>
      </div>
    </NavProvider>
  );
}
