/**
 * supabase-vault controller
 *
 * Install at: ui/src/ui/controllers/supabase-vault.ts
 *
 * Manages all state and gateway RPC calls for the Supabase Vault dashboard page.
 */

import type { GatewayBrowserClient } from "../gateway";

export type VaultSecret = { name: string; id: string };

export type SupabaseVaultState = {
  client: GatewayBrowserClient | null;
  connected: boolean;

  // Status
  svLoading: boolean;
  svConnected: boolean;
  svMethod: string;
  svUrl: string;
  svKeyCount: number;
  svError: string | null;

  // Secrets list
  svSecrets: VaultSecret[];
  svSecretsLoading: boolean;

  // Setup form
  svSetupUrl: string;
  svSetupKey: string;
  svShowKey: boolean;
  svConnecting: boolean;

  // Add secret form
  svShowAdd: boolean;
  svAddName: string;
  svAddValue: string;
  svAddBusy: boolean;

  // Migrate
  svMigrating: boolean;
  svMigrateOutput: string | null;

  // Messages
  svMessage: { kind: "success" | "error"; text: string } | null;
};

function initialState(): Partial<SupabaseVaultState> {
  return {
    svLoading: false,
    svConnected: false,
    svMethod: "",
    svUrl: "",
    svKeyCount: 0,
    svError: null,
    svSecrets: [],
    svSecretsLoading: false,
    svSetupUrl: "",
    svSetupKey: "",
    svShowKey: false,
    svConnecting: false,
    svShowAdd: false,
    svAddName: "",
    svAddValue: "",
    svAddBusy: false,
    svMigrating: false,
    svMigrateOutput: null,
    svMessage: null,
  };
}

function showMsg(
  setState: (s: Partial<SupabaseVaultState>) => void,
  kind: "success" | "error",
  text: string,
) {
  setState({ svMessage: { kind, text } });
  setTimeout(() => setState({ svMessage: null }), 4000);
}

// ─── Exported controller ──────────────────────────────────────────────────────

export function createSupabaseVaultController(
  getState: () => SupabaseVaultState,
  setState: (s: Partial<SupabaseVaultState>) => void,
) {
  async function loadStatus() {
    const { client } = getState();
    if (!client) return;
    setState({ svLoading: true, svError: null });
    try {
      const res = await client.request("supabase-vault.status", {});
      const data = res as {
        ok: boolean; connected: boolean; method: string; url: string; keyCount: number;
      };
      setState({
        svConnected: data.connected,
        svMethod: data.method || "",
        svUrl: data.url || "",
        svKeyCount: data.keyCount || 0,
        svLoading: false,
      });
      if (data.connected) {
        await loadSecrets();
      }
    } catch (e) {
      setState({ svError: String(e), svLoading: false });
    }
  }

  async function loadSecrets() {
    const { client } = getState();
    if (!client) return;
    setState({ svSecretsLoading: true });
    try {
      const res = await client.request("supabase-vault.list", {});
      const data = res as { ok: boolean; secrets: VaultSecret[] };
      setState({ svSecrets: data.secrets || [], svSecretsLoading: false });
    } catch (e) {
      setState({ svSecretsLoading: false, svError: String(e) });
    }
  }

  async function connect() {
    const { client, svSetupUrl, svSetupKey } = getState();
    if (!client) return;
    if (!svSetupUrl.trim() || !svSetupKey.trim()) {
      showMsg(setState, "error", "Project URL and service role key are required.");
      return;
    }
    setState({ svConnecting: true, svError: null });
    try {
      const res = await client.request("supabase-vault.connect", {
        url: svSetupUrl.trim(),
        serviceRoleKey: svSetupKey.trim(),
      });
      const data = res as { ok: boolean; method: string; url: string };
      setState({
        svConnected: true,
        svMethod: data.method,
        svUrl: data.url,
        svSetupKey: "",
        svConnecting: false,
      });
      showMsg(setState, "success", `Connected via ${data.method}. Gateway restart required.`);
      await loadStatus();
    } catch (e) {
      setState({ svError: String(e), svConnecting: false });
      showMsg(setState, "error", String(e));
    }
  }

  async function disconnect() {
    const { client } = getState();
    if (!client) return;
    try {
      await client.request("supabase-vault.disconnect", {});
      setState({
        svConnected: false,
        svMethod: "",
        svUrl: "",
        svKeyCount: 0,
        svSecrets: [],
      });
      showMsg(setState, "success", "Disconnected from Supabase Vault.");
    } catch (e) {
      showMsg(setState, "error", String(e));
    }
  }

  async function addSecret() {
    const { client, svAddName, svAddValue } = getState();
    if (!client) return;
    if (!svAddName.trim() || !svAddValue.trim()) {
      showMsg(setState, "error", "Name and value are required.");
      return;
    }
    setState({ svAddBusy: true });
    try {
      await client.request("supabase-vault.write", {
        name: svAddName.trim(),
        value: svAddValue.trim(),
      });
      setState({ svAddName: "", svAddValue: "", svShowAdd: false, svAddBusy: false });
      showMsg(setState, "success", `Secret "${svAddName.trim()}" saved to Supabase Vault.`);
      await loadSecrets();
    } catch (e) {
      setState({ svAddBusy: false });
      showMsg(setState, "error", String(e));
    }
  }

  async function deleteSecret(name: string) {
    const { client } = getState();
    if (!client) return;
    try {
      await client.request("supabase-vault.delete", { name });
      showMsg(setState, "success", `Secret "${name}" deleted.`);
      await loadSecrets();
    } catch (e) {
      showMsg(setState, "error", String(e));
    }
  }

  async function migrate() {
    const { client } = getState();
    if (!client) return;
    setState({ svMigrating: true, svMigrateOutput: null });
    try {
      const res = await client.request("supabase-vault.migrate", {});
      const data = res as { ok: boolean; output: string };
      setState({ svMigrating: false, svMigrateOutput: data.output || "Done." });
      showMsg(setState, "success", "Migration complete. Restart gateway to apply.");
      await loadSecrets();
    } catch (e) {
      setState({ svMigrating: false, svMigrateOutput: String(e) });
      showMsg(setState, "error", String(e));
    }
  }

  return {
    initialState,
    loadStatus,
    loadSecrets,
    connect,
    disconnect,
    addSecret,
    deleteSecret,
    migrate,
  };
}
