import { StardotsConfig, UploadResult, ListResult } from './types';
export declare class StardotsClient {
    private client;
    private config;
    private readonly baseURL;
    constructor(config: StardotsConfig);
    private generateNonce;
    private generateSign;
    private getAuthHeaders;
    uploadImage(imagePath: string, space?: string, metadata?: Record<string, any>): Promise<UploadResult>;
    listFiles(params: {
        page?: number;
        pageSize?: number;
        space?: string;
    }): Promise<ListResult>;
    deleteFile(fileId: string, space?: string): Promise<boolean>;
}
//# sourceMappingURL=stardots-client.d.ts.map