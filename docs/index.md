# Test

Test mkdocs. All this documentation is just random.

## Changelog

- Use github actions

## Getting started

### Configuration

This API use environment variables as a configuration. You can use the
default example file:

    # Create your own env file from example
    cp .env.example .env
    vim .env
    source .env

    # Install your python virtual environment
    pipenv install

#### Environment variables

Name | Description,  usage | Mandatory | Default
--- | --- | --- | ---
ENV | Environment name on which Flask is currently running | No | production
DEBUG | Enable debug mode  | No | False
TESTING | Enable testing mode  | No | False
FLASK_HOST | Addr to expose flask server (ex: 0.0.0.0) | No | 127.0.0.1
FLASK_PORT |  Port of flask server | No | 5000
FLASK_SECRET |  Secret used by Flask | Yes |
DATABASE_TYPE | Database type (only "postgres" supported curently)  | Yes |
DATABASE_HOST | Database server IP or domain name  | Yes |
DATABASE_PORT | Database server port | Yes |
DATABASE_NAME | Database name | Yes |
DATABASE_USER | Database user name | Yes |
DATABASE_PASSWORD | Database password | Yes |

### Launch API

2 alternatives:

#### Run API in your local environment

    # Laucnh API in development mode
    pipenv run python run.py

#### Run API with Docker

    # Build & run API with Docker
    docker build -t grid_api:latest .
    docker run -d -p $FLASK_PORT:$FLASK_PORT --env-file .env --name my_grid_api grid_api:latest

