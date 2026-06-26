# THE_TIME_MASHEEN

![](logo.webp)

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/mrjessek/the-time-masheen/main/install.sh)
```

You can't go back. Not without a Time Masheen.

---

## What It Is

Okay so it's a tool. For websites.

You know how you want to get the thing off the website and the website's like — no. And you're like, come on. And it's like — NO. So you go a little deeper. Get up in there. And the website's all like, oh no please don't. And you're like, yeah you know you want me to. And then it just — gives you everything. All this crazy data stuff. Just comes right out.

That's this.

They each do a thing that connects the other things to like - get things really connected.

---

## These Three Things

**Scrapling**

Scraply's the one that just, really gets webs. You give this address thing, and it just like, goes there and gets all your stuff. But then all these walls come up and you're just like Sheeeesh, why even put that there. And then, you can't get it. So Scraplingy got like this thing about going in from different angles. The webs doesn't even know what happened and just gives all the stuff. I don't even know, something about the clouds n cafes.

**Wayback Machine**

Okay, so there's this place that's been just like, saving all these copies of webs since, like, forever. All of it. Just sitting there. So when someone acts all "I dunno". You're like, yeah you know.

**playwright**

Some websites got this button stuff. And it's all "no you can't do that because you're not kewl enough." So you're just like, yeah I am, and it's all like "ok here's all the stuff". Then you give that stuff to the other thing and it's all, "Hey, thanks for the stuff".

---

## When Use This

**Webs Changed.**
Get the new stuff. Get the old stuff. Put the stuff together.

**Webs Gone.**
It's in the thing. All the stuff is.

**Can't get the stuff.**
Play right and Scrapy get all the stuff.

---

## How To Use It

**Normal Webs**
```bash
scrapling extract get "https://example.com" output.md
```

**Webs got no script thing**
```bash
scrapling extract fetch "https://example.com" output.md --network-idle --wait 3000
```

**Webs being all greedy about it's stuff**
```bash
scrapling extract stealthy-fetch "https://example.com" output.md --solve-cloudflare
```

**Needs find more old stuff**
```bash
curl -s "https://web.archive.org/cdx/search/cdx?url=example.com&output=json&collapse=timestamp:4&fl=timestamp,statuscode&filter=statuscode:200"
```

**Stuff in 2022**
```bash
scrapling extract get "https://web.archive.org/web/20220601000000/https://example.com/" old.md
```

**See how changed**
```bash
diff old.md output.md
```

---

## What Need

- Scrapling: `pip install "scrapling[all]"`
- playwright: `npm install -g playwright-cli`
- curl: already on the computer
- OpenClaw: only if running as an agent skill

---

![](the-time-masheen.jpg)
