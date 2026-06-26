interface SkillContext {
    userMessage: {
        content: string;
        attachments?: Array<{
            type?: string;
            path: string;
            filename?: string;
        }>;
    };
    config?: any;
    tools: {
        exec: (options: {
            command: string;
            timeout?: number;
        }) => Promise<{
            stdout: string;
            stderr: string;
        }>;
    };
}
interface SkillResult {
    message: string;
    data?: any;
}
interface Skill {
    name: string;
    description: string;
    execute(context: SkillContext): Promise<SkillResult>;
}
export default class StardotsBackupSkill implements Skill {
    name: string;
    description: string;
    execute(context: SkillContext): Promise<SkillResult>;
    private getConfig;
    private generateSign;
    private generateNonce;
    private uploadImage;
}
export {};
//# sourceMappingURL=index.d.ts.map