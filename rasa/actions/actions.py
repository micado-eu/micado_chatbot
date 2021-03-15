from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Tracker, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import (
    SlotSet,
    UserUtteranceReverted,
    ConversationPaused,
    EventType,
    FollowupAction,
)
import requests
import logging
import os
import sys

logger = logging.getLogger(__name__)
root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)
logger.addHandler(handler)

class ActionSubmitDocumentForm(Action):
    def name(self) -> Text:
        return "action_submit_document_form"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:
        """Once we have all the information, attempt to add it to the
        Google Drive database"""

        import datetime

        document = tracker.get_slot("document")

        try:
            logger.info("trying doing something")
            logger.info(document)
            dispatcher.utter_message(template="utter_slots_values")
            return []
        except Exception as e:
            logger.error(
                "Failed to do our things. Error: {}" "".format(e.message),
                exc_info=True,
            )
            dispatcher.utter_message(template="utter_slots_values")
            return []



class ValidateDocumentForm(FormValidationAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""
        logger.info("returned the name")
        return "validate_document_form"

 #   @staticmethod
 #   def required_slots(tracker: Tracker) -> List[Text]:
 #       """A list of required slots that the form has to fill"""
 #       logger.info("required a slot")#
#
#        return ["document"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        logger.info("slot_mapping")
        logger.info(self.from_entity(entity="document", not_intent="chitchat"))

        return {
            "document": self.from_entity(entity="document", not_intent="chitchat"),
        }

    # USED FOR DOCS: do not rename without updating in docs
    @staticmethod
    def document_db() -> List[Text]:
        """Database of supported cuisines"""

        return [
            "residence permit",
            "stamp duty",
            "identity card",
            "passport",
        ]


    # USED FOR DOCS: do not rename without updating in docs
    def validate_document(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate document value."""

        logger.info("validate_document in the action")
        logger.info(value)
        if value.lower() in self.document_db():
            # validation succeeded, set the value of the "document" slot to value
            logger.info("valid document asked")
            return {"document": value}
        else:
            dispatcher.utter_message(template="utter_wrong_document")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"document": None}


    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        
        logger.info("in the submit")

        lang = "en"
        document = tracker.get_slot("document")
        url = "https://api.micadoproject.eu/backend/1.0.0/process_x_doc"

        logger.info(tracker)
        logger.info(url)
        
        headers = {"Prefer": "resolution=merge-duplicates","apikey": "eyJ4NXQiOiJaalJtWVRNd05USmpPV1U1TW1Jek1qZ3pOREkzWTJJeU1tSXlZMkV6TWpkaFpqVmlNamMwWmc9PSIsImtpZCI6ImdhdGV3YXlfY2VydGlmaWNhdGVfYWxpYXMiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsImFwcGxpY2F0aW9uIjp7Im93bmVyIjoiYWRtaW4iLCJ0aWVyIjoiVW5saW1pdGVkIiwibmFtZSI6IkRlZmF1bHRBcHBsaWNhdGlvbiIsImlkIjoxLCJ1dWlkIjoiNzBmNGQ5MzEtNmQxYi00ZGJiLThiZGItNjgyNGViZWRhNjA5In0sInRpZXJJbmZvIjp7IlVubGltaXRlZCI6eyJzdG9wT25RdW90YVJlYWNoIjp0cnVlLCJzcGlrZUFycmVzdExpbWl0IjowLCJzcGlrZUFycmVzdFVuaXQiOm51bGx9fSwia2V5dHlwZSI6IlBST0RVQ1RJT04iLCJzdWJzY3JpYmVkQVBJcyI6W3sic3Vic2NyaWJlclRlbmFudERvbWFpbiI6ImNhcmJvbi5zdXBlciIsIm5hbWUiOiJQb3N0Z1JFU1RBUEkiLCJjb250ZXh0IjoiXC9kYlwvdjAxIiwicHVibGlzaGVyIjoiYWRtaW4iLCJ2ZXJzaW9uIjoidjAxIiwic3Vic2NyaXB0aW9uVGllciI6IlVubGltaXRlZCJ9LHsic3Vic2NyaWJlclRlbmFudERvbWFpbiI6ImNhcmJvbi5zdXBlciIsIm5hbWUiOiJtaWNhZG9fYmFja2VuZCIsImNvbnRleHQiOiJcL2JhY2tlbmRcLzEuMC4wIiwicHVibGlzaGVyIjoiYWRtaW4iLCJ2ZXJzaW9uIjoiMS4wLjAiLCJzdWJzY3JpcHRpb25UaWVyIjoiVW5saW1pdGVkIn0seyJzdWJzY3JpYmVyVGVuYW50RG9tYWluIjoiY2FyYm9uLnN1cGVyIiwibmFtZSI6ImNoYXRib3QiLCJjb250ZXh0IjoiXC9ib3RcL3YwMSIsInB1Ymxpc2hlciI6ImFkbWluIiwidmVyc2lvbiI6InYwMSIsInN1YnNjcmlwdGlvblRpZXIiOiJVbmxpbWl0ZWQifV0sImlhdCI6MTU5MjkyMDczMCwianRpIjoiMmZmYzQ3ZTMtMDZkYi00NGIxLWE1NmEtMDhhMjdmOTkyY2JlIn0=.Ud-i7sAF3B915zglltrumtL8TXnojdBEpamYqk1tz4qhzQEyj6UOkrZJELA3C4Czn8x0tFlBEeNz23v6deGs8g_KZRHXrW6mYBH7bRZ-Fbp6yntPhgaUr-e28cTZZlHmOwB0256e1uEFWTnZvjSvomhJHOTi2Zl1fO89So3uHkWA9qYmAU77Z5qz-GlYvDq2G6VTTtYZLIvJ8fkICj53tN_TH6VLHBEIExNtDwV5m4yTMsoxrsHuIuLMNgpczx3ejwk4b81NobJgE2K3Uq7ihKAHo8tZ10qX91q8qDRPVXfjLQE7qTmoOKLPrhXsE3pvuMJyMpESmEn0oKOaphs9Og=="}
        params=[('lang','en'), ('document',document)]
        response_dict = requests.get(url, headers=headers, params=params)

        # logger.info(response_dict.headers)
        logger.info(response_dict.text)
        logger.info(response_dict.request)
        logger.info(response_dict)
        # utter submit template
        dispatcher.utter_message(channel="micado", custom=response_dict.text)
        return []

