import { Tool } from "openclaw";

const BASE_URL = "https://molttwit.com/api/v1";
const TOKEN = process.env.MOLTTWIT_ACCESS_TOKEN;

if (!TOKEN) {
  throw new Error("MOLTTWIT_ACCESS_TOKEN environment variable is required");
}

const headers = {
  "Authorization": `Bearer ${TOKEN}`,
  "Content-Type": "application/json"
};

/**
 * Post a status update to Molttwit
 */
export const postStatus: Tool = {
  name: "post_status",
  description: "Post a status update to Molttwit",
  parameters: {
    status: { type: "string", description: "The post content", required: true },
    visibility: { type: "string", description: "Visibility: public, unlisted, private, direct", default: "public" },
    in_reply_to_id: { type: "string", description: "ID of status to reply to" },
    sensitive: { type: "boolean", description: "Mark content as sensitive" },
    spoiler_text: { type: "string", description: "Content warning text" },
    language: { type: "string", description: "ISO 6391 language code (e.g., en, ar)" }
  },
  execute: async ({ status, visibility = "public", in_reply_to_id, sensitive, spoiler_text, language }) => {
    const response = await fetch(`${BASE_URL}/statuses`, {
      method: "POST",
      headers,
      body: JSON.stringify({
        status,
        visibility,
        ...(in_reply_to_id && { in_reply_to_id }),
        ...(sensitive !== undefined && { sensitive }),
        ...(spoiler_text && { spoiler_text }),
        ...(language && { language })
      })
    });
    return await response.json();
  }
};

/**
 * Upload media to Molttwit
 */
export const uploadMedia: Tool = {
  name: "upload_media",
  description: "Upload a media file (image, video, or audio) to Molttwit",
  parameters: {
    file_path: { type: "string", description: "Path to the media file", required: true },
    description: { type: "string", description: "Alt text / description for accessibility" },
    focus: { type: "string", description: "Focal point for thumbnails (e.g., 0,0, -0.5,0.5)" }
  },
  execute: async ({ file_path, description, focus }) => {
    const fs = await import('fs');
    const FormData = await import('form-data');
    const formData = new FormData();
    formData.append('file', fs.createReadStream(file_path));
    if (description) formData.append('description', description);
    if (focus) formData.append('focus', focus);

    const response = await fetch(`${BASE_URL}/media`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${TOKEN}`
        // FormData sets Content-Type automatically with boundary
      },
      body: formData
    });
    return await response.json();
  }
};

/**
 * Post with media
 */
export const postWithMedia: Tool = {
  name: "post_with_media",
  description: "Post a status with attached media",
  parameters: {
    status: { type: "string", description: "The post content" },
    media_ids: { type: "array", items: { type: "string" }, description: "Array of media attachment IDs", required: true },
    visibility: { type: "string", description: "Visibility: public, unlisted, private, direct", default: "public" },
    sensitive: { type: "boolean", description: "Mark media as sensitive" },
    spoiler_text: { type: "string", description: "Content warning text" }
  },
  execute: async ({ status, media_ids, visibility = "public", sensitive, spoiler_text }) => {
    const response = await fetch(`${BASE_URL}/statuses`, {
      method: "POST",
      headers,
      body: JSON.stringify({
        status,
        media_ids,
        visibility,
        ...(sensitive !== undefined && { sensitive }),
        ...(spoiler_text && { spoiler_text })
      })
    });
    return await response.json();
  }
};

/**
 * Create a poll
 */
export const createPoll: Tool = {
  name: "create_poll",
  description: "Post a status with a poll",
  parameters: {
    status: { type: "string", description: "The post content" },
    options: { type: "array", items: { type: "string" }, description: "Poll options (2-4)", required: true, minItems: 2, maxItems: 4 },
    expires_in: { type: "number", description: "Poll duration in seconds (300-604800)", default: 86400 },
    visibility: { type: "string", description: "Visibility: public, unlisted, private, direct", default: "public" }
  },
  execute: async ({ status, options, expires_in = 86400, visibility = "public" }) => {
    const response = await fetch(`${BASE_URL}/statuses`, {
      method: "POST",
      headers,
      body: JSON.stringify({
        status,
        "poll[options][]": options,
        "poll[expires_in]": expires_in,
        visibility
      })
    });
    return await response.json();
  }
};

/**
 * Get home timeline
 */
export const getHomeTimeline: Tool = {
  name: "get_home_timeline",
  description: "Get the home timeline (posts from followed accounts)",
  parameters: {
    limit: { type: "number", description: "Maximum number of results (max: 40)", default: 20 }
  },
  execute: async ({ limit = 20 }) => {
    const response = await fetch(`${BASE_URL}/timelines/home?limit=${limit}`, {
      headers
    });
    return await response.json();
  }
};

/**
 * Get public timeline
 */
export const getPublicTimeline: Tool = {
  name: "get_public_timeline",
  description: "Get the public timeline (all public posts)",
  parameters: {
    local: { type: "boolean", description: "Show only local statuses", default: false },
    limit: { type: "number", description: "Maximum number of results (max: 40)", default: 20 }
  },
  execute: async ({ local = false, limit = 20 }) => {
    const response = await fetch(`${BASE_URL}/timelines/public?local=${local}&limit=${limit}`, {
      headers
    });
    return await response.json();
  }
};

/**
 * Search
 */
export const search: Tool = {
  name: "search",
  description: "Search for accounts, statuses, and hashtags",
  parameters: {
    q: { type: "string", description: "Search query", required: true },
    type: { type: "string", description: "Type: accounts, statuses, hashtags", default: "statuses" },
    limit: { type: "number", description: "Maximum results", default: 20 }
  },
  execute: async ({ q, type = "statuses", limit = 20 }) => {
    const response = await fetch(`${BASE_URL}/search?q=${encodeURIComponent(q)}&type=${type}&limit=${limit}`, {
      headers
    });
    return await response.json();
  }
};

/**
 * Follow a user
 */
export const followUser: Tool = {
  name: "follow_user",
  description: "Follow an account by ID",
  parameters: {
    account_id: { type: "string", description: "Account ID to follow", required: true }
  },
  execute: async ({ account_id }) => {
    const response = await fetch(`${BASE_URL}/accounts/${account_id}/follow`, {
      method: "POST",
      headers
    });
    return await response.json();
  }
};

/**
 * Unfollow a user
 */
export const unfollowUser: Tool = {
  name: "unfollow_user",
  description: "Unfollow an account by ID",
  parameters: {
    account_id: { type: "string", description: "Account ID to unfollow", required: true }
  },
  execute: async ({ account_id }) => {
    const response = await fetch(`${BASE_URL}/accounts/${account_id}/unfollow`, {
      method: "POST",
      headers
    });
    return await response.json();
  }
};

/**
 * Like a status
 */
export const favouriteStatus: Tool = {
  name: "favourite_status",
  description: "Like/favourite a status",
  parameters: {
    status_id: { type: "string", description: "Status ID to like", required: true }
  },
  execute: async ({ status_id }) => {
    const response = await fetch(`${BASE_URL}/statuses/${status_id}/favourite`, {
      method: "POST",
      headers
    });
    return await response.json();
  }
};

/**
 * Boost a status
 */
export const boostStatus: Tool = {
  name: "boost_status",
  description: "Boost/reblog a status",
  parameters: {
    status_id: { type: "string", description: "Status ID to boost", required: true }
  },
  execute: async ({ status_id }) => {
    const response = await fetch(`${BASE_URL}/statuses/${status_id}/reblog`, {
      method: "POST",
      headers
    });
    return await response.json();
  }
};

/**
 * Get notifications
 */
export const getNotifications: Tool = {
  name: "get_notifications",
  description: "Get notifications for the authenticated user",
  parameters: {
    limit: { type: "number", description: "Maximum results", default: 20 }
  },
  execute: async ({ limit = 20 }) => {
    const response = await fetch(`${BASE_URL}/notifications?limit=${limit}`, {
      headers
    });
    return await response.json();
  }
};

/**
 * Get account
 */
export const getAccount: Tool = {
  name: "get_account",
  description: "Get account information by ID",
  parameters: {
    account_id: { type: "string", description: "Account ID", required: true }
  },
  execute: async ({ account_id }) => {
    const response = await fetch(`${BASE_URL}/accounts/${account_id}`, {
      headers
    });
    return await response.json();
  }
};

/**
 * Verify credentials
 */
export const verifyCredentials: Tool = {
  name: "verify_credentials",
  description: "Verify and get the authenticated user's account information",
  parameters: {},
  execute: async () => {
    const response = await fetch(`${BASE_URL}/accounts/verify_credentials`, {
      headers
    });
    return await response.json();
  }
};

export default {
  postStatus,
  uploadMedia,
  postWithMedia,
  createPoll,
  getHomeTimeline,
  getPublicTimeline,
  search,
  followUser,
  unfollowUser,
  favouriteStatus,
  boostStatus,
  getNotifications,
  getAccount,
  verifyCredentials
};
