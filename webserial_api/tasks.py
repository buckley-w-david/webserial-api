from flask import current_app

import webserial  # type: ignore
from webserial.fff import FanFicFare  # type: ignore
from webserial.calibredb import CalibreDb  # type: ignore
from webserial.config import WebserialConfig  # type: ignore


def submit_story(story_url: str, user: str, password: str, library: str):
    calibredb = CalibreDb(user, password, library)
    fanficfare = FanFicFare()
    webserial.perform(calibredb, fanficfare, [story_url])


def delete_story(story_id: int, user: str, password: str, library: str):
    query = f"Identifiers:url:https://www.royalroad.com/fiction/{story_id}"
    calibredb = CalibreDb(user, password, library)
    results = calibredb.search(query)
    if results:
        calibredb.remove(results[0])
