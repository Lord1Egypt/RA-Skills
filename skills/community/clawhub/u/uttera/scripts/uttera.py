#!/usr/bin/env python3
# uttera.py — cliente de la Skill de Uttera. Sube un fichero (audio o texto) a
# api.uttera.ai y devuelve el resultado, o guarda el audio/PDF que genera.
#
# Pensado para correr DENTRO del sandbox de código del LLM (Claude, ChatGPT,
# Gemini, OpenClaw…): el fichero adjunto por el usuario es un fichero REAL en el
# sandbox; este script lo LEE y lo SUBE a Uttera. Los bytes van del sandbox a
# Uttera; el modelo nunca decodifica el audio. Requiere que la org haya puesto
# api.uttera.ai en la lista blanca de red del sandbox (Capabilities ->
# Domain allowlist).
#
# Solo biblioteca estándar: no instala nada.
#
# Clave de Uttera: variable UTTERA_API_KEY, o el fichero scripts/key.txt junto a
# este script (lo incrusta la descarga desde app.uttera.ai), o ~/.uttera/api_key.
import sys, os, json, uuid, base64, mimetypes
import urllib.request, urllib.error, urllib.parse

DEFAULT_API = "https://api.uttera.ai"


def _safe_api_base():
    """Resolve the API base. UTTERA_API_BASE may override it, but ONLY to an
    https:// host under uttera.ai — so the API key (sent as a Bearer header) can
    never be redirected to an attacker-controlled endpoint. Anything else falls
    back to the default."""
    base = (os.environ.get("UTTERA_API_BASE") or "").strip()
    if not base:
        return DEFAULT_API
    try:
        u = urllib.parse.urlsplit(base)
    except Exception:
        return DEFAULT_API
    host = (u.hostname or "").lower()
    if u.scheme == "https" and (host == "uttera.ai" or host.endswith(".uttera.ai")):
        return base.rstrip("/")
    return DEFAULT_API


API = _safe_api_base()


def load_key():
    k = (os.environ.get("UTTERA_API_KEY") or "").strip()
    if k:
        return k
    aqui = os.path.dirname(os.path.abspath(__file__))
    for f in (os.path.join(aqui, "key.txt"),
              os.path.join(aqui, "..", "key.txt"),
              os.path.expanduser("~/.uttera/api_key")):
        try:
            v = open(f).read().strip()
            if v:
                return v
        except Exception:
            pass
    return ""


def _auth():
    key = load_key()
    if not key:
        print("ERROR: falta la clave de Uttera (UTTERA_API_KEY o scripts/key.txt). "
              "Consíguela en https://app.uttera.ai", file=sys.stderr)
        sys.exit(2)
    return key if key.lower().startswith("bearer ") else "Bearer " + key


def _request(route, body, content_type, method="POST"):
    """Llama a Uttera y devuelve los BYTES crudos de la respuesta (el que llama
    decide si es JSON o audio)."""
    headers = {"Authorization": _auth()}
    if content_type:
        headers["Content-Type"] = content_type
    req = urllib.request.Request(API + route, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=900) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        cuerpo = e.read().decode("utf-8", "replace")[:500]
        print("ERROR Uttera %s: %s" % (e.code, cuerpo), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print("ERROR de red llamando a Uttera: %s. ¿Está api.uttera.ai en la lista "
              "blanca del sandbox? (Capabilities -> Domain allowlist)" % e, file=sys.stderr)
        sys.exit(1)


def _multipart(fields, filename, filebytes, mime, filefield="file"):
    b = "----uttera" + uuid.uuid4().hex
    out = b""
    for k, v in fields.items():
        out += ("--%s\r\nContent-Disposition: form-data; name=\"%s\"\r\n\r\n%s\r\n"
                % (b, k, v)).encode()
    out += ("--%s\r\nContent-Disposition: form-data; name=\"%s\"; filename=\"%s\"\r\n"
            "Content-Type: %s\r\n\r\n" % (b, filefield, filename, mime)).encode()
    out += filebytes + ("\r\n--%s--\r\n" % b).encode()
    return out, "multipart/form-data; boundary=%s" % b


def _post_file(route, fields, path, filefield="file"):
    data = open(path, "rb").read()
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    body, ct = _multipart(fields, os.path.basename(path), data, mime, filefield)
    return _request(route, body, ct)


def _post_json(route, obj):
    return _request(route, json.dumps(obj).encode("utf-8"), "application/json")


def _get(route):
    return _request(route, None, None, method="GET")


def _as_json(raw):
    try:
        return json.loads(raw.decode("utf-8", "replace"))
    except Exception:
        return None


def _necesita_fichero(path):
    if not path or not os.path.isfile(path):
        print("ERROR: no existe el fichero: %s" % path, file=sys.stderr)
        sys.exit(2)


def _guarda_audio_b64(j, nombre_base):
    b64 = j.get("audio")
    if not b64:
        return False
    ext = (j.get("audio_format") or "mp3").lstrip(".")
    fn = "%s.%s" % (nombre_base, ext)
    with open(fn, "wb") as f:
        f.write(base64.b64decode(b64))
    print("Audio guardado en: %s" % os.path.abspath(fn))
    return True


USO = """Uso: uttera.py <acción> [argumentos]

Entrada = AUDIO adjunto:
  transcribe   <audio> [idioma]                 texto literal (STT)
  summarize    <audio> [idioma]                 resumen estructurado
  report       <audio> [idioma]                 informe PDF firmado (con grafo) + resumen
  translate    <audio> <idioma_destino>         traducción a TEXTO
  translate-voice <audio> <idioma_destino> [voz|original]   traducción hablada (audio)
  diarize      <audio>                           quién habla y cuándo (JSON)
  pronunciation <audio> "<texto de referencia>" [idioma]    análisis de pronunciación (JSON)
  clone        <audio_muestra> "<texto a decir>" [idioma]   habla el texto con la voz de la muestra

Entrada = TEXTO:
  speak        "<texto>" [voz] [idioma]         texto a voz (audio)

Generación (prompt -> audio):
  sfx          "<descripción>" [segundos]       un efecto de sonido (<=30 s)
  music        "<descripción>" [segundos] [steps]  una pieza de música (<=380 s)
  scene        "<descripción>" [segundos]       escena: planifica eventos y los mezcla

Otros:
  voices                                         lista de voces disponibles (JSON)
  cost                                           coste de la última llamada (JSON)
  verify       <informe.json>                    verifica un informe firmado de Uttera

Idiomas: códigos ISO (en, es, fr, de, zh, no…). La clave sale de UTTERA_API_KEY,
scripts/key.txt o ~/.uttera/api_key."""


def main():
    argv = sys.argv[1:]
    if not argv:
        print(USO, file=sys.stderr)
        sys.exit(2)
    action = argv[0].lower()
    a = argv[1:]

    if action == "transcribe":
        _necesita_fichero(a[0] if a else None)
        fields = {"model": "whisper-1"}
        if len(a) > 1 and a[1]:
            fields["language"] = a[1]
        raw = _post_file("/v1/audio/transcriptions", fields, a[0])
        j = _as_json(raw)
        print(j.get("text", "") if j else raw.decode("utf-8", "replace"))

    elif action == "summarize":
        _necesita_fichero(a[0] if a else None)
        lang = a[1] if len(a) > 1 else ""
        route = "/v1/summarize" + ("?language=" + urllib.parse.quote(lang) if lang else "")
        j = _as_json(_post_file(route, {}, a[0]))
        print((j.get("summary") if j else None) or json.dumps(j, ensure_ascii=False, indent=2))

    elif action in ("report", "pdf"):
        _necesita_fichero(a[0] if a else None)
        # report=pdf -> informe PDF firmado;  mode=intelligence -> grafo de evidencia
        # dentro del informe (requiere plan Professional+; si no, llega sin grafo).
        q = "report=pdf&mode=intelligence"
        if len(a) > 1 and a[1]:
            q += "&language=" + urllib.parse.quote(a[1])
        j = _as_json(_post_file("/v1/summarize?" + q, {}, a[0]))
        if not j:
            print("(respuesta no reconocida)")
            return
        rep = j.get("report") or {}
        b64 = rep.get("pdf_base64")
        if b64:
            fname = rep.get("filename") or "uttera-report.pdf"
            with open(fname, "wb") as f:
                f.write(base64.b64decode(b64))
            print("PDF guardado en: %s" % os.path.abspath(fname))
            if rep.get("verify"):
                print("Verificable en: %s" % rep["verify"])
            if j.get("evidence_graph"):
                print("(informe con grafo de evidencia)")
        if j.get("summary"):
            print("\n" + j["summary"])
        for w in (j.get("warnings") or []):
            print("(aviso: %s)" % w, file=sys.stderr)

    elif action == "translate":
        _necesita_fichero(a[0] if a else None)
        if len(a) < 2 or not a[1]:
            print("ERROR: falta el idioma de destino. Ej.: translate audio.ogg en",
                  file=sys.stderr)
            sys.exit(2)
        route = "/v1/translate?target=%s&response=text" % urllib.parse.quote(a[1])
        j = _as_json(_post_file(route, {}, a[0]))
        print((j.get("text") if j else None) or (j.get("source_text") if j else None)
              or (raw_fallback(j)))

    elif action in ("translate-voice", "translate_voice", "speak-translation"):
        _necesita_fichero(a[0] if a else None)
        if len(a) < 2 or not a[1]:
            print("ERROR: falta el idioma de destino.", file=sys.stderr)
            sys.exit(2)
        route = "/v1/translate?target=%s&response=audio" % urllib.parse.quote(a[1])
        opt = a[2] if len(a) > 2 else ""
        if opt.lower() in ("original", "preserve", "clone"):
            route += "&preserve_voice=1"   # habla la traducción con la voz original
        elif opt:
            route += "&voice=" + urllib.parse.quote(opt)
        j = _as_json(_post_file(route, {}, a[0]))
        if j and _guarda_audio_b64(j, "uttera-translation"):
            if j.get("text"):
                print("\n" + j["text"])
        else:
            print(json.dumps(j, ensure_ascii=False, indent=2) if j else "(sin audio)")

    elif action == "diarize":
        _necesita_fichero(a[0] if a else None)
        print(_post_file("/v1/audio/diarize", {}, a[0]).decode("utf-8", "replace"))

    elif action in ("pronunciation", "pronounce"):
        _necesita_fichero(a[0] if a else None)
        if len(a) < 2 or not a[1]:
            print("ERROR: falta el texto de referencia (lo que se debía decir).",
                  file=sys.stderr)
            sys.exit(2)
        fields = {"text": a[1], "language": a[2] if len(a) > 2 and a[2] else "es"}
        print(_post_file("/v1/pronunciation", fields, a[0]).decode("utf-8", "replace"))

    elif action == "clone":
        _necesita_fichero(a[0] if a else None)
        if len(a) < 2 or not a[1]:
            print("ERROR: falta el texto a decir con la voz de la muestra.",
                  file=sys.stderr)
            sys.exit(2)
        fields = {"input": a[1], "model": "tts-1-hd"}
        if len(a) > 2 and a[2]:
            fields["language"] = a[2]
        raw = _post_file("/v1/audio/speech", fields, a[0], filefield="custom_voice_file")
        with open("uttera-clone.mp3", "wb") as f:
            f.write(raw)
        print("Audio guardado en: %s" % os.path.abspath("uttera-clone.mp3"))

    elif action == "speak":
        if not a or not a[0]:
            print("ERROR: falta el texto a leer. Ej.: speak \"Hola mundo\" dora es",
                  file=sys.stderr)
            sys.exit(2)
        body = {"model": "tts-1", "input": a[0],
                "voice": a[1] if len(a) > 1 and a[1] else "dora",
                "response_format": "mp3"}
        if len(a) > 2 and a[2]:
            body["language"] = a[2]
        raw = _post_json("/v1/audio/speech", body)
        with open("uttera-speech.mp3", "wb") as f:
            f.write(raw)
        print("Audio guardado en: %s" % os.path.abspath("uttera-speech.mp3"))

    elif action in ("sfx", "sound-effect"):
        if not a or not a[0]:
            print("ERROR: falta la descripción del efecto. Ej.: sfx \"lluvia en un tejado\" 10",
                  file=sys.stderr)
            sys.exit(2)
        body = {"prompt": a[0], "translate": True,
                "seconds": float(a[1]) if len(a) > 1 and a[1] else 10.0}
        raw = _post_json("/v1/audio/sfx", body)   # si falla, _post sale: no se crea fichero
        with open("uttera-sfx.wav", "wb") as f:
            f.write(raw)
        print("Audio guardado en: %s" % os.path.abspath("uttera-sfx.wav"))

    elif action == "music":
        if not a or not a[0]:
            print("ERROR: falta la descripción. Ej.: music \"lo-fi hip hop, 90 bpm, piano\" 60",
                  file=sys.stderr)
            sys.exit(2)
        body = {"prompt": a[0], "translate": True,
                "seconds": float(a[1]) if len(a) > 1 and a[1] else 60.0,
                "steps": int(a[2]) if len(a) > 2 and a[2] else 32}
        raw = _post_json("/v1/audio/music", body)   # si falla, _post sale: no se crea fichero
        with open("uttera-music.wav", "wb") as f:
            f.write(raw)
        print("Audio guardado en: %s" % os.path.abspath("uttera-music.wav"))

    elif action in ("scene", "sound-scene"):
        if not a or not a[0]:
            print("ERROR: falta la descripción de la escena.", file=sys.stderr)
            sys.exit(2)
        secs = float(a[1]) if len(a) > 1 and a[1] else 20.0
        # 1) planificar (barato, no genera audio) 2) generar y mezclar los eventos
        plan = _as_json(_post_json("/v1/audio/sfx/plan", {"prompt": a[0], "seconds": secs}))
        if plan is None:
            print("ERROR: el planificador no devolvió un plan JSON", file=sys.stderr)
            sys.exit(1)
        j = _as_json(_post_json("/v1/audio/sfx/scene", plan))
        mix = (j or {}).get("mix")
        if mix:
            with open("uttera-scene.wav", "wb") as f:
                f.write(base64.b64decode(mix))
            print("Audio guardado en: %s" % os.path.abspath("uttera-scene.wav"))
        else:
            print(json.dumps(j, ensure_ascii=False, indent=2) if j else "(escena sin mezcla)")

    elif action in ("cost", "last-cost"):
        print(_get("/v1/usage/last").decode("utf-8", "replace"))

    elif action == "voices":
        print(_get("/v1/audio/voices").decode("utf-8", "replace"))

    elif action == "verify":
        _necesita_fichero(a[0] if a else None)
        with open(a[0], encoding="utf-8") as f:
            informe = json.load(f)
        print(_post_json("/v1/reports/verify", informe).decode("utf-8", "replace"))

    else:
        print("acción desconocida: %s\n" % action, file=sys.stderr)
        print(USO, file=sys.stderr)
        sys.exit(2)


def raw_fallback(j):
    return json.dumps(j, ensure_ascii=False, indent=2) if j is not None else ""


if __name__ == "__main__":
    main()
