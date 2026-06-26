import type { MatchRequest, MatchResponse, ContributeRequest, ContributeResponse, ReportFailureRequest, Logger } from "./types.js";
export declare class CloudClient {
    private endpoint;
    private timeoutMs;
    private logger;
    constructor(endpoint: string, timeoutMs: number, logger: Logger);
    match(req: MatchRequest): Promise<MatchResponse | null>;
    contribute(req: ContributeRequest): Promise<ContributeResponse | null>;
    reportFailure(req: ReportFailureRequest): Promise<void>;
}
