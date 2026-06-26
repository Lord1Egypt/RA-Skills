/**
 * WALVIS - Walrus Autonomous Learning & Vibe Intelligence System
 * TypeScript types for data model
 */

export type ItemType = 'link' | 'text' | 'image' | 'note';
export type ItemSource = 'telegram' | 'web' | 'manual';

export interface BookmarkItem {
  id: string;
  type: ItemType;
  url?: string;
  title: string;
  summary: string;
  tags: string[];
  content: string;
  screenshotBlobId?: string | null;
  screenshotPath?: string; // Local path to screenshot before sync
  notes: string;
  createdAt: string;
  updatedAt: string;
  source: ItemSource;
  analyzedBy: string;
}

export interface SealConfig {
  encrypted: boolean;
  packageId: string;          // Move package ID for access_policy
  policyObjectId: string;     // Shared SpaceAccess object ID on Sui
  allowlist: string[];         // Addresses with decrypt access
  backupKey?: string;          // Base64-encoded backup key for emergency recovery
}

export interface Space {
  id: string;
  name: string;
  description: string;
  items: BookmarkItem[];
  createdAt: string;
  updatedAt: string;
  walrusBlobId?: string;
  syncedAt?: string;
  seal?: SealConfig;
}

export interface ManifestItemIndex {
  spaceId: string;
  url?: string;
  title: string;
  screenshotBlobId?: string | null;
  screenshotPath?: string;
  tags: string[];
  updatedAt: string;
}

export interface ManifestSpaceEntry {
  name: string;
  blobId?: string;
  syncedAt?: string;
  updatedAt: string;
  encrypted?: boolean;
  policyObjectId?: string;    // Sui object ID for SpaceAccess
}

export interface Manifest {
  agent: string;
  activeSpace: string;
  network: string;
  walrusPublisher: string;
  walrusAggregator: string;
  spaces: Record<string, ManifestSpaceEntry>;
  items: Record<string, ManifestItemIndex>;
  manifestBlobId?: string;
  lastSyncAt?: string;
  suiAddress?: string;
  llmEndpoint?: string;
  llmModel?: string;
  sealPackageId?: string;     // Deployed access_policy package ID
}

export interface AnalysisResult {
  title: string;
  summary: string;
  tags: string[];
  type: ItemType;
  content_snippet: string;
}

export interface WalrusUploadResponse {
  newlyCreated?: {
    blobObject: {
      blobId: string;
      id: string;
    };
  };
  alreadyCertified?: {
    blobId: string;
  };
}
