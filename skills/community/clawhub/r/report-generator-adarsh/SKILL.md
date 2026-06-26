# Report Generator Skill

## Purpose
Single GPT-4.1-mini call that transforms aggregated marketing data into a structured, professional audit report. This is the ONLY AI call in the entire audit pipeline.

## Input Schema
```typescript
interface AuditData {
 input: AuditInput;
 instagram: InstagramData;
 metaAds: MetaAdsData;
 keywords: KeywordData;
 competitors: CompetitorData;
 websiteAudit: WebsiteAuditData;
 collectedAt: string;
}
```

## Output Schema
```typescript
interface MarketingReport {
 brand: string;
 generatedAt: string;
 sections: ReportSections;
 rawData: AuditData;
 reportMarkdown: string;
}
```

## API Dependencies
- **API:** OpenAI
- **Model:** `gpt-4.1-mini`
- **Auth:** `OPENAI_API_KEY`
- **Cost:** ~$0.001-0.002 per call

## Implementation Pattern
- System prompt defines the analyst persona and exact 6-section format
- User message is the full AuditData JSON
- Single API call with `max_tokens: 1500`, `temperature: 0.4`
- Response markdown is parsed into individual sections via `## ` header splitting
- Token usage is logged for cost tracking
- Fallback report is generated if OpenAI call fails

## Token Budget
- Input: ~1,500-2,000 tokens (JSON data)
- Output: ~800-1,200 tokens (report)

## Error Handling
- Missing API key: returns fallback report with error message
- API failure: returns fallback report with raw data preserved
- All errors logged with context

## Example Usage
```typescript
const report = await generateMarketingReport(auditData);
console.log(report.reportMarkdown);
```

## Notes
- This is the ONLY file that should make OpenAI calls (except competitor collector fallback)
- Never add additional GPT calls to other modules
