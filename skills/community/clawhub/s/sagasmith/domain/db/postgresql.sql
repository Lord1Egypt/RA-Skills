CREATE EXTENSION IF NOT EXISTS vector;
ALTER TABLE IF EXISTS rule_chunks ADD COLUMN IF NOT EXISTS embedding_vector vector(1024);
ALTER TABLE IF EXISTS rule_chunks ADD COLUMN IF NOT EXISTS search_vector tsvector;
UPDATE rule_chunks SET search_vector =
  to_tsvector('simple', coalesce(heading, '') || ' ' || coalesce(breadcrumb, '') || ' ' || chunk_text);
CREATE INDEX IF NOT EXISTS idx_rule_chunks_search_vector ON rule_chunks USING gin(search_vector);
CREATE INDEX IF NOT EXISTS idx_rule_chunks_embedding_hnsw ON rule_chunks
USING hnsw (embedding_vector vector_cosine_ops);
