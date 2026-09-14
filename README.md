# Bsimp

Bsimp is a minimalistic S3-backed audio library. It lets you play audio files from an S3 bucket with any arbitrary directory structure.

It works with AWS S3 or any S3 API compatible storage such as DigitalOcean Spaces, Backblaze B2, Cloudflare R2 or MinIO.

## Why

Over the years I acquired a large library of audio files from different sources - Bandcamp, Google Music and I even ripped some CDs myself a decade ago. I wanted a way to listen my audio files from different devices and also have them backed up reliably on cloud storage. S3 solves both of these problems - it serves as a live audio library and as a backup at the same time.

I didn't want to go with the existing [open source](https://github.com/awesome-selfhosted/awesome-selfhosted#media-streaming---audio-streaming) audio streaming services. I found them resource-heavy, having many dependencies and features I would never use.

## Features

- Cover art support
- Responsive design
- Stateless - no database required

## Screenshots

Directory Browser

<img src="docs/directory-browser.png" alt="directory-browser" width="631"/>

Audio Player

<img src="docs/player.png" alt="player" width="631"/>

## Configuring

DigitalOcean Spaces config example:

```toml
[s3]
region = "nyc3"
endpoint = "https://nyc3.digitaloceanspaces.com"
bucket = "foo"

[s3.credentials]
id = "SPACES KEY"
secret = "SPACES SECRET"
```

MinIO config example:
```toml
[s3]
region = "local"
endpoint = "http://localhost:9000"
bucket = "music"
force_path_style = true

[s3.credentials]
id = "minioadmin" 
secret = "minioadmin"
```

## Running

```sh
bsimp -config=/etc/bsimp/config.toml -http=":8080"
```

## Docker Compose

Copy the example environment file and fill in your S3 bucket and credentials:

```sh
cp .env.example .env
# Edit .env, then start both containers:
docker compose up -d --build
```

Open http://localhost:8080 and sign in with username `admin` and password
`changeme`. Nginx requires HTTP Basic authentication for all app routes, including
static assets and stream redirects. Only Nginx publishes a host port; the app is
accessible within the Compose network.

The defaults are set in `docker-compose.yaml`. Override them in the `.env` file
next to it (use single quotes for passwords containing `$` or `#`):

```dotenv
AUTH_USERNAME=admin
AUTH_PASSWORD='replace-with-your-password'
HTTP_PORT=8080
```

Apply environment changes with `docker compose up -d`. At each startup, the container entrypoint
creates `/etc/bsimp/config.toml` from the `S3_*` variables with owner-only
permissions, and Nginx generates its password file. No host config file is needed.
`S3_BUCKET` is required; `.env.example` lists all supported settings. Set
`S3_ACCESS_KEY_ID` and `S3_SECRET_ACCESS_KEY` together. `S3_SESSION_TOKEN` is optional.
The defaults are region `us-east-1`, signed URL expiry `2h`, and path-style access
disabled. `.env` is excluded from Git and the image build context.

For S3-compatible storage, its endpoint must be reachable from both the container
and your browser; `localhost` inside the container refers to that container.
Standalone usage accepts a TOML file as before. Environment-to-TOML generation
is handled entirely by the Docker entrypoint.

This setup serves HTTP. Before exposing it to the Internet, replace the default
credentials and add HTTPS so Basic authentication credentials are encrypted in
transit. Audio playback redirects to temporary signed S3 URLs; those URLs remain
usable without Nginx authentication until they expire.

Stop the containers with `docker compose down`.

## Security

Bsimp doesn't have built-in authentication or rate-limiting. The server should never be exposed to the Internet directly to avoid unexpected S3 bills.

When exposed to the Internet, the server should run behind a full-fledged web server like Nginx with the following features enabled:
- HTTPS
- Authentication
- Rate Limiting

## FAQ

### What audio formats does it support?

All audio formats [supported](https://caniuse.com/?search=audio%20format) by the web browser.

### Is there a mobile app?

No, but the web interface works well on mobile phones. The Media Session API lets you control the playback from the notification bar or the lock screen.

### Does it support playlists?

No, Bsimp follows the S3 bucket directory structure.

### Does it support transcoding?

No, audio files are streamed as is.
