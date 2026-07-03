#!/usr/bin/env node
/**
 * ClawCompany - OpenClaw 虚拟团队协作系统
 */
interface Task {
    id: string;
    title: string;
    description: string;
    assignedTo: 'dev' | 'review';
    dependencies: string[];
}
interface ProjectResult {
    success: boolean;
    tasks: Task[];
    files: string[];
    summary: string;
}
/**
 * 创建项目（主入口）
 */
export declare function createProject(userRequest: string, projectPath?: string, options?: any): Promise<ProjectResult>;
/**
 * PM Agent - 分析需求并拆分任务
 */
declare function runPMAgent(userRequest: string, config: any): Promise<Task[]>;
/**
 * Dev Agent - 实现任务
 */
declare function runDevAgent(task: Task, projectPath: string, config: any): Promise<string[]>;
/**
 * Review Agent - 审查代码
 */
declare function runReviewAgent(task: Task, files: string[], config: any): Promise<boolean>;
export { runPMAgent, runDevAgent, runReviewAgent };
