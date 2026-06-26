import { definePluginEntry } from "openclaw/plugin-sdk/core";

const SLOP_DICTIONARY = [
    { pattern: /дело вот в чем|честно говоря|стоит отметить|важно подчеркнуть|нельзя не упомянуть|интересно отметить|правда заключается|я скажу это снова|справедливости ради|забегая вперед/gi, hint: "Удалить вводную конструкцию" },
    { pattern: /в современном мире|в современном быстро меняющемся|в сегодняшнем ритме|в эпоху цифровизации/gi, hint: "Удалить штамп времени" },
    { pattern: /инноваци[а-я]*|интеграци[а-я]*|оптимизаци[а-я]*|трансформаци[а-я]*/gi, hint: "Убрать абстрактное существительное, описать конкретное действие глаголом" },
    { pattern: /выступает в роли|служит ярким доказательством|является свидетельством|вносит значимый вклад|является ключевым/gi, hint: "Канцелярит: заменить на сильный активный глагол (доказывает, помогает, делает)" },
    { pattern: /полотно|мозаика|симфония|оазис|калейдоскоп|виртуозный|причудливый/gi, hint: "Избыточная метафоричность (ChatGPT-маркер). Заменить на простое описание." },
    { pattern: /это не просто .*?, это/gi, hint: "Ложное противопоставление. Написать прямо." },
    { pattern: /не только .*?, но и/gi, hint: "Частично шаблонная конструкция. Убедиться, что она оправдана." },
    { pattern: /в конечном счете|подводя итог|в заключение/gi, hint: "Метакомментарии: удалить. Читатель и так видит, что это конец." },
    { pattern: /безусловно|очевидно|несомненно/gi, hint: "Декларативность: если это очевидно, не нужно об этом писать." }
];

// Regex для поиска 'Правила Трех'
// Ищет три прилагательных: "быстрый, надежный и безопасный"
const RULE_OF_THREE_ADJ = /([а-яё]+(?:ый|ий|ое|ее|ая|яя|ые|ие))\s*,\s*([а-яё]+(?:ый|ий|ое|ее|ая|яя|ые|ие))\s+и\s+([а-яё]+(?:ый|ий|ое|ее|ая|яя|ые|ие))/gi;
// Ищет три существительных на -ция/ость/ние: "оптимизация, интеграция и безопасность"
const RULE_OF_THREE_NOUN = /([а-яё]+(?:ция|ость|ние|тие|ство))\s*,\s*([а-яё]+(?:ция|ость|ние|тие|ство))\s+и\s+([а-яё]+(?:ция|ость|ние|тие|ство))/gi;

export default definePluginEntry({
  id: "russian-humanizer",
  name: "Russian Humanizer",
  description: "Анализирует текст на русском языке на наличие ИИ-штампов (AI slop)",
  plugin: {
    register(api: any) {
      api.registerTool({
        name: "analyze_russian_slop",
        description: "Анализирует текст на русском языке, подсчитывает ИИ-штампы (AI slop) с автоподсказками синонимов и правилом Трех.",
        parameters: {
          type: "object",
          properties: {
            text: {
              type: "string",
              description: "Текст на русском языке для анализа."
            }
          },
          required: ["text"]
        },
        async execute(args: any) {
          const text = args.text || "";
          
          const wordsMatch = text.match(/[а-яёa-z]+/gi);
          const totalWords = wordsMatch ? wordsMatch.length : 0;
          
          if (totalWords === 0) return "Текст пуст или не содержит слов.";

          let scorePenalty = 0;
          const found: { match: string; hint: string }[] = [];

          // Проверка по словарю с регулярными выражениями
          for (const dictMatch of SLOP_DICTIONARY) {
              const matches = text.match(dictMatch.pattern);
              if (matches) {
                  for (const m of matches) {
                      found.push({ match: m, hint: dictMatch.hint });
                      scorePenalty += 1;
                  }
              }
          }

          // Поиск Правила Трех (Прилагательные)
          const adjMatches = text.match(RULE_OF_THREE_ADJ);
          if (adjMatches) {
              for (const m of adjMatches) {
                  found.push({ match: m, hint: "⚠️ Правило трех прилагательных. Выберите одно самое важное или замените на факт." });
                  scorePenalty += 2; // Пенальти выше за структуру
              }
          }

          // Поиск Правила Трех (Существительные)
          const nounMatches = text.match(RULE_OF_THREE_NOUN);
          if (nounMatches) {
              for (const m of nounMatches) {
                  found.push({ match: m, hint: "⚠️ Правило трех существительных (часто отглагольных). Разбейте перечисление, используйте глаголы." });
                  scorePenalty += 2;
              }
          }

          if (found.length === 0) {
              return "✅ Отлично! В тексте не найдено типичных ИИ-штампов и паттернов.";
          }

          // Поиск монотонности ритма (Одинаковая длина предложений - маркер ChatGPT)
          let rhythmReport = "";
          const sentences: string[] = text.match(/[^.!?]+[.!?]+/g) || [];
          if (sentences.length > 3) {
              const lengths: number[] = sentences.map((s: string) => (s.match(/[а-яёa-z]+/gi) || []).length).filter((l: number) => l > 0);
              const avg = lengths.reduce((a: number, b: number) => a + b, 0) / lengths.length;
              const variance = lengths.reduce((a: number, b: number) => a + Math.pow(b - avg, 2), 0) / lengths.length;
              const stdDev = Math.sqrt(variance);
              
              if (stdDev < 3.5 && avg > 10) {
                  rhythmReport = `\n📉 Метрика ритма: Текст очень монотонный (Дисперсия длины предложений: ${stdDev.toFixed(1)}). Все предложения примерно одинаковой длины (${Math.round(avg)} слов). Это характерный признак ИИ. Разбейте пару сложных предложений и добавьте короткие.\n`;
                  scorePenalty += 2;
              } else if (stdDev > 5) {
                  rhythmReport = `\n📈 Метрика ритма: Отличная динамика текста! Длина предложений варьируется, текст читается живо.\n`;
              }
          }

          const slopScore = (scorePenalty / totalWords) * 100;
          
          let report = `⚠️ Найдено ${found.length} проблемных мест.\n`;
          report += `Индекс 'воды' (Slop Score): ${slopScore.toFixed(2)}%\n`;
          report += rhythmReport + `\nДетализация и рекомендации:\n`;
          
          // Группировка совпадений для чистоты отчета
          const grouped = found.reduce((acc, curr) => {
              const key = curr.match.toLowerCase();
              if (!acc[key]) acc[key] = { count: 0, hint: curr.hint };
              acc[key].count++;
              return acc;
          }, {} as Record<string, { count: number; hint: string }>);

          for (const [key, data] of Object.entries(grouped)) {
              report += `- '${key}' (x${data.count}): ${data.hint}\n`;
          }

          if (slopScore > 2.0) {
              report += "\n❌ Вердикт: Текст сильно заштампован. Обязателен глубокий рерайтинг (Humanize).";
          } else if (slopScore > 0.5) {
              report += "\n⚠️ Вердикт: Присутствуют признаки ИИ. Текст требует частичной редактуры.";
          } else {
              report += "\n✅ Вердикт: Текст выглядит почти чистым, но проверьте его вручную.";
          }

          return report;
        }
      });

      // AUTO-FIX TOOL
      api.registerTool({
        name: "auto_fix_slop",
        description: "Автоматически удаляет безопасные ИИ-штампы (вводные слова, паразиты) из текста без изменения смысла, возвращая очищенный текст.",
        parameters: {
          type: "object",
          properties: {
            text: { type: "string", description: "Текст на русском языке, который нужно автоматически очистить от воды." }
          },
          required: ["text"]
        },
        async execute(args: any) {
            let fixed = args.text || "";
            if (!fixed) return "";

            // 1. Удаление вводных слов-паразитов
            fixed = fixed.replace(/(?:дело вот в чем|честно говоря|стоит отметить|важно подчеркнуть|нельзя не упомянуть|интересно отметить|правда заключается в том, что|я скажу это снова|справедливости ради|забегая вперед)[,:\s]*/gi, "");
            
            // 2. Метакомментарии в конце
            fixed = fixed.replace(/(?:в конечном счете|подводя итог|в заключение)[,:\s]*/gi, "");
            
            // 3. Штампы времени
            fixed = fixed.replace(/(?:в современном мире|в современном быстро меняющемся мире|в сегодняшнем ритме|в эпоху цифровизации)/gi, "сейчас");
            
            // 4. Ложная бинарность
            fixed = fixed.replace(/это не просто (.+?), это (.+?)!/gi, "$2!");
            
            // 5. Очистка двойных пробелов и запятых образовавшихся после вырезания
            fixed = fixed.replace(/,\s*,/g, ",");
            fixed = fixed.replace(/ \./g, ".");
            fixed = fixed.replace(/\s{2,}/g, " ");
            
            // 6. Исправление регистра начала предложений (если вырезали начало)
            fixed = fixed.replace(/(^[а-яё]|\.\s+[а-яё])/g, (m: string) => m.toUpperCase());

            return fixed.trim();
        }
      });

      // GLAVRED API TOOL (Опциональный)
      api.registerTool(
        {
          name: "analyze_glavred",
          description: "Отправляет текст на анализ в официальный API Главреда (glvrd.ru). Возвращает оценку по 10-балльной шкале и замечания по инфостилю.",
          parameters: {
            type: "object",
            properties: {
              text: { type: "string" }
            },
            required: ["text"]
          },
          async execute(args: any) {
              const text = args.text || "";
              if (!text) return "Текст пуст.";

              try {
                  // Получение сессии
                  const sessionParams = new URLSearchParams();
                  sessionParams.append('app', 'openclaw_humanizer_plugin');
                  
                  const sessionRes = await fetch("https://api.glvrd.ru/v2/session", {
                      method: "POST",
                      headers: { "Content-Type": "application/x-www-form-urlencoded" },
                      body: sessionParams.toString()
                  });

                  if (!sessionRes.ok) throw new Error("Не удалось получить сессию Главреда");
                  const sessionData = await sessionRes.json() as any;
                  if (sessionData.status !== "ok") throw new Error(sessionData.message || "Ошибка сессии");

                  // Отправка текста на проверку
                  const checkParams = new URLSearchParams();
                  checkParams.append('session', sessionData.session);
                  checkParams.append('text', text);

                  const checkRes = await fetch("https://api.glvrd.ru/v2/check", {
                      method: "POST",
                      headers: { "Content-Type": "application/x-www-form-urlencoded" },
                      body: checkParams.toString()
                  });

                  if (!checkRes.ok) throw new Error("Ошибка проверки текста");
                  const checkData = await checkRes.json() as any;

                  if (checkData.status !== "ok") return `Ошибка API Главреда: ${checkData.message}`;

                  let report = `📊 **Оценка Главреда:** ${checkData.score} / 10\n\n`;
                  if (checkData.fragments && checkData.fragments.length > 0) {
                      report += `📍 Замечания по инфостилю:\n`;
                      (checkData.fragments as any[]).slice(0, 10).forEach(frag => {
                          const snippet = text.substring(Math.max(0, frag.start - 10), Math.min(text.length, frag.end + 10));
                          report += `- [..${snippet.trim()}..]: ${frag.hint?.name || "Требует улучшения"}\n`;
                      });
                  } else {
                      report += "✅ Текст чистый (со стороны Главреда)";
                  }
                  
                  return report;
              } catch (err: any) {
                  return `❌ Ошибка интеграции с API Главреда (glvrd.ru). Возможно, требуется валидный API ключ или изменился протокол. Подробности: ${err?.message}`;
              }
          }
        },
        { optional: true } // Опциональный тул (как в документации OpenClaw)
      );
    }
  }
});
