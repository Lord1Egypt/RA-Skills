import { useRef } from 'react';

interface Props {
  value: string;
  onChange: (v: string) => void;
  placeholder?: string;
}

export function SearchBar({ value, onChange, placeholder = 'Search items…' }: Props) {
  const ref = useRef<HTMLInputElement>(null);

  return (
    <div style={{
      position: 'relative',
      display: 'flex',
      alignItems: 'center',
    }}>
      {/* Search icon */}
      <span style={{
        position: 'absolute',
        left: 14,
        color: value ? 'var(--glow)' : 'var(--text-dim)',
        pointerEvents: 'none',
        transition: 'color 0.2s',
        display: 'flex',
        alignItems: 'center',
      }}>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="11" cy="11" r="8" />
          <line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
      </span>

      <input
        ref={ref}
        type="text"
        value={value}
        onChange={e => onChange(e.target.value)}
        placeholder={placeholder}
        style={{
          width: '100%',
          background: 'var(--layer)',
          border: `1px solid ${value ? 'var(--walrus-mint-dim)' : 'var(--rim)'}`,
          borderRadius: 6,
          padding: '10px 14px 10px 40px',
          color: 'var(--text)',
          fontFamily: 'var(--font-data)',
          fontSize: 13,
          outline: 'none',
          transition: 'border-color 0.2s',
        }}
        onFocus={e => {
          (e.target as HTMLInputElement).style.borderColor = 'var(--glow-dim)';
          (e.target as HTMLInputElement).style.boxShadow = '0 0 0 3px var(--glow-faint)';
        }}
        onBlur={e => {
          (e.target as HTMLInputElement).style.borderColor = value ? 'var(--walrus-mint-dim)' : 'var(--rim)';
          (e.target as HTMLInputElement).style.boxShadow = 'none';
        }}
      />

      {value && (
        <button
          onClick={() => { onChange(''); ref.current?.focus(); }}
          style={{
            position: 'absolute',
            right: 12,
            background: 'none',
            border: 'none',
            color: 'var(--text-dim)',
            cursor: 'pointer',
            fontSize: 14,
            lineHeight: 1,
            padding: '2px 4px',
            borderRadius: 3,
          }}
        >
          ×
        </button>
      )}
    </div>
  );
}
