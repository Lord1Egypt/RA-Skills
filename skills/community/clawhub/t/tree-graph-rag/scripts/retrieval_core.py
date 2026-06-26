def _normalize_keywords(keywords: list[str]) -> list[str]:
    return [" ".join(keyword.strip().lower().split()) for keyword in keywords if keyword and keyword.strip()]


async def hybrid_retrieve(db_pool, workspace: str, extracted_keywords: list):
    """
    Use graph hits to find anchored tree nodes, then assemble tree summaries and content.
    """
    normalized_keywords = _normalize_keywords(extracted_keywords)
    if not normalized_keywords:
        return "No relevant context found."

    async with db_pool.acquire() as conn:
        anchors = await conn.fetch("""
            SELECT DISTINCT node_id
            FROM pageindex_entities
            WHERE workspace = $1 AND canonical_name = ANY($2)
            UNION
            SELECT DISTINCT r.node_id
            FROM pageindex_relationships r
            WHERE r.workspace = $1
              AND EXISTS (
                  SELECT 1
                  FROM unnest(r.keywords) AS keyword
                  WHERE lower(keyword) = ANY($2)
              )
        """, workspace, normalized_keywords)

        target_node_ids = [row['node_id'] for row in anchors]
        if not target_node_ids:
            return "No relevant context found."

        tree_rows = await conn.fetch("""
            SELECT node_id, parent_id, title, summary
            FROM pageindex_nodes
            WHERE workspace = $1 AND node_id = ANY($2)
        """, workspace, target_node_ids)

        context_rows = await conn.fetch("""
            SELECT n.title, n.summary, c.content
            FROM pageindex_nodes n
            JOIN pageindex_node_contents c ON n.node_id = c.node_id
            WHERE n.workspace = $1 AND n.node_id = ANY($2)
        """, workspace, target_node_ids)

        assembled_context = "### Context Information:\n\n"
        if tree_rows:
            assembled_context += "## Anchor Nodes\n"
            for row in tree_rows:
                assembled_context += f"- {row['title']} | summary={row['summary']}\n"
            assembled_context += "\n"

        for row in context_rows:
            assembled_context += f"**Section**: {row['title']}\n"
            assembled_context += f"**Summary**: {row['summary']}\n"
            assembled_context += f"**Details**: {row['content']}\n\n"

        return assembled_context
