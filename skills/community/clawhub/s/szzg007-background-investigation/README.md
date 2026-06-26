# SZZG007 Background Investigation Skill - Usage Guide

## Overview
The SZZG007 Background Investigation Skill provides comprehensive profiling and background checks for customers, bloggers, and other individuals. It gathers information from various sources to create detailed profiles and risk assessments.

## Features
- Social media profiling across multiple platforms
- Content analysis and sentiment evaluation
- Network mapping and connection analysis
- Risk assessment and trust scoring
- Professional affiliation verification
- Historical activity timeline

## Installation
The skill is already installed in `/Users/zhuzhenguo/.openclaw/workspace/skills/szzg007-background-investigation/`

## Usage

### Command Line Interface
```bash
# Investigate a customer
python investigate.py john_doe --type customer

# Investigate a blogger
python investigate.py tech_blog_writer --type blogger

# Investigate with custom output
python investigate.py business_partner --type partner --output partner_report.json

# Verbose output for detailed analysis
python investigate.py influencer_name --type blogger --verbose
```

### Parameters
- `identifier`: The target to investigate (username, email, name, etc.)
- `--type`: Type of target (customer, blogger, partner, vendor, individual)
- `--output`: Custom path for the investigation report
- `--verbose`: Enable detailed output

## Investigation Process

### 1. Data Collection
- Social media profiles and activity
- Public records and business affiliations
- Content analysis and historical activity
- Network connections and associations

### 2. Analysis
- Trust scoring based on multiple factors
- Risk assessment with red flag identification
- Content quality and consistency evaluation
- Professional credibility verification

### 3. Reporting
- Structured JSON report with all findings
- Summary of key findings and recommendations
- Risk assessment with next steps

## Example Reports

### Customer Investigation
```json
{
  "investigation_id": "INV-20260401-223012",
  "target_type": "customer",
  "sections": {
    "social_media": {
      "platforms": {
        "primary": {
          "profile_info": {
            "username": "john_doe",
            "followers": 1250,
            "engagement_rate": 3.6
          }
        }
      }
    },
    "content_analysis": {
      "topics": ["technology", "business", "marketing"],
      "sentiment": "positive",
      "quality_score": 7.5
    },
    "risk_assessment": {
      "trust_score": 7.8,
      "recommendation": "approved"
    }
  }
}
```

### Blogger Investigation
Similar structure but with additional fields for content analysis, audience metrics, and publishing patterns.

## Ethical Guidelines
- All investigations respect privacy laws and regulations
- Focus on publicly available information
- Transparent methodology and documented sources
- Fair and unbiased analysis
- Proper data handling and security

## Integration with OpenClaw
This skill integrates seamlessly with the OpenClaw framework and can be called when background investigations are needed for customers, partners, or other stakeholders.

## Next Steps
1. Configure API keys for social media platforms (when available)
2. Integrate with real data sources
3. Expand to additional data sources
4. Add more sophisticated analysis algorithms