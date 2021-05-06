# micado_chatbot
Repository for the chatbot code


To develop the chatbot the pipeline is as follows:
- (set -a; source prod.env; set +a; docker-compose -f docker-compose.yaml up -d micado_db action_server) : this allows to have DB and action server working
- (set -a; source prod.env; set +a; docker-compose -f docker-compose.yaml run  chatbot_shell) : this run the chatbot interactive shell to talk with the bot in debug mode and see the analisys that it does on the message
- (set -a; source prod.env; set +a; docker-compose -f docker-compose.yaml run  chatbot_train) : to train a new model