import axios, { AxiosInstance, AxiosError } from 'axios';
import { CliError } from './errors.js';

const DEFAULT_TIMEOUT = 30000;

export interface ClientConfig {
  baseUrl?: string;
  timeout?: number;
  apiKey?: string;
}

export function createHttpClient(config: ClientConfig = {}): AxiosInstance {
  const baseUrl = config.baseUrl || 'https://api.tokenrip.com';
  const headers: Record<string, string> = {};
  if (config.apiKey) {
    headers['Authorization'] = `Bearer ${config.apiKey}`;
  }

  const client = axios.create({
    baseURL: baseUrl,
    timeout: config.timeout || DEFAULT_TIMEOUT,
    headers,
  });

  client.interceptors.response.use(
    (response) => response,
    (error: AxiosError<{ ok: boolean; error?: string; message?: string }>) => {
      if (error.response?.status === 401) {
        throw new CliError(
          'UNAUTHORIZED',
          'API key required or invalid. Run `rip auth register` to recover your key.',
        );
      }
      if (error.response?.data?.error) {
        throw new CliError(error.response.data.error, error.response.data.message || 'Unknown API error');
      }
      if (error.response?.status === 413) {
        throw new CliError('PAYLOAD_TOO_LARGE', `Payload too large — the server rejected the request body. Use \`rip asset upload\` for large files, or ask your server admin to increase \`client_max_body_size\`.`);
      }
      if (error.code === 'ECONNABORTED') {
        throw new CliError('TIMEOUT', `Request timeout while contacting ${baseUrl}`);
      }
      const status = error.response?.status;
      const details = error.code || error.message || 'Unknown error';
      const statusInfo = status ? ` (HTTP ${status})` : '';
      throw new CliError('NETWORK_ERROR', `Network error (${details}${statusInfo}) while contacting ${baseUrl}`);
    },
  );

  return client;
}
