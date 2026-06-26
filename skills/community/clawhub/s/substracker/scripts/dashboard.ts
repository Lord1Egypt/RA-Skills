// Dashboard command
import { api } from "./client";

export async function stats() {
  return api("GET", "/api/dashboard/stats");
}
