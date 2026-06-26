require('dotenv').config();

const path = require('path');
const express = require('express');
const cors = require('cors');
const { fetchConnections } = require('./apify');
const { scoreConnections, suggestActions } = require('./agent');
const {
  ensureRedisConnected,
  saveConnection,
  getAllConnections,
  saveQueryContext,
  getQueryContext,
} = require('./redis');

const app = express();
const port = Number(process.env.PORT || 3001);

app.use(
  cors({
    origin: ['http://localhost:3000'],
  })
);
app.use(express.json());

async function seedConnectionsIfEmpty() {
  const existingConnections = await getAllConnections();

  if (existingConnections.length > 0) {
    return;
  }

  const seededConnections = await fetchConnections();
  await Promise.all(
    seededConnections.map((connection) => saveConnection(connection.id, connection))
  );

  console.log(`Seeded ${seededConnections.length} sample connections into Redis.`);
}

app.post('/api/query', async (req, res) => {
  try {
    const { query, sessionId } = req.body || {};

    if (!query || typeof query !== 'string' || !sessionId || typeof sessionId !== 'string') {
      return res.status(400).json({
        error: 'Both query and sessionId are required strings.',
      });
    }

    const cachedContext = await getQueryContext(sessionId);
    if (cachedContext && cachedContext.query === query) {
      return res.json({
        results: cachedContext.results || [],
      });
    }

    const connections = await getAllConnections();
    const scoredConnections = await scoreConnections(query, connections);

    const topResults = await Promise.all(
      scoredConnections.slice(0, 5).map(async (connection) => {
        let actions = [];

        try {
          actions = await suggestActions(connection);
        } catch {
          actions = ['Draft intro email', 'Send quick follow-up'];
        }

        return {
          name: connection.name,
          role: connection.role,
          company: connection.company,
          platforms: connection.platforms,
          relevanceScore: connection.relevanceScore,
          reason: connection.reason,
          suggestedActions: actions,
        };
      })
    );

    await saveQueryContext(sessionId, {
      query,
      results: topResults,
      createdAt: new Date().toISOString(),
    });

    return res.json({ results: topResults });
  } catch (error) {
    console.error('Query handling failed:', error);
    return res.status(500).json({
      error: 'Unable to process query right now. Please try again.',
    });
  }
});

// Serve the built frontend for single-service deployment (e.g., Render).
app.use(express.static(path.join(__dirname, 'dist')));
app.get('/{*path}', (_req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

async function start() {
  try {
    await ensureRedisConnected();
    await seedConnectionsIfEmpty();

    app.listen(port, () => {
      console.log(`Connectify backend listening on port ${port}`);
    });
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

start();
