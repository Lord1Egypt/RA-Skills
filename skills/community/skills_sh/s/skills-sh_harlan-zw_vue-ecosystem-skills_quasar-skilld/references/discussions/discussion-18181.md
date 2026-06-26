---
number: 18181
title: Removing black background in q-video
category: General - Components / Directives / etc
created: 2025-11-20
url: "https://github.com/quasarframework/quasar/discussions/18181"
upvotes: 1
comments: 0
answered: false
---

# Removing black background in q-video

On my page I have a YouTube video playing, but I can't seem to be able to hide the black background. From what I can tell, this is some YouTube iframe that defines the background, making it impossible to override
I have tried whatever I could find, in hopes something would magically work, but so far no luck

I have this method

`	toYouTubeEmbedUrl(idOrUrl: string, opts?: { autoplay?: 0 | 1; mute?: 0 | 1; controls?: 0 | 1; rel?: 0 | 1 })
	{
		const id = this.extractYouTubeId(idOrUrl) ?? idOrUrl
		const params = new URLSearchParams({
			autoplay: String(opts?.autoplay ?? 0),
			mute: String(opts?.mute ?? 0),
			controls: String(opts?.controls ?? 1),
			rel: String(opts?.rel ?? 0),
//wmode:'transparent', // Also tried this, but sounds like this is some old code?
			modestbrandin...