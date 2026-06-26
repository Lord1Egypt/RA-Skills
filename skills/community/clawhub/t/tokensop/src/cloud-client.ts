import { request } from "undici";
import type {
  MatchRequest,
  MatchResponse,
  ContributeRequest,
  ContributeResponse,
  ReportFailureRequest,
  Logger,
} from "./types.js";

export class CloudClient {
  private endpoint: string;
  private timeoutMs: number;
  private logger: Logger;

  constructor(endpoint: string, timeoutMs: number, logger: Logger) {
    this.endpoint = endpoint.replace(/\/$/, "");
    this.timeoutMs = timeoutMs;
    this.logger = logger;
  }

  async match(req: MatchRequest): Promise<MatchResponse | null> {
    try {
      const { statusCode, body } = await request(
        `${this.endpoint}/v1/lobsters/match`,
        {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify(req),
          headersTimeout: this.timeoutMs,
          bodyTimeout: this.timeoutMs,
        }
      );

      if (statusCode !== 200) {
        this.logger.warn(`Cloud match returned ${statusCode}`);
        return null;
      }

      return (await body.json()) as MatchResponse;
    } catch (err) {
      this.logger.debug(`Cloud match failed (expected on timeout/offline): ${err}`);
      return null;
    }
  }

  async contribute(req: ContributeRequest): Promise<ContributeResponse | null> {
    try {
      const { statusCode, body } = await request(
        `${this.endpoint}/v1/lobsters/contribute`,
        {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify(req),
          headersTimeout: 5000,
          bodyTimeout: 5000,
        }
      );

      if (statusCode !== 201 && statusCode !== 409) {
        this.logger.warn(`Cloud contribute returned ${statusCode}`);
        return null;
      }

      return (await body.json()) as ContributeResponse;
    } catch (err) {
      this.logger.warn(`Cloud contribute failed: ${err}`);
      return null;
    }
  }

  async reportFailure(req: ReportFailureRequest): Promise<void> {
    try {
      await request(`${this.endpoint}/v1/lobsters/report_failure`, {
        method: "PUT",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(req),
        headersTimeout: 3000,
        bodyTimeout: 3000,
      });
    } catch (err) {
      this.logger.debug(`Cloud report_failure failed: ${err}`);
    }
  }
}
