#!/bin/sh
set -eu

: "${AUTH_USERNAME:?AUTH_USERNAME must be set and non-empty}"
: "${AUTH_PASSWORD:?AUTH_PASSWORD must be set and non-empty}"

# Colons and line breaks would corrupt the htpasswd record.
case "$AUTH_USERNAME" in
  *:*|*[[:cntrl:]]*) echo 'AUTH_USERNAME must not contain colons or control characters' >&2; exit 1 ;;
esac
case "$AUTH_PASSWORD" in
  *[[:cntrl:]]*) echo 'AUTH_PASSWORD must not contain control characters' >&2; exit 1 ;;
esac

umask 077
password_hash=$(printf '%s\n' "$AUTH_PASSWORD" | openssl passwd -apr1 -stdin)
printf '%s:%s\n' "$AUTH_USERNAME" "$password_hash" > /etc/nginx/.htpasswd
chown root:nginx /etc/nginx/.htpasswd
chmod 640 /etc/nginx/.htpasswd
unset AUTH_USERNAME AUTH_PASSWORD password_hash
