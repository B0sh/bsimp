#!/usr/bin/env python3
"""Generate the container config, then replace this process with Bsimp."""
import json
import os
from pathlib import Path
import sys


def config_from_env(env):
    if not env.get("S3_BUCKET"):
        raise ValueError("S3_BUCKET must be set and non-empty")
    key = env.get("S3_ACCESS_KEY_ID", "")
    secret = env.get("S3_SECRET_ACCESS_KEY", "")
    if bool(key) != bool(secret):
        raise ValueError("S3_ACCESS_KEY_ID and S3_SECRET_ACCESS_KEY must be set together")
    path_style = env.get("S3_FORCE_PATH_STYLE", "false").lower() or "false"
    if path_style not in ("true", "false", "1", "0", "t", "f"):
        raise ValueError("S3_FORCE_PATH_STYLE must be a boolean")

    # JSON string escapes are also valid TOML basic-string escapes. TOML also
    # requires DEL to be escaped; preserve Unicode without JSON surrogate pairs.
    def quoted(value):
        return json.dumps(value, ensure_ascii=False).replace("\x7f", "\\u007f")

    lines = ["[s3]"]
    for name, default in (
        ("bucket", ""), ("region", "us-east-1"), ("endpoint", ""),
        ("base_prefix", ""), ("request_presign_expiry", "2h"),
    ):
        value = env.get("S3_" + name.upper()) or default
        lines.append(f"{name} = {quoted(value)}")
    lines.append("force_path_style = " + str(path_style in ("true", "1", "t")).lower())
    if key:
        lines.extend(["", "[s3.credentials]", f"id = {quoted(key)}",
                      f"secret = {quoted(secret)}",
                      f"token = {quoted(env.get('S3_SESSION_TOKEN', ''))}"])
    return "\n".join(lines) + "\n"


def main():
    try:
        content = config_from_env(os.environ)
        os.umask(0o077)
        path = Path("/etc/bsimp/config.toml")
        temporary = path.with_suffix(".toml.tmp")
        temporary.write_text(content, encoding="utf-8")
        temporary.chmod(0o600)
        temporary.replace(path)
    except (ValueError, OSError) as exc:
        sys.exit(f"Failed generating config: {exc}")
    os.execvp("bsimp", ["bsimp", *sys.argv[1:]])


if __name__ == "__main__":
    main()
