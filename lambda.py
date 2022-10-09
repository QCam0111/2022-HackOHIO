# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
import pymysql

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

db = pymysql.connect(host='masterpasswordvault.cwhx4xtc0ihm.us-east-1.rds.amazonaws.com', port=3306, user='admin', password='Team404error')
cursor = db.cursor()
cursor.execute("USE masterpasswordvault")

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to the Password Vault Manager."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class GetEntryIntentHandler(AbstractRequestHandler):
    """Handler for Get Entry Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GetEntryIntent")(handler_input)
        
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        goToVault = ask_utils.request_util.get_slot_value(handler_input, "vaultName")
        getService = ask_utils.request_util.get_slot_value(handler_input, "service")
        
        getUser = ("SELECT USERNAME FROM " + goToVault + " WHERE SERVICE=%s")
        cursor.execute(getUser,getService)
        
        speak_output = "The username is " + cursor.fetchone()[0]
        getPass = ("SELECT PASSWORD FROM " + goToVault + " WHERE SERVICE=%s")
        cursor.execute(getPass,getService)
        
        speak_output = speak_output + ", and the password is " + cursor.fetchone()[0]
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Would you like to do anything else?")
                .response
        )
    
    
class CreateVaultIntentHandler(AbstractRequestHandler):
    """Handler for Create Vault Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CreateVaultIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slotName = ask_utils.request_util.get_slot_value(handler_input, "vaultName")
        cursor.execute("CREATE TABLE " + slotName + " (SERVICE VARCHAR(32), USERNAME VARCHAR(32), PASSWORD VARCHAR(32))")
        speak_output = "The vault " + slotName + " has been created."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Would you like to do anything else?")
                .response
        )

class AddEntryIntentHandler(AbstractRequestHandler):
    """Handler for Add Entry Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AddEntryIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        vault = ask_utils.request_util.get_slot_value(handler_input, "vaultName")
        service = ask_utils.request_util.get_slot_value(handler_input, "service")
        username = ask_utils.request_util.get_slot_value(handler_input, "username")
        password = ask_utils.request_util.get_slot_value(handler_input, "password")
        
        insertSQL = "INSERT INTO " + vault + " (SERVICE, USERNAME, PASSWORD) VALUES (%s, %s, %s)"
        cursor.execute(insertSQL, (service,username,password))
        db.commit()
        speak_output = "Uhh, lets go!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class RemoveEntryIntentHandler(AbstractRequestHandler):
    """Handler for Remove Entry Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("RemoveEntryIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        vault = ask_utils.request_util.get_slot_value(handler_input, "vaultName")
        service = ask_utils.request_util.get_slot_value(handler_input, "service")
        username = ask_utils.request_util.get_slot_value(handler_input, "username")
        password = ask_utils.request_util.get_slot_value(handler_input, "password")
        
        deleteSQL = "DELETE FROM " + vault + " WHERE SERVICE=%s AND USERNAME=%s AND PASSWORD=%s"
        cursor.execute(deleteSQL, (service,username,password))
        db.commit()
        speak_output = "Annndd drop!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can create or modify password vaults with me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(GetEntryIntentHandler())
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CreateVaultIntentHandler())
sb.add_request_handler(AddEntryIntentHandler())
sb.add_request_handler(RemoveEntryIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
