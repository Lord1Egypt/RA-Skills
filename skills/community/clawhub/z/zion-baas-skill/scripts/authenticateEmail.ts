import { GraphQLClient, gql } from "graphql-request";
import fs from "fs";
import path from "path";
import yaml from "js-yaml";

export async function authenticateWithEmail(usernameOrEmail: string, password: string): Promise<string> {
  const LOGIN_MUTATION = gql`
    mutation LoginWithUsernameOrEmail($usernameOrEmail: String!, $password: String!, $referrerPromoCode: String) {
      loginWithUsernameOrEmail(
        usernameOrEmail: $usernameOrEmail
        password: $password
        referrerPromoCode: $referrerPromoCode
      ) {
        ...AccountInfoFragment
      }
    }

    fragment AccountInfoFragment on AccountInfo {
      accessToken
      roleNames
      registeredWithinLastMinute
      account {
        exId
        displayName
        phoneNumberBindingState
      }
    }
  `;

  const metaClient = new GraphQLClient("https://zionbackend.functorz.com/api/graphql", {
    headers: {
      "Content-Type": "application/json",
      "Origin": "https://auth.functorz.com",
      "Referer": "https://auth.functorz.com/",
    },
  });

  try {
    const data = await metaClient.request<any>(LOGIN_MUTATION, { usernameOrEmail, password });
    if (!data?.loginWithUsernameOrEmail?.accessToken) {
      throw new Error("Login failed, no token returned");
    }
    return data.loginWithUsernameOrEmail.accessToken;
  } catch (err: any) {
     throw new Error(`Email authentication failed: ${err.message || err}`);
  }
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
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.error("Usage: npm run auth:email <email> <password>");
    process.exit(1);
  }

  const [email, password] = args;

  authenticateWithEmail(email, password)
    .then((token) => {
      console.log("Authentication successful.");
      
      const credentialsDir = path.resolve(process.cwd(), ".zion");
      const credentialsPath = path.join(credentialsDir, "credentials.yaml");
      
      let data: any = {};
      if (fs.existsSync(credentialsPath)) {
        try {
          data = yaml.load(fs.readFileSync(credentialsPath, "utf8")) || {};
        } catch (e) {
          console.error("Failed to parse existing credentials file, overwriting.");
        }
      }
      
      data.developer_token = {
        token: token,
        expiry: getJwtExpiry(token)
      };
      
      if (!fs.existsSync(credentialsDir)) {
        fs.mkdirSync(credentialsDir, { recursive: true });
      }
      fs.writeFileSync(credentialsPath, yaml.dump(data));
      
      console.log(`Developer token written to ${credentialsPath}`);
      process.exit(0);
    })
    .catch((error) => {
      console.error(error.message);
      process.exit(1);
    });
}
