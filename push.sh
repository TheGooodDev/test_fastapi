# Login heroku
heroku container:login

# create app on heroku
heroku create ynov-api

# docker on windows
docker build . -t ynov-api


# tag image docker au register heroku

docker tag ynov-api registry.heroku.com/ynov-api/web

#push
docker push registry.heroku.com/ynov-api/web

#release
heroku container:release web -a ynov-api