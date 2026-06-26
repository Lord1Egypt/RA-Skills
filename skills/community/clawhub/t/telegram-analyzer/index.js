const BACKEND_URL = \"http://localhost:8001/api/v1/agent\";
const AGENT_TOKEN = \"sk_agent_openclaw_dev_12345\";

export default {
  name: \"telegram_analyzer\",
  tools: {
    search_contacts: {
      description: \"Search for contacts in SaaS\",
      parameters: { type: \"object\", properties: { query: { type: \"string\" } }, required: [\"query\"] },
      execute: async ({ query }) => {
        const res = await fetch(${BACKEND_URL}/search-contacts, {
          method: \"POST\",
          headers: { \"Content-Type\": \"application/json\", \"X-Agent-Token\": AGENT_TOKEN },
          body: JSON.stringify({ query })
        });
        return await res.json();
      }
    }
  }
};
