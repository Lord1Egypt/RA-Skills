import { createFileRoute, useNavigate } from '@tanstack/react-router';
import { useState, useEffect, useCallback } from 'react';
import { fetchManifest, fetchAllSpaces, fetchLocalManifest, fetchAllLocalSpaces, searchItems, getAllTags, isLocalMode, getEncryptedSpaceIds } from '../lib/walrus';
import { fetchAndDecryptSpace } from '../lib/seal';
import type { Space, BookmarkItem, Manifest } from '../lib/types';
import { ItemCard } from '../components/ItemCard';
import { ItemDetailModal } from '../components/ItemDetailModal';
import { SpaceCard } from '../components/SpaceCard';
import { SearchBar } from '../components/SearchBar';
import { TagFilter } from '../components/TagFilter';
import { useNavContext } from '../lib/nav-context';
import { useCurrentAccount, useSignPersonalMessage } from '@mysten/dapp-kit';

export const Route = createFileRoute('/')({
  component: HomePage,
});

type ViewState =
  | { kind: 'landing' }
  | { kind: 'loading' }
  | { kind: 'error'; message: string }
  | { kind: 'loaded'; manifest: Manifest; spaces: Space[]; mode: 'local' | 'walrus' };

const PUBLIC_MANIFEST_PRESETS = [
  {
    label: 'Public test vault · no encryption',
    blobId: '6CaR9NjOllO98mMhC-wmCF7Nd0QNBjvmMU01YSLhwis',
  },
];

function DepthGrid() {
  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      zIndex: 0,
      overflow: 'hidden',
      pointerEvents: 'none',
    }}>
      {/* Radial depth gradient */}
      <div style={{
        position: 'absolute',
        inset: 0,
        background: 'radial-gradient(ellipse 80% 50% at 50% 100%, rgba(0,60,100,0.4) 0%, transparent 70%)',
      }} />
      {/* Top glow */}
      <div style={{
        position: 'absolute',
        top: -200,
        left: '50%',
        transform: 'translateX(-50%)',
        width: 600,
        height: 400,
        background: 'radial-gradient(ellipse, rgba(0,200,255,0.06) 0%, transparent 70%)',
        borderRadius: '50%',
      }} />
      {/* Grid lines */}
      <svg style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', opacity: 0.04 }}>
        <defs>
          <pattern id="grid" width="60" height="60" patternUnits="userSpaceOnUse">
            <path d="M 60 0 L 0 0 0 60" fill="none" stroke="#00c8ff" strokeWidth="0.5" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />
      </svg>
      {/* Banner background */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: '50%',
        transform: 'translateX(-50%)',
        width: '100%',
        maxWidth: 1200,
        height: '100%',
        backgroundImage: 'url(/shark-banner.png)',
        backgroundRepeat: 'no-repeat',
        backgroundPosition: 'center 56px',
        backgroundSize: 'contain',
        opacity: 0.07,
        maskImage: 'linear-gradient(to bottom, black 0%, transparent 60%)',
        WebkitMaskImage: 'linear-gradient(to bottom, black 0%, transparent 60%)',
      }} />
    </div>
  );
}

function LandingInput({ onLoad }: { onLoad: (blobId: string) => void }) {
  const [blobId, setBlobId] = useState('');
  const [focused, setFocused] = useState(false);
  const [copiedBlobId, setCopiedBlobId] = useState<string | null>(null);

  // Auto-load local data in dev mode
  useEffect(() => {
    if (isLocalMode) {
      onLoad('local');
    }
  }, [onLoad]);

  const copyPreset = async (nextBlobId: string) => {
    try {
      await navigator.clipboard.writeText(nextBlobId);
      setCopiedBlobId(nextBlobId);
      window.setTimeout(() => {
        setCopiedBlobId(current => current === nextBlobId ? null : current);
      }, 1600);
    } catch {
      setCopiedBlobId(null);
    }
  };

  return (
    <div style={{
      position: 'relative',
      zIndex: 1,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: 'calc(100vh - 120px)',
      gap: 48,
      animation: 'float-up 0.7s ease forwards',
    }}>
      {/* Title block */}
      <div style={{ textAlign: 'center' }}>
        <div style={{
          fontFamily: 'var(--font-display)',
          fontWeight: 800,
          fontSize: 'clamp(42px, 8vw, 80px)',
          letterSpacing: '-0.02em',
          lineHeight: 0.95,
          background: 'linear-gradient(135deg, #fff 20%, var(--glow) 60%, #0066ff)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
          marginBottom: 16,
        }}>
          W.A.L.V.I.S.
        </div>
        <p style={{
          fontSize: 12,
          letterSpacing: '0.3em',
          textTransform: 'uppercase',
          color: 'var(--text-muted)',
        }}>
          Walrus Autonomous Learning &amp; Vibe Intelligence System
        </p>
        <p style={{
          fontSize: 13,
          color: 'var(--text-dim)',
          marginTop: 12,
          fontFamily: 'var(--font-data)',
          maxWidth: 'min(92vw, 560px)',
          lineHeight: 1.6,
        }}>
          {isLocalMode ? (
            'Loading local data...'
          ) : (
            <>
              Your AI knowledge vault on Walrus — save anything,{' '}
              <span style={{ whiteSpace: 'nowrap' }}>find it anytime</span>
            </>
          )}
        </p>
      </div>

      {!isLocalMode && (
        <>
          {/* Input */}
          <div style={{
            width: '100%',
            maxWidth: 560,
            position: 'relative',
          }}>
            <div style={{
              display: 'flex',
              gap: 0,
              border: `1px solid ${focused ? 'var(--glow-dim)' : 'var(--rim)'}`,
              borderRadius: 6,
              overflow: 'hidden',
              background: 'var(--layer)',
              transition: 'border-color 0.2s',
              boxShadow: focused ? '0 0 0 3px var(--glow-faint), 0 0 40px rgba(0,200,255,0.05)' : 'none',
            }}>
              <span style={{
                padding: '12px 14px',
                color: 'var(--glow)',
                fontSize: 11,
                letterSpacing: '0.1em',
                borderRight: '1px solid var(--rim)',
                whiteSpace: 'nowrap',
                fontFamily: 'var(--font-data)',
                display: 'flex',
                alignItems: 'center',
              }}>
                BLOB_ID
              </span>
              <input
                type="text"
                value={blobId}
                onChange={e => setBlobId(e.target.value)}
                onFocus={() => setFocused(true)}
                onBlur={() => setFocused(false)}
                onKeyDown={e => e.key === 'Enter' && blobId.trim() && onLoad(blobId.trim())}
                placeholder="Enter manifest blob ID…"
                style={{
                  flex: 1,
                  background: 'transparent',
                  border: 'none',
                  outline: 'none',
                  padding: '12px 14px',
                  color: 'var(--text)',
                  fontFamily: 'var(--font-data)',
                  fontSize: 13,
                }}
              />
              <button
                onClick={() => blobId.trim() && onLoad(blobId.trim())}
                disabled={!blobId.trim()}
                style={{
                  background: blobId.trim() ? 'var(--glow)' : 'transparent',
                  border: 'none',
                  color: blobId.trim() ? '#000' : 'var(--text-dim)',
                  padding: '12px 20px',
                  fontSize: 11,
                  letterSpacing: '0.15em',
                  textTransform: 'uppercase',
                  fontFamily: 'var(--font-data)',
                  fontWeight: 500,
                  cursor: blobId.trim() ? 'pointer' : 'default',
                  transition: 'all 0.2s',
                  whiteSpace: 'nowrap',
                }}
              >
                Dive In →
              </button>
            </div>

            <p style={{
              marginTop: 10,
              fontSize: 11,
              color: 'var(--text-dim)',
              textAlign: 'center',
              letterSpacing: '0.1em',
            }}>
              Get your blob ID by running{' '}
              <code style={{ color: 'var(--glow)', fontSize: 10 }}>/walvis sync</code>
              {' '}in Telegram
            </p>

            <div style={{
              marginTop: 16,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: 8,
            }}>
              <div style={{
                fontSize: 10,
                letterSpacing: '0.18em',
                color: 'var(--text-dim)',
                textTransform: 'uppercase',
              }}>
                Copy a public test blob ID
              </div>
              <div style={{
                display: 'flex',
                flexDirection: 'column',
                gap: 10,
                width: '100%',
              }}>
                {PUBLIC_MANIFEST_PRESETS.map(preset => (
                  <div
                    key={preset.blobId}
                    style={{
                      padding: '12px 14px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      gap: 12,
                      background: 'var(--glow-faint)',
                      border: '1px solid var(--rim)',
                      borderRadius: 8,
                      maxWidth: '100%',
                    }}
                  >
                    <div style={{ minWidth: 0, textAlign: 'left' }}>
                      <div style={{
                        fontSize: 10,
                        letterSpacing: '0.12em',
                        color: 'var(--walrus-mint)',
                        textTransform: 'uppercase',
                        marginBottom: 4,
                      }}>
                        {preset.label}
                      </div>
                      <code style={{
                        fontSize: 11,
                        color: 'var(--text-muted)',
                        wordBreak: 'break-all',
                      }}>
                        {preset.blobId}
                      </code>
                    </div>
                    <button
                      type="button"
                      title={`Copy ${preset.blobId}`}
                      onClick={() => copyPreset(preset.blobId)}
                      style={{
                        minHeight: 40,
                        padding: '0 14px',
                        borderRadius: 6,
                        border: '1px solid var(--rim)',
                        background: copiedBlobId === preset.blobId ? 'var(--glow)' : 'var(--layer)',
                        color: copiedBlobId === preset.blobId ? '#000' : 'var(--text)',
                        fontSize: 11,
                        letterSpacing: '0.1em',
                        textTransform: 'uppercase',
                        fontFamily: 'var(--font-data)',
                        cursor: 'pointer',
                        whiteSpace: 'nowrap',
                        flexShrink: 0,
                      }}
                    >
                      {copiedBlobId === preset.blobId ? 'Copied' : 'Copy'}
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Feature pills */}
          <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', justifyContent: 'center' }}>
            {['Save anything', 'AI-tagged', 'Walrus storage', 'Seal encrypted', 'Full-text search'].map(f => (
              <span key={f} style={{
                fontSize: 11,
                padding: '5px 12px',
                border: '1px solid var(--rim)',
                borderRadius: 20,
                color: 'var(--text-muted)',
                background: 'var(--glow-faint)',
                letterSpacing: '0.05em',
              }}>{f}</span>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

function LoadingView() {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: 'calc(100vh - 120px)',
      gap: 24,
      position: 'relative',
      zIndex: 1,
    }}>
      <div style={{ position: 'relative', width: 100, height: 100 }}>
        {[0, 1, 2].map(i => (
          <div key={i} style={{
            position: 'absolute',
            inset: 0,
            borderRadius: '50%',
            border: '1px solid var(--glow)',
            animation: `sonar-pulse 2s ease-out ${i * 0.66}s infinite`,
          }} />
        ))}
        <div style={{
          position: 'absolute',
          inset: 0,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: 28,
        }}>
          <img src="/shark-icon.png" alt="WALVIS" style={{ width: 48, height: 48, objectFit: 'contain', background: 'transparent' }} />
        </div>
      </div>
      <div style={{
        fontFamily: 'var(--font-data)',
        fontSize: 11,
        letterSpacing: '0.3em',
        color: 'var(--text-muted)',
        textTransform: 'uppercase',
      }}>
        Diving into Walrus
        <span style={{ animation: 'blink-cursor 1s infinite' }}>_</span>
      </div>
    </div>
  );
}

function StatPill({ label, value }: { label: string; value: string | number }) {
  return (
    <div style={{
      display: 'flex',
      alignItems: 'baseline',
      gap: 6,
    }}>
      <span style={{ fontFamily: 'var(--font-display)', fontSize: 18, fontWeight: 700, color: 'var(--walrus-mint)', letterSpacing: '-0.02em' }}>{value}</span>
      <span style={{ fontSize: 9, letterSpacing: '0.15em', color: 'var(--text-dim)', textTransform: 'uppercase' }}>{label}</span>
    </div>
  );
}

function EncryptedSpaceCard({ entry, packageId, onDecrypted }: {
  entry: { id: string; blobId: string; policyObjectId: string };
  packageId: string;
  onDecrypted: (space: Space) => void;
}) {
  const [state, setState] = useState<'locked' | 'decrypting' | 'error'>('locked');
  const [error, setError] = useState('');
  const account = useCurrentAccount();
  const { mutateAsync: signPersonalMessage } = useSignPersonalMessage();

  const handleDecrypt = async () => {
    if (!account) {
      setError('Connect your wallet first');
      setState('error');
      return;
    }
    setState('decrypting');
    setError('');

    const result = await fetchAndDecryptSpace(
      entry.blobId,
      packageId,
      entry.policyObjectId,
      account.address,
      signPersonalMessage,
    );

    if (result.success) {
      onDecrypted(result.space);
    } else {
      setError(result.error);
      setState('error');
    }
  };

  return (
    <div style={{
      background: 'var(--layer)',
      border: '1px solid var(--rim)',
      borderRadius: 12,
      padding: '20px 24px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      gap: 16,
      position: 'relative',
      overflow: 'hidden',
    }}>
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        height: 2,
        background: 'linear-gradient(90deg, rgba(151,240,229,0.2), rgba(151,240,229,0.5), rgba(151,240,229,0.2))',
      }} />

      <div style={{ flex: 1, minWidth: 0 }}>
        <h3 style={{
          fontFamily: 'var(--font-display)',
          fontWeight: 700,
          fontSize: 18,
          letterSpacing: '-0.02em',
          color: 'var(--text)',
          margin: 0,
          display: 'flex',
          alignItems: 'center',
          gap: 8,
        }}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--walrus-mint)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
            <path d="M7 11V7a5 5 0 0 1 10 0v4" />
          </svg>
          Space {entry.id.slice(0, 8)}...
        </h3>
        <div style={{
          marginTop: 6,
          fontSize: 10,
          color: 'var(--text-dim)',
          letterSpacing: '0.08em',
          textTransform: 'uppercase',
        }}>
          Seal Encrypted
          {error && <span style={{ color: '#ff6b6b', marginLeft: 8, textTransform: 'none', letterSpacing: 0 }}>{error}</span>}
        </div>
      </div>

      <button
        onClick={handleDecrypt}
        disabled={state === 'decrypting'}
        style={{
          background: state === 'decrypting' ? 'transparent' : 'var(--walrus-mint-faint)',
          border: '1px solid var(--walrus-mint-dim)',
          color: 'var(--walrus-mint)',
          padding: '8px 16px',
          borderRadius: 6,
          fontSize: 11,
          letterSpacing: '0.1em',
          textTransform: 'uppercase',
          fontFamily: 'var(--font-data)',
          cursor: state === 'decrypting' ? 'wait' : 'pointer',
          transition: 'all 0.2s',
          whiteSpace: 'nowrap',
        }}
      >
        {state === 'decrypting' ? 'Decrypting...' : state === 'error' ? 'Retry' : 'Unlock'}
      </button>
    </div>
  );
}

function LoadedView({ manifest, spaces: initialSpaces, mode }: { manifest: Manifest; spaces: Space[]; mode: 'local' | 'walrus' }) {
  const [spaces, setSpaces] = useState(initialSpaces);
  const [query, setQuery] = useState('');
  const [activeTag, setActiveTag] = useState<string | null>(null);
  const [selectedItem, setSelectedItem] = useState<{ item: BookmarkItem; space: Space } | null>(null);
  const navigate = useNavigate();
  const { setCenterLabel } = useNavContext();

  // Track encrypted spaces that haven't been decrypted yet
  const encryptedEntries = mode === 'walrus' ? getEncryptedSpaceIds(manifest) : [];
  const [pendingEncrypted, setPendingEncrypted] = useState(encryptedEntries);

  const handleDecrypted = (space: Space) => {
    setSpaces(prev => [...prev, space]);
    setPendingEncrypted(prev => prev.filter(e => e.id !== space.id));
  };

  // Set header center label to agent name / space names
  useEffect(() => {
    const label = spaces.length === 1
      ? spaces[0].name
      : `${manifest.agent} // ${mode === 'local' ? 'LOCAL' : manifest.network.toUpperCase()}`;
    setCenterLabel(label);
    return () => setCenterLabel('');
  }, [spaces, manifest, mode, setCenterLabel]);

  const allTags = getAllTags(spaces);
  const totalItems = spaces.reduce((sum, s) => sum + s.items.length, 0);

  const searchResults = query.length >= 2 ? searchItems(spaces, query) : [];

  // Tag-filtered view
  const tagResults = activeTag
    ? spaces.flatMap(s => s.items.filter(i => i.tags.includes(activeTag)).map(i => ({ item: i, space: s })))
    : [];

  const displayResults = activeTag ? tagResults : searchResults;
  const showResults = activeTag || query.length >= 2;

  return (
    <div style={{ position: 'relative', zIndex: 1, animation: 'depth-fade 0.5s ease forwards' }}>
      {/* Stats bar */}
      <div style={{
        display: 'flex',
        gap: 20,
        marginBottom: 32,
        alignItems: 'center',
        justifyContent: 'flex-end',
      }}>
        <StatPill label="Spaces" value={spaces.length} />
        <span style={{ color: 'var(--rim)', fontSize: 10 }}>·</span>
        <StatPill label="Items" value={totalItems} />
        <span style={{ color: 'var(--rim)', fontSize: 10 }}>·</span>
        <StatPill label="Tags" value={allTags.length} />
      </div>

      {/* Search */}
      <div style={{ marginBottom: 20 }}>
        <SearchBar value={query} onChange={setQuery} />
      </div>

      {/* Tag filter */}
      {allTags.length > 0 && (
        <div style={{ marginBottom: 28 }}>
          <TagFilter tags={allTags} active={activeTag} onSelect={t => setActiveTag(activeTag === t ? null : t)} />
        </div>
      )}

      {/* Results or spaces */}
      {showResults ? (
        <div>
          <div style={{
            fontSize: 10,
            letterSpacing: '0.2em',
            color: 'var(--text-dim)',
            textTransform: 'uppercase',
            marginBottom: 16,
          }}>
            {activeTag ? `#${activeTag}` : `"${query}"`} — {displayResults.length} result{displayResults.length !== 1 ? 's' : ''}
          </div>
          <div style={{
            columns: '320px auto',
            columnGap: '12px',
          }}>
            {displayResults.map(({ item, space }) => (
              <div key={item.id} style={{ breakInside: 'avoid', marginBottom: 12 }}>
                <ItemCard
                  item={item}
                  onClick={() => setSelectedItem({ item, space })}
                />
              </div>
            ))}
          </div>
        </div>
      ) : totalItems === 0 ? (
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '80px 20px',
          gap: 20,
        }}>
          <img src="/shark-icon.png" alt="WALVIS" style={{ width: 48, height: 48, objectFit: 'contain' }} />
          <div style={{
            fontFamily: 'var(--font-display)',
            fontSize: 20,
            fontWeight: 700,
            color: 'var(--text)',
          }}>
            No items yet
          </div>
          <div style={{
            color: 'var(--text-muted)',
            fontSize: 12,
            textAlign: 'center',
            maxWidth: 400,
            lineHeight: 1.8,
          }}>
            Send anything to{' '}
            <code style={{ color: 'var(--glow)', fontSize: 11 }}>/walvis</code>{' '}
            in Telegram to start saving.
          </div>
          <div style={{
            display: 'flex',
            gap: 10,
            marginTop: 8,
            flexWrap: 'wrap',
            justifyContent: 'center',
          }}>
            {[
              { cmd: '/walvis <url>', desc: 'Save a link' },
              { cmd: '/walvis <text>', desc: 'Save a note' },
              { cmd: '/walvis sync', desc: 'Sync to Walrus' },
            ].map(h => (
              <div key={h.cmd} style={{
                padding: '8px 14px',
                background: 'var(--layer)',
                border: '1px solid var(--rim)',
                borderRadius: 6,
                fontSize: 11,
              }}>
                <code style={{ color: 'var(--glow)' }}>{h.cmd}</code>
                <span style={{ color: 'var(--text-dim)', marginLeft: 8 }}>{h.desc}</span>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div>
          <div style={{
            fontSize: 10,
            letterSpacing: '0.2em',
            color: 'var(--text-dim)',
            textTransform: 'uppercase',
            marginBottom: 16,
          }}>
            Your Spaces
          </div>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
            gap: 14,
            marginBottom: 32,
          }}>
            {spaces.map(space => (
              <SpaceCard
                key={space.id}
                space={space}
                encrypted={!!space.seal?.encrypted}
                onClick={() => navigate({ to: '/space/$id', params: { id: space.id } })}
              />
            ))}
          </div>

          {/* Encrypted spaces awaiting unlock */}
          {pendingEncrypted.length > 0 && manifest.sealPackageId && (
            <>
              <div style={{
                fontSize: 10,
                letterSpacing: '0.2em',
                color: 'var(--text-dim)',
                textTransform: 'uppercase',
                marginBottom: 16,
              }}>
                Encrypted Spaces
              </div>
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
                gap: 14,
                marginBottom: 32,
              }}>
                {pendingEncrypted.map(entry => (
                  <EncryptedSpaceCard
                    key={entry.id}
                    entry={entry}
                    packageId={manifest.sealPackageId!}
                    onDecrypted={handleDecrypted}
                  />
                ))}
              </div>
            </>
          )}
          {/* All items masonry */}
          <div style={{
            fontSize: 10,
            letterSpacing: '0.2em',
            color: 'var(--text-dim)',
            textTransform: 'uppercase',
            marginBottom: 16,
          }}>
            All Items
          </div>
          <div style={{
            columns: '320px auto',
            columnGap: '12px',
          }}>
            {spaces.flatMap(s => s.items.map(item => (
              <div key={item.id} style={{ breakInside: 'avoid', marginBottom: 12 }}>
                <ItemCard
                  item={item}
                  onClick={() => setSelectedItem({ item, space: s })}
                />
              </div>
            )))}
          </div>
        </div>
      )}

      {/* Detail Modal */}
      {selectedItem && (
        <ItemDetailModal
          item={selectedItem.item}
          onClose={() => setSelectedItem(null)}
          isLocalMode={mode === 'local'}
          spaceId={selectedItem.space.id}
          onItemChanged={(updated) => {
            setSpaces(prev => prev.map(s =>
              s.id === selectedItem.space.id
                ? { ...s, items: s.items.map(i => i.id === updated.id ? updated : i) }
                : s
            ));
          }}
          onItemDeleted={(id) => {
            setSpaces(prev => prev.map(s =>
              s.id === selectedItem.space.id
                ? { ...s, items: s.items.filter(i => i.id !== id) }
                : s
            ));
          }}
        />
      )}
    </div>
  );
}

export default function HomePage() {
  const [state, setState] = useState<ViewState>({ kind: 'landing' });

  const handleLoad = useCallback(async (blobId: string) => {
    setState({ kind: 'loading' });
    try {
      if (blobId === 'local') {
        // Local mode
        const manifest = await fetchLocalManifest();
        const spaces = await fetchAllLocalSpaces(manifest);
        setState({ kind: 'loaded', manifest, spaces, mode: 'local' });
      } else {
        // Walrus mode
        const manifest = await fetchManifest(blobId);
        const spaces = await fetchAllSpaces(manifest);
        setState({ kind: 'loaded', manifest, spaces, mode: 'walrus' });
      }
    } catch (err) {
      setState({ kind: 'error', message: (err as Error).message });
    }
  }, []);

  return (
    <>
      <DepthGrid />
      {state.kind === 'landing' && <LandingInput onLoad={handleLoad} />}
      {state.kind === 'loading' && <LoadingView />}
      {state.kind === 'error' && (
        <div style={{
          position: 'relative', zIndex: 1,
          display: 'flex', flexDirection: 'column', alignItems: 'center',
          justifyContent: 'center', minHeight: 'calc(100vh - 120px)', gap: 16,
        }}>
          <div style={{ fontSize: 32 }}>⚠</div>
          <div style={{ color: 'var(--amber)', fontFamily: 'var(--font-display)', fontSize: 18, fontWeight: 700 }}>Signal Lost</div>
          <div style={{ color: 'var(--text-muted)', fontSize: 12 }}>{state.message}</div>
          <button
            onClick={() => setState({ kind: 'landing' })}
            style={{
              marginTop: 8, background: 'var(--layer)', border: '1px solid var(--rim)',
              color: 'var(--glow)', padding: '8px 20px', borderRadius: 4,
              fontSize: 11, letterSpacing: '0.15em', cursor: 'pointer',
            }}
          >
            Try Again
          </button>
        </div>
      )}
      {state.kind === 'loaded' && <LoadedView manifest={state.manifest} spaces={state.spaces} mode={state.mode} />}
    </>
  );
}
