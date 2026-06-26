import { createFileRoute, useNavigate } from '@tanstack/react-router';
import { useState, useEffect } from 'react';
import type { Space } from '../lib/types';
import { ItemCard } from '../components/ItemCard';
import { TagFilter } from '../components/TagFilter';
import { SearchBar } from '../components/SearchBar';

export const Route = createFileRoute('/space/$id')({
  component: SpacePage,
});

function SpacePage() {
  const { id } = Route.useParams();
  const navigate = useNavigate();
  const [space] = useState<Space | null>(null);
  const [query, setQuery] = useState('');
  const [activeTag, setActiveTag] = useState<string | null>(null);

  useEffect(() => {
    // Try to load from Walrus if we have a blobId stored
    const loadSpace = async () => {
      try {
        // Check local state first — in a real app you'd use a store
        // For now, navigate back if no state
        navigate({ to: '/' });
      } catch (err) {
        // Error handling
      }
    };
    loadSpace();
  }, [id, navigate]);

  if (!space) return null;

  const tags = [...new Set(space.items.flatMap(i => i.tags))];
  const tagCounts = tags.map(tag => ({
    tag,
    count: space.items.filter(i => i.tags.includes(tag)).length,
  }));

  const filtered = space.items.filter(item => {
    const matchTag = !activeTag || item.tags.includes(activeTag);
    const matchQuery = !query || query.length < 2 ||
      item.title.toLowerCase().includes(query.toLowerCase()) ||
      item.summary.toLowerCase().includes(query.toLowerCase()) ||
      item.tags.some(t => t.includes(query.toLowerCase()));
    return matchTag && matchQuery;
  });

  return (
    <div style={{ animation: 'depth-fade 0.4s ease forwards' }}>
      <button
        onClick={() => navigate({ to: '/' })}
        style={{
          background: 'none', border: 'none', color: 'var(--text-muted)',
          fontSize: 11, letterSpacing: '0.15em', cursor: 'pointer',
          marginBottom: 24, display: 'flex', alignItems: 'center', gap: 6,
        }}
      >
        ← Back
      </button>

      <div style={{ marginBottom: 28 }}>
        <h1 style={{
          fontFamily: 'var(--font-display)', fontWeight: 800,
          fontSize: 32, letterSpacing: '-0.02em', color: 'var(--text)',
        }}>{space.name}</h1>
        {space.description && (
          <p style={{ color: 'var(--text-muted)', marginTop: 6, fontSize: 13 }}>{space.description}</p>
        )}
        <div style={{
          marginTop: 12, fontSize: 10, color: 'var(--text-dim)',
          letterSpacing: '0.15em', textTransform: 'uppercase',
        }}>
          {space.items.length} items · last synced {space.syncedAt ? new Date(space.syncedAt).toLocaleDateString() : 'never'}
        </div>
      </div>

      <div style={{ marginBottom: 16 }}>
        <SearchBar value={query} onChange={setQuery} />
      </div>
      <div style={{ marginBottom: 24 }}>
        <TagFilter tags={tagCounts} active={activeTag} onSelect={t => setActiveTag(activeTag === t ? null : t)} />
      </div>

      <div style={{
        columns: '320px auto',
        columnGap: '12px',
      }}>
        {filtered.map(item => (
          <div key={item.id} style={{ breakInside: 'avoid', marginBottom: 12 }}>
            <ItemCard
              item={item}
              onClick={() => navigate({ to: '/item/$id', params: { id: item.id }, search: { spaceId: space.id } })}
            />
          </div>
        ))}
      </div>
    </div>
  );
}
