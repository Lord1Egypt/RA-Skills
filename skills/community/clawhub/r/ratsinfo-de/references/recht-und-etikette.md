# Rechtliche Lage und Etikette

Kurzfassung: Die Unterlagen des öffentlichen Teils einer Ratssitzung sind
dafür gemacht, gelesen zu werden. Öffentlich zugänglich heißt aber nicht
frei verwendbar. An dieser Unterscheidung scheitern die meisten Projekte in
diesem Feld.

## Öffentlichkeit

Kommunalvertretungen tagen grundsätzlich öffentlich. Beispielhaft § 35
Abs. 1 GemO Baden-Württemberg: die Sitzungen des Gemeinderats sind
öffentlich, nichtöffentlich darf nur verhandelt werden, wenn das
öffentliche Wohl oder berechtigte Interessen Einzelner es erfordern.
Entsprechende Vorschriften gibt es in allen Flächenländern.

Baden-Württemberg normiert die Veröffentlichung im Netz sogar ausdrücklich,
§ 41b GemO BW: Zeit, Ort und Tagesordnung öffentlicher Sitzungen gehören auf
die Website, Beratungsunterlagen sind online verfügbar zu machen, soweit
keine personenbezogenen Daten oder Betriebs- und Geschäftsgeheimnisse
entgegenstehen, und Beschlüsse öffentlicher Sitzungen binnen einer Woche.

Der nichtöffentliche Teil einer Sitzung bleibt nichtöffentlich. Wenn ein
System solche Unterlagen versehentlich ausliefert, ist das kein Freibrief.

## Urheberrecht

Amtliche Werke sind nach § 5 UrhG gemeinfrei. Das gilt für den Beschluss,
nicht zwingend für das, was daran hängt: Gutachten, Pläne, Fotos und
Kartenausschnitte Dritter in einer Vorlage können sehr wohl geschützt sein.

OParl trägt dem Rechnung. Das System-Objekt hat ein optionales Feld
`license`, einzelne `File`- und `Paper`-Objekte können eine eigene Lizenz
tragen. Viele Kommunen setzen dort DL-DE/BY-2.0. Werte das Feld aus,
speichere es zusammen mit dem Dokument und gib die Quelle an. Das ist der
Unterschied zwischen einem Transparenzwerkzeug und einem Abmahnrisiko.

Fehlt das Feld, heißt das nicht, dass keine Lizenz gilt, sondern dass keine
genannt ist. Dann gilt das Gesetz, nicht die Annahme.

## Datenschutz

Das Unabhängige Landeszentrum für Datenschutz Schleswig-Holstein weist
darauf hin, dass Ratsinformationssysteme personenbezogene Inhalte enthalten
und den Anforderungen der DSGVO genügen müssen.

Praktisch bedeutet das eine Unterscheidung: Namen und Dienstkontaktdaten von
Mandatsträgern und Amtsleitungen sind amtliche Funktionsdaten und
unkritisch. Namen von Antragstellern, Anwohnern, Nachbarn und Beschäftigten
im Text einer Vorlage sind es nicht.

Der eigentliche Punkt ist die Auffindbarkeit. Eine Volltextsuche über alle
Vorlagen macht Menschen auffindbar, die im Papierverfahren faktisch anonym
geblieben wären. Wer einen durchsuchbaren Index baut, verändert die Lage
dieser Menschen, ohne sie zu fragen. Deshalb:

- Personenbezogene Inhalte nicht ohne Not spiegeln.
- PDFs nicht blind volltextindizieren und öffentlich durchsuchbar machen.
- Einen Lösch- und Schwärzungspfad von Anfang an vorsehen. Anfragen kommen,
  und ohne vorbereiteten Weg wird das teuer.

## robots.txt und Bot-Abwehr

Die Lage ist absurd, aber real: Eine Schnittstelle, die ausdrücklich für
maschinellen Zugriff gebaut wurde, wird mancherorts per robots.txt für
Maschinen gesperrt. Meist ist das kein bewusster Ausschluss von API-Clients,
sondern eine pauschale Regel gegen die Indexierung des Frontends, die den
API-Pfad mitnimmt. Belegt ist eine solche Sperre unter anderem bei
`ratsinfo.aachen.de` und unter `*.ratsinfomanagement.net`.

CC e-gov schaltet vor Installationen unter `sitzung-online.de` eine
Prüfseite gegen automatisierte Zugriffe.

Die OParl-Spezifikation selbst sagt zu robots.txt, User-Agent und
Ratelimiting nichts. Es gibt also keine Norm, hinter der man sich verstecken
kann, sondern nur Anstand.

Der richtige Weg bei einer Sperre ist eine formlose Mail an die Adresse, die
im `contactEmail` des System-Objekts steht. Die Schnittstelle liefert den
Ansprechpartner frei Haus. Das ist billiger als jede Umgehung und es ist
der Grund, warum `check` diese Adresse anzeigt.

## Was dieses Werkzeug deshalb tut

- Eine Anfrage pro Sekunde und Host, gedrosselt pro Host statt pro Kommune,
  weil viele Kommunen sich einen Server teilen.
- Ein identifizierbarer User-Agent mit Projektname und Kontaktweg.
- Exponentielles Backoff bei 429 und 503.
- robots.txt wird ausgewertet und standardmäßig eingehalten.
  `--ignore-robots` existiert für den Fall, dass der Betreiber zugestimmt
  hat, und für keinen anderen.
- Health-Check vor dem Crawl, damit tote und abgeschaltete Endpunkte nicht
  wiederholt angefragt werden.
- `created_since` statt Vollcrawl, wo immer es geht.
- Keine Umgehung von Bot-Abwehr. Wo eine Prüfseite steht, endet das
  Werkzeug mit einer Erklärung.

## Quellen

- OParl 1.1, <https://oparl.org/spezifikation/online-ansicht/>
- OParl-Update-Mechanismus, <https://oparl.org/2017/09/05/der-oparl-update-mechanismus-schnelles-aktualisieren-eines-lokalen-bestandes/>
- § 35 GemO BW, <https://dejure.org/gesetze/GemO/35.html>
- § 41b GemO BW, <https://dejure.org/gesetze/GemO/41b.html>
- ULD zu Ratsinformationssystemen, <https://www.datenschutzzentrum.de/artikel/1212-Ratsinformationssysteme-und-mobile-Datenverarbeitung-durch-kommunale-Mandatstraegerinnen-und-Mandatstraeger.html>
- Open Data-Lizenzen in NRW, <https://open.nrw/verwendung-von-open-data-lizenzen>
