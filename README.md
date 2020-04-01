# Joyjet-tech-interview

#### API RESPONSES

Clone this repo:\
` git clone git@github.com:ilitotor/Joyjet-tech-interview.git `

Go to the project directory and build project container:\
`docker build -t flask:latest . `

Run:\
`docker run -d -p 5000:5000 flask`

To access the responses via terminal:\
`curl -i http://0.0.0.0:5000/level1`

`curl -i http://0.0.0.0:5000/level2`

`curl -i http://0.0.0.0:5000/level3`

#### TESTS

Run:\
`docker ps`

Get the _Container ID_ then run:\
`docker exec -ti <container id> bash`

Then run:\
`python test_app.py`
