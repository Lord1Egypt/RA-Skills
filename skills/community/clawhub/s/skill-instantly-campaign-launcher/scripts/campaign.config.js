/**
 * Instantly Campaign Config Template
 * Customize this for each new outreach campaign.
 */

module.exports = {
  // Campaign name — if already exists, the script reuses it (no duplicate created)
  campaignName: 'My Cold Email Campaign',

  // Schedule — when emails are sent
  schedule: {
    name: 'UAE Business Hours',
    timing: { from: '09:00', to: '17:00' },
    days: {
      monday: true, tuesday: true, wednesday: true,
      thursday: true, friday: true, saturday: false, sunday: false,
    },
    timezone: 'Asia/Dubai',
  },

  // 3-step D0 / D3 / D8 email sequence
  // Instantly variables: {{firstName}}, {{companyName}}, {{website}}
  sequences: [
    {
      step: 1,
      delay: 0, // days after campaign start (D0)
      subject: 'Quick question, {{firstName}}',
      body: `Hi {{firstName}},

[D0 email body here — introduce yourself, state the pain, offer the value prop]

[CTA — link or reply ask]

— [Your Name]
[Company]`,
    },
    {
      step: 2,
      delay: 3, // D3 follow-up
      subject: 'Re: Quick question, {{firstName}}',
      body: `Hi {{firstName}},

[D3 follow-up — address the most common hesitation, reinforce ROI]

[Soft CTA]

— [Your Name]`,
    },
    {
      step: 3,
      delay: 8, // D8 closing email
      subject: 'Last note, {{firstName}}',
      body: `Hi {{firstName}},

[D8 close — create urgency or give a soft out]

[Final CTA]

— [Your Name]`,
    },
  ],
};
