/**
 * supabase-vault views
 *
 * Install at: ui/src/ui/views/supabase-vault.ts
 *
 * Lit HTML template for the Supabase Vault dashboard page.
 * Registered as an Integrations tab.
 */

import { html, nothing } from "lit";
import type { SupabaseVaultState, VaultSecret } from "../controllers/supabase-vault.js";

export type SupabaseVaultProps = SupabaseVaultState & {
  onLoadStatus: () => void;
  onConnect: () => void;
  onDisconnect: () => void;
  onAddSecret: () => void;
  onDeleteSecret: (name: string) => void;
  onMigrate: () => void;
  onSetupUrlChange: (v: string) => void;
  onSetupKeyChange: (v: string) => void;
  onToggleShowKey: () => void;
  onToggleAddForm: () => void;
  onAddNameChange: (v: string) => void;
  onAddValueChange: (v: string) => void;
};

const SETUP_SQL_PREVIEW = `-- Run once in Supabase SQL Editor
CREATE EXTENSION IF NOT EXISTS vault WITH SCHEMA vault;
-- (then paste full contents of assets/setup.sql)`;

export function renderSupabaseVault(p: SupabaseVaultProps) {
  return html`
    <div class="page-body" style="max-width:780px;">

      <!-- Title bar -->
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;">
        <div>
          <h2 style="margin:0;font-size:18px;font-weight:600;">🔐 Supabase Vault</h2>
          <div style="font-size:12px;color:var(--text-muted);margin-top:4px;">
            AES-256 encrypted secret storage in your Supabase Postgres database
          </div>
        </div>
        <button
          class="btn btn-ghost btn-sm"
          @click=${p.onLoadStatus}
          ?disabled=${p.svLoading}
          title="Refresh status"
        >↻</button>
      </div>

      <!-- Message banner -->
      ${p.svMessage ? html`
        <div style="
          margin-bottom:14px;padding:10px 14px;border-radius:8px;font-size:13px;
          background:${p.svMessage.kind === "success" ? "var(--bg-success,#0d2b1a)" : "var(--bg-error,#2b0d0d)"};
          color:${p.svMessage.kind === "success" ? "var(--text-success,#3fb950)" : "var(--text-error,#f85149)"};
          border:1px solid ${p.svMessage.kind === "success" ? "var(--border-success,#238636)" : "var(--border-error,#da3633)"};
        ">
          ${p.svMessage.kind === "success" ? "✓" : "✗"} ${p.svMessage.text}
        </div>
      ` : nothing}

      <!-- Status card -->
      <section class="card" style="margin-bottom:16px;">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
          <div>
            <div class="card-title" style="margin-bottom:6px;">Connection Status</div>
            ${p.svLoading ? html`
              <span style="font-size:13px;color:var(--text-muted);">Checking…</span>
            ` : p.svConnected ? html`
              <div style="display:flex;align-items:center;gap:8px;">
                <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#3fb950;"></span>
                <span style="font-size:13px;color:var(--text-success,#3fb950);font-weight:600;">Connected</span>
                <span style="font-size:12px;color:var(--text-muted);">
                  ${p.svUrl} · ${p.svKeyCount} secret${p.svKeyCount !== 1 ? "s" : ""}
                </span>
              </div>
              <div style="font-size:11px;color:var(--text-muted);margin-top:4px;">
                Keychain: <code>${p.svMethod}</code>
              </div>
            ` : html`
              <div style="display:flex;align-items:center;gap:8px;">
                <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--text-muted);"></span>
                <span style="font-size:13px;color:var(--text-muted);">Not connected</span>
              </div>
            `}
          </div>
          ${p.svConnected ? html`
            <button class="btn btn-ghost btn-sm" style="color:var(--text-error,#f85149);"
              @click=${p.onDisconnect}>
              Disconnect
            </button>
          ` : nothing}
        </div>
      </section>

      <!-- Setup card (shown when not connected) -->
      ${!p.svConnected ? html`
        <section class="card" style="margin-bottom:16px;">
          <div class="card-title" style="margin-bottom:14px;">Connect to Supabase</div>

          <div style="margin-bottom:16px;padding:10px 14px;background:var(--bg-surface,#0d1117);border:1px solid var(--border,#30363d);border-radius:8px;font-size:12px;color:var(--text-muted);">
            ℹ️ You need a Supabase project. Get your Project URL and service_role key from
            <a href="https://supabase.com/dashboard/project/_/settings/api" target="_blank"
              style="color:var(--text-link,#58a6ff);">Settings → API</a>.
            Run <code>assets/setup.sql</code> in the SQL Editor first.
          </div>

          <label style="display:block;margin-bottom:12px;">
            <div style="font-size:12px;color:var(--text-muted);margin-bottom:4px;">Project URL</div>
            <input
              type="url"
              class="input"
              placeholder="https://abcxyz.supabase.co"
              .value=${p.svSetupUrl}
              @input=${(e: Event) => p.onSetupUrlChange((e.target as HTMLInputElement).value)}
              style="width:100%;font-family:monospace;font-size:13px;"
            />
          </label>

          <label style="display:block;margin-bottom:16px;">
            <div style="font-size:12px;color:var(--text-muted);margin-bottom:4px;">Service Role Key</div>
            <div style="position:relative;">
              <input
                .type=${p.svShowKey ? "text" : "password"}
                class="input"
                placeholder="eyJhbGci…"
                .value=${p.svSetupKey}
                @input=${(e: Event) => p.onSetupKeyChange((e.target as HTMLInputElement).value)}
                style="width:100%;font-family:monospace;font-size:13px;padding-right:48px;"
              />
              <button
                class="btn btn-ghost btn-sm"
                @click=${p.onToggleShowKey}
                style="position:absolute;right:6px;top:50%;transform:translateY(-50%);padding:2px 6px;"
                title="${p.svShowKey ? "Hide" : "Show"}"
              >${p.svShowKey ? "👁" : "👁‍🗨"}</button>
            </div>
          </label>

          ${p.svError ? html`
            <div style="margin-bottom:12px;font-size:12px;color:var(--text-error,#f85149);">✗ ${p.svError}</div>
          ` : nothing}

          <button
            class="btn btn-primary"
            @click=${p.onConnect}
            ?disabled=${p.svConnecting || !p.svSetupUrl || !p.svSetupKey}
          >
            ${p.svConnecting ? "Connecting…" : "Connect & Test"}
          </button>
        </section>

        <!-- SQL Setup instructions -->
        <section class="card" style="margin-bottom:16px;">
          <div class="card-title" style="margin-bottom:10px;">Step 1 — Run SQL Setup</div>
          <div style="font-size:12px;color:var(--text-muted);margin-bottom:10px;">
            Run this in your Supabase project's
            <a href="https://supabase.com/dashboard/project/_/sql" target="_blank"
              style="color:var(--text-link,#58a6ff);">SQL Editor</a>
            to create the required vault wrapper functions:
          </div>
          <pre style="
            background:var(--bg-surface,#0d1117);border:1px solid var(--border,#30363d);
            border-radius:6px;padding:12px;font-size:11px;line-height:1.5;
            overflow-x:auto;color:var(--text-code,#e6edf3);margin:0;
          ">${SETUP_SQL_PREVIEW}</pre>
          <div style="margin-top:8px;font-size:11px;color:var(--text-muted);">
            Full SQL is in <code>~/.openclaw/skills/supabase-vault/assets/setup.sql</code>
          </div>
        </section>
      ` : nothing}

      <!-- Secrets list (shown when connected) -->
      ${p.svConnected ? html`
        <section class="card" style="margin-bottom:16px;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
            <div class="card-title">Vault Secrets (${p.svSecrets.length})</div>
            <button class="btn btn-sm btn-ghost" @click=${p.onToggleAddForm}
              style="${p.svShowAdd ? "color:var(--text-muted);" : ""}">
              ${p.svShowAdd ? "✕ Cancel" : "+ Add Secret"}
            </button>
          </div>

          <!-- Add secret form -->
          ${p.svShowAdd ? html`
            <div style="
              margin-bottom:14px;padding:14px;
              background:var(--bg-surface,#0d1117);border:1px solid var(--border,#30363d);
              border-radius:8px;
            ">
              <div style="display:flex;gap:8px;margin-bottom:8px;">
                <input
                  class="input"
                  placeholder="KEY_NAME"
                  .value=${p.svAddName}
                  @input=${(e: Event) => p.onAddNameChange((e.target as HTMLInputElement).value)}
                  style="flex:1;font-family:monospace;font-size:13px;"
                />
                <input
                  type="password"
                  class="input"
                  placeholder="Secret value"
                  .value=${p.svAddValue}
                  @input=${(e: Event) => p.onAddValueChange((e.target as HTMLInputElement).value)}
                  style="flex:2;font-family:monospace;font-size:13px;"
                />
              </div>
              <button
                class="btn btn-primary btn-sm"
                @click=${p.onAddSecret}
                ?disabled=${p.svAddBusy || !p.svAddName || !p.svAddValue}
              >${p.svAddBusy ? "Saving…" : "Save to Vault"}</button>
            </div>
          ` : nothing}

          <!-- Secrets table -->
          ${p.svSecretsLoading ? html`
            <div style="color:var(--text-muted);font-size:13px;">Loading…</div>
          ` : p.svSecrets.length === 0 ? html`
            <div style="color:var(--text-muted);font-size:13px;text-align:center;padding:20px 0;">
              No secrets yet. Add one above or migrate from local vault below.
            </div>
          ` : html`
            <div style="display:flex;flex-direction:column;gap:2px;">
              ${p.svSecrets.map((s: VaultSecret) => html`
                <div style="
                  display:flex;align-items:center;justify-content:space-between;
                  padding:8px 10px;border-radius:6px;
                  border:1px solid var(--border,#30363d);
                  background:var(--bg-surface,#0d1117);
                ">
                  <div style="display:flex;align-items:center;gap:8px;">
                    <span style="color:var(--text-success,#3fb950);font-size:11px;">☁️</span>
                    <code style="font-size:13px;">${s.name}</code>
                  </div>
                  <button
                    class="btn btn-ghost btn-sm"
                    style="color:var(--text-error,#f85149);padding:2px 8px;"
                    @click=${() => {
                      if (confirm(`Delete secret "${s.name}" from Supabase Vault?`)) {
                        p.onDeleteSecret(s.name);
                      }
                    }}
                  >Delete</button>
                </div>
              `)}
            </div>
          `}
        </section>

        <!-- Migrate from local vault -->
        <section class="card" style="margin-bottom:16px;">
          <div class="card-title" style="margin-bottom:8px;">Migrate from Local Vault</div>
          <div style="font-size:12px;color:var(--text-muted);margin-bottom:14px;">
            Move all keys from <code>~/.openclaw/secrets.json</code> to Supabase Vault.
            SecretRefs in <code>openclaw.json</code> will be updated automatically.
            Requires a gateway restart after migration.
          </div>
          <button
            class="btn btn-secondary"
            @click=${p.onMigrate}
            ?disabled=${p.svMigrating}
          >${p.svMigrating ? "Migrating…" : "🔄 Migrate from Local Vault"}</button>
          ${p.svMigrateOutput ? html`
            <pre style="
              margin-top:10px;padding:10px;background:var(--bg-surface,#0d1117);
              border:1px solid var(--border,#30363d);border-radius:6px;
              font-size:11px;line-height:1.5;overflow-x:auto;white-space:pre-wrap;
              color:var(--text-code,#e6edf3);max-height:200px;
            ">${p.svMigrateOutput}</pre>
          ` : nothing}
        </section>
      ` : nothing}

      <!-- Footer note -->
      <div style="font-size:11px;color:var(--text-muted);text-align:center;padding:8px 0;">
        Secrets stored encrypted in Supabase Vault (AES-256/libsodium).
        Bootstrap credentials protected by ${p.svMethod || "AES-256-GCM"}.
        The AI agent never sees your keys.
      </div>

    </div>
  `;
}
