import asyncio
from ingestion_core import extract_and_insert_graph, insert_tree_skeleton
from retrieval_core import hybrid_retrieve


class FakeAcquire:
    def __init__(self, conn):
        self.conn = conn

    async def __aenter__(self):
        return self.conn

    async def __aexit__(self, exc_type, exc, tb):
        return False


class FakeConn:
    def __init__(self):
        self.executemany_calls = []
        self.execute_calls = []
        self.fetch_calls = []

    async def executemany(self, sql, rows):
        self.executemany_calls.append((sql, rows))

    async def execute(self, sql, *params):
        self.execute_calls.append((sql, params))

    async def fetch(self, sql, *params):
        self.fetch_calls.append((sql, params))
        if "FROM pageindex_node_contents" in sql and "SELECT node_id, content" in sql:
            return [{"node_id": "doc_001", "content": "Tim Cook leads Apple in Cupertino."}]
        if "FROM pageindex_entities" in sql or "FROM pageindex_relationships" in sql:
            return [{"node_id": "doc_001"}]
        if "SELECT node_id, parent_id, title, summary" in sql:
            return [{"node_id": "doc_001", "parent_id": None, "title": "Leadership", "summary": "Apple leadership overview"}]
        if "JOIN pageindex_node_contents" in sql:
            return [{"title": "Leadership", "summary": "Apple leadership overview", "content": "Tim Cook leads Apple in Cupertino."}]
        return []


class FakePool:
    def __init__(self):
        self.conn = FakeConn()

    def acquire(self):
        return FakeAcquire(self.conn)


async def fake_llm_extract(text):
    return {
        "entities": [
            {"name": "Tim Cook", "type": "person", "desc": "CEO of Apple"},
            {"name": "Apple", "type": "company", "desc": "Technology company"},
        ],
        "relationships": [
            {"source": "Tim Cook", "target": "Apple", "desc": "leads", "keywords": ["leadership", "ceo"]}
        ],
    }


async def main():
    pool = FakePool()
    tree = [{"node_id": "001", "title": "Leadership", "summary": "Apple leadership overview", "text": "Tim Cook leads Apple in Cupertino."}]
    await insert_tree_skeleton(pool, "demo", "doc", tree)
    await extract_and_insert_graph(pool, "demo", fake_llm_extract)
    context = await hybrid_retrieve(pool, "demo", ["Tim Cook", "leadership"])
    print(context)


if __name__ == "__main__":
    asyncio.run(main())
