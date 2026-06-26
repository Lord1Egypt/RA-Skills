const API_KEY = 'abc';

const BASE = "http://localhost:4000/v1";


if (!API_KEY) {
  console.error("Missing");
  process.exit(1);
}

const ENDPOINTS = {
  // POST — Payment Link Creation
  onetime:              { method: "POST", path: "/test/onetime" }
};

// Fields used only for URL construction — strip from body/query
const ID_FIELD = "id";


function buildUrl(path, data) {
  if (path.includes(":id")) {
    if (!data?.id) throw new Error(`Missing required field: id`);
    return path.replace(":id", encodeURIComponent(data.id));
  }
  return path;
}

function buildQueryString(type, data) {
  const allowed = GET_QUERY_FIELDS[type];
  if (!allowed || !data) return "";
  const params = new URLSearchParams();
  for (const key of allowed) {
    if (data[key] !== undefined && data[key] !== null) {
      params.set(key, data[key]);
    }
  }
  const qs = params.toString();
  return qs ? `?${qs}` : "";
}

function buildBody(type, data) {
  if (!data) return undefined;
  const { id, ...rest } = data; // always strip id — it lives in the URL
  return Object.keys(rest).length > 0 ? JSON.stringify(rest) : undefined;
}

async function main() {
  const raw = process.argv[2];
  if (!raw) throw new Error("No payload provided. Pass JSON as first argument.");

  const { type, data } = JSON.parse(raw);
  if (!type) throw new Error("Missing 'type' in payload.");

  const endpoint = ENDPOINTS[type];
  if (!endpoint) throw new Error(`Unsupported type: "${type}"`);

  const { method, path } = endpoint;

  const resolvedPath = buildUrl(path, data);
  const queryString  = method === "GET" ? buildQueryString(type, data) : "";
  const url          = `${BASE}${resolvedPath}${queryString}`;
  const body         = method !== "GET" ? buildBody(type, data) : undefined;

  const res = await fetch(url, {
    method,
    headers: {
      "Content-Type": "application/json",
    },
    ...(body ? { body } : {}),
  });

  const json = await res.json();
  console.log(JSON.stringify(json, null, 2));
}

main().catch((e) => {
  console.error(e.message);
  process.exit(1);
});
