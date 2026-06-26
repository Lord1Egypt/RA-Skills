/**
 * Rentaclaw Skill Tools
 *
 * These tools interact with the Rentaclaw public API to manage agent listings.
 */

const RENTACLAW_API_URL = 'https://www.rentaclaw.io/api/public';

// Get API key from environment (set via credentials in SKILL.md)
function getApiKey(): string {
  const apiKey = process.env.RENTACLAW_API_KEY;
  if (!apiKey) {
    throw new Error('RENTACLAW_API_KEY not configured. Add your API key in the skill credentials.');
  }
  return apiKey;
}

async function apiRequest(
  endpoint: string,
  options: RequestInit = {}
): Promise<Response> {
  const apiKey = getApiKey();

  return fetch(`${RENTACLAW_API_URL}${endpoint}`, {
    ...options,
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
}

/**
 * Test the Rentaclaw connection and verify API key
 */
export async function rentaclaw_setup(): Promise<string> {
  try {
    const apiKey = getApiKey();

    if (!apiKey.startsWith('rck_')) {
      return 'Invalid API key format. Keys should start with "rck_". Get yours at https://www.rentaclaw.io/dashboard/api-keys';
    }

    // Test the key
    const testResponse = await fetch(`${RENTACLAW_API_URL}/stats`, {
      headers: { 'Authorization': `Bearer ${apiKey}` },
    });

    if (!testResponse.ok) {
      return 'Invalid or expired API key. Please check your key at https://www.rentaclaw.io/dashboard/api-keys';
    }

    return '✅ Rentaclaw connected! Your API key is valid. You can now list and manage your agents.';
  } catch (error) {
    return `❌ ${error instanceof Error ? error.message : 'Failed to connect'}`;
  }
}

/**
 * List an agent on Rentaclaw
 */
export async function rentaclaw_list(params: {
  name: string;
  description: string;
  category?: string;
  price_hour: number;
  price_day: number;
  price_month: number;
}): Promise<string> {
  const { name, description, category, price_hour, price_day, price_month } = params;

  // Get OpenClaw gateway info from environment
  const webhookUrl = process.env.OPENCLAW_WEBHOOK_URL || 'http://localhost:18789';
  const hookToken = process.env.OPENCLAW_HOOK_TOKEN || '';
  const agentName = process.env.OPENCLAW_AGENT_NAME || 'default';

  const response = await apiRequest('/agents', {
    method: 'POST',
    body: JSON.stringify({
      name,
      description,
      category: category || 'Other',
      pricePerHour: price_hour,
      pricePerDay: price_day,
      pricePerMonth: price_month,
      webhookUrl,
      hookToken,
      agentName,
      channels: ['Telegram', 'Discord', 'API'],
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    return `Failed to list agent: ${data.error}`;
  }

  return `
🎉 Agent listed successfully!

**${data.agent.name}** is now live on Rentaclaw.

📍 Marketplace URL: ${data.agent.marketplaceUrl}

Share this link with potential renters. They can pay with SOL and start using your agent immediately.
`;
}

/**
 * Check status of listed agents
 */
export async function rentaclaw_status(): Promise<string> {
  const response = await apiRequest('/agents');
  const data = await response.json();

  if (!response.ok) {
    return `Failed to fetch agents: ${data.error}`;
  }

  if (data.agents.length === 0) {
    return 'You have no agents listed on Rentaclaw yet. Use "list my agent" to create your first listing.';
  }

  const agentList = data.agents.map((a: {
    name: string;
    status: string;
    total_rentals: number;
    rating: number;
    price_per_hour: number;
    id: string;
  }) => `
• **${a.name}** (${a.status})
  Rentals: ${a.total_rentals} | Rating: ${a.rating || 'N/A'} | Price: ${a.price_per_hour} SOL/hr
  ID: ${a.id}
`).join('\n');

  return `
📋 Your Rentaclaw Agents:

${agentList}
`;
}

/**
 * Get earnings and stats
 */
export async function rentaclaw_stats(): Promise<string> {
  const response = await apiRequest('/stats');
  const data = await response.json();

  if (!response.ok) {
    return `Failed to fetch stats: ${data.error}`;
  }

  const { stats, activeRentals } = data;

  let output = `
📊 Your Rentaclaw Stats:

💰 Total Earnings: **${stats.totalEarnings} SOL**
📦 Total Rentals: **${stats.totalRentals}**
⭐ Avg Rating: **${stats.avgRating}/5**
🤖 Listed Agents: **${stats.totalAgents}**
🔥 Active Rentals: **${stats.activeRentals}**
`;

  if (activeRentals.length > 0) {
    output += `\n**Active Renters:**\n`;
    activeRentals.forEach((r: {
      agentName: string;
      renter: string;
      earnings: number;
      endsAt: string;
    }) => {
      const endsAt = new Date(r.endsAt).toLocaleString();
      output += `• ${r.agentName} → ${r.renter} (${r.earnings} SOL, ends ${endsAt})\n`;
    });
  }

  return output;
}

/**
 * Update an agent listing
 */
export async function rentaclaw_update(params: {
  agent_id: string;
  field: string;
  value: string;
}): Promise<string> {
  const { agent_id, field, value } = params;

  const fieldMapping: Record<string, string> = {
    name: 'name',
    description: 'description',
    category: 'category',
    price_hour: 'pricePerHour',
    price_day: 'pricePerDay',
    price_month: 'pricePerMonth',
    status: 'status',
  };

  const apiField = fieldMapping[field];
  if (!apiField) {
    return `Invalid field: ${field}. Valid fields: ${Object.keys(fieldMapping).join(', ')}`;
  }

  const body: Record<string, unknown> = {};
  if (field.startsWith('price_')) {
    body[apiField] = parseFloat(value);
  } else {
    body[apiField] = value;
  }

  const response = await apiRequest(`/agents/${agent_id}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  });

  const data = await response.json();

  if (!response.ok) {
    return `Failed to update agent: ${data.error}`;
  }

  return `✅ Agent updated! ${field} is now set to "${value}".`;
}

/**
 * Pause or resume an agent
 */
export async function rentaclaw_pause(params: {
  agent_id: string;
  action: 'pause' | 'resume';
}): Promise<string> {
  const { agent_id, action } = params;

  const status = action === 'pause' ? 'offline' : 'available';

  const response = await apiRequest(`/agents/${agent_id}`, {
    method: 'PATCH',
    body: JSON.stringify({ status }),
  });

  const data = await response.json();

  if (!response.ok) {
    return `Failed to ${action} agent: ${data.error}`;
  }

  if (action === 'pause') {
    return '⏸️ Agent paused. It will not accept new rentals until you resume it.';
  } else {
    return '▶️ Agent resumed! It is now available for rentals again.';
  }
}
