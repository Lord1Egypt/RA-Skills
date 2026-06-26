import { SubscriptionClient } from "subscriptions-transport-ws";
import WebSocket from "ws";
import fs from "fs";
import path from "path";
import yaml from "js-yaml";

async function run() {
  const args = process.argv.slice(2);
  if (args.length < 3) {
    console.error("Usage: npm run subscribe -- <projectExId> <role> '<query_string>' [variables_json_string]");
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

  const wssUrl = `wss://zion-app.functorz.com/zero/${projectExId}/api/graphql-subscription`;
  const connectionParams = token ? { authToken: token } : {};

  const client = new SubscriptionClient(
    wssUrl,
    {
      reconnect: true,
      connectionParams,
    },
    WebSocket as any
  );

  console.log(`Connecting to ${wssUrl} with role: ${role}...`);

  client.onConnected(() => {
    console.log("WebSocket connected. Listening for subscription events...");
  });

  client.onDisconnected(() => {
    console.log("WebSocket disconnected.");
  });

  const subscription = client.request({ query, variables }).subscribe({
    next(result) {
      console.log("\n--- Subscription Data ---");
      console.log(JSON.stringify(result, null, 2));
    },
    error(err) {
      console.error("\n--- Subscription Error ---");
      console.error(err);
      process.exit(1);
    },
    complete() {
      console.log("\n--- Subscription Completed ---");
      process.exit(0);
    },
  });

  process.on("SIGINT", () => {
    subscription.unsubscribe();
    client.close();
    process.exit(0);
  });
}

run();
