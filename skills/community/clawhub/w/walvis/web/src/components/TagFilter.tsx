interface TagEntry { tag: string; count: number; }

interface Props {
  tags: TagEntry[];
  active: string | null;
  onSelect: (tag: string) => void;
}

export function TagFilter({ tags, active, onSelect }: Props) {
  if (tags.length === 0) return null;

  return (
    <div style={{
      display: 'flex',
      flexWrap: 'wrap',
      gap: 6,
      alignItems: 'center',
    }}>
      <span style={{
        fontSize: 9,
        letterSpacing: '0.2em',
        color: 'var(--text-dim)',
        textTransform: 'uppercase',
        marginRight: 4,
        flexShrink: 0,
      }}>
        Filter
      </span>
      {tags.slice(0, 20).map(({ tag, count }) => {
        const isActive = active === tag;
        return (
          <button
            key={tag}
            onClick={() => onSelect(tag)}
            style={{
              background: isActive ? 'var(--glow)' : 'var(--glow-faint)',
              border: `1px solid ${isActive ? 'var(--glow)' : 'rgba(0,200,255,0.15)'}`,
              borderRadius: 3,
              padding: '3px 8px',
              fontSize: 10,
              letterSpacing: '0.05em',
              color: isActive ? '#000' : 'var(--text-muted)',
              cursor: 'pointer',
              fontFamily: 'var(--font-data)',
              transition: 'all 0.15s',
              display: 'inline-flex',
              alignItems: 'center',
              gap: 4,
            }}
            onMouseEnter={e => {
              if (!isActive) {
                (e.currentTarget as HTMLElement).style.borderColor = 'var(--glow-dim)';
                (e.currentTarget as HTMLElement).style.color = 'var(--text)';
              }
            }}
            onMouseLeave={e => {
              if (!isActive) {
                (e.currentTarget as HTMLElement).style.borderColor = 'rgba(0,200,255,0.15)';
                (e.currentTarget as HTMLElement).style.color = 'var(--text-muted)';
              }
            }}
          >
            #{tag}
            <span style={{
              fontSize: 9,
              opacity: 0.6,
              marginLeft: 2,
            }}>
              {count}
            </span>
          </button>
        );
      })}
    </div>
  );
}
