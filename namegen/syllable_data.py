# namegen/syllable_data.py
"""
Dados fonéticos usados pelos geradores: línguas, sílabas iniciais (onsets),
sílabas finais (codas) e mapeamento raça → língua.
"""
from typing import Dict, List, Optional, Tuple

# ============================================================
# LÍNGUAS
# ============================================================

LANGUAGES: Dict[str, Dict] = {
    "orcish": {
        "name": "Djolgronin",
        "vowels": ["a", "o", "u", "u", "a", "ra"],
        "consonants": ["g", "k", "r", "z", "sh", "gr", "kr", "th", "d", "b", "m"],
        "suffixes": {
            "personal": ["ash", "uk", "og", "rak", "gul", "mok"],
            "family": ["skull", "fang", "gor", "rak", "bash", "maw"],
            "place": ["gash", "durz", "mor", "krag", "lug"],
        },
        "examples": ["Grommash", "Thrall", "Gorbag", "Shagrat", "Azog", "Ugluk", "Durotan", "Garrosh"],
    },
    "elvish": {
        "name": "Elgaran",
        "vowels": ["a", "e", "i", "ae", "ia", "ie", "o"],
        "consonants": ["l", "r", "n", "th", "s", "v", "nd", "lv", "ss", "m", "f"],
        "suffixes": {
            "personal": ["iel", "wen", "dril", "las", "ion", "ael"],
            "family": ["dorei", "thalas", "siel", "vanya", "loth", "nore"],
            "place": ["ost", "dor", "lond", "nor", "ithil", "wen"],
        },
        "examples": ["Legolas", "Galadriel", "Elrond", "Arwen", "Thranduil", "Celeborn", "Finrod", "Luthien"],
    },
    "dwarvish": {
        "name": "Dornval",
        "vowels": ["a", "o", "u", "i", "ai", "e"],
        "consonants": ["d", "r", "n", "b", "g", "k", "th", "rn", "rg", "l", "m"],
        "suffixes": {
            "personal": ["in", "ur", "ain", "rim", "dur", "ek"],
            "family": ["forge", "hammer", "beard", "stone", "helm", "bar"],
            "place": ["heim", "dum", "baraz", "zad", "hold"],
        },
        "examples": ["Thorin", "Gimli", "Balin", "Dwalin", "Durin", "Bofur", "Gloin", "Dain"],
    },
    "common": {
        "name": "Istralino",
        "vowels": ["a", "e", "i", "o", "u", "ia"],
        "consonants": ["r", "n", "l", "d", "m", "s", "t", "c", "v", "br", "dr"],
        "suffixes": {
            "personal": ["ric", "an", "mund", "el", "on", "ard"],
            "family": ["wood", "ford", "stone", "well", "brook", "son"],
            "place": ["ton", "ford", "burg", "wick", "dale", "shire"],
        },
        "examples": ["Aldric", "Roland", "Edmund", "Marian", "Gareth", "Beatrice", "Tristan", "Elena"],
    },
    "sylvan": {
        "name": "Aoslin",
        "vowels": ["i", "e", "a", "ee", "y", "ia"],
        "consonants": ["l", "f", "s", "w", "p", "n", "th", "v", "r", "ph"],
        "suffixes": {
            "personal": ["wyn", "lee", "bell", "ri", "sy", "ith"],
            "family": ["dew", "bloom", "thistle", "glimmer", "leaf", "moth"],
            "place": ["glade", "hollow", "mere", "dell", "wyld"],
        },
        "examples": ["Titania", "Oberon", "Puck", "Peaseblossom", "Mab", "Fennwyn", "Liriel", "Sylphie"],
    },
    "draconic": {
        "name": "Vethrix",
        "vowels": ["a", "e", "i", "o", "y", "ae"],
        "consonants": ["x", "th", "r", "k", "v", "z", "sv", "gh", "dr", "l"],
        "suffixes": {
            "personal": ["thrax", "nax", "rion", "vyr", "gos", "xis"],
            "family": ["kethend", "vorel", "turrok", "ixen", "zaroth"],
            "place": ["vax", "thrix", "oth", "kar", "drak"],
        },
        "examples": ["Smaug", "Ancalagon", "Tiamat", "Bahamut", "Vermithrax", "Alduin", "Glaurung", "Paarthurnax"],
    },
    "infernal": {
        "name": "Xarveth",
        "vowels": ["a", "e", "o", "u", "ae", "y"],
        "consonants": ["z", "b", "l", "m", "ph", "s", "x", "g", "r", "ch"],
        "suffixes": {
            "personal": ["oth", "zel", "mon", "goth", "rax", "ial"],
            "family": ["bael", "moloch", "azar", "ruin", "vex"],
            "place": ["gehen", "dis", "phleg", "abyss", "styx"],
        },
        "examples": ["Asmodeus", "Mephisto", "Baalzebul", "Belial", "Zariel", "Malphas", "Orcus", "Azazel"],
    },
    "beastial": {
        "name": "Feran",
        "vowels": ["a", "o", "u", "ar", "e"],
        "consonants": ["r", "w", "g", "h", "k", "f", "rr", "sk", "t", "n"],
        "suffixes": {
            "personal": ["fang", "claw", "maw", "rok", "hra", "wulf"],
            "family": ["pelt", "howl", "mane", "tusk", "talon"],
            "place": ["den", "lair", "pack", "rock", "hunt"],
        },
        "examples": ["Rakash", "Ghorra", "Warrok", "Sharrkan", "Huragok", "Fenrir", "Akela", "Shere"],
    },
    "halfling": {
        "name": "Brambel",
        "vowels": ["a", "e", "i", "o", "u", "y"],
        "consonants": ["b", "m", "p", "r", "l", "n", "d", "w", "t", "s", "bb", "ll"],
        "suffixes": {
            "personal": ["in", "bo", "wise", "lin", "doc", "win", "ina", "ma"],
            "family": ["foot", "burrow", "bottle", "gold", "brook", "hill", "barrel"],
            "place": ["ton", "wick", "bel", "hill", "dale", "brook"],
        },
        "examples": ["Perrin", "Tumnus", "Peregrin", "Samwise", "Bilbo", "Meriadoc", "Marigold", "Willow"],
    },
    "gnomish": {
        "name": "Fizzwick",
        "vowels": ["i", "e", "a", "o", "y", "ee"],
        "consonants": ["z", "zz", "b", "m", "bl", "g", "dg", "t", "n", "ck", "w", "p", "sp", "gl"],
        "suffixes": {
            "personal": ["wick", "bit", "ble", "ker", "ette", "elle", "ina", "y"],
            "family": ["gear", "sprocket", "cog", "whistle", "spark", "bolt", "fuse"],
            "place": ["ton", "burgo", "wick", "glade", "peak", "brook", "hill"],
        },
        "examples": ["Fizzwick", "Bimble", "Tinker", "Glimbrin", "Gadger", "Cogswell", "Wrenna", "Sparkle"],
    },
}

# ============================================================
# SÍLABAS INICIAIS (ONSETS) — início do nome
# ============================================================

ONSET_SYLLABLES: Dict[str, List[str]] = {
    "orcish": ["Gr", "Kr", "Ug", "Az", "Sh", "Th", "Gor", "Mug", "Dur", "Bol", "Zug", "Rag"],
    "elvish": ["Ae", "El", "Gal", "Leg", "Thr", "Cel", "Fin", "Lu", "Ar", "Syl", "Ith", "Fae"],
    "dwarvish": ["Th", "Gim", "Bal", "Dw", "Dur", "Bof", "Gl", "Da", "Thr", "Kil", "Bor", "Har"],
    "common": ["Al", "Ro", "Ed", "Mar", "Gar", "Be", "Tris", "El", "Wil", "Hen", "Ja", "Ka"],
    "sylvan": ["Ti", "Ob", "Pe", "Fen", "Li", "Syl", "Wi", "Bri", "Pip", "Fae", "Ny", "Ely"],
    "draconic": ["Sm", "Anc", "Ti", "Ba", "Ver", "Al", "Gl", "Pa", "Vy", "Kh", "Xa", "Dra"],
    "infernal": ["As", "Me", "Ba", "Be", "Za", "Mal", "Or", "Az", "Mo", "Ly", "Ne", "Ab"],
    "beastial": ["Ra", "Gho", "Wa", "Sha", "Hu", "Fe", "Ak", "Gr", "Ka", "Ur", "Tor", "Ho"],
    "halfling": ["Bram", "Tum", "Per", "Wil", "Cor", "Ned", "Bob", "Pip", "Tom", "Sam", "Bil", "Mer"],
    "gnomish": ["Fizz", "Bim", "Tin", "Wren", "Glim", "Pip", "Gad", "Cog", "Spark", "Zip", "Nim", "Bix"],
}

# ============================================================
# SÍLABAS FINAIS (CODAS)
# ============================================================

CODA_SYLLABLES: Dict[str, List[str]] = {
    "orcish": ["k", "g", "sh", "z", "rk", "th"],
    "elvish": ["l", "n", "s", "th", "nd", "r"],
    "dwarvish": ["n", "r", "k", "m", "rn", "d"],
    "common": ["n", "d", "c", "l", "s", "t"],
    "sylvan": ["n", "l", "s", "th", "f", ""],
    "draconic": ["x", "th", "s", "n", "r", "g"],
    "infernal": ["s", "l", "th", "x", "n", "b"],
    "beastial": ["r", "k", "sh", "g", "rr", "f"],
    "halfling": ["n", "m", "l", "r", "d", ""],
    "gnomish": ["k", "x", "t", "n", "s", ""],
}

# ============================================================
# RAÇA → LÍNGUA
# ============================================================

RACE_TO_LANGUAGE: Dict[str, str] = {
    "orc": "orcish",
    "goblin": "orcish",
    "elf": "elvish",
    "dwarf": "dwarvish",
    "gnome": "gnomish",
    "human": "common",
    "halfling": "halfling",
    "fae": "sylvan",
    "dragon": "draconic",
    "daemon": "infernal",
    "beastfolk": "beastial",
}

# Nomes de raça em português (usados nos bancos .csv) → nome interno
RACE_ALIASES: Dict[str, str] = {
    "elfo": "elf",
    "anao": "dwarf",
    "anão": "dwarf",
    "gnomo": "gnome",
    "humano": "human",
    "dragao": "dragon",
    "dragão": "dragon",
    "demonio": "daemon",
    "demônio": "daemon",
    "povo-bicho": "beastfolk",
    "povo-fera": "beastfolk",
}

# Outros nomes pelos quais cada língua é conhecida (ex.: nos bancos .csv).
# O nome exibido ("name" em LANGUAGES) também é aceito automaticamente.
LANGUAGE_ALIASES: Dict[str, str] = {}


def normalize_race(race: str) -> str:
    """Converte nomes em português/variações para o nome interno da raça."""
    race = race.strip().lower()
    return RACE_ALIASES.get(race, race)


def language_for_race(race: str) -> Optional[str]:
    """Língua de uma raça (aceita nomes em português), ou None."""
    return RACE_TO_LANGUAGE.get(normalize_race(race))


def resolve_language(name: str) -> Optional[str]:
    """Aceita a chave interna, o nome exibido ou um apelido da língua."""
    name = name.strip().lower()
    if name in LANGUAGES:
        return name
    for key, data in LANGUAGES.items():
        if data["name"].lower() == name:
            return key
    return LANGUAGE_ALIASES.get(name)

# ============================================================
# PADRÕES DE TAMANHO (mín., máx. de sílabas)
# ============================================================

NAME_LENGTH_PATTERNS: Dict[str, Tuple[int, int]] = {
    "short": (1, 2),
    "medium": (2, 3),
    "long": (3, 4),
}
