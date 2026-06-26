// OpenClaw Pet — i18n + per-pet personality dialogue bundle
// Languages: tr (default), en, fr, de
// Pet types: penguin, cat, dog, fish, chick

(function () {
  const SUPPORTED = ['tr', 'en', 'fr', 'de'];

  // ─── UI labels ────────────────────────────────────────────────────
  const UI = {
    tr: {
      eggHeader: '🐣 OpenClaw Pet', eggHint: '📱 Telefonu salla!', eggCount: (n) => `${n} / 3`,
      hatched: 'Tebrikler!', hatchedSub: 'Bir hayvan çıktı!', namePlaceholder: 'İsim ver...', save: 'Kaydet',
      level: (n) => `Level ${n}`, streakSuffix: 'gün', sad: (name) => `😾 ${name} küstü — ilgilen!`,
      feed: 'Feed', play: 'Play', sleep: 'Sleep', friends: '🤝 Arkadaşlar', share: '🔗 Paylaş',
      visitMode: '🌍 Ziyaret modu', befriend: '🤝 Arkadaş ol', playdate: '🎉 Playdate',
      backHome: '← Kendi pet\'ime dön', friendsTitle: '🤝 Arkadaşların', noFriends: 'Henüz arkadaş yok. Pet linkini paylaş!',
      close: 'Kapat', bondLabel: 'Bond:', friendCount: 'arkadaş',
      memorialTitle: 'In Memoriam', memorialFooter: 'Sevgili dostumuz huzur içinde uyusun 🕯️',
      shareMemorial: '🕯️ Anıt paylaş', newEgg: '🥚 Yeni yumurta',
      reviveConfirm: 'Reenkarnasyon: Aynı tipte yeni bir pet doğacak ama tüm arkadaşlar ve level kaybolacak.\n\nEvet → reenkarnasyon\nİptal → tamamen yeni yumurta',
      shareText: (name) => `🐣 ${name || 'Benim pet\'im'}'i ziyaret et!`,
      shareMemorialText: (name) => `🪦 ${name || 'Sevgili pet'} hayata gözlerini yumdu. Anısı yaşasın.`,
      friendMade: 'Arkadaş oldunuz! 🎉', notFound: 'Pet bulunamadı', error: 'Hata',
      cooldown: '24 saatte bir playdate',
    },
    en: {
      eggHeader: '🐣 OpenClaw Pet', eggHint: '📱 Shake your phone!', eggCount: (n) => `${n} / 3`,
      hatched: 'Congratulations!', hatchedSub: 'It hatched!', namePlaceholder: 'Name it...', save: 'Save',
      level: (n) => `Level ${n}`, streakSuffix: 'days', sad: (name) => `😾 ${name} is upset — give some love!`,
      feed: 'Feed', play: 'Play', sleep: 'Sleep', friends: '🤝 Friends', share: '🔗 Share',
      visitMode: '🌍 Visit mode', befriend: '🤝 Befriend', playdate: '🎉 Playdate',
      backHome: '← Back to my pet', friendsTitle: '🤝 Your friends', noFriends: 'No friends yet. Share your pet link!',
      close: 'Close', bondLabel: 'Bond:', friendCount: 'friends',
      memorialTitle: 'In Memoriam', memorialFooter: 'Rest in peace, dear friend 🕯️',
      shareMemorial: '🕯️ Share memorial', newEgg: '🥚 New egg',
      reviveConfirm: 'Reincarnation: A new pet of the same type will be born, but all friends and level will be lost.\n\nOK → reincarnate\nCancel → fresh egg',
      shareText: (name) => `🐣 Visit ${name || 'my pet'}!`,
      shareMemorialText: (name) => `🪦 ${name || 'Beloved pet'} has passed. Long live their memory.`,
      friendMade: 'You\'re friends! 🎉', notFound: 'Pet not found', error: 'Error',
      cooldown: 'Playdate once every 24h',
    },
    fr: {
      eggHeader: '🐣 OpenClaw Pet', eggHint: '📱 Secoue le téléphone !', eggCount: (n) => `${n} / 3`,
      hatched: 'Félicitations !', hatchedSub: 'Un animal est apparu !', namePlaceholder: 'Donne un nom...', save: 'Enregistrer',
      level: (n) => `Niveau ${n}`, streakSuffix: 'jours', sad: (name) => `😾 ${name} boude — occupe-toi de lui !`,
      feed: 'Nourrir', play: 'Jouer', sleep: 'Dormir', friends: '🤝 Amis', share: '🔗 Partager',
      visitMode: '🌍 Mode visite', befriend: '🤝 Devenir amis', playdate: '🎉 Rendez-vous',
      backHome: '← Retour à mon pet', friendsTitle: '🤝 Tes amis', noFriends: 'Pas encore d\'amis. Partage ton lien !',
      close: 'Fermer', bondLabel: 'Lien :', friendCount: 'amis',
      memorialTitle: 'In Memoriam', memorialFooter: 'Repose en paix, cher ami 🕯️',
      shareMemorial: '🕯️ Partager le mémorial', newEgg: '🥚 Nouvel œuf',
      reviveConfirm: 'Réincarnation : un nouveau pet du même type naîtra, mais tu perdras amis et niveau.\n\nOK → réincarnation\nAnnuler → nouvel œuf',
      shareText: (name) => `🐣 Rends visite à ${name || 'mon pet'} !`,
      shareMemorialText: (name) => `🪦 ${name || 'Cher pet'} nous a quittés. Que sa mémoire vive.`,
      friendMade: 'Vous êtes amis ! 🎉', notFound: 'Pet introuvable', error: 'Erreur',
      cooldown: 'Un rendez-vous toutes les 24h',
    },
    de: {
      eggHeader: '🐣 OpenClaw Pet', eggHint: '📱 Schüttle dein Handy!', eggCount: (n) => `${n} / 3`,
      hatched: 'Herzlichen Glückwunsch!', hatchedSub: 'Es ist geschlüpft!', namePlaceholder: 'Gib einen Namen...', save: 'Speichern',
      level: (n) => `Level ${n}`, streakSuffix: 'Tage', sad: (name) => `😾 ${name} ist beleidigt — kümmer dich!`,
      feed: 'Füttern', play: 'Spielen', sleep: 'Schlafen', friends: '🤝 Freunde', share: '🔗 Teilen',
      visitMode: '🌍 Besuchsmodus', befriend: '🤝 Freundschaft', playdate: '🎉 Verabredung',
      backHome: '← Zurück zu meinem Pet', friendsTitle: '🤝 Deine Freunde', noFriends: 'Noch keine Freunde. Teile deinen Link!',
      close: 'Schließen', bondLabel: 'Bindung:', friendCount: 'Freunde',
      memorialTitle: 'In Memoriam', memorialFooter: 'Ruhe in Frieden, lieber Freund 🕯️',
      shareMemorial: '🕯️ Andenken teilen', newEgg: '🥚 Neues Ei',
      reviveConfirm: 'Reinkarnation: Ein neues Pet desselben Typs wird geboren, aber Freunde und Level gehen verloren.\n\nOK → Reinkarnation\nAbbrechen → neues Ei',
      shareText: (name) => `🐣 Besuche ${name || 'mein Pet'}!`,
      shareMemorialText: (name) => `🪦 ${name || 'Geliebter Pet'} ist verstorben. Möge sein Andenken weiterleben.`,
      friendMade: 'Ihr seid Freunde! 🎉', notFound: 'Pet nicht gefunden', error: 'Fehler',
      cooldown: 'Verabredung alle 24h',
    },
  };

  // ─── Per-pet personality dialogue ─────────────────────────────────
  // Situations: greet, idle_happy, idle_hungry, idle_tired, fed, played, slept
  const D = {
    cat: {
      tr: {
        greet: ['miyav... yine sen', 'ne istiyon insanım', 'önce mama, sonra konuşuruz', 'kim çağırdı'],
        idle_happy: ['kuyruğum mutlu', 'pencereye bakıyorum', 'aristokrat gibiyim', 'sen olmasan da olur'],
        idle_hungry: ['açım ama gururum var', 'mama. hemen.', 'tabağa bak', 'açlık seni de bulacak'],
        idle_tired: ['18 saat uyumalıyım', 'rüya görüyorum, rahatsız etme', 'pufff'],
        fed: ['bu sefer iyiydi', 'doydum, gidebilirsin', 'saygı duyuyorum'],
        played: ['eğlendim ama söyleme', 'yine isterim', 'lazerli olsa daha iyiydi'],
        slept: ['zzz', 'tatlı rüyalar... kendime'],
      },
      en: {
        greet: ['meow... you again', 'what do you want, human', 'food first, talk later', 'who summoned me'],
        idle_happy: ['my tail is content', 'staring at the window', 'i am aristocracy', 'i tolerate you'],
        idle_hungry: ['hungry but proud', 'food. now.', 'look at the bowl', 'hunger comes for all'],
        idle_tired: ['need 18h sleep', 'dreaming, do not disturb', 'pfff'],
        fed: ['acceptable', 'i am full, you may leave', 'respect granted'],
        played: ['fun, do not tell anyone', 'again', 'lasers would be better'],
        slept: ['zzz', 'sweet dreams... for me'],
      },
      fr: {
        greet: ['miaou... encore toi', 'qu\'est-ce que tu veux', 'la nourriture d\'abord', 'qui m\'a appelé'],
        idle_happy: ['ma queue est heureuse', 'je fixe la fenêtre', 'je suis aristocrate', 'je te tolère'],
        idle_hungry: ['j\'ai faim mais j\'ai ma fierté', 'nourriture. maintenant.', 'regarde le bol'],
        idle_tired: ['j\'ai besoin de 18h de sommeil', 'je rêve, ne dérange pas'],
        fed: ['acceptable', 'je suis rassasié, tu peux partir'],
        played: ['amusant, ne dis rien', 'encore'],
        slept: ['zzz', 'doux rêves... pour moi'],
      },
      de: {
        greet: ['miau... schon wieder du', 'was willst du, Mensch', 'erst Futter, dann reden', 'wer hat mich gerufen'],
        idle_happy: ['mein Schwanz ist zufrieden', 'ich starre aus dem Fenster', 'ich bin Aristokrat'],
        idle_hungry: ['hungrig, aber stolz', 'Futter. Jetzt.', 'sieh den Napf an'],
        idle_tired: ['brauche 18h Schlaf', 'ich träume, störe nicht'],
        fed: ['akzeptabel', 'ich bin satt, du kannst gehen'],
        played: ['Spaß, sag es niemandem', 'nochmal'],
        slept: ['zzz', 'süße Träume... für mich'],
      },
    },
    dog: {
      tr: {
        greet: ['HAV HAV HAV', 'KANKAAA!', 'GELDİN GELDİN GELDİN', 'KOŞALIM MI'],
        idle_happy: ['kuyruğum kopacak', 'sen en iyisisin', 'top atalım?', 'parka gidelim?'],
        idle_hungry: ['açım kanka', 'mamacı geldi mi', 'biraz et?'],
        idle_tired: ['hav hav... zzz', 'yere uzanıyorum', 'biraz şekerleme'],
        fed: ['EN İYİ MAMA BU', 'TEŞEKKÜRLERRR', 'sahibim harikasın'],
        played: ['ÇOK EĞLENDİMMM', 'TEKRAR TEKRAR', 'BU GÜN GÜZEL GÜNDÜ'],
        slept: ['rüyamda kemik vardı', 'tatlı rüyalar sahibim'],
      },
      en: {
        greet: ['WOOF WOOF WOOF', 'FRIEND!!!', 'YOU CAME YOU CAME', 'LET\'S RUN'],
        idle_happy: ['tail will fall off', 'you are the best', 'fetch?', 'park?'],
        idle_hungry: ['hungry friend', 'is it food time', 'a bit of meat?'],
        idle_tired: ['woof... zzz', 'lying down', 'small nap'],
        fed: ['BEST FOOD EVER', 'THAAANK YOU', 'owner you are amazing'],
        played: ['SO MUCH FUN', 'AGAIN AGAIN', 'WHAT A DAY'],
        slept: ['dreamed of bones', 'sweet dreams owner'],
      },
      fr: {
        greet: ['OUAF OUAF OUAF', 'COPAIN !!!', 'TU ES VENU', 'ON COURT'],
        idle_happy: ['ma queue va tomber', 'tu es le meilleur', 'la balle ?'],
        idle_hungry: ['j\'ai faim copain', 'c\'est l\'heure de manger', 'un peu de viande ?'],
        idle_tired: ['ouaf... zzz', 'je m\'allonge', 'petite sieste'],
        fed: ['MEILLEURE NOURRITURE', 'MEEERCI', 'maître tu es génial'],
        played: ['TROP FUN', 'ENCORE ENCORE', 'QUELLE JOURNÉE'],
        slept: ['j\'ai rêvé d\'os', 'doux rêves maître'],
      },
      de: {
        greet: ['WAU WAU WAU', 'FREUND!!!', 'DU BIST DA', 'LASS UNS RENNEN'],
        idle_happy: ['mein Schwanz fliegt ab', 'du bist der beste', 'Stöckchen?'],
        idle_hungry: ['hungrig Freund', 'ist es Futterzeit', 'etwas Fleisch?'],
        idle_tired: ['wau... zzz', 'ich lege mich hin', 'kleines Nickerchen'],
        fed: ['BESTES FUTTER', 'DAANKE', 'Herrchen du bist großartig'],
        played: ['SO VIEL SPASS', 'NOCHMAL NOCHMAL', 'TOLLER TAG'],
        slept: ['ich träumte von Knochen', 'süße Träume Herrchen'],
      },
    },
    penguin: {
      tr: {
        greet: ['🧊 selam', 'cool olalım', 'buz gibiyim', 'antarktika selamlar'],
        idle_happy: ['balıkları izliyorum', 'cool durumdayım', 'kayıyorum yavaşça'],
        idle_hungry: ['balık istiyorum', 'açım ama hiperventile değilim', 'ringa olur mu'],
        idle_tired: ['kar üstünde uyumalıyım', 'cool yorgunluk'],
        fed: ['balık iyiydi', 'memnun kaldım', 'cool sayılabilir'],
        played: ['kayma yarışı yapalım', 'eğlence sahnesi'],
        slept: ['buz tutmuş rüyalar'],
      },
      en: {
        greet: ['🧊 hi', 'staying cool', 'i am ice', 'greetings from antarctica'],
        idle_happy: ['watching the fish', 'staying cool', 'sliding slowly'],
        idle_hungry: ['need fish', 'hungry but composed', 'herring?'],
        idle_tired: ['must sleep on ice', 'cool tiredness'],
        fed: ['fish was good', 'satisfied', 'almost cool'],
        played: ['sliding race?', 'entertainment'],
        slept: ['frozen dreams'],
      },
      fr: {
        greet: ['🧊 salut', 'on reste cool', 'je suis glace'],
        idle_happy: ['je regarde les poissons', 'cool', 'je glisse lentement'],
        idle_hungry: ['besoin de poisson', 'faim mais calme'],
        idle_tired: ['je dors sur la glace'],
        fed: ['le poisson était bon', 'satisfait'],
        played: ['course de glisse ?'],
        slept: ['rêves glacés'],
      },
      de: {
        greet: ['🧊 hallo', 'bleib cool', 'ich bin Eis'],
        idle_happy: ['ich beobachte Fische', 'bleibe cool', 'gleite langsam'],
        idle_hungry: ['brauche Fisch', 'hungrig aber ruhig'],
        idle_tired: ['muss auf Eis schlafen'],
        fed: ['Fisch war gut', 'zufrieden'],
        played: ['Rutschrennen?'],
        slept: ['gefrorene Träume'],
      },
    },
    fish: {
      tr: {
        greet: ['blub blub', 'hoşgeldin', 'huzur içinde'],
        idle_happy: ['blub blub blub', 'akvaryumda zen', 'su güzel'],
        idle_hungry: ['mama kıvılcımları', 'pul mu var'],
        idle_tired: ['suda dinleniyorum', 'yavaş yüz'],
        fed: ['blub teşekkür', 'doydum'],
        played: ['baloncuk eğlencesi'],
        slept: ['rüyada okyanus'],
      },
      en: {
        greet: ['blub blub', 'welcome', 'peaceful'],
        idle_happy: ['blub blub blub', 'aquarium zen', 'water is nice'],
        idle_hungry: ['need fish flakes', 'any food?'],
        idle_tired: ['resting in water'],
        fed: ['blub thanks', 'full'],
        played: ['bubble fun'],
        slept: ['ocean dreams'],
      },
      fr: {
        greet: ['blub blub', 'bienvenue'],
        idle_happy: ['blub blub blub', 'zen aquarium'],
        idle_hungry: ['flocons ?'],
        idle_tired: ['je me repose'],
        fed: ['blub merci'],
        played: ['amusement bulles'],
        slept: ['rêves d\'océan'],
      },
      de: {
        greet: ['blubb blubb', 'willkommen'],
        idle_happy: ['blubb blubb blubb', 'Aquarium-Zen'],
        idle_hungry: ['Flocken?'],
        idle_tired: ['ich ruhe mich aus'],
        fed: ['blubb danke'],
        played: ['Blasenspaß'],
        slept: ['Ozeanträume'],
      },
    },
    chick: {
      tr: {
        greet: ['CIK CIK CIK', 'merhabaaa', 'YENİ BİRŞEY YENİ BİRŞEY'],
        idle_happy: ['cik cik cik', 'tüylerim güzel', 'koşuyorum cik'],
        idle_hungry: ['CIK!! AÇIM', 'tohum var mı', 'cik cik açım'],
        idle_tired: ['cik... zzz', 'küçük bir cik şekerlemesi'],
        fed: ['CIK CIK CIK TEŞEKKÜRRR', 'doydum koşuyorum'],
        played: ['EN İYİ OYUN', 'CIK CIK CIK YAYY'],
        slept: ['cik rüyalar'],
      },
      en: {
        greet: ['CHEEP CHEEP', 'hello!!', 'NEW THING NEW THING'],
        idle_happy: ['cheep cheep', 'feathers nice', 'running cheep'],
        idle_hungry: ['CHEEP!! HUNGRY', 'any seeds', 'cheep hungry'],
        idle_tired: ['cheep... zzz', 'tiny cheep nap'],
        fed: ['CHEEP THANK YOU', 'full running'],
        played: ['BEST GAME', 'CHEEP YAY'],
        slept: ['cheep dreams'],
      },
      fr: {
        greet: ['PIOU PIOU', 'bonjour !!'],
        idle_happy: ['piou piou', 'plumes belles'],
        idle_hungry: ['PIOU !! FAIM', 'des graines ?'],
        idle_tired: ['piou... zzz'],
        fed: ['PIOU MERCI'],
        played: ['MEILLEUR JEU'],
        slept: ['rêves piou'],
      },
      de: {
        greet: ['PIEP PIEP', 'hallo!!'],
        idle_happy: ['piep piep', 'Federn schön'],
        idle_hungry: ['PIEP!! HUNGER', 'Körner?'],
        idle_tired: ['piep... zzz'],
        fed: ['PIEP DANKE'],
        played: ['BESTES SPIEL'],
        slept: ['Piep-Träume'],
      },
    },
  };

  // ─── Streak / mood spice ──────────────────────────────────────────
  const STREAK_LINES = {
    tr: { 3: '🔥 3. günümüz, devam!', 7: '🔥 1 hafta oldu, sen efsanesin', 30: '🔥 1 ay! daha çok seviyoruz' },
    en: { 3: '🔥 day 3, keep going!', 7: '🔥 1 week strong', 30: '🔥 1 month — legendary' },
    fr: { 3: '🔥 jour 3, continue !', 7: '🔥 1 semaine, fort', 30: '🔥 1 mois — légendaire' },
    de: { 3: '🔥 Tag 3, weiter!', 7: '🔥 1 Woche stark', 30: '🔥 1 Monat — legendär' },
  };

  // ─── API ──────────────────────────────────────────────────────────
  function detectLang() {
    const tg = window.Telegram && window.Telegram.WebApp;
    const code = (tg && tg.initDataUnsafe && tg.initDataUnsafe.user && tg.initDataUnsafe.user.language_code) || '';
    const base = code.slice(0, 2).toLowerCase();
    return SUPPORTED.includes(base) ? base : 'tr';
  }

  function pick(arr) { return arr && arr.length ? arr[Math.floor(Math.random() * arr.length)] : ''; }

  function petLine(petType, situation, lang) {
    lang = lang || detectLang();
    const byType = D[petType] || D.cat;
    const byLang = byType[lang] || byType.tr;
    return pick(byLang[situation] || []);
  }

  function streakLine(streak, lang) {
    lang = lang || detectLang();
    const map = STREAK_LINES[lang] || STREAK_LINES.tr;
    if (streak === 3) return map[3];
    if (streak === 7) return map[7];
    if (streak === 30) return map[30];
    return null;
  }

  function ui(lang) {
    lang = lang || detectLang();
    return UI[lang] || UI.tr;
  }

  window.PetI18n = { detectLang, ui, petLine, streakLine, supported: SUPPORTED };
})();
