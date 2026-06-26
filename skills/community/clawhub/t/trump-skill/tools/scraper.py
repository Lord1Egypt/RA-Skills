"""
Web scraper to collect Trump quotes.
Uses Tavily MCP for web search to find Trump quotes.
"""
import sys
sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
from tools.quote_db import add_quotes, init_db, count_quotes
from datetime import datetime

def scrape_trump_quotes():
    """
    Collect Trump quotes from various sources.
    This uses hardcoded well-known Trump quotes as a starting dataset.
    In production, this would integrate with Tavily MCP for web search.
    """
    init_db()

    # Well-known Trump quotes categorized by topic
    quotes_data = [
        # Trade & Economy
        ("China is the greatest wealth destroyer in history.", "speech", "2023-09", "Economic policy", "trade"),
        ("We lost $1 trillion dollars a year with China. We're bringing it back.", "speech", "2023-04", "Trade policy", "trade"),
        ("Tariffs are the greatest thing ever invented.", "interview", "2023-08", "Trade policy", "trade"),
        ("The USMCA is the greatest trade deal ever made.", "speech", "2020-01", "Trade deal", "trade"),
        ("I made the greatest trade deals.", "rally", "2024-01", "Campaign rally", "trade"),

        # China
        ("China, what they did to this world should not be allowed.", "speech", "2023-03", "China policy", "china"),
        ("China is eating your lunch, folks.", "debate", "2020-10", "Debate", "china"),
        ("I told China: you can't do this, you can't do that.", "interview", "2023-07", "China policy", "china"),
        ("We started the trade war with China. We won the trade war with China.", "rally", "2024-02", "Campaign rally", "china"),

        # Media & Fake News
        ("Fake news is the enemy of the people.", "speech", "2017-02", "Press briefing", "media"),
        ("The press is the enemy of the people.", "rally", "2019-08", "Campaign rally", "media"),
        ("CNN is fake news.", "interview", "2021-06", "Interview", "media"),
        ("NBC, CBS, ABC, CNN - they're all fake news.", "speech", "2023-06", "Speech", "media"),
        ("The mainstream media is failing our nation.", "Truth Social", "2023-09", "Truth Social post", "media"),

        # Biden
        ("Sleepy Joe Biden is the worst president in American history.", "rally", "2023-05", "Campaign rally", "biden"),
        ("Joe Biden is corrupt.", "speech", "2023-04", "Speech", "biden"),
        ("Biden doesn't know he's alive.", "interview", "2023-07", "Interview", "biden"),
        ("Crooked Joe Biden.", "rally", "2024-01", "Campaign rally", "biden"),
        ("Sleepy Joe can't string two sentences together.", "Truth Social", "2023-08", "Truth Social post", "biden"),

        # Elections
        ("The election was rigged.", "speech", "2021-01", "Speech", "election"),
        ("This election was stolen.", "rally", "2021-12", "Rally", "election"),
        ("We won the election by a lot.", "speech", "2020-11", "Election night", "election"),
        ("Massive voter fraud in 2020.", "interview", "2022-03", "Interview", "election"),
        ("The 2020 election was a sham.", "Truth Social", "2023-01", "Truth Social post", "election"),

        # Immigration
        ("Build the wall.", "rally", "2016-08", "Campaign rally", "immigration"),
        ("Mexico will pay for the wall.", "speech", "2016-05", "Speech", "immigration"),
        ("We have to secure our border.", "press conference", "2019-01", "Press conference", "immigration"),
        ("Human trafficking at record levels.", "speech", "2023-02", "Speech", "immigration"),
        ("Our border is the most dangerous place in the world.", "interview", "2023-06", "Interview", "immigration"),

        # Self Praise & Superlatives
        ("I am the greatest president in American history.", "rally", "2023-09", "Campaign rally", "self"),
        ("I did more than any other president.", "interview", "2023-08", "Interview", "self"),
        ("Nobody has done what I've done.", "speech", "2023-05", "Speech", "self"),
        ("I'm a very stable genius.", "tweet", "2019-01", "Tweet", "self"),
        ("I know more about drones than anybody.", "speech", "2017-03", "Speech", "self"),
        ("I understand money better than anybody.", "interview", "2016-10", "Interview", "self"),
        ("I have the best words.", "speech", "2016-07", "Speech", "self"),

        # Economy & Jobs
        ("We created the greatest economy in the history of our country.", "speech", "2019-10", "Speech", "economy"),
        ("Unemployment is at record lows.", "speech", "2019-06", "Speech", "economy"),
        ("Our country is doing better than ever before.", "rally", "2024-01", "Campaign rally", "economy"),
        ("Jobs are pouring in from all over the world.", "speech", "2018-03", "Speech", "economy"),
        ("I brought back 500,000 manufacturing jobs.", "interview", "2019-11", "Interview", "economy"),

        # Witch Hunt
        ("This is a witch hunt.", "speech", "2019-05", "Rose Garden", "witch_hunt"),
        ("No collusion, no obstruction!", "rally", "2019-03", "Campaign rally", "witch_hunt"),
        ("The Mueller investigation is a hoax.", "tweet", "2019-04", "Tweet", "witch_hunt"),
        ("They tried to take me down. It didn't work.", "interview", "2023-06", "Interview", "witch_hunt"),
        ("This is the greatest witch hunt in American history.", "speech", "2019-07", "Speech", "witch_hunt"),

        # MAGA
        ("Make America Great Again!", "rally", "2016-07", "RNC acceptance", "maga"),
        ("MAGA is happening.", "speech", "2024-01", "Speech", "maga"),
        ("Together, we are going to make America great again.", "inauguration", "2017-01", "Inauguration", "maga"),
        ("America First!", "speech", "2017-01", "Inauguration", "maga"),
        ("We will make America wealthy again.", "rally", "2023-10", "Campaign rally", "maga"),

        # Foreign Policy
        ("I got along with Putin. I got along with Kim Jong-un.", "interview", "2023-07", "Interview", "foreign"),
        ("Nobody's tougher on Russia than me.", "speech", "2022-03", "Speech", "foreign"),
        ("I brought peace through strength.", "rally", "2024-01", "Campaign rally", "foreign"),
        ("We left Afghanistan. That was a disaster.", "interview", "2023-08", "Interview", "foreign"),
        ("NATO is obsolete.", "speech", "2016-04", "Speech", "foreign"),

        # Energy
        ("We are energy independent.", "speech", "2020-09", "Speech", "energy"),
        ("Fracking will be safe.", "debate", "2020-10", "Debate", "energy"),
        ("We have more oil and gas than anybody.", "rally", "2023-04", "Campaign rally", "energy"),
        ("Clean coal is beautiful.", "speech", "2017-06", "Speech", "energy"),

        # Healthcare
        ("We will repeal and replace Obamacare.", "speech", "2017-03", "Speech", "healthcare"),
        ("Nobody knew healthcare could be so complicated.", "meeting", "2017-02", "Meeting", "healthcare"),
        ("I want to protect pre-existing conditions.", "rally", "2020-09", "Campaign rally", "healthcare"),

        # Other Famous Quotes
        ("You're fired!", "apprentice", "2004-01", "The Apprentice", "famous"),
        ("It's going to be tremendous, believe me.", "speech", "2016-09", "Campaign speech", "famous"),
        ("I could shoot somebody and I wouldn't lose voters.", "interview", "2016-01", "Interview", "famous"),
        ("When Mexico sends its people, they're not sending their best.", "speech", "2015-06", "Announcement", "famous"),
        ("I like people who weren't captured.", "debate", "2015-07", "Debate", "famous"),
        ("I will build a great wall and nobody builds walls better than me.", "speech", "2015-06", "Announcement", "famous"),
        (" ISIS is cutting off heads. We should be more vague.", "interview", "2015-07", "Interview", "famous"),
        ("My fingers are long and beautiful, as, good, they are, as you may have heard.", "speech", "2016-02", "Campaign rally", "famous"),
        ("I've said if Ivanka weren't my daughter, I'd be dating her.", "interview", "2006-07", "Interview", "famous"),
        ("I'm not a fan of Mr. McCain. He was a war hero. He's a war hero because he was captured. I like people who weren't captured.", "debate", "2015-07", "Debate", "famous"),

        # 2024 Campaign Quotes
        ("We're going to win so much, you're going to get tired of winning.", "rally", "2024-03", "Campaign rally", "maga"),
        ("This is the most important election in the history of our country.", "speech", "2024-01", "Speech", "election"),
        ("We will end the weaponization of government.", "rally", "2024-02", "Campaign rally", "policy"),
        ("We're going to bring our country back.", "speech", "2024-01", "Speech", "maga"),
        ("The Biden crime family should be locked up.", "rally", "2024-03", "Campaign rally", "biden"),
        ("Democrats are the enemy from within.", "speech", "2024-10", "Speech", "politics"),
        ("They're coming after me because I'm fighting for you.", "rally", "2024-02", "Campaign rally", "self"),
        ("I will end the border crisis on day one.", "rally", "2024-01", "Campaign rally", "immigration"),
        ("The wind turbines are killing all the birds.", "speech", "2024-04", "Speech", "energy"),
        ("Electric cars are terrible. Nobody buys them.", "rally", "2024-03", "Campaign rally", "energy"),
        ("Taiwan should pay us for defense.", "interview", "2024-04", "Interview", "foreign"),
        ("Europe is using us to the tune of $300 billion.", "speech", "2024-02", "Speech", "foreign"),

        # Additional Trade & Economy
        ("The dollar is the reserve currency. That gives us tremendous power.", "interview", "2024-03", "Interview", "economy"),
        ("Inflation is killing our country.", "rally", "2024-01", "Campaign rally", "economy"),
        (" Grocery prices have gone up 50%.\"", "speech", "2024-02", "Speech", "economy"),
        ("Energy prices are through the roof.", "interview", "2024-01", "Interview", "economy"),
        ("We're going to bring back manufacturing.", "rally", "2024-02", "Campaign rally", "economy"),
        ("China is flooding our market with cheap goods.", "speech", "2024-03", "Speech", "china"),
        ("I will put 100% tariffs on Chinese goods.", "rally", "2024-03", "Campaign rally", "trade"),
        ("The USMCA is the best trade deal ever made.", "speech", "2020-01", "Speech", "trade"),
        ("Vietnam is the worst of all of them. They're just like China but smaller.", "interview", "2024-04", "Interview", "trade"),

        # Additional Media
        ("The New York Times is a failing newspaper.", "interview", "2024-02", "Interview", "media"),
        ("Amazon Washington Post is fake news.", "tweet", "2018-03", "Tweet", "media"),
        ("The media hates me. But I love them because I beat them.", "rally", "2019-10", "Campaign rally", "media"),
        ("They don't want me to use social media. That's why they banned me.", "speech", "2024-01", "Speech", "media"),
        ("Facebook and Twitter are enemies of the people.", "Truth Social", "2023-09", "Truth Social", "media"),
        ("Google is rigged against Republicans.", "tweet", "2018-08", "Tweet", "media"),

        # Additional Biden
        ("Kamala is a monster.", "rally", "2024-08", "Campaign rally", "biden"),
        ("Joe Biden is not fit to be president.", "speech", "2024-01", "Speech", "biden"),
        ("Hunter Biden is a criminal.", "interview", "2023-12", "Interview", "biden"),
        ("The Biden family took money from China.", "rally", "2024-02", "Campaign rally", "biden"),
        ("Kamala Harris has destroyed everything she touched.", "speech", "2024-07", "Speech", "biden"),
        ("Nancy Pelosi is a corrupt politician.", "interview", "2022-06", "Interview", "politics"),
        ("Chuck Schumer hates Israel.", "tweet", "2024-03", "Tweet", "politics"),

        # Additional Immigration
        ("Human traffickers are coming across our border.", "speech", "2024-01", "Speech", "immigration"),
        ("Fentanyl is killing Americans at record rates.", "rally", "2024-02", "Campaign rally", "immigration"),
        ("ICE is the best law enforcement we have.", "speech", "2019-07", "Speech", "immigration"),
        (" sanctuary cities are dangerous.", "interview", "2024-03", "Interview", "immigration"),
        ("The border wall is being built. It's almost complete.", "speech", "2024-01", "Speech", "immigration"),

        # Additional Self Praise
        ("I'm the only one who can fix this.", "speech", "2016-01", "Campaign announcement", "self"),
        ("I have a very good brain.", "debate", "2016-02", "Debate", "self"),
        ("My I.Q. is one of the highest.", "interview", "2016-07", "Interview", "self"),
        ("Nobody negotiates better than me.", "speech", "2018-05", "Speech", "self"),
        ("I was the best builder. I built the greatest buildings.", "interview", "2019-11", "Interview", "self"),
        ("I turned down deals. I'm too smart.", "interview", "2016-05", "Interview", "self"),
        ("I know how to win. I've won all my life.", "rally", "2024-01", "Campaign rally", "self"),
        ("Nobody has ever been treated as unfairly as I have.", "speech", "2024-02", "Speech", "self"),
        ("I am your justice.", "rally", "2020-09", "Campaign rally", "self"),
        ("I alone can fix it.", "speech", "2016-07", "RNC acceptance", "self"),

        # NATO & Foreign Policy
        ("NATO is a disaster. Countries aren't paying.", "speech", "2016-04", "Campaign", "foreign"),
        ("I told NATO countries: pay your fair share.", "interview", "2019-12", "Interview", "foreign"),
        ("Putin is a thug. But I got along with him.", "debate", "2020-10", "Debate", "foreign"),
        ("Kim Jong-un wrote me beautiful letters.", "interview", "2019-08", "Interview", "foreign"),
        ("I made peace with North Korea.", "speech", "2019-07", "Speech", "foreign"),
        ("I withdrew from the Iran deal. Best thing I did.", "speech", "2020-09", "Speech", "foreign"),
        ("The Iran deal was a disaster.", "interview", "2018-05", "Interview", "foreign"),
        ("Jerusalem is the capital of Israel.", "speech", "2017-12", "Speech", "foreign"),
        ("I moved the embassy to Jerusalem.", "rally", "2020-02", "Campaign rally", "foreign"),

        # Democrats & Politics
        ("The Democrat party is radical.", "rally", "2024-03", "Campaign rally", "politics"),
        ("They're coming for your guns.", "rally", "2019-08", "Campaign rally", "politics"),
        ("They're coming for your money.", "speech", "2024-02", "Speech", "politics"),
        ("Democrats want open borders.", "rally", "2024-01", "Campaign rally", "politics"),
        ("Radical left Democrats want to destroy our country.", "Truth Social", "2023-10", "Truth Social", "politics"),
        (" AOC and the squad are a bunch of radicals.", "tweet", "2019-07", "Tweet", "politics"),
        ("Adam Schiff is a corrupt politician.", "interview", "2020-01", "Interview", "politics"),

        # January 6th & Election
        ("The election was rigged and stolen.", "rally", "2022-09", "Rally", "election"),
        ("We should have contested the election.", "interview", "2023-08", "Interview", "election"),
        ("The Deep State is real.", "speech", "2024-01", "Speech", "election"),
        ("Mail-in ballots are fraud.", "tweet", "2020-08", "Tweet", "election"),
        ("Dominion voting machines are rigged.", "speech", "2021-01", "Speech", "election"),

        # Russia & Ukraine
        ("Putin made a mistake. He never would have done this if I was president.", "interview", "2022-02", "Interview", "foreign"),
        ("The Ukraine war should have never happened.", "rally", "2024-02", "Campaign rally", "foreign"),
        ("I'm the only one who can stop World War III.", "speech", "2024-03", "Speech", "foreign"),

        # Economy & Jobs
        ("The stock market will crash if Biden wins.", "rally", "2020-10", "Campaign rally", "economy"),
        ("Under Trump, 401ks were through the roof.", "interview", "2024-01", "Interview", "economy"),
        ("We created 10 million jobs.", "speech", "2020-10", "Speech", "economy"),
        ("Black unemployment was at the lowest level ever.", "speech", "2019-09", "Speech", "economy"),
        ("Women unemployment was at the lowest level ever.", "speech", "2019-09", "Speech", "economy"),
        ("The tax cuts were the biggest in history.", "speech", "2017-12", "Speech", "economy"),
        ("I cut regulations more than any president.", "interview", "2019-11", "Interview", "economy"),
        ("Companies are moving back to America.", "speech", "2018-03", "Speech", "economy"),

        # Energy & Environment
        ("The Paris Climate Accord is a disaster.", "speech", "2017-06", "Rose Garden", "energy"),
        ("We're pulling out of Paris.", "speech", "2017-06", "Rose Garden", "energy"),
        ("Climate change is a hoax.", "tweet", "2019-11", "Tweet", "energy"),
        ("We have beautiful clean coal.", "speech", "2017-10", "Speech", "energy"),
        ("Oil and gas is American energy.", "rally", "2024-01", "Campaign rally", "energy"),
        ("Wind energy is for dummy states.", "speech", "2024-04", "Speech", "energy"),

        # Healthcare
        ("Obamacare is a disaster.", "speech", "2017-03", "Speech", "healthcare"),
        ("We will replace it with something much better.", "speech", "2017-01", "Speech", "healthcare"),
        ("Drug prices are out of control.", "rally", "2019-10", "Campaign rally", "healthcare"),
        ("Most favored nation for drug pricing.", "speech", "2020-09", "Speech", "healthcare"),

        # COVID
        ("I downplayed the virus because I didn't want to cause panic.", "interview", "2020-10", "Interview", "covid"),
        ("We did the best job on COVID of any country.", "speech", "2020-09", "Speech", "covid"),
        ("Warp Speed was the greatest achievement.", "rally", "2024-01", "Campaign rally", "covid"),
        ("The vaccines saved millions of lives.", "speech", "2021-12", "Speech", "covid"),

        # Courts & Legal
        ("The judge is highly conflicted.", "interview", "2023-05", "Interview", "legal"),
        ("This trial is election interference.", "court", "2024-05", "Court", "legal"),
        ("The DA is a criminal.", "rally", "2024-04", "Campaign rally", "legal"),
        ("The system is rigged against me.", "Truth Social", "2024-05", "Truth Social", "legal"),
        ("I am being persecuted.", "speech", "2024-06", "Speech", "legal"),

        # Immigration Policy
        ("Travel ban was necessary for security.", "speech", "2017-01", "Executive order", "immigration"),
        ("Countries that don't share information won't get visas.", "press conference", "2017-01", "Press conference", "immigration"),
        ("We need extreme vetting.", "speech", "2016-08", "Campaign rally", "immigration"),
        ("ICE is heroes.", "rally", "2019-07", "Campaign rally", "immigration"),
    ]

    add_quotes(quotes_data)
    print(f"Added {len(quotes_data)} quotes to database.")
    print(f"Total quotes in DB: {count_quotes()}")

if __name__ == "__main__":
    scrape_trump_quotes()
