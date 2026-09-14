FROM docker.io/library/nginx:stable-alpine
RUN apk add --no-cache openssl
COPY default.conf /etc/nginx/conf.d/default.conf
COPY --chmod=755 40-basic-auth.sh /docker-entrypoint.d/40-basic-auth.sh
