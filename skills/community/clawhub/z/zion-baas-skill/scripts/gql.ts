import { GraphQLClient } from "graphql-request";
import fs from "fs";
import path from "path";
import yaml from "js-yaml";

async function run() {
  const args = process.argv.slice(2);
  if (args.length < 3) {
    console.error("Usage: npm run gql -- <projectExId> <role> '<query_string>' [variables_json_string]");
    console.error("role can be 'admin', 'anonymous', or a specific 'user_id'");
    process.exit(1);
  }

  const [projectExId, role, query, variablesJson] = args;

  let variables = {};
  if (variablesJson) {
    try {
      variables = JSON.parse(variablesJson);
    } catch (e) {
      console.error("Failed to parse variables JSON string");
      process.exit(1);
    }
  }

  let token = "";
  if (role !== "anonymous") {
    const credentialsPath = path.resolve(process.cwd(), ".zion/credentials.yaml");
    if (!fs.existsSync(credentialsPath)) {
      console.error(`Credentials file not found at ${credentialsPath}. Please run auth/fetch-token first.`);
      process.exit(1);
    }
    const fileContents = fs.readFileSync(credentialsPath, "utf8");
    const data = yaml.load(fileContents) as any;

    if (role === "admin") {
      token = data?.project?.admin_token?.token;
    } else {
      const user = data?.project?.other_users?.find((u: any) => u.user_id === role);
      token = user?.token?.token;
    }

    if (!token) {
      console.error(`Could not find token for role: ${role}`);
      process.exit(1);
    }
  }

  const endpoint = `https://zion-app.functorz.com/zero/${projectExId}/api/graphql-v2`;
  const headers: Record<string, string> = {};
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const client = new GraphQLClient(endpoint, { headers });

  try {
    const result = await client.request(query, variables);
    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error("GraphQL Request Failed:");
    console.error(error);
    process.exit(1);
  }
}

run();
