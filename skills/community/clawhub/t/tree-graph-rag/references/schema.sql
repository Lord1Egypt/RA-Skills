CREATE TABLE IF NOT EXISTS pageindex_documents (
    doc_id VARCHAR(255) PRIMARY KEY,
    workspace VARCHAR(255) NOT NULL,
    doc_name VARCHAR(512) NOT NULL,
    total_pages INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pageindex_nodes (
    node_id VARCHAR(255) PRIMARY KEY,
    workspace VARCHAR(255) NOT NULL,
    doc_id VARCHAR(255) NOT NULL REFERENCES pageindex_documents(doc_id) ON DELETE CASCADE,
    parent_id VARCHAR(255),
    structure VARCHAR(100),
    title VARCHAR(1024) NOT NULL,
    summary TEXT,
    start_index INTEGER,
    end_index INTEGER,
    node_order INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS pageindex_node_contents (
    node_id VARCHAR(255) PRIMARY KEY REFERENCES pageindex_nodes(node_id) ON DELETE CASCADE,
    workspace VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    token_count INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS pageindex_entities (
    entity_id VARCHAR(255) PRIMARY KEY,
    workspace VARCHAR(255) NOT NULL,
    node_id VARCHAR(255) NOT NULL REFERENCES pageindex_nodes(node_id) ON DELETE CASCADE,
    entity_name VARCHAR(255) NOT NULL,
    canonical_name VARCHAR(255) NOT NULL,
    entity_type VARCHAR(100),
    description TEXT
);

CREATE TABLE IF NOT EXISTS pageindex_relationships (
    rel_id VARCHAR(255) PRIMARY KEY,
    workspace VARCHAR(255) NOT NULL,
    node_id VARCHAR(255) NOT NULL REFERENCES pageindex_nodes(node_id) ON DELETE CASCADE,
    source_entity_id VARCHAR(255) REFERENCES pageindex_entities(entity_id),
    target_entity_id VARCHAR(255) REFERENCES pageindex_entities(entity_id),
    description TEXT,
    keywords TEXT[] NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_pageindex_documents_workspace
    ON pageindex_documents (workspace, doc_id);

CREATE INDEX IF NOT EXISTS idx_pageindex_nodes_doc_parent
    ON pageindex_nodes (workspace, doc_id, parent_id, node_order);

CREATE INDEX IF NOT EXISTS idx_pageindex_entities_lookup
    ON pageindex_entities (workspace, canonical_name, node_id);

CREATE INDEX IF NOT EXISTS idx_pageindex_relationships_node
    ON pageindex_relationships (workspace, node_id);
