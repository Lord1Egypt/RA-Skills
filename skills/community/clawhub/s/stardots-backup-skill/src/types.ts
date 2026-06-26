export interface StardotsConfig {
  apiKey: string;
  apiSecret: string;
  space: string;
}

export interface UploadParams {
  imagePath: string;
  space?: string;
  metadata?: Record<string, any>;
}

export interface UploadResult {
  url: string;
  success: boolean;
  message?: string;
}

export interface ListFilesParams {
  page?: number;
  pageSize?: number;
  space?: string;
}

export interface FileInfo {
  id: string;
  name: string;
  url: string;
  size: number;
  createdAt: string;
  metadata?: Record<string, any>;
}

export interface ListResult {
  files: FileInfo[];
  total: number;
  page: number;
  pageSize: number;
}