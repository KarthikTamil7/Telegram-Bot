import os
import logging

class Config:

    CAPTION = os.environ.get("CAPTION", "")
    LIMIT = int(os.environ.get("LIMIT", "25000"))
    SKIP_NO = int(os.environ.get("SKIP_NO", "0"))
    FILTER_TYPE = os.environ.get("FILTER_TYPE", "")

    # FOR AUTOMATICALLY FORWARDING MESSAGES
    FROM_CHATS = [-1001234704297]  # List of chat id's to forward messages from
    TO_CHATS = [-1001128355490]  # List of chat id's to forward messages to
