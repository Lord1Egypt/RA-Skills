/**
 * SocialPack — Multi-Platform Social Media Generator
 * @author @TheShadowRose
 * @license MIT
 */

const LIMITS = {
  twitter: 280, linkedin: 3000, instagram: 2200, reddit_title: 300, mastodon: 500, facebook: 63206
};

class SocialPack {
  formatForTwitter(text) {
    if (text.length <= LIMITS.twitter) return [text];
    // Split into thread
    const words = text.split(' ');
    const tweets = [];
    let current = '';
    for (const word of words) {
      if ((current + ' ' + word).length > LIMITS.twitter - 8) { // Reserve space for " 999/999"
        tweets.push(current.trim());
        current = word;
      } else {
        current += (current ? ' ' : '') + word;
      }
    }
    if (current.trim()) tweets.push(current.trim());
    return tweets.map((t, i) => `${t} ${i+1}/${tweets.length}`);
  }

  formatForLinkedIn(text, hashtags = []) {
    let post = text.substring(0, LIMITS.linkedin);
    if (hashtags.length) post += '\n\n' + hashtags.map(h => '#' + h.replace(/\s/g, '')).join(' ');
    return post;
  }

  formatForInstagram(text, hashtags = []) {
    let caption = text;
    if (hashtags.length) caption += '\n\n' + hashtags.slice(0, 30).map(h => '#' + h.replace(/\s/g, '')).join(' ');
    return caption.substring(0, LIMITS.instagram);
  }

  formatForReddit(title, body, subreddit) {
    return { title: title.substring(0, LIMITS.reddit_title), body, subreddit: subreddit || '' };
  }

  formatAll(brief, options = {}) {
    const hashtags = options.hashtags || [];
    return {
      twitter: this.formatForTwitter(brief),
      linkedin: this.formatForLinkedIn(brief, hashtags),
      instagram: this.formatForInstagram(brief, hashtags),
      reddit: this.formatForReddit(brief.split('.')[0], brief),
      mastodon: brief.substring(0, LIMITS.mastodon)
    };
  }

  generateHashtags(text, max = 10) {
    const words = text.toLowerCase().split(/\s+/).filter(w => w.length > 4);
    const freq = {};
    for (const w of words) freq[w.replace(/[^a-z]/g, '')] = (freq[w.replace(/[^a-z]/g, '')] || 0) + 1;
    return Object.entries(freq).filter(([w]) => w.length > 0).sort((a, b) => b[1] - a[1]).slice(0, max).map(([w]) => w);
  }
}

module.exports = { SocialPack };
