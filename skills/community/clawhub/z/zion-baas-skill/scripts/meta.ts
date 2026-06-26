import { GraphQLClient, gql } from "graphql-request";
import fs from "fs";
import path from "path";
import yaml from "js-yaml";

const FUZZY_SEARCH_PROJECT_NAME = gql`
  query FuzzySearchProjectName(
    $projectName: String!
    $paginator: ConnectionPaginatorInput
  ) {
    fuzzySearchProjectName(projectName: $projectName, paginator: $paginator) {
      pageInfo {
        hasNextPage
        hasPreviousPage
        startCursor { value }
        endCursor { value }
      }
      edges {
        cursor { value }
        node {
          exId
          type
          name
          projectName
          collaboratorType
          hasPublished
          projectOwner
          lastOpenedAt
          isExpired
        }
      }
    }
  }
`;

const SIMPLIFIED_CAUGHT_UP_SERVER_SCHEMA = gql`
  query SimplifiedCaughtUpServerSchema($projectExId: String!) {
    project(projectExId: $projectExId) {
      simplifiedCaughtUpServerSchema {
        dataModel
        actionFlows
        apis
        zAiConfigs
      }
    }
  }
`;

async function run() {
  const args = process.argv.slice(2);
  if (args.length < 1) {
    console.error("Usage: npm run meta -- <command> [args...]");
    console.error("Commands:");
    console.error("  search-projects [projectName]   Search for projects by name (or leave empty for all)");
    console.error("  fetch-schema <projectExId>      Fetch the schema (data models, actionflows, apis) for a project");
    process.exit(1);
  }

  const [command, ...cmdArgs] = args;

  // Load developer token
  const credentialsPath = path.resolve(process.cwd(), ".zion/credentials.yaml");
  let developerToken = "";

  if (fs.existsSync(credentialsPath)) {
    try {
      const fileContents = fs.readFileSync(credentialsPath, "utf8");
      const data = yaml.load(fileContents) as any;
      if (data?.developer_token?.token) {
        developerToken = data.developer_token.token;
      }
    } catch (e) {
      console.error("Failed to parse credentials file.", e);
    }
  }

  if (!developerToken) {
    console.error(`Could not find a valid developer_token in ${credentialsPath}. Please run auth script first.`);
    process.exit(1);
  }

  const client = new GraphQLClient("https://zionbackend.functorz.com/api/graphql", {
    headers: {
      Authorization: `Bearer ${developerToken}`,
      "x-zed-version": "2.0.5",
    },
  });

  try {
    if (command === "search-projects") {
      const projectName = cmdArgs[0] || "";
      console.log(`Searching projects with name: "${projectName}"...`);
      const data = await client.request<any>(FUZZY_SEARCH_PROJECT_NAME, {
        projectName,
        paginator: { first: 20 },
      });
      
      const projects = data.fuzzySearchProjectName.edges.map((e: any) => e.node);
      console.log(JSON.stringify(projects, null, 2));

    } else if (command === "fetch-schema") {
      const projectExId = cmdArgs[0];
      if (!projectExId) {
        console.error("Error: projectExId is required for fetch-schema");
        process.exit(1);
      }
      
      console.log(`Fetching schema for project: ${projectExId}...`);
      const data = await client.request<any>(SIMPLIFIED_CAUGHT_UP_SERVER_SCHEMA, {
        projectExId,
      });

      const schema = data.project?.simplifiedCaughtUpServerSchema;
      if (!schema) {
        console.error("Schema not found or project does not exist.");
        process.exit(1);
      }

      console.log(JSON.stringify(schema, null, 2));

    } else {
      console.error(`Unknown command: ${command}`);
      process.exit(1);
    }
  } catch (error) {
    console.error(`GraphQL Request Failed for command '${command}':`);
    console.error(error);
    process.exit(1);
  }
}

run();
