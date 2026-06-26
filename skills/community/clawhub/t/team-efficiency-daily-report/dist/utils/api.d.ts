import type { Page } from "puppeteer";
interface ReportConfig {
    url: string;
    dataAPI: string;
    name?: string;
    needModify?: boolean;
    column: Record<string, string>;
}
interface FilterValue {
    startTime: number;
    endTime: number;
}
interface Payload {
    filters: Array<{
        filterValue: FilterValue;
    }>;
    [key: string]: unknown;
}
export declare function capturePayload(page: Page, reportConfig: ReportConfig): Promise<Payload>;
export declare function requestAPI(page: Page, api: string, payload: Payload, needModify?: boolean): Promise<unknown[]>;
export {};
//# sourceMappingURL=api.d.ts.map