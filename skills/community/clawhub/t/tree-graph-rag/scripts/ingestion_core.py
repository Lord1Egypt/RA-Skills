import uuid
from typing import Any


def _canonicalize(value: str) -> str:
    return " ".join(value.strip().lower().split())


async def insert_tree_skeleton(db_pool, workspace: str, doc_id: str, tree_structure: list[dict[str, Any]]):
    """
    Flatten PageIndex tree output into relational rows.
    """
    nodes_to_insert = []
    contents_to_insert = []

    def flatten_tree(nodes_list, parent_id=None):
        for index, node in enumerate(nodes_list):
            node_id = f"{doc_id}_{node.get('node_id', str(uuid.uuid4()))}"

            nodes_to_insert.append((
                node_id, workspace, doc_id, parent_id,
                node.get('structure'), node.get('title'), node.get('summary'),
                node.get('start_index'), node.get('end_index'), index
            ))

            if 'text' in node and node['text']:
                contents_to_insert.append((
                    node_id, workspace, node['text'], node.get('text_token_count', 0)
                ))

            if 'nodes' in node and node['nodes']:
                flatten_tree(node['nodes'], parent_id=node_id)

    flatten_tree(tree_structure)

    async with db_pool.acquire() as conn:
        await conn.executemany("""
            INSERT INTO pageindex_nodes
            (node_id, workspace, doc_id, parent_id, structure, title, summary, start_index, end_index, node_order)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            ON CONFLICT (node_id) DO UPDATE SET
                parent_id = EXCLUDED.parent_id,
                structure = EXCLUDED.structure,
                title = EXCLUDED.title,
                summary = EXCLUDED.summary,
                start_index = EXCLUDED.start_index,
                end_index = EXCLUDED.end_index,
                node_order = EXCLUDED.node_order
        """, nodes_to_insert)

        if contents_to_insert:
            await conn.executemany("""
                INSERT INTO pageindex_node_contents
                (node_id, workspace, content, token_count)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (node_id) DO UPDATE SET
                    content = EXCLUDED.content,
                    token_count = EXCLUDED.token_count
            """, contents_to_insert)


async def extract_and_insert_graph(db_pool, workspace: str, llm_extract_func):
    """
    Extract entities and relationships from each node content and anchor them to the tree node.

    Expected llm_extract_func output:
    {
        "entities": [{"name": "...", "type": "...", "desc": "..."}],
        "relationships": [{
            "source": "...",
            "target": "...",
            "desc": "...",
            "keywords": ["...", "..."]
        }]
    }
    """
    async with db_pool.acquire() as conn:
        contents = await conn.fetch("SELECT node_id, content FROM pageindex_node_contents WHERE workspace = $1", workspace)

        for row in contents:
            node_id = row['node_id']
            text = row['content']

            graph_data = await llm_extract_func(text)

            entity_id_by_name: dict[str, str] = {}
            for ent in graph_data.get('entities', []):
                entity_id = str(uuid.uuid4())
                entity_name = ent['name']
                canonical_name = _canonicalize(entity_name)
                entity_id_by_name[canonical_name] = entity_id
                await conn.execute("""
                    INSERT INTO pageindex_entities
                    (entity_id, workspace, node_id, entity_name, canonical_name, entity_type, description)
                    VALUES ($1, $2, $3, $4, $5, $6, $7)
                """, entity_id, workspace, node_id, entity_name, canonical_name, ent.get('type'), ent.get('desc'))

            for rel in graph_data.get('relationships', []):
                source_id = entity_id_by_name.get(_canonicalize(rel['source']))
                target_id = entity_id_by_name.get(_canonicalize(rel['target']))
                if source_id is None or target_id is None:
                    continue
                await conn.execute("""
                    INSERT INTO pageindex_relationships
                    (rel_id, workspace, node_id, source_entity_id, target_entity_id, description, keywords)
                    VALUES ($1, $2, $3, $4, $5, $6, $7)
                """, str(uuid.uuid4()), workspace, node_id, source_id, target_id, rel.get('desc'), rel.get('keywords', []))
