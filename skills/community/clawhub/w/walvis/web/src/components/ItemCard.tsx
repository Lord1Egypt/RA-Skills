import type { BookmarkItem } from '../lib/types';

interface Props {
  item: BookmarkItem;
  onClick: () => void;
}

// Pseudo-random height based on item ID for masonry effect
function getCardHeight(id: string): number {
  const hash = id.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
  const heights = [240, 280, 320, 360, 400];
  return heights[hash % heights.length];
}

export function ItemCard({ item, onClick }: Props) {
  const height = getCardHeight(item.id);

  // Link cards: screenshot + title overlay
  if (item.type === 'link' && item.screenshot) {
    return (
      <div
        onClick={onClick}
        style={{
          height: `${height}px`,
          borderRadius: 8,
          overflow: 'hidden',
          cursor: 'pointer',
          position: 'relative',
          background: 'var(--layer)',
          border: '1px solid var(--rim)',
          transition: 'all 0.25s ease',
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'scale(1.02)';
          e.currentTarget.style.filter = 'brightness(1.1)';
          e.currentTarget.style.borderColor = 'var(--walrus-mint-dim)';
          e.currentTarget.style.boxShadow = '0 0 20px rgba(151, 240, 229, 0.15)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'scale(1)';
          e.currentTarget.style.filter = 'brightness(1)';
          e.currentTarget.style.borderColor = 'var(--rim)';
          e.currentTarget.style.boxShadow = 'none';
        }}
      >
        {/* Screenshot */}
        <img
          src={item.screenshot}
          alt={item.title}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
          }}
        />
        {/* Bottom gradient overlay with title */}
        <div style={{
          position: 'absolute',
          bottom: 0,
          left: 0,
          right: 0,
          padding: '40px 16px 16px',
          background: 'linear-gradient(to top, rgba(8, 14, 27, 0.95), transparent)',
        }}>
          <div style={{
            fontFamily: 'var(--font-display)',
            fontSize: 14,
            fontWeight: 600,
            color: '#fff',
            lineHeight: 1.3,
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            display: '-webkit-box',
            WebkitLineClamp: 2,
            WebkitBoxOrient: 'vertical',
          }}>
            {item.title}
          </div>
          {/* Tags */}
          {item.tags.length > 0 && (
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginTop: 8 }}>
              {item.tags.slice(0, 3).map(tag => (
                <span key={tag} style={{
                  fontSize: 9,
                  padding: '2px 6px',
                  background: 'rgba(151, 240, 229, 0.15)',
                  border: '1px solid rgba(151, 240, 229, 0.3)',
                  borderRadius: 3,
                  color: 'var(--walrus-mint)',
                  letterSpacing: '0.05em',
                }}>
                  #{tag}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    );
  }

  // Image cards: image fills entire card, title on hover
  if (item.type === 'image') {
    return (
      <div
        onClick={onClick}
        style={{
          height: `${height}px`,
          borderRadius: 8,
          overflow: 'hidden',
          cursor: 'pointer',
          position: 'relative',
          background: 'var(--layer)',
          border: '1px solid var(--rim)',
          transition: 'all 0.25s ease',
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'scale(1.02)';
          e.currentTarget.style.filter = 'brightness(1.1)';
          e.currentTarget.style.borderColor = 'var(--walrus-mint-dim)';
          e.currentTarget.style.boxShadow = '0 0 20px rgba(151, 240, 229, 0.15)';
          const overlay = e.currentTarget.querySelector('.hover-overlay') as HTMLElement;
          if (overlay) overlay.style.opacity = '1';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'scale(1)';
          e.currentTarget.style.filter = 'brightness(1)';
          e.currentTarget.style.borderColor = 'var(--rim)';
          e.currentTarget.style.boxShadow = 'none';
          const overlay = e.currentTarget.querySelector('.hover-overlay') as HTMLElement;
          if (overlay) overlay.style.opacity = '0';
        }}
      >
        {/* Image */}
        <img
          src={item.url || item.content}
          alt={item.title}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
          }}
        />
        {/* Hover overlay with title */}
        <div
          className="hover-overlay"
          style={{
            position: 'absolute',
            inset: 0,
            background: 'rgba(8, 14, 27, 0.85)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: 20,
            opacity: 0,
            transition: 'opacity 0.25s ease',
          }}
        >
          <div style={{
            fontFamily: 'var(--font-display)',
            fontSize: 16,
            fontWeight: 600,
            color: '#fff',
            textAlign: 'center',
            lineHeight: 1.4,
          }}>
            {item.title}
          </div>
        </div>
      </div>
    );
  }

  // Text/note cards: dark gradient, text content, left border accent
  return (
    <div
      onClick={onClick}
      style={{
        height: `${height}px`,
        borderRadius: 8,
        overflow: 'hidden',
        cursor: 'pointer',
        position: 'relative',
        background: 'linear-gradient(135deg, rgba(17, 29, 48, 0.9), rgba(12, 21, 36, 0.95))',
        border: '1px solid var(--rim)',
        borderLeft: '3px solid var(--walrus-mint)',
        padding: 16,
        display: 'flex',
        flexDirection: 'column',
        gap: 10,
        transition: 'all 0.25s ease',
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = 'scale(1.02)';
        e.currentTarget.style.filter = 'brightness(1.1)';
        e.currentTarget.style.borderColor = 'var(--walrus-mint-dim)';
        e.currentTarget.style.boxShadow = '0 0 20px rgba(151, 240, 229, 0.15)';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = 'scale(1)';
        e.currentTarget.style.filter = 'brightness(1)';
        e.currentTarget.style.borderColor = 'var(--rim)';
        e.currentTarget.style.boxShadow = 'none';
      }}
    >
      {/* Title */}
      <div style={{
        fontFamily: 'var(--font-display)',
        fontSize: 14,
        fontWeight: 600,
        color: '#fff',
        lineHeight: 1.3,
      }}>
        {item.title}
      </div>
      {/* Content preview */}
      <div style={{
        fontSize: 12,
        color: 'var(--text-muted)',
        lineHeight: 1.6,
        overflow: 'hidden',
        display: '-webkit-box',
        WebkitLineClamp: Math.floor((height - 100) / 20),
        WebkitBoxOrient: 'vertical',
        flex: 1,
      }}>
        {item.content || item.summary}
      </div>
      {/* Tags */}
      {item.tags.length > 0 && (
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginTop: 'auto' }}>
          {item.tags.slice(0, 3).map(tag => (
            <span key={tag} style={{
              fontSize: 9,
              padding: '2px 6px',
              background: 'rgba(151, 240, 229, 0.1)',
              border: '1px solid rgba(151, 240, 229, 0.2)',
              borderRadius: 3,
              color: 'var(--walrus-mint)',
              letterSpacing: '0.05em',
            }}>
              #{tag}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
