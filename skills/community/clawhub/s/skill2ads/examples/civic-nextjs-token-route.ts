/**
 * Example Next.js route to fetch a Civic access token.
 *
 * Place in: app/api/civic-token/route.ts
 * Then call: GET /api/civic-token
 */
import { NextResponse } from "next/server";
import { getTokens } from "@civic/auth/nextjs";

export async function GET() {
  try {
    const tokens = await getTokens();
    if (!tokens?.accessToken) {
      return NextResponse.json(
        { error: "No Civic access token. User may not be logged in." },
        { status: 401 }
      );
    }
    return NextResponse.json({ accessToken: tokens.accessToken });
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Failed to get token." },
      { status: 500 }
    );
  }
}
