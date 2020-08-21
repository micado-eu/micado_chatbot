## happy path short
* greet
    - utter_greet
* request_document
    - document_form
    - form{"name": "document_form"}
    - form{"name": null}
    - action_restart

## happy path
* greet
    - utter_greet
* request_document
    - document_form
    - form{"name": "document_form"}
    - form{"name": null}
* thankyou
    - utter_noworries
    - action_restart

## unhappy path
* greet
    - utter_greet
* request_document
    - document_form
    - form{"name": "document_form"}
* chitchat
    - utter_chitchat
    - document_form
    - form{"name": null}
    - utter_slots_values_document
* thankyou
    - utter_noworries
    - action_restart

## very unhappy path
* greet
    - utter_greet
* chitchat
    - utter_chitchat
    - document_form
* chitchat
    - utter_chitchat
    - document_form
* chitchat
    - utter_chitchat
    - document_form
    - form{"name": null}
    - utter_slots_values_document
* thankyou
    - utter_noworries
    - action_restart

## stop but continue path
* greet
    - utter_greet
* request_document
    - document_form
    - form{"name": "document_form"}
* stop
    - utter_ask_continue
* affirm
    - document_form
    - form{"name": null}
    - utter_slots_values_document
* thankyou
    - utter_noworries
    - action_restart

## stop and really stop path
* greet
    - utter_greet
* request_document
    - document_form
    - form{"name": "document_form"}
* stop
    - utter_ask_continue
* deny
    - action_deactivate_form
    - form{"name": null}
    - action_restart

## chitchat stop but continue path
* request_document
    - document_form
    - form{"name": "document_form"}
* chitchat
    - utter_chitchat
    - document_form
* stop
    - utter_ask_continue
* affirm
    - document_form
    - form{"name": null}
    - utter_slots_values_document
* thankyou
    - utter_noworries
    - action_restart

## stop but continue and chitchat path
* greet
    - utter_greet
* request_document
    - document_form
    - form{"name": "document_form"}
* stop
    - utter_ask_continue
* affirm
    - document_form
* chitchat
    - utter_chitchat
    - document_form
    - form{"name": null}
    - utter_slots_values_document
* thankyou
    - utter_noworries
    - action_restart

## chitchat stop but continue and chitchat path
* greet
    - utter_greet
* request_document
    - document_form
    - form{"name": "document_form"}
* chitchat
    - utter_chitchat
    - document_form
* stop
    - utter_ask_continue
* affirm
    - document_form
* chitchat
    - utter_chitchat
    - document_form
    - form{"name": null}
    - utter_slots_values_document
* thankyou
    - utter_noworries
    - action_restart

## chitchat, stop and really stop path
* greet
    - utter_greet
* request_document
    - document_form
    - form{"name": "document_form"}
* chitchat
    - utter_chitchat
    - document_form
* stop
    - utter_ask_continue
* deny
    - action_deactivate_form
    - form{"name": null}
    - action_restart

## bot challenge
* bot_challenge
  - utter_iamabot
    - action_restart
