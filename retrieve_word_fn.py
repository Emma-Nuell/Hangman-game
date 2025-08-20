# import requests
import requests
import random
from requests.exceptions import RequestException
from typing import Optional

WORD_API: str = "https://random-word-api.herokuapp.com/word?"


LOCAL_WORDS: dict[int, list[str]] = {
    4: ["book", "tree", "fish", "door"],
    5: [
        "apple",
        "beach",
        "crisp",
        "dwarf",
        "eagle",
        "flame",
        "grape",
        "honey",
        "igloo",
        "jolly",
        "koala",
        "lemon",
        "mango",
        "noble",
        "olive",
        "peach",
        "queen",
        "river",
        "sunny",
        "tiger",
    ],
    6: [
        "banana",
        "camera",
        "dancer",
        "earthy",
        "floral",
        "guitar",
        "hiking",
        "island",
        "jacket",
        "kitten",
        "lizard",
        "marble",
        "nectar",
        "orange",
        "pepper",
        "quasar",
        "rocket",
        "sunset",
        "turtle",
        "velvet",
    ],
    7: [
        "bicycle",
        "kitchen",
        "giraffe",
        "diamond",
        "airport",
        "balloon",
        "captain",
        "dolphin",
        "elephant",
        "freedom",
        "gallery",
        "harmony",
        "jackpot",
        "laptop",
        "mystery",
    ],
    10: [
        "butterfly",
        "chocolate",
        "discovery",
        "earthquake",
        "friendship",
        "generation",
        "helicopter",
        "impressive",
        "jazzercise",
        "kindergarten",
        "lighthouse",
        "motivation",
        "notorious",
        "outstanding",
        "passionate",
    ],
    11: [
        "adventurous",
        "breakthrough",
        "celebration",
        "demonstrate",
        "extraordinary",
        "fascinating",
        "grandfather",
        "handsome",
        "inspiration",
        "justification",
        "knowledgeable",
        "magnificent",
        "nevertheless",
        "opportunity",
        "performance",
    ],
    12: [
        "acknowledged",
        "breathtaking",
        "communication",
        "determination",
        "entertainment",
        "fountainhead",
        "governmental",
        "hypothetical",
        "intelligence",
        "jurisdiction",
        "kaleidoscope",
        "laboriously",
        "mathematical",
        "neighborhood",
        "overwhelming",
    ],
    14: [
        "accountability",
        "bibliographical",
        "characteristic",
        "discrimination",
        "environmental",
        "fundamentalist",
        "hospitalization",
        "individuality",
        "jurisprudential",
        "knowledgeability",
        "lexicographer",
        "metamorphosis",
        "neurobiological",
        "organizational",
        "personification",
    ],
    13: [
        "astonishingly",
        "breathtakingly",
        "comfortability",
        "disappointing",
        "extraordinary",
        "fascinatingly",
        "grandstanding",
        "hallucination",
        "inconvenience",
        "jurisprudence",
        "kindheartedly",
        "lackadaisical",
        "mischievously",
        "nevertheless",
        "overwhelmingly",
        "paradoxically",
        "questioningly",
        "revolutionary",
        "sophisticated",
        "troubleshooting",
    ],
}


def retrieve_word(length: int = 10) -> Optional[str]:
    if length > 14 or length <= 3:
        raise ValueError("length parameter must be below 14 and greater than 3")
    try:
        response: requests.Response = requests.get(
            f"{WORD_API}length={length}", timeout=7
        )
        response.raise_for_status()
        return response.json()[0]
    except (RequestException, ValueError, IndexError):
        return get_local_word(length)


def get_local_word(length: int) -> str:
    """Get a random word from local cache with length validation."""
    if length in LOCAL_WORDS:
        return random.choice(LOCAL_WORDS[length])
    raise ValueError(f"No words available for length {length}")
