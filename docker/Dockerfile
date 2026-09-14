FROM docker.io/library/golang:1.26-alpine AS build
WORKDIR /src
COPY app/go.mod app/go.sum ./
RUN go mod download
COPY app/ .
RUN CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o /bsimp .

FROM docker.io/library/alpine:3.23
RUN apk add --no-cache ca-certificates python3 \
    && mkdir -p /etc/bsimp \
    && chown 65532:65532 /etc/bsimp
COPY --from=build /bsimp /usr/local/bin/bsimp
COPY --chmod=755 docker/entrypoint.py /usr/local/bin/bsimp-entrypoint
USER 65532:65532
EXPOSE 8080
ENTRYPOINT ["bsimp-entrypoint"]
CMD ["-config=/etc/bsimp/config.toml", "-http=:8080"]
