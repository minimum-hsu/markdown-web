# Markdown Website

This project is within Docker.

## Build Docker image

You can directly use minimum/markdown-web image, or

### Build with docker-compose command

```sh
docker-compose -f docker-compose.yml build
```

### Build with docker command

```sh
docker build -t minimum/markdown-web -f Dockerfile .
```

## Run

### Run with docker-compose command

```sh
docker-compose -f docker-compose.yml up -d
```

### Run with docker command

```sh
docker run -d --name portal -p 80:80 minimum/markdown-web
```

## Mount your markdown files

If your files is in _./flask/markdown_,

### Run with docker-compose command

```sh
docker-compose -f mount.yml up -d
```

### Run with docker command

```sh
docker run -d --name portal -p 80:80 -v `pwd`/flask/markdown:/home/python/markdown minimum/markdown-web
```

## Open Browser

In example, openning _http://IP/_, you will see

```
Welcome to Markdown World!
``` 

## This project can do

1. In markdown directory, file can be in multi-level directory.

2. Dynamically loading files.

## TODO

1. Dynamically updating directories.
