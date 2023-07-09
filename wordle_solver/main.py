from collections import defaultdict
import json
from operator import itemgetter
from random import sample
from tqdm import tqdm


NROWS = 6
NCOLS = 5


def read_json(fname: str) -> list[str]:
    with open(fname, "r") as f:
        return json.load(f)


def match_green(word: str, green: list[tuple[int, str]]) -> bool:
    return all(word[idx] == letter for idx, letter in green)


def match_black(
    word: str, black: list[tuple[int, str]], free_indices: list[int]
) -> bool:
    return all(
        letter not in itemgetter(*free_indices)(word) for _, letter in black
    )


def match_yellow(
    word: str, yellow: list[tuple[int, str]], free_indices: list[int]
) -> bool:
    return all(
        word[idx] != letter and letter in itemgetter(*free_indices)(word)
        for idx, letter in yellow
    )


def get_num_words(words: list[str], green, yellow, black, free_indices) -> int:
    return len(
        [
            word
            for word in words
            if match_green(word, green)
            and match_black(word, black, free_indices)
            and match_yellow(word, yellow, free_indices)
        ]
    )


def get_words_entropies(words: list[str]):
    # if we take a guess, we have 3^5 = 243 possible arrangements of colors
    buckets = defaultdict(int)
    word = "salet"
    for to_guess in tqdm(words):
        green = []
        black = []
        yellow = []
        for i in range(NCOLS):
            free_indices = [
                j for j in [0, 1, 2, 3, 4] if j not in [g[0] for g in green]
            ]
            if word[i] == to_guess[i]:
                green.append((i, word[i]))
            elif len(free_indices) > 0 and word[i] in itemgetter(
                *free_indices
            )(to_guess):
                yellow.append((i, word[i]))
            elif len(free_indices) > 0 and word[i] not in itemgetter(
                *free_indices
            )(to_guess):
                black.append((i, word[i]))
        n = get_num_words(words, green, yellow, black, free_indices)
        buckets[word] += n / len(words)
    print(sorted(buckets.items(), key=lambda x: x[1], reverse=True))
    exit()
    # tares leaves 287.795 words on average after the first guess
    # TODO: find a word that after the guess, we limit number of words to guess by maximum


def main() -> int:
    words = read_json("words.json")
    print(
        """Tutorial:
    Write a 5-letter string of b, y or g, where each letter
    is a color you got on wordle guess."""
    )
    WORD = ["" for _ in range(NCOLS)]
    print(len(words))
    words_entropies = get_words_entropies(words)
    while True:
        word = sample(words, 1)[0]
        print(f"guess: {word}")
        print(f"Words left: {len(words)}")
        inp = input()
        assert len(inp) == NCOLS
        black, yellow, green = [], [], []
        for idx, (color, letter) in enumerate(zip(inp, word)):
            assert color.lower() in "byg"
            match color.lower():
                case "b":
                    black.append(letter)
                case "y":
                    yellow.append((idx, letter))
                case "g":
                    green.append((idx, letter))
        for idx, letter in green:
            WORD[idx] = letter
        filtered_words = []
        for word in words:
            match = all(word[idx] == letter for idx, letter in green)
            if match:
                filtered_words.append(word)
        words = filtered_words[:]
        filtered_words = []
        free_indices = [idx for idx, letter in enumerate(WORD) if letter == ""]
        if len(black) > 0:
            for word in words:
                match = not any(
                    b in itemgetter(*[i for i in free_indices])(word)
                    for b in black
                )
                if match:
                    filtered_words.append(word)
        words = filtered_words[:]
        filtered_words = []
        if len(yellow) > 0:
            for word in words:
                match = all(
                    word[idx] != letter
                    and letter in itemgetter(*[i for i in free_indices])(word)
                    for idx, letter in yellow
                )
                if match:
                    filtered_words.append(word)
            words = filtered_words[:]
        if len(words) == 1:
            print(f"Guess: {words[0]}")
            break
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
