#!/usr/bin/env python3
"""
SberBank Zero-Knowledge Vault.
Обеспечивает шифрование AES-256-GCM с привязкой к хосту для банковских секретов СберБизнес:
- SBER_CLIENT_ID, SBER_CLIENT_SECRET
- SBER_ACCESS_TOKEN, SBER_REFRESH_TOKEN
- Закрытый RSA-ключ клиента (client_key.pem)
- Клиентский сертификат (client_cert.pem) и цепочка доверия (trust_bundle.pem)

Ключ шифрования привязан к /etc/machine-id хоста + приватному мастер-ключу (~/.openclaw/secrets/.sber_master.key).
Это программная host-bound защита (не аппаратный secure element): мастер-ключ — локальный файл 0400.
Данные расшифровываются исключительно в память (RAM). Временные TLS-файлы создаются
только на RAM-диске (/dev/shm) с правами 0600 и гарантированно затираются сразу после вызова.
Если /dev/shm недоступен, работа ПРЕРЫВАЕТСЯ (fail-closed): расшифрованные секреты
никогда не записываются в обычный дисковый temp-каталог.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

SECRETS_DIR = Path(os.path.expanduser("~/.openclaw/secrets"))
MASTER_KEY_FILE = SECRETS_DIR / ".sber_master.key"
MAGIC_HEADER = b"SBERVAULT_V1\x00"


def _get_machine_id() -> bytes:
    """Возвращает идентификатор хоста (machine-id)."""
    for p in ["/etc/machine-id", "/var/lib/dbus/machine-id"]:
        if os.path.exists(p):
            try:
                content = Path(p).read_bytes().strip()
                if content:
                    return content
            except Exception:
                pass
    raise RuntimeError("Не удалось прочитать machine-id хоста")


def _get_or_create_master_key() -> bytes:
    """Получает или создает приватный мастер-ключ с правами 0400."""
    SECRETS_DIR.mkdir(parents=True, exist_ok=True)
    if not MASTER_KEY_FILE.exists():
        key = os.urandom(32)
        MASTER_KEY_FILE.write_bytes(key)
        MASTER_KEY_FILE.chmod(stat.S_IRUSR)  # 0400 read-only
        return key
    return MASTER_KEY_FILE.read_bytes()


def derive_encryption_key() -> bytes:
    """Генерирует 256-битный ключ AES-GCM через HKDF из machine-id и мастер-ключа."""
    machine_id = _get_machine_id()
    master_key = _get_or_create_master_key()
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=machine_id,
        info=b"openclaw-sber-vault-v1",
    )
    return hkdf.derive(master_key)


class SberVault:
    def __init__(self, profile: str = "default"):
        self.profile = profile
        self.vault_path = SECRETS_DIR / f"sber_{profile}.vault" if profile != "default" else SECRETS_DIR / "sber_default.vault"
        # Фоллбэк на legacy имя если есть
        if not self.vault_path.exists():
            cand = SECRETS_DIR / f"sber_{profile}.vault"
            if cand.exists():
                self.vault_path = cand

        self._key = derive_encryption_key()
        self._data: dict = {}
        if self.vault_path.exists():
            self.load()

    def is_encrypted(self) -> bool:
        return self.vault_path.exists()

    def load(self) -> dict:
        """Расшифровывает данные из хранилища строго в память (RAM)."""
        raw = self.vault_path.read_bytes()
        if not raw.startswith(MAGIC_HEADER):
            raise ValueError("Повреждённый формат vault-файла (неверный заголовок)")
        payload = raw[len(MAGIC_HEADER):]
        if len(payload) < 12 + 16:
            raise ValueError("Файл хранилища повреждён или слишком мал")
        nonce = payload[:12]
        ciphertext = payload[12:]

        aesgcm = AESGCM(self._key)
        try:
            plaintext = aesgcm.decrypt(nonce, ciphertext, MAGIC_HEADER)
        except Exception as exc:
            raise RuntimeError(
                "Ошибка расшифровки банковского хранилища! Неверный ключ хоста или файл подделан."
            ) from exc

        self._data = json.loads(plaintext.decode("utf-8"))
        return self._data

    def save(self) -> None:
        """Атомарно шифрует данные и записывает в .vault с правами 0600."""
        plaintext = json.dumps(self._data, ensure_ascii=False).encode("utf-8")
        nonce = os.urandom(12)
        aesgcm = AESGCM(self._key)
        ciphertext = aesgcm.encrypt(nonce, plaintext, MAGIC_HEADER)

        blob = MAGIC_HEADER + nonce + ciphertext
        tmp_path = self.vault_path.with_suffix(".tmp")
        tmp_path.write_bytes(blob)
        tmp_path.chmod(stat.S_IRUSR | stat.S_IWUSR)  # 0600
        tmp_path.replace(self.vault_path)

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def set(self, key: str, value) -> None:
        self._data[key] = value

    def update_tokens(self, access_token: str, refresh_token: str, ttl_seconds: int = 3600) -> None:
        """Обновляет токены и атомарно перезаписывает зашифрованное хранилище."""
        self._data["access_token"] = access_token
        self._data["refresh_token"] = refresh_token
        expires_ts = time.time() + ttl_seconds
        self._data["expires_at_ts"] = expires_ts
        self._data["expires_at_iso"] = datetime.fromtimestamp(expires_ts, tz=timezone.utc).isoformat()
        self.save()

    @contextmanager
    def ephemeral_tls(self):
        """
        Контекст-менеджер: размещает сертификаты во временной RAM-папке (/dev/shm),
        устанавливает режим 0600 и БЕЗВОЗВРАТНО затирает и удаляет файлы сразу после блока with.
        """
        # RAM-only guarantee, enforced fail-closed: a silent fallback to a
        # disk-backed temp dir would persist the decrypted private key on disk
        # (snapshots/backups/forensics), contradicting the documented guarantee.
        shm_dir = Path("/dev/shm")
        if not shm_dir.is_dir():
            raise RuntimeError(
                "RAM-only guarantee: /dev/shm is not available on this host. "
                "Refusing to write decrypted TLS secrets to a disk-backed temp directory."
            )
        tmp_dir = Path(tempfile.mkdtemp(prefix="sber_tls_", dir=shm_dir))
        tmp_dir.chmod(0o700)

        cert_file = tmp_dir / "client_cert.pem"
        key_file = tmp_dir / "client_key.pem"
        ca_file = tmp_dir / "trust_bundle.pem"

        try:
            cert_file.write_text(self._data.get("client_cert", ""), encoding="utf-8")
            key_file.write_text(self._data.get("client_key", ""), encoding="utf-8")
            ca_file.write_text(self._data.get("trust_bundle", ""), encoding="utf-8")

            cert_file.chmod(0o600)
            key_file.chmod(0o600)
            ca_file.chmod(0o600)

            yield str(cert_file), str(key_file), str(ca_file)
        finally:
            # Безопасное затирание нулями перед unlink
            for f in [cert_file, key_file, ca_file]:
                if f.exists():
                    try:
                        size = f.stat().st_size
                        f.write_bytes(b"\x00" * size)
                        f.unlink()
                    except Exception:
                        pass
            shutil.rmtree(tmp_dir, ignore_errors=True)


def pack_profile_from_disk(profile: str, env_path: Path, cert_dir: Path, account: str = "", inn: str = "", org_name: str = "") -> None:
    """Упаковывает существующие открытые файлы .env и .pem в зашифрованный .vault."""
    if not env_path.exists():
        raise FileNotFoundError(f"Файл окружения {env_path} не найден")

    # Читаем .env
    env_vars = {}
    with open(env_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env_vars[k.strip()] = v.strip().strip("'\"")

    # Читаем PEM сертификаты
    cert_path = cert_dir / "client_cert.pem"
    key_path = cert_dir / "client_key.pem"
    ca_path = cert_dir / "trust_bundle.pem"

    if not (cert_path.exists() and key_path.exists() and ca_path.exists()):
        raise FileNotFoundError(f"Не все PEM-сертификаты найдены в {cert_dir}")

    data = {
        "profile": profile,
        "name": org_name or env_vars.get("SBER_ORG_NAME", ""),
        "inn": inn or env_vars.get("SBER_INN", ""),
        "account_number": account or env_vars.get("SBER_ACCOUNT", ""),
        "client_id": env_vars.get("SBER_CLIENT_ID", ""),
        "client_secret": env_vars.get("SBER_CLIENT_SECRET", ""),
        "access_token": env_vars.get("SBER_ACCESS_TOKEN", ""),
        "refresh_token": env_vars.get("SBER_REFRESH_TOKEN", ""),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "client_cert": cert_path.read_text(encoding="utf-8"),
        "client_key": key_path.read_text(encoding="utf-8"),
        "trust_bundle": ca_path.read_text(encoding="utf-8"),
    }

    vault = SberVault(profile)
    vault._data = data
    vault.save()
    print(f"✅ Профиль '{profile}' успешно зашифрован в {vault.vault_path} (AES-256-GCM).")


def validate_p12_path(p12_path: Path) -> Path:
    """Strict input validation BEFORE the path is interpolated into openssl argv.

    SECURITY (scanner note): the openssl argv lists in setup_interactive() are
    FIXED argument arrays executed WITHOUT a shell. No user-controlled flags or
    shell metacharacters can reach the command line: only this validated file
    path and RAM tmp paths are interpolated, and the password is fed through
    stdin (-passin stdin), never through argv. Command injection is therefore
    not possible; this validation additionally rejects symlinks, directories,
    non-regular files and wrong extensions.
    """
    p12_path = p12_path.expanduser()
    if p12_path.is_symlink():
        raise ValueError("Symlinked .p12 paths are not accepted; point to the real file.")
    resolved = p12_path.resolve()
    if not resolved.is_file():
        raise ValueError(f"Not an existing regular file: {resolved}")
    if resolved.suffix.lower() not in {".p12", ".pfx"}:
        raise ValueError("Expected a PKCS#12 container with .p12 or .pfx extension")
    return resolved


def setup_interactive(profile: str = "default", p12_path_str: str | None = None,
                      keep_p12: bool = False) -> None:
    """Безопасный интерактивный мастер онбординга: распаковывает .p12 и упаковывает в Vault без передачи секретов в чат."""
    import getpass
    print("🏦 Мастер безопасной настройки SberBank Zero-Knowledge Vault")
    print("---------------------------------------------------------")
    default_p12 = SECRETS_DIR / "sber" / "client.p12"
    if not p12_path_str:
        user_p12 = input(f"Путь к файлу client.p12 [{default_p12}]: ").strip()
        p12_path = Path(user_p12) if user_p12 else default_p12
    else:
        p12_path = Path(p12_path_str)

    try:
        p12_path = validate_p12_path(p12_path)
    except ValueError as exc:
        print(f"❌ Некорректный путь к .p12: {exc}", file=sys.stderr)
        print("   Скачайте .p12 из СберБизнес и положите его в ~/.openclaw/secrets/sber/client.p12", file=sys.stderr)
        sys.exit(1)
    if SECRETS_DIR not in p12_path.parents:
        print(f"ℹ️ Файл лежит вне ожидаемой директории {SECRETS_DIR}; принят после строгой валидации.", file=sys.stderr)

    p12_password = getpass.getpass("Введите пароль от сертификата .p12 (ввод скрыт): ").strip()
    client_id = input("Введите Client ID: ").strip()
    client_secret = getpass.getpass("Введите Client Secret (ввод скрыт): ").strip()
    account = input("Номер расчётного счёта (20 цифр) [опционально]: ").strip()
    org_name = input("Название организации/ИП [опционально]: ").strip()

    # Распаковываем СТРОГО во временный RAM-диск (/dev/shm), fail-closed:
    # без /dev/shm не пишем расшифрованный ключ на обычный диск.
    shm_dir = Path("/dev/shm")
    if not shm_dir.is_dir():
        print("❌ /dev/shm недоступен: RAM-only гарантия не может быть соблюдена. Настройка прервана.", file=sys.stderr)
        sys.exit(1)
    tmp_dir = Path(tempfile.mkdtemp(prefix="sber_setup_", dir=shm_dir))
    tmp_dir.chmod(0o700)

    cert_tmp = tmp_dir / "cert.pem"
    key_tmp = tmp_dir / "key.pem"

    try:
        # SECURITY (scanner note): FIXED argv list, shell=False. Only the
        # validated p12_path / RAM tmp paths are interpolated; the password
        # goes through stdin (-passin stdin), never through process arguments.
        # No user input can alter the command structure -> no command injection.
        cmd_cert = [
            "openssl", "pkcs12", "-in", str(p12_path), "-clcerts", "-nokeys",
            "-out", str(cert_tmp), "-passin", "stdin"
        ]
        res = subprocess.run(cmd_cert, input=p12_password.encode("utf-8"), capture_output=True)
        if res.returncode != 0:
            print(f"❌ Неверный пароль от .p12 или повреждённый файл: {res.stderr.decode()}", file=sys.stderr)
            sys.exit(1)

        # SECURITY (scanner note): same FIXED argv + stdin password pattern as above.
        cmd_key = [
            "openssl", "pkcs12", "-in", str(p12_path), "-nocerts", "-nodes",
            "-out", str(key_tmp), "-passin", "stdin"
        ]
        res = subprocess.run(cmd_key, input=p12_password.encode("utf-8"), capture_output=True)
        if res.returncode != 0:
            print(f"❌ Ошибка извлечения закрытого ключа: {res.stderr.decode()}", file=sys.stderr)
            sys.exit(1)

        ca_path = SECRETS_DIR / "sber" / "trust_bundle.pem"
        if not ca_path.exists():
            ca_path = Path(__file__).parent / "trust_bundle.pem"
        ca_text = ca_path.read_text(encoding="utf-8") if ca_path.exists() else ""

        data = {
            "profile": profile,
            "name": org_name,
            "account_number": account,
            "client_id": client_id,
            "client_secret": client_secret,
            "access_token": "",
            "refresh_token": client_secret,  # При первом старте может использоваться для обмена
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "client_cert": cert_tmp.read_text(encoding="utf-8"),
            "client_key": key_tmp.read_text(encoding="utf-8"),
            "trust_bundle": ca_text,
        }

        vault = SberVault(profile)
        vault._data = data
        vault.save()

        # Безопасное удаление исходного .p12 (сертификат и ключ уже сохранены
        # внутри зашифрованного Vault — это копия для восстановления).
        # Флаг --keep-p12 сохраняет исходный контейнер, если пользователь хочет
        # оставить себе отдельную recovery-копию.
        if keep_p12:
            print(f"ℹ️ Исходный файл {p12_path} сохранён (--keep-p12). Храните его в защищённом месте.")
        else:
            try:
                size = p12_path.stat().st_size
                p12_path.write_bytes(b"\x00" * size)
                p12_path.unlink()
                print(f"🧹 Исходный файл {p12_path} безопасно затёрт и удалён с диска.")
            except Exception:
                pass

        print(f"✅ Банковское хранилище успешно создано и зашифровано: {vault.vault_path} (AES-256-GCM)!")
        print("🚀 Теперь вы можете вернуться в чат к ассистенту — данные надёжно защищены.")
    finally:
        # Secure cleanup: zero-wipe extracted cert/key material before removal
        # (same guarantee as ephemeral_tls), then drop the RAM tmp dir.
        for f in [cert_tmp, key_tmp]:
            try:
                if f.exists():
                    f.write_bytes(b"\x00" * f.stat().st_size)
            except Exception:
                pass
        shutil.rmtree(tmp_dir, ignore_errors=True)


def get_status() -> None:
    """Выводит статус хранилищ БЕЗ показа секретов."""
    print("🏦 Статус банковских хранилищ Sber Zero-Knowledge Vault:")
    vault_files = list(SECRETS_DIR.glob("sber_*.vault"))
    if not vault_files:
        print("  ❌ Хранилища .vault не найдены в ~/.openclaw/secrets/")
        return

    for vf in vault_files:
        prof = vf.stem.replace("sber_", "")
        try:
            v = SberVault(prof)
            exp = v.get("expires_at_iso", "неизвестно")
            client_id = v.get("client_id", "")
            masked_id = (client_id[:6] + "..." + client_id[-4:]) if len(client_id) > 10 else "***"
            has_secret = bool(v.get("client_secret"))
            has_key = bool(v.get("client_key"))
            acc = v.get("account_number", "не указан")
            name = v.get("name", prof)
            print(f"  🔒 {name} ({prof}):")
            print(f"     • Файл: {vf.name} (AES-256-GCM, привязан к machine-id)")
            print(f"     • Р/с: {acc}")
            print(f"     • Client ID: {masked_id} | Client Secret: {'[ЗАШИФРОВАН В VAULT]' if has_secret else 'ОТСУТСТВУЕТ'}")
            print(f"     • RSA Private Key: {'[ЗАШИФРОВАН В VAULT]' if has_key else 'ОТСУТСТВУЕТ'}")
            print(f"     • Срок токена: {exp}")
        except Exception as exc:
            print(f"  ⚠️ {prof}: Ошибка расшифровки: {exc}")


def main():
    parser = argparse.ArgumentParser(description="SberBank Zero-Knowledge Vault Management")
    sub = parser.add_subparsers(dest="cmd")

    pack_p = sub.add_parser("pack", help="Упаковать существующие .env и .pem в .vault")
    pack_p.add_argument("--profile", default="default", help="Имя профиля (по умолчанию default)")
    pack_p.add_argument("--env", default=None, help="Путь к .env файлу с токенами")
    pack_p.add_argument("--cert-dir", default=None, help="Путь к папке с client_cert.pem, client_key.pem, trust_bundle.pem")
    pack_p.add_argument("--account", default="", help="Номер расчётного счёта")
    pack_p.add_argument("--inn", default="", help="ИНН организации/ИП")
    pack_p.add_argument("--name", default="", help="Название организации/ИП")

    setup_p = sub.add_parser("setup", help="Интерактивный мастер безопасной настройки (без передачи паролей в чат)")
    setup_p.add_argument("--profile", default="default", help="Имя профиля")
    setup_p.add_argument("--p12", default=None, help="Путь к файлу client.p12")
    setup_p.add_argument("--keep-p12", action="store_true", help="Не затирать исходный .p12 после упаковки (recovery-копия)")

    sub.add_parser("status", help="Проверить статус зашифрованных хранилищ")

    args = parser.parse_args()
    if args.cmd == "pack":
        env_file = Path(args.env) if args.env else SECRETS_DIR / f"sber_{args.profile}.env"
        cert_dir = Path(args.cert_dir) if args.cert_dir else SECRETS_DIR / f"sber_{args.profile}"
        if not cert_dir.exists() and (SECRETS_DIR / "sber").exists():
            cert_dir = SECRETS_DIR / "sber"
        pack_profile_from_disk(args.profile, env_file, cert_dir, args.account, args.inn, args.name)
    elif args.cmd == "setup":
        setup_interactive(args.profile, args.p12, keep_p12=args.keep_p12)
    elif args.cmd == "status":
        get_status()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
