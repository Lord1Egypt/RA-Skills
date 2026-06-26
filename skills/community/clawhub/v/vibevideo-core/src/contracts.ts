export const HTTP_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH"] as const;
export type HttpMethod = (typeof HTTP_METHODS)[number];

export const RESPONSE_CONTRACTS = ["standard", "legacy", "typed", "redirect", "planned"] as const;
export type ResponseContract = (typeof RESPONSE_CONTRACTS)[number];

export const PROVIDER_TRANSPORTS = ["redirect", "embedded", "popup", "server_proxy", "server_only"] as const;
export type ProviderTransport = (typeof PROVIDER_TRANSPORTS)[number];

export const AUTH_STRATEGIES = [
  "oauth_redirect",
  "email_link",
  "email_code",
  "session_handoff",
  "internal_service",
] as const;
export type AgentAuthStrategy = (typeof AUTH_STRATEGIES)[number];

export const CAPABILITY_CATEGORIES = [
  "auth",
  "identity",
  "access",
  "scripts",
  "tools",
  "assets",
  "projects",
  "notifications",
  "agent_bridge",
  "service",
] as const;
export type CapabilityCategory = (typeof CAPABILITY_CATEGORIES)[number];

export const CAPABILITY_STATUSES = ["implemented", "planned", "provider_specific"] as const;
export type CapabilityStatus = (typeof CAPABILITY_STATUSES)[number];

export const AGENT_SCOPES = ["anonymous", "authenticated", "owner", "sub_user", "internal"] as const;
export type AgentScope = (typeof AGENT_SCOPES)[number];

export const AGENT_LAUNCHERS = ["redirect", "embedded", "popup", "server_only"] as const;
export type AgentLauncher = (typeof AGENT_LAUNCHERS)[number];

export const BRIDGE_MODES = ["backend_only", "frontend_callback", "hybrid"] as const;
export type BridgeMode = (typeof BRIDGE_MODES)[number];

export const AUDIT_EVENTS = [
  "session_issued",
  "session_exchanged",
  "capability_denied",
  "provider_callback_received",
  "task_started",
  "task_completed",
] as const;
export type AgentAuditEventName = (typeof AUDIT_EVENTS)[number];

export interface AgentRouteBinding {
  method: HttpMethod;
  path: string;
  responseContract: ResponseContract;
  localeHeader?: boolean;
  notes?: string;
}

export interface AgentCapabilityDescriptor {
  key: string;
  title: string;
  category: CapabilityCategory;
  status: CapabilityStatus;
  scopes: ReadonlyArray<AgentScope>;
  route?: AgentRouteBinding;
  dependsOn?: ReadonlyArray<string>;
  tags?: ReadonlyArray<string>;
  notes?: string;
}

export interface AgentAuthSurface {
  primaryStrategy: AgentAuthStrategy;
  fallbackStrategies?: ReadonlyArray<AgentAuthStrategy>;
  login?: AgentRouteBinding;
  verify?: AgentRouteBinding;
  callback?: AgentRouteBinding;
  currentUser?: AgentRouteBinding;
  cookieSetup?: AgentRouteBinding;
  sessionBrokerPath?: string;
  bridgeTokenTtlSeconds?: number;
  neverSharePrimaryCookie: boolean;
}

export interface AgentProviderUi {
  launcher: AgentLauncher;
  entryPath?: string;
  callbackPath?: string;
}

export interface AgentProviderSecurity {
  bridgeMode: BridgeMode;
  auditEventNamespace: string;
  requiresAuditTrail: boolean;
  allowedOrigins?: ReadonlyArray<string>;
}

export interface AgentProviderManifest {
  providerId: string;
  displayName: string;
  providerUrl?: string;
  transport: ProviderTransport;
  auth: AgentAuthSurface;
  capabilities: ReadonlyArray<string>;
  requiredScopes: ReadonlyArray<AgentScope>;
  extensionPoints?: ReadonlyArray<CapabilityCategory>;
  ui: AgentProviderUi;
  security: AgentProviderSecurity;
  notes?: string;
}

export interface AgentBridgeSessionGrant {
  providerId: string;
  ownerUserId: string;
  subUserId?: string | null;
  tokenId?: string | null;
  locale: string;
  capabilityKeys: ReadonlyArray<string>;
  scopes: ReadonlyArray<AgentScope>;
  expiresAt: string;
  callbackUrl?: string;
  nonce: string;
}

export interface AgentBridgeAuditEvent {
  providerId: string;
  event: AgentAuditEventName;
  ownerUserId: string;
  subUserId?: string | null;
  tokenId?: string | null;
  timestamp: string;
  metadata?: Record<string, unknown>;
}
