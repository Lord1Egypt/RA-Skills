import { GraphQLClient, gql } from "graphql-request";
import fs from "fs";
import path from "path";
import yaml from "js-yaml";

/**
 * Fetch the runtime backend token (data visualizer token) for a given Zion project.
 * 
 * @param projectExId The project's unique execution ID.
 * @param developerJwtToken The developer token acquired from OAuth authentication.
 * @returns The runtime backend admin token and zeroUrl.
 */
export async function fetchRuntimeToken(projectExId: string, developerJwtToken: string): Promise<{ adminToken: string, zeroUrl: string, projectName: string }> {
  const FETCH_DATA_VISUALIZER = gql`
    query FetchDataVisualizer($projectExId: String!, $appExId: String, $appVersionExId: String) {
      fetchAppDetailByExId(
        projectExId: $projectExId
        appExId: $appExId
        appVersionExId: $appVersionExId
      ) {
        appType
        ... on WebApp {
          project {
            name
            dataVisualizers { token zeroUrl zeroSubscriptionUrl }
          }
        }
        ... on WechatMiniProgramApp {
          project {
            name
            dataVisualizers { token zeroUrl zeroSubscriptionUrl }
          }
        }
        ... on Project {
          name
          dataVisualizers { token zeroUrl zeroSubscriptionUrl }
        }
      }
    }
  `;

  // Meta API Endpoint
  const metaClient = new GraphQLClient("https://zionbackend.functorz.com/api/graphql", {
    headers: {
      Authorization: `Bearer ${developerJwtToken}`,
      "x-zed-version": "2.0.5",
    },
  });

  // Fetch Data Visualizer (Runtime Backend Admin Token)
  console.log(`Fetching runtime backend token for project: ${projectExId}...`);
  const dvData = await metaClient.request<any>(FETCH_DATA_VISUALIZER, { projectExId });
  
  const projectDetail = dvData.fetchAppDetailByExId.project || dvData.fetchAppDetailByExId;
  const visualizer = projectDetail.dataVisualizers?.[0];

  if (!visualizer) {
    throw new Error("Could not find data visualizers for the provided projectExId.");
  }

  const adminToken = visualizer.token;
  const zeroUrl = visualizer.zeroUrl || `https://zion-app.functorz.com/zero/${projectExId}/api/graphql-v2`;
  const projectName = projectDetail.name || "Unknown Project";

  return { adminToken, zeroUrl, projectName };
}

function getJwtExpiry(token: string): string {
  try {
    const payloadBase64 = token.split('.')[1];
    const payloadJson = Buffer.from(payloadBase64, 'base64').toString('utf8');
    const payload = JSON.parse(payloadJson);
    if (payload.exp) {
      return new Date(payload.exp * 1000).toISOString();
    }
  } catch (e) {
    // Ignore invalid JWTs
  }
  return "unknown";
}

// Example usage when run directly
if (import.meta.url === `file://${process.argv[1]}`) {
  const [, , projectExId] = process.argv;
  
  if (!projectExId) {
    console.error("Usage: npm run fetch-token -- <projectExId>");
    process.exit(1);
  }

  // Attempt to load developer token from credentials.yaml
  const credentialsDir = path.resolve(process.cwd(), ".zion");
  const credentialsPath = path.join(credentialsDir, "credentials.yaml");
  
  let data: any = {};
  let developerJwtToken = "";

  if (fs.existsSync(credentialsPath)) {
    try {
      const fileContents = fs.readFileSync(credentialsPath, "utf8");
      data = yaml.load(fileContents) || {};
      if (data?.developer_token?.token) {
        developerJwtToken = data.developer_token.token;
      }
    } catch (e) {
      console.error("Failed to parse credentials file.", e);
    }
  }

  if (!developerJwtToken) {
    console.error(`Could not find a valid developer_token in ${credentialsPath}. Please run the auth script first.`);
    process.exit(1);
  }

  fetchRuntimeToken(projectExId, developerJwtToken)
    .then(({ adminToken, zeroUrl, projectName }) => {
      console.log("Successfully retrieved runtime admin token.");
      
      data.project = data.project || {};
      data.project.exId = projectExId;
      data.project.name = projectName;
      data.project.admin_token = {
        token: adminToken,
        expiry: getJwtExpiry(adminToken)
      };

      if (!data.project.other_users) {
        data.project.other_users = [];
      }
      
      if (!fs.existsSync(credentialsDir)) {
        fs.mkdirSync(credentialsDir, { recursive: true });
      }
      fs.writeFileSync(credentialsPath, yaml.dump(data));
      
      console.log(`Admin token written to ${credentialsPath}`);
      console.log(`Zero URL: ${zeroUrl}`);
      process.exit(0);
    })
    .catch((error) => {
      console.error("Error fetching runtime token:", error);
      process.exit(1);
    });
}
