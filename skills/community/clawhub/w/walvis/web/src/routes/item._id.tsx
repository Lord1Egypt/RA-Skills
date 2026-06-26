import { createFileRoute, useNavigate } from '@tanstack/react-router';
import { useEffect } from 'react';

export const Route = createFileRoute('/item/$id')({
  validateSearch: (s: Record<string, unknown>) => ({ spaceId: s.spaceId as string | undefined }),
  component: ItemPage,
});

function ItemPage() {
  const navigate = useNavigate();

  useEffect(() => {
    navigate({ to: '/' });
  }, [navigate]);

  return null;
}
