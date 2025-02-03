# Login heroku
heroku container:login

# Création d'une image docker
docker build . -t ynov-api

# Start un container
docker run -p 5000:8000 -e PORT=5000 -v "$(pwd):/home/app" -it ynov-api