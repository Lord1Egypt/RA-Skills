import type { ScrapedTable } from '../types.js';

export class TableExtractor {
  extract(html: string, url: string): ScrapedTable {
    // Parse HTML table
    const rows: Record<string, string | number>[] = [];
    const headers: string[] = [];

    // Extract headers
    const headerMatch = html.match(/<th[^>]*>([^<]*)<\/th>/gi);
    if (headerMatch) {
      headerMatch.forEach(th => {
        const text = th.replace(/<[^>]+>/g, '').trim();
        if (text) headers.push(text);
      });
    }

    // Extract rows
    const rowMatches = html.match(/<tr[^>]*>(.*?)<\/tr>/gis);
    if (rowMatches) {
      for (const rowHtml of rowMatches) {
        const cellMatches = rowHtml.match(/<td[^>]*>([^<]*)<\/td>/gi);
        if (cellMatches && cellMatches.length > 0) {
          const row: Record<string, string | number> = {};
          cellMatches.forEach((td, index) => {
            const text = td.replace(/<[^>]+>/g, '').trim();
            const header = headers[index] || `col${index}`;
            
            // Try to parse as number
            const numValue = parseFloat(text.replace(/[$,]/g, ''));
            row[header] = isNaN(numValue) ? text : numValue;
          });
          rows.push(row);
        }
      }
    }

    return {
      type: 'table',
      headers: headers.length > 0 ? headers : Object.keys(rows[0] || {}),
      rows,
      url
    };
  }
}
