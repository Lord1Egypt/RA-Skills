interface SkillContext {
    userMessage: {
        content: string;
    };
    config: Record<string, any>;
}
interface SkillResult {
    success: boolean;
    message: string;
    data?: any;
    error?: string;
    suggestActions?: string[];
}
export default class StardotsBackupSkill {
    name: string;
    description: string;
    version: string;
    private client;
    private config;
    initialize(config: Record<string, any>): Promise<void>;
    execute(context: SkillContext): Promise<SkillResult>;
    private matchUploadIntent;
    private matchListIntent;
    private handleUpload;
    private handleList;
    private getHelpMessage;
}
export {};
//# sourceMappingURL=index.d.ts.map