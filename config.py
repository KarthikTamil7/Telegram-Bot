import os
import logging

class Config:

    CAPTION = os.environ.get("CAPTION", "")
    LIMIT = int(os.environ.get("LIMIT", "25000"))
    SKIP_NO = int(os.environ.get("SKIP_NO", "0"))
    FILTER_TYPE = os.environ.get("FILTER_TYPE", "")
